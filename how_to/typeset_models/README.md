A document proposing a way to typeset CP Optimizer models in LaTeX is available [here](conventions.pdf).

Here is the adaptation of these conventions that we will adopt for typesetting CP Optimizer models in text format. If you just want to see a couple of examples, jump to the [Examples](#section_examples) section.

# General constructs

## Comments

Comments are prefixed by `#`

## Scopes

A scope is a set of tuples used for indexing. For describing a scope, we use the
classical set notation. For instance if N and M are two integers:

   * `i in [N..M]` is the set of all integers i in {N,N+1,...M} (assuming N<=M) 
   * `i in [N..M)` is the set of all integers i in {N,N+1,...M-1}
   * `i in [1..N], j in [1..M]` is the cartesian product (i,j) in [1,N]x[1,M]
   * `i,j in [1..N] | i!=j` is the subset of the cartesian product [1,N]x[1,N] such that i!=j

When the order of the elements in the scope is important (like for instance
in the vectors or matrices below), the tuples are supposed to be generated by
iterating on the indexes from left to right. For instance:
`i,j in [1..3] | i!=j` will generate the ordered set of tuples (1,2),(1,3),(2,1),(2,3),(3,1),(3,2).

## Vectors

Vectors are denoted `[v1,v2,...,vn]` or `[ v(s) : s in SCOPE ]`

For instance:

   * `V1 = [i : i in [1..5]]` is vector `[1,2,3,4,5]`
   * `V2 = [i+j: i,j in [1..3] | i!=j]` is vector `[3,4,3,5,4,5]` (see section 'Scopes' above)

Vectors are indexed by the tuples in the scope. If `V` is a vector and `s` a tuple in its scope, the value of `V` for tuple `s` is `V[s]`.

For the examples above:

   * `V1[1]=1, V1[2]=2, ...` 
   * `V2[1,2]=3, V2[1,3]=4,...`

Vectors can be appended by using the `+` operator:

   * `[a,b,c] + [u,v] = [a,b,c,u,v]`

## Sets

Sets are denoted `{v1,v2,...,vn}` or `{ v(s) : s in SCOPE }`

For instance:

   * `S1 = {i : i in [1..5]}` is set `{1,2,3,4,5}`
   * `S2 = {i+j: i,j in [1..3] | i!=j}` is set `{3,4,5}` (see section 'Scopes' above)

## Matrices

Matrices are vectors of vectors.

For instance matrix `M = [ [ |i-j| : i in [1..3] ] : j in [1..3] ]` is matrix:

```
         |  M[1][1]  M[1][2]  M[1][3]  |     |  0  1  2  |
   M  =  |  M[2][1]  M[2][2]  M[2][3]  |  =  |  1  0  1  |
         |  M[3][1]  M[3][2]  M[3][3]  |     |  2  1  0  |
```

## Decision variables

CP Optimizer provides different types of decision variables (integer, interval, sequence, state function). The general syntax for defining a decision variable is:

```
TYPE NAME    DOMAIN
TYPE NAME[s] DOMAIN : s in SCOPE
```
The second construction will create a vector `NAME` of decision variables indexed by scope `s`.

As a rule of thumb, we denote decision variables with lower cases whereas constants of the problem (including known stepwise or piecewise linear functions) are denoted with upper cases.

### Integer variables

The keyword for the type of an integer variable is `integer`. The domain is a set or a vector of integers. So for instance we can have:

```
integer x      in [1..N]
integer y[i]   in {2k+1 : k in [0..M)}  : i in [1..N]
integer z[i,j] in {0,1}                 : i,j in [1..N] | i!=j
```

### Interval variables

The keyword for the type of an interval variable is `interval`. The domain is a subset of domain specifiers in the following order, separated by a comma:

   * Minimal start (R) and maximal end (D) range: `in [R..D]` (default: `in [0..+oo]`)
   * Specification whether the interval is optional: `optional` (default: not optional that is, interval is present)
   * Value or range for the interval size: `size = S` or `size in [S1..S2]` (default: `size in [0..+oo]`)
   * Intensity function (stepwise function F): `intensity = F` (default: no intensity)

For instance:

```
interval x 
interval y[i] in [-H..H]                                                   : i in [1..N]
interval z[i,j] in [0..H], optional, size in [A[i]..B[i]], intensity=F[j]  : i in [1..N], j in [1..M] 
```

### Sequence variables

The keyword for the type of a sequence variable is `sequence`. The domain is a vector `X` of interval variables (see section Vector above). Optionally, the domain can specify a vector of integer types `T` (`T` must have the same dimension as `X`). For instance:

```
sequence s[i] in [x[i,j] : j in [1..M]]                                 : i in [1..N]
sequence r[i] in [x[i,j] : j in [1..M]], types [[T[i,j] : j in [1..M]]  : i in [1..N]
```

### State functions

The keyword for the type of a state function is `stateFunction`. The domain of a state function can specify a matrix of integers as transition distance between the states. For instance:

```
stateFunction f[k]                                : k in [1..M] 
stateFunction g[k] with [D[i,j] : i,j in [0..S)]  : k in [1..M] 
```

## Constraints

Constraints are defined as follows:

```
CONSTRAINT
CONSTRAINT[s] : s in SCOPE
```

The signature of the different constraints available in CP Optimizer is listed in the [Keywords](#keywords) section.

For instance:

```
v[i] <= v[j]                : i,j in [1..N] | i<j
endBeforeStart(x[i],x[i+1]) : i in [1..N)
```

In the case of constraints using vectors as arguments, if there is no ambiguity, the `[` `]` delimiters of the vector can be omitted. For instance `allDifferent( [ x[i] : i in [1..N] ] )` can be simply written `allDifferent(x[i] : i in [1..N])`.

## Expressions

The signature of the different constraints available in CP Optimizer is listed in the [Keywords](#keywords) section.

In the case of expressions using vectors as arguments, if there is no ambiguity, the `[` `]` delimiters of the vector can be omitted. For instance `sum( [ x[i] : i in [1..N] ] )` can be simply written `sum(x[i] : i in [1..N])`.

Blackbox functions are first declared as follow (by default, the dimension D that is the size of the returned vector is 1):

```
blackbox FUNCTION
blackbox FUNCTION dim D
```

For instance:

```
blackbox f dim 2              # f(X)[0] is the average of X, f(X)[1] is the standard deviation
integer  x[i] : i in [1..N]
stats = f(X)
maximize(stats[0] + stats[1])
```

Note that constraints can be used as boolean expressions where CP Optimizer allows it. For example:

   * `x=3 || y=4`
   * `sum( x[i]!=x[j] : i,j in [1..N] | i!=j ) <= K`

Expressions can be defined directly in the constraints they are used in (case 1) or as separate definitions (case 2). The second case is particularly useful when a given expression is used in several constraints.

Two examples of case 1:

   * `sum( R[i]*x[i] : i in [1..N] ) <= D`
   * `sum( pulse(y[i],Q[i]) : i in [1..N] ) <= C`

Equivalent examples using case 2:

```
u = sum( R[i]*x[i] : i in [1..N] )
u <= D
```

```
f = sum( pulse(y[i],Q[i]) : i in [1..N] )
f <= C
```

<a name="section_examples"></a>
# Examples 

## Sudoku

```
Given:
 G[r,c] : r,c in [0..8]  # Value of the input grid, G[r,c]=0 means that the cell is empty

integer x[r,c] in [1..9]                   : r,c in [0..8]

x[r,c] = G[r,c]                            : r,c in [0..8] | G[r,c]!=0  # Input grid values
allDifferent(x[r,c] : c in [0..8])         : r in [0..8]                # Different value on rows
allDifferent(x[r,c] : r in [0..8])         : c in [0..8]                # Different value on columns
allDifferent(x[3i+r,3j+c] : r,c in [0..2]) : i,j in [0..2]              # Different value on sub-squares
```

## Job-shop scheduling problem

The model below formulates a general job-shop scheduling problem (not necessarily rectangular):

```
Given:
 N                                     # Number of jobs
 M                                     # Number of machines
 O[i]   : i in [1..N]                  # Number of operations of job i
 D[i,j] : i in [1..N], j in [1..O[i]]  # Duration of the jth operation of job i
 R[i,j] : i in [1..N], j in [1..O[i]]  # Machine of the jth operation of job i
 
interval x[i,j] size D[i,j]                                  : i in [1..N], j in [1..O[i]]
 
minimize max(endOf(x[i,O[i]]) : i in [1..N])

noOverlap(x[i,j] : i in [1..N], j in [1..O[i]] | R[i,j]=k)   : k in [1..M]
endBeforeStart(x[i,j-1], x[i,j])                             : i in [1..N], j in [2..O[i]]  
```

## Resource-constrained project scheduling problem (RCPSP)

Here is a CP Optimizer formulation of the classical RCPSP with N tasks and M
resources. 

```
Given:
 N                                 # Number of tasks
 M                                 # Number of resources
 D[i]   : i in [1..N]              # Duration of task i
 Q[i,k] : i in [1..N], k in [1..M] # Number of units of resource k used by task i
 C[k]   : k in [1..M]              # Capacity of resource k
 P                                 # Set of precedence constraints (i,j) between tasks

interval x[i] size D[i]                        : i in [1..N]

minimize max(endOf(x[i]) : i in [1..N])

sum(pulse(x[i],Q[i,k]) : i in [1..N]) <= C[k]  : k in [1..M]
endBeforeStart(x[i],x[j])                      : (i,j) in P
```

# Keywords

We use the following notations for the arguments of the operators:

   * `a,b,c,d` Integer or numerical constants
   * `stp` Stepwise function
   * `pwl` Piecewise linear function
   * `u,v,w` Integer variables or expressions
   * `x,y,z` Interval variables
   * `r,s` Sequence variables
   * `cf` Cumul function
   * `sf` State function 

Upper cases denote vectors, for instance `Y` denotes a vector of interval variables, `A` denotes a vector of integer constants. 

`M` denotes a matrix of integers. 

Variants of a given keyword are denoted `[VARIANT1|VARIANT2...]`.

## Constraint keywords

| Keyword                         | Short description     |
| :------------------------------ | :-------------        |
| `=, !=, <=, >=, <, >`             | Classical arithmetical constraints   |
| `allDifferent(V)`                 | Global all different constraint   |
| `pack(U,V,A,w)`                   | Bin-packing constraint   |
| `allMinDistance(U,a)`             | Minimal distance between all values   |
| `inverse(U,V)`                    | Inverse constraint   |
| `allowedAssignments(U,M)`         | Allowed combinations of values   |
| `forbiddenAssignments(U,M)`       | Forbidden combinations of values   |
| `lexicographic(U,V )`             | Lexicographic ordering constraint   |
| `presenceOf(x)`                   |  Presence of an interval variable   |
| `[start\|end][Before\|At][Start\|End](x,y,a)`     | Precedence constraints |
| `forbid[Start\|End\|Extent](x,stp)` | Forbidden values   |
| `alternative(x,Y,u)`              | Alternative   |
| `span(x,Y)`                       | Span   |
| `noOverlap(s,M,bool)`             | No-overlap   |
| `first(s,x)`                      | First on a sequence   |
| `last(s,x)`                       | Last on a sequence   |
| `prev(s,x,y)`                     | Immediately before on a sequence   |
| `before(s,x,y)`                   | Before on a sequence   |
| `sameSequence(r,s,X,Y)`           | Same sequence   |
| `sameCommonSubsequence(r,s,X,Y)`  | Same common subsequence   |
| `isomorphism(X,Y)`                | Isomorphism   |
| `alwaysIn(f,x,a,b)`               | Always-in constraint on cumul or state function   |
| `alwaysEqual(sf,x,a,bool,bool)`   | Always-equal constraint on state function   |
| `alwaysConstant(sf,x,bool,bool)`  | Always-constant constraint on state function   |
| `alwaysNoState(sf,x)`             | Always-no-state constraint on state function   |


## Expression keywords

| Keyword                            | Short description     |
| :--------------------------------- | :-------------        |
| `-, log(x), abs(x), ...`           | Classical unary arithmetical expressions   |
| `!`                                | Classical logical `Not` unary expression   |
| `+, -, *, /, :, mod, x^y`          | Classical binary arithmetical expressions   |
| `x \|\| y, x && y`                   | Classical logical binary expressions   |
| `sum(X), prod(X), min(X), max(X)`  | Classical n-ary arithmetical expressions, `X` is a vector |
| `or(X), and(X)`                    | Classical n-ary logical expressions, `X` is a vector |
| `A[v], U[v]`                       | Array expressions: `v` is an integer index variable |
| `count(U,a)`                       | Count variables with given value   |
| `countDifferent(U)`                | Count number of different values   |
| `standardDeviation(U,a,b)`         | Standard deviation   |
| `[start\|end\|size\|length]Of(x,a)`  |  Start (end, etc.) value of an interval variable   |
| `[start\|end\|size\|length]Eval(pwl,x,a)` | Piecewise linear function evaluated on the start (etc.) value  |
| `[start\|end\|size\|length]OfNext(s,x,a,b)` | Start (etc.) value of next interval in a sequence  |
| `[start\|end\|size\|length]OfPrev(s,x,a,b)` | Start (etc.) value of previous interval in a sequence  |
| `heightAt[Start\|End](cf,x)` | Contribution of `x` to a cumul function at start (or end)  |
| `overlapLength(x,y,a)` | Overlap length between interval variables  |
| `pulse(x,a,b])` |  Cumul expression: pulse  |
| `step(a, b)`  |  Cumul expression: step at constant value |
| `stepAt[Start\|End](x,a,b)` | Cumul expression: step at start (or end) of interval variable |