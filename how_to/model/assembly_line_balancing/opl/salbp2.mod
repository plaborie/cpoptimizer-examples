// 1. READING DATA

int nb_operations    = ...;
range N = 0..nb_operations-1;
int cycle_time       = ...; // Not used in SALBP-2
int nb_stations      = ...;
range M = 0..nb_stations;
int durations[N]     = ...;
tuple P { int i; int j; }
{ P } successors = ...;

// 2. MODELING THE PROBLEM WITH CP-OPTIMIZER
using CP;

// Decision variables: operations, station boundaries and cycle time
dvar interval op[i in N] size durations[i];
dvar interval sb[k in M] size 1;
dvar int c in max(i in N) durations[i] .. sum(i in N) durations[i];

// Objective: minimize cycle time
minimize c;
subject to {
  // Constraints: cycle time of each stations
  forall(k in M) {
    startOf(sb[k]) == k*(1+c);
  }
  // Constraints: precedence between operations
  forall(<i,j> in successors) {
    endBeforeStart(op[i], op[j]);
  }
  // Constraints: operations finish before end time of the last station
  forall(i in N) {
    endBeforeStart(op[i],sb[nb_stations]);
  } 
  // Constraints: operations and station boundaries do not overlap
  noOverlap(append(op,sb));
}

// 3. POST-PROCESSING
execute {
  writeln("Cycle time = ", c);
}

