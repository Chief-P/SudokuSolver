#include <iostream>

typedef Node *pos;

class Node
{
public:
    bool data;
    pos left;
    pos right;
    pos up;
    pos down;
};

class DancingLinks
{
public:
    pos head;

    DancingLinks(const int col)
    {
        head = calloc(1, sizeof(struct Node));
        head->up = head->down = head;
        pos prev = head;
        pos cur;
        for (int i = 0; i < col; ++i)
        {
            cur = calloc(1, sizeof(struct Node));
            cur->data = i;
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

    }
};

void createdlx()
{

}