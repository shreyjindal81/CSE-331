"""
Shrey Jindal
Lukas Richters & Sean Nguyen
Inspired by: Anna De Biasi & Andrew McDonald
CC11 - Tries - Solution Code
CSE 331 Spring 2021
Professor Sebnem Onsay
"""

from __future__ import annotations
from typing import List
from collections import defaultdict


class Node:
    """
    The node class is used to implement a trie.
    """

    __slots__ = ["children", "is_end"]

    def __init__(self) -> None:
        """
        Constructs a Node.
        """
        self.children = defaultdict(Node)
        self.is_end = False

    def __str__(self) -> str:
        """
        Returns a string representation of the node.
        """
        return "Node"

    def __repr__(self) -> str:
        """
        Returns a string representation of the node.
        """
        return str(self)


class Trie:
    """
    A trie is a type of tree data structure designed to allow for similar functionality to a
    Python dictionary.
    """

    __slots__ = ["root"]

    def __init__(self) -> None:
        """
        Initializes a root and a size.
        """
        self.root = Node()

    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        :param word: the word to insert.
        :return: None
        """

        # If no word is given, nothing to insert.
        if len(word) == 0:
            return
        # Get the root node.
        node = self.root

        # Iterate through each character in the word to set the given value.
        for char in word:
            node = node.children[char]

        # Mark the end of the word
        node.is_end = True

    def __str__(self) -> str:
        """
        Returns a string representation of the trie.
        :return: None
        """

        def pretty_print(node: Node, prefix: str, string: str) -> str:

            for child, c_node in node.children.items():
                if c_node.is_end > 0:
                    string += f"{prefix}{child}, "
                else:
                    string = pretty_print(c_node, prefix + child, string)

            return string

        return pretty_print(self.root, '', 'Trie<')[:-2] + '>'

    def __repr__(self) -> str:
        """
        Returns a string representation of the trie.
        :return: None
        """
        return str(self)


def enemy_revealer(trie: Trie, key: str) -> List[str]:
    """
    reveal all the enemies
    :param: trie structure with all names
    :param: key the search criteria
    :returns: a list of filtered names
    """
    def inner_revealer(node, idx, capcount, curr_val):
        """
        helper recursive function for outer function
        :param: node the node at which the recursion currently stands
        :param: idx index of key at which we currently sit
        :param: capcount the number of capitals already traversed
        :param: curr_val the current value
        """
        if idx >= len(key):
            focus = ""
        else:
            focus = key[idx]

        for chara in node.children:
            if chara == focus:
                int_val = curr_val + focus
                focus_node = node.children[focus]
                int_cap = capcount
                if focus.isupper():
                    int_cap += 1
                if int_cap > caps:
                    return
                if focus_node.is_end and idx >= len(key) - 1:
                    final.append(int_val)
                inner_revealer(focus_node, idx + 1, int_cap, int_val)
            else:
                gchild = node.children[chara]
                int_val = curr_val + chara
                if gchild.is_end and idx >= len(key):
                    final.append(int_val)
                if chara.islower():
                    inner_revealer(node.children[chara], idx, capcount, int_val)
                elif capcount + 1 <= caps:
                    inner_revealer(node.children[chara], idx, capcount + 1, int_val)

    final = []
    caps = 0
    for i in key:
        if i.isupper():
            caps += 1

    inner_revealer(trie.root, 0, 0, "")
    return final



