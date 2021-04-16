"""
Your name here
Coding Challenge 7
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from __future__ import annotations  # allow self-reference
from typing import List, Optional
from AVLTree import Node, AVLTree


class TreeNode:
    """
    Tree Node that contains a value as well as left and right pointers
    """
    def __init__(self, val: int, left: TreeNode = None, right: TreeNode = None):
        self.val = val
        self.left = left
        self.right = right


def rewind_combo(points: List[int]) -> List[Optional[int]]:
    """
    creates a list of largest smaller element to the left
    :param: integer list that needs to be modified
    :returns: the new list
    """
    result = []
    for count, value in enumerate(points):
        tree = AVLTree()
        for i in range(count+1):
            tree.insert(points[i])
        max = tree.max(tree.origin)
        if max.value <
    return result

