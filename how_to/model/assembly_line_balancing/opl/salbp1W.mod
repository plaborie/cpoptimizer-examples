// 1. READING DATA

int nb_operations    = ...;
range N = 0..nb_operations-1;
int cycle_time       = ...;
int nb_stations      = ...; // Not used in SALBP-1
int durations[N]     = ...;
tuple P { int i; int j; }
{ P } successors = ...;
int W = 2;

// 2. MODELING THE PROBLEM WITH CP-OPTIMIZER
using CP;

// Decision variables: operations
dvar interval op[i in N] size durations[i];

// Decision expression: number of operations over time
cumulFunction load = sum(i in N) pulse(op[i],1);

// Objective: minimize project makespan
dexpr int makespan = max(i in N) endOf(op[i]);
minimize makespan;
subject to {
  // Constraints: precedence between operations
  forall(<i,j> in successors) {
    endBeforeStart(op[i], op[j]);
  }
  // Constraints: time values of station boundaries
  forall (k in N) {
    alwaysIn(load,k*(1+cycle_time),k*(1+cycle_time)+1,0,0);
  }
  // Constraints: maximal number of workers
  load <= W;
}

// 3. POST-PROCESSING
int nstations = (makespan+cycle_time) div (1+cycle_time);
execute {
  writeln("Number of stations = ", nstations);
}
