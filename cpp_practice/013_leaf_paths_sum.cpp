/*
    2024.11.06 -- 2024.11.21
    Root to leaf paths sum
    Given a binary tree, where every node value is a number. Find the sum of all the numbers that are formed from root to leaf paths. The formation of the numbers would be like 10*parent + current (see the examples for more clarification).

    Input:      
    Output: 13997
    Explanation : There are 4 leaves, resulting in leaf path of 632, 6357, 6354, 654 sums to 13997.

    Input:    
    Output: 2630
    Explanation: There are 3 leaves, resulting in leaf path of 1240, 1260, 130 sums to 2630.
    Input:    
            1
            /
            2                    
    Output: 12
    Explanation: There is 1 leaf, resulting in leaf path of 12.

    Constraints:
    1 ≤ number of nodes ≤ 31
    1 ≤ node->data ≤ 100

    Time Complexity: O(n)
    Auxiliary Space: O(h)
*/

//{ Driver Code Starts
#include <bits/stdc++.h>
using namespace std;

struct Node {
    int data;
    struct Node* left;
    struct Node* right;
};

Node* newNode(int val) {
    Node* temp = new Node;
    temp->data = val;
    temp->left = NULL;
    temp->right = NULL;

    return temp;
}

Node* buildTree(string str) {
    // Corner Case
    if (str.length() == 0 || str[0] == 'N')
        return NULL;

    // Creating vector of strings from input
    // string after spliting by space
    vector<string> ip;

    istringstream iss(str);
    for (string str; iss >> str;)
        ip.push_back(str);

    // Create the root of the tree
    Node* root = newNode(stoi(ip[0]));

    // Push the root to the queue
    queue<Node*> queue;
    queue.push(root);

    // Starting from the second element
    int i = 1;
    while (!queue.empty() && i < ip.size()) {

        // Get and remove the front of the queue
        Node* currNode = queue.front();
        queue.pop();

        // Get the current node's value from the string
        string currVal = ip[i];

        // If the left child is not null
        if (currVal != "N") {

            // Create the left child for the current node
            currNode->left = newNode(stoi(currVal));

            // Push it to the queue
            queue.push(currNode->left);
        }

        // For the right child
        i++;
        if (i >= ip.size())
            break;
        currVal = ip[i];

        // If the right child is not null
        if (currVal != "N") {

            // Create the right child for the current node
            currNode->right = newNode(stoi(currVal));

            // Push it to the queue
            queue.push(currNode->right);
        }
        i++;
    }

    return root;
}


// } Driver Code Ends
/* Tree node structure  used in the program
 struct Node
 {
     int data;
     Node* left, *right;
}; */

class Solution {
  public:
    int treePathsSum(Node *root) {
        // code here.
        int sum = root->data;
        int l = 0;
        int r = 0;
        // 左右子树非空，则进入搜索
        if(root->left) l = search_leaf(root->left, sum);
        if(root->right) r = search_leaf(root->right, sum);

        return l+r;
    }

    int search_leaf(Node *n, int sum) {
        // 当前累计和
        sum = sum*10 + n->data;
        int l_sum = 0;
        int r_sum = 0;
        if(n->left) l_sum = search_leaf(n->left, sum);
        if(n->right) r_sum = search_leaf(n->right, sum);

        // 叶子结点时返回sum，因为此时 l_sum 和 r_sum 都为 0
        if(!l_sum && !r_sum) return sum;

        // 非叶子结点时返回左右子树累计和，不需要再＋到目前为止的和
        return l_sum + r_sum;
    }
};


//{ Driver Code Starts.

int main() {
    int t;
    scanf("%d ", &t);
    while (t--) {
        string s;
        getline(cin, s);
        Node* root = buildTree(s);
        Solution ob;
        cout << ob.treePathsSum(root);
        cout << endl;
        cout << "~\n";
    }
    return 0;
}

// } Driver Code Ends