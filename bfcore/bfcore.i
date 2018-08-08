/* Interface file */
%module bfcore
%{
#include "sudoku.hpp";
extern Sudoku::Sudoku(const int column, const int row, const int boxColumn, const int boxRow);
extern Sudoku::~Sudoku();
extern void Sudoku::read();
extern void Sudoku::print();
extern bool Sudoku::isEmpty(const int x,  const int y);
extern bool Sudoku::isValid(const int x, const int y, const int n);
extern bool Sudoku::isUsedInColumn(const int x, const int n);
extern bool Sudoku::isUsedInRow(const int y, const int n);
extern bool Sudoku::isUsedInBox(const int x, const int y, const int n);
extern void Sudoku::dfs(const int x, const int y);
%}

%include "sudoku.hpp";
extern Sudoku::Sudoku(const int column, const int row, const int boxColumn, const int boxRow);
extern Sudoku::~Sudoku();
extern void Sudoku::read();
extern void Sudoku::print();
extern bool Sudoku::isEmpty(const int x,  const int y);
extern bool Sudoku::isValid(const int x, const int y, const int n);
extern bool Sudoku::isUsedInColumn(const int x, const int n);
extern bool Sudoku::isUsedInRow(const int y, const int n);
extern bool Sudoku::isUsedInBox(const int x, const int y, const int n);
extern void Sudoku::dfs(const int x, const int y);