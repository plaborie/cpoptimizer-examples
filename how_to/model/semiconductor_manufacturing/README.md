# Semiconductor manufacturing

## Problem description

The problem, described in [1], can be seen as a [flexible job-shop](../classical_scheduling_problems/flexible_job_shop/README.md) using resources similar to the [simplified photolithography machines](../simplified_photolithography_machine/README.md) with an objective function related with the tardiness and the time lag between operations.

The problem consist of scheduling the treatment of a certain number of _wafer lots_ on a set of machines. A wafer lot `i` (or _lot_ for short) can be seen as a _job_ in a job-shop scheduling problem. It is associated a size (the number of wafer) `W[i]`, a priority `P[i]`, a release date `RD[i]` and a due date `DD[i]`.

Each lot `i` needs to follow a series of `O[i]` successive treatment _steps_: `x[i,1]`, `x[i,2]`,..., `x[i,O[i]]`. Steps can be considered as the different operations of a job in a job-shop scheduling problem. 

Each step `x[i,j]` belongs to a particular family `F[i,j]` depending on the type of treatment to be performed and has to be scheduled on one machine among the possible machines that can perform treatment `F[i,j]`.

A set of `M` machine is available. A machine `k in [1..M]` can perform any steps `x[i,j]` whose family `F[i,j]` belongs to a given set `MF[k]`. If a step `x[i,j]` is eligible to be performed on a machine `k`, the machine defines the processing time of the step `PT[k,f]` depending on its family `f=F[i,j]`.

Steps of the same family can be processed together on the same machine `k` (parallel batch) provided that the total number of wafers in the batch does not exceed the machine capacity `C[k]`. Steps that are batched together start and end at the same time.

There is a family-dependent setup times on the machines due to the reconfiguration of the machine when switching from one family to the other. The setup time duration on a machine `k` to switch from a family `f1` to the next family `f2` is given by a matrix `S[k][f1][f2]`.

Some physical and chemical properties may impose some maximum time lags between pairs of steps of a given lot. This is a soft constraint with a violation cost. More formally for some pairs of endpoints `(t1,t2)` (start or end) of some steps of a given lot, the violation cost `V` of the maximum time lag between `t1` and `t2` is a growing function of the time lag `l = t2 - t1`:

   * `V` is 0 as long as `l<=A`
   * `V` grows quadratically when `A<l<=B`
   * `V` saturates to a value `C` when `B<l`

So `V` is given by `V = min(C, C*max(0,(l-A)^2/(B-A)^2)`.

In the example, for simplicity we only consider time lags between the end of a step `j1` and the start of a later step `j2>j1`.

There is a lexicographical objective function: 

   * Criterion 1: minimize the total violation of maximum time lags
   * Criterion 2: minimize the weighted tardiness cost of lots


[1] S. Knopp, S. Dauzère-Pérès, C. Yugma. _Modeling Maximum Time Lags in Complex Job-Shops with Batching in Semiconductor Manufacturing_. In 15th International Conference on Project Management and Scheduling (2016), pp. 227–230.


## CP Optimizer formulation


> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../typeset_models/README.md)

```
Given:
 N                                     # Number of lots
 W[i]    : i in [1..N]                 # Number of wafers of lot i
 P[i]    : i in [1..N]                 # Priority of lot i
 RD[i]   : i in [1..N]                 # Release date of lot i
 DD[i]   : i in [1..N]                 # Due date of lot i
 O[i]    : i in [1..N]                 # Number of steps of lot i
 F[i,j]  : i in [1..N], j in [1..O[i]] # Family of step j of lot i
 M                                     # Number of machines
 CAP[k]  : k in [1..M]                 # Capacity of machine k
 S[k]    : k in [1..M]                 # Family-dependent setup time matrix of machine k
 MF[k]   : k in [1..M]                 # Set of families executable by machine k
 PT[k,f] : k in [1..M], f in MK[k]     # Processing time of a step of family f on machine k
 L                                     # Number of max time lag constraints
 LOT[l]  : l in L                      # Lot of time lag constraint l
 S1[l]   : l in L                      # Source step of time lag constraint l
 S2[l]   : l in L                      # Target step of time lag constraint l
 A[l]    : l in L                      # Coefficient A of time lag constraint l
 B[l]    : l in L                      # Coefficient B of time lag constraint l
 C[l]    : l in L                      # Coefficient C of time lag constraint l
 
Let M[i,j] = { k | F[i,j] in MF[k] } denote the set of machines that can perform step i,j
 
interval x[i,j]                                : i in [1..N], j in [1..O[i]]
interval y[i,j,k] optional, size=PT[k,F[i,j]]  : i in [1..N], j in [1..O[i]], k in M[i,j]
stateFunction f[k] with S[k]                   : k in [1..M]
integer lag[l]                                 : l in [1..L]

minimize staticLex(
  sum( min(C[l], C[l] * max(0,(lag[l]-A[l])^2/(B[l]-A[l])^2) : l in [1..L] ),
  sum( P[i] * max(0, endOf(x[i,L[i]])-DD[i])                 : i in [1..N] )
)

RD[i] <= startOf(x[i,1])                             : i in [1..N]
endBeforeStart(x[i,j-1],x[i,j])                      : i in [1..N], j in [2..O[i]]
alternative(x[i,j], [ y[i,j,k] : k in M[i,j] ])      : i in [1..N], j in [1..O[i]]
sum( pulse(y[i,j,k],W[i]) : i in [1..N], j in [1..O[i]] | k in M[i,j] ) <= CAP[k]   : k in [1..M]
alwaysEqual(f[k], y[i,j,k], F[i,j], 1, 1)            : i in [1..N], j in [1..O[i]], k in M[i,j]
endAtStart(x[LOT[l],S1[l]], x[LOT[l],S2[l]], lag[l]) : l in [1..L]
```

## Code samples

The corresponding implementation in Python is available here : [semiconductor_manufacturing.py](python/semiconductor_manufacturing.py)