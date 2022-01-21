# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
n = data["n"]
d = data["d"]
P = data["P"]
S = data["S"]
C = data["C"]
N  = range(n)
D  = range(d)

DC = [ set(j for j in D if P[j]==i)        for i in N ] # Alternative decompositions of task i
NP = [ len(set(j for j in D if i in S[j])) for i in N ] # Number of parent tasks of task i

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

x = [ interval_var(optional=True)             for i in N                          ]
y = [ interval_var(optional=True)             for j in D                          ]

model.add(
# [ maximize ( sum(presence_of(x[i]) for i in N))                                 ] +
  [ presence_of(x[i])                         for i in N if NP[i]==0 and C[i]==1  ] +
  [ alternative(x[i], [y[j] for j in DC[i]])  for i in N if 0<len(DC[i])          ] +
  [ span(y[j], [x[i] for i in S[j]])          for j in D                          ] +
  [ presence_of(y[j]) <= presence_of(x[i])    for j in D for i in S[j] if C[i]==1 ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION

print("Selected tasks: " + str([i for i in N if sol.get_var_solution(x[i]).is_present()]))
