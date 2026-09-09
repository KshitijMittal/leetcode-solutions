class Solution {
public:
    bool isAnagram(string s, string t) {
        // Frequency array
        if (s.length() != t.length()) return false;

        int count[26] = {0}; 
        int lengthS = s.length();

        for (int i = 0; i < lengthS; i++) {
            count[s[i] - 'a']++;
            count[t[i] - 'a']--;
        }

        for (int i = 0; i < 26; i++) {
            if (count[i] != 0) {
                return false;
            }
        }

        return true;
    }
};