# Pegasus-like graphs

The topology of the Chimera architecture is presented in `pegasus_graph.csv`

Reference solutions found by Gurobi 9.1 on a tower server equipped with an Intel Core i9-10900X CPU, 128GB DDR4 memory and 128GB HDD swap memory. Gurobi is allowed to instantiate 20 threads and occupy almost all CPU time slices and memory resources.

| Filename             | Number of nodes | Number of edges | energy             | Time (s)              |
|----------------------|-----------------|-----------------|--------------------|-----------------------|
| pegasus_node0543.cnf |  378 |   333 |   164.89186974365475 |     0.019006967544555664 |
| pegasus_node1086.cnf | 1021 |  1424 |   724.1389326178405  |     0.03659510612487793  |
| pegasus_node1629.cnf | 1591 |  3226 |  1572.497343142735   |     0.5250778198242188   |
| pegasus_node2172.cnf | 2154 |  5921 |  2832.674123650683   |     7.723367929458618    |
| pegasus_node2715.cnf | 2687 |  9169 |  4379.317399867191   |    22.622870922088623    |
| pegasus_node3258.cnf | 3230 | 13100 |  6204.1349262155945  |   469.820219039917       |
| pegasus_node3801.cnf | 3768 | 17921 |  8385.009037390244   |  4221.54202413559        |
| pegasus_node4344.cnf | 4299 | 23532 | 10840.847001669104   | 31258.30106806755        |
| pegasus_node4887.cnf | 4840 | 29619 | 13518.824074565064   | 34999.98590302467        |
| pegasus_node5430.cnf | 5378 | 36636 | 16614.5258882768     | 34286.06880402565        |
