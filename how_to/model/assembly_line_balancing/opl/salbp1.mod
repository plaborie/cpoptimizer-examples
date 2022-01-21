// 1. READING DATA

int nb_operations    = ...;
range N = 0..nb_operations-1;
int cycle_time       = ...;
int nb_stations      = ...; // Not used in SALBP-1
int durations[N]     = ...;
tuple P { int i; int j; }
{ P } successors = ...;

// 2. MODELING THE PROBLEM WITH CP-OPTIMIZER
using CP;

// Decision variables: operations and station boundaries
dvar interval op[i in N] size durations[i];
dvar interval sb[i in N] size 1;

// Objective: minimize project makespan
dexpr int makespan = max(i in N) endOf(op[i]);
minimize makespan;
subject to {
  // Constraints: dates of station boundaries
  forall(k in N) {
    startOf(sb[k]) == k*(1+cycle_time);
  }
  // Constraints: precedence between operations
  forall(<i,j> in successors) {
    endBeforeStart(op[i], op[j]);
  }
  // Constraints: operations and station boundaries do not overlap
  noOverlap(append(op,sb));
}

// 3. POST-PROCESSING
int nstations = (makespan+cycle_time) div (1+cycle_time);
execute {
  writeln("Number of stations = ", nstations);
}

