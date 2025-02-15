/*
    2024.11.2 -- 2024.11.20 & 21
    Given an unsorted array arr and a number k which is smaller than the size of the array. Return true if the array contains any duplicate within k distance throughout the array else false.

    Examples:

    Input: arr[] = [1, 2, 3, 4, 1, 2, 3, 4] and k = 3
    Output: false
    Explanation: All duplicates are more than k distance away.

    Input: arr[] = [1, 2, 3, 1, 4, 5] and k = 3
    Output: true
    Explanation: 1 is repeated at distance 3.

    Input: arr[] = [6, 8, 4, 1, 8, 5, 7] and k = 3
    Output: true
    Explanation: 8 is repeated at distance 3.

    Constraints:
    1 ≤ arr.size() ≤ 106
    1 ≤ k < arr.size()
    1 ≤ arr[i] ≤ 105
*/

//{ Driver Code Starts
#include <bits/stdc++.h>
using namespace std;


// } Driver Code Ends
// User function template for C++

/*
    formal solution
class Solution {
  public:

    bool checkDuplicatesWithinK(vector<int>& arr, int k) {
        int n = arr.size();
        // Creates an empty hashset
        unordered_set<int> myset;

        // Traverse the input array
        for (int i = 0; i < n; i++) {
            // If already present n hash, then we found
            // a duplicate within k distance
            if (myset.find(arr[i]) != myset.end())
                return true;

            // Add this item to hashset
            myset.insert(arr[i]);

            // Remove the k+1 distant item
            if (i >= k)
                myset.erase(arr[i - k]);
        }
        return false;
    }
};
*/

class Solution {
  public:

    bool checkDuplicatesWithinK(vector<int>& arr, int k) {
        // your code

        vector<int> b(pow(10, 5), 0);

        for (int i = 0; i < k; i++) {
            if (b[arr[i]]) return true;
            b[arr[i]]=1;
        }

        for (int i = k; i < arr.size(); i++) {
            if (b[arr[i]])
                return true;
            b[arr[i]] = 1;
            b[arr[i-k]] = 0;
        }
        
        return false;
    }
};

//{ Driver Code Starts.

int main() {
    string ts;
    getline(cin, ts);
    int t = stoi(ts);
    while (t--) {
        vector<int> arr;
        string input;
        getline(cin, input);
        stringstream ss(input);
        int number;
        while (ss >> number) {
            arr.push_back(number);
        }
        string ks;
        getline(cin, ks);
        int k = stoi(ks);
        Solution obj;
        bool res = obj.checkDuplicatesWithinK(arr, k);
        if (res)
            cout << "true" << endl;
        else
            cout << "false" << endl;
        // cout << res << endl;
        cout << "~" << endl;
    }
    return 0;
}
// } Driver Code Ends