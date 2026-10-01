---- MODULE MC_private_return_L1 ----
EXTENDS RegistryAudit_L1
VARIABLE step
ReplayNext == /\ step<16
 /\ (CASE step=0 -> Reveal
 [] step=1 -> Produce(1)
 [] step=2 -> Produce(2)
 [] step=3 -> Fetch(1)
 [] step=4 -> Tick
 [] step=5 -> Produce(1)
 [] step=6 -> Tick
 [] step=7 -> Produce(1)
 [] step=8 -> Tick
 [] step=9 -> Tick
 [] step=10 -> Return
 [] step=11 -> Fetch(2)
 [] step=12 -> Produce(1)
 [] step=13 -> Produce(2)
 [] step=14 -> Heal
 [] step=15 -> Fetch(2))
 /\ step'=step+1
Replay == Init /\ bitcoin=(0:>0 @@ 1:>0 @@ 2:>0)
 /\ journal={} /\ l1journal={} /\ step=0
 /\ [][ReplayNext /\ journal'=journal\cup ObservedEntries
                   /\ l1journal'=l1journal\cup ObservedL1]_<<vars,journal,l1journal,step>>
\* A witness to the missing implication, not a new definition of ordinary CP.
\* Both branches advance A (b=1); the private prefix is shorter at epoch start.
MissingBridge == /\ step>=14
 /\ Class(chains[1],chains[2])="i_raw"
 /\ WindowCount(chains[1],2)>=MaxReorg
 /\ WindowCount(chains[2],2)>=MaxReorg
 /\ Len(Before(chains[2],4))<Len(Before(chains[1],4))
 /\ (\E a,b\in l1journal: a.e=2 /\ b.e=2 /\ a.D#b.D
                         /\ a.kind="signature" /\ b.kind="signature")
 /\ \A a\in l1journal: a.e<2 => IsPrefix(a.chain,chains[1])
NoWitnessMissingBridge == ~MissingBridge
====
