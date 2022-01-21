# Classical Flow-shop scheduling problem

## Problem description

The classical flow-shop scheduling problem (FSP) is a particular case of [job-shop](../job_shop/README.md) scheduling problem where the i-th operation of the job must be executed on the i-th machine. No machine can perform more than one operation simultaneously. For each operation of each job, execution time is specified. Operations within one job must be performed in the specified order. The first operation gets executed on the first machine, then (as the first operation is finished) the second operation on the second machine, and so on until the n-th operation. The problem, known to be NP-hard, is to sequence operations on the machines so that the maximum completion time over all jobs (makespan) is minimized. 

## CP Optimizer formulation


> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 N                                  # Number of jobs
 M                                  # Number of operations per job (number of machines)
 D[i,j] : i in [1..N], j in [1..M]  # Duration of the jth operation of job i
 
interval x[i,j] size D[i,j]                 : i in [1..N], j in [1..M]
 
minimize max(endOf(x[i,M]) : i in [1..N])

noOverlap(x[i,k] : i in [1..N])             : k in [1..M]
endBeforeStart(x[i,j-1], x[i,j])            : i in [1..N], j in [2..M]  
```

## Code samples

The corresponding implementation in Python is available here : [flowshop.py](python/flowshop.py)
