"""
Shrey Jindal
Coding Challenge 5
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from typing import List


def check_walls_cover(walls: List[int]) -> List[int]:
    """
    finds the number of visible walls
    INPUT : list[int] the height of walls
    OUTPUT : list[int] corresponding number of visible walls
    TIME COMPLEXITY :  O(n)
    SPACE COMPLEXITY : O(n)
    """
    stack = []
    for i in range(len(walls)):
        m = walls[i]
        n = 0
        for j in range(i, len(walls)):
            if walls[j] > m:
                n += 1
                m = walls[j]
        stack.append(n)
    return stack




