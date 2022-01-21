# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
n = data["ntasks"]
m = data["nresources"]
C = data["capacities"]
D = data["durations"]
R = data["requirements"]
G = data["delays"]
N = range(n)
M = range(m)

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: tasks x[i]
x = [interval_var(size = D[i], name="T"+str(i)) for i in N]

model.add(
 # Objective: minimize project makespan
 [ minimize(max(end_of(x[i])                     for i in N)) ] +
 # Constraints: precedence between tasks
 [ start_before_start(x[i],x[j],d)               for [i,j,d] in G ] +
 # Constraints: resource capacity
 [ sum(pulse(x[i],q) for [i,q] in R[j]) <= C[j]  for j in M ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION OR FIND A CONFLICT IF PROBLEM IS PROVED INFEASIBLE

if sol.is_solution():
    for i in N:
        task = sol.get_var_solution(x[i])
        print("Task"+str(i)+":  "+str(task.start)+"->"+str(task.end))
elif sol.get_search_status() == SEARCH_STATUS_COMPLETED:
    conflict = model.refine_conflict(add_conflict_as_cpo=False)
    conflict.write()
