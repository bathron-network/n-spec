---- MODULE RegistryModelFast2_L1 ----
EXTENDS RegistryModelFast2

\* Observers only: no guard or change of the inherited transition relation.
Before(c,s) == SelectSeq(c,LAMBDA x: Slot(x)<s)
Closed(c,e) == e=0 \/ Carrier(c,e)>0
Forked(a,b) == ~IsPrefix(a,b) /\ ~IsPrefix(b,a)
FirstSlot(a,b) == LET k==LCA(a,b) IN
 IF Slot(a[k+1])<Slot(b[k+1]) THEN Slot(a[k+1]) ELSE Slot(b[k+1])
ForkRegistry(c,s) == ProductionRegistry(Before(c,s),Epoch(s),s)
DifferentEpochs(a,b) == {e\in Es: Closed(a,e) /\ Closed(b,e) /\ Supports(a,e)#Supports(b,e)}
FirstEpoch(a,b) == CHOOSE e\in DifferentEpochs(a,b): \A f\in DifferentEpochs(a,b):e<=f
Schedule(c,e) == [s\in (e*SlotsPerEpoch)..((e+1)*SlotsPerEpoch-1) |->
 LET r==Registry(c,e) j==(s+bitcoin[e]+Root(r)+1)%Weight(r)
 IN IF j<r[1] THEN 1 ELSE IF j<r[1]+r[2] THEN 2 ELSE 3]
FirstBlockCommon == \A a,b\in {chains[i]:i\in Branches}:
 Forked(a,b) => LET s==FirstSlot(a,b) IN
 /\ ForkRegistry(a,s)=ForkRegistry(b,s)
 /\ Seed(ForkRegistry(a,s),Epoch(s))=Seed(ForkRegistry(b,s),Epoch(s))
CommonInterval == \A a,b\in {chains[i]:i\in Branches}:
 (Forked(a,b) /\ DifferentEpochs(a,b)#{}) =>
 LET e==FirstEpoch(a,b) s==FirstSlot(a,b) IN
 \A j\in Epoch(s)..(e-1): (Closed(a,j) /\ Closed(b,j)) =>
 /\ Registry(a,j)=Registry(b,j)
 /\ Seed(Registry(a,j),j)=Seed(Registry(b,j),j)
 /\ Schedule(a,j)=Schedule(b,j)
\* Structural classification, NOT a claim that a raw fork violates CP.
Class(a,b) == IF DifferentEpochs(a,b)={} THEN "none" ELSE
 LET e==FirstEpoch(a,b) IN
 IF RawSupport(a,e)#RawSupport(b,e) THEN "i_raw"
 ELSE IF (WindowCount(a,e)>=MaxReorg)#(WindowCount(b,e)>=MaxReorg)
 THEN "ii_pivot" ELSE "other"
NoOtherStructural == \A a,b\in {chains[i]:i\in Branches}: Class(a,b)#"other"
NoWitnessRaw == \A a,b\in {chains[i]:i\in Branches}: Class(a,b)#"i_raw"
NoWitnessPivot == \A a,b\in {chains[i]:i\in Branches}: Class(a,b)#"ii_pivot"

====
