# Resource-Constrained Project Scheduling Problem with discounted cash flows (RCPSPDC)

## Problem description

The Resource-Constrained Project Scheduling Problem with discounted cash flows is an extension of the classical [RCPSP](../RCPSP/README.md). The problem can be stated as follows. Given:

   * A set of `N` tasks with given durations
   * A set of `M` resources with given capacities,
   * A network of precedence constraints between the tasks
   * For each task and each resource the amount of the resource required by the task over its execution
   * A deadline `H` for the project
   * For each task `i`, a cash flow `A[i]` : the cash flow is negative if the task consumes some cash and positive in case it produces some cach
   * A discounted rate `R`

The goal of the RCPSP is to find a schedule satisfying all the constraints (i.e. precedence and resource capacity constraints) that maximizes the project net present value (NPV) defined as (assuming `end_of(x[i])` is the end of task `i`): 

```
NPV = sum( A[i] * exp(-R * end_of(x[i])) : i in [1..N]
```


## CP Optimizer formulation

Here is a formulation of the RCPSPDC in CP Optimizer. 

> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 N                                 # Number of tasks
 M                                 # Number of resources
 H                                 # Project deadline
 R                                 # Discount rate
 A[i]   : i in [1..N]              # Cash flow of task i
 D[i]   : i in [1..N]              # Duration of task i
 Q[i,k] : i in [1..N], k in [1..M] # Number of units of resource k used by task i
 C[k]   : k in [1..M]              # Capacity of resource k
 P                                 # Set of precedence constraints (i,j) between tasks
 

interval x[i] in [0..H], size=D[i]             : i in [1..N]

maximize sum(A[i] * exp(-R*endOf(x[i])) : i in [1..N])

sum(pulse(x[i],Q[i,k]) : i in [1..N]) <= C[k]  : k in [1..M]
endBeforeStart(x[i],x[j])                      : (i,j) in P
```

## Code samples

The corresponding implementation in Python is available here : [rcpspdc.py](python/rcpspdc.py)
