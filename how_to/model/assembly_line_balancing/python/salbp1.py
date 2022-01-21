# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
n = data["nb_operations"]
c = data["cycle_time"]
D = data["durations"]
S = data["successors"]
N = range(n)

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: operations and station boundaries
op = [ interval_var(size=D[i])            for i in N ]
sb = [ interval_var(size=1,start=k*(1+c)) for k in N ]

model.add(
 # Objective: minimize project makespan
 [ minimize( max(end_of(op[i]) for i in N) )     ] +
 # Constraints: precedence between operations
 [ end_before_start(op[i],op[j])  for [i,j] in S ] +
 # Constraints: operations and station boundaries do not overlap
 [ no_overlap(op + sb)                           ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(TimeLimit=30, LogPeriod=1000000)
nstations = (sol.get_objective_values()[0]+c) // (1+c)
