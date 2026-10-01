---- MODULE H1Reevaluation ----
EXTENDS Integers, FiniteSets, TLC
VARIABLES ranking,btc,cache,decision
vars==<<ranking,btc,cache,decision>>
Maxima(r)==IF r=0 THEN {"C"} ELSE IF r=1 THEN {"W"} ELSE {"C","W"}
Eval(r,b)==LET m==Maxima(r)
 temporal==b /\ "C"\in m
 base==IF "W"\in m THEN "STOP_DEEP" ELSE "MAINTAIN"
 IN [temporal|->temporal,base|->base,primary|->IF temporal THEN "STOP_H1" ELSE base,
     positive|->IF ~temporal /\ base="MAINTAIN" THEN {"C"} ELSE {}]
Init== /\ ranking=0 /\ btc=TRUE /\ cache=TRUE /\ decision=Eval(0,TRUE)
Update(r,b)== /\ ranking'=r /\ btc'=b /\ decision'=Eval(r,b) /\ UNCHANGED cache
Evict== /\ cache'=~cache /\ UNCHANGED <<ranking,btc,decision>>
Next==(\E r\in 0..2,b\in BOOLEAN:Update(r,b)) \/ Evict
Spec==Init /\ [][Next]_vars
Reevaluated==decision=Eval(ranking,btc)
BaseRetained=="W"\in Maxima(ranking) => decision.base="STOP_DEEP"
H1Subset==decision.positive\subseteq (IF decision.base="MAINTAIN" THEN {"C"} ELSE {})
MaintainVeto==decision.temporal=>decision.positive={}
NoWitnessRankExit==~(ranking=1 /\ btc /\ ~decision.temporal /\ decision.base="STOP_DEEP")
====
