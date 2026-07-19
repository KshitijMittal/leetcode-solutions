# Notes

## Intuition
The problem asks to move all zeros to the end while maintaining relative order of non-zero elements, in-place. A two-pointer approach works well: one pointer (`count`) tracks where the next non-zero element should go, and the other pointer (`i`) iterates through the array. Whenever we find a non-zero, we swap it to the `count` position and advance both pointers.

## Approach
1. Get array length `n`. If `n == 0`, return early.
2. Initialize `count = 0` — this marks the position to place the next non-zero element.
3. Iterate `i` from 0 to `n - 1`:
   - If `arr[i] != 0`, swap `arr[i]` with `arr[count]`, then increment `count`.
4. After the loop, all non-zero elements are at the front in their original order, and zeros are pushed to the end.

## Time Complexity
**O(n)** — Single pass through the array with O(1) swaps.

## Space Complexity
**O(1)** — All operations are done in-place with only a constant number of extra variables.

## Mistakes
- Initially tried to count zeros and overwrite the array in a second pass, which works but requires two passes. The two-pointer swap approach is cleaner and done in one pass.
- Forgot the edge case of an empty array.

## Revision Date
July 11, 2026
