# 1. READING THE DATA

import json
with open("data-ft10.json") as file:
    data = json.load(file)
J = data["jobs"]
N = range(len(J))                                  # Number of jobs
L = [ len(J[i])-1 for i in N ]                     # Last operation of job i
M = range(max([o[0] for i in N for o in J[i] ])+1) # Number of machines
O  = { (i,j) for i in N for j in range(0,L[i]+1)}  # Set of all operations
MC = { (i,j) : J[i][j][0] for (i,j) in O }         # Machine of an operation
PT = { (i,j) : J[i][j][1] for (i,j) in O }         # Processing time of an operation

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: operations
x = { o : interval_var(size=PT[o]) for o in O }

model.add(
 # Objective: minimize makespan
 [ minimize( max(end_of(x[i,L[i]]) for i in N) )             ] +
 # Constraints: operations do not overlap on a machine
 [ no_overlap( x[o] for o in O if MC[o]==m )  for m in M     ] +
 # Constraints: precedence between consecutive operations of a job
 [ end_before_start(x[i,j-1], x[i,j]) for (i,j) in O if 0<j  ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(TimeLimit=30, LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION

for i in N:
    print("Job"+str(i)+":")
    for j in range(L[i]):
        op = sol.get_var_solution(x[i,j])
        print("  "+str(op.start)+"->"+str(op.end))
