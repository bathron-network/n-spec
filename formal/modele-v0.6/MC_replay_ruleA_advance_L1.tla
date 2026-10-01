---- MODULE MC_replay_ruleA_advance_L1 ----
EXTENDS RegistryModelFast2_L1
VARIABLE step
ReplayNext== /\ step<17
 /\ (CASE step=0 -> Reveal
 [] step=1 -> Return
 [] step=2 -> Heal
 [] step=3 -> Produce(1)
 [] step=4 -> Fetch(1)
 [] step=5 -> Fetch(2)
 [] step=6 -> Tick
 [] step=7 -> Produce(1)
 [] step=8 -> Fetch(2)
 [] step=9 -> Tick
 [] step=10 -> Produce(1)
 [] step=11 -> Fetch(2)
 [] step=12 -> Tick
 [] step=13 -> Produce(1)
 [] step=14 -> Fetch(1)
 [] step=15 -> Tick
 [] step=16 -> Produce(1))
 /\ step'=step+1
Replay==Init /\ bitcoin=(0:>0 @@ 1:>0 @@ 2:>0) /\ step=0 /\ [][ReplayNext]_<<vars,step>>
NoWitnessAdvance==~(\E b\in Branches:Support(chains[b],2)# <<>>)
====
