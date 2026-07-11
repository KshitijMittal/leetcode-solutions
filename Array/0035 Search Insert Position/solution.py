class Solution(object):
    def searchInsert(self, nums, target):
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            # If target is found, return its index
            if nums[mid] == target:
                return mid

            # If target is greater, search right half
            elif nums[mid] < target:
                left = mid + 1

            # If target is smaller, search left half
            else:
                right = mid - 1

        return left        