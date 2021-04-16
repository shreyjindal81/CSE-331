"""
Name
Coding Challenge 2
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from typing import List, Tuple
from CC2.linked_list import DLLNode, LinkedList


def pokemon_machine(pokemon: LinkedList, orders: List[Tuple]) -> LinkedList:
    """
    this functions updates the pokemon list based on a list of orders
    input : the pokemon list
            the order list
    output : the pokemon list
    """


    def add_pokemon(cur_node: DLLNode, added_pokemon: str) -> None:
        """
        This function adds a pokemon to the linked list
        input : cur_node the node after which pokemon to be added
                added_pokemon the name of the pokemon in the form of a string
        output : none
        """
        add_node = DLLNode(added_pokemon)
        add_node.prev = cur_node
        if cur_node.nxt is not None:
            add_node.nxt = cur_node.nxt
            cur_node.nxt.prev = add_node
        cur_node.nxt = add_node

    def remove_pokemon(cur_node: DLLNode) -> None:
        """
        this function removes an element from the list
        input: the node to be removed
        output : none
        """
        if cur_node.nxt is not None:
            if cur_node.prev is not None:
                cur_node.prev.nxt = cur_node.nxt
            cur_node.nxt.prev = cur_node.prev
        else:
            cur_node.prev.nxt = None

    def swap_pokemon(first_node: DLLNode, second_node: DLLNode) -> None:
        """
        this function swaps positions of 2 nodes
        input : the 2 nodes
        output : none
        """

        val = first_node.val
        first_node.val = second_node.val
        second_node.val = val


    def get_node(dll: LinkedList, index: int) -> DLLNode:
        """
        this function returns the node at the given index
        input : the list
                the index number
        output : the node
        """
        curr_node = dll.head
        for i in range(0, index):
            curr_node = curr_node.nxt
        return curr_node

    for tuplex in orders:
        if tuplex[0] == 'add':
            this_node = get_node(pokemon, tuplex[1])
            add_pokemon(this_node, tuplex[2])
        elif tuplex[0] == 'remove':
            this_node = get_node(pokemon, tuplex[1]+1)
            remove_pokemon(this_node)
        else:
            this_node1 = get_node(pokemon, tuplex[1]+1)
            this_node2 = get_node(pokemon, tuplex[2]+1)
            swap_pokemon(this_node1, this_node2)

    return pokemon
