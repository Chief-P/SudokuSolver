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
    Sudoku(const int column, const int row, const int boxColumn, const int boxRow);
    ~Sudoku();
    void read();
    void dfs(const int x, const int y);

private:
    const int column;
    const int row;
    const int boxColumn;
    const int boxRow;
    vector2d grid;
    bool isSolved;
    int zeroNum;
    const int boxPerColumn;
    const int boxPerRow;

	bool isEmpty(const int x, const int y);
    bool isValid(const int x, const int y, const int n);
    bool isUsedInColumn(const int x, const int n);
    bool isUsedInRow(const int y, const int n);
    bool isUsedInBox(const int x, const int y, const int n);
    void print();
};

#endif