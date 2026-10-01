---------------- MODULE MC_replay_spec_adopt_on ----------------
EXTENDS RegistryModel
VARIABLE step
ReplayNext == /\ step < 12
              /\ CASE step = 0 -> Reveal
                  [] step = 1 -> Produce(1)
                  [] step = 2 -> Tick
                  [] step = 3 -> Tick
                  [] step = 4 -> Tick
                  [] step = 5 -> Produce(1)
                  [] step = 6 -> Tick
                  [] step = 7 -> Produce(2)
                  [] step = 8 -> Return
                  [] step = 9 -> Fetch(2)
                  [] step = 10 -> Heal
                  [] step = 11 -> Fetch(2)
                  [] OTHER -> FALSE
              /\ step' = step+1
Replay == Init /\ bitcoin = (0 :> 0 @@ 1 :> 1 @@ 2 :> 1)
          /\ step = 0 /\ [][ReplayNext]_<<vars,step>>
============================================================
