#include "sudoku.hpp"

int main()
{
    // Read sudoku parameter
    int column, row;
    int boxColumn, boxRow;
    cin >> column >> row;
    cin >> boxColumn >> boxRow;

    // Initialize sudoku
    Sudoku sdk(column, row, boxColumn, boxRow);

    // Read cell
    sdk.read();

    // Solve it
    sdk.dfs(0, 0);

    return 0;
}