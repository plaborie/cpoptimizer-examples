# Classical Hybrid flow-shop scheduling problem

## Problem description

An Hybrid flow-shop scheduling problem is an extended form of classical [flow-shop](../flow_shop/README.md) in which parallel machines are available to perform the same operation. It can be briefly described as follows: a set of jobs has to be processed on a set of processing centers. Each machine centre consists of a set of identical parallel machines, and the non-pre-emptive processing of a job has to be done on exactly one of the machines of each centre.. 

## CP Optimizer formulation


> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../../typeset_models/README.md)

```
Given:
 N                                  # Number of jobs
 M                                  # Number of steps and machines types
 C[j] : j in [1..M]                 # Number of identical machines for step j
 D[i,j] : i in [1..N], j in [1..M]  # Duration of the jth operation of job i
 
interval x[i,j] size D[i,j]                 : i in [1..N], j in [1..M]
 
minimize max(endOf(x[i,M]) : i in [1..N])

sum(pulse(x[i,k],1) : i in [1..N]) <= C[j]  : j in [1..M]
endBeforeStart(x[i,j-1], x[i,j])            : i in [1..N], j in [2..M]  
```

Of course, the classical [jobs-shop](../job_shop/README.md) and [open-shop](../open_shop/README.md) problems can also be easily extended to hybrid jobs-shop and open-shop problems by simply using cumul functions instead of no-overlap constraints.

## Code samples

The corresponding implementation in Python is available here : [hybrid_flowshop.py](python/hybrid_flowshop.py)
