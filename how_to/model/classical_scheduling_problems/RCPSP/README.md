# Resource-Constrained Project Scheduling Problem (RCPSP)

## Problem description

Informally, an Resource-Constrained Project Scheduling Problem (RCPSP) considers a set of resources of limited availability and a set of tasks of known durations and known resource requirements, linked by precedence constraints. The problem consists of finding a schedule of minimal duration by assigning a start time to each task such that the precedence constraints and the resource limits are respected

More formally, the RCPSP can be stated as follows. Given:

   * A set of `N` tasks with given durations
   * A set of `M` resources with given capacities,
   * A network of precedence constraints between the tasks, and
   * For each task and each resource the amount of the resource required by the task over its execution

The goal of the RCPSP is to find a schedule satisfying all the constraints (i.e. precedence and resource capacity constraints) whose makespan (i.e. the time at which all tasks are finished) is minimal.

## CP Optimizer formulation

Here is a formulation of the RCPSP in CP Optimizer. 

More information about the formulation of this problem in CP Optimizer and the performance of the search is available in this [post](https://ibm.biz/CPO_RCPSP).

> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 N                                 # Number of tasks
 M                                 # Number of resources
 D[i]   : i in [1..N]              # Duration of task i
 Q[i,k] : i in [1..N], k in [1..M] # Number of units of resource k used by task i
 C[k]   : k in [1..M]              # Capacity of resource k
 P                                 # Set of precedence constraints (i,j) between tasks

interval x[i] size D[i]                        : i in [1..N]

minimize max(endOf(x[i]) : i in [1..N])

sum(pulse(x[i],Q[i,k]) : i in [1..N]) <= C[k]  : k in [1..M]
endBeforeStart(x[i],x[j])                      : (i,j) in P
```


## Code samples

The corresponding implementation in Python is available here : [rcpsp.py](python/rcpsp.py)
