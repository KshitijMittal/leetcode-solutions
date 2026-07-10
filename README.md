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

## 🧠 My Workflow

1. I solve problems directly on LeetCode.
2. The GitHub Action automatically syncs the solution and problem statement here.
3. I periodically pull the changes locally and fill out the `notes.md` template with my thought process, time/space complexity, and edge cases I might have missed.

---
*Last synced automatically via GitHub Actions.*
```