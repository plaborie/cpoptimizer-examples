# Oversubscribed satellite scheduling problem

## Problem description

This problem was initially described in [1]. It is a generalization of two real-world oversubscribed scheduling domains, the USAF Satellite Control Network (AFSCN) scheduling problem and the USAF Air Mobility Command (AMC) airlift scheduling problem. 

In the AFSCN version, the problem instance consists of `N` tasks (communication requests). These tasks require some resource to execute (a ground station among a set of `M` possible ground stations). Each ground station has a limited capacity (number of antennas). Each task `i` has a number of opportunities `O[i]` to be executed on the ground stations. If the task is executed, it needs to select one of these opportunities. Each opportunity `j` of a task `i` requires one antenna of ground station `R[i,j]`. Furthermore, each opportunity defines a duration `D[i,j]` and a possible time window `[S[i,j],E[i,j]]` within which the duration of the task needs to be allocated. This time window corresponds to satellite visibility from the graound station. All tasks are optional, the objective is to minimize the number of unassignedtasks.

The results of the CP Optimizer automatic search on these problems are reported in [2].

[1] L. A. Kramer, L. V. Barbulescu, S. F. Smith. _Understanding Performance Trade-offs in Algorithms for Solving Oversubscribed Scheduling_. In: Proc. 22nd AAAI Conference on Artificial Intelligence (AAAI-07). (2007) pp1019-1024.

[2] P. Laborie. _IBM ILOG CP Optimizer for Detailed Scheduling Illustrated on Three Problems_. Proc. 6th International Conference on Integration of AI and OR Techniques in Constraint Programming for Combinatorial Optimization Problems (CPAIOR 2009)


## CP Optimizer formulation


> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../typeset_models/README.md)

```
Given:
 N                                     # Number of tasks
 M                                     # Number of ground stations
 C[k]   : k in [1..M]                  # Number of antennas of ground station k
 O[i]   : i in [1..N]                  # Number of opportunities for executing task i
 R[i,j] : i in [1..N], j in [1..O[i]]  # Ground station used by opportunity j of task i
 D[i,j] : i in [1..N], j in [1..O[i]]  # Duration of task i in opportunity j
 S[i,j] : i in [1..N], j in [1..O[i]]  # Start of time window of task i in opportunity j
 E[i,j] : i in [1..N], j in [1..O[i]]  # End of time window of task i in opportunity j
 
interval x[i] optional                                     : i in [1..N]
interval y[i,j] in [S[i,j],E[i,j]], optional, size=D[i,j]  : i in [1..N], j in [1..O[i]] 
 
maximize sum( presenceOf(x[i])  : i in [1..N] ) 

alternative( x[i], y[i,j] : j in [1..O[i]] )                              : i in [1..N]
sum( pulse(y[i,j],1) :  i in [1..N], j in [1..O[i]] | R[i,j]=k ) <= C[k]  : k in [1..M]
```

## Code samples

The corresponding implementation in Python is available here : [oversubscribed_satellite.py](python/oversubscribed_satellite.py)