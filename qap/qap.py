#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


def load_qap(filename):

    with open(filename, 'r') as fh:
        n = int(fh.readline())

        numbers = [float(n) for n in fh.read().split()]

        data = np.asarray(numbers).reshape(2, n, n)
        f = data[1]
        d = data[0]
        
    i = range(len(f))
    f[i, i] = 0
    d[i, i] = 0

    return f, d


# In[3]:


def qubo_qap(g, penalty=None):
    """Quadratic Assignment Problem (QAP)"""
    
    flow, distance = g
    n = len(flow)
    q = np.einsum("ij,kl->ikjl", flow, distance)
    
    if penalty is None:
        penalty = qubo_qap_penalty(g)

    i = range(len(q))
    q[i,:,i,:] += 1 * penalty
    q[i,:,i,:] -= 2 * penalty * np.eye(n)
    q[:,i,:,i] += 1 * penalty
    q[:,i,:,i] -= 2 * penalty * np.eye(n)

    q = q.reshape(n**2,n**2).astype(np.float32)

    offset = penalty * 2 * n
    linear = {i: q[i, i] for i in range(q.shape[0])}
    quadratic = {(i, j): q[i, j] for j in range(q.shape[1]) for i in range(q.shape[0]) if i > j}

    return linear, quadratic, offset

def qubo_qap_penalty(g):
    F, D = g
    q = np.einsum("ij,kl->ikjl", F, D)
    return F.shape[0] * np.abs(q).max()


# In[4]:


def qubo_qap_feasibility(g, solution:dict):
    F, D = g
    
    solution = [[k, v] for k, v in solution.items()]
    solution.sort(key=lambda x: x[0])
    _, vals = zip(*solution)
    vals = np.asarray(vals).reshape(F.shape)
    
    assert np.all(np.logical_or(vals==0, vals==1)), 'Decision variable must be 0 or 1'
    return np.all(vals.sum(axis=0)==1) and np.all(vals.sum(axis=1)==1)

def qubo_qap_energy(g, solution:dict):
    
    F, D = g
    
    solution = [[k, v] for k, v in solution.items()]
    solution.sort(key=lambda x: x[0])
    _, vals = zip(*solution)
    vals = np.asarray(vals).reshape(F.shape)
    
    state = np.vstack(np.where(vals==1)).T
    state = np.array(state).astype(np.int32)
    energy = 0
    for i in range(len(state)):
        energy += np.einsum('i,i->', F[state[i,0], state[:,0]], D[state[i,1], state[:,1]])
    return energy


# In[5]:


if __name__ in '__main__':
    F, D = load_qap('tinyqap/tiny08a.dat')
    print(f'The QAP instance is:')
    print(F)
    print(D)
    print()
    
    linear, quadratic, offset = qubo_qap((F, D))
    print(f'The qubo form is:')
    print(f'linear: {linear}')
    print(f'quadratic: {quadratic}')
    print(f'offset: {offset}\n')

    import numpy as np
    rng = np.random.default_rng(seed=1234)
    random_solution = {i: rng.integers(2) for i in range(F.size)}
    print(f'The random solution is {random_solution}\n')

    feasibility = qubo_qap_feasibility((F, D), random_solution)
    print(f'The feasibility of the random solution is {feasibility}\n')
    
    feasible_solution = np.zeros(F.shape)
    sequence = np.arange(F.shape[0])
    np.random.shuffle(sequence)
    for i in range(F.shape[0]):
        feasible_solution[i, sequence[i]] = 1
    feasible_solution = {k:v for k, v in enumerate(feasible_solution.flatten())}
    print(f'The feasible solution is {feasible_solution}\n')
    
    feasibility = qubo_qap_feasibility((F, D), feasible_solution)
    print(f'The feasibility of the feasible solution is {feasibility}\n')
    
    energy = qubo_qap_energy((F,D), feasible_solution)
    print(f'The energy of the feasible solution is {energy}')

