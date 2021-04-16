"""
Name
Coding Challenge 3
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from typing import List


def finding_best_bot(bots_list: List[int]) -> int:
    """
    finds the index of the bot where the salmonid defeat count stopped 
    increasing in the given python list.
    INPUT : the list of integers to be examined
    OUTPUT : an integer representing the position of the bot
    """

    def finding_best_bot_helper(start: int, end: int):
        """
        finds the index of the bot where the salmonid defeat count stopped
        increasing in the given python list.
        INPUT : the indeces between which to examine
        OUTPUT : an integer representing the position of the bot
        """
        if start >= end:
            return start
        mid = (start+end)//2
        if bots_list[mid] < bots_list[mid+1]:
            return finding_best_bot_helper(mid+1, end)
        return finding_best_bot_helper(start, mid)


    return finding_best_bot_helper(0, len(bots_list)-1)+1
