class Solution {
public:
    string removeOccurrences(string s, string part) {
        string result = "";
        int partLen = part.length();

        for (char c : s) {
            result.push_back(c);

            if (result.length() >= partLen) {
                bool match = true;
                for (int i = 0; i < partLen; i++) {
                    if (result[result.length() - partLen + i] != part[i]) {
                        match = false;
                        break;
                    }
                }

                if (match) {
                    for (int i = 0; i < partLen; i++) {
                        result.pop_back();
                    }
                }
            }
        }

        return result;
    }
};