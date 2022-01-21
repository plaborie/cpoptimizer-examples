# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
n = data["nb_operations"]
m = data["nb_stations"]
D = data["durations"]
S = data["successors"]

N = range(n)
M = range(m+1)

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: operations, station boundaries and cycle time
op = [interval_var(size=D[i]) for i in N ]
sb = [interval_var(size=1)    for k in M ]
c  = integer_var(max([D[i] for i in N]), sum([D[i] for i in N]))

model.add(
 # Objective: minimize cycle time
 [ minimize(c)                                   ] +
 # Constraints: precedence between operations
 [ end_before_start(op[i],op[j])  for [i,j] in S ] +
 # Constraints: operations finish before end time of the last station
 [ end_before_start(op[i],sb[m])  for i in N     ] +
 # Constraints: cycle time of each stations
 [ start_of(sb[k]) == k*(1+c)     for k in M     ] +
 # Constraints: operations and station boundaries do not overlap
 [ no_overlap(op + sb)                           ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(TimeLimit=30, LogPeriod=1000000)
nstations = (sol.get_objective_values()[0]+c) // (1+c)
