/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* partition(ListNode* head, int x) {
        ListNode dummy1(0);
        ListNode dummy2(0);

        ListNode* small = &dummy1;
        ListNode* large = &dummy2;
        
        ListNode* curr = head;

        while (curr != nullptr) {
            if (curr->val < x) {
                small->next = curr;
                small = small->next;
            } else {
                large->next = curr;
                large = large->next;
            }
            curr = curr->next;
        }

        large->next = nullptr;

        small->next = dummy2.next;

        return dummy1.next;
    }
};