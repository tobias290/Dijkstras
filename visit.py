class Visit:
    """
    This represent a visited node and stores the node's name and who it was visited by, and it current value
    """
    def __init__(self, node_name: str, visited_by: str, value: int):
        """
        Visit initializer
        :param node_name: Visited node name
        :param visited_by: Who the node was visited by
        :param value: The value of the node (i.e. it weight/value to travel here)
        """
        self.__node_name: str = node_name
        self.__visited_by: str = visited_by
        self.__cost: int = value

    def __str__(self) -> str:
        return "Node: {}, Visited By: {}, Value: {}".format(self.__node_name, self.__visited_by, self.cost)

    def __repr__(self) -> str:
        return "[Node: {}, Visited By: {}, Value: {}]".format(self.__node_name, self.__visited_by, self.cost)

    @property
    def node_name(self) -> str:
        """
        :return: Returns the node's name
        """
        return self.__node_name

    @property
    def visited_by(self) -> str:
        """
        :return: Returns who the node was visited by
        """
        return self.__visited_by

    @visited_by.setter
    def visited_by(self, visited_by: str):
        """
        Sets who the node was visited by
        :param visited_by: Name of the node who visited this node
        """
        self.__visited_by = visited_by

    @property
    def cost(self) -> int:
        """
        :return: Returns the current cost/weight to visit it via the visited node (and their visited nodes)
        """
        return self.__cost

    @cost.setter
    def cost(self, cost: int):
        """
        Sets the value
        :param cost: Cost to set
        """
        self.__cost = cost
