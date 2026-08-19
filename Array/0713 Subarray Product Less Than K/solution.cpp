class Solution {
public:
    int numSubarrayProductLessThanK(vector<int>& nums, int k) {
        // Two-pointer
        if(k <= 1) return 0;
        
        int n = nums.size();
        int count = 0;
        long long current_product = 1;
        int left = 0;
        
        for(int right = 0; right < n; right++) {
            current_product *= nums[right];
            
            while(current_product >= k) {
                current_product /= nums[left];
                left++;
            }

            count += (right - left + 1);
        }
        
        return count;
    }
};