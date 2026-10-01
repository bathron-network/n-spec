---- MODULE MC_replay_general_k1_L1 ----
EXTENDS RegistryModelFast2_L1
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
Replay==Init /\ bitcoin=(0:>0 @@ 1:>0 @@ 2:>1) /\ step=0 /\ [][ReplayNext]_<<vars,step>>
====
