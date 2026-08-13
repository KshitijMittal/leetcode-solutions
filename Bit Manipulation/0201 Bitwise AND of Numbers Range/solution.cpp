class Solution {
public:
    int rangeBitwiseAnd(int left, int right) {
        // if (left >= INT_MAX || right >= INT_MAX) return 0;

        // int ans = left;
        // for (long long i = left; i <= right; i++) {
        //     ans &= i;
        //     if (ans == 0) break;
        // }

        // return ans;

        int count = 0;
        while (left < right) {
            left >>= 1;
            right >>= 1;
            count ++;
        }

        return left << count;
    }

};