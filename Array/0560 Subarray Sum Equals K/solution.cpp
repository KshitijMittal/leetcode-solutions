class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        // Brute Force
        /*int count = 0;
        int n = nums.size();

        for (int i = 0; i < n; i++) {
            int current_sum = 0;
            
            for (int j = i; j < n; j++) {
                current_sum += nums[j];
                
                if (current_sum == k) {
                    count++;
                }
            }
        }
        
        return count;*/

        // Hash map
        int count = 0;
        int current_sum = 0;

        std :: unordered_map<int, int> prefix_sum;
        prefix_sum[0] = 1;

        for(int num : nums) {
            current_sum += num;

            if(prefix_sum.count(current_sum - k)) {
                count += prefix_sum[(current_sum - k)];
            }

            prefix_sum[current_sum]++;
        }

        return count;
    }
};