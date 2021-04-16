"""
Shrey Jindal
Coding Challenge 8
CSE 331 Spring 2021
Professor Sebnem Onsay
"""

from typing import Set, Tuple, Dict
from CC8.InventoryItems import ItemInfo, ALL_ITEMS


class Bundle:
    """ Bundle Class """

    def __init__(self) -> None:
        """
        initializes the Bundle class
        """
        self.dict = {}
        self.total = 0

    def to_set(self) -> Set[Tuple[str, int]]:
        """
        converts Bundle to a set of tuples
        :returns: the set
        """
        sett = set()
        for key in self.dict:
            sett.add((key, self.dict[key]))

        return sett

    def add_to_bundle(self, item_name: str, amount: int) -> bool:
        """
        adds item to the bundle if possible
        :param: the name of the item
        :param: the amount to be added
        :returns: bool indicating if addition was successful or not
        """
        it_info = ALL_ITEMS[item_name]
        itvalue = it_info.amount_in_stack
        per_unit_place = 64 / itvalue
        total_required_space = per_unit_place * amount
        if self.total + total_required_space > 64:
            return False
        if item_name in self.dict:
            self.dict[item_name] += amount
            self.total += total_required_space
        else:
            self.dict[item_name] = amount
            self.total += total_required_space
        return True

    def remove_from_bundle(self, item_name: str, amount: int) -> bool:
        """
        remove item from bundle if possible
        :param: name of item
        :param: amount to be removed
        :returns: bool indicating if removal was successful
        """
        if item_name not in self.dict or self.dict[item_name] < amount:
            return False
        it_info = ALL_ITEMS[item_name]
        itvalue = it_info.amount_in_stack
        per_unit_place = 64 / itvalue
        self.dict[item_name] -= amount
        if self.dict[item_name] == 0:
            self.dict.pop(item_name)
        self.total -= amount * per_unit_place
        return True
