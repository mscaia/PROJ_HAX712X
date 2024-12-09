import sys
import os
import pytest
import osmnx as ox
import networkx as nx

# Directly add the absolute path to the root of the project
sys.path.append('C:\\Users\\stecu\\OneDrive\\Документы\\UMI\\Dev Log\\PROJ_HAX712X')

# Check that the path was correctly added
print("sys.path:", sys.path)

from Cycle3.map.map import route_to_coords


def test_route_to_coords():
    """
    Tests the `route_to_coords` function, checking the correctness of converting route nodes to coordinates.
    """
    # Create a test graph
    G = nx.Graph()
    G.add_node(1, x=3.0, y=45.0)  # Node with coordinates
    G.add_node(2, x=3.1, y=45.1)
    G.add_edge(1, 2)  # Connection between nodes

    # Test data
    route = [1, 2]
    expected_coords = [(45.0, 3.0), (45.1, 3.1)]

    # Check the result
    assert route_to_coords(G, route) == expected_coords


def test_graph_creation():
    """
    Tests the creation of a graph for a specified city using osmnx.
    """
    # Create a graph for the city of Montpellier, France
    city = "Montpellier, France"
    G = ox.graph_from_place(city, network_type="all")

    # Check that the graph contains at least one node
    assert len(G.nodes) > 0, "The graph for the city was not created or is empty"
