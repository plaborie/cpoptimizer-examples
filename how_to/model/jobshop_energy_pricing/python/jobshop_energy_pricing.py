# 1. READING THE DATA

job, pos, mch, dur, end, nrj = range(6)

import json
with open("E11e.json") as file:
    data = json.load(file)
n     = data["N"]
m     = data["M"]
WIdle = data['WIdle']
Ops   = data['Ops']
N = range(n)
M = range(m)

# Energy price during the day
PriceArray = [26,26,27,26,26,29,36,46,44,39,53,47,42,42,40,39,48,67,78,80,81,73,63,48]
# Energy price after horizon
EM = 100000
# Common power
P = 5

# 2. MODELING THE MAKESPAN MINIMIZATION PROBLEM WITH CP-OPTIMIZER

from docplex.cp.model import *

model = CpoModel()

OPERS = { (o[job],o[pos]): o for o in Ops }

# Decision variables: operations x[j,p]
x = { o: interval_var(size=OPERS[o][dur], name='J{}O{}'.format(o[job],o[pos]))  for o in OPERS }
schedule = interval_var(name='Schedule')

model.add(span(schedule, [x[o] for o in OPERS] ))
model.add(end_before_start(x[o], x[o[job],o[pos]+1]) for o in OPERS if OPERS[o][end]==0 )
model.add(no_overlap(x[o] for o in OPERS if OPERS[o][mch]-1==k) for k in M)

makespan = end_of(schedule)

objective = minimize( makespan )
model.add(objective)

# 3. SOLVING THE MAKESPAN MINIMIZATION PROBLEM

res = model.solve(TimeLimit=600, NoOverlapInferenceLevel="Extended", LogPeriod=1000000);

# Set solution as starting point for minimizing energy
model.set_starting_point(res.get_solution())

H = int(res.get_objective_values()[0])

# 4. CHANGING THE OBJECTIVE FUNCTION TO MINIMIZE TOTAL ENERGY

def integral(Price,H):
    I = [EM for h in range(H+2)]
    I[0],I[1] = 0,PriceArray[0]
    for h in range(1,H):
        I[h+1]=I[h]+PriceArray[h%24]
    return I

I = integral(PriceArray,H)

def price(s,d):
    return I[s+d]-I[s] if s+d<=H else EM

D = set([o[dur] for o in Ops])

# Price(t) gives the price at time t
Price = CpoSegmentedFunction((0,-1), [ (t,PriceArray[t%24],PriceArray[(t+1)%24]-PriceArray[t%24])  for t in range(H) ])
# TotalPrice(t) gives the integral of the price on [0,t)
TotalPrice = CpoSegmentedFunction((0,-1), [ (t,I[t],I[t+1]-I[t])  for t in range(H) ])
# StartPrice[d](t) gives the integral of the price on [t,t+d)
StartPrice = { d: CpoSegmentedFunction((0,-1), [ (t,price(t,d),price(t+1,d)-price(t,d))  for t in range(H) ]) for d in D }

common_energy_cost    = P * end_eval(schedule, TotalPrice);
operation_energy_cost = sum( o[nrj] * start_eval(x[o[job],o[pos]], StartPrice[o[dur]]) for o in Ops)
idle_energy_cost      = sum( WIdle[k] * end_eval(schedule, TotalPrice) for k in M) \
                      - sum( WIdle[o[mch]-1] * start_eval(x[o[job],o[pos]], StartPrice[o[dur]]) for o in Ops)

energy_cost = common_energy_cost + operation_energy_cost + idle_energy_cost;

model.remove(objective)
model.add(makespan <= H)
# New objective: minimize total energy
objective = minimize( energy_cost )
model.add(objective)

# 5. SOLVING THE ENERGY MINIMIZATION PROBLEM

res = model.solve(TimeLimit=600, LogPeriod=1000000, NoOverlapInferenceLevel="Extended", RelativeOptimalityTolerance=0)

# 4. DISPLAY THE SOLUTION

import docplex.cp.utils_visu as visu
if res and visu.is_visu_enabled():
    visu.timeline('Solution', origin=0, horizon=60)
    visu.panel('Machines')
    for k in M:
        visu.sequence(name='M' + str(k+1),
                      intervals=[(res.get_var_solution(x[o[job],o[pos]]), o[job], 'J{}-O{}'.format(o[job],o[pos])) for o in Ops if o[mch]-1==k])
    visu.panel('Energy price')
    visu.function(segments=Price, color=1)
    visu.show()
