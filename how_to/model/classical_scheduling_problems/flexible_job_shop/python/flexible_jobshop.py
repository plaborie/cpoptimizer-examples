# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
m = data["NbMachines"]
J = data["Jobs"]
N = range(len(J))
M = range(m)
O = [len(J[i]) for i in N]

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Operations
x = [ [ interval_var() for j in J[i]] for i in N ]
# Operations on machines
y = [ [ [ interval_var(optional=True, size=a[1]) for a in j ] for j in J[i] ] for i in N]

model.add(
 # Minimize makespan
 [ minimize(max([end_of(x[i][O[i]-1]) for i in N])) ] +
 # Precedence constraints between consecutive operations
 [ end_before_start(x[i][j-1], x[i][j])     for i in N for j in range(1,O[i]) ] +
 # Allocation on possible machines
 [ alternative(x[i][j], y[i][j])            for i in N for j in range(O[i])   ] +
 # Machines can only process one operation at a time
 [ no_overlap([y[i][j][u] for i in N for j in range(O[i]) for u,a in enumerate(J[i][j]) if a[0]==k])   for k in M]
 )

# 3. SOLVING THE PROBLEM

sol = model.solve(TimeLimit=30, LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION

for i in N:
    print("Job"+str(i)+":")
    for j in range(O[i]):
        for u,a in enumerate(J[i][j]):
            sy = sol.get_var_solution(y[i][j][u])
            if (sy.is_present()):
                print("  "+str(sy.start)+"->"+str(sy.end)+ " on machine "+str(a[0]))
