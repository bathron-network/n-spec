---------------- MODULE MC_replay_h1 ----------------
EXTENDS NModel
VARIABLE step
ReplayNext == /\ step < 10
              /\ CASE step = 0 -> Reveal
                  [] step = 1 -> Return
                  [] step = 2 -> Produce(2)
                  [] step = 3 -> Fetch(1)
                  [] step = 4 -> Evidence("LAG")
                  [] step = 5 -> Tick
                  [] step = 6 -> Produce(1)
                  [] step = 7 -> Tick
                  [] step = 8 -> Produce(1)
                  [] step = 9 -> Fetch(1)
                  [] OTHER -> FALSE
              /\ step' = step+1
Replay == Init /\ bitcoin = (0 :> 0 @@ 1 :> 1 @@ 2 :> 1)
          /\ step = 0 /\ [][ReplayNext]_<<vars,step>>
============================================================
