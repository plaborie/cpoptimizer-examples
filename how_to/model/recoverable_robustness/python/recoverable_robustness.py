# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
n = data["N"]
s = data["S"]
D = data['D']
Q = data['Q']
P = data['P']
N = range(n)
S = range(s)

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: x[k][i] is job i in scenario k
x = [ [interval_var(size=P[k][i], optional=True, end=[0,D[i]], name=str(i)) for i in N] for k in S ]

model.add(
 # Maximize expected number of tasks
 [ maximize( sum( Q[k]*presence_of(x[k][i]) for i in N for k in S))             ] +
 # Tasks present in a scenario must not overlap
 [ no_overlap(x[k][i] for i in N)                for k in S                     ] +
 # If a task is executed in scenario k>0, it must be also planned in baseline scenario 0
 [ presence_of(x[k][i]) <= presence_of(x[0][i])  for i in N for k in range(1,s) ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(TimeLimit=10,LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION

for k in S:
    if k==0:
        print("Reference scenario")
    else:
        print ("Scenario {0}".format(k))
    S = sorted([ (sol.get_var_solution(x[k][i]).start,i)  for i in N if sol.get_var_solution(x[k][i]).is_present() ])
    for s in S:
        print("  Task {0}: start={1}, end={2}, deadline={3}".format(s[1], s[0], s[0]+P[k][s[1]], D[s[1]]))
