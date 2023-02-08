import networkx as nx
from abc import ABC, abstractmethod


class InvalidEdgeType(Exception):
    pass


class InvalidShortestPathType(Exception):
    pass


class RateCard(ABC):
    """"""

    @abstractmethod
    def __init__(
        self, graph, cabinet: int, chamber: int, pot: int, tverge: int, troad: int
    ):
        pass

    @abstractmethod
    def get_node_cost(self, node: str):
        pass

    @abstractmethod
    def get_edge_cost(self, edge: str):
        pass

    @abstractmethod
    def total_node_cost(self):
        pass

    @abstractmethod
    def total_edge_cost(self):
        pass

    @abstractmethod
    def total_cost(self):
        pass


class RateCardBasic(RateCard):
    def __init__(
        self, graph, cabinet: int, chamber: int, pot: int, tverge: int, troad: int
    ):
        self.tverge = tverge
        self.troad = troad
        self.graph = graph
        self._cost = {"Cabinet": cabinet, "Chamber": chamber, "Pot": pot}

    def get_node_cost(self, node: str) -> int:
        node_type = nx.get_node_attributes(self.graph, "type")[node]
        return self._cost[node_type]

    def get_edge_cost(self, edge) -> int:
        lenth = nx.get_edge_attributes(self.graph, "length")[edge]
        edge_type = nx.get_edge_attributes(self.graph, "material")[edge]

        if edge_type == "verge":
            return lenth * self.tverge

        if edge_type == "road":
            return lenth * self.troad

        raise InvalidEdgeType("trenth material must be verge or road")

    def total_node_cost(self) -> int:
        return sum([self.get_node_cost(node=n) for n in self.graph.nodes])

    def total_edge_cost(self) -> int:
        return sum([self.get_edge_cost(edge=e) for e in self.graph.edges])

    def total_cost(self) -> int:
        return self.total_node_cost() + self.total_edge_cost()


class RateCardA(RateCardBasic):
    def __init__(self, graph, cabinet=1000, chamber=200, pot=100, tverge=50, troad=100):
        super().__init__(graph, cabinet, chamber, pot, tverge, troad)


class RateCardB(RateCardBasic):
    def __init__(self, graph, cabinet=1200, chamber=200, tverge=40, troad=80):
        super().__init__(
            graph, cabinet=cabinet, chamber=chamber, pot=0, tverge=tverge, troad=troad
        )

    def get_node_cost(self, node: str) -> int:
        node_type = nx.get_node_attributes(self.graph, "type")[node]
        cabinet = [
            k
            for k, v in nx.get_node_attributes(self.graph, "type").items()
            if v == "Cabinet"
        ][0]
        if node_type == "Pot":
            l = nx.shortest_path_length(
                self.graph, source=node, target=cabinet, weight="length"
            )
            if isinstance(l, int):
                return 20 * l
            raise InvalidShortestPathType(
                f"Shortest path for cabinet {cabinet} to pot {node} not returned an Integer."
            )
        else:
            return self._cost[node_type]


if __name__ == "__main__":
    graph = nx.read_graphml("./problem.graphml")
    card_a = RateCardA(graph=graph)
    card_b = RateCardB(graph=graph)
    print(card_a.total_cost())
    print(card_b.total_cost())
