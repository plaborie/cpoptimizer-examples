# Multi-Mode Resource-Constrained Project Scheduling Problem (MM-RCPSP)

## Problem description

The MM-RCPSP (Multi-Mode Resource-Constrained Project Scheduling Problem) is a generalization of the [Resource-Constrained Project Scheduling problem](../RCPSP/README.md).

In the MM-RCPSP, each task can be performed in one out of several modes.
Each mode of a task represents an alternative way of combining different levels of resource requirements with a related duration.

Renewable and non-renewable resources are distinguished.

While renewable resources have a limited instantaneous availability such as
manpower and machines, non renewable resources are limited for the entire project, allowing to model, e.g., a budget for the project.

The objective is to find a mode and a start time for each activity such that the schedule is makespan minimal and feasible with regard to the precedence and resource constraints.


## CP Optimizer formulation

Here is a formulation of the MM-RCPSP in CP Optimizer. 

Each task `i` is represented by an interval variable `x[i]`. The possible execution modes of a task `i` are represented by optional interval variables `y[i,m]`. Interval variable `y[i,m]` will be present if and only if mode `m` is the selected mode for task `i`. Mode selection is formulated as `alternative` constraints. Resource constraints are posted on the mode variables `y[i,m]` for renewable and non-renewable resources. Non-renewable resources use classical linear expressions on the Boolean presents status of the mode whereas renewable resources use cumul functions as they constrain the resource level at any point in time. 

> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 S                                 # Number of non-renewable resources
 R                                 # Number of renewable resources
 CS[k]     : k in [1..S]           # Capacity of non-renewable resource k
 CR[k]     : k in [1..R]           # Capacity of renewable resource k
 N                                 # Number of tasks
 P                                 # Set of precedence constraints (i,j) between tasks
 M[i]                              # Number of modes for executing task i
 D[i,m]    : i in [1..N], m in [1..M[i]] 
                                   # Duration of task i in mode m
 QS[i,m,k] : i in [1..N], m in [1..M[i]], k in [1..S] 
                                   # Number of units of non-renewable resource k used by task i in mode m
 QR[i,m,k] : i in [1..N], m in [1..M[i]], k in [1..R] 
                                   # Number of units of renewable resource k used by task i in mode m

interval x[i]                            : i in [1..N]
interval y[i,m] optional, size=D[i,m]    : i in [1..N], m in [1..M[i]] 

minimize max(endOf(x[i]) : i in [1..N])

alternative( x[i], [y[i,m] : m in [1..M[i]] ])  : i in [1..N]
sum( presenceOf(y[i,m])*QS[i,m,k]) : i in [1..N], m in [1..M[i]], k in [1..S] ) <= CS[k] : k in [1..S]
sum( pulse(y[i,m],QR[i,m,k])       : i in [1..N], m in [1..M[i]], k in [1..R] ) <= CR[k] : k in [1..R]
endBeforeStart(x[i],x[j])                       : (i,j) in P
```


## Code samples

The corresponding implementation in Python is available here : [rcpsp_multi_mode.py](python/rcpsp_multi_mode.py)
