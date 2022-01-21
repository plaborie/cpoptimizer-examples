from docplex.cp.model import *

# MODELING THE PROBLEM WITH CP-OPTIMIZER

model = CpoModel()

# Decision variables
c = interval_var(optional=True, size=3,     end=[0,5], name="c")
d = interval_var(optional=True, size=[2,3], end=[0,5], name="d")

# Objective function
model.add(maximize(presence_of(c) + presence_of(d)))

# Constraints
model.add(if_then(presence_of(c), logical_not(presence_of(d)) ))

# SOLVING THE PROBLEM

sol = model.solve(LogVerbosity="Quiet")

# DISPLAY THE SOLUTION

print("Optimal solution: value = {0}".format(sol.get_objective_values()[0]))
for s in sol.get_all_var_solutions():
  if (s.is_present()):
      print("  {0} = [{1},{2})".format(s.get_name(), s.get_start(), s.get_end()))
  else: # s is absent
      print("  {0} = absent".format(s.get_name()))
