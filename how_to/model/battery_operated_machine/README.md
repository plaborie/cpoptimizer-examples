# Battery operated machine

## Problem description

Suppose you have a machine available for performing activities one at a time. 
Processing an activity `i` consumes some energy on the machine `RD*D[i]` that is proportional to the activity duration `D[i]`. 
The energy is stored on a battery of limited capacity `C`. In between activities, the machine batterry can be recharged at a constant rate `RR`.

Let's suppose for simplification that `RD=RR=1`. For instance, if the machine battery is initially empty and the first activity (say `A`) last 10 time units, then activity `A` will not be able to start earlier than date 10 in order to leave enough time for the battery to charge at level 10. If the next activity (say `B`) lasts 20 units, it will have to wait at least 20 units after the end date of `A` (20) before to start. So a feasible solution is (`t` denotes the start or end time of the activity, `l` the battery level at this time):

`[t=10,l=10]--A->[t=20,l=0] ... [t=40,l=20]--B->[t=60,l=0]`

Another solution could be :

`[t=20,l=20]--A->[t=30,l=10] ... [t=40,l=20]--B->[t=60,l=0]`

The level of the battery is capped by the battery capacity so if in this example the battery capacity is `C=30`, another feasible solution is for instance:

`[t=20,l=20]--A->[t=30,l=10] ... [t=100,l=30]--B->[t=120,l=10]`

## CP Optimizer formulation

Here is a formulation of the problem on a single battery operated machine, assuming the battery consumption/production rate is 1 (the model can trivially be adapted to the case of different rates). Activities are optional, have specific time-windows and the objective is to maximize the number of executed activities. It uses expressions `typeOfPrev` to track the level of the battery at the end of each operation.

> NOTE: _The conventions for typesetting CP Optimizer models are available [here](../../typeset_models/README.md)_

    Given:
     N                    # Number of activities
     C                    # Battery capacity
     D[i] : i in [1..N]   # Duration of activity i
     S[i] : i in [1..N]   # Earliest start time of activity i
     E[i] : i in [1..N]   # Latest end time of activity i

    interval x[i] in [S[i]..E[i]], optional, size=D[i]  : i in [1..N]  # Optional activity i
    integer  l[i] in 0..C                               : i in [0..N]  # Battery level at the end of x[i]
    sequence s in x types [1..N]

    maximize sum(presenceOf(x[i]) : i in [1..N])

    noOverlap(seq)
    l[0] = 0
    l[i] = min( C, l[typeOfPrev(s,x[i],0)] + startOf(x[i],D[i]) - endOfPrev(s,x[i],0) ) - D[i]  : i in [1..N]

The formulation uses a sequence variable `s` on the set of optional actvities `x`. In this sequence variables, the type of activity `x[i]` is the index `i` of the activity.

Variable `l[i]` denotes the level of the battery at the end of activity `x[i]`. An additional variable `l[0]` denotes the initial level of the battery. 

The last constraints of the formulation define the level of the battery at the end of activity `x[i]` to be equal to the level of the battery at the end of the previous activity (the one with index `typeOfPrev(s,x[i],0)`) plus the delay between the end time of the previous activity (`endOfPrev(s,x[i],0)`) and the start time of `x[i]` capped by battery capacity `C`, minus the battery consumption of activity `x[i]` (`D[i]`).

These constraints are also valid when interval variable `x[i]` is absent as in this case `typeOfPrev(s,x[i],0)=0`, `startOf(x[i],D[i])=D[i]`, `endOfPrev(s,x[i],0)=0` and the constraint boils down to `l[i] = min(C,l[0]+D[i])-D[i]` which is a valid value in the domain of `l[i]`.


## Code samples

The corresponding formulation in OPL is here : [single-machine.mod](./opl/single-machine.mod)

A second OPL model ([jobshop-batteries.mod](./opl/jobshop-batteries.mod)) integrates the battery operated machines in a classical jobshop scheduling problem. 
