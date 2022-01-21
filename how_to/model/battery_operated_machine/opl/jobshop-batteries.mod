using 

int nbJobs = 6;
int nbMchs = 6;

range Jobs = 1..nbJobs;
range Mchs = 1..nbMchs; 
// Mchs is used both to index machines and operation position in job

tuple Operation {
  int mch; // Machine
  int pt;  // Processing time
};

Operation Ops[Jobs][Mchs] = [
 [ <6,4>, <2,3>, <5,3>, <4,2>, <1,1>, <3,2> ],
 [ <2,3>, <1,8>, <6,7>, <3,2>, <5,9>, <4,3> ],
 [ <4,1>, <5,9>, <2,9>, <1,7>, <6,5>, <3,5> ],
 [ <4,8>, <5,2>, <2,1>, <6,7>, <3,8>, <1,9> ],
 [ <2,6>, <4,2>, <5,5>, <6,5>, <1,3>, <3,1> ],
 [ <5,10>, <3,4>, <1,4>, <4,3>, <2,2>, <6,3> ]
];

int C = 10; // Battery capacity

int O[j in Jobs][m in Mchs] = first({o | o in Mchs : Ops[j][o].mch == m}); // Operation of job j on machine m

dvar interval op[j in Jobs][o in Mchs] size Ops[j][o].pt;
dvar sequence mchs[m in Mchs] 
  in    all(j in Jobs, o in Mchs : Ops[j][o].mch == m) op[j][o]
  types all(j in Jobs, o in Mchs : Ops[j][o].mch == m) j;
          
dvar int l[m in Mchs][j in 0..nbJobs] in 0..C; // Battery level at the end of operation of job j on machine m

minimize max(j in Jobs) endOf(op[j][nbMchs]);
subject to {
  forall (m in Mchs) {
    l[m][0] == 0;
    noOverlap(mchs[m]);
    forall (j in Jobs) {
      l[m][j] == minl(C, l[m][typeOfPrev(mchs[m],op[j][O[j][m]],0)] + (startOf(op[j][O[j][m]])-endOfPrev(mchs[m],op[j][O[j][m]],0)))-Ops[j][O[j][m]].pt;
    }      
  }    
  forall (j in Jobs, o in 1..nbMchs-1)
    endBeforeStart(op[j][o], op[j][o+1]);
}
