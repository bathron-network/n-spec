---------------- MODULE MC_replay_tip ----------------
EXTENDS NModel
VARIABLE step
ReplayNext == /\ step < 6
              /\ CASE step = 0 -> Produce(2)
                  [] step = 1 -> Tick
                  [] step = 2 -> Return
                  [] step = 3 -> Reveal
                  [] step = 4 -> Produce(1)
                  [] step = 5 -> Fetch(2)
                  [] OTHER -> FALSE
              /\ step' = step+1
Replay == Init /\ bitcoin = (0 :> 0 @@ 1 :> 0 @@ 2 :> 0)
          /\ step = 0 /\ [][ReplayNext]_<<vars,step>>
============================================================
