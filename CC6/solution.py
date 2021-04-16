"""
Name: Shrey Jindal
Coding Challenge 6
CSE 331 Spring 2021
Professor Sebnem Onsay
"""


def gates_needed(departures, arrivals):
    """
    a function that taken in the departure and arrivals list
    and returns the number of maximiumn gate needs
    :param: departures a list of float
    :param: arrivals a list of floats
    :return: an int representing the max need
    :runtime complexity: O(n+m)
    """
    arr = 0
    dep = 0
    max_need = 0
    curr_need = 0
    while arr < len(arrivals) and dep < len(departures) + 1:
        if dep == len(departures):
            arr += 1
            curr_need += 1
        else:
            if arrivals[arr] == departures[dep]:
                arr += 1
                dep += 1
            elif arrivals[arr] > departures[dep]:
                dep += 1
                curr_need -= 1
            elif departures[dep] > arrivals[arr]:
                arr += 1
                curr_need += 1
        if curr_need > max_need:
            max_need = curr_need
    return max_need
