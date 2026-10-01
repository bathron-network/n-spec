---- MODULE MC_replay_closure_checked_fixed_L1 ----
EXTENDS RegistryCommitmentsChecked_L1
VARIABLE step
ReplayNext== /\ step<2
 /\ (CASE step=0 -> Commit(1,<<0,11,13>>,"signature")
      [] step=1 -> Commit(1,<<0,23>>,"adoption"))
 /\ step'=step+1
Replay==Init /\ step=0 /\ [][ReplayNext]_<<vars,step>>
====
