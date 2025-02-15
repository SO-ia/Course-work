/*
You are given an integer array arr[]. The task is to find the sum of it.

Examples:
Input: arr[] = [1, 2, 3, 4]
Output: 10
Explanation: 1 + 2 + 3 + 4 = 10.
*/

//{ Driver Code Starts
#include <bits/stdc++.h>
using namespace std;

// } Driver Code Ends
// User function template for C++
class Solution
{
public:
    // Function to return sum of elements
    int sum(vector<int> &arr)
    {
        // code here
        int ans = 0;
        for (int i : arr)
            ans += i;

        return ans;
    }
};

//{ Driver Code Starts.

int main()
{
    string ts;
    getline(cin, ts);
    int t = stoi(ts);

    while (t--)
    {
        string line;
        getline(cin, line);
        stringstream ss(line);
        vector<int> nums;
        int num;
        while (ss >> num)
        {
            nums.push_back(num);
        }
        Solution ob;
        int ans = ob.sum(nums); // Pass the vector nums to the sum function
        cout << ans << "\n";
    }
    return 0;
}
// } Driver Code Ends