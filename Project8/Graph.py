"""
Name: Shrey Jindal
CSE 331 FS20 (Onsay)
"""

import heapq
import itertools
import math
import queue
import random
import time
import csv
from typing import TypeVar, Callable, Tuple, List, Set

import matplotlib.cm as cm
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

T = TypeVar('T')
Matrix = TypeVar('Matrix')  # Adjacency Matrix
Vertex = TypeVar('Vertex')  # Vertex Class Instance
Graph = TypeVar('Graph')    # Graph Class Instance


class Vertex:
    """ Class representing a Vertex object within a Graph """

    __slots__ = ['id', 'adj', 'visited', 'x', 'y']

    def __init__(self, idx: str, x: float = 0, y: float = 0) -> None:
        """
        DO NOT MODIFY
        Initializes a Vertex
        :param idx: A unique string identifier used for hashing the vertex
        :param x: The x coordinate of this vertex (used in a_star)
        :param y: The y coordinate of this vertex (used in a_star)
        """
        self.id = idx
        self.adj = {}             # dictionary {id : weight} of outgoing edges
        self.visited = False      # boolean flag used in search algorithms
        self.x, self.y = x, y     # coordinates for use in metric computations

    def __eq__(self, other: Vertex) -> bool:
        """
        DO NOT MODIFY
        Equality operator for Graph Vertex class
        :param other: vertex to compare
        """
        if self.id != other.id:
            return False
        elif self.visited != other.visited:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex visited flags not equal: self.visited={self.visited},"
                  f" other.visited={other.visited}")
            return False
        elif self.x != other.x:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex x coords not equal: self.x={self.x}, other.x={other.x}")
            return False
        elif self.y != other.y:
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex y coords not equal: self.y={self.y}, other.y={other.y}")
            return False
        elif set(self.adj.items()) != set(other.adj.items()):
            diff = set(self.adj.items()).symmetric_difference(set(other.adj.items()))
            print(f"Vertex '{self.id}' not equal")
            print(f"Vertex adj dictionaries not equal:"
                  f" symmetric diff of adjacency (k,v) pairs = {str(diff)}")
            return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        :return: string representing Vertex object
        """
        lst = [f"<id: '{k}', weight: {v}>" for k, v in self.adj.items()]

        return f"<id: '{self.id}'" + ", Adjacencies: " + "".join(lst) + ">"

    def __str__(self) -> str:
        """
        DO NOT MODIFY
        :return: string representing Vertex object
        """
        return repr(self)

    def __hash__(self) -> int:
        """
        DO NOT MODIFY
        Hashes Vertex into a set; used in unit tests
        :return: hash value of Vertex
        """
        return hash(self.id)

#============== Modify Vertex Methods Below ==============#

    def degree(self) -> int:
        """
        gets degree of vertex
        :returns: degree value as int
        """
        return len(self.adj)

    def get_edges(self) -> Set[Tuple[str, float]]:
        """
        gets info of outgoing edges of vertex
        :return: a set of tuples with id weight pairs
        """
        edges = set()
        for key in self.adj:
            tuplex = (key, self.adj[key])
            edges.add(tuplex)
        return edges

    def euclidean_distance(self, other: Vertex) -> float:
        """
        get euclidian distance between 2 vertices
        param: other vertex
        :returns: the distance
        """
        return ((self.x-other.x)**2+(self.y-other.y)**2)**.5

    def taxicab_distance(self, other: Vertex) -> float:
        """
        get taxicab distance between 2 vertices
        param: other vertex
        :returns: the distance
        """
        return abs(self.x - other.x) + abs(self.y - other.y)


class Graph:
    """ Class implementing the Graph ADT using an Adjacency Map structure """

    __slots__ = ['size', 'vertices', 'plot_show', 'plot_delay']

    def __init__(self, plt_show: bool = False, matrix: Matrix = None, csv: str = "") -> None:
        """
        DO NOT MODIFY
        Instantiates a Graph class instance
        :param: plt_show : if true, render plot when plot() is called; else, ignore calls to plot()
        :param: matrix : optional matrix parameter used for fast construction
        :param: csv : optional filepath to a csv containing a matrix
        """
        matrix = matrix if matrix else np.loadtxt(csv, delimiter=',', dtype=str).tolist() if csv else None
        self.size = 0
        self.vertices = {}

        self.plot_show = plt_show
        self.plot_delay = 0.2

        if matrix is not None:
            for i in range(1, len(matrix)):
                for j in range(1, len(matrix)):
                    if matrix[i][j] == "None" or matrix[i][j] == "":
                        matrix[i][j] = None
                    else:
                        matrix[i][j] = float(matrix[i][j])
            self.matrix2graph(matrix)


    def __eq__(self, other: Graph) -> bool:
        """
        DO NOT MODIFY
        Overloads equality operator for Graph class
        :param other: graph to compare
        """
        if self.size != other.size or len(self.vertices) != len(other.vertices):
            print(f"Graph size not equal: self.size={self.size}, other.size={other.size}")
            return False
        else:
            for vertex_id, vertex in self.vertices.items():
                other_vertex = other.get_vertex(vertex_id)
                if other_vertex is None:
                    print(f"Vertices not equal: '{vertex_id}' not in other graph")
                    return False

                adj_set = set(vertex.adj.items())
                other_adj_set = set(other_vertex.adj.items())

                if not adj_set == other_adj_set:
                    print(f"Vertices not equal: adjacencies of '{vertex_id}' not equal")
                    print(f"Adjacency symmetric difference = "
                          f"{str(adj_set.symmetric_difference(other_adj_set))}")
                    return False
        return True

    def __repr__(self) -> str:
        """
        DO NOT MODIFY
        :return: String representation of graph for debugging
        """
        return "Size: " + str(self.size) + ", Vertices: " + str(list(self.vertices.items()))

    def __str__(self) -> str:
        """
        DO NOT MODFIY
        :return: String representation of graph for debugging
        """
        return repr(self)

    def plot(self) -> None:
        """
        DO NOT MODIFY
        Creates a plot a visual representation of the graph using matplotlib
        """
        if self.plot_show:

            # if no x, y coords are specified, place vertices on the unit circle
            for i, vertex in enumerate(self.get_vertices()):
                if vertex.x == 0 and vertex.y == 0:
                    vertex.x = math.cos(i * 2 * math.pi / self.size)
                    vertex.y = math.sin(i * 2 * math.pi / self.size)

            # show edges
            num_edges = len(self.get_edges())
            max_weight = max([edge[2] for edge in self.get_edges()]) if num_edges > 0 else 0
            colormap = cm.get_cmap('cool')
            for i, edge in enumerate(self.get_edges()):
                origin = self.get_vertex(edge[0])
                destination = self.get_vertex(edge[1])
                weight = edge[2]

                # plot edge
                arrow = patches.FancyArrowPatch((origin.x, origin.y),
                                                (destination.x, destination.y),
                                                connectionstyle="arc3,rad=.2",
                                                color=colormap(weight / max_weight),
                                                zorder=0,
                                                **dict(arrowstyle="Simple,tail_width=0.5,"
                                                                  "head_width=8,head_length=8"))
                plt.gca().add_patch(arrow)

                # label edge
                plt.text(x=(origin.x + destination.x) / 2 - (origin.x - destination.x) / 10,
                         y=(origin.y + destination.y) / 2 - (origin.y - destination.y) / 10,
                         s=weight, color=colormap(weight / max_weight))

            # show vertices
            x = np.array([vertex.x for vertex in self.get_vertices()])
            y = np.array([vertex.y for vertex in self.get_vertices()])
            labels = np.array([vertex.id for vertex in self.get_vertices()])
            colors = np.array(
                ['yellow' if vertex.visited else 'black' for vertex in self.get_vertices()])
            plt.scatter(x, y, s=40, c=colors, zorder=1)

            # plot labels
            for j, _ in enumerate(x):
                plt.text(x[j] - 0.03*max(x), y[j] - 0.03*max(y), labels[j])

            # show plot
            plt.show()
            # delay execution to enable animation
            time.sleep(self.plot_delay)

    def add_to_graph(self, start_id: str, dest_id: str = None, weight: float = 0) -> None:
        """
        Adds to graph: creates start vertex if necessary,
        an edge if specified,
        and a destination vertex if necessary to create said edge
        If edge already exists, update the weight.
        :param start_id: unique string id of starting vertex
        :param dest_id: unique string id of ending vertex
        :param weight: weight associated with edge from start -> dest
        :return: None
        """
        if self.vertices.get(start_id) is None:
            self.vertices[start_id] = Vertex(start_id)
            self.size += 1
        if dest_id is not None:
            if self.vertices.get(dest_id) is None:
                self.vertices[dest_id] = Vertex(dest_id)
                self.size += 1
            self.vertices.get(start_id).adj[dest_id] = weight

    def matrix2graph(self, matrix: Matrix) -> None:
        """
        Given an adjacency matrix, construct a graph
        matrix[i][j] will be the weight of an edge between the vertex_ids
        stored at matrix[i][0] and matrix[0][j]
        Add all vertices referenced in the adjacency matrix, but only add an
        edge if matrix[i][j] is not None
        Guaranteed that matrix will be square
        If matrix is nonempty, matrix[0][0] will be None
        :param matrix: an n x n square matrix (list of lists) representing Graph as adjacency map
        :return: None
        """
        for i in range(1, len(matrix)):         # add all vertices to begin with
            self.add_to_graph(matrix[i][0])
        for i in range(1, len(matrix)):         # go back through and add all edges
            for j in range(1, len(matrix)):
                if matrix[i][j] is not None:
                    self.add_to_graph(matrix[i][0], matrix[j][0], matrix[i][j])

    def graph2matrix(self) -> Matrix:
        """
        given a graph, creates an adjacency matrix of the type described in "construct_from_matrix"
        :return: Matrix
        """
        matrix = [[None] + [v_id for v_id in self.vertices]]
        for v_id, outgoing in self.vertices.items():
            matrix.append([v_id] + [outgoing.adj.get(v) for v in self.vertices])
        return matrix if self.size else None

    def graph2csv(self, filepath: str) -> None:
        """
        given a (non-empty) graph, creates a csv file containing data necessary to reconstruct that graph
        :param filepath: location to save CSV
        :return: None
        """
        if self.size == 0:
            return

        with open(filepath, 'w+') as graph_csv:
            csv.writer(graph_csv, delimiter=',').writerows(self.graph2matrix())

#============== Modify Graph Methods Below ==============#

    def reset_vertices(self) -> None:
        """
        reset the visited flag of all vertices in graph
        """
        for key in self.vertices:
            self.vertices[key].visited = False

    def get_vertex(self, vertex_id: str) -> Vertex:
        """
        get vertex from graph
        :param: id
        :returns: the vertex
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        return None

    def get_vertices(self) -> Set[Vertex]:
        """
        get all vertices of graph
        :returns: set of vertices
        """
        vss = set()
        for key in self.vertices:
            vss.add(self.vertices[key])
        return vss

    def get_edge(self, start_id: str, dest_id: str) -> Tuple[str, str, float]:
        """
        get edge between passed vertices
        :param: starting id
        :param: ending id
        :returns: a tuple with startid, endid and weight of edge
        """
        if start_id in self.vertices and dest_id in self.vertices[start_id].adj:
            return start_id, dest_id, float(self.vertices[start_id].adj[dest_id])
        return None

    def get_edges(self) -> Set[Tuple[str, str, float]]:
        """
        get all edges
        :return: set of tuples with edge data
        """
        ess = set()
        for vert in self.vertices:
            for ver2 in self.vertices[vert].adj:
                ess.add(self.get_edge(vert, ver2))
        return ess

    def bfs(self, start_id: str, target_id: str) -> Tuple[List[str], float]:
        """
        breadth first search for target from start
        :param: start id
        :param: target id
        :returns: tuple with path list and cost
        """
        self.reset_vertices()
        if start_id not in self.vertices or target_id not in self.vertices:
            return [], 0
        prev_vertex = {}
        last_round_weight = {start_id: 0}
        next_n = queue.SimpleQueue()
        next_n.put(start_id)
        self.vertices[start_id].visited = True
        found = False
        while not next_n.empty() and not found:
            nid = next_n.get()
            for vid in self.vertices[nid].adj:
                if not self.vertices[vid].visited:
                    next_n.put(vid)
                    self.vertices[vid].visited = True
                    prev_vertex[vid] = nid
                    last_round_weight[vid] = self.vertices[nid].adj[vid]
                    if vid == target_id:
                        found = True
                        break
        if not found:
            return [], 0
        order = []
        weight = 0
        thisid = target_id
        while thisid != start_id:
            order.append(thisid)
            weight += last_round_weight[thisid]
            thisid = prev_vertex[thisid]
        order.append(start_id)
        order.reverse()
        self.reset_vertices()
        return order, weight

    def dfs(self, start_id: str, target_id: str) -> Tuple[List[str], float]:
        """
        depth first search for target from start
        :param: startid
        :param: target id
        :returns: tuple with path list and cost
        """
        weight = [0]
        order = []

        def dfs_inner(node_id: str):
            """
            iterator for dfs
            :param: the current node
            """
            self.vertices[node_id].visited = True
            found = False
            if target_id in self.vertices[node_id].adj:
                found = True
                weight[0] += self.get_edge(node_id, target_id)[2]
                order.append(target_id)
                order.append(node_id)
                return True
            else:
                for vert_id in self.vertices[node_id].adj:
                    if not self.vertices[vert_id].visited:
                        value = dfs_inner(vert_id)
                        if value:
                            weight[0] += self.get_edge(node_id, vert_id)[2]
                            order.append(node_id)
                            return True
            return False
        if start_id not in self.vertices or target_id not in self.vertices:
            return [], 0

        dfs_inner(start_id)
        order.reverse()
        self.reset_vertices()
        return order, weight[0]

    def detect_cycle(self) -> bool:
        """
        detect any cycles in graph
        :return: bool indicating presence of cycle
        """
        result = [0]

        def detect_inner(node_id, ancestory):
            """
            iterator for detect cycle
            :param: current node id
            """
            self.vertices[node_id].visited = True
            ancestory.append(node_id)
            for vert_id in self.vertices[node_id].adj:
                if vert_id in ancestory:
                    result[0] += 1
                    return
                detect_inner(vert_id, ancestory)
                ancestory.pop()

        self.reset_vertices()
        for node in self.vertices:
            if not self.vertices[node].visited:
                detect_inner(node, [])
        return False if result[0] == 0 else True


    def a_star(self, start_id: str, target_id: str,
               metric: Callable[[Vertex, Vertex], float]) -> Tuple[List[str], float]:
        self.reset_vertices()
        a_star_q = AStarPriorityQueue()
        weight_keeper = {}
        best_track = {}

        for nid in self.vertices:
            if nid != start_id:
                weight_keeper[nid] = float('inf')
                a_star_q.push(float('inf'), self.vertices[nid])
            else:
                weight_keeper[nid] = 0
                self.vertices[nid].visited = True
                a_star_q.push(0, self.vertices[nid])

        while not a_star_q.empty():
            key, vert = a_star_q.pop()
            vert.visited = True
            if target_id == vert.id:
                break
            for vid2 in vert.adj:
                vert2 = self.vertices[vid2]
                if not vert2.visited:
                    last_weight = self.get_edge(vert.id, vert2.id)[2]
                    if last_weight + weight_keeper[vert.id] < weight_keeper[vert2.id]:
                        weight_keeper[vert2.id] = last_weight + weight_keeper[vert.id]
                        newval = metric(self.vertices[target_id], vert2) + weight_keeper[vert2.id]
                        a_star_q.update(newval, vert2)
                        best_track[vid2] = vert.id

        order = [target_id]
        weight = 0
        this_id = target_id
        while this_id != start_id:
            prev_id = best_track[this_id]
            weight += self.get_edge(prev_id, this_id)[2]
            this_id = prev_id
            order.append(this_id)
        order.reverse()
        self.reset_vertices()
        return order, weight


class AStarPriorityQueue:
    """
    Priority Queue built upon heapq module with support for priority key updates
    Created by Andrew McDonald
    Inspired by https://docs.python.org/2/library/heapq.html
    """

    __slots__ = ['data', 'locator', 'counter']

    def __init__(self) -> None:
        """
        Construct an AStarPriorityQueue object
        """
        self.data = []                        # underlying data list of priority queue
        self.locator = {}                     # dictionary to locate vertices within priority queue
        self.counter = itertools.count()      # used to break ties in prioritization

    def __repr__(self) -> str:
        """
        Represent AStarPriorityQueue as a string
        :return: string representation of AStarPriorityQueue object
        """
        lst = [f"[{priority}, {vertex}], " if vertex is not None else "" for
               priority, count, vertex in self.data]
        return "".join(lst)[:-1]

    def __str__(self) -> str:
        """
        Represent AStarPriorityQueue as a string
        :return: string representation of AStarPriorityQueue object
        """
        return repr(self)

    def empty(self) -> bool:
        """
        Determine whether priority queue is empty
        :return: True if queue is empty, else false
        """
        return len(self.data) == 0

    def push(self, priority: float, vertex: Vertex) -> None:
        """
        Push a vertex onto the priority queue with a given priority
        :param priority: priority key upon which to order vertex
        :param vertex: Vertex object to be stored in the priority queue
        :return: None
        """
        # list is stored by reference, so updating will update all refs
        node = [priority, next(self.counter), vertex]
        self.locator[vertex.id] = node
        heapq.heappush(self.data, node)

    def pop(self) -> Tuple[float, Vertex]:
        """
        Remove and return the (priority, vertex) tuple with lowest priority key
        :return: (priority, vertex) tuple where priority is key,
        and vertex is Vertex object stored in priority queue
        """
        vertex = None
        while vertex is None:
            # keep popping until we have valid entry
            priority, count, vertex = heapq.heappop(self.data)
        del self.locator[vertex.id]            # remove from locator dict
        vertex.visited = True                  # indicate that this vertex was visited
        while len(self.data) > 0 and self.data[0][2] is None:
            heapq.heappop(self.data)          # delete trailing Nones
        return priority, vertex

    def update(self, new_priority: float, vertex: Vertex) -> None:
        """
        Update given Vertex object in the priority queue to have new priority
        :param new_priority: new priority on which to order vertex
        :param vertex: Vertex object for which priority is to be updated
        :return: None
        """
        node = self.locator.pop(vertex.id)      # delete from dictionary
        node[-1] = None                         # invalidate old node
        self.push(new_priority, vertex)         # push new node

# Extra Credit Problem
def defeat_the_chonk(chonk: Graph) -> List[List[float]]:
    return []
