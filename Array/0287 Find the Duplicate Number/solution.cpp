class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        std :: unordered_set<int> value;

        for(int i : nums) {
            if(value.count(i)) {
                return i;
            }

            value.insert(i);
        }

        return -1;
    }
};