class Solution {
public:
    int maxSubarrayLength(vector<int>& nums, int k) {
        // Brute Force
        /*int n = nums.size();
        int max_len = 0;

        for (int i = 0; i < n; i++) {
            unordered_map<int, int> freq;

            for (int j = i; j < n; j++) {
                freq[nums[j]]++;

                if (freq[nums[j]] > k) {
                    break; 
                }

                max_len = max(max_len, j - i + 1);
            }
        }

        return max_len;*/

        // Sliding Window
        int n = nums.size();
        int max_len = 0;
        int left = 0;
        unordered_map<int, int> freq;

        for (int right = 0; right < n; right++) {
            freq[nums[right]]++;

            while (freq[nums[right]] > k) {
                freq[nums[left]]--;
                left++;
            }

            max_len = max(max_len, right - left + 1);
        }

        return max_len;
    }
};
