class Solution {
public:
    int divide(int dividend, int divisor) {
        if (divisor == 0) return 0;

        if (dividend == INT_MIN && divisor == -1) {
            return INT_MAX;
        }

        long long divid = llabs(dividend);
        long long div = llabs(divisor);
        long long ans = 0;

        while(divid >= div) {
            long long count = 0;
            while(divid >= (div << (count + 1))) {
                count ++;
            }

            divid -= (div << count);
            ans += (1 << count);
        }

        if ((dividend < 0 && divisor > 0) || (dividend > 0 && divisor < 0)) {
            return -ans;
        } else {
            return ans;
        }
    }
};