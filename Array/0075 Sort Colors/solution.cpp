class Solution {
public:
    void sortColors(vector<int>& nums) {
        int count_zero = 0;
        int count_ones = 0;
        int count_twos = 0;

        for(int i = 0; i < nums.size(); i++) {
            if (nums[i] == 0) count_zero++;
            if (nums[i] == 1) count_ones++;
            if (nums[i] == 2) count_twos++;
        }

        for(int i = 0; i < nums.size(); i++) {
            if (count_zero > 0) {
                nums[i] = 0;
                count_zero--;
            }
            else if (count_ones > 0) {
                nums[i] = 1;
                count_ones--;
            }
            else {
                nums[i] = 2;
            }
        }
    }
};