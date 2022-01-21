# Simple Assembly Line Balancing Problem 


## Problem description

The Simple Assembly Line Balancing Problem ([SALBP](https://assembly-line-balancing.de/salbp/)) is the basic optimization problem in assembly line balancing research. Given is a set of operations each of which has a deterministic duration. The operations are partially ordered by precedence relations defining a precedence graph. The paced assembly line consists of a sequence of (work) stations. In each station a subset of the operations is performed by a single operator. The resulting station time (sum of the respective operation times) must not exceed the cycle time. Concerning the precedence relations, no task is allowed to be executed in an earlier station than any of its predecessors. We consider the version where the cycle time is given and we want to minimize the number of stations (SALBP-1).

More information about the formulation of this problem in CP Optimizer and the performance of the search is available in this [post](https://ibm.biz/CPO_SALBP).

## CP Optimizer formulation

The formulation creates one interval variable `op[i]` per operation. There are at most `n` stations. The time boundaries of stations is modeled by fixed interval variables of length 1 (the value 1 could be any positive integer, it represents the time taken to move from one station to the next one, the value of this duration has no impact on the problem). Precedence relations are posted using `endBeforeStart` constraints between operations and a global `noOverlap` constraint is posted to ensure that operations do not overlap each other and do not overlap station boundaries. Finally, the objective function is to minimize the makespan (end time of the last operation) as the number of stations is directly related with the makespan: `nstations = ceil(makespan/(C+1))`.

> NOTE: _The conventions for typesetting CP Optimizer models are available [here](../../typeset_models/README.md)_

    Given:
     N                    # Number of activities
     C                    # Cycle time
     D[i] : i in [1..N]   # Duration of activity i
     P                    # Set of precedence constraints between operations (i,j)
 
    interval op[i] size D[i]    : i in [1..N]
    interval sb[k] size 1       : k in [1..N]
 
    makespan = max( endOf(op[i]) i in [1..N] )
    nstations = (makespan + C) div (C+1)
    
    minimize makespan
     
    startOf(sb[k])=k*(C+1)      : k in [1..N]
    endBeforeStart(op[i],op[j]) : (i,j) in P
    noOverlap(op+sb)

## Code samples

The corresponding formulations in Python and OPL are here : [salbp1.py](./python/salbp1.py), [salbp1.mod](./opl/salbp1.mod)

A more realistic variant where there are multiple operators for handling the operations are available here: [salbp1W.py](./python/salbp1W.py), [salbp1W.mod](./opl/salbp1W.mod). They use a _cumul function_ instead of a _no overlap_ constraint.

The variant that minimizes the cycle time given a fixed number of stations (known as SALBP-2) is available here: [salbp2.py](./python/salbp2.py), [salbp2.mod](./opl/salbp2.mod).
