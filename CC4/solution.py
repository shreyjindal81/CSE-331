"""
Name
Coding Challenge 4
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from typing import List


def challenger_finder(stocks_list: List[int], k: int) -> List[int]:
    """
    this function lists the number of possible matches for each player
    INPUT : list of player stocks
    OUTPUT : list of corresponding matches.
    """
    result = []
    for i in range(len(stocks_list)):
        result.append(0)

    for i in range(0, len(stocks_list)-1):
        for j in range(i+1, len(stocks_list)):
            if abs(stocks_list[i] - stocks_list[j]) <= k:
                result[i] += 1
                result[j] += 1
    return result

