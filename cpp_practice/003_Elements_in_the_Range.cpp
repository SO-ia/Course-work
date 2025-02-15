/*
Given an array arr[] containing positive elements. A and B are two numbers defining a range. The task is to check if the array contains all elements in the given range (inclusive).

Note: If the array contains all elements in the given range return true otherwise return false.

Examples :

Input: n = 7, A = 2, B = 5, arr[] =  {1, 4, 5, 2, 7, 8, 3}
Output: True
Explanation: It has all elements between range 2-5 i.e 2,3,4,5.
*/

//{ Driver Code Starts
#include <bits/stdc++.h>
using namespace std;

// } Driver Code Ends
class Solution
{
public:
    bool check_elements(int arr[], int n, int A, int B)
    {
        // Your code goes here
    }
};

//{ Driver Code Starts.

int main()
{

    int t;
    cin >> t;
    while (t--)
    {
        int n, A, B;
        cin >> n >> A >> B;
        int a[n];
        for (int i = 0; i < n; ++i)
            cin >> a[i];

        Solution ob;
        if (ob.check_elements(a, n, A, B))
            cout << "True";
        else
            cout << "False";

        cout << "\n";
    }
    return 0;
}

// } Driver Code Ends