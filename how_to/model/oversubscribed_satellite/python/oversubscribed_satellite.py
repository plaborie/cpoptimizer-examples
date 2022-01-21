# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
S = { s[1] : s for s in data["Stations"] }
O = [ tuple(o) for o in data["Opportunities"] ]
T = set([str(o[0]) for o in O])

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: tasks x[i]
x = { i : interval_var(optional=True)  for i in T }
# Decision variables: y[o] is opportunity o
y = { o : interval_var(optional=True, size=o[3], start=[o[2],o[4]], end=[o[2],o[4]])  for o in O }

model.add(
 # Objective: maximize number of executed tasks
 [ maximize( sum( [ presence_of(x[i])   for i in T ]))                  ] +
 # Constraints: selection of an opportunity for each task i
 [ alternative(x[i], [ y[o] for o in O if o[0]==i ] )        for i in T ] +
 # Constraints: limited capacities of stations s
 [ sum( [ pulse(y[o],1) for o in O if o[1]==s ]) <= S[s][2]  for s in S ] 
)

# 3. SOLVING THE PROBLEM

sol = model.solve(TimeLimit=30,LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION

for o in O:
    op = sol.get_var_solution(y[o])
    if op.is_present():
        print("Opportunity " + str(o[0]) + " executed on station " + S[o[1]][0] + " on " + str(op.start) + " -> " + str(op.end))
