---- MODULE RegistryAudit ----
EXTENDS RegistryModelFast2
VARIABLE journal
CalendarFor(r,e)==[s\in (e*SlotsPerEpoch)..((e+1)*SlotsPerEpoch-1)|->
 LET j==(s+bitcoin[e]+Root(r)+1)%Weight(r)
 IN IF j<r[1] THEN 1 ELSE IF j<r[1]+r[2] THEN 2 ELSE 3]
IsSignature(n)==local'[n].signed>=0 /\ local'[n].signed#local[n].signed
IsInstall(n)== /\ local'[n].history.epoch=local'[n].epoch
 /\ (local'[n].tip#local[n].tip \/ local'[n].epoch#local[n].epoch \/ local'[n].registry#local[n].registry)
 /\ (local'[n].epoch=0 \/ Carrier(local'[n].tip,local'[n].epoch)>0)
ObservedEntries=={LET h==local'[n].history IN
 [node|->n,e|->h.epoch,slot|->slot',kind|->IF IsSignature(n) THEN "signature" ELSE IF local'[n].tip#local[n].tip THEN "adoption" ELSE "installation",
 X|-><<"v6",local'[n].origin,bitcoin'>>,D|->h.supports,R|->h.registry,
 control|->UNION {Ops(h.supports[j]):j\in 0..h.epoch},calendar|->CalendarFor(h.registry,h.epoch)]
 :n\in {k\in Nodes:local'[k].history.epoch>=0 /\ (IsSignature(k) \/ IsInstall(k))}}
AuditNext==Next /\ journal'=journal\cup ObservedEntries
AuditSpec==Init /\ journal={} /\ [][AuditNext]_<<vars,journal>>
CPregGlobal==\A a,b\in journal:(a.e=b.e /\ a.X=b.X)=>a.D=b.D
C6Global==\A a,b\in journal:(a.e=b.e /\ a.X=b.X /\ a.D=b.D)=>
 a.R=b.R /\ a.control=b.control /\ a.calendar=b.calendar
====
