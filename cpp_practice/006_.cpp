/*
    2024.10.01 / 2024.10.xx
    Given elements as nodes of the two singly linked lists. The task is to multiply these two linked lists, say L1 and L2.
    Note: The output could be large take modulo 10^9+7.

    Examples :
    Input: LinkedList L1 : 3->2 , LinkedList L2 : 2
    Output: 64
    Explanation: Multiplication of 32 and 2 gives 64.

    Expected Time Complexity: O(max(n,m))
    Expected Auxilliary Space: O(1)
    where n is the size of L1 and m is the size of L2

    Constraints:
    1 <= number of nodes <= 10^5
    1 <= node->data <= 10^3
*/

//{ Driver Code Starts
#include <bits/stdc++.h>
using namespace std;

/* Linked list Node */
struct Node {
    int data;
    struct Node *next;

    Node(int x) {
        data = x;
        next = NULL;
    }
};

/* Function to create a new Node with given data */
struct Node *newNode(int data) {
    struct Node *new_Node = new Node(data);

    return new_Node;
}

Node *reverse(Node **r) {
    Node *prev = NULL;
    Node *cur = *r;
    Node *nxt;
    while (cur != NULL) {
        nxt = cur->next;
        cur->next = prev;
        prev = cur;
        cur = nxt;
    }
    *r = prev;
}

/* Function to insert a Node at the beginning of the Doubly Linked List */
void push(struct Node **head_ref, int new_data) {
    /* allocate Node */
    struct Node *new_Node = newNode(new_data);

    /* link the old list off the new Node */
    new_Node->next = (*head_ref);

    /* move the head to point to the new Node */
    (*head_ref) = new_Node;
}

void freeList(struct Node *Node) {
    struct Node *temp;
    while (Node != NULL) {

        temp = Node;
        Node = Node->next;
        free(temp);
    }
}


// } Driver Code Ends
/* Linked list node structure
struct Node
{
    int data;
    Node* next;

    Node(int x){
        data = x;
        next = NULL;
    }

};*/

/*The method multiplies
two  linked lists l1 and l2
and returns their product*/

/* Multiply contents of two linked lists */
class solution {
  public:
    long long multiplyTwoLists(Node *first, Node *second) {
        // code here
        // long long first_m = 0;
        // long long second_n = 0;

        vector<int> first_m;
        vector<long long> second_n;

        long long num_m = 0;
        // long long num_n = 0;
        long long res = 0;

        for (Node *n = first; n != NULL; n = n->next)
            first_m.push_back(n->data);

        for (Node *n = second; n != NULL; n = n->next)
            second_n.push_back(n->data);

        int len_m = first_m.size();
        int len_n = second_n.size();
        
        for (int i = 0; i < len_m; i++) {
            num_m += first_m[i] * pow(10, len_m - i - 1);
            // printf("%d %d", num_m, first_m);
        }

        // for (int i = 0; i < len_n; i++) {
        //     num_n += second_n[i] * pow(10, len_n - i - 1);
        //     // printf("%d %d", num_n, second_n);
        // }

        for (int i = 0; i < len_n; i++) {
            res += num_m * second_n[i] * pow(10, len_n - i - 1);
            // printf("%d %d", num_n, second_n);
        }

        return res;
    }
};

//{ Driver Code Starts.

// A utility function to print a linked list
void printList(struct Node *Node) {
    while (Node != NULL) {
        printf("%d ", Node->data);
        Node = Node->next;
    }
    printf("\n");
}

/* Driver program to test above function */
int main(void) {

    int t;
    cin >> t;
    cin.ignore();
    while (t--) {

        struct Node *first = NULL;
        struct Node *second = NULL;
        vector<int> arr;
        string input;
        getline(cin, input);
        stringstream ss(input);
        int number;

        while (ss >> number) {
            arr.push_back(number);
        }
        for (int i = 0; i < arr.size(); i++) {
            push(&first, arr[i]);
        }
        vector<int> brr;
        string input2;
        getline(cin, input2);
        stringstream ss2(input2);
        int number1;
        while (ss2 >> number1) {
            brr.push_back(number1);
        }
        for (int i = 0; i < brr.size(); i++) {
            push(&second, brr[i]);
        }
        reverse(&first);
        reverse(&second);
        solution ob;
        long long res = ob.multiplyTwoLists(first, second);
        cout << res << endl;
        freeList(first);
        freeList(second);
    }
    return 0;
}

// } Driver Code Ends