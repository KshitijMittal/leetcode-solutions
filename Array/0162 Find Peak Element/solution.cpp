class Solution {
public:
    int findPeakElement(vector<int>& nums) {
        // Brute Force
        /*int n = nums.size();

        for (int i = 0; i < n - 1; i++) {
            if (nums[i] > nums[i + 1]) {
                return i;
            }
        }

        return (n - 1);*/

        // Binary Search
        int n = nums.size();
        int left = 0;
        int right = n - 1;

        while(left < right) {
            int mid = left + (right - left) / 2;

            if (nums[mid] < nums[mid + 1]) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        return left;
        
    }
};