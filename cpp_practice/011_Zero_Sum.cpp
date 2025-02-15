/*
    2024.11.04 -- 2024.11.21
    Find All Triplets with Zero Sum
    Given an array arr[], find all possible indices [i, j, k] of triplets [arr[i], arr[j], arr[k]] in the array whose sum is equal to zero. Return indices of triplets in any order and all the returned triplets indices should also be internally sorted, i.e., for any triplet indices [i, j, k], the condition i < j < k should hold.

    Note: Try to solve this using the O(n2) approach.

    Examples:
    Input: arr[] = [0, -1, 2, -3, 1]
    Output: [[0, 1, 4], [2, 3, 4]]
    Explanation: Triplets with sum 0 are:
    arr[0] + arr[1] + arr[4] = 0 + (-1) + 1 = 0
    arr[2] + arr[3] + arr[4] = 2 + (-3) + 1 = 0

    Input: arr[] = [1, -2, 1, 0, 5]
    Output: [[0, 1, 2]]
    Explanation: Only triplet which satisfies the condition is arr[0] + arr[1] + arr[2] = 1 + (-2) + 1 = 0

    Input: arr[] = [2, 3, 1, 0, 5]
    Output: [[]]
    Explanation: There is no triplet with sum 0.

    Constraints:
    3 <= arr.size() <= 10^3
    -10^4 <= arr[i] <= 10^4
*/

//{ Driver Code Starts
#include <bits/stdc++.h>
using namespace std;


// } Driver Code Ends
// User function Template for C++
class Solution {
  public:
    vector<vector<int>> findTriplets(vector<int> &arr) {
        // Code here
        set<vector<int>> resSet;
        unordered_map<int, vector<pair<int, int>>> mp;
        int n = arr.size();

        // store all pairs of index that sum of arr[i] and arr[j]
        for (int i = 0; i < n; i++) 
            for (int j = i + 1; j < n; j++)
                mp[arr[i] + arr[j]].push_back({i, j});

        for (int k = 0; k < n; k++) {
            // 不对！我有个问题
            // 经查证 unordered_map 的 find 操作的平均时间复杂度为 O(1)
            if (mp.find(-arr[k]) != mp.end()) {
                vector<pair<int, int>> tmp = mp[-arr[k]];
                for (auto it : tmp) {
                    if (it.first != k && it.second != k) {
                        vector<int> com = {k, it.first, it.second};
                        sort(com.begin(), com.end());
                        resSet.insert(com);
                    }
                }
            }
        }

        vector<vector<int>> res(resSet.begin(), resSet.end());

        return res;
    }
};

//{ Driver Code Starts.

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
        Solution ob;

        vector<vector<int>> res = ob.findTriplets(arr);
        sort(res.begin(), res.end());
        if (res.size() == 0) {
            cout << "[]\n";
        }
        for (int i = 0; i < res.size(); i++) {
            for (int j = 0; j < res[i].size(); j++) {
                cout << res[i][j] << " ";
            }
            cout << endl;
        }
        cout << "~" << endl;
    }
    return 0;
}
// } Driver Code Ends