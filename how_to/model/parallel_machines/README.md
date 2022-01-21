# Parallel machine scheduling

## Problem description

This problem is the one described [here](http://yetanothermathprogrammingconsultant.blogspot.com/2021/03/parallel-machine-scheduling-i-two.html)

It is a parallel machine scheduling problem with precedence constraints between jobs. 

* Jobs have release dates: they cannot start before a certain time. 
* Some jobs also have some precedence relationships: they cannot start until some other job finishes. For instance: `job4` needs to wait until job1 is completed. 
* The weights on the jobs can be used used to make some jobs more important: they may be used in some objectives.

We assume we have four identical machines at our disposal and that each job requires one machine.

Several objectives can be considered and combined:

* `min sum weighted tardiness`: tries to minimize the total amount each job being tardy.
* `min sum weighted completion`: pushes all jobs towards early completion
* `min max tardiness`: tries to prevent jobs that are very tardy.
* `min num tardy jobs`: minimize the number of tardy jobs. This can help prevent many jobs from being just a little bit tardy.
* `min makespan`. minimize the completion time of the last job


## CP Optimizer formulation

As in the problem, the machines are equivalent, we do not need to handle the allocation of job to particuar machines in this problem. It is sufficient to constrain the number of jobs executing at any moment to be less than 4. This constraint is modeled on a cumul function counting the number of jobs executing at any time. 


> NOTE: The conventions for typesetting CP Optimizer models are available [here](../../typeset_models/README.md)

```
Given:
 N                         # Number of jobs
 M                         # Number of machines
 P[i] : i in [1..N]        # Processing time of job i
 R[i] : i in [1..N]        # Release date of job i
 D[i] : i in [1..N]        # Due date of job i
 W[i] : i in [1..N]        # Weight of job i
 G                         # Precedence constraints between jobs
 
interval x[i] size P[i] in [R[i]..+oo]     : i in [1..N]

sumtardiness  = sum( W[i] * max(0, endOf(x[i])-D[i])  : i in [1..N] )
sumcompletion = sum( W[i] * endOf(x[i])               : i in [1..N] )
maxtardiness  = max(        max(0, endOf(x[i])-D[i])  : i in [1..N] )
numtardy      = sum(        (endOf(x[i])>D[i])        : i in [1..N] )
makespan      = max(        endOf(x[i])               : i in [1..N] )

minimize sumtardiness     # For example

sum( pulse(x[i],1) :  i in [1..N] ) <= M
endBeforeStart(x[i],x[j])                     : (i,j) in G
alwaysEqual(f, x[i], F[i], 1, 1)              : i in [1..N]

```

## Code samples

The corresponding implementation in Python is available here : [parallel_machines.py](python/parallel_machines.py)