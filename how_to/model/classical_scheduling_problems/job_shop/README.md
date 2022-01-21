# Classical Job-shop scheduling problem

## Problem description

The classical job-shop scheduling problem (JSP) consists of a set of independent jobs, each having its own processing order through a set of machines. Each job has an ordered set of operations, each of which must be processed on a predefined machine. The problem, known to be strongly NP-hard, is to sequence operations on the machines so that the maximum completion time over all jobs (makespan) is minimized. Considerable research has been devoted to this problem in the literature. 

## CP Optimizer formulation

The model below formulates a general job-shop scheduling problem (not necessarily rectangular).

> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 N                                     # Number of jobs
 M                                     # Number of machines
 O[i]   : i in [1..N]                  # Number of operations of job i
 D[i,j] : i in [1..N], j in [1..O[i]]  # Duration of the jth operation of job i
 R[i,j] : i in [1..N], j in [1..O[i]]  # Machine of the jth operation of job i
 
interval x[i,j] size D[i,j]                                  : i in [1..N], j in [1..O[i]]
 
minimize max(endOf(x[i,O[i]]) : i in [1..N])

noOverlap(x[i,j] : i in [1..N], j in [1..O[i]] | R[i,j]=k)   : k in [1..M]
endBeforeStart(x[i,j-1], x[i,j])                             : i in [1..N], j in [2..O[i]]  
```

## Code samples

The corresponding implementation in Python is available here : [jobshop.py](python/jobshop.py)