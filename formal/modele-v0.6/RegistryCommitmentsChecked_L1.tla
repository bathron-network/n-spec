---- MODULE RegistryCommitmentsChecked_L1 ----
EXTENDS RegistryCommitmentsChecked

Class(a,b) == IF a.D=b.D THEN "none" ELSE
 IF Raw(a.chain)#Raw(b.chain) THEN "i_raw"
 ELSE IF (Count(a.chain)>=MaxReorg)#(Count(b.chain)>=MaxReorg) THEN "ii_pivot" ELSE "other"
NoOtherStructural == \A a,b\in journal: Class(a,b)#"other"
NoWitnessPivot == \A a,b\in journal: Class(a,b)#"ii_pivot"
NoWitnessTwoSignatures == ~\E a,b\in journal:
 a.D#b.D /\ a.kind="signature" /\ b.kind="signature"

====
