using CP;

int N = 1000; // Number of activities
int C = 100;  // Battery capacity
int H = 30*N;

// Random data
execute {
  Opl.srand(1);
}
int D[i in 1..N] = 1+rand(50);
int S[i in 1..N] = rand(H - (H div 10));
int E[i in 1..N] = S[i]+D[i]+rand(H div 10);

dvar interval x[i in 1..N] optional in S[i]..E[i] size D[i]; // Optional activities x[i]
dvar int l[i in 0..N] in 0..C; // Battery level at the end of x[i]

dvar sequence seq in all(i in 1..N) x[i] types all(i in 1..N) i; // sequence of activities on the machine

execute {
  var f = cp.factory;
  cp.setSearchPhases(f.searchPhase(seq)); 
}

maximize sum(i in 1..N) presenceOf(x[i]);
subject to {
  noOverlap(seq);
  l[0]==0;
  forall (i in 1..N) {
    l[i] == minl(C, l[typeOfPrev(seq,x[i],0)] + (startOf(x[i],D[i])-endOfPrev(seq,x[i],0)))-D[i];
    // When x[i] is absent, by the above constraint: l[i]=0
  }
}
