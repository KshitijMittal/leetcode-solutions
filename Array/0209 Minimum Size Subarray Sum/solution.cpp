class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        // int n = nums.size();
        // int min_length = INT_MAX;

        // for (int i = 0; i < n; ++i) {
        //     int current_sum = 0;

        //     for (int j = i; j < n; ++j) {
        //         current_sum += nums[j];

        //         if (current_sum >= target) {
        //             min_length = min(min_length, j - i + 1);
        //             break;
        //         }
        //     }
        // }

        // return(min_length == INT_MAX) ? 0 : min_length;


        int n = nums.size();
        int min_length = INT_MAX;
        int current_sum = 0;
        int left = 0;

        for(int right = 0; right < n; right++) {
            current_sum += nums[right];

            while(current_sum >= target) {
                min_length = min(min_length, right - left + 1);
                current_sum -= nums[left];
                left++;
            }
        }

        return(min_length == INT_MAX) ? 0 : min_length;
    }
};