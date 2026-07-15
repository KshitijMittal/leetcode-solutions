# Notes

## Intuition
Anagrams share the exact same character frequency count. So if I create a signature for each string based on its character counts (26 letters for lowercase), all anagrams will map to the same signature. A hash map from signature → list of strings is the natural data structure to group them.

## Approach
1. Import `defaultdict(list)` for convenient grouping.
2. For each string `s` in `strs`:
   - Create a `count` array of size 26 initialized to zeros.
   - Iterate over each character `c` in `s` and increment `count[ord(c) - ord('a')]`.
   - Convert the count array to a tuple (so it's hashable) and use it as the key.
   - Append `s` to the corresponding list in the result dictionary.
3. Return all the grouped values as a list.

## Time Complexity
**O(n * k)** — Where n is the number of strings and k is the average length of each string. We iterate over each character of each string exactly once.

## Space Complexity
**O(n * k)** — We store all strings in the hash map. The count array is O(26) = O(1) per string.

## Mistakes
- Initially thought about sorting each string (O(k log k)) as the key. That works but is slower. The counting approach is more efficient.
- Forgot to use `tuple(count)` instead of `count` directly — lists aren't hashable in Python.

## Revision Date
July 11, 2026
