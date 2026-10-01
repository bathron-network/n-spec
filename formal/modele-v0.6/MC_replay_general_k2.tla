---- MODULE MC_replay_general_k2 ----
EXTENDS RegistryModelFast2
VARIABLE step
ReplayNext== /\ step<13
 /\ (CASE step=0 -> Produce(2)
 [] step=1 -> Tick
 [] step=2 -> Tick
 [] step=3 -> Tick
 [] step=4 -> Reveal
 [] step=5 -> Produce(2)
 [] step=6 -> Tick
 [] step=7 -> Heal
 [] step=8 -> Return
 [] step=9 -> Fetch(2)
 [] step=10 -> Produce(1)
 [] step=11 -> Produce(2)
 [] step=12 -> Fetch(1))
 /\ step'=step+1
Replay==Init /\ bitcoin=(0:>0 @@ 1:>1 @@ 2:>1) /\ step=0 /\ [][ReplayNext]_<<vars,step>>
====
