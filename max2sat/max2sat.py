#!/usr/bin/env python
# coding: utf-8

# In[31]:


import csv
import json
import os

from functools import reduce


# In[13]:


def load_max2sat_cnf(filename):
    """ Load a set of clauses, in the format of 
            (sign0, node0), (sign1, node1), weight
        A sign of 0 means negation, 1 means no negation.
    """

    with open(filename, 'r') as f:
        data = f.readlines()

    while data[0].startswith('c '):
        data.pop(0)

    while data[0].startswith('p '):
        problem_line = data.pop(0)

    _, _, num_nodes, num_edges = problem_line.split()
    num_nodes, num_edges = int(num_nodes), int(num_edges)

    clauses = []
    for row in data:

        row = row.strip()
        if row == '':
            continue

        v0, v1, w = row.split()
        s0, v0 = (0, int(v0[1:])) if v0.startswith('-') else (1, int(v0))
        s1, v1 = (0, int(v1[1:])) if v1.startswith('-') else (1, int(v1))

        clause = ((s0, v0), (s1, v1), float(w))

        clauses.append(clause)

    return clauses


# In[22]:


def qubo_max2sat(clauses):
    """convert max2sat as a QUBO minimisation problem, in which the total weight of 
        unsatisfied clauses is minimised. 
    """

    variables = reduce(lambda a, b: a + b, [[n0, n1] for (s0, n0), (s1, n1), w in clauses])
    variables = list(set(variables))

    linear = {v: 0 for v in variables}
    quadratic = {}
    offset = 0

    for (s0, n0), (s1, n1), w in clauses:

        if n0 > n1:
            n0, n1 = n1, n0
            s0, s1 = s1, s0

        if (n0, n1) not in quadratic:
            quadratic[n0, n1] = 0

        if s0 == 1 and s1 == 1:
            # No negations
            offset += w
            linear[n0] -= w
            linear[n1] -= w
            quadratic[n0, n1] += w
        elif s0 == 1 and s1 == 0:
            # n1 negation
            linear[n1] += w
            quadratic[n0, n1] -= w
        elif s0 == 0 and s1 == 1:
            # n0 negation
            linear[n0] += w
            quadratic[n0, n1] -= w
        else:
            # both negation
            assert s0 == 0 and s1 == 0
            quadratic[n0, n1] += w

    return linear, quadratic, offset


# In[15]:


def evaluate_max2sat(clauses, cfg):
    """return total weight of clauses that are satisfied"""

    energy = 0
    for (s0, n0), (s1, n1), w in clauses:
        c0 = cfg[n0] if s0 else 1 - cfg[n0]
        c1 = cfg[n1] if s1 else 1 - cfg[n1]
        energy += int(c0 or c1) * w

    return energy

def evaluate_max2sat_qubo(linear, quadratic, cfg, offset=0):
    """return total weight of clauses that are not satisfied"""

    energy  = offset
    energy += sum(cfg[k] * v for k, v in linear.items())
    energy += sum(cfg[k0] * cfg[k1] * v for (k0, k1), v in quadratic.items())

    return energy
