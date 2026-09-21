class Solution {
public:
    int repeatedStringMatch(string a, string b) {
        string temp = a;
        int repeats = 1;

        while (temp.length() < b.length()) {
            temp += a;
            repeats++;
        }

        if (temp.find(b) != string::npos) {
            return repeats;
        }

        temp += a;
        if (temp.find(b) != string::npos) {
            return repeats + 1;
        }

        return -1;
    }
};