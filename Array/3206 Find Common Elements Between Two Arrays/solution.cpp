class Solution {
public:
    vector<int> findIntersectionValues(vector<int>& nums1, vector<int>& nums2) {
        // std :: unordered_set<int>set1(num1.begin(), num1.end());
        // std :: unordered_set<int>set2(num2.begin(), num2.end());

        // int count1 = 0;
        // int count2 = 0;

        // for(int i : num1) {
        //     if(set2.count(i)) {
        //         count1++;
        //     }            
        // }

        // for(int i : num2) {
        //     if(set1.count(i)) {
        //         count2++;
        //     }
        // }

        // return {count1, count2};

        int count1 = 0;
        int count2 = 0;

        int n1 = nums1.size();
        int n2 = nums2.size();
        
        for (int i = 0; i < n1; i++) {
            for (int j = 0; j < n2; j++) {
                if (nums1[i] == nums2[j]) {
                    count1++;
                    break; 
                }
            }
        }

        for (int i = 0; i < n2; i++) {
            for (int j = 0; j < n1; j++) {
                if (nums2[i] == nums1[j]) {
                    count2++;
                    break; 
                }
            }
        }
        
        return {count1, count2};
    }
};