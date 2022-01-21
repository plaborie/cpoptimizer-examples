# Classical Permutation flow-shop scheduling problem

## Problem description

The permutation flow-shop scheduling problem (PFSP) is a special type of [flow-shop](../flow_shop/README.md) scheduling problem in which the processing order of the jobs on the machines is the same for each subsequent operation of processing. No machine can perform more than one operation simultaneously. For each operation of each job, execution time is specified. Operations within one job must be performed in the specified order. The first operation gets executed on the first machine, then (as the first operation is finished) the second operation on the second machine, and so on until the n-th operation. The problem, known to be NP-hard, is to sequence operations on the machines so that the maximum completion time over all jobs (makespan) is minimized. 

## CP Optimizer formulation


> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 N                                  # Number of jobs
 M                                  # Number of operations per job (number of machines)
 D[i,j] : i in [1..N], j in [1..M]  # Duration of the jth operation of job i
 
interval x[i,j] size D[i,j]                 : i in [1..N], j in [1..M]
sequence s[k] in [x[i,k] : i in [1..N]]     : k in [1..M]

minimize max(endOf(x[i,M]) : i in [1..N])

noOverlap(s[k])                             : k in [1..M]
sameSequence(s[1],s[k])                     : k in [2..M]
endBeforeStart(x[i,j-1], x[i,j])            : i in [1..N], j in [2..M]  
```

## Code samples

The corresponding implementation in Python is available here : [permutation_flowshop.py](python/permutation_flowshop.py)
