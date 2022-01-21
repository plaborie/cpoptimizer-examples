# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
n  = data["n"]
m  = data["m"]
RD = data["rd"]
DD = data["dd"]
W  = data["w"]
D  = data["d"]
N = range(n)
M = range(m)

NW = sum([  W[i]*sum([D[i][j] for j in M]) for i in N])

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: operations
x = [ [interval_var(size=D[i][j]) for j in M] for i in N ]

model.add(
 # Objective: minimize makespan
 [ minimize( sum([ W[i]*abs(end_of(x[i][m-1])-DD[i]) for i in N ]) / NW) ] +
 [ RD[i] <= start_of(x[i][0])                  for i in N] +
 # Constraints: operations do not overlap on machines
 [ no_overlap([x[i][k] for i in N])            for k in M] +
 # Constraints: precedence between consecutive operations of a job
 [ end_before_start(x[i][j-1], x[i][j])        for i in N for j in range(1,m)]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(TimeLimit=30, LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION

for i in N:
    print("Job"+str(i)+":")
    for j in M:
        op = sol.get_var_solution(x[i][j])
        print("  "+str(op.start)+"->"+str(op.end))
