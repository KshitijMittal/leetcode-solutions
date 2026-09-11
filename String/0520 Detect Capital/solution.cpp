class Solution {
public:
    bool detectCapitalUse(string word) {
        int len = 0;
        int capitals = 0;

        for (char ch : word) {
            len++;
            if (ch >= 'A' && ch <= 'Z') {
                capitals++;
            }
        }

        if (capitals == len || capitals == 0) {
            return true;
        }

        if (capitals == 1) {
            if (word[0] >= 'A' && word[0] <= 'Z') {
                return true;
            }
        }
        
        return false;
    }
};