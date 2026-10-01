---- MODULE TieDelivery ----
EXTENDS Integers, FiniteSets, TLC
VARIABLES seen,reserved
vars== <<seen,reserved>>
Init== /\ seen= <<{"A"},{"B"}>> /\ reserved= <<"none","none">>
Parent(v)==IF "A"\in v THEN "A" ELSE "B"
Deliver(n)== /\ seen'=[seen EXCEPT ![n]={"A","B"}] /\ UNCHANGED reserved
Reserve(n)== /\ reserved[n]="none" /\ reserved'=[reserved EXCEPT ![n]=Parent(seen[n])]
 /\ UNCHANGED seen
Next==\E n\in 1..2:Deliver(n) \/ Reserve(n)
Spec==Init /\ [][Next]_vars
ParentDeterministic==seen[1]=seen[2] => Parent(seen[1])=Parent(seen[2])
ReservationsConverge==seen[1]=seen[2] /\ "none"\notin {reserved[1],reserved[2]} => reserved[1]=reserved[2]
====
