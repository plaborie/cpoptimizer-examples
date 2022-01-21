# Classical Flexible job-shop scheduling problem

## Problem description

The Flexible Job Shop Problem (FJSP) is an extension of the classical [job-shop](../job_shop/README.md) scheduling problem which allows an operation to be processed by any machine from a given set. The problem is to assign each operation to a machine and to order the operations on the machines, such that the maximal completion time (makespan) of all operations is minimized

## CP Optimizer formulation

The model below formulates a flexible job-shop scheduling problem. The jth operation of job i is represented by an interval variable `x[i,j]`. Each possible allocation of this operation on a machine is represented by an optional interval variable `y[i,j,k]`. Alternative constraints state that one and only one model `k` must be selected for each operation `x[i,j]` and a no-overlap constraint is posted on the interval variables `y[i,j,k]` of each machine.

> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 N                                                         # Number of jobs
 M                                                         # Number of machines
 O[i]     : i in [1..N]                                    # Number of operations of job i
 A[i,j]   : i in [1..N], j in [1..O[i]]                    # Number of possible modes of the jth operation of job i
 D[i,j,k] : i in [1..N], j in [1..O[i]], k in [1..A[i,j]]  # Duration of the jth operation of job i in mode k
 R[i,j,k] : i in [1..N], j in [1..O[i]], k in [1..A[i,j]]  # Machine of the jth operation of job i in mode k
 
interval x[i,j]                               : i in [1..N], j in [1..O[i]]
interval y[i,j,k] optional, size=D[i,j,k]     : i in [1..N], j in [1..O[i]], k in [1..A[i,j]]

minimize max(endOf(x[i,O[i]]) : i in [1..N])
alternative(x[i,j], [y[i,j,k] : k in [1..A[i,j]])                                  : i in [1..N], j in [1..O[i]]
noOverlap(y[i,j,k] : i in [1..N], j in [1..O[i]], k in [1..A[i,j]] | R[i,j,k]=m)   : m in [1..M]
endBeforeStart(x[i,j-1], x[i,j])                                                   : i in [1..N], j in [2..O[i]]  
```

It may also be useful to add the following redundant constraint that states that no more than `M` operations can execute in parallel at any moment:

```
sum( pulse(x[i,j],1) :i in [1..N], j in [1..O[i]] ) <= M
```

## Code samples

The corresponding implementation in Python is available here : [flexible_jobshop.py](python/flexible_jobshop.py)
