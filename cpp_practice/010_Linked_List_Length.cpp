/*
    2024.11.3 -- 2024.11.21
    Is Linked List Length Even?
    Given a linked list, your task is to complete the function isLengthEven() which contains the head of the linked list, and check whether the length of the linked list is even or not. Return true if it is even, otherwise false.

    Examples:

    Input: Linked list: 12->52->10->47->95->0
    Output: true
    Explanation: The length of the linked list is 6 which is even, hence returned true.

    Input: Linked list: 9->4->3
    Output: false
    Explanation: The length of the linked list is 3 which is odd, hence returned false.

    Constraints:
    1 <= number of nodes <= 105
    1 <= elements of the linked list <= 105
*/

//{ Driver Code Starts
#include <algorithm>
#include <bits/stdc++.h>
#include <cmath>
#include <cstdio>
#include <ios>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

struct Node {
    int data;
    struct Node *next;

    Node(int x) {
        data = x;
        next = NULL;
    }
};


// } Driver Code Ends
/*structure of a node of the linked list is as
struct Node
{
    int data;
    struct Node* next;

    Node(int x){
        data = x;
        next = NULL;
    }

};
*/
class Solution {
  public:
    bool isLengthEven(struct Node **head) {
        // Code here
        int len = 1;
        Node *head_ptr = *head;
        for (Node *n = head_ptr; n->next != NULL; n = n->next) {
            len += 1;
        }

        if (len%2)
            return false;

        return true;
    }
};

//{ Driver Code Starts.

/* Function to print nodes in a given linked list */
void printList(struct Node *head) {
    struct Node *temp = head;
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->next;
    }
    printf("\n");
}

int main() {
    int t;
    cin >> t;
    cin.ignore();
    while (t--) {
        vector<int> arr;
        string input;
        getline(cin, input);
        stringstream ss(input);
        int number;
        while (ss >> number) {
            arr.push_back(number);
        }

        if (arr.empty()) {
            cout << "empty" << endl;
            continue;
        }

        struct Node *head = new Node(arr[0]);
        struct Node *tail = head;
        for (int i = 1; i < arr.size(); ++i) {
            tail->next = new Node(arr[i]);
            tail = tail->next;
        }
        Solution ob;
        if (ob.isLengthEven(&head))
            cout << "true" << endl;
        else
            cout << "false" << endl;
        cout << "~" << endl;

        // Clean up the remaining nodes to avoid memory leaks
        while (head != NULL) {
            struct Node *temp = head;
            head = head->next;
            delete temp;
        }
    }
    return 0;
}

// } Driver Code Ends