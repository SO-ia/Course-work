/*
    2024.11.09 -- 2024.11.21
    Minimum sum
    Given an array arr[] such that each element is in the range [0 - 9], find the minimum possible sum of two numbers formed using the elements of the array. All digits in the given array must be used to form the two numbers. Return a string without leading zeroes.

    Examples :

    Input: arr[] = [6, 8, 4, 5, 2, 3]
    Output: 604
    Explanation: The minimum sum is formed by numbers 358 and 246.
    Input: arr[] = [5, 3, 0, 7, 4]
    Output: 82
    Explanation: The minimum sum is formed by numbers 35 and 047.
    Input: arr[] = [9, 4]
    Output: 13
    Explanation: The minimum sum is formed by numbers 9 and 4.
    Constraints:
    1 ≤ arr.size() ≤ 106
    0 ≤ arr[i] ≤ 9

    Time Complexity: O(n log n)
    Auxiliary Space: O(n)
*/

//{ Driver Code Starts
#include <bits/stdc++.h>
using namespace std;


// } Driver Code Ends
// User function template for C++

class Solution {
  public:
    string minSum(vector<int> &arr) {
        // code here
    }
};

//{ Driver Code Starts.

int main() {
    int t;
    cin >> t;
    cin.ignore();
    while (t--) {
        vector<int> a;
        string input;
        getline(cin, input);
        stringstream ss(input);
        int number;
        while (ss >> number) {
            a.push_back(number);
        }

        Solution ob;
        string ans = ob.minSum(a);
        cout << ans << endl;
        cout << "~" << endl;
    }
    return 0;
}

// } Driver Code Ends