# Notes

## Intuition
Right rotation by k is equivalent to reversing parts of the array. If I reverse the first portion, then the remaining portion, and finally the entire array, the elements end up in the right rotated order. This is a clever trick that works in-place with O(1) extra space. Also need to handle k > n by taking k %= n.

## Approach
1. Get array length `n`. If `n == 0`, return early.
2. Normalize `k` with `k %= n` (handles cases where k > n).
3. Convert right rotation to left rotation by setting `k = n - k`.
4. Define a helper `reverse(start, end)` that swaps elements from the two ends inward.
5. Reverse the first `k` elements: `reverse(0, k - 1)`.
6. Reverse the remaining elements: `reverse(k, n - 1)`.
7. Reverse the entire array: `reverse(0, n - 1)`.

## Time Complexity
**O(n)** — Each element is swapped exactly twice (once in a partial reverse, once in the full reverse).

## Space Complexity
**O(1)** — All operations are done in-place with no extra arrays.

## Mistakes
- Initially tried to rotate by shifting elements one by one, which is O(n*k) — too slow.
- Forgot the `k %= n` normalization and got index errors for k > n.
- The reversal logic took a minute to reason through; had to trace with a small example.

## Revision Date
July 11, 2026
