#!/usr/bin/env python
# coding: utf-8

def load_max2sat_cnf(filename):

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
