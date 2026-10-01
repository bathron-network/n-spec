---- MODULE RegistryWindow ----
EXTENDS Integers, Sequences, FiniteSets, TLC
CONSTANTS Threshold, Mutation
Cut == 1
VARIABLES chain, s, pending, phase, installed, audit, rejected, signed
vars == <<chain,s,pending,phase,installed,audit,rejected,signed>>
Raw(c) == SelectSeq(c,LAMBDA b:b.slot<Cut)
Carrier(c) == LET ks=={i\in 1..Len(c):c[i].mature}
 IN IF ks={} THEN 0 ELSE CHOOSE i\in ks: \A j\in ks:i<=j
Count(c) == IF Carrier(c)=0 THEN 0 ELSE Cardinality({i\in 1..Carrier(c):c[i].slot>=Cut})
Support(c) == IF Mutation="tip" THEN c ELSE
 IF Carrier(c)>0 /\ (Mutation="no_threshold" \/ Count(c)>=Threshold) THEN Raw(c) ELSE <<>>
R(c) == 4+Len(Support(c))
Init == /\ chain= <<>> /\ s=0 /\ pending= <<>> /\ phase="idle"
 /\ installed=4 /\ audit=TRUE /\ rejected=0 /\ signed=FALSE
Prepare(m) == /\ phase="idle" /\ s<=5 /\ (m=>s>=3)
 /\ pending'=Append(chain,[slot|->s,mature|->m \/ Carrier(chain)>0,op|->s%3])
 /\ phase'="prepared" /\ UNCHANGED <<chain,s,installed,audit,rejected,signed>>
Validate(ok) == /\ phase="prepared"
 /\ LET candidate==pending
        old==chain
    IN /\ chain'=IF ok THEN candidate ELSE chain
       /\ installed'=IF ok /\ Carrier(candidate)>0 THEN R(candidate) ELSE installed
       /\ audit'=audit /\ (~ok \/ Carrier(old)=0 \/ Count(candidate)=Count(old))
       /\ signed'=signed \/ (ok /\ s>=4 /\ Carrier(candidate)>0)
 /\ phase'="idle" /\ pending'= <<>> /\ s'=s+1
 /\ rejected'=IF ok THEN rejected ELSE rejected+1
Skip == /\ phase="idle" /\ s<=5 /\ s'=s+1
 /\ UNCHANGED <<chain,pending,phase,installed,audit,rejected,signed>>
Next == (\E m\in BOOLEAN:Prepare(m)) \/ (\E ok\in BOOLEAN:Validate(ok)) \/ Skip
Spec == Init /\ [][Next]_vars
ARule == /\ audit /\ (Carrier(chain)>0 => installed=(IF Count(chain)>=Threshold THEN 4+Len(Raw(chain)) ELSE 4))
 /\ \A b\in Raw(chain):b.slot<Cut
NoCircularity == phase="prepared" /\ Carrier(pending)>0 =>
 \A b\in Raw(pending): b.slot<pending[Len(pending)].slot
NoWitnessThreshold == ~(Carrier(chain)>0 /\ Count(chain)=Threshold /\ Len(Raw(chain))>0)
NoWitnessBelow == ~(Carrier(chain)>0 /\ Count(chain)=Threshold-1 /\ Len(Raw(chain))>0)
NoWitnessAbove == ~(Carrier(chain)>0 /\ Count(chain)=Threshold+1 /\ Len(Raw(chain))>0)
NoWitnessEmpty == ~(signed /\ \A b\in {chain[i]:i\in 1..Len(chain)}:b.slot>=4)
NoWitnessReject == ~(rejected>0 /\ signed)
====
