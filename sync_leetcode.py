import os
import requests
import json
import re

LEETCODE_SESSION = os.environ.get("LEETCODE_SESSION")
USERNAME = os.environ.get("LEETCODE_USERNAME")

if not LEETCODE_SESSION or not USERNAME:
    print("Missing secrets. Please set LEETCODE_SESSION and LEETCODE_USERNAME.")
    exit(1)

GRAPHQL_URL = "https://leetcode.com/graphql/"

# Create a session to handle cookies automatically
session = requests.Session()
session.cookies.set("LEETCODE_SESSION", LEETCODE_SESSION, domain=".leetcode.com")

# Fetch CSRF token by visiting the homepage
print("Fetching CSRF token...")
res = session.get("https://leetcode.com/")
csrf_token = session.cookies.get("csrftoken")

if not csrf_token:
    print("Warning: Could not retrieve CSRF token. The script might fail to fetch code.")

HEADERS = {
    "Content-Type": "application/json",
    "Referer": "https://leetcode.com",
    "Origin": "https://leetcode.com",
    "x-csrftoken": csrf_token
}

# Language mapping to file extensions
LANG_EXT = {
    "python": "py", "python3": "py", "cpp": "cpp", "java": "java",
    "javascript": "js", "typescript": "ts", "c": "c", "csharp": "cs",
    "ruby": "rb", "swift": "swift", "golang": "go", "kotlin": "kt"
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
    response = session.post(GRAPHQL_URL, json={"query": query, "variables": variables}, headers=HEADERS)
    if response.status_code != 200:
        # Improved error message to see exactly what LeetCode complained about
        raise Exception(f"Query failed: {response.status_code} - {response.text}")
    return response.json()

def get_recent_submissions(limit=20):
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
    data = graphql_request(query, {"username": USERNAME, "limit": limit})
    return data.get("data", {}).get("recentAcSubmissionList", [])

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
    return data.get("data", {}).get("question", {})

def get_submission_code(submission_id):
    query = """
    query submissionDetails($submissionId: ID!) {
      submissionDetails(submissionId: $submissionId) {
        code
      }
    }
    """
    data = graphql_request(query, {"submissionId": str(submission_id)})
    return data.get("data", {}).get("submissionDetails", {}).get("code", "")

def clean_html(html):
    # Very basic HTML to text conversion for README
    text = re.sub('<[^<]+?>', '', html)
    return text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&#39;', "'")

def main():
    print("Fetching recent submissions...")
    submissions = get_recent_submissions(20)

    if not submissions:
        print("No submissions found or failed to fetch.")
        return

    for sub in submissions:
        slug = sub["titleSlug"]
        title = sub["title"]
        sub_id = sub["id"]
        lang = sub["lang"]

        # Check if folder already exists to avoid duplicate work
        # A quick check to see if any folder starts with the slug or title
        if os.path.exists(slug):
            print(f"Skipping {title} (already exists).")
            continue

        print(f"Processing: {title}")

        # Fetch details and code
        details = get_problem_details(slug)
        code = get_submission_code(sub_id)

        if not details or not code:
            print(f"Could not fetch details/code for {title}. Skipping.")
            continue

        q_id = details["questionId"].zfill(4)
        difficulty = details["difficulty"]
        tags = [tag["name"] for tag in details["topicTags"]]
        description = clean_html(details["content"])

        # Determine parent folder (use first tag, fallback to 'Misc')
        parent_folder = tags[0] if tags else "Misc"
        problem_folder = f"{q_id} {title.replace('/', '-')}"
        path = os.path.join(parent_folder, problem_folder)

        os.makedirs(path, exist_ok=True)

        # 1. Create Solution file
        ext = LANG_EXT.get(lang, "txt")
        with open(os.path.join(path, f"solution.{ext}"), "w", encoding="utf-8") as f:
            f.write(code)

        # 2. Create README.md
        readme_content = f"# {q_id}. {title}\n\n"
        readme_content += f"**Difficulty:** {difficulty}\n\n"
        readme_content += f"**Tags:** {', '.join(tags)}\n\n"
        readme_content += "## Description\n\n"
        readme_content += description + "\n"

        with open(os.path.join(path, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)

        # 3. Create notes.md
        with open(os.path.join(path, "notes.md"), "w", encoding="utf-8") as f:
            f.write(NOTES_TEMPLATE)

    print("Sync complete!")

if __name__ == "__main__":
    main()