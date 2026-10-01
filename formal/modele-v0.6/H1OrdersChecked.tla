---------------- MODULE H1OrdersChecked ----------------
EXTENDS Integers, FiniteSets, TLC
CONSTANTS Scenario, Mutation, MaxReorg
Nodes == {1,2}
Branches == {"C","W","L"}
Events == Branches \cup {"BTC","F","A"}
VARIABLES received, adopted, result, auth, audit, evicted
vars == <<received,adopted,result,auth,audit,evicted>>
V(r) == r \cap Branches
Rank(b) == IF b="C" THEN 3 ELSE IF b="W" THEN IF Scenario="mutual" THEN 3 ELSE 2 ELSE 1
M(r) == {b \in V(r): ~\E a \in V(r): Rank(a)>Rank(b)}
Distance(b) == IF Scenario="shallow" THEN 1 ELSE IF b="C" THEN 3 ELSE 2
Deep(c,w,n) == c#w /\ (Distance(c)>MaxReorg \/ Distance(w)>MaxReorg \/
                                      (Mutation="anchor_deep" /\ n=2))
Lag(c,w) == CASE Scenario="inverse" -> c="W" /\ w="C"
 [] Scenario="mutual" -> {c,w}={"C","W"}
 [] Scenario="foreign" -> FALSE
 [] Scenario="false" -> FALSE
 [] Scenario="losers" -> c="W" /\ w="L"
 [] OTHER -> c="C" /\ w="W"
Pairs(r,n,a) == {p \in M(r) \X V(r): Deep(p[1],p[2],n) /\
                          (Mutation#"adopted_only" \/ p[2]=a)}
H1(r,n,a) ==
 IF "BTC" \notin r THEN "FALSE"
 ELSE IF "F" \in r /\ "A" \in r /\ \E p \in Pairs(r,n,a): Lag(p[1],p[2]) THEN "TRUE"
 ELSE IF "A" \notin r /\ Pairs(r,n,a)#{} THEN "UNKNOWN"
 ELSE "FALSE"
Base(r) == IF Cardinality(M(r))=1 THEN M(r) ELSE {}
Evaluate(r,n,a) == IF Mutation="maintain" /\ a="C" THEN "FALSE" ELSE H1(r,n,a)
Permit(r,h) == IF Mutation="promote" /\ h="TRUE" THEN {"W"}
              ELSE IF h="FALSE" THEN Base(r) ELSE {}
Init == /\ received=[n \in Nodes |-> {}] /\ adopted=[n \in Nodes |-> "G"]
 /\ result=[n \in Nodes |-> "FALSE"] /\ auth=[n \in Nodes |-> {}]
 /\ audit=TRUE /\ evicted={}
Deliver(n,items) ==
 /\ items \subseteq Events\received[n] /\ items#{}
 /\ LET r==received[n]\cup items
        h==Evaluate(r,n,adopted[n])
        p==Permit(r,h)
    IN /\ received'=[received EXCEPT ![n]=r]
       /\ result'=[result EXCEPT ![n]=h]
       /\ auth'=[auth EXCEPT ![n]=p]
       /\ adopted'=[adopted EXCEPT ![n]=IF p={} THEN @ ELSE CHOOSE b \in p: TRUE]
       /\ audit'=(audit /\ p \subseteq Base(r))
 /\ UNCHANGED evicted
Evict(n) == /\ n\notin evicted /\ evicted'=evicted\cup{n}
            /\ UNCHANGED <<received,adopted,result,auth,audit>>
Next == (\E n\in Nodes,items\in SUBSET Events: Deliver(n,items)) \/ (\E n\in Nodes: Evict(n))
Spec == Init /\ [][Next]_vars
H1Order == received[1]=received[2] => result[1]=result[2]
H1Subset == audit
H1NonVacuity == \A n\in Nodes:
 (received[n]=Events /\ Scenario\in {"forward","stale","mutual"}) => result[n]="TRUE"
H1Orientation == \A n\in Nodes:
 (received[n]=Events /\ Scenario\in {"inverse","foreign","false","losers","shallow"}) => result[n]="FALSE"
NoContinuation == \A n\in Nodes: H1(received[n],n,adopted[n])="TRUE" => auth[n]={}
NoWitnessCommonVeto == ~(received[1]=Events /\ received[2]=Events /\ result[1]="TRUE" /\ result[2]="TRUE")
NoWitnessMaintain == ~(\E n\in Nodes: adopted[n]="C" /\ result[n]="TRUE")
NoWitnessUnknown == ~(\E n\in Nodes: result[n]="UNKNOWN")
====
