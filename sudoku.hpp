#ifndef SUDOKU_H
#define SUDOKU_H

#include <iostream>
#include <vector>

using std::cin;
using std::cout;
using std::endl;
using std::vector;

typedef vector<vector<int>> vector2d;

class Sudoku
{
public:
    const int column;
    const int row;
    const int boxColumn;
    const int boxRow;
    vector2d grid;

    Sudoku(int column, int row, int boxColumn, int boxRow)
      : isSolved(false), zeroNum(0),
		column(column), row(row),
        boxColumn(boxColumn), boxRow(boxRow),
        boxPerColumn(column / boxColumn), boxPerRow(row / boxRow),
        grid(row, vector<int>(column))
    {
        if (row != column || row != boxColumn * boxRow)
            cout << "Wrong input!" << endl;
    }

    ~Sudoku()
    {
        if (!isSolved)
            cout << "No solution!" << endl;
    }

	bool isEmpty(int x, int y);
    bool isValid(int x, int y, int n);
    bool isUsedInColumn(int x, int n);
    bool isUsedInRow(int y, int n);
    bool isUsedInBox(int x, int y, int n);
    void dfs(int x, int y);
    void read();
    void print();

private:
    bool isSolved;
    int zeroNum;
    const int boxPerColumn;
    const int boxPerRow;
};

#endif