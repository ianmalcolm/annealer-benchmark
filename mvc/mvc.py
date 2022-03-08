#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import csv


# In[2]:


def load_csv(filename:str):
    """ filename: csv file
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


def load_dimacs2(filename:str):
    
    with open(filename, 'r') as f:
        data = f.readlines()
    
    preamble = [d for d in data if d.startswith('p')][0]
    _, _, num_nodes, num_edges = preamble.split()
    num_nodes, num_edges = int(num_nodes), int(num_edges)
        
    edges = [d for d in data if d.startswith('e')]
    edges = [row.split() for row in edges]
    edges = [tuple(sorted([int(e[1]), int(e[2])])) for e in edges]
    edges = list(set(edges))

    g = nx.Graph()
    g.add_nodes_from(list(range(1, num_nodes+1)), weight=1)
    g.add_edges_from(edges)

    return g


# In[4]:


def load_dimacs10(filename:str):
    
    adj_list = []
    
    with open(filename) as f:
        num_vertices, num_edges, weighted = map(int, f.readline().split())
        for i in range(num_vertices):
            adj_list.append(map(int, f.readline().split()))
            
    G = nx.Graph()
    for i in range(len(adj_list)):
        for j in adj_list[i]:
            G.add_edge(i + 1, j, weight=1)
    
    node_weights = {k: {'weight': 1} for k in G.nodes()}
    nx.set_node_attributes(G, node_weights)
            
    return G


# In[5]:


def qubo_mvc(g:nx.Graph, penalty=None):

    q = {(k, k): v for k, v in g.nodes(data='weight')}
    
    if penalty is None:
        penalty = qubo_mvc_penalty(g)

    for s, d in g.edges:

        q[(s, s)] -= penalty
        q[(d, d)] -= penalty

        if s > d:
            s, d = d, s
            
        if (s, d) not in q:
            q[(s, d)]  = penalty
        else:
            q[(s, d)] += penalty

    q = {k: v for k, v in q.items() if v != 0}
    
    linear    = {      k0: v for (k0, k1), v in q.items() if k0 == k1}
    quadratic = {(k0, k1): v for (k0, k1), v in q.items() if k0 != k1}

    return linear, quadratic


# In[6]:


def qubo_mvc_penalty(g:nx.Graph):
    """ Find appropriate penalty weight to ensure feasibility """
    # For D-Wave, you cannot randomly choose a positive penalty weight, otherwise
    # you get infeasible solutions very likely. If all weight equals to 1,
    # set penalty to the largest degree will ensure high feasibility.

    highest_degree = max(sum(g.nodes[k]['weight'] for k in g[i].keys()) for i in g.nodes())
    return highest_degree


# In[7]:


def mvc_feasibility(g, solution):
    """ Check if the solution violates the constraints of the problem """
    for k0, k1 in g.edges:
        if solution[k0] == solution[k1] == 0:
            return False
    return True

def mvc_energy(g, solution):
    return sum(solution[k] * v for k, v in g.nodes.data('weight'))

def mvc_easy_fix(g, solution):
    """ fix violation"""
    
    t = {k: v for k, v in solution.items()}

    for k0, k1 in g.edges:
        if t[k0] == t[k1] == 0:
            t[k0] = 1
            
    return t


# In[11]:


if __name__ in '__main__':
    g = load_csv('pegasus-like/pegasus_node0543.csv')
    print(f'The graph is:')
    print(f'nodes: {g.nodes}')
    print(f'edges: {g.edges}\n')
    
    linear, quadratic = qubo_mvc(g)
    print(f'The qubo form is:')
    print(f'linear: {linear}')
    print(f'quadratic: {quadratic}\n')
    
    import numpy as np
    rng = np.random.default_rng(seed=1234)
    random_solution = {i: rng.integers(2) for i in g.nodes}
    print(f'The random solution is {random_solution}\n')
    
    feasibility = mvc_feasibility(g, random_solution)
    print(f'The feasibility is {feasibility}\n')
    
    fixed_solution = mvc_easy_fix(g, random_solution)
    print(f'After fixation, the solution is {fixed_solution}\n')

    feasibility = mvc_feasibility(g, fixed_solution)
    print(f'The feasibility is {feasibility}\n')

    energy = mvc_energy(g, fixed_solution)
    print(f'The energy is {energy}')
    

