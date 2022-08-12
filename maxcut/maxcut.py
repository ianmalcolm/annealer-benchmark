#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import networkx as nx


# In[2]:


def load_csv(filename):
    """ filename: csv file, each row is an edge, specified by a start point
        an end point, and the weight.
    """
    
    with open(filename, 'r', newline='') as f:
        reader = csv.reader(f)
        data = [[int(row[0]), int(row[1]), float(row[2])] for row in reader]
    
    nodes = [k0 for k0, k1, v in data if k0 == k1]
    edges = [[k0, k1] for k0, k1, v in data if k0 != k1]
    
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    
    node_weights = {k0: {'weight': v} for k0, k1, v in data if k0 == k1}
    edge_weights = {(k0, k1): {'weight': v} for k0, k1, v in data if k0 != k1}

    nx.set_edge_attributes(g, edge_weights)
    nx.set_node_attributes(g, node_weights)

    return g


# In[3]:


def qubo_maxcut(g):
    linear = {k: 0 for k in g.nodes}
    quadratic = {(k0, k1): 0 for k0, k1 in g.edges}
    for s, d, w in g.edges.data('weight'):
        quadratic[(s, d)] += 2*w
        linear[s] -= w
        linear[d] -= w
    return linear, quadratic


# In[4]:


def maxcut_energy(g, solution):
    energy = 0
    for k0, k1, w in g.edges.data('weight'):
        energy += abs(solution[k0] - solution[k1]) * w
    return energy


# In[5]:


if __name__ == '__main__':
    
    g = load_csv('chimera-like/chimera_node0204.csv')
    print(f'The graph is:')
    print(f'nodes: {g.nodes}')
    print(f'edges: {g.edges}\n')
    
    linear, quadratic = qubo_maxcut(g)
    print(f'The qubo form is:')
    print(f'linear: {linear}')
    print(f'quadratic: {quadratic}\n')
    
    import numpy as np
    rng = np.random.default_rng(seed=1234)
    random_solution = {i: rng.integers(2) for i in g.nodes}
    print(f'The random solution is {random_solution}\n')
    
    energy = maxcut_energy(g, random_solution)
    print(f'The energy is {energy}')
    

