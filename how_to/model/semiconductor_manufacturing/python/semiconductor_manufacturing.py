# 1. READING THE DATA

import json
with open("data.json") as file:
    data = json.load(file)
N   = data["N"]
W   = data['W']
P   = data['P']
RD  = data['RD']
DD  = data['DD']
O   = data['O']
F   = { (i,j):data['F'][i][j] for i in range(N) for j in range(O[i]) }
M   = data['M']
CAP = data['CAP']
S   = data['S']
MF  = data['MF']
PT  = { (k,f):data['PT'][k][i] for k in range(M) for i,f in enumerate(MF[k]) }
L   = data['L']
LOT = data['LOT']
S1  = data['S1']
S2  = data['S2']
A   = data['A']
B   = data['B']
C   = data['C']

MCH = { (i,j) : { k for k in range(M) if F[i,j] in MF[k] } for i in range(N) for j in range(O[i]) }

# 2. MODELING THE PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *
model = CpoModel()

# Decision variables: steps x[i,j] 
x = { (i,j)   : interval_var(name = "{0}_{1}".format(i,j))      for i in range(N)  for j in range(O[i]) }
# Decision variables: steps on candidate machines y[i,j,k]
y = { (i,j,k) : interval_var(optional=True, size=PT[k,F[i,j]])  for i in range(N)  for j in range(O[i]) for k in MCH[i,j]  }
# Decision variables: state function describing family executing on machine k
f = [ state_function(S[k]) for k in range(M) ]
# Decision variables: Time lags
lag = [ integer_var() for l in range(L)]

model.add(
  # Objective: lexicographical objective 
  [ minimize_static_lex( [
    # Criterion 1: minimize violation of time lag constraints
    sum( [ min([C[l], C[l]*max([0, (lag[l]-A[l])**2/(B[l]-A[l])**2])  ]) for l in range(L) ]),
    # Criterion #2: minimize total weighted tardiness cost
    sum( [ P[i] * max([0,end_of(x[i,O[i]-1])-DD[i]]) for i in range(N) ]) ])                                                                   ] +
  # Constraints: release dates
  [ RD[i] <= start_of(x[i,0])                                                                        for i in range(N)                         ] +
  # Constraints: precedence between consecutive steps of a lot
  [ end_before_start(x[i,j-1], x[i,j])                                                               for i in range(N) for j in range(1,O[i])  ] +
  # Constraints: machine allocation
  [ alternative(x[i,j], [y[i,j,k] for k in MCH[i,j] ])                                               for i in range(N) for j in range(O[i])    ] +
  # Constraints: parallel batches on machines
  [ always_equal(f[k], y[i,j,k], F[i,j], 1, 1) for i in range(N)  for j in range(O[i])               for k in MCH[i,j]                         ] +
  # Constraints: machine capacity
  [ sum( [pulse(y[i,j,k],W[i]) for i in range(N) for j in range(O[i]) if k in MCH[i,j] ]) <= CAP[k]  for k in range(M)                         ] +
  # Constraints: time lags
  [ end_at_start(x[LOT[l],S1[l]], x[LOT[l],S2[l]], lag[l])                                           for l in range(L)                         ]
)

# 3. SOLVING THE PROBLEM

sol = model.solve(TimeLimit=60,LogPeriod=1000000)

# 4. DISPLAY THE SOLUTION

S = sorted([ (sol.get_var_solution(y[i,j,k]).start,i,j,k)  
     for i in range(N) 
     for j in range(O[i]) 
     for k in MCH[i,j] if sol.get_var_solution(y[i,j,k]).is_present() ])

for s in S:
    op = sol.get_var_solution(x[s[1],s[2]])
    print("Lot {0}, step {1}, wafers {2}, family {3} on machine {4} : {5} -> {6}".format(s[1],s[2],W[s[1]],F[s[1],s[2]],s[3],op.start,op.end))
    