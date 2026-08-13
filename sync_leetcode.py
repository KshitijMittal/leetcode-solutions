import html
import json
import os
import re
import sys
import time

import requests

LEETCODE_SESSION = os.environ.get("LEETCODE_SESSION")
USERNAME = os.environ.get("LEETCODE_USERNAME")

if not LEETCODE_SESSION or not USERNAME:
    print("Missing secrets. Please set LEETCODE_SESSION and LEETCODE_USERNAME.")
    exit(1)

GRAPHQL_URL = "https://leetcode.com/graphql/"

# Keeps a record of already-synced submission IDs so the script can detect
# (and warn about) submissions that fall outside the API's fetch window.
# Committed to the repo so every Action run shares the same state.
STATE_FILE = ".sync_state.json"

# Create a session that keeps cookies (incl. CSRF token) automatically.
session = requests.Session()
session.cookies.set("LEETCODE_SESSION", LEETCODE_SESSION, domain=".leetcode.com")
session.headers.update(
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
)

# Fetch the CSRF token by visiting the homepage (retry once).
# If it can't be fetched, it usually means LEETCODE_SESSION is expired.
print("Fetching CSRF token...")
csrf_token = None
for attempt in range(2):
    try:
        session.get("https://leetcode.com/", timeout=30)
        csrf_token = session.cookies.get("csrftoken")
        if csrf_token:
            break
    except requests.RequestException as exc:
        print(f"  Homepage fetch attempt {attempt + 1} failed: {exc}")

if not csrf_token:
    print(
        "WARNING: Could not retrieve CSRF token. This usually means your "
        "LEETCODE_SESSION cookie is expired - update the secret in "
        "Settings > Secrets and variables > Actions and re-run."
    )

HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "Origin": "https://leetcode.com",
    "x-csrftoken": csrf_token,
}

# Language -> file extension. Unknown languages fall back to .txt instead of
# crashing the whole sync.
LANG_EXT = {
    "python": "py", "python3": "py", "pypy3": "py", "pandas": "py",
    "cpp": "cpp", "c": "c", "csharp": "cs",
    "java": "java", "javascript": "js", "typescript": "ts",
    "ruby": "rb", "swift": "swift", "golang": "go", "kotlin": "kt",
    "rust": "rs", "mysql": "sql", "mssql": "sql", "oraclesql": "sql",
    "dart": "dart", "scala": "scala", "php": "php", "bash": "sh",
    "erlang": "erl", "elixir": "ex", "racket": "rkt", "perl": "pl",
    "haskell": "hs", "lua": "lua", "r": "r",
}

NOTES_TEMPLATE = """# Notes

## Intuition
<!-- What did you initially think about when seeing this problem? -->

## Approach
<!-- Outline your step-by-step approach. -->

## Time Complexity
<!-- O(?) -->

## Space Complexity
<!-- O(?) -->

## Mistakes
<!-- Any edge cases you missed or bugs you ran into? -->

## Revision Date
<!-- Update this when you revisit the problem -->
"""


def graphql_request(query, variables):
    """POST a GraphQL query and raise a clear error if LeetCode rejects it."""
    response = session.post(
        GRAPHQL_URL,
        json={"query": query, "variables": variables},
        headers=HEADERS,
        timeout=30,
    )
    if response.status_code != 200:
        raise Exception(f"Query failed: {response.status_code} - {response.text[:500]}")

    try:
        data = response.json()
    except ValueError:
        raise Exception(
            "LeetCode returned an unexpected (non-JSON) response - usually a "
            "login or block page. Check that LEETCODE_SESSION is still valid.\n"
            f"{response.text[:300]}"
        )

    # LeetCode answers with HTTP 200 + "data": null + "errors" when the request
    # is rejected (e.g. expired session). Surface that clearly.
    if data.get("data") is None or data.get("errors"):
        errors = data.get("errors") or []
        message = "; ".join(str(e.get("message", e)) for e in errors) or "unknown error"
        lowered = message.lower()
        if any(
            word in lowered
            for word in (
                "not logged in",
                "unauthorized",
                "authentication",
                "login required",
                "session",
            )
        ):
            raise Exception(
                f"LeetCode rejected the request: {message} - your "
                "LEETCODE_SESSION is likely expired. Update the secret "
                "(Settings > Secrets and variables > Actions > LEETCODE_SESSION) "
                "and re-run."
            )
        raise Exception(f"LeetCode GraphQL error: {message}")

    return data


def verify_username():
    """Fail fast if the configured username doesn't resolve on LeetCode.

    The profile query is public data, so it works regardless of session state.
    A clean response means the username is valid; any error means the secret
    is wrong.
    """
    query = """
    query userPublicProfile($username: String!) {
      matchedUser(username: $username) {
        username
      }
    }
    """
    data = graphql_request(query, {"username": USERNAME})
    matched = (data.get("data") or {}).get("matchedUser")
    if not matched:
        raise Exception(
            f"Username '{USERNAME}' was not found on LeetCode. "
            "Check the LEETCODE_USERNAME secret."
        )


def fetch_recent_submissions():
    """Fetch accepted submissions, merging two endpoints to widen the net.

    - recentSubmissionList: up to 50 recent submissions of ANY status.
    - recentAcSubmissionList: up to 20 recent accepted submissions.

    LeetCode silently returns an empty list for both when the session cookie
    is invalid, which is why we verify the session separately (see main()).
    """
    submissions = {}

    try:
        query = """
        query recentSubmissionList($username: String!, $limit: Int!) {
          recentSubmissionList(username: $username, limit: $limit) {
            id
            title
            titleSlug
            timestamp
            statusDisplay
            lang
          }
        }
        """
        data = graphql_request(query, {"username": USERNAME, "limit": 50})
        for sub in (data.get("data") or {}).get("recentSubmissionList") or []:
            if (sub.get("statusDisplay") or "") == "Accepted":
                submissions[sub["id"]] = sub
    except Exception as exc:
        print(f"  recentSubmissionList query failed ({exc}); using recentAcSubmissionList only")

    try:
        query = """
        query recentAcSubmissions($username: String!, $limit: Int!) {
          recentAcSubmissionList(username: $username, limit: $limit) {
            id
            title
            titleSlug
            timestamp
            lang
          }
        }
        """
        data = graphql_request(query, {"username": USERNAME, "limit": 20})
        for sub in (data.get("data") or {}).get("recentAcSubmissionList") or []:
            submissions[sub["id"]] = sub
    except Exception as exc:
        print(f"  recentAcSubmissionList query failed ({exc})")

    return sorted(
        submissions.values(),
        key=lambda s: int(s.get("timestamp") or 0),
        reverse=True,
    )


def get_submission_calendar():
    """Per-day submission counts (UTC midnight -> count) for the past year.

    This is public data and keeps working even after the session expires,
    which lets us tell "no recent solves" apart from "session died".
    """
    query = """
    query userProfileCalendar($username: String!, $year: Int) {
      matchedUser(username: $username) {
        userCalendar(year: $year) {
          submissionCalendar
        }
      }
    }
    """
    data = graphql_request(query, {"username": USERNAME})
    user_calendar = ((data.get("data") or {}).get("matchedUser") or {}).get("userCalendar") or {}
    raw = user_calendar.get("submissionCalendar") or "{}"
    try:
        return json.loads(raw)
    except ValueError:
        return {}


def has_recent_calendar_activity(days=7):
    """True if the public calendar shows any submission within `days` days."""
    calendar = get_submission_calendar()
    if not calendar:
        return False
    cutoff = time.time() - days * 86400
    return any(int(ts) >= cutoff and count > 0 for ts, count in calendar.items())


def get_problem_details(title_slug):
    query = """
    query questionData($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        difficulty
        content
        topicTags { name }
      }
    }
    """
    data = graphql_request(query, {"titleSlug": title_slug})
    return (data.get("data") or {}).get("question") or {}


def get_submission_code(submission_id):
    query = """
    query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) {
        code
      }
    }
    """
    data = graphql_request(query, {"submissionId": int(submission_id)})
    submission = (data.get("data") or {}).get("submissionDetails") or {}
    return submission.get("code") or ""


def clean_html(html_text):
    if not html_text:
        return ""
    text = re.sub(r"<[^>]+>", "", html_text)
    return html.unescape(text)


def sanitize_title(title):
    """Make a problem title safe to use as a folder name on any OS
    (the repo is also pulled locally on Windows)."""
    safe = re.sub(r'[<>:"/\\|?*]', "-", title)
    safe = safe.strip().rstrip(". ")
    return safe or "Problem"


def write_readme_and_notes(path, q_id, title, tags, details):
    difficulty = details.get("difficulty", "Unknown")
    description = clean_html(details.get("content"))
    readme_content = f"# {q_id}. {title}\n\n"
    readme_content += f"**Difficulty:** {difficulty}\n\n"
    readme_content += f"**Tags:** {', '.join(tags)}\n\n"
    readme_content += "## Description\n\n"
    readme_content += description + "\n"
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    with open(os.path.join(path, "notes.md"), "w", encoding="utf-8") as f:
        f.write(NOTES_TEMPLATE)


def process_submission(sub):
    """Handles one accepted submission.

    Returns one of: 'created', 'updated', 'skipped'.
    README.md and notes.md are only ever written for brand-new problems, so
    your personal notes are never overwritten.
    """
    title = (sub or {}).get("title", "Unknown")
    slug = (sub or {}).get("titleSlug")
    sub_id = (sub or {}).get("id")
    lang = (sub or {}).get("lang", "").lower()

    if not slug or not sub_id:
        print(f"Skipping submission with missing data: {title}")
        return "skipped"

    details = get_problem_details(slug)
    if not details:
        print(f"Could not fetch details for {title}. Skipping.")
        return "skipped"

    q_id = str(details.get("questionId", "")).zfill(4)
    tags = [tag["name"] for tag in (details.get("topicTags") or [])]
    parent_folder = tags[0] if tags else "Misc"
    path = os.path.join(parent_folder, f"{q_id} {sanitize_title(title)}")

    ext = LANG_EXT.get(lang, "txt")
    solution_file = os.path.join(path, f"solution.{ext}")

    print(f"Processing: {title} ({lang or 'unknown language'})")

    # Fetch the submitted code for this problem.
    code = get_submission_code(sub_id)
    if not code:
        print(f"  Could not fetch code for {title}. Skipping.")
        return "skipped"

    folder_exists = os.path.exists(path)

    # Case 1: this language's solution is already stored. Fetching the code
    # lets us pick up improved re-submissions; README/notes stay untouched.
    if folder_exists and os.path.exists(solution_file):
        try:
            with open(solution_file, "r", encoding="utf-8") as f:
                existing = f.read()
        except OSError:
            existing = ""
        if existing == code:
            print(f"  Up to date - skipping {title} (solution.{ext} unchanged).")
            return "skipped"
        with open(solution_file, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"  Updated solution.{ext} (newer submission found).")
        return "updated"

    # Case 2: folder exists (solved before in another language, or a partial
    # folder left by a crashed run) -> add/fix files, keep notes untouched.
    if folder_exists:
        if not (os.path.exists(os.path.join(path, "README.md"))
                and os.path.exists(os.path.join(path, "notes.md"))):
            write_readme_and_notes(path, q_id, title, tags, details)
            print("  Recreated missing README/notes.")
        print(f"  Adding {lang} solution to existing folder (README/notes untouched).")
        with open(solution_file, "w", encoding="utf-8") as f:
            f.write(code)
        return "created"

    # Case 3: brand-new problem -> full set of files.
    write_readme_and_notes(path, q_id, title, tags, details)
    with open(solution_file, "w", encoding="utf-8") as f:
        f.write(code)
    print("  Created folder + README + notes template.")
    return "created"


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        if not isinstance(state, dict) or not isinstance(state.get("synced_submission_ids"), list):
            raise ValueError
        return state
    except (OSError, ValueError):
        return {"synced_submission_ids": []}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def main():
    print("Verifying LeetCode username...")
    try:
        verify_username()
    except Exception as exc:
        print(f"FAILED: {exc}")
        return 1

    print("Fetching recent submissions...")
    try:
        submissions = fetch_recent_submissions()
    except Exception as exc:
        # Fail fast (exit code 1 -> the GitHub Action turns red) so a stale
        # cookie is impossible to miss, instead of silently syncing nothing.
        print(f"FAILED: {exc}")
        return 1

    if not submissions:
        # LeetCode silently returns an EMPTY list for an expired session, even
        # when the user solved problems recently. The submission calendar is
        # public data, so we use it to distinguish "nothing to sync" (fine,
        # stay green) from "session died" (fail loudly -> red Action).
        if has_recent_calendar_activity(days=7):
            print(
                "FAILED: LeetCode returned no recent submissions even though your "
                "calendar shows solves within the last 7 days. This means the "
                "LEETCODE_SESSION cookie is expired. Update the secret "
                "(Settings > Secrets and variables > Actions > LEETCODE_SESSION) "
                "and re-run this workflow."
            )
            return 1
        print("No recent accepted submissions to sync.")
        return 0

    state = load_state()
    synced_ids = set(state.get("synced_submission_ids", []))
    already_synced = sum(1 for sub in submissions if str(sub.get("id")) in synced_ids)

    created = updated = skipped = failed = 0
    for sub in submissions:
        try:
            result = process_submission(sub)
            if result in ("created", "updated"):
                synced_ids.add(str(sub.get("id")))
                if result == "updated":
                    updated += 1
                else:
                    created += 1
            else:
                skipped += 1
        except Exception as exc:
            failed += 1
            print(f"ERROR processing '{sub.get('title', '?')}': {exc}")

    state["synced_submission_ids"] = sorted(synced_ids, key=int)
    save_state(state)

    print(f"Sync complete: {created} created, {updated} updated, "
          f"{skipped} skipped, {failed} failed")

    # The API only returns the ~50 most recent submissions. If the window is
    # full, older solves may be unreachable - warn so nothing is lost silently.
    if len(submissions) >= 50:
        print(
            "WARNING: the submission window is full (50+ recent submissions). "
            "If you solved more than that since the last successful sync, the "
            "oldest ones may be missing. Re-submitting them on LeetCode will "
            "pull them in."
        )
    if failed:
        print("Some problems failed to sync - check the errors above.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
