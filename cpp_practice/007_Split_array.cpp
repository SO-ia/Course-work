/*
    Split array in three equal sum subarrays
Given an array, arr[], determine if arr can be split into three consecutive parts such that the sum of each part is equal. If possible, return any index pair(i, j) in an array such that sum(arr[0..i]) = sum(arr[i+1..j]) = sum(arr[j+1..n-1]), otherwise return an array {-1,-1}.

Note: Driver code will print true if arr can be split into three equal sum subarrays, otherwise, it is false.

Examples :

Input:  arr[] = [1, 3, 4, 0, 4]
Output: true
Explanation:
[1, 2] is valid pair as sum of subarray arr[0..1] is equal to sum of subarray arr[2..3] and also to sum of subarray arr[4..4]. The sum is 4.

Input: arr[] = [2, 3, 4]
Output: false
Explanation: No three subarrays exist which have equal sum.
Input: arr[] = [0, 1, 1]
Output: false

Constraints:
3 ≤ arr.size() ≤ 106
0 ≤ arr[i] ≤ 106
*/

//{ Driver Code Starts
// Initial Template for C++
#include <bits/stdc++.h>
using namespace std;


// } Driver Code Ends
// User function Template for C++
//  Class Solution to contain the method for solving the problem.
class Solution {
  public:
    // Function to determine if array arr can be split into three equal sum sets.
    vector<int> findSplit(vector<int>& arr) {
        // code here
        int sum = 0;
        vector<int> res = {-1, -1};

        for (int i : arr)
            sum += i;
        int sub_sum = sum / 3;

        if (sum % 3) {
            res[0] = -1;
            res[1] = -1;
            return res;
        }
        
        if (!sum) {
            res[0] = 0;
            res[1] = 1;
            return res;
        }
        
        int j = 0;
        for (int i = 0; i < arr.size(); i++) {
            if (!sub_sum) {
                res[j++] = i - 1;
                sub_sum =  sum / 3;
            }
            sub_sum -= arr[i];
        }

        return res;
    }
};

//{ Driver Code Starts.

int main() {
    int test_cases;
    cin >> test_cases;
    cin.ignore();
    while (test_cases--) {
        string input;
        vector<int> arr;

        // Read the array from input line
        getline(cin, input);
        stringstream ss(input);
        int number;
        while (ss >> number) {
            arr.push_back(number);
        }

        // Solution instance to invoke the function
        Solution ob;
        vector<int> result = ob.findSplit(arr);

        // Output result
        if (result[0] == -1 && result[1] == -1 || result.size() != 2) {
            cout << "false" << endl;
        } else {
            int sum1 = 0, sum2 = 0, sum3 = 0;
            for (int i = 0; i < arr.size(); i++) {
                if (i <= result[0])
                    sum1 += arr[i];

                else if (i <= result[1])
                    sum2 += arr[i];

                else
                    sum3 += arr[i];
            }
            if (sum1 == sum2 && sum2 == sum3) {
                cout << "true" << endl;
            } else {
                cout << "false" << endl;
            }
        }
        cout << "~" << endl;
    }
    return 0;
}

// } Driver Code Ends