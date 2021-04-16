"""
Project 5
CSE 331 S21 (Onsay)
Your Name
AVLTree.py
"""

import queue
from typing import TypeVar, Generator, List, Tuple

# for more information on typehinting, check out https://docs.python.org/3/library/typing.html
T = TypeVar("T")            # represents generic type
Node = TypeVar("Node")      # represents a Node object (forward-declare to use in Node __init__)
AVLWrappedDictionary = TypeVar("AVLWrappedDictionary")      # represents a custom type used in application


####################################################################################################


class Node:
    """
    Implementation of an AVL tree node.
    Do not modify.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["value", "parent", "left", "right", "height"]

    def __init__(self, value: T, parent: Node = None,
                 left: Node = None, right: Node = None) -> None:
        """
        Construct an AVL tree node.

        :param value: value held by the node object
        :param parent: ref to parent node of which this node is a child
        :param left: ref to left child node of this node
        :param right: ref to right child node of this node
        """
        self.value = value
        self.parent, self.left, self.right = parent, left, right
        self.height = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return f"<{str(self.value)}>"

    def __str__(self) -> str:
        """
        Represent the AVL tree node as a string.

        :return: string representation of the node.
        """
        return f"<{str(self.value)}>"


####################################################################################################


class AVLTree:
    """
    Implementation of an AVL tree.
    Modify only below indicated line.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["origin", "size"]

    def __init__(self) -> None:
        """
        Construct an empty AVL tree.
        """
        self.origin = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the AVL tree as a string. Inspired by Anna De Biasi (Fall'20 Lead TA).

        :return: string representation of the AVL tree
        """
        if self.origin is None:
            return "Empty AVL Tree"

        # initialize helpers for tree traversal
        root = self.origin
        result = ""
        q = queue.SimpleQueue()
        levels = {}
        q.put((root, 0, root.parent))
        for i in range(self.origin.height + 1):
            levels[i] = []

        # traverse tree to get node representations
        while not q.empty():
            node, level, parent = q.get()
            if level > self.origin.height:
                break
            levels[level].append((node, level, parent))

            if node is None:
                q.put((None, level + 1, None))
                q.put((None, level + 1, None))
                continue

            if node.left:
                q.put((node.left, level + 1, node))
            else:
                q.put((None, level + 1, None))

            if node.right:
                q.put((node.right, level + 1, node))
            else:
                q.put((None, level + 1, None))

        # construct tree using traversal
        spaces = pow(2, self.origin.height) * 12
        result += "\n"
        result += f"AVL Tree: size = {self.size}, height = {self.origin.height}".center(spaces)
        result += "\n\n"
        for i in range(self.origin.height + 1):
            result += f"Level {i}: "
            for node, level, parent in levels[i]:
                level = pow(2, i)
                space = int(round(spaces / level))
                if node is None:
                    result += " " * space
                    continue
                if not isinstance(self.origin.value, AVLWrappedDictionary):
                    result += f"{node} ({parent} {node.height})".center(space, " ")
                else:
                    result += f"{node}".center(space, " ")
            result += "\n"
        return result

    def __str__(self) -> str:
        """
        Represent the AVL tree as a string. Inspired by Anna De Biasi (Fall'20 Lead TA).

        :return: string representation of the AVL tree
        """
        return repr(self)

    def height(self, root: Node) -> int:
        """
        Return height of a subtree in the AVL tree, properly handling the case of root = None.
        Recall that the height of an empty subtree is -1.

        :param root: root node of subtree to be measured
        :return: height of subtree rooted at `root` parameter
        """
        return root.height if root is not None else -1

    def left_rotate(self, root: Node) -> Node:
        """
        Perform a left rotation on the subtree rooted at `root`. Return new subtree root.

        :param root: root node of unbalanced subtree to be rotated.
        :return: new root node of subtree following rotation.
        """
        if root is None:
            return None

        new_root, rl_child = root.right, root.right.left
        root.right = rl_child
        if rl_child is not None:
            rl_child.parent = root

        new_root.left = root
        new_root.parent = root.parent
        if root.parent is not None:
            if root is root.parent.left:
                root.parent.left = new_root
            else:
                root.parent.right = new_root
        root.parent = new_root

        if root is self.origin:
            self.origin = new_root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        new_root.height = 1 + max(self.height(new_root.left), self.height(new_root.right))
        return new_root

    ########################################
    # Implement functions below this line. #
    ########################################

    def right_rotate(self, root: Node) -> Node:
        """
        Perform a right rotation on the subtree rooted at `root`. Return new subtree root.

        :param root: root node of unbalanced subtree to be rotated.
        :return: new root node of subtree following rotation.
        """

        if root is None:
            return None

        new_root, lr_child = root.left, root.left.right
        root.left = lr_child
        if lr_child is not None:
            lr_child.parent = root

        new_root.right = root
        new_root.parent = root.parent
        if root.parent is not None:
            if root is root.parent.right:
                root.parent.right = new_root
            else:
                root.parent.left = new_root
        root.parent = new_root

        if root is self.origin:
            self.origin = new_root

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        new_root.height = 1 + max(self.height(new_root.left), self.height(new_root.right))
        return new_root

    def balance_factor(self, root: Node) -> int:
        """
        finds the balance factor of the passed node

        :param: the node at which to compute the balance factor
        :return: the balance factor
        :time complexity: O(1)
        :space complexity: O(1)
        """
        return 0 if root is None else self.height(root.left) - self.height(root.right)

    def rebalance(self, root: Node) -> Node:
        """
        re-balance the subtree rooted at root (if necessary)

        :param: the root node of subtree
        :return: the root node of balanced subtree
        :time complexity: O(1)
        """
        if root is None:
            return None
        root.height = 1 + max(self.height(root.left), self.height(root.right))
        factor = self.balance_factor(root)
        if abs(factor) < 2:
            return root
        if factor < -1:
            if self.balance_factor(root.right) == 1:
                self.right_rotate(root.right)
            return self.left_rotate(root)
        if factor > 1:
            if self.balance_factor(root.left) == -1:
                self.left_rotate(root.left)
        return self.right_rotate(root)

    def insert(self, root: Node, val: T) -> Node:
        """
        insert new node to the AVL
        :param: the value to be inserted
        :param: the root node of subtree
        :returns: new root node of adjusted subtree
        """
        if self.origin is None:
            self.size += 1
            self.origin = Node(val)
            return self.origin

        if root.value == val:
            return self.rebalance(root)

        if val < root.value and root.left is not None:
            self.insert(root.left, val)

        elif val > root.value and root.right is None:
            root.right = Node(val, parent=root)
            self.size += 1

        elif val < root.value and root.left is None:
            self.size += 1
            root.left = Node(val, parent=root)

        elif val > root.value and root.right is not None:
            self.insert(root.right, val)

        root.height = 1 + max(self.height(root.left), self.height(root.right))

        root_node = self.rebalance(root)

        return root_node

    def min(self, root: Node) -> Node:
        """
        find min value of subtree
        :param: root of subtree
        :return: the min node
        """
        if root is None:
            return root
        if root.left is None:
            return root
        return self.min(root.left)

    def max(self, root: Node) -> Node:
        """
        find max value of subtree
        :param: root of subtree
        :return: the max node
        """
        if root is None:
            return root
        if root.right is None:
            return root
        return self.max(root.right)

    def search(self, root: Node, val: T) -> Node:
        """
        search the subtree for a given value:
        :param: the root of subtree
        :param: the value to be searched
        :return: the node value below which val would be inserted
                or the node itself if found
        """
        if root is None:
            return root
        if val == root.value:
            return root
        if val < root.value:
            if root.left is None:
                return root
            else:
                return self.search(root.left, val)
        if val > root.value:
            if root.right is None:
                return root
            else:
                return self.search(root.right, val)

    def inorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a in-order traversal of the subtree
        :param: the root of subtree
        :returns: Generator Object
        """
        if root is None:
            return None

        yield from self.inorder(root.left) if root.left else ()

        yield root

        yield from self.inorder(root.right) if root.right else ()

    def preorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a pre-order traversal of the subtree
        :param: the root of subtree
        :returns: Generator Object
        """
        if root is None:
            return None

        yield root

        yield from self.preorder(root.left) if root.left else ()

        yield from self.preorder(root.right) if root.right else ()

    def postorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a post-order traversal of the subtree
        :param: the root of subtree
        :returns: Generator Object
        """
        if root is None:
            return None

        yield from self.postorder(root.left) if root.left else ()

        yield from self.postorder(root.right) if root.right else ()

        yield root

    def levelorder(self, root: Node) -> Generator[Node, None, None]:
        """
        Perform a level-order (breadth-first) traversal of the subtree
        :param: the root of subtree
        :returns: Generator Object
        """
        if root is None:
            return root

        out = queue.SimpleQueue()

        out.put(root)

        while out.empty() is False:
            sec_root = out.get()
            yield sec_root

            if sec_root.left:
                out.put(sec_root.left)

            if sec_root.right:
                out.put(sec_root.right)

    def remove(self, root: Node, val: T) -> Node:
        """
        Remove the node with value val from the subtree rooted at root, and
        return the root of the balanced subtree following removal.
        :param: root: Node: The root Node of the subtree from which to delete val.
        :param: val: T: The value to be deleted from the subtree rooted at root.
        :return: Root of new subtree after removal and rebalancing (could be the original root).
        """

        res1 = self.search(root, val)
        if res1.value != val or res1 is None:
            return

        if res1.left is None and res1.right is None:
            par = res1.parent
            if par is None:
                root = None
            elif par.right is not None and par.right.value == val:
                par.right = None
            else:
                par.left = None
            self.size -= 1
            return

        if res1.right is None or res1.left is None:
            par = res1.parent
            if res1.right is None:
                child = res1.left
            else:
                child = res1.right
            if par is None:
                root = child




    ####################################################################################################


class AVLWrappedDictionary:
    """
    Implementation of a helper class which will be used as tree node values in the
    NearestNeighborClassifier implementation. Compares objects with keys less than
    1e-6 apart as equal.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["key", "dictionary"]

    def __init__(self, key: float) -> None:
        """
        Construct a AVLWrappedDictionary with a key to search/sort on and a dictionary to hold data.

        :param key: floating point key to be looked up by.
        """
        self.key = key
        self.dictionary = {}

    def __repr__(self) -> str:
        """
        Represent the AVLWrappedDictionary as a string.

        :return: string representation of the AVLWrappedDictionary.
        """
        return f"key: {self.key}, dict: {self.dictionary}"

    def __str__(self) -> str:
        """
        Represent the AVLWrappedDictionary as a string.

        :return: string representation of the AVLWrappedDictionary.
        """
        return f"key: {self.key}, dict: {self.dictionary}"

    def __eq__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement == operator to compare 2 AVLWrappedDictionaries by key only.
        Compares objects with keys less than 1e-6 apart as equal.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating whether keys of AVLWrappedDictionaries are equal
        """
        return abs(self.key - other.key) < 1e-6

    def __lt__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement < operator to compare 2 AVLWrappedDictionarys by key only.
        Compares objects with keys less than 1e-6 apart as equal.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating ordering of AVLWrappedDictionaries
        """
        return self.key < other.key and not abs(self.key - other.key) < 1e-6

    def __gt__(self, other: AVLWrappedDictionary) -> bool:
        """
        Implement > operator to compare 2 AVLWrappedDictionaries by key only.
        Compares objects with keys less than 1e-6 apart as equal.

        :param other: other AVLWrappedDictionary to compare with
        :return: boolean indicating ordering of AVLWrappedDictionaries
        """
        return self.key > other.key and not abs(self.key - other.key) < 1e-6


class NearestNeighborClassifier:
    """
    Implementation of a one-dimensional nearest-neighbor classifier with AVL tree lookups.
    Modify only below indicated line.
    """
    # preallocate storage: see https://stackoverflow.com/questions/472000/usage-of-slots
    __slots__ = ["resolution", "tree"]

    def __init__(self, resolution: int) -> None:
        """
        Construct a one-dimensional nearest neighbor classifier with AVL tree lookups.
        Data are assumed to be floating point values in the closed interval [0, 1].

        :param resolution: number of decimal places the data will be rounded to, effectively
                           governing the capacity of the model - for example, with a resolution of
                           1, the classifier could maintain up to 11 nodes, spaced 0.1 apart - with
                           a resolution of 2, the classifier could maintain 101 nodes, spaced 0.01
                           apart, and so on - the maximum number of nodes is bounded by
                           10^(resolution) + 1.
        """
        self.tree = AVLTree()
        self.resolution = resolution

        # pre-construct lookup tree with AVLWrappedDictionary objects storing (key, dictionary)
        # pairs, but which compare with <, >, == on key only
        for i in range(10**resolution + 1):
            w_dict = AVLWrappedDictionary(key=(i/10**resolution))
            self.tree.insert(self.tree.origin, w_dict)

    def __repr__(self) -> str:
        """
        Represent the NearestNeighborClassifier as a string.

        :return: string representation of the NearestNeighborClassifier.
        """
        return f"NNC(resolution={self.resolution}):\n{self.tree}"

    def __str__(self) -> str:
        """
        Represent the NearestNeighborClassifier as a string.

        :return: string representation of the NearestNeighborClassifier.
        """
        return f"NNC(resolution={self.resolution}):\n{self.tree}"

    def fit(self, data: List[Tuple[float, str]]) -> None:
        """
        REPLACE
        """
        pass

    def predict(self, x: float, delta: float) -> str:
        """
        REPLACE
        """
        pass