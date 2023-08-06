import networkx as nx
import numpy as np

# Array for selecting the functions in generating persistence
functions = ["None",  "radial_distance", "height", "path_length", "branch_order", "custom_distance"]
nx_version = int(float(nx.__version__))


def custom_distance(G,u,v):
    """user defined custom functions for persistence
    """
    # write your code here
    scalar = None
    return scalar


# A selection of filter functions
def radial_distance(G, u, v):
    """calculate radial distance for persistence
    """
    if nx_version > 1:
        # changed for version 2.x of networkX
        n = G.nodes[u]['pos']
        r = G.nodes[v]['pos']
    else:
        n = G.node[u]['pos']
        r = G.node[v]['pos']

    return np.sqrt(np.dot(n - r, n - r))


def height(G, u, v):
    """calculate height for persistence
    """
    if nx_version > 1:
        n = G.nodes[u]['pos']
        r = G.nodes[v]['pos']
    else:
        n = G.node[u]['pos']
        r = G.node[v]['pos']
    return np.abs((n - r))[2]


def path_length(G, u, v):
    """calculate path length for persistence
    """
    return nx.shortest_path_length(G, v, u, weight='path_length')


def branch_order(G, u, v):
    """calculate branch order for persistence
    """
    if u == v:
        bo = 0
    else:
        path = nx.shortest_path(G, v, u)
        bo = np.sum(np.array(list(dict(nx.degree(G, path)).values())) > 2)
    return bo
