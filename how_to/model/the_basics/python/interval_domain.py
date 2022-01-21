from docplex.cp.model import *

# This function creates a model containing only decision variable x
# and enumerates all its solution. Stated otherwise, it enumerates
# the initial domain of possible values for x

def enumerateValues(x):
    # Create a model containing only interval variable x
    model = CpoModel()
    model.add(x)
    # Enumerate all solutions of the model
    sols = model.start_search(LogVerbosity="Quiet", WarningLevel=0)
    values = []
    for sol in sols:
        solx = sol.get_var_solution(x)
        if (solx.is_present()):
            values.append("[{0},{1})".format(solx.get_start(), solx.get_end()))
        else: # solx is absent
            values.append("absent")
    allvalues = sorted(set(values))
    # Display sorted values
    print("Domain({0}) = {1}".format(x.get_name(), allvalues))

# Examples of interval variables and their domain of possible values

a = interval_var(size=3, end=[0,5], name="a")
enumerateValues(a) # Domain(a) = ['[0,3)', '[1,4)', '[2,5)']

b = interval_var(size=[2,3], end=[0,5], name="b")
enumerateValues(b) # Domain(b) = ['[0,2)', '[0,3)', '[1,3)', '[1,4)', '[2,4)', '[2,5)', '[3,5)']

c = interval_var(optional=True, size=3, end=[0,5], name="c")
enumerateValues(c) # Domain(c) = ['[0,3)', '[1,4)', '[2,5)', 'absent']

d = interval_var(optional=True, size=[2,3], end=[0,5], name="d")
enumerateValues(d) # Domain(d) = ['[0,2)', '[0,3)', '[1,3)', '[1,4)', '[2,4)', '[2,5)', '[3,5)', 'absent']
