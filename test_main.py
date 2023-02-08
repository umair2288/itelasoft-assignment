import networkx as nx
from .main import RateCardA, RateCardB
import pytest


@pytest.fixture
def graph():
    g = nx.Graph()
    g.add_nodes_from(
        [
            ("A", {"type": "Cabinet"}),
            ("B", {"type": "Chamber"}),
            ("C", {"type": "Pot"}),
        ]
    )

    g.add_edge("A", "B", material="verge", length=5)
    g.add_edge("B", "C", material="verge", length=5)

    return g


def test_get_node_cost(graph):
    assert RateCardA(graph).total_node_cost() == 1300
    assert RateCardB(graph).total_node_cost() == 1600


def test_get_edge_cost(graph):
    assert RateCardA(graph).total_edge_cost() == 500
    assert RateCardB(graph).total_edge_cost() == 400


def test_get_total_cost(graph):
    assert RateCardA(graph).total_cost() == 1800
    assert RateCardB(graph).total_cost() == 2000
