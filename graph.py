from typing import List

class WeightedEdge:
    """
    Represents a weighted edge between to nodes
    It also stores the weight
    """
    def __init__(self, f: str, t: str, weight: int):
        """
        WeightedEdge initializer.
        :param f: From node's name
        :param t: To node's name
        :param weight: Weight of the edge
        """
        self.__from: str = f
        self.__to: str = t
        self.__weight: int = weight

    @property
    def fr(self) -> str:
        """
        :return: Returns who this edge is from
        """
        return self.__from

    @property
    def to(self) -> str:
        """
        :return: Returns who this edge is to
        """
        return self.__to

    @property
    def weight(self) -> int:
        """
        :return: Returns the weight of the edge
        """
        return self.__weight


class Node:
    """
    Represents a node and also stores it edges (i.e. who it connects to)
    """
    def __init__(self, name: str, edges: List[WeightedEdge]):
        """
        Node initializer.
        :param name: Name of the node
        :param edges: All of the nodes edges
        """
        self.__name: str = name
        self.__edges: List[WeightedEdge] = edges
        self.__visited_by: list = []
        self.__is_fully_visited: bool = False

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name

    @property
    def name(self) -> str:
        """
        :return: Returns the name of the node
        """
        return self.__name

    @property
    def edges(self) -> list:
        """
        :return: Returns the node's edges
        """
        return self.__edges

    def get_edge(self, to) -> WeightedEdge:
        """
        Gets a edges between this node and another
        :param to: The node the edge is connecting to
        """
        return next(edge for edge in self.__edges if edge.to == to)

    @property
    def visited_by(self) -> list:
        """
        :return: Returns the list of what other nodes have visited this node
        """
        return self.__visited_by

    def is_visited_by(self, node_name):
        """
        Check whether this node has been visited by a specific node
        :param node_name: Node to check
        :return: Returns whether it has been visited by the given node
        """
        return node_name in self.__visited_by

    def visit(self, name: str):
        """
        Add a node to the visit list
        :param name: Node to add to the list
        """
        if name not in self.__visited_by:
            self.__visited_by.append(name)

    @property
    def is_fully_visited(self) -> bool:
        """
        :return: Returns whether this node is fully visited
        (i.e.
        Has visited all of its neighbours.
        All the nodes that have this node as a neighbour have visited this node.
        )
        """
        return self.__is_fully_visited

    @is_fully_visited.setter
    def is_fully_visited(self, value: bool):
        """
        Set's whether this node has been fully visited
        :param value: Either True or False
        """
        self.__is_fully_visited = value


class Graph:
    """
    Represents a graph contains nodes
    """
    def __init__(self, nodes: List[Node]):
        """
        Graph initializer.
        :param nodes: Nodes of the graph
        """
        self.__nodes: list = nodes

    @property
    def nodes(self) -> list:
        """
        :return: Returns all the graph's nodes
        """
        return self.__nodes

    def get_node_by_name(self, node_name: str) -> Node:
        """
        Get's a specific node via it's name
        :param node_name: Name of node to search for
        :return: Returns the node's instance
        """
        return next(node for node in self.__nodes if node.name == node_name)

    def get_neighbours(self, node_name: str) -> list:
        """
        Gets all the neighbours of a specific node
        :param node_name: Name of node to retrieve neighbours
        :return: Returns a list of nodes that neighbour the given node
        """
        # Loop over all the node's edges and append the edge's to node
        return [self.get_node_by_name(edges.to) for edges in self.get_node_by_name(node_name).edges]
