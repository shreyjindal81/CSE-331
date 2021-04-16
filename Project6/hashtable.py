"""
Project 6
CSE 331 S21 (Onsay)
Shrey Jindal
hashtable.py
"""

from typing import TypeVar, List, Tuple

T = TypeVar("T")
HashNode = TypeVar("HashNode")
HashTable = TypeVar("HashTable")


class HashNode:
    """
    DO NOT EDIT
    """
    __slots__ = ["key", "value", "deleted"]

    def __init__(self, key: str, value: T, deleted: bool = False) -> None:
        self.key = key
        self.value = value
        self.deleted = deleted

    def __str__(self) -> str:
        return f"HashNode({self.key}, {self.value})"

    __repr__ = __str__

    def __eq__(self, other: HashNode) -> bool:
        return self.key == other.key and self.value == other.value

    def __iadd__(self, other: T) -> None:
        self.value += other


class HashTable:
    """
    Hash Table Class
    """
    __slots__ = ['capacity', 'size', 'table', 'prime_index']

    primes = (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
        89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
        281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389,
        397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617,
        619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739,
        743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
        863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991,
        997)

    def __init__(self, capacity: int = 8) -> None:
        """
        DO NOT EDIT
        Initializes hash table
        :param capacity: capacity of the hash table
        """
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

        i = 0
        while HashTable.primes[i] <= self.capacity:
            i += 1
        self.prime_index = i - 1

    def __eq__(self, other: HashTable) -> bool:
        """
        DO NOT EDIT
        Equality operator
        :param other: other hash table we are comparing with this one
        :return: bool if equal or not
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False
        for i in range(self.capacity):
            if self.table[i] != other.table[i]:
                return False
        return True

    def __str__(self) -> str:
        """
        DO NOT EDIT
        Represents the table as a string
        :return: string representation of the hash table
        """
        represent = ""
        bin_no = 0
        for item in self.table:
            represent += "[" + str(bin_no) + "]: " + str(item) + '\n'
            bin_no += 1
        return represent

    __repr__ = __str__

    def _hash_1(self, key: str) -> int:
        """
        ---DO NOT EDIT---
        Converts a string x into a bin number for our hash table
        :param key: key to be hashed
        :return: bin number to insert hash item at in our table, None if key is an empty string
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)
        return hashed_value % self.capacity

    def _hash_2(self, key: str) -> int:
        """
        ---DO NOT EDIT---
        Converts a string x into a hash
        :param key: key to be hashed
        :return: a hashed value
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)

        prime = HashTable.primes[self.prime_index]

        hashed_value = prime - (hashed_value % prime)
        if hashed_value % 2 == 0:
            hashed_value += 1
        return hashed_value

    def __len__(self) -> int:
        """
        gets size of map
        :return: int size of map
        """
        return self.size

    def __setitem__(self, key: str, value: T) -> None:
        """
        sets key,value pair in map
        :param: key
        :param: value
        """
        return self._insert(key, value)

    def __getitem__(self, key: str) -> T:
        """
        finds value associated with passed key
        :param: the key
        :return: the value if present
        """
        if self._get(key) is None:
            raise KeyError
        return self._get(key).value

    def __delitem__(self, key: str) -> None:
        """
        remove passed key from map
        :param: the key
        """
        if self._get(key) is None:
            raise KeyError
        return self._delete(key)

    def __contains__(self, key: str) -> bool:
        """
        tells if passed key exists in map
        :param: the key
        """
        return self._get(key) is not None

    def hash(self, key: str, inserting: bool = False) -> int:
        """
        provide appropriate index for a key
        :param: the key
        :param: insert bool
        :returns: the index
        """
        for i in range(len(self.table)):
            idx = (self._hash_1(key) + i * self._hash_2(key)) % len(self.table)
            if idx is None:
                return None
            if self.table[idx] is None or self.table[idx].deleted and \
                    inserting or self.table[idx].key == key:
                break
        return idx

    def _insert(self, key: str, value: T) -> None:
        """
        insert passed key,value pair in the map
        :param: key
        :param: value
        """
        add_node = self.table[self.hash(key, inserting=True)]
        if add_node is not None and add_node.key == key:
            add_node.value = value
            return
        self.table[self.hash(key, inserting=True)] = HashNode(key,value)
        self.size += 1

        if (self.size * 2) >= self.capacity:
            self._grow()

    def _get(self, key: str) -> HashNode:
        """
        find hashnode if passed key in map
        :param: key
        :returns: the hashnode
        """
        return None if self.hash(key) is None else self.table[self.hash(key)]

    def _delete(self, key: str) -> None:
        """
        delete passed key from map if present
        :param: key
        """
        if self.hash(key) and self.table[self.hash(key)] and self.table[self.hash(key)].key == key:
            self.table[self.hash(key)].value = None
            self.table[self.hash(key)].deleted = True
            self.table[self.hash(key)].key = None
            self.size -= 1


    def _grow(self) -> None:
        """
        double capacity of map and rearrange nodes
        """

        table = HashTable(self.capacity * 2)
        self.prime_index = table.prime_index
        i = 0
        while i < self.capacity:
            element = self.table[i]
            if element and not element.deleted:
                table._insert(element.key, element.value)
            i += 1

        self.table = table.table
        self.capacity = self.capacity * 2

    def update(self, pairs: List[Tuple[str, T]] = []) -> None:
        """
        update map based on data from passed list
        :param: list of key value pairs
        """
        for pair in pairs:
            self[pair[0]] = pair[1]

    def keys(self) -> List[str]:
        """
        enlist all keys in the map
        :returns: a list of all keys
        """
        listx = []
        for node in self.table:
            if node is not None:
                listx.append(node.key)
        return listx

    def values(self) -> List[T]:
        """
        enlist all values in a map
        :returns: a list of all values
        """
        listx = []
        for node in self.table:
            if node is not None:
                listx.append(node.value)
        return listx

    def items(self) -> List[Tuple[str, T]]:
        """
        enlist all key,value pairs in map
        :returns: list of all pairs
        """
        listx = []
        for node in self.table:
            if node is not None:
                listx.append((node.key, node.value))
        return listx

    def clear(self) -> None:
        """
        clear the table
        """
        self.size = 0
        self.table = self.capacity * [None]


class CataData:
    '''
    Cata Data Class
    '''
    def __init__(self) -> None:
        """
        initializes 2 maps for data processing
        """
        self.entry_log = HashTable()
        self.final_log = HashTable()

    def enter(self, idx: str, origin: str, time: int) -> None:
        """
        process entry data in cata system
        :param: id of user
        :param: origin station
        :param: time of entry
        """
        self.entry_log[idx] = (origin, time)

    def exit(self, idx: str, dest: str, time: int) -> None:
        """
        process exit data in cata system
        :param: id of user
        :param: dest station
        :param: time of exit
        """
        entry_data = self.entry_log[idx]
        name = entry_data[0] + dest
        delta = time - entry_data[1]
        if name in self.final_log:
            self.final_log[name].append(delta)
        else:
            self.final_log[name] = [delta]

    def get_average(self, origin: str, dest: str) -> float:
        """
        computes average travel time between stations
        :param: origin station
        :param: exit station
        :returns: average time
        """
        name = origin + dest
        if name not in self.final_log:
            return 0
        listx = self.final_log[name]
        return sum(listx)/len(listx)
