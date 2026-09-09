class Solution {
public:
    bool rotateString(string s, string goal) {
        if (s.length() != goal.length()) {
            return false;
        }

        int n = s.length();
        if (n == 0)
            return true;

        for (int i = 0; i < n; i++) {
            bool isMatch = true;

            for (int j = 0; j < n; j++) {
                if (s[(i + j) % n] != goal[j]) {
                    isMatch = false;
                    break;
                }
            }

            if (isMatch) {
                return true;
            }
        }

        return false;
    }
};