# Resource-Constrained Project Scheduling Problem with maximum delays (RCPSP/max)

## Problem description

The Resource-Constrained Project Scheduling Problem with maximum delays (RCPSP/max) is an extension of the classical [RCPSP](../RCPSP/README.md) with some maximal delays between tasks.

## CP Optimizer formulation

Here is a formulation of the RCPSP/max in CP Optimizer. 

Some experiments with the CP Optimizer automatic search on this formulation were performed in 2019 on the 90 largest instances (with 1000 tasks) of the classical [UBO benchmark](https://www.wiwi.tu-clausthal.de/en/chairs/produktion/research/research-areas/project-generator/rcpspmax/) and compared with the best known results: [52 bounds](https://www.wiwi.tu-clausthal.de/fileadmin/Produktion/Benchmark/RCPSP/benchmarks_ubo1000.txt) (either lower-bounds or better solutions) were improved.

> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 N                                 # Number of tasks
 M                                 # Number of resources
 D[i]   : i in [1..N]              # Duration of task i
 Q[i,k] : i in [1..N], k in [1..M] # Number of units of resource k used by task i
 C[k]   : k in [1..M]              # Capacity of resource k
 P                                 # Set of precedence constraints (i,j,d) with 
                                   # (possibly negative) delay d between start times of tasks 

interval x[i] size D[i]                        : i in [1..N]

minimize max(endOf(x[i]) : i in [1..N])

sum(pulse(x[i],Q[i,k]) : i in [1..N]) <= C[k]  : k in [1..M]
startBeforeStart(x[i],x[j],d)                  : (i,j,d) in P
```



## Code samples

The corresponding implementation in Python is available here : [rcpsp_max.py](python/rcpsp_max.py)

This sample also illustrates how the CP Optimizer *conflict refiner* can be used to identify the reasons why a particular instance is infeasible. The instance [data-infeasible.json](python/data-infeasible.json) is infeasible. Running the conflit refiner on this instance explains the reason: the following subset of constraints is inconsistent as it introduces a positive cycle of temporal constraints.

```
startBeforeStart(T0, T3, 2)
startBeforeStart(T5, T0, -2)
startBeforeStart(T3, T5, 1)
```


