/*
2024.10.28
Nearest multiple of 10
A string str is given to represent a positive number. The task is to round str to the nearest multiple of 10.  If you have two multiples equally apart from str, choose the smallest element among them.

Examples:
Input: str = 29
Output: 30
Explanation: Close multiples are 20 and 30, and 30 is the nearest to 29.

Expected Time Complexity: O(n).
Expected Auxiliary Space: O(1).
Constraints: 1 <= str.size()<= 10^5
*/

//{ Driver Code Starts
#include <iostream>
using namespace std;

// } Driver Code Ends

class Solution
{
public:
    string roundToNearest(string str)
    {
        // Complete the function
        int len = str.length();
        int a = str[len - 1] - '0';

        if (a < 6) {
            str[len - 1] = '0';
            return str;
        }

        if (a > 6 && len == 1) 
            return "10";

        // str.replace(len - 1, 1, "0");
        string str_new = "0";
        int if_add = 1;
        for (int i = len - 2; i >= 0; i--) {
            int tmp = str[i] - '0';
            if(if_add && tmp < 9) {
                str_new.append(to_string(tmp + 1));
                if_add = 0;
            } else if (if_add && tmp > 8 && i != 0) {
                str_new.append("0");
            } else if (if_add && tmp > 8 && i == 0) {
                str_new.append("01");
            } else {
                str_new.push_back(str[i]);
            }
        }

        string str1 = "";
        for (int i = str_new.length() - 1; i >= 0; i--)
            str1.push_back(str_new[i]);

        return str1;
    }
};

// class Solution {
//   public:
//     string roundToNearest(string str) {
//         int n = str.size();

//         // If the last digit is less then or equal to 5
//         // then it can be rounded to the nearest
//         // (previous) multiple of 10 by just replacing
//         // the last digit with 0
//         if (str[n - 1] - '0' <= 5) {

//             // Set the last digit to 0
//             str[n - 1] = '0';

//             // Print the updated number
//             return str.substr(0, n);
//         }

//         // The number hast to be rounded to
//         // the next multiple of 10
//         else {

//             // To store the carry
//             int carry = 0;

//             // Replace the last digit with 0
//             str[n - 1] = '0';

//             // Starting from the second last digit, add 1
//             // to digits while there is carry
//             int i = n - 2;
//             carry = 1;

//             // While there are digits to consider
//             // and there is carry to add
//             while (i >= 0 && carry == 1) {

//                 // Get the current digit
//                 int currentDigit = str[i] - '0';

//                 // Add the carry
//                 currentDigit += carry;

//                 // If the digit exceeds 9 then
//                 // the carry will be generated
//                 if (currentDigit > 9) {
//                     carry = 1;
//                     currentDigit = 0;
//                 }

//                 // Else there will be no carry
//                 else
//                     carry = 0;

//                 // Update the current digit
//                 str[i] = (char)(currentDigit + '0');

//                 // Get to the previous digit
//                 i--;
//             }

//             // If the carry is still 1 then it must be
//             // inserted at the beginning of the string
//             if (carry == 1)
//                 cout << carry;

//             // Prin the rest of the number
//             return str.substr(0, n);
//         }
//     }
// };

//{ Driver Code Starts.

int main()
{

    int t;
    cin >> t;
    while (t--)
    {
        string str;
        cin >> str;
        Solution ob;
        cout << ob.roundToNearest(str) << endl;
    }

    return 0;
}
// } Driver Code Ends