class Solution {
public:
    bool searchMatrix(vector<vector<int>>& matrix, int target) {
        // Brute Force
        /*int rows = matrix.size();
        int cols = matrix[0].size();

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (matrix[r][c] == target) {
                    return true;
                }
            }
        }

        return false;*/

        // Binary Search
        int rows = matrix.size();
        int cols = matrix[0].size();

        int left = 0;
        int right = (rows * cols) - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            int mid_val = matrix[mid / cols][mid % cols];
            
            if (mid_val == target) {
                return true;
            } else if (mid_val < target) {
                left = mid + 1; // Search the right half
            } else {
                right = mid - 1; // Search the left half
            }
        }
        return false;
    }
};