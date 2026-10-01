---- MODULE MC_replay_anchor_split_checked ----
EXTENDS AnchorBTCChecked
VARIABLE step
ReplayNext== /\ step<2
 /\ CASE step=0 -> Select(1)
      [] step=1 -> Select(2)
 /\ step'=step+1
Replay==Init /\ rank= <<3,2>> /\ step=0 /\ [][ReplayNext]_<<vars,step>>
====
