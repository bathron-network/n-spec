---- MODULE Replay_PivotDeep ----
EXTENDS RegistryModel_PivotDeep
\* Directed replay driver: a hand-built path of actions of the model.
\* Each step must be ENABLED; PathNotStuck (plain invariant) fails otherwise.
VARIABLE step
Do(x) == CASE x[1] = "tick"  -> Tick
           [] x[1] = "hp"    -> HProduce(x[2],x[3])
           [] x[1] = "ap"    -> AProduce(x[2],x[3],x[4])
           [] x[1] = "fork"  -> Fork(x[2])
           [] x[1] = "rev"   -> Reveal(x[2])
           [] x[1] = "fetch" -> Fetch(x[2])
ReplayNextP(P) == /\ step < Len(P) /\ Do(P[step+1]) /\ step' = step + 1
ReplaySpecP(P) == Init /\ step = 0 /\ [][ReplayNextP(P)]_<<vars,step>>
PathNotStuckP(P) == step < Len(P) => ENABLED ReplayNextP(P)
Ticks(k) == [i \in 1..k |-> <<"tick">>]
\* Common public prefix: honest blocks at slots 1,2 (raw) and 4,5 (window,
\* c = 2 common window blocks), then the private lane is rooted at length 5.
Common5 == << <<"hp",1,1>>, <<"fetch",2>>, <<"tick">>, <<"hp",2,1>>, <<"fetch",1>>,
              <<"tick">>, <<"tick">>, <<"hp",1,1>>, <<"fetch",2>>, <<"tick">>,
              <<"hp",2,1>>, <<"fetch",1>>, <<"fork",5>> >>
\* From slot 5: honest skip 6..12 (availability); honest 13 (h1) and 14 (h2,
\* first honest block carrying m_E: X closes, count 4 >= 4, installs raw).
\* At slot 14 the adversary backdates slot 12 WITH m_E on the private lane
\* (Y closes early: count 3 < 4, inherits), then signs 15.
Race15 == Ticks(8) \o << <<"hp",1,1>>, <<"fetch",2>>, <<"tick">>, <<"hp",2,1>>,
              <<"fetch",1>>, <<"ap",2,12,TRUE>>, <<"tick">>, <<"ap",2,15,TRUE>> >>
====
