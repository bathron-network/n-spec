---------------- MODULE MC_replay_spec_strong_v06 ----------------
EXTENDS NModel_v06
VARIABLE step
ReplayNext == /\ step < 8
              /\ CASE step = 0 -> Reveal
                  [] step = 1 -> Produce(1)
                  [] step = 2 -> Tick
                  [] step = 3 -> Tick
                  [] step = 4 -> Tick
                  [] step = 5 -> Tick
                  [] step = 6 -> Produce(2)
                  [] step = 7 -> Fetch(1)
                  [] OTHER -> FALSE
              /\ step' = step+1
Replay == Init /\ bitcoin = (0 :> 0 @@ 1 :> 0 @@ 2 :> 1)
          /\ step = 0 /\ [][ReplayNext]_<<vars,step>>
============================================================
