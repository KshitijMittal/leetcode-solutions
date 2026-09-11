class Solution {
public:
    bool buddyStrings(string s, string goal) {
        if (s.length() != goal.length()) {
            return false;
        }

        if (s == goal) {
            int count[26] = {0};
            for (char ch : s) {
                count[ch - 'a']++; 
                if (count[ch - 'a'] > 1) {
                    return true;
                }

            }
            
            return false;
        }

        int diff[2], count = 0;
        for (int i = 0; i < s.length(); ++i) {
            if (s[i] != goal[i]) {
                if (count == 2) return false; 
                diff[count++] = i; 
            }
        }

        if (count != 2) {
            return false;
        }

        return s[diff[0]] == goal[diff[1]] && s[diff[1]] == goal[diff[0]];
    }
};