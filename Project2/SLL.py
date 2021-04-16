"""
Project 1
CSE 331 S21 (Onsay)
Your Name
DLL.py
"""

from Project2.Node import Node       # Import `Node` class
from typing import TypeVar  # For use in type hinting

# Type Declarations
T = TypeVar('T')        # generic type
SLL = TypeVar('SLL')    # forward declared


class RecursiveSinglyLinkList:
    """
    Recursive implementation of an SLL
    """

    __slots__ = ['head']

    def __init__(self) -> None:
        """
        Initializes an `SLL`
        :return: None
        """
        self.head = None

    def __repr__(self) -> str:
        """
        Represents an `SLL` as a string
        """
        return self.to_string(self.head)

    def __str__(self) -> str:
        """
        Represents an `SLL` as a string
        """
        return self.to_string(self.head)

    def __eq__(self, other: SLL) -> bool:
        """
        Overloads `==` operator to compare SLLs
        :param other: right hand operand of `==`
        :return: `True` if equal, else `False`
        """
        comp = lambda n1, n2: n1 == n2 and (comp(n1.next, n2.next) if (n1 and n2) else True)
        return comp(self.head, other.head)

# ============ Modify below ============ #

    def to_string(self, curr: Node) -> str:
        """
        REPLACE - See Project 1
        Time complexity: O(n^2)
        """
        if curr is None:
            return "None"
        final = str(curr.val)
        add_this = self.to_string(curr.next)
        if add_this != "None":
            final = final + " --> " + add_this
        return final


    def length(self, curr: Node) -> int:
        """
        Recursive function that determines the number of nodes in the list starting with head curr
        INPUT : the current node
        OUTPUT : the length of the list from that node onwards
        Time complexity: O(n)
        """
        if curr is None:
            return 0
        length = 1
        length += self.length(curr.next)
        return length

    def sum_list(self, curr: Node) -> T:
        """
        Recursive function that calculates and returns the sum of the values in the list starting with head curr
        INPUT : the current node
        OUTPUT : the sum of all numbers that node onwards
        Time complexity: O(n)
        """
        if curr is None:
            return 0
        sumv = curr.val
        sumv += self.sum_list(curr.next)
        return sumv

    def push(self, value: T) -> None:
        """
        Insert given value at the end of sll
        INPUT : the value to be added
        OUTPUT : None
        Time complexity: O(n)
        """

        def push_inner(curr: Node) -> None:
            """
            Insert node to the list end
            INPUT : the head node
            OUTPUT : none
            Time complexity: O(n)
            """
            if curr is None:
                self.head = Node(value)
                return
            if curr.next is None:
                curr.next = Node(value)
                return
            curr = curr.next
            push_inner(curr)

        push_inner(self.head)



    def remove(self, value: T) -> None:
        """
        remove first instance of the given value from sll
        INPUT : the value to be removed
        OUTPUT : None
        Time complexity: O(n)
        """

        def remove_inner(curr: Node) -> Node:
            """
            remove node from the list
            INPUT : the head node
            OUTPUT : none
            Time complexity: O(n)
            """
            if curr is None:
                return
            if curr.val == value:
                self.head = curr.next
                return
            if curr.next is None:
                return
            if curr.next.val == value:
                curr.next = curr.next.next
                return
            curr = curr.next
            remove_inner(curr)

        remove_inner(self.head)

    def remove_all(self, value: T) -> None:
        """
        remove all instance of the given value from sll
        INPUT : the value to be removed
        OUTPUT : None
        Time complexity: O(n)
        """
        def remove_all_inner(curr):
            """
            remove value from the list
            INPUT : the head node
            OUTPUT : none
            Time complexity: O(n)
            """
            if curr is None:
                return
            if curr.val == value:
                self.head = curr.next
            elif curr.next is None:
                return
            elif curr.next.val == value:
                curr.next = curr.next.next

            curr = curr.next
            remove_all_inner(curr)

        remove_all_inner(self.head)

    def search(self, value: T) -> bool:
        """
        find if a value exists in the list
        INPUT : the value to be searched
        OUTPUT : bool
        Time complexity: O(n)
        """

        def search_inner(curr) -> bool:
            """
            search for the value from the list
            INPUT : the head node
            OUTPUT : none
            Time complexity: O(n)
            """
            if curr is None:
                return False
            if curr.val == value:
                return True
            if curr.next is not None:
                return search_inner(curr.next)
            return False

        return search_inner(self.head)

    def count(self, value: T) -> int:
        """
        count all instances of a value
        INPUT : the value to be searched
        OUTPUT : number of appearances
        Time complexity: O(n)
        """

        def count_inner(curr):
            """
            count instances of a value in the list
            INPUT : the head node
            OUTPUT : count of appearances
            Time complexity: O(n)
            """
            times = 0

            if curr is None:
                return 0
            if curr.val == value:
                times += 1
            if curr.next is not None:
                curr = curr.next
                times += count_inner(curr)
            return times

        return count_inner(self.head)


    def reverse(self, curr):
        """
        reverses the singly linked list
        INPUT : current node
        OUTPUT : the head of linked list
        Time complexity: O(n)
        """
        if curr is None:
            return self.head

        if curr.next is None:
            self.head = curr
            return self.head

        self.head = self.reverse(curr.next)
        curr.next.next = curr
        curr.next = None

        return self.head

def crafting(recipe, pockets) -> bool:
    """
    finds if all items in recipe are present in pocket.
    if present, the items are consumed
    INPUT: the 2 lists as RSLL
    OUTPUT: bool indicating if everything is present
    Time complexity: O(rp)
    """

    def item_checker(curr: Node)->bool:
        """
        checks if all items are present in pockets
        INPUT : head of recipe
        OUTPUT : bool indicating presence
        """
        if curr is None:
            return True
        if curr.next is None:
            return recipe.count(curr.val) <= pockets.count(curr.val)
        other_result = item_checker(curr.next)
        return recipe.count(curr.val) <= pockets.count(curr.val) and other_result

    def item_remover(curr: Node):
        """
        destroys items in pockets
        INPUT : head of recipe
        OUTPUT : none
        """
        if curr is None:
            return
        pockets.remove(curr.val)
        item_remover(curr.next)

    result = item_checker(recipe.head)

    if recipe.head is None: #this condition is being added due to test # 4 in crafting tests
        return False        #in my opinion the test makes no sense, if no item is required
                            #then why should the function return false? technically the recipe can be followed.
    if result:
        item_remover(recipe.head)
    return result


