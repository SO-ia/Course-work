/*
    2024.11.10 -- 2024.11.21
    Union of Two Sorted Arrays with Distinct Elements
    Given two sorted arrays a[] and b[], where each array contains distinct elements , the task is to return the elements in the union of the two arrays in sorted order.
    Union of two arrays can be defined as the set containing distinct common elements that are present in either of the arrays.

    Examples:
    Input: a[] = [1, 2, 3, 4, 5], b[] = [1, 2, 3, 6, 7]
    Output: 1 2 3 4 5 6 7
    Explanation: Distinct elements including both the arrays are: 1 2 3 4 5 6 7.

    Input: a[] = [2, 3, 4, 5], b[] = [1, 2, 3, 4]
    Output: 1 2 3 4 5
    Explanation: Distinct elements including both the arrays are: 1 2 3 4 5.

    Input: a[] = [1], b[] = [2]
    Output: 1 2
    Explanation: Distinct elements including both the arrays are: 1 2.

    Constraints:
    1  <=  a.size(), b.size()  <=  105
    -109  <=  a[i] , b[i]  <=  109

    Time Complexity: O(n + m)
    Auxiliary Space: O(n + m)
*/
//{ Driver Code Starts
#include <bits/stdc++.h>

using namespace std;


// } Driver Code Ends
class Solution {
  public:
    // a,b : the arrays
    // Function to return a list containing the union of the two arrays.
    vector<int> findUnion(vector<int> &a, vector<int> &b) {
        // Your code here
        // return vector with correct order of elements
    }
};

//{ Driver Code Starts.
int main() {
    int t;
    cin >> t;
    cin.ignore();
    while (t--) {
        vector<int> a, b;
        string input;

        // Read first array
        getline(cin, input);
        stringstream ss(input);
        int number;
        while (ss >> number) {
            a.push_back(number);
        }

        // Read second array
        getline(cin, input);
        stringstream ss2(input);
        while (ss2 >> number) {
            b.push_back(number);
        }

        Solution ob;
        vector<int> ans = ob.findUnion(a, b);
        for (int i : ans)
            cout << i << ' ';
        cout << endl;
        cout << "~" << endl;
    }
    return 0;
}

// } Driver Code Ends