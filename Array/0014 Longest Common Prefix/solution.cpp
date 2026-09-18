class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
      if (strs.empty()) {
            return "";
        }
        
        string firstStr = strs[0];
        string prefixStr = "";

        for (int i = 0; i < firstStr.length(); i++) {
            char ch = firstStr[i];
            for (int j = 1; j < strs.size(); j++) {
                if (i >= strs[j].length() || strs[j][i] != ch) {
                    return prefixStr;
                }
            }

            prefixStr += ch;
        }

        return prefixStr;
    }
};