# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
CR = data['CR']
CS = data['CS']
T  = data['TASKS']
M  = { t['id'] : len(t['MODES']) for t in T }
R  = range(len(CR))
S  = range(len(CS))
N  = range(len(T))

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: x[i] is interval of task i
x = { t['id']: interval_var() for t in T}
# Decision variables: y[i,m] is task i in mode m
y = { (t['id'], m['id']): interval_var(optional=True, size=m['DUR']) for t in T for m in t['MODES'] }

model.add(
 # Objective: minimize project makespan
 [ minimize(max(end_of(x[i])                         for i in N))                        ] +
 # Constraints: precedence between tasks
 [ end_before_start(x[t['id']], x[s])                for t in T for s in t['SUCC']       ] +
 # Constraints: mode selection
 [ alternative(x[i], [y[i,j] for j in range(M[i])])  for i in N                          ] +
 # Constraints: non-renewable resource capacity
 [ sum( [ presence_of(y[t['id'],m['id']])*m['QS'][k] for t in T for m in t['MODES'] ] ) <= CS[k]  for k in S ] +
 # Constraints: renewable resource capacity
 [ sum( [ pulse(y[t['id'],m['id']], m['QR'][k])      for t in T for m in t['MODES'] ] ) <= CR[k]  for k in R ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION

for t in T:
    for m in t['MODES']:
        task = sol.get_var_solution(y[t['id'],m['id']])
        if task.is_present():
          print("Task "+str(t['id'])+" executed in mode "+str(m['id'])+":  "+str(task.start)+"->"+str(task.end))
