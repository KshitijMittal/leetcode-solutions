class Solution(object):
    def rotate(self, arr, k):
        # length of the array
        n = len(arr)
        if n == 0: return

        # define reverse function
        def reverse(start, end):
            while start < end:
                # swap the two
                arr[start], arr[end] = arr[end], arr[start]
                start += 1
                end -= 1

        # handles if k > n
        k %= n
        # converted right rotation k to left rotation
        k = n - k

        # reverse first k elements
        reverse(0, k - 1)
        # reverse the remaining elements
        reverse(k, n - 1)
        # reverse the entire array
        reverse(0, n - 1)
        