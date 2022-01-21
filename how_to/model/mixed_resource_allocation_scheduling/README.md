# Mixed Resource Allocation and Scheduling Problem 


## Problem description

This mixed resource allocation and scheduling problem was described in [1]. It consists of a set of `N` independent jobs that needs to be scheduled within their specified time window. A set of `M` resources is available for executing the jobs. Each job must be executed on one of the `M` machines. The duration of the job depends on the machine. machines can execute jobs in parallel provided their maximal capacity is not exceeded. Each machine has a maximal capacity and each job requires a certain capacity of the machine (this quantity depends on the machine the job is allocated to). Finally, there is an allocation cost for each pair (job,machine). The problem is to allocate a machine to each job and find a start time for each job so that the overall allocation cost is minimized.

CP Optimizer was used to find for the first time an optimal solution for all the instances of the benchmark proposed in [1]. More information about the formulation of this problem in CP Optimizer and the performance of the automatic search is available in [2].


[1] J.N. Hooker. _A Hybrid Method for Planning and Scheduling_. In: Proc. 10th International Conference on Principles and Practice of Constraint Programming (CP 2004).

[2] P. Laborie. _An Update on the Comparison of MIP, CP and Hybrid Approaches for Mixed Resource Allocation and Scheduling_. In: Proc. 15th International Conference on the Integration of Constraint Programming, Artificial Intelligence, and Operations Research (CPAIOR 2018) 

## CP Optimizer formulation

The formulation creates one interval variable `x[i]` per job and one optional interval variable `y[i,j]` per possible allocation pair (job,resource). The objective is to minimize the total resource allocation cost formulated as a sum of the individual allocation cost of the present interval variables `y[i,j]`. Resource allocation is modeled thanks to 'alternative' constraints. The constraint on the maximal capacity of resources uses a cumul function.

> NOTE: _The conventions for typesetting CP Optimizer models are available [here](../../typeset_models/README.md)_

    Given:
     N                                  # Number of jobs
     M                                  # Number of resources
     W[i]   : i in [1..N]               # Time window of job i
     C[j]   : j in [1..M]               # Capacity of resource j
     D[i,j] : i in [1..N], j in [1..M]  # Duration of job i on resource j
     Q[i,j] : i in [1..N], j in [1..M]  # Quantity of resource j used by job i
     F[i,j] : i in [1..N], j in [1..M]  # Cost of allocating job i to resource j
 
    interval x[i] in W[i]                 : i in [1..N]               # Job i
    interval y[i,j] optional, size D[i,j] : i in [1..N], j in [1..M]  # Job i on resource j
 
    minimize sum( F[i,j]*presenceOf(y[i,j]) : i in [1..N], j in [1..M] )
     
    alternative(x[i], y[i,j] : j in [1..M] )            : i in [1..N]
    sum( pulse(y[i][j],Q[i,j]) : i in [1..N] ) <= C[j]  : j in [1..M]
    
## Code samples

The corresponding formulations in Python is here : [mras.py](./python/mras.py)
