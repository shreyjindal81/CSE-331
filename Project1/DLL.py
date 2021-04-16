"""
Project 1
CSE 331 S21 (Onsay)
Shrey Jindal
DLL.py
"""

from typing import TypeVar, List, Tuple
import datetime

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")  # represents generic type
Node = TypeVar("Node")  # represents a Node object (forward-declare to use in Node __init__)


# pro tip: PyCharm auto-renders docstrings (the multiline strings under each function definition)
# in its "Documentation" view when written in the format we use here. Open the "Documentation"
# view to quickly see what a function does by placing your cursor on it and using CTRL + Q.
# https://www.jetbrains.com/help/pycharm/documentation-tool-window.html


class Node:
    """
    Implementation of a doubly linked list node.
    Do not modify.
    """
    __slots__ = ["value", "next", "prev"]

    def __init__(self, value: T, next: Node = None, prev: Node = None) -> None:
        """
        Construct a doubly linked list node.

        :param value: value held by the Node.
        :param next: reference to the next Node in the linked list.
        :param prev: reference to the previous Node in the linked list.
        :return: None.
        """
        self.next = next
        self.prev = prev
        self.value = value

    def __repr__(self) -> str:
        """
        Represents the Node as a string.

        :return: string representation of the Node.
        """
        return str(self.value)

    def __str__(self) -> str:
        """
        Represents the Node as a string.

        :return: string representation of the Node.
        """
        return str(self.value)


class DLL:
    """
    Implementation of a doubly linked list without padding nodes.
    Modify only below indicated line.
    """
    __slots__ = ["head", "tail", "size"]

    def __init__(self) -> None:
        """
        Construct an empty doubly linked list.

        :return: None.
        """
        self.head = self.tail = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        result = ""
        node = self.head
        while node is not None:
            result += str(node)
            if node.next is not None:
                result += " <-> "
            node = node.next
        return result

    def __str__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        return repr(self)

    # MODIFY BELOW #

    def empty(self) -> bool:
        """
        Return boolean indicating whether DLL is empty.

        Suggested time & space complexity (respectively): O(1) & O(1).

        :return: True if DLL is empty, else False.
        """
        return self.size == 0

    def push(self, val: T, back: bool = True) -> None:
        """
        Create Node containing `val` and add to back (or front) of DLL. Increment size by one.

        Suggested time & space complexity (respectively): O(1) & O(1).

        :param val: value to be added to the DLL.
        :param back: if True, add Node containing value to back (tail-end) of DLL;
            if False, add to front (head-end).
        :return: None.
        """
        self.size += 1
        if self.size == 1:
            self.head = Node(val)
            self.tail = self.head
            return
        if back:
            this_node = Node(val, self.tail, self.tail)
            this_node.next = None
            self.tail.next = this_node
            self.tail = this_node
        else:
            this_node = Node(val, self.head, self.head)
            this_node.prev = None
            self.head.prev = this_node
            self.head = this_node

    def pop(self, back: bool = True) -> None:
        """
        Remove Node from back (or front) of DLL. Decrement size by 1. If DLL is empty, do nothing.

        Suggested time & space complexity (respectively): O(1) & O(1).

        :param back: if True, remove Node from (tail-end) of DLL;
            if False, remove from front (head-end).
        :return: None.
        """
        if self.size == 0:
            return
        self.size -= 1
        if self.size == 0:
            self.head = None
            self.tail = None
            return
        if back:
            self.tail.prev.next = None
            self.tail = self.tail.prev
        else:
            self.head.next.prev = None
            self.head = self.head.next

    def from_list(self, source: List[T]) -> None:
        """
        Construct DLL from a standard Python list.

        Suggested time & space complexity (respectively): O(n) & O(n).

        :param source: standard Python list from which to construct DLL.
        :return: None.
        """
        for i in source:
            self.push(i)

    def to_list(self) -> List[T]:
        """
        Construct standard Python list from DLL.

        Suggested time & space complexity (respectively): O(n) & O(n).

        :return: standard Python list containing values stored in DLL.
        """
        result = []
        node = self.head
        while node is not None:
            result.append(node.value)
            node = node.next
        return result

    def find(self, val: T) -> Node:
        """
        Find first instance of `val` in the DLL and return associated Node object.

        Suggested time & space complexity (respectively): O(n) & O(1).

        :param val: value to be found in DLL.
        :return: first Node object in DLL containing `val`.
            If `val` does not exist in DLL, return None.
        """
        if self.head is None:
            return None
        result = self.head
        while result.value != val:
            if result.next is None:
                return None
            result = result.next

        return result

    def find_all(self, val: T) -> List[Node]:
        """
        Find all instances of `val` in DLL and return Node objects in standard Python list.

        Suggested time & space complexity (respectively): O(n) & O(n).

        :param val: value to be searched for in DLL.
        :return: Python list of all Node objects in DLL containing `val`.
            If `val` does not exist in DLL, return empty list.
        """
        result = []
        it = self.head
        while it is not None:
            if it.value == val:
                result.append(it)
            it = it.next
        return result

    def delete(self, val: T) -> bool:
        """
        Delete first instance of `val` in the DLL.

        Suggested time & space complexity (respectively): O(n) & O(1).

        :param val: value to be deleted from DLL.
        :return: True if Node containing `val` was deleted from DLL; else, False.
        """
        if self.size == 0:
            return False
        if self.size == 1:
            if self.head.value != val:
                return False
            self.head = None
            self.tail = None
            self.size = 0
            return True

        if self.head.value == val:
            self.head.next.prev = None
            self.head = self.head.next
            self.size -= 1
            return True

        curr_node = self.head
        while curr_node.next is not None:
            if curr_node.value == val:
                curr_node.prev.next = curr_node.next
                curr_node.next.prev = curr_node.prev
                self.size -= 1
                return True
            curr_node = curr_node.next

            if self.tail.value == val:
                self.tail.prev.next = None
                self.tail = self.tail.prev
                self.size -= 1
                return True

        return False

    def delete_all(self, val: T) -> int:
        """
        Delete all instances of `val` in the DLL.

        Suggested time & space complexity (respectively): O(n) & O(1).

        :param val: value to be deleted from DLL.
        :return: integer indicating the number of Nodes containing `val` deleted from DLL;
                 if no Node containing `val` exists in DLL, return 0.
        """
        result = 0
        b = True
        while b:
            b = self.delete(val)
            result += 1
        return result - 1

    def reverse(self) -> None:
        """
        Reverse DLL in-place by modifying all `next` and `prev` references of Nodes in the
        DLL and resetting the `head` and `tail` references.
        Must be implemented in-place for full credit. May not create new Node objects.

        Suggested time & space complexity (respectively): O(n) & O(1).

        :return: None.
        """
        curr_node = self.head
        while curr_node is not None:
            nxt = curr_node.next
            curr_node.next = curr_node.prev
            curr_node.prev = nxt
            curr_node = curr_node.prev
        head = self.head
        self.head = self.tail
        self.tail = head


class Stock:
    """
    Implementation of a stock price on a given day.
    Do not modify.
    """

    __slots__ = ["date", "price"]

    def __init__(self, date: datetime.date, price: float) -> None:
        """
        Construct a stock.

        :param date: date of stock.
        :param price: the price of the stock at the given date.
        """
        self.date = date
        self.price = price

    def __repr__(self) -> str:
        """
        Represents the Stock as a string.

        :return: string representation of the Stock.
        """
        return f"<{str(self.date)}, ${self.price}>"

    def __str__(self) -> str:
        """
        Represents the Stock as a string.

        :return: string representation of the Stock.
        """
        return repr(self)


def intellivest(stocks: DLL) -> Tuple[datetime.date, datetime.date, float]:
    """
    Given a DLL representing daily stock prices,
    find the optimal streak of days over which to invest.
    To be optimal, the streak of stock prices must:

        (1) Be strictly increasing, such that the price of the stock on day i+1
        is greater than the price of the stock on day i, and
        (2) Have the greatest total increase in stock price from
        the first day of the streak to the last.

    In other words, the optimal streak of days over which to invest is the one over which stock
    price increases by the greatest amount, without ever going down (or staying constant).

    Suggested time & space complexity (respectively): O(n) & O(1).

    :param stocks: DLL with Stock objects as node values, as defined above.
    :return: Tuple with the following elements:
        [0]: date: The date at which the optimal streak begins.
        [1]: date: The date at which the optimal streak ends.
        [2]: float: The (positive) change in stock price between the start and end
                dates of the streak.
    """

    if stocks.size == 0:
        return None, None, 0
    if stocks.size == 1:
        return stocks.head.value.date, stocks.head.value.date, 0
    curr_node = stocks.head
    start_value = 0.0
    current_profit = 0.0
    final_profit = 0.0
    final_start_date = stocks.head.value.date
    final_end_date = stocks.head.value.date
    current_start_date = stocks.head.value.date
    current_end_date = stocks.head.value.date
    running = False
    while curr_node.next is not None:
        if curr_node.value.price < curr_node.next.value.price:
            if not running:
                running = True
                current_start_date = curr_node.value.date
                start_value = curr_node.value.price
            if curr_node.next == stocks.tail:
                running = False
                current_end_date = curr_node.next.value.date
                current_profit = curr_node.next.value.price - start_value

        else:
            if running:
                running = False
                current_end_date = curr_node.value.date
                current_profit = curr_node.value.price - start_value
        if not running:
            if current_profit > final_profit:
                final_profit = current_profit
                final_end_date = current_end_date
                final_start_date = current_start_date
            profit = 0

        curr_node = curr_node.next
    result = (final_start_date, final_end_date, final_profit)
    return result
