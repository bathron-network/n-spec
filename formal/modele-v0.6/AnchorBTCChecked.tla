---- MODULE AnchorBTCChecked ----
EXTENDS Integers, Sequences, FiniteSets, TLC
CONSTANT Mutation, MaxReorg, Dbtc, SlowBTC
Branches=={"A","B"}
\* Explicit competing Bitcoin chains: differing chainwork, including a tie.
BTC=={"g","a1","a2","a3","a4","b1","b2","b3","b4"}
Parent==[x\in BTC|->CASE x="g"->"g" [] x\in{"a1","b1"}->"g"
 [] x="a2"->"a1" [] x="a3"->"a2" [] x="a4"->"a3"
 [] x="b2"->"b1" [] x="b3"->"b2" [] OTHER->"b3"]
Height(x)==IF x="g" THEN 0 ELSE IF x\in{"a1","b1"} THEN 1 ELSE IF x\in{"a2","b2"} THEN 2 ELSE IF x\in{"a3","b3"} THEN 3 ELSE 4
RECURSIVE Anc(_)
Anc(x)==IF x="g" THEN {"g"} ELSE {x}\cup Anc(Parent[x])
Ref(b,h)==IF h=0 THEN "g" ELSE IF SlowBTC THEN "a3" ELSE IF h<=2 THEN "a1" ELSE "a3"
Min(a,b)==IF a<b THEN a ELSE b
Max(a,b)==IF a>b THEN a ELSE b
VARIABLES tips,anchor,btc,seed,seal,mode,chosen,audit,rank,seen
vars== <<tips,anchor,btc,seed,seal,mode,chosen,audit,rank,seen>>
Init== /\ tips=[n\in 1..2|->[branch|->"G",height|->0]]
 /\ anchor=tips /\ btc={"a4"} /\ seed=FALSE /\ seal=TRUE
 /\ mode=[n\in 1..2|->"RUN"] /\ chosen=[n\in 1..2|->{}] /\ audit=TRUE
 /\ rank\in {<<3,2>>,<<3,3>>}
 /\ seen= <<{"A"},{"B"}>>
Chainwork(x)==Height(x)
BestWork(heads)=={x\in heads: \A y\in heads: Chainwork(x)>=Chainwork(y)}
View==CHOOSE x\in btc:TRUE
BTCOk==/\ Cardinality(btc)=1 /\ (Mutation="forget_seal" \/ ~seal \/ "a1"\in Anc(View))
 /\ (~seed \/ "a2"\in Anc(View))
Valid(b)==Ref(b,3)\in Anc(View)
M(n)=={b\in seen[n]:Valid(b) /\ ~\E c\in seen[n]:Valid(c) /\ rank[IF c="A" THEN 1 ELSE 2]>rank[IF b="A" THEN 1 ELSE 2]}
Compatible(a,b)==a.height=0 \/ a.branch=b
Deep(n,b)==~Compatible(anchor[n],b) \/ (tips[n].branch#b /\ tips[n].height>MaxReorg)
Bbound(b)==CHOOSE h\in 0..3:
 (h=0 \/ (Ref(b,h)\in Anc(View) /\ Height(View)-Height(Ref(b,h))+1>=Dbtc)) /\
 \A k\in (h+1)..3: ~(Ref(b,k)\in Anc(View) /\ Height(View)-Height(Ref(b,k))+1>=Dbtc)
Exact(n,b)==Max(anchor[n].height,Min(Max(0,3-MaxReorg),Bbound(b)))
Select(n)==
 /\ LET stop==~BTCOk \/ (\E b\in M(n):Deep(n,b)) \/ Cardinality(M(n))#1
        b==IF M(n)={} THEN "A" ELSE CHOOSE x\in M(n):TRUE
        h==IF Mutation="free_anchor" THEN 3 ELSE Exact(n,b)
    IN /\ mode'=[mode EXCEPT ![n]=IF Cardinality(btc)>1 THEN "BTC_TIE_PENDING" ELSE IF ~BTCOk THEN "STOP_BTC" ELSE IF \E c\in M(n):Deep(n,c) THEN "STOP_DEEP" ELSE IF Cardinality(M(n))#1 THEN "TIE_OR_WAIT" ELSE "RUN"]
       /\ tips'=IF stop THEN tips ELSE [tips EXCEPT ![n]=[branch|->b,height|->3]]
       /\ anchor'=IF stop THEN anchor ELSE [anchor EXCEPT ![n]=[branch|->b,height|->h]]
       /\ chosen'=[chosen EXCEPT ![n]=IF stop THEN {} ELSE {b}]
       /\ audit'=(audit /\ (stop \/ h=Exact(n,b)))
 /\ UNCHANGED <<btc,seed,seal,rank,seen>>
Reorg(v)== /\ v\in {{"a4"},{"a2","b2"},{"b4"},{"a2"},{"a4","b2"},{"a2","b4"}} /\ btc'=BestWork(v)
 /\ mode'=[n\in 1..2|->"RECHECK"] /\ chosen'=[n\in 1..2|->{}]
 /\ UNCHANGED <<tips,anchor,seed,seal,audit,rank,seen>>
ConsumeSeed== /\ ~seed /\ btc={"a4"} /\ seed'=TRUE
 /\ UNCHANGED <<tips,anchor,btc,seal,mode,chosen,audit,rank,seen>>
Deliver(n)== /\ seen[n]#Branches /\ seen'= [seen EXCEPT ![n]=Branches]
 /\ UNCHANGED <<tips,anchor,btc,seed,seal,mode,chosen,audit,rank>>
Next==(\E n\in 1..2:Select(n)) \/ (\E v\in {{"a4"},{"a2","b2"},{"b4"},{"a2"},{"a4","b2"},{"a2","b4"}}:Reorg(v)) \/ ConsumeSeed \/ (\E n\in 1..2:Deliver(n))
Spec==Init /\ [][Next]_vars
AnchorExact==audit
NewAccept==BTCOk
G0== /\ (NewAccept => "a1"\in Anc(View))
 /\ \A n\in 1..2:mode[n]="RUN" /\ chosen[n]#{} => "a1"\in Anc(View)
SafeBTC==\A n\in 1..2:mode[n]="RUN" /\ chosen[n]#{} => (~seed \/ "a2"\in Anc(View))
A4==anchor[1].height=0 \/ anchor[2].height=0 \/ anchor[1].branch=anchor[2].branch
NoWitnessBTCStop==~(\E n\in 1..2:mode[n]="STOP_BTC" /\ tips[n].height=3)
NoWitnessSealOnly==~(~seed /\ btc={"b4"} /\ (\A n\in 1..2:tips[n].height=0) /\ (\E n\in 1..2:mode[n]="STOP_BTC") /\ ~NewAccept)
NoWitnessSlowAnchor==~(SlowBTC /\ (\E n\in 1..2:tips[n].height=3 /\ anchor[n].height=0 /\ mode[n]="RUN"))
====
