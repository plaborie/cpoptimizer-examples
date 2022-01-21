# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
n  = data["ntasks"]
m  = data["nresources"]
C  = data["capacities"]
PT = data["durations"]
R  = data["requirements"]
P  = data["successors"]
N  = range(n)
M  = range(m)

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: tasks x[i]
x = [ interval_var(size = PT[i])                 for i in N      ]

model.add(
 # Objective: minimize project makespan
 [ minimize( max(end_of(x[i]) for i in N) )                      ] +
 # Constraints: precedence between tasks
 [ end_before_start(x[i],x[j])                   for (i,j) in P  ] +
 # Constraints: resource capacity
 [ sum(pulse(x[i],q) for (i,q) in R[k]) <= C[k]  for k in M      ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION

for i in N:
    task = sol.get_var_solution(x[i])
    print("Task"+str(i)+":  "+str(task.start)+"->"+str(task.end))
