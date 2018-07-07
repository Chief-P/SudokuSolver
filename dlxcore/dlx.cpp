#include <iostream>
#include "dlx.hpp"

DancingLinks::DancingLinks(const int col) : column(col)
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

DancingLinks::~DancingLinks()
{
    pos prev = head;
    for (int i = 0; i < column; ++i)
    {
        pos cur = prev->right;
        delete cur;
    }
    delete head;
}

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

bool DancingLinks::Solve()
{
    if (head->right == head)
        return true; // Trial success

    pos node = head->right->down;
    while (node != head->right)
    {
        AddToAnswer(node);
        if (Solve())
            return true;
        RemoveFromAnswer(node);
        node = node->down;
    }

    return false; // Trial error
}

void DancingLinks::PrintAnswer()
{
    for (auto i : ans)
        std::cout << i << " ";
    std::cout << std::endl;
}