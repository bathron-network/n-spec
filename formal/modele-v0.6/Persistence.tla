---- MODULE Persistence ----
EXTENDS Integers, FiniteSets, TLC
CONSTANT Mutation
Nodes=={1,2}
Digests=={"A","B"}
VARIABLES generation,prepared,witness,exported,committed,crashes
vars== <<generation,prepared,witness,exported,committed,crashes>>
Key(n)==IF Mutation="generation" THEN generation[n] ELSE 0
Init== /\ generation=[n\in Nodes|->0] /\ prepared=[n\in Nodes|->"none"]
 /\ witness={} /\ exported={} /\ committed={} /\ crashes=[n\in Nodes|->0]
Prepare(n,d)== /\ prepared[n]="none" /\ prepared'=[prepared EXCEPT ![n]=d]
 /\ UNCHANGED <<generation,witness,exported,committed,crashes>>
Reserve(n)== /\ prepared[n]#"none"
 /\ ~\E r\in witness:r.key=Key(n) /\ r.digest#prepared[n]
 /\ witness'=witness\cup{[key|->Key(n),digest|->prepared[n]]}
 /\ UNCHANGED <<generation,prepared,exported,committed,crashes>>
Export(n)== /\ prepared[n]#"none" /\ [key|->Key(n),digest|->prepared[n]]\in witness
 /\ exported'=exported\cup{prepared[n]}
 /\ UNCHANGED <<generation,prepared,witness,committed,crashes>>
Commit(n)== /\ prepared[n]\in exported /\ committed'=committed\cup{prepared[n]}
 /\ prepared'=[prepared EXCEPT ![n]="none"]
 /\ UNCHANGED <<generation,witness,exported,crashes>>
CrashRestore(n)== /\ crashes[n]<2 /\ crashes'=[crashes EXCEPT ![n]=@+1]
 /\ prepared'=[prepared EXCEPT ![n]="none"]
 /\ UNCHANGED <<generation,witness,exported,committed>>
Rotate(n)== /\ generation[n]=0 /\ generation'=[generation EXCEPT ![n]=1]
 /\ UNCHANGED <<prepared,witness,exported,committed,crashes>>
Next== (\E n\in Nodes,d\in Digests:Prepare(n,d)) \/
 (\E n\in Nodes:Reserve(n) \/ Export(n) \/ Commit(n) \/ CrashRestore(n) \/ Rotate(n))
Spec==Init /\ [][Next]_vars
S1==Cardinality(exported)<=1
NoWitnessCrash==~(Cardinality(exported)=1 /\ crashes[1]=2 /\ generation[2]=1)
\* Fault verification accepts differing effective contexts, rejects a non-effective key.
Effective(g,r)==g=r
Fault(g1,r1,g2,r2,d1,d2)==Effective(g1,r1) /\ Effective(g2,r2) /\ d1#d2
S2==Fault(0,0,1,1,"A","B") /\ ~Fault(0,0,1,0,"A","B")
====
