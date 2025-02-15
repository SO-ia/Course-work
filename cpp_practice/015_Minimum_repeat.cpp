/*
    2024.11.08 -- 2024.11.21
    Minimum repeat to make substring
    Given two strings s1 and s2. Return a minimum number of times s1 has to be repeated such that s2 is a substring of it. If s2 can never be a substring then return -1.

    Note: Both the strings contain only lowercase letters.

    Examples:

    Input: s1 = "ww", s2 = "www"
    Output: 2
    Explanation: Repeating s1 two times "wwww", s2 is a substring of it.

    Input: s1 = "abcd", s2 = "cdabcdab" 
    Output: 3 
    Explanation: Repeating s1 three times "abcdabcdabcd", s2 is a substring of it. s2 is not a substring of s1 when it is repeated less than 3 times.

    Input: s1 = "ab", s2 = "cab"
    Output: -1
    Explanation: No matter how many times we repeat s1, we can't get a string such that s2 is a substring of it.

    Constraints:
    1 ≤ s1.size(), s2.size() ≤ 105

    Time Complexity: O(n + m)
    Auxiliary Space: O(n)
*/
//{ Driver Code Starts
#include <bits/stdc++.h>
using namespace std;


// } Driver Code Ends
// User function Template for C++

class Solution {
  public:
    int minRepeats(string& s1, string& s2) {
        // code here
        unordered_map<char, int> str2;
        for (char ch : s2) {
            str2[ch] += 1;
        }

        int max_cnt = -1;
        for (char ch : s1) {
            auto it = str2.find(ch) != str2.end();
            if (it && str2[ch] > max_cnt)
                max_cnt = str2[ch];
        }

        return max_cnt;
    }
};

//{ Driver Code Starts.

int main() {
    int t;
    scanf("%d ", &t);
    while (t--) {
        string A, B;
        getline(cin, A);
        getline(cin, B);

        Solution ob;
        cout << ob.minRepeats(A, B) << endl;
    }
    return 0;
}
// } Driver Code Ends