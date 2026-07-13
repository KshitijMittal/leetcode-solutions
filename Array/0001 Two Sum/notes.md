# Notes

## Intuition
When I first saw this problem, I immediately thought of using a hash map to track numbers I've already seen. Since we need to find two numbers that sum to a target, for each number we can check if its complement (target - num) has already appeared. This avoids the brute force O(n²) nested loop approach.

## Approach
1. Initialize an empty dictionary `seen` to store each number and its index.
2. Iterate through the array using a loop with index `i`.
3. For each element `nums[i]`, compute `needed = target - nums[i]`.
4. Check if `needed` exists in the `seen` dictionary.
   - If yes, return `[seen[needed], i]` as the answer.
   - If no, store `nums[i]` with its index `i` in the dictionary.
5. Since the problem guarantees exactly one solution, we'll always find it before the loop ends.

## Time Complexity
**O(n)** — We traverse the array once. Each dictionary lookup/insertion is O(1) on average.

## Space Complexity
**O(n)** — In the worst case, we store up to n-1 elements in the dictionary before finding the pair.

## Mistakes
- Initially forgot to check the edge case where the complement equals the current number at the same index — but since we only check against previously stored elements, this is naturally handled.
- Almost used a brute-force double loop first, which is unnecessary.

## Revision Date
July 11, 2026
