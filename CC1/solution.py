"""
Name
Coding Challenge 1 - Love Is In The Air
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from typing import List, Tuple


def story_progression(answers: List[int], questions: List[Tuple[int, int]]) -> List[str]:
    """
    Determine if each tuple in the question list to check that range of the answer list
    to determine if that chunk results in a win or a loss for the player.
    It will be a win condition if the chunk contains a majority
    :param answers: list of 0’s and 1’s, 1 represents a correct choice, 0 otherwise
    :param questions: list of questions, is a list of tuple of length 2, where
           Element [0] is starting index of the interested range
           Element [1] is ending index of the interested range
    :return: A Python list of the same length as list of question,
            each element is either “Win” or “Lose,”
    """
    result = []
    for tup in questions:
        zeros = 0
        ones = 0
        for num in answers[tup[0]:tup[1]+1]:
            if num != 0:
                ones += 1
            else:
                zeros += 1
        if ones>zeros:
            result.append('Win')
        else:
            result.append('Lose')

    return result
