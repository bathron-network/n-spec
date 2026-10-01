---- MODULE BrakeArithmetic ----
EXTENDS Integers, FiniteSets, TLC
VARIABLE Q
vars==<<Q>>
Weights==<<680,120,190,5,5>>
Init==Q\in SUBSET (1..5)
Next==UNCHANGED Q
Total(s)==(IF 1\in s THEN 680 ELSE 0)+(IF 2\in s THEN 120 ELSE 0)+
 (IF 3\in s THEN 190 ELSE 0)+(IF 4\in s THEN 5 ELSE 0)+(IF 5\in s THEN 5 ELSE 0)
Eligible==Total((1..5)\Q)
Filled==IF 1\in Q THEN 0 ELSE 680
Health==Eligible>0 /\ 10*Filled>=7*Eligible
Spec==Init /\ [][Next]_vars
Density068==680*100=68*1000
MaskFixed==Q={2,3,4,5} => Health
DenominatorZero==(Eligible=0)=>~Health
NoWitnessHealth==~(Q={2,3,4,5} /\ Health)
====
