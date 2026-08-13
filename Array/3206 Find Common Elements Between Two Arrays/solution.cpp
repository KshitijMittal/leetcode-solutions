class Solution {
public:
    vector<int> findIntersectionValues(vector<int>& num1, vector<int>& num2) {
        std :: unordered_set<int>set1(num1.begin(), num1.end());
        std :: unordered_set<int>set2(num2.begin(), num2.end());

        int count1 = 0;
        int count2 = 0;

        for(int i : num1) {
            if(set2.count(i)) {
                count1++;
            }            
        }

        for(int i : num2) {
            if(set1.count(i)) {
                count2++;
            }
        }

        return {count1, count2};
    }
};