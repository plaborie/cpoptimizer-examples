# Flow-shop scheduling problem with earliness/tardiness cost

## Problem description

The problem is a [flow-shop](../flow_shop/README.md) scheduling problem with earliness and tardiness costs desribed in [1] that have been used in a number of studies. In this problem, a set of `N` jobs is to be executed
on a set of `M` machines. Each job `i` is a chain of exactly `M` operations, one per machine. All jobs require the machines in the same order that is, the position of an operation in the job determines the machine it will be executed on. Each operation `j` of a job `i` is specified by an integer duration `D[i,j]`. Operations cannot be interrupted and each machine can process only one operation at
a time. The objective function is to minimize the total earliness/tardiness cost. Typically, this objective might arise in just-in-time inventory management: a late job has negative consequence on customer satisfaction and time to market, while an early job increases storage costs. Each job `i` is characterized by its release date `RD[i]`, its due date `DD[i]` and its weight `W[i]`. The first operation of job `i` cannot start before the release date `RD[i]`. Let `C[i]` be the completion date of the last operation of job `i`. The earliness/tardiness cost incurred by job `i` is `W[i]*abs(C[i]-DD[i])`. In the instances of [1], the total earliness/tardiness cost is normalized by the sum of operation processing times so the global cost to minimize is:

```
sum( W[i]*abs(C[i]-DD[i]) ) : i in [1..N]) / NW
```
 where 

```
NW = sum( W[i] * sum(D[i,j] : j in [1..M]) : i in [1..N])
```

The results of the CP Optimizer automatic search on these problems are reported in [2].

[1] T. Morton, D. Pentico. _Heuristic Scheduling Systems_. Wiley (1993)

[2] P. Laborie. _IBM ILOG CP Optimizer for Detailed Scheduling Illustrated on Three Problems_. Proc. 6th International Conference on Integration of AI and OR Techniques in Constraint Programming for Combinatorial Optimization Problems (CPAIOR 2009) 


## CP Optimizer formulation


> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 N                                  # Number of jobs
 M                                  # Number of operations per job (number of machines)
 RD[i]  : i in [1..N]               # Release date of job i
 DD[i]  : i in [1..N]               # Due date of job i
 W [i]  : i in [1..N]               # Weight of job i
 D[i,j] : i in [1..N], j in [1..M]  # Duration of the jth operation of job i
 
 NW = sum( W[i] * sum(D[i,j] : j in [1..M] ) : i in [1..N])
 
interval x[i,j] size D[i,j]                  : i in [1..N], j in [1..M]
 
minimize sum( W[i]*abs(endOf(x[i,M])-DD[i])  : i in [1..N]) / NW

RD[i] <= startOf(x[i,M])                     : i in [1..N]
noOverlap(x[i,k] : i in [1..N])              : k in [1..M]
endBeforeStart(x[i,j-1], x[i,j])             : i in [1..N], j in [2..M]  
```

## Code samples

The corresponding implementation in Python is available here : [flowshop_earliness_tardiness.py](python/flowshop_earliness_tardiness.py)
