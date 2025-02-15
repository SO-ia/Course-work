/*
    Swap and Maximize
    
    Given an array arr[ ] of positive elements. Consider the array as a circular array, meaning the element after the last element is the first element of the array. The task is to find the maximum sum of the absolute differences between consecutive elements with shuffling of array elements allowed i.e. shuffle the array elements and make [a1..an] such order that  |a1 – a2| + |a2 – a3| + …… + |an-1 – an| + |an – a1| is maximized.

    Examples:
    Input: arr[] = [4, 2, 1, 8]
    Output: 18
    Explanation: After Shuffling, we get [1, 8, 2, 4]. Sum of absolute difference between consecutive elements after rearrangement = |1 - 8| + |8 - 2| + |2 - 4| + |4 - 1| = 7 + 6 + 2 + 3 = 18.

    Input: arr[] = [10, 12]
    Output: 4
    Explanation: No need of rearrangement. Sum of absolute difference between consecutive elements = |10 - 12| + |12 - 10| = 2 + 2 = 4.
    Constraints:
    2 ≤ arr.size()≤ 10^5
    1 <= arr[i] <= 10^5
*/

//{ Driver Code Starts
#include <bits/stdc++.h>
using namespace std;

// long long int maxSum(int arr[], int n);

// } Driver Code Ends
// Function to find the maximum sum of the array elements
class Solution {
  public:

    long long maxSum(vector<int> &arr) {
        long long sum = 0;
        int n = arr.size(); // Size of the array

        // Sorting the array in ascending order
        sort(arr.begin(), arr.end());

        // Looping over the first half of the array
        for (int i = 0; i < n / 2; i++) {
            // Subtracting twice the current element and adding twice
            // the element at the opposite end of the array to the sum
            sum -= (2 * arr[i]);
            sum += (2 * arr[n - i - 1]);
        }

        // Returning the maximum sum
        return sum;
    }
};


//{ Driver Code Starts.

int main() {
    int t;
    cin >> t;
    cin.ignore(); // To ignore any newline character left in the buffer
    while (t--) {
        string line;
        getline(cin, line); // Read the entire line of input
        stringstream ss(line);
        vector<int> arr;
        int num;

        // Parse the input line into integers and add to the vector
        while (ss >> num) {
            arr.push_back(num);
        }

        Solution ob;
        long long ans = ob.maxSum(arr);

        cout << ans << endl;
        cout << "~" << endl;
    }
    return 0;
}
// } Driver Code Ends