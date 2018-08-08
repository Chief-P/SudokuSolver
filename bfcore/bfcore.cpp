#include "sudoku.hpp"

Sudoku::Sudoku(const int column, const int row, const int boxColumn, const int boxRow)
  : isSolved(false), zeroNum(0),
	column(column), row(row),
    boxColumn(boxColumn), boxRow(boxRow),
    boxPerColumn(column / boxColumn), boxPerRow(row / boxRow),
    grid(row, vector<int>(column))
{
    if (row != column || row != boxColumn * boxRow)
        cout << "Wrong input!" << endl;
}

Sudoku::~Sudoku()
{
    if (!isSolved)
        cout << "No solution!" << endl;
}

void Sudoku::read()
{
    for (int i = 0; i < row; ++i)
        for (int j = 0; j < column; ++j)
        {
            cin >> grid[i][j];
            if (!grid[i][j])
            	++zeroNum;
        }
}

void Sudoku::print()
{
    cout << "Solution:" << endl;
    for (size_t i = 0; i < grid.size(); ++i)
    {
        for (size_t j = 0; j < grid[i].size(); ++j)
            cout << grid[i][j] << " ";
        cout << endl;
    }
}

bool Sudoku::isEmpty(const int x,  const int y)
{
	return !grid[y][x];
}

bool Sudoku::isValid(const int x, const int y, const int n)
{
    return !isUsedInColumn(x, n) && !isUsedInRow(y, n) && !isUsedInBox(x / boxColumn, y / boxRow, n);
}

// Memoization to optimize
bool Sudoku::isUsedInColumn(const int x, const int n)
{
    for (int i = 0; i < row; ++i)
        if (grid[i][x] == n)
            return true;

    return false;
}

bool Sudoku::isUsedInRow(const int y, const int n)
{
    for (int j = 0; j < column; ++j)
        if (grid[y][j] == n)
            return true;

    return false;
}

bool Sudoku::isUsedInBox(const int x, const int y, const int n)
{
    const int sx = x * boxColumn;
    const int tx = (x + 1) * boxColumn;
    const int sy = y * boxRow;
    const int ty = (y + 1) * boxRow;

    for (int i = sy; i < ty; ++i)
        for (int j = sx; j < tx; ++j)
            if (grid[i][j] == n)
                return true;
    
    return false;
}

void Sudoku::dfs(const int x, const int y) // Brute force
{
    if (!isEmpty(x, y))
    {
    	if (x != column - 1)
        	dfs(x + 1, y);
        else
            dfs(0, y + 1);
        
    	if (isSolved)
        	return;
	}
	else
	{
    	for (int n = 1; n <= row; ++n)
    	{		
        	if (isValid(x, y, n))
        	{
            	grid[y][x] = n;
            	--zeroNum;

            	// Search from up to bottom
            	if (!zeroNum) // Solved
    			{
        			isSolved = true;
        			print();
        			return;
    			}
    		
            	if (x != column - 1)
            	    dfs(x + 1, y);
            	else
            	    dfs(0, y + 1);

            	if (isSolved)
            	    return;

            	grid[y][x] = 0;
            	++zeroNum;
            }
        }
    }
}