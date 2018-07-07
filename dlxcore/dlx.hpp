/* 
 * Abstract data structure for 0-1 matrix
 * Used to solve exact cover problem
 * Sudoku is a typical ECP
 */

#ifndef DLX_H
#define DLX_H

#include <vector>

typedef class Node *pos;

class Node
{
public:
    pos left;
    pos right;
    pos up;
    pos down;
    int row;
    pos colHead;
};

class DancingLinks
{
public:
    DancingLinks(const int col = 0);
    ~DancingLinks();
    void InsertRow(const int row, const std::vector<int> &colvec);
    bool Solve();
    void PrintAnswer();

private:
    pos head;
    const int column;
    std::vector<int> ans;

    pos FindCol(const int col);
    void DeleteNode(const pos node);
    void DeleteDFS(const pos node);
    void UndeleteNode(const pos node);
    void UndeleteDFS(const pos node);
    void AddToAnswer(const pos node);
    void RemoveFromAnswer(const pos node);
};

#endif