# Notes

## Intuition
The array is sorted, and the problem asks for O(log n) runtime — that's a dead giveaway for binary search. Instead of just searching for the target, we need to handle the case where the target isn't present and return the correct insertion position. The left pointer naturally ends up at the insertion index when the binary search terminates without finding the target.

## Approach
1. Initialize `left = 0` and `right = len(nums) - 1`.
2. While `left <= right`:
   - Calculate `mid = (left + right) // 2`.
   - If `nums[mid] == target`, return `mid`.
   - If `nums[mid] < target`, search the right half: `left = mid + 1`.
   - If `nums[mid] > target`, search the left half: `right = mid - 1`.
3. If the loop ends without finding the target, `left` is the index where the target should be inserted.

## Time Complexity
**O(log n)** — Standard binary search halves the search space each iteration.

## Space Complexity
**O(1)** — Only a few integer variables used, no extra data structures.

## Mistakes
- Almost confused whether to return `left` or `right` at the end. Debugged with a quick example: for `nums = [1,3,5,6]`, `target = 2`, the left pointer ends at 1 (correct insertion index).
- Forgot to handle the case where target is greater than all elements — but binary search still works, returning `len(nums)`.

## Revision Date
July 11, 2026
