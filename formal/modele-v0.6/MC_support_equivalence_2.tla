---- MODULE MC_support_equivalence_2 ----
EXTENDS RegistryModelFast
AllSlots == 0..EndSlot
Full(b) == [i\in 1..(EndSlot+1)|->Block(b,i-1)]
Universe == UNION {{SelectSeq(Full(b),LAMBDA x: Slot(x)\in ss):ss\in SUBSET AllSlots}:b\in Branches}
Equivalent == \A c\in Universe,e\in Es:Support(c,e)=ReferenceSupport(c,e)
Static == Init /\ [][UNCHANGED vars]_vars
====
