"""
Name: Shrey Jindal
Project 3 - Hybrid Sorting
Developed by Sean Nguyen and Andrew Haas
Based on work by Zosha Korzecke and Olivia Mikola
CSE 331 Spring 2021
Professor Sebnem Onsay
"""
from typing import TypeVar, List, Callable

T = TypeVar("T")            # represents generic type


def merge_sort(data: List[T], threshold: int = 0,
               comparator: Callable[[T, T], bool] = lambda x, y: x <= y) -> int:
    """
    merge sort algorithm with inbuilt inversions counter
    INPUT : list of data to be sorted
            the comparator for comparison
    OUTPUT : integer value for inversion counter
    """
    inversion_counter = 0

    if threshold == 0:
        change_value = 1
    else:
        change_value = threshold
    if len(data) <= change_value:
        insertion_sort(data, comparator)
        return 0
    else:
        if len(data) < 2:
            return 0
        mid = len(data)//2
        d1 = data[:mid]
        d2 = data[mid:]
        inversion_counter += merge_sort(d1, threshold, comparator)
        inversion_counter += merge_sort(d2, threshold, comparator)
        i = j = 0
        while i + j < len(data):
            if j == len(d2) or (i < len(d1) and comparator(d1[i], d2[j])):
            #    inversion_counter += len(d2) - j
                data[i + j] = d1[i]
                i = i + 1
            else:
                inversion_counter += len(d1) - i
                data[i + j] = d2[j]
                j = j + 1

    if threshold != 0:
        return 0
    return inversion_counter


def insertion_sort(data: List[T], comparator: Callable[[T, T], bool] = lambda x, y: x <= y) -> None:
    """
    insertion sort algorithm
    INPUT : list of data to be sorted
            the comparator for comparison
    OUTPUT : none
    """
    n = len(data)
    for i in range(1,n):
        j = i
        while (j>0) and comparator(data[j], data[j-1]):
            data[j], data[j-1] = data[j-1], data[j]
            j -= 1


def hybrid_sort(data: List[T], threshold: int,
                comparator: Callable[[T, T], bool] = lambda x, y: x <= y) -> None:
    """
    hybrid sort algorithm
    INPUT : list of data to be sorted
            the comparator for comparison
    OUTPUT : none
    """
    merge_sort(data, threshold, comparator)


def inversions_count(data: List[T]) -> int:
    """
    inversion counter wrapper
    INPUT : list of data ot count inversion
    OUTPUT : inversion counter
    """
    data2 = []
    for i in data:
        data2.append(i)
    return merge_sort(data2)


def reverse_sort(data: List[T], threshold: int) -> None:
    """
    hybrid sort algorithm in reverse
    INPUT : list of data to be sorted
            threshold value
    OUTPUT : none
    """
    comparator: Callable[[T, T], bool] = lambda x, y: x >= y
    merge_sort(data, threshold, comparator)


def password_rate(password: str) -> float:
    """
    rates a string as a password
    INPUT : the string to rate
    OUTPUT : a float rating
    """
    unique = []
    total = []

    for i in password:
        total.append(i)
        if i not in unique:
            unique.append(i)

    inv = inversions_count(total)

    return (len(total)**.5)*(len(unique)**.5) + inv


def password_sort(data: List[str]) -> None:
    """
    sorts passwords from strongest to weakest
    INPUT : a list of strings to compare
    OUTPUT : none
    """
    dic = {}
    rating = []
    for i in range(len(data)):
        dic[password_rate(data[i])] = data[i]
        rating.append(password_rate(data[i]))
    data.clear()
    reverse_sort(rating,0)
    for i in range(len(rating)):
        data.append(dic[rating[i]])
