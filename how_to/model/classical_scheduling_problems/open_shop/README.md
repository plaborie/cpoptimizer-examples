# Classical Open-shop scheduling problem

## Problem description

The input to the open-shop scheduling problem consists of a set of `N` jobs, another set of `M` machines, and a two-dimensional table of the amount of time each job should spend at each machine (possibly zero). Each job may be processed only at one machine at a time, and each machine can process only one job at a time. However, unlike the [job-shop](../job_shop/README.md) problem, the order in which the processing steps happen can vary freely. The goal is to assign a time for each job to be processed by each machine, so that no two jobs are assigned to the same machine at the same time, no job is assigned to two machine at the same time, and every job is assigned to each machine for the desired amount of time. The usual measure of quality of a solution is its makespan, the amount of time from the start of the schedule (the first assignment of a job to a machine) to its end (the finishing time of the last job at the last machine).

## CP Optimizer formulation


> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 N                                  # Number of jobs
 M                                  # Number of machines
 D[i,j] : i in [1..N], j in [1..M]  # Duration of the operation of job i on machine j
 
interval x[i,j] size D[i,j]                 : i in [1..N], j in [1..M]
 
minimize max(endOf(x[i,M]) : i in [1..N])

noOverlap(x[i,k] : i in [1..N])             : k in [1..M]
noOverlap(x[i,k] : k in [1..M])             : i in [1..N]
```

## Code samples

The corresponding implementation in Python is available here : [openshop.py](python/openshop.py)
