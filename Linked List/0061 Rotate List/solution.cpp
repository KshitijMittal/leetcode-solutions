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
    ListNode* rotateRight(ListNode* head, int k) {
        if (!head || !head->next || k == 0) {
            return head;
        }

        int length = 1;
        ListNode* temp = head;
        while (temp->next != nullptr) {
            temp = temp->next;
            length++;
        }

        k = k % length;
        if (k == 0)
            return head;

        temp->next = head;

        int steps = length - k;
        ListNode* temp2 = head;

        int i = 0;
        while (i < length - k - 1) {
            temp2 = temp2->next;
            i++;
        }

        ListNode* newHead = temp2->next;
        temp2->next = nullptr;

        return newHead;
    }
};