/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        if (!headA || !headB) return nullptr;

        int lenA = 0;
        int lenB = 0;

        ListNode* currA = headA;
        ListNode* currB = headB;

        while (currA != nullptr) {
            lenA++;
            currA = currA->next;
        }

        while (currB != nullptr) {
            lenB++;
            currB = currB->next;
        }

        currA = headA;
        currB = headB;

        while (lenA > lenB) {
            currA = currA->next;
            lenA--;
        }
        while (lenB > lenA) {
            currB = currB->next;
            lenB--;
        }

         while (currA != currB) {
            currA = currA->next;
            currB = currB->next;
        }

        return currA;
    }
};