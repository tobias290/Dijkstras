from graph import Graph, Node, WeightedEdge
from visit import Visit


class Dijkstra:
    """
    Dijkstra's shortest path algorithm
    """
    def __init__(self, graph: Graph):
        """
        Dijkstra initializer
        :param graph: The weighted graph to use for the algorithm
        """
        self.__graph: Graph = graph
        self.__fully_visited: list = []
        self.__priority_queue: list = []
        self.__is_solved: bool = False
        self.__to: str = None
        self.__fr: str = None

    @property
    def visited_nodes(self) -> list:
        """
        :return: Returns all the visited nodes
        """
        return self.__priority_queue

    @property
    def fully_visited_nodes(self):
        """
        :return: Returns all the nodes that have been fully visited
        """
        return self.__fully_visited

    def solve(self, fr: str, to: str):
        """
        Carries out the algorithm
        :param fr: The name of the node to start from
        :param to: The name of the node to end at
        """
        self.__fr, self.__to = fr, to

        self.__priority_queue.append(Visit(self.__fr, self.__fr, 0))

        # Set the first node to the starting node
        visit = fr

        # Constantly loops over until the priority queue is empty or the end/to node has been fully visited
        while not self.__is_solved:
            # Visit the current node
            self.__visit_neighbours(visit)
            # Checks to see if the current node is fully visited
            self.__update_node_fully_visited(visit)
            # Update the priority queue
            self.__update_priority_queue()

            # Check for end state
            if self.__priority_queue and not self.__is_to_value_fully_visited:
                # If the algorithm hasn't finished find the next node to visit
                visit = self.__get_next_visit_node()
            else:
                self.__is_solved = True

    @property
    def shortest_path(self) -> list:
        """
        :return: Returns the shortest path node names in a list for start to end
        """
        if not self.__is_solved:
            raise ArithmeticError("Cannot get path until 'solve' has been called")

        path = [self.__to]

        for node in reversed(self.__fully_visited):
            previous_node_name = node.visited_by
            path.append(previous_node_name)

            if previous_node_name == self.__fr:
                break

        path.reverse()
        return path

    @property
    def final_weight(self) -> int:
        """
        :return: Returns the weight/value of the journey between start and finish
        """
        return self.__fully_visited[-1].cost

    def __visit_neighbours(self, node_name: str):
        """
        Visits all the neighbours of given node
        :param node_name: Name of the node to visit neighbours of
        """
        # Get the actual node
        node = self.__graph.get_node_by_name(node_name)
        # Get the neighbours
        node_neighbours = self.__graph.get_neighbours(node_name)

        # Loop over the neighbours and visit them all
        for neighbour in node_neighbours:
            # Get the edge (with weight) between node and neighbour
            edge = node.get_edge(neighbour.name)

            # Set the neighbour's visited_by's list to have been visited by the node
            neighbour.visit(node_name)

            # Check if node has already been visited
            if self.__check_node_is_already_visited(neighbour.name):
                # Get the visited node class
                visited_node = self.__get_visited_node(neighbour.name)

                # Checks the current value for the visit, if the new path is shorter update it
                if visited_node.cost > self.__get_visited_node(visited_node.visited_by).cost + edge.weight:
                    visited_node.visited_by = node_name
                    visited_node.cost = self.__get_visited_node(visited_node.visited_by).cost + edge.weight
                    self.__update_visited_node(visited_node)
            else:
                # Create a new visit class
                visit = Visit(neighbour.name, node_name, self.__get_visited_node(node_name).cost + edge.weight)
                self.__priority_queue.append(visit)

    def __get_next_visit_node(self) -> str:
        """
        Looks at the priority queue to see which has the lowest value and returns that nodes name.
        That node will be the next to be searched
        :return: Returns the name of the node to search next
        """
        node = None

        for visit in self.__priority_queue:
            # We can't visit the start node
            if visit.node_name == self.__fr:
                continue

            # Finds the lowest value node
            if node is None or visit.cost < node.cost:
                node = visit

        return node.node_name

    def __check_node_is_already_visited(self, node_name: str) -> bool:
        """
        Sees is a given node (via name) has already been visited (i.e checks if it's in the priority queue)
        :param node_name: Name of the node to check
        :return: Returns whether it has been visited or not
        """
        return next((True for visited_node in self.__priority_queue if visited_node.node_name == node_name), False)

    def __get_visited_node(self, node_name: str) -> Visit:
        """
        Gets a visited node via the node's name
        :param node_name: Name of node ot look for
        :return: Returns the node's visit class
        :raise: Raises an error if the wanted doesn't doesn't exist if the priority queue
        """
        # Checks the priority queue
        for visited_node in self.__priority_queue:
            if visited_node.node_name == node_name:
                return visited_node
        else:
            return next((visited_node for visited_node in self.__fully_visited if visited_node.node_name == node_name), None)

    def __update_visited_node(self, node: Visit):
        """
        If a visit node has been changed this update's it in the priority queue
        :param node: Visit node to update
        """
        for i, visited_node in enumerate(self.__priority_queue):
            # Looks for a match via the nodes name
            if visited_node.node_name == node.node_name:
                # Update the node
                self.__priority_queue[i] = node

    def __update_node_fully_visited(self, node_name: str):
        """
        Takes a node and check if it has been fully visited and update its 'is_fully_visited' boolean
        :param node_name: Name of the node to check
        """
        node = self.__graph.get_node_by_name(node_name)
        node_neighbours = self.__graph.get_neighbours(node_name)

        # Set it to true to begin with as the first for loop required AND
        fully_visited = True

        for neighbour in node_neighbours:
            # Update the variable by ANDing it against itself and whether the neighbour has been visited by the node
            fully_visited = fully_visited and neighbour.is_visited_by(node_name)

        # This does the reverse of neighbours and gets every node that this node as a neighbour
        edges_names = [n.name for n in self.__graph.nodes if node_name in [edge.to for edge in n.edges]]

        # This checks the edge_names against the node's visited by
        # If they are the same then this node has been visited by all the node's that have this node as a neighbour
        fully_visited = fully_visited and sorted(edges_names) == sorted(node.visited_by)

        # Update the node's value
        node.is_fully_visited = fully_visited

    def __update_priority_queue(self):
        """
        Updates the priority queue and removes all nodes that have been fully visited
        All fully visited nodes are removed from the priority queue and moves to the fully visited list
        """
        # Loop over every node
        for node in self.__graph.nodes:
            # Only if its fully visited do we want to remove it
            if node.is_fully_visited:
                # This searched for the wanted visited node
                for visited_node in self.__priority_queue:
                    if visited_node.node_name == node.name:
                        # Once found move it to the fully visited list
                        self.__fully_visited.append(visited_node)
                        # Then remove it form the priority queue
                        self.__priority_queue.remove(visited_node)

    @property
    def __is_to_value_fully_visited(self) -> bool:
        """
        :return: Returns whether the end/final node has been fully visited
        """
        return next(
            (fully_visited_node
             for fully_visited_node in self.__fully_visited
             if fully_visited_node.node_name == self.__to
             ), False)


if __name__ == "__main__":
    weighted_graph = Graph([
        Node("A", [
            WeightedEdge("A", "B", 3),
            WeightedEdge("A", "C", 8),
        ]),
        Node("B", [
            WeightedEdge("B", "D", 2),
        ]),
        Node("C", [
            WeightedEdge("C", "E", 3),
        ]),
        Node("D", [
            WeightedEdge("D", "E", 10),
        ]),
        Node("E", [
            WeightedEdge("E", "F", 3),
            WeightedEdge("E", "Z", 7),
        ]),
        Node("F", [
            WeightedEdge("F", "Z", 2),
        ]),
        Node("Z", []),
    ])

    dijkstra = Dijkstra(weighted_graph)
    dijkstra.solve("A", "Z")
    print("Path:", dijkstra.shortest_path)
    print("Distance:", dijkstra.final_weight)