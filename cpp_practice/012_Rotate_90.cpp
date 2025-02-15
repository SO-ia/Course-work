/*
    2024.11.05 -- 2024.11.21
    Rotate by 90 degree
    Given a square mat[][]. The task is to rotate it by 90 degrees in clockwise direction without using any extra space.

    Examples:

    Input: mat[][] = [[1 2 3], [4 5 6], [7 8 9]]
    Output:
    7 4 1 
    8 5 2
    9 6 3

    Input: mat[][] = [1 2], [3 4]
    Output:
    3 1 
    4 2
    
    Input: mat[][] = [[1]]
    Output:
    1

    Constraints:
    1 ≤ mat.size() ≤ 1000
    1 <= mat[][] <= 100
*/

//{ Driver Code Starts
// Initial template for C++

#include <bits/stdc++.h>
using namespace std;


// } Driver Code Ends
// User function template for C++

/* matrix : given input matrix, you are require
 to change it in place without using extra space */
void rotate(vector<vector<int>>& mat) {
    // Your code goes here
    int n = mat.size();
    for (int i = 0; i < n; i++) {
        for (int j = n - 1; j >= 0; j--) {
            // 每行从末尾 push 与行号相同的列元素
            mat[i].push_back(mat[j][i]);
        }
    }

    for (int i = 0; i < n; i++)
        mat[i].erase(mat[i].begin(), mat[i].begin()+n);
}


//{ Driver Code Starts.

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<vector<int> > matrix(n);
        for (int i = 0; i < n; i++) {
            matrix[i].resize(n);
            for (int j = 0; j < n; j++)
                cin >> matrix[i][j];
        }
        rotate(matrix);
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; j++)
                cout << matrix[i][j] << " ";
            cout << "\n";
        }

        cout << "~"
             << "\n";
    }
    return 0;
}

// } Driver Code Ends