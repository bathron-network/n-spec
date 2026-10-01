---- MODULE RegistryAudit_L1 ----
EXTENDS RegistryAudit, RegistryModelFast2_L1

VARIABLE l1journal
ObservedL1 == {LET h==local'[n].history
 c==IF IsSignature(n) THEN CHOOSE c\in {chains'[b]:b\in Branches}:
 Len(c)>0 /\ Slot(c[Len(c)])=slot' /\ Owner(Prefix(c,Len(c)-1),h.epoch,slot')=n
 ELSE local'[n].tip
 IN [node|->n,e|->h.epoch,kind|->IF IsSignature(n) THEN "signature" ELSE "adoption_or_installation",
 D|->h.supports,R|->h.registry,chain|->c]
 : n\in {k\in Nodes:local'[k].history.epoch>=0 /\ (IsSignature(k) \/ IsInstall(k))}}
L1AuditNext == AuditNext /\ l1journal'=l1journal\cup ObservedL1
L1AuditSpec == Init /\ journal={} /\ l1journal={} /\ [][L1AuditNext]_<<vars,journal,l1journal>>
NoHonestOther == \A a,b\in l1journal: (a.e=b.e /\ a.D#b.D) => Class(a.chain,b.chain)#"other"
NoWitnessTwoSignatures == ~\E a,b\in l1journal:
 a.e=b.e /\ a.D#b.D /\ a.kind="signature" /\ b.kind="signature"

====
