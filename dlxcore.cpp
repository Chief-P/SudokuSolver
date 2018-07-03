/* 
 * Abstract data structure for 0-1 matrix
 * Used to solve exact cover problem
 * Sudoku is a typical ECP
 */

#include <iostream>
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
    int col;
};

class DancingLinks
{
public:
    pos head;
    const int column;

    DancingLinks(const int col = 0) : column(col)
    {
        head = new Node;
        head->up = head->down = head;
        pos prev = head;
        pos cur;
        for (int i = 0; i < column; ++i)
        {
            cur = new Node;
            cur->row = -1;
            cur->col = i;
            cur->up = cur->down = cur;
            cur->left = prev;
            prev->right = cur;
            prev = cur;
        }
        head->left = cur;
        cur->right = head;
    }

    ~DancingLinks()
    {
        pos prev = head;
        for (int i = 0; i < column; ++i)
        {
            pos cur = prev->right;
            
        }
    }

    void Insert(const int row, const std::vector<int> &colvec);
    pos FindCol(const int col);
};

// Linear search O(column)
pos DancingLinks::FindCol(const int col)
{
    pos cur = head;
    for (int i = 0; i <= col; ++i, cur = cur->right);

    return cur;
}

void DancingLinks::Insert(const int row, const std::vector<int> &colvec)
{
    pos prev = nullptr, cur, first;
    for (auto col : colvec)
    {
        pos colNode = FindCol(col);
        cur = new Node;
        cur->row = row;
        cur->col = col;
        cur->left = prev;
        if (prev != nullptr)
            prev->right = cur;
        else
            first = cur;
        cur->up = colNode->up;
        cur->down = colNode;
        colNode->up->down = cur;
        colNode->up = cur;
        prev = cur;
    }
    cur->right = first;
    first->left = cur;
}

void DancingLinks::Delete(const int )