# 🚀 LeetCode Solutions

Welcome to my LeetCode solutions repository! This repository is a curated, automatically synced collection of my accepted LeetCode solutions, organized by data structures and algorithms.

## 📂 Repository Structure

Unlike a flat list of files, this repository is organized by **Topic Tags** to make it easier to track progress and review specific concepts.

Every problem folder contains:
- `README.md` — The full problem description, examples, and constraints (auto-generated).
- `solution.ext` — My accepted solution code in the language I solved it in.
- `notes.md` — My personal notes on intuition, approach, time/space complexity, and mistakes.

```text
LeetCode/
│
├── Arrays/
│   └── 0001 Two Sum/
│       ├── README.md
│       ├── solution.py
│       └── notes.md
│
├── Linked List/
│   └── 0206 Reverse Linked List/
│       ├── README.md
│       ├── solution.py
│       └── notes.md
│
├── Trees/
├── Graphs/
└── Dynamic Programming/
```

## 🤖 Automation Workflow

This repository is maintained entirely by a **custom GitHub Action**—no browser extensions required!

Every day, a Python script runs on GitHub's servers that:
1. Connects to the LeetCode GraphQL API.
2. Fetches my most recent accepted submissions.
3. Retrieves problem metadata (title, difficulty, description, constraints) and the exact code I submitted.
4. Automatically creates the topic folder and problem folder.
5. Generates the `README.md` and a `notes.md` template.
6. Commits and pushes the changes to this repository.

Because the script checks for existing folders, it never overwrites my personal `notes.md` once I've written in them.

The sync runs every 6 hours (00:00, 06:00, 12:00, 18:00 UTC) so solutions land in the repo the same day they're solved.

## ⚠️ Troubleshooting

If the **Sync LeetCode Solutions** Action turns **red**, it almost always means the `LEETCODE_SESSION` cookie has expired. LeetCode silently hides submissions from an invalid session, so the script fails loudly instead of pushing nothing.

1. Log in to LeetCode in your browser.
2. Open DevTools → Application → Cookies → `https://leetcode.com`.
3. Copy the value of the `LEETCODE_SESSION` cookie.
4. Update the secret at **Settings → Secrets and variables → Actions → LEETCODE_SESSION**.
5. Re-run the workflow from the Actions tab (or wait for the next scheduled run).

Missed solves are picked up automatically as long as they're within the ~50 most recent submissions; older ones can be recovered by re-submitting them on LeetCode.

## 🧠 My Workflow

1. I solve problems directly on LeetCode.
2. The GitHub Action automatically syncs the solution and problem statement here.
3. I periodically pull the changes locally and fill out the `notes.md` template with my thought process, time/space complexity, and edge cases I might have missed.

---
*Last synced automatically via GitHub Actions.*
```