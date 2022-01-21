# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
C = data["Capacity"]
O = data["Operations"]
M = data['Setups']
N = range(len(O))

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: tasks x[i]
x = [ interval_var(size=[o[3],o[4]])  for o in O ]
f = state_function(M)

model.add(
 # Objective: maximize number of executed tasks
 [ minimize( max( [ end_of(x[i])   for i in N ]))               ] +
 # Constraints: selection of an opportunity for each task i
 [ always_equal(f, x[o[0]], o[1], True, True)        for o in O ] +
 # Constraints: limited capacities of stations s
 [ sum( [ pulse(x[o[0]],o[2]) for o in O  ]) <= C               ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(TimeLimit=30,LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION

S = sorted([ (sol.get_var_solution(x[o[0]]).start,o[0])  for o in O ])
for s in S:
    op,o = sol.get_var_solution(x[s[1]]), O[s[1]]
    print("Operation " + str(o[0]) + " wafers " + str(o[2]) + " family " + str(o[1]) + " on " + str(op.start) + " -> " + str(op.end))
