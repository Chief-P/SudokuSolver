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
    pos colHead;
};

class DancingLinks
{
public:
    pos head;
    const int column;
    std::vector<int> ans;

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
            cur->colHead = cur;
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

    pos FindCol(const int col);
    void InsertRow(const int row, const std::vector<int> &colvec);
    void DeleteNode(const pos node);
    void DeleteDFS(const pos node);
    void UndeleteNode(const pos node);
    void UndeleteDFS(const pos node);
    void AddToAnswer(const pos node);
    void RemoveFromAnswer(const pos node);
    int DancingLinks::Solve();
};

// Linear search O(column)
pos DancingLinks::FindCol(const int col)
{
    pos cur = head;
    for (int i = 0; i <= col; ++i, cur = cur->right);

    return cur;
}

void DancingLinks::InsertRow(const int row, const std::vector<int> &colvec)
{
    pos prev = nullptr, cur, first;
    for (auto col : colvec)
    {
        pos colHead = FindCol(col);
        cur = new Node;
        cur->row = row;
        cur->colHead = colHead;
        cur->left = prev;
        if (prev != nullptr)
            prev->right = cur;
        else
            first = cur;
        cur->up = colHead->up;
        cur->down = colHead;
        colHead->up->down = cur;
        colHead->up = cur;
        prev = cur;
    }
    cur->right = first;
    first->left = cur;
}

void DancingLinks::DeleteNode(const pos node)
{
    node->left->right = node->right;
    node->right->left = node->left;
    node->up->down = node->down;
    node->down->up = node->up;
}

void DancingLinks::UndeleteNode(const pos node)
{
    node->left->right = node;
    node->right->left = node;
    node->up->down = node;
    node->down->up =  node;
}

// void DancingLinks::DeleteDFS(const pos node)
// {
//     DeleteNode(node);
//     if (node->row != -1 && node->right != node)
//         DeleteDFS(node->right);
//     if (node->down != node)
//         DeleteDFS(node->down);
// }

// void DancingLinks::UndeleteDFS(const pos node)
// {
//     UndeleteNode(node);
//     if (node->row != -1 && node->right != node)
//         UndeleteDFS(node->right);
//     if (node->down != node)
//         UndeleteDFS(node->down);
// }

void DancingLinks::AddToAnswer(const pos node)
{
    ans.push_back(node->row);
    for (pos i = node; i->right != i; i = i->right)
        for (pos j = i; j->down != j; j = j->down)
            for (pos k = j; k->right != k; k = k->right)
                DeleteNode(k);
}

void DancingLinks::RemoveFromAnswer(const pos node)
{
    ans.pop_back();
    for (pos i = node; i->right != node; i = i->right)
        for (pos j = i; j->down != i; j = j->down)
            for (pos k = j; k->right != j; k = k->right)
                UndeleteNode(k);
}

int DancingLinks::Solve()
{
    while (head->right != head)
    {
        if (head->right->down == head->right)
        {

        }
    }

    return 0;
}