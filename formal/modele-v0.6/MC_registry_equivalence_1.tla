---- MODULE MC_registry_equivalence_1 ----
EXTENDS RegistryModelFast2
AllSlots == 0..EndSlot
Full(b) == [i\in 1..(EndSlot+1)|->Block(b,i-1)]
Universe == UNION {{SelectSeq(Full(b),LAMBDA x: Slot(x)\in ss):ss\in SUBSET AllSlots}:b\in Branches}
RegistryEquivalent == \A c\in Universe,e\in Es:Registry(c,e)=Weights(ReplayOps(c,e))
Equivalent == \A c\in Universe,e\in Es:Support(c,e)=ReferenceSupport(c,e)
Static == Init /\ [][UNCHANGED vars]_vars
====
