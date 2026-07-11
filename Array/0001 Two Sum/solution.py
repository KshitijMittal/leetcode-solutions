class Solution(object):
    def twoSum(self, nums, target):
        # Dictionary to store number and its index
        seen = {}

        # Traverse the array
        for i in range(len(nums)):
            needed = target - nums[i]

            # If required number is already seen, return indices
            if needed in seen:
                return [seen[needed], i]

            # Store current number with its index
            seen[nums[i]] = i