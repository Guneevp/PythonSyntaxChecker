"""Lab 9: Binary Search Trees

=== CSC148 Winter 2025 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains a few BinarySearchTree methods that you will implement.
Make sure you understand the *BST Property*; it will play an important role
in several of these methods.
"""
from __future__ import annotations
from typing import Any, Optional


class BinarySearchTree:
    """Binary Search Tree class.

    This class represents a binary tree satisfying the Binary Search Tree
    property: for every item, its value is >= all items stored in its left
    subtree, and <= all items stored in its right subtree.
    """
    # === Private Attributes ===
    # The item stored at the root of the tree, or None if the tree is empty.
    _root: Optional[Any]
    # The left subtree, or None if the tree is empty.
    _left: Optional[BinarySearchTree]
    # The right subtree, or None if the tree is empty.
    _right: Optional[BinarySearchTree]

    # === Representation Invariants ===
    #  - If self._root is None, then so are self._left and self._right.
    #    This represents an empty BST.
    #  - If self._root is not None, then self._left and self._right
    #    are BinarySearchTrees.
    #  - (BST Property) If self is not empty, then
    #    all items in self._left are <= self._root, and
    #    all items in self._right are >= self._root.

    def __init__(self, root: Optional[Any]) -> None:
        """Initialize a new BST containing only the given root value.

        If <root> is None, initialize an empty tree.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        """Return True if this BST is empty.

        >>> bst = BinarySearchTree(None)
        >>> bst.is_empty()
        True
        >>> bst = BinarySearchTree(10)
        >>> bst.is_empty()
        False
        """
        return self._root is None

    # -------------------------------------------------------------------------
    # Standard Container methods (search)
    # -------------------------------------------------------------------------
    def __contains__(self, item: Any) -> bool:
        """Return whether <item> is in this BST.

        >>> bst = BinarySearchTree(3)
        >>> bst._left = BinarySearchTree(2)
        >>> bst._right = BinarySearchTree(5)
        >>> 3 in bst
        True
        >>> 5 in bst
        True
        >>> 2 in bst
        True
        >>> 4 in bst
        False
        """
        if self.is_empty():
            return False
        elif item == self._root:
            return True
        elif item < self._root:
            return item in self._left   # or, self._left.__contains__(item)
        else:
            return item in self._right  # or, self._right.__contains__(item)

    # ------------------------------------------------------------------------
    # Deletion code from lecture (profiled in Task 3)
    # ------------------------------------------------------------------------
    def delete(self, item: Any) -> None:
        """Remove *one* occurrence of item from this BST.

        Do nothing if <item> is not in the BST.
        """
        if self.is_empty():
            pass
        elif self._root == item:
            self.delete_root()
        elif item < self._root:
            self._left.delete(item)
        else:
            self._right.delete(item)

    def delete_root(self) -> None:
        """Remove the root of this tree.

        Precondition: this tree is *non-empty*.
        """
        if self._left.is_empty() and self._right.is_empty():
            self._root = None
            self._left = None
            self._right = None
        elif self._left.is_empty():
            # "Promote" the right subtree.
            # Note that self = self._right does NOT work!
            self._root, self._left, self._right = \
                self._right._root, self._right._left, self._right._right
        elif self._right.is_empty():
            # "Promote" the left subtree.
            self._root, self._left, self._right = \
                self._left._root, self._left._left, self._left._right
        else:
            # Both subtrees are non-empty. Can shooe to replace the root
            # from either the max value of the left subtree, or the min value
            # of the right subtree. (Implementations are very similar.)
            self._root = self._left.extract_max()

    def extract_max(self) -> Any:
        """Remove and return the maximum item stored in this tree.

        Precondition: this tree is *non-empty*.
        """
        if self._right.is_empty():
            max_item = self._root
            # "Promote" the left subtree.
            # Alternate approach: call self.delete_root()!
            self._root, self._left, self._right = \
                self._left._root, self._left._left, self._left._right
            return max_item
        else:
            return self._right.extract_max()

    # -------------------------------------------------------------------------
    # Additional BST methods
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        """Return a string representation of this BST.

        This string uses indentation to show depth.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this BST.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            answer = depth * '  ' + str(self._root) + '\n'
            answer += self._left._str_indented(depth + 1)
            answer += self._right._str_indented(depth + 1)
            return answer

    # ------------------------------------------------------------------------
    # Task 1
    # ------------------------------------------------------------------------
    def height(self) -> int:
        """Return the height of this BST.

        >>> BinarySearchTree(None).height()
        0
        >>> bst = BinarySearchTree(7)
        >>> bst.height()
        1
        >>> bst._left = BinarySearchTree(5)
        >>> bst.height()
        2
        >>> bst._right = BinarySearchTree(9)
        >>> bst.height()
        2
        """
        if self.is_empty():
            return 0
        elif self._left.is_empty() and self._right.is_empty():
            return 1
        else:
            return max([self._left.height(), self._right.height()]) + 1


    # TODO: implement this method!
    def items_in_range(self, start: Any, end: Any) -> list:
        """Return the items in this BST between <start> and <end>, inclusive.

        Precondition: all items in this BST can be compared with <start> and
        <end>.
        The items should be returned in sorted order.

        As usual, use the BST property to minimize the number of recursive
        calls.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> bst.items_in_range(4, 11)
        [5, 7, 9, 11]
        >>> bst.items_in_range(10, 13)
        [11, 13]
        """
        if self.is_empty():
            return []
        elif start <= self._root <= end:
                return self._left.items_in_range(start, end) + [self._root] + self._right.items_in_range(start, end)
        elif self._root > end:
            return self._left.items_in_range(start, end)
        elif self._root < start:
            return self._right.items_in_range(start, end)
        else:
            return self._right.items_in_range(start, end)

    # ------------------------------------------------------------------------
    # Task 2
    # ------------------------------------------------------------------------
    # TODO: implement this method!
    def insert(self, item: Any) -> None:
        """Insert <item> into this BST, maintaining the BST property.

        Do not change positions of any other nodes.

        >>> bst = BinarySearchTree(10)
        >>> bst.insert(3)
        >>> bst.insert(20)
        >>> bst._root
        10
        >>> bst._left._root
        3
        >>> bst._right._root
        20
        """
        curr = self
        while not (curr._left.is_empty() and curr._right.is_empty()):
            if not curr._left.is_empty():
                if item< curr._root:
                    curr = curr._left
            else:
                if curr._root > item:
                    curr = curr._right


    # ------------------------------------------------------------------------
    # Task 4
    # ------------------------------------------------------------------------
    def rotate_right(self) -> None:
        """Rotate the BST clockwise, i.e. make the left subtree the root.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> right = BinarySearchTree(11)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> bst._left = left
        >>> bst._right = right
        >>> print(bst)
        7
          3
            2
            5
          11
        <BLANKLINE>
        >>> bst.rotate_right()
        >>> print(bst)
        3
          2
          7
            5
            11
        <BLANKLINE>
        >>> bst.rotate_right()
        >>> print(bst)
        2
          3
            7
              5
              11
        <BLANKLINE>
        """
        just_this_root = BinarySearchTree(self._root)
        just_this_root._right = self._right
        a = self._left._right
        self._left, self._root, self._right = self._left._left, self._left._root, just_this_root
        self._right._left = a

    def rotate_left(self) -> None:
        """Rotate the BST counter-clockwise,
        i.e. make the right subtree the root.

        >>> bst = BinarySearchTree(7)
        >>> left = BinarySearchTree(3)
        >>> left._left = BinarySearchTree(2)
        >>> left._right = BinarySearchTree(5)
        >>> right = BinarySearchTree(11)
        >>> right._left = BinarySearchTree(9)
        >>> right._right = BinarySearchTree(13)
        >>> bst._left = left
        >>> bst._right = right
        >>> print(bst)
        7
          3
            2
            5
          11
            9
            13
        <BLANKLINE>
        >>> bst.rotate_left()
        >>> print(bst)
        11
          7
            3
              2
              5
            9
          13
        <BLANKLINE>
        >>> bst.rotate_left()
        >>> print(bst)
        13
          11
            7
              3
                2
                5
              9
        <BLANKLINE>
        """
        # TODO: implement this method!
        just_this_root = BinarySearchTree(self._root)
        just_this_root._left = self._left
        a = self._right._left
        self._right, self._root, self._left = self._right._right, self._right._root, just_this_root
        self._left._right = a

    def __eq__(self: BinarySearchTree, other: BinarySearchTree) -> bool:
        """
        Returns True if the two BSTs are equal, False otherwise.
        Two BSTs are considered equal if they have the same structure and the same values at each node.
        >>> a = bst_from_sorted_list(list(range(9)))
        >>> b = bst_from_sorted_list(list(range(9)))
        >>> a == b
        True
        >>> a == BinarySearchTree(2)
        False
        """
        lst1 = get_items_helper(self)
        lst2 = get_items_helper(other)
        return lst1 == lst2
        # visited1 = []
        # visited2 = []
        # to_visit1 = [self]
        # to_visit2 = [other]
        # while to_visit1:
        #     curr = to_visit1.pop(0)
        #     visited1.append(curr)
        #     if not curr._left.is_empty():
        #         to_visit1.append(curr._left)
        #     if not curr._right.is_empty():
        #         to_visit1.append(curr._right)
        # while to_visit2:
        #     curr = to_visit2.pop(0)
        #     visited2.append(curr)
        #     if not curr._left.is_empty():
        #         to_visit2.append(curr._left)
        #     if not curr._right.is_empty():
        #         to_visit2.append(curr._right)
        # if len(visited1) != len(visited2):
        #     return False
        # for i in range(len(visited1)):
        #     if visited1[i]._root != visited2[i]._root:
        #         return False
        # return True

def is_balanced(tree: BinarySearchTree) -> bool:
    """
    Returns True if the tree is balanced, False otherwise.
    Recall that a tree is balanced iff the difference in height of the
    left and right subtrees of every node is at most 1.
    I.e: |height(left) - height(right)| <= 1 for every node in the tree.
    """
    if tree.is_empty():
        return True
    else:
        return all((abs(tree._left.height() - tree._right.height()) <= 1, is_balanced(tree._left), is_balanced(tree._right)))

def bst_from_sorted_list(values: list[int]) -> BinarySearchTree:
    """
    Given a list of sorted values, creates a balanced BST.
    Precondition: The list of values is sorted in ascending order. (What would happen if it was sorted in **descending** order?)
    >>> a = bst_from_sorted_list(list(range(9)))
    >>> a._root == 4
    True
    >>> is_balanced(a)
    True
    """
    if not values:
        return BinarySearchTree(None)
    copy = values.copy()
    middle = len(values) // 2
    top = BinarySearchTree(copy[middle])
    copy.pop(middle)
    top._left = bst_from_sorted_list(copy[:middle])
    top._right = bst_from_sorted_list(copy[middle:])
    return top

def __eq__(self: BinarySearchTree, other: BinarySearchTree) -> bool:
    """
    Returns True if the two BSTs are equal, False otherwise.
    Two BSTs are considered equal if they have the same structure and the same values at each node.
    >>> a = bst_from_sorted_list(list(range(9)))
    >>> b = bst_from_sorted_list(list(range(9)))
    >>> a == b
    True
    >>> a == BinarySearchTree(2)
    False
    """
    # if not self._root == other._root:
    #     return False
    # if not (isinstance(self._left, BinarySearchTree) == isinstance(other._left, BinarySearchTree)
    #         or isinstance(self._right, BinarySearchTree) == isinstance(other._right, BinarySearchTree)):
    #     return False
    # if not (self._left == other._left
    #     and self._right == other._right):
    #     return False
    # return True
        # iterative implementation
    # visited1 = [self]
    # visited2 = [other]
    # to_visit1 = [self]
    # to_visit2 = [other]
    # while to_visit1:
    #     curr = to_visit1.pop(0)
    #     visited1.append(curr)
    #     if not curr._left.is_empty():
    #         to_visit2.append(curr._left)
    #     if not curr._right.is_empty():
    #         to_visit2.append(curr._right)
    # while to_visit2:
    #     curr = to_visit2.pop(0)
    #     visited2.append(curr)
    #     if not curr._left.is_empty():
    #         to_visit2.append(curr._left)
    #     if not curr._right.is_empty():
    #         to_visit2.append(curr._right)
    # if len(visited1) != len(visited2):
    #     return False
    # for i in range(len(visited1)):
    #     if visited1[i]._root != visited2[i]._root:
    #         return False
    # return True
    #For equality 2


def get_items_helper(self: BinarySearchTree) -> list[Any]:
    if self.is_empty():
        return []
    else:
        return (get_items_helper(self._left) + [self._root]
                + get_items_helper(self._right))



if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all()
