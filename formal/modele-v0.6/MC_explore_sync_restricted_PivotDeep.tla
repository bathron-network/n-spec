---- MODULE MC_explore_sync_restricted_PivotDeep ----
EXTENDS RegistryModel_PivotDeep
\* Witness search on a SUB-relation of Next: the Byzantine producer only
\* signs on its private lane 2 (never on the public lane). Every behaviour of
\* RSpec is a behaviour of Spec, so a violated trap is a witness of Spec; a
\* PASS here would say NOTHING about Spec (restricted adversary).
RNext == \/ \E n \in Nodes: Fetch(n)
         \/ \E p \in Nodes, b \in Branches: HProduce(p,b)
         \/ \E s \in 1..EndSlot, mm \in BOOLEAN: AProduce(2,s,mm)
         \/ \E k \in 1..(EndSlot+1): Fork(k)
         \/ \E n \in Nodes: Reveal(n)
         \/ Tick
RSpec == Init /\ [][RNext]_vars
====
