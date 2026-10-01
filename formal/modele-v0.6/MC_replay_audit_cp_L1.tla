---- MODULE MC_replay_audit_cp_L1 ----
EXTENDS RegistryAudit_L1
VARIABLE step
ReplayNext== /\ step<12
 /\ (CASE step=0 -> Produce(2)
 [] step=1 -> Tick
 [] step=2 -> Tick
 [] step=3 -> Tick
 [] step=4 -> Tick
 [] step=5 -> Heal
 [] step=6 -> Return
 [] step=7 -> Fetch(2)
 [] step=8 -> Reveal
 [] step=9 -> Produce(1)
 [] step=10 -> Produce(2)
 [] step=11 -> Fetch(1))
 /\ step'=step+1
Replay==Init /\ journal={} /\ l1journal={} /\ bitcoin=(0:>0 @@ 1:>0 @@ 2:>1) /\ step=0 /\ [][ReplayNext /\ journal'=journal\cup ObservedEntries /\ l1journal'=l1journal\cup ObservedL1]_<<vars,journal,l1journal,step>>
====
