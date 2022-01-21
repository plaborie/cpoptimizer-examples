# Simplified photolithography machine

## Problem description

Here is a CP Optimizer formulation to model a batching machine in the context of a photolithography scheduling problem. A set of `N` operations is to be scheduled on the machine. Each operation `x[i]` consists in the treatment of a set of `W[i]` wafers on the machine. Each operation `i` specifies a minimal (`PTMin[i]`) and a maximal (`PTMAX[i]`) processing time. There are different families of operations, the family of an operation `x[i]` is denoted `F[i]`. The machine can perform several operations at the same time (notion of a batch) provided that:

  1. The processing time of the operations is the same as that of the batch, 
  2. The operations are from the same family and 
  3. The total capacity `CAP` of the machine in terms of number of wafers is not exceeded. 

Batches of operations are synchronized: that is, all operations in the same batch start (resp. end) at the same time. Furthermore, some family-dependent setup time given by a matrix `S` is needed to configure the machine from a given batch family to the next batch family. 

## CP Optimizer formulation

The limited capacity of the machine is modeled as a cumul function. A state function `f` describes the evolution over time of the operation family currently executing on the machine. Batching constraints are defined using `alwaysEqual` constraints on the state function with start and end alignment. In this version we are minimizing the makespan.


> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../typeset_models/README.md)

```
Given:
 N                         # Number of operations
 CAP                       # Capacity of the machine
 W[i]  : i in [1..N]       # Number of wafers of operation i
 PTMIN[i]  : i in [1..N]   # Minimal processing time of operation i
 PTMAX[i]  : i in [1..N]   # Maximal processing time of operation i
 F[i]  : i in [1..N]       # Family of operation i
 S                         # Family-dependent setup time matrix
 
interval x[i] size in [PTMIN[i]..PTMAX[i]     : i in [1..N]
stateFunction f with S
 
minimize max( endOf(x[i])  : i in [1..N] ) 

sum( pulse(x[i],W[i]) :  i in [1..N] ) <= CAP
alwaysEqual(f, x[i], F[i], 1, 1)              : i in [1..N]

```

## Code samples

The corresponding implementation in Python is available here : [simplified_photolithography_machine.py](python/simplified_photolithography_machine.py)