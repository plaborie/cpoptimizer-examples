# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
M = data['MACHINES']
J = data["JOBS"]
G = data['PRECS']

proctime, release, duedate, weights = 0, 1, 2, 3

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: operations
x = { j : interval_var(size=J[j][proctime], start=[J[j][release],INTERVAL_MAX], name=j) for j in J }

# Total weighted tardiness cost
sumtardiness  = sum( J[j][weights] * max(0,end_of(x[j])-J[j][duedate] )  for j in J)
# Total weighted completion time
sumcompletion = sum( J[j][weights] * end_of(x[j])                        for j in J)
# Maximum tardiness
maxtardiness  = max(                 max(0,end_of(x[j])-J[j][duedate] )  for j in J)
# Number of tardy jobs
numtardy      = sum(                 (end_of(x[j])>J[j][duedate] )       for j in J)
# Makespan
makespan      = max(                 end_of(x[j])                        for j in J)

model.add(
 # Objective
 [ minimize(sumtardiness)                                   ] +
 #[ minimize_static_lex([sumtardiness, sumcompletion])      ] +
 # Constraints: number of machines
 [ sum( pulse(x[j],1) for j in J ) <= M                     ] +
 # Constraints: precedence between jobs
 [ end_before_start(x[p], x[s])              for [p,s] in G ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(TimeLimit=5)

# 4. DISPLAY THE SOLUTION

for j in J:
    job = sol.get_var_solution(x[j])
    tardi = max(0, job.end -J[j][duedate])
    if tardi>0:
        print("{0}\t on {1} -> {2} \t tardiness = {3}".format(j,job.start,job.end,tardi))
    else:
        print("{0}\t on {1} -> {2}".format(j,job.start,job.end))
