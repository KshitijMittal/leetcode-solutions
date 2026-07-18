# Notes

## Intuition
The simplest way to detect duplicates is to track elements I've already seen. A hash set gives O(1) lookups and insertions, so I can iterate through the array once and check if each element is already in the set. If it is, we have a duplicate.

## Approach
1. Initialize an empty set `hashset`.
2. Iterate through each `num` in `nums`:
   - If `num` is already in `hashset`, return `True` (duplicate found).
   - Otherwise, add `num` to the set.
3. If the loop completes without finding duplicates, return `False`.

## Time Complexity
**O(n)** — Single pass through the array. Set operations are O(1) on average.

## Space Complexity
**O(n)** — In the worst case (no duplicates), we store all n elements in the set.

## Mistakes
- Initially considered sorting first (O(n log n)), but the hash set approach is more efficient.
- Almost forgot that the problem allows any value to appear at least twice — so returning on the first duplicate is correct.

## Revision Date
July 11, 2026
