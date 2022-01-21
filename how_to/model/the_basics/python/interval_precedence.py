from docplex.cp.model import *

# MODELING THE PROBLEM WITH CP-OPTIMIZER

model = CpoModel()

# Decision variables
d = interval_var(optional=True, size=[2,3], end=[0,5], name="d")
e = interval_var(optional=True, size=[2,3], end=[0,5], name="e")

# Objective function
model.add(minimize(end_of(d,1) + end_of(e,5)))

# Constraints
model.add(if_then(presence_of(e), presence_of(d) ))
model.add(end_before_start(d,e))

# SOLVING THE PROBLEM

sol = model.solve(LogVerbosity="Quiet")

# DISPLAY THE SOLUTION

print("Optimal solution: value = {0}".format(sol.get_objective_values()[0]))
for s in sol.get_all_var_solutions():
  if (s.is_present()):
      print("  {0} = [{1},{2})".format(s.get_name(), s.get_start(), s.get_end()))
  else: # s is absent
      print("  {0} = absent".format(s.get_name()))
