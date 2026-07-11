class Solution(object):
    def moveZeroes(self, arr):
        n = len(arr)
        if n == 0: return None

        count = 0

        for i in range(n):
            if arr[i] != 0:
                arr[i], arr[count] = arr[count], arr[i]
                count += 1
        