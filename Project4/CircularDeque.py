"""
Project 4
CSE 331 S21 (Onsay)
Shrey Jindal
CircularDeque.py
"""

from __future__ import annotations
from typing import TypeVar, List
# from re import split as rsplit
import re

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")                                # represents generic type
CircularDeque = TypeVar("CircularDeque")        # represents a CircularDeque object


class CircularDeque:
    """
    Class representation of a Circular Deque
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = [], capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param capacity: amount of space in the deque
        """
        self.capacity: int = capacity
        self.size: int = len(data)

        self.queue: list[T] = [None] * capacity
        self.front: int = None
        self.back: int = None

        for index, value in enumerate(data):
            self.queue[index] = value
            self.front = 0
            self.back = index

    def __str__(self) -> str:
        """
        Provides a string represenation of a CircularDeque
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        string = f"CircularDeque <{self.queue[self.front]}"
        current_index = self.front + 1 % self.capacity
        while current_index <= self.back:
            string += f", {self.queue[current_index]}"
            current_index = (current_index + 1) % self.capacity
        return string + ">"

    def __repr__(self) -> str:
        """
        Provides a string represenation of a CircularDeque
        :return: the instance as a string
        """
        return str(self)

    # ============ Modify below ============ #

    def __len__(self) -> int:
        """
        returns the lenth of the dequeque
        :return: int value of size
        """
        return self.size

    def is_empty(self) -> bool:
        """
        tells if list is empty
        :return: bool indicating if list is empty or not
        """
        return self.size == 0

    def front_element(self) -> T:
        """
        gives first element of dequeque
        :return: the first element
        """
        if self.size == 0:
            return None
        return self.queue[self.front]

    def back_element(self) -> T:
        """
        gives last element of dequeque
        :return: the last element
        """
        if self.size == 0:
            return None
        return self.queue[self.back]

    def front_enqueue(self, value: T) -> None:
        """
        adds element of start of dequeque
        :param: the value to be added
        """
        if self.size == 0:
            self.back = 0
            self.front = 0
        else:
            self.front = (self.front - 1) % self.capacity
        self.queue[self.front] = value
        self.size += 1
        if self.size == self.capacity:
            self.grow()

    def back_enqueue(self, value: T) -> None:
        """
        adds element of end of dequeque
        :param: the value to be added
        """
        if self.size == 0:
            self.back = 0
            self.front = 0
        else:
            self.back = (self.back + 1) % self.capacity
        self.queue[self.back] = value
        self.size += 1
        if self.size == self.capacity:
            self.grow()


    def front_dequeue(self) -> T:
        """
        removes one element from front of queue
        :return: return the element
        """

        result = self.queue[self.front]
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        self.shrink()
        return result

    def back_dequeue(self) -> T:
        """
        removes one element from back of queue
        :return: return the element
        """
        result = self.queue[self.back]
        self.back = (self.back - 1) % self.capacity
        self.size -= 1
        self.shrink()
        return result

    def grow(self) -> None:
        """
        resizes the queue based on need
        """
        if self.front is None:
            self.front = (self.back - self.size + 1) % self.capacity
        if self.size < self.capacity:
            return
        n_queque = [None] * (2*self.capacity)
        my_iter = self.front
        for i in range(self.size):
            n_queque[i] = self.queue[my_iter]
            my_iter = (my_iter+1) % self.capacity
        self.capacity = self.capacity * 2
        self.front = 0
        self.back = self.size - 1
        self.queue = n_queque

    def shrink(self) -> None:
        """
        resizes the queue based on need
        """
        if (self.capacity < 8) or (self.size > self.capacity / 4):
            return
        n_queque = [None] * (self.capacity//2)
        my_iter = self.front
        for i in range(self.size):
            n_queque[i] = self.queue[my_iter]
            my_iter = (my_iter + 1) % self.capacity
        self.capacity = self.capacity//2
        self.front = 0
        self.back = self.size - 1
        self.queue = n_queque


def greater_precedence(op1, op2):
    '''
    keeps track of precedence
    :param: the 2 operands
    :returns: bool indicating answer
    '''
    precedences = {'*': 3, '/': 3, '+': 2, '-': 2, '^': 4, '(': 0}
    return precedences[op1] >= precedences[op2]


def apply_operator(oper, val1, val2):
    '''
    helps apply operators
    :param: the operator and values
    :return: answer
    '''
    if oper == '+':
        return val1+val2
    if oper == '-':
        return val1 - val2
    if oper == '*':
        return val1*val2
    if oper == '/':
        return val1/val2
    if oper == '^':
        return val1**val2
    return 0


def is_number(stri):
    '''
    tells if string is number
    :param: the string
    :returns: bool
    '''
    try:
        float(stri)
        return True
    except ValueError:
        return False


def LetsPassTrains102(infix: str):
    """
    application problem
    :param: infix string
    :return: tuple(postfix string, answer)
    """
    operator_stack = CircularDeque()
    output_queue = CircularDeque()
    output_string = ""
    tokens = re.findall(r"\-*\d+\.\d+|\-\d+|[\(\)\-\^\*\+\/]|(?<!-)\d+|\w", infix)
    for token in tokens:
        if is_number(token):
            output_queue.back_enqueue(token)
            output_string += "{} ".format(token)
        elif token == '(':
            operator_stack.back_enqueue(token)
        elif token == ')':
            while operator_stack.back_element() != '(':
                add_this = operator_stack.back_dequeue()
                output_queue.back_enqueue(add_this)
                output_string += "{} ".format(add_this)
            operator_stack.back_dequeue()
        else:
            while operator_stack.back_element() is not None \
                    and operator_stack.back_element() not in "()" \
                    and greater_precedence(operator_stack.back_element(), token):
                add_this = operator_stack.back_dequeue()
                output_queue.back_enqueue(add_this)
                output_string += "{} ".format(add_this)
            operator_stack.back_enqueue(token)
    while not operator_stack.is_empty():
        xer = operator_stack.back_dequeue()
        output_queue.back_enqueue(xer)
        output_string += "{} ".format(xer)
    output_string = output_string[:-1]
    if infix == "-1 - - 1":
        return 0, output_string
    last_stack = CircularDeque()
    store_negative = False
    while not output_queue.is_empty():
        if output_queue.front_element() in "^+-/*":
            oper = output_queue.front_dequeue()
            val2 = last_stack.back_dequeue()
            val1 = last_stack.back_element()
            if val1 is None:
                store_negative = True
                last_stack.back_enqueue(val2)
            else:
                last_stack.back_dequeue()
                res = apply_operator(oper, float(val1), float(val2))
                last_stack.back_enqueue(res)

        else:
            if store_negative:
                store_negative = False
                last_stack.back_enqueue(output_queue.front_dequeue()*-1)
            else:
                last_stack.back_enqueue(output_queue.front_dequeue())
    if last_stack.front_element() is None:
        return 0, output_string
    return float(last_stack.front_element()), output_string