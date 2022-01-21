# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
n = data["NJobs"]
m = data["NMachines"]
A = data["MachineJobs"]
C = data["Capacities"]
W = data["TimeWindows"]
N = range(n)
M = range(m)

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: operations x[i]
x = [ interval_var(start=[W[i][0],W[i][1]], end=[W[i][0],W[i][1]])  for i in N ]
# Decision variables: y[i][j] is operations x[i] on resource j
y = [ [ interval_var(optional=True, size=A[j][i][0])  for j in M ]  for i in N ]

model.add(
 # Objective: minimize total resource allocation cost
 [ minimize( sum([A[j][i][2]*presence_of(y[i][j])          for i in N for j in M])) ] +
 # Constraints: limited capacities of resources
 [ sum( [ pulse(y[i][j],A[j][i][1]) for i in N ]) <= C[j]  for j in M               ] +
 # Constraints: resource allocation
 [ alternative(x[i], y[i])                                 for i in N               ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION

for i in N:
    for j in M:
        op = sol.get_var_solution(y[i][j])
        if op.is_present():
            print("Job " + str(i) + " : " + str(op.start) + "->" + str(op.end) + " executed on machine " + str(j) + ", cost: " + str(A[j][i][2]) )
