# A recoverable robustness scheduling problem

## Problem description

This problem is described in [1], here is the part of the abstract of this paper that described the problem:

"Minimizing the number of late jobs on a single machine is a classic scheduling problem, which can be used to model the situation that from a set of potential customers, we have to select as many as possible whom we want to serve, while selling no to the other ones. This problem can be solved by Moore–Hodgson’s algorithm, provided that all data are deterministic. We consider a stochastic variant of this problem, where we assume that there is a small probability that the processing times differ from their standard values as a result of some kind of disturbance. When such a disturbance occurs, then we must apply some recovery action to make the solution feasible again. This leads us to the area of recoverable robustness, which handles this uncertainty by modeling each possible disturbance as a scenario; in each scenario, the initial solution must then be made feasible by applying a given, simple recovery algorithm to it. Since we cannot accept previously rejected customers, our only option is to reject customers that would have been served in the undisturbed case. Our problem therefore becomes to find a solution for the undisturbed case together with a feasible recovery to every possible disturbance. Our goal hereby is to maximize the expected number of served customers; we assume here that we know the probability that a given scenario occurs. In this respect, our problem falls outside the area of the ‘standard’ recoverable robustness, which contains the worst-case recovery cost as a component of the objective. Therefore, we consider our approach as a combination of two-stage stochastic programming and recoverable robustness."

[1] M. van den Akker, H. Hoogeveen, J. Stoef. Combining two-stage stochastic programming and recoverable robustness to minimize the number of late jobs in the case of uncertain processing times. Journal of Scheduling. Vol. 21, p607–617.


## CP Optimizer formulation

The input data is a number `N` of jobs to be scheduled and a number `S` of different scenarios. Scenario `0` denotes the baseline scenario where everything occurs as expected. Each job `i` is associated a deadline `D[i]`. Each scenario `k` is associated a probability `Q[k]` and defines particular processing times `P[k][i]` (some variations around the baseline processing time `P[0][i]`) for the tasks `i`.

The problem is to maximize the number of scheduled tasks across all scenarios in the context of recoverable robustness. More precisely, we want a feasible schedule for all the scenarios (that is: all the selected tasks are scheduled before their deadlines) that maximizes the expected number of scheduled tasks and that is such that every task executed in a scenario must also be executed in the baseline scenario. The rationale is that we want to propose a schedule for the baseline scenario that can be easily adapted to the different scenario variants (if this variant occurs) by removing some tasks.  


> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../typeset_models/README.md)

```
Given:
 N                                  # Number of tasks
 S                                  # Number of scenarios
 D[i]   : i in [1..N]               # Deadline of task i
 Q[k]   : k in [0,S-1]              # Probability of scenario k
 P[k,i] : k in [0,S-1], i in [1..N] # Processing time of task i in scenario k
 
interval x[k,i] optional, in [0..D[i]], size P[k,i] : k in [0,S-1], i in [1..N]
 
maximize sum( Q[k] * presenceOf(x[k,i]) ) : k in [0,S-1], i in [1..N] ) 
no_overlap( x[k,i] for i in N )           : k in [0,S-1]
presenceOf(x[k,i]) => presenceOf(x[0,i])  : k in [1,S-1], i in [1..N]
```

## Code samples

The corresponding implementation in Python is available here : [recoverable_robustness.py](python/recoverable_robustness.py)