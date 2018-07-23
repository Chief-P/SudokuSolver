/*
 * 9 * 9 Sudoku implementation of dlx
 * 0-80 col:    (i * 9 + j) marks is (i, j) filled
 * 81-161 col:  80 + (i * 9 + n) marks is n in row i
 * 162-242 col: 161 + (j * 9 + n) marks is n in column j
 * 243-323 col: 242 + ((p * 3 + q) * 9 + n) marks is n in 3 * 3 box(p, q)
 */

#include <iostream>
#include <vector>
#include "dlx.hpp"

const int row = 9;
const int col = 9;
const int boxRow = 3;
const int boxCol = 3;
const int maxNum = 9;

void Insert(DancingLinks dlx, const int i, const int j, const int n)
{
    static int cnt = 0;
    int p = i / 3;
    int q = j / 3;
    int posFil = i * 9 + j;
    int posRow = 80 + (i * 9 + n);
    int posCol = 161 + (j * 9 + n);
    int posBox = 242 + ((p * 3 + q) * 9 + n);
    std::vector<int> vec{posFil, posRow, posCol, posBox};
    dlx.InsertRow(cnt++, vec);
}

int main(int argc, char const *argv[])
{
    const int dlxCol = 324;
    DancingLinks dlx(dlxCol);
    
    for (int i = 0; i < row; ++i)
        for (int j = 0; j < col; ++j)
        {
            int n;
            std::cin >> n;
            if (n != 0)
                Insert(dlx, i, j, n);
            else
            {
                for (int k = 1; k < maxNum; ++k)
                    Insert(dlx, i, j, k);
            }
        }

    std::cout << "ok" << std::endl;
    if (dlx.Solve())
    {
        std::cout << "err print" << std::endl;
        dlx.PrintAnswer();
    }
    else
        std::cout << "Error" << std::endl;
    
    return 0;
}
