# Classical Flexible job-shop scheduling problem with sequence-dependent setup times

## Problem description

The Flexible job-shop scheduling problem with sequence-dependent setup times is an extension of the classical [flexible job-shop](../flexible_job_shop/README.md) scheduling problem which introduces a setup time between consecutive operations on a machine. The problem is to assign each operation to a machine and to order the operations on the machines, such that the maximal completion time (makespan) of all operations is minimized

## CP Optimizer formulation

The model below formulates a flexible job-shop scheduling problem with sequence-dependent setup times. The jth operation of job i is represented by an interval variable `x[i,j]`. Each possible allocation of this operation on a machine is represented by an optional interval variable `y[i,j,k]`. Alternative constraints state that one and only one model `k` must be selected for each operation `x[i,j]`. Each operations is associated a type `T[i,j]` and a setup time matrix `S[m]` is available for each machine `m` that gives the setup time between the types of two consecutive operations on the machine. A no-overlap constraint with the setup-time matrix is posted on the interval variables `y[i,j,k]` of each machine.

> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 N                                                          # Number of jobs
 M                                                          # Number of machines
 P                                                          # Number of operation types
 O[i]      : i in [1..N]                                    # Number of operations of job i
 A[i,j]    : i in [1..N], j in [1..O[i]]                    # Number of possible modes of operation i,j
 T[i,j,k]  : i in [1..N], j in [1..O[i]], k in [1..A[i,j]]  # Type of operation i,j in mode k
 D[i,j,k]  : i in [1..N], j in [1..O[i]], k in [1..A[i,j]]  # Duration of operation i,j in mode k
 R[i,j,k]  : i in [1..N], j in [1..O[i]], k in [1..A[i,j]]  # Machine of operation i,j in mode k
 S[m][u,v] : m in [1..M], u,v in [1..P]                     # Setup time between an operation of type u 
                                                            # and an operation of type v on machine m

interval x[i,j]                               : i in [1..N], j in [1..O[i]]
interval y[i,j,k] optional, size=D[i,j,k]     : i in [1..N], j in [1..O[i]], k in [1..A[i,j]]
sequence s[m] 
  in    [ y[i,j,k] : i in [1..N], j in [1..O[i]], k in [1..A[i,j]] | R[i,j,k]=m ]
  types [ T[i,j,k] : i in [1..N], j in [1..O[i]], k in [1..A[i,j]] | R[i,j,k]=m ]  : m in [1..M]
  
minimize max(endOf(x[i,O[i]]) : i in [1..N])

alternative(x[i,j], [y[i,j,k] : k in [1..A[i,j]])  : i in [1..N], j in [1..O[i]]
noOverlap(s[m],S[m])                               : m in [1..M]
endBeforeStart(x[i,j-1], x[i,j])                   : i in [1..N], j in [2..O[i]]  
```


## Code samples

The corresponding implementation in Python is available here : [flexible_jobshop_setup_times.py](python/flexible_jobshop_setup_times.py)
