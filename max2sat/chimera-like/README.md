# Chimera-like graphs

The topology of the Chimera architecture is presented in `chimera_graph.csv`

Reference solutions found by Gurobi 9.1 on a tower server equipped with an Intel Core i9-10900X CPU, 128GB DDR4 memory and 128GB HDD swap memory. Gurobi is allowed to instantiate 20 threads and occupy almost all CPU time slices and memory resources.

| Filename             | Number of nodes | Number of edges | energy             | Time (s)              |
|----------------------|-----------------|-----------------|--------------------|-----------------------|
| chimera_node0204.cnf |              94 |              59 |  31.27456794660515 |  0.007303953170776367 |
| chimera_node0408.cnf |             303 |             254 | 124.01454553829205 |  0.021575212478637695 |
| chimera_node0612.cnf |             529 |             516 | 252.21920287906346 |  0.025577068328857422 |
| chimera_node0816.cnf |             762 |             965 | 491.44157783478346 |  0.0366978645324707   |
| chimera_node1020.cnf |            1008 |            1504 |  759.1011940946989 |  0.07856607437133789  |
| chimera_node1224.cnf |            1219 |            2117 | 1039.1047472741675 |  0.20924901962280273  |
| chimera_node1428.cnf |            1427 |            2907 | 1454.0494912042366 |  0.5871858596801758   |
| chimera_node1632.cnf |            1632 |            3813 | 1872.8076569655100 |  3.688628911972046    |
| chimera_node1836.cnf |            1836 |            4839 | 2384.3891070134487 |  6.467827081680298    |
| chimera_node2040.cnf |            2040 |            5968 | 2910.1353804738214 | 15.859795093536377    |
