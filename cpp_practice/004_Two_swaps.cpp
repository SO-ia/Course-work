/*Two Swaps
Given a permutation of some of the first natural numbers in an array arr[], determine if the array can be sorted in exactly two swaps. A swap can involve the same pair of indices twice. (!!!可以对同一组数交换两次)

Return true if it is possible to sort the array with exactly two swaps, otherwise return false.

Examples:

Input: arr = [4, 3, 2, 1]
Output: true
Explanation: First, swap arr[0] and arr[3]. The array becomes [1, 3, 2, 4]. Then, swap arr[1] and arr[2]. The array becomes [1, 2, 3, 4], which is sorted.

Input: arr = [1, 2, 3, 4]
Output: true*/

//{ Driver Code Starts

#include <bits/stdc++.h>
using namespace std;

// } Driver Code Ends
class Solution
{
public:
    bool checkSorted(vector<int> &arr)
    {
        // code here
        int mis = 0;
        for (int i = 0; i < arr.size(); i++) {
            if (arr[i] != i + 1)
                mis++;
        }

        // 0: 正确排序
        // 3: 有三个错位，一定正好能在2次中正确排序
        if (mis == 0 || mis == 3)
            return true;

        // 2: 交换一次后就已经正确排序了，后续再怎么移动都会错位
        // >4: 错位的数多于4个，一定是不能再两次交换内正确排序的
        if (mis == 2 || mis > 4)
            return false;

        // ==4: 4个错位的情况下，只有两两错位才能在2次交换内正确排序，否则都视为false
        // 两两错位: (3 4 2 1), (4 3 2 1), (2 1 4 3)
        for (int i = 0; i < arr.size(); i++){
            if (arr[i] != i + 1) {
                if (arr[arr[i] - 1] == i + 1)
                    return true;
            }
        }
        return false;
    }
};

//{ Driver Code Starts.

int main()
{

    int t;
    cin >> t;
    cin.ignore();
    while (t--)
    {
        string input;
        getline(cin, input);
        stringstream ss(input);
        int num;
        vector<int> arr;
        while (ss >> num)
            arr.push_back(num);

        Solution ob;
        bool ans = ob.checkSorted(arr);
        if (ans)
            cout << "true" << endl;
        else
            cout << "false" << endl;
    }
}

// } Driver Code Ends