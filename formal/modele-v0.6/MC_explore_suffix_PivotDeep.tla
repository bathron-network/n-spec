---- MODULE MC_explore_suffix_PivotDeep ----
EXTENDS Replay_PivotDeep
\* Semi-directed bounded exploration: a fixed prefix of Spec steps (honest
\* raw block at 1, private lane rooted at length 2, honest window block at 4,
\* ticks to slot 7), then the FULL Next, exhaustively, up to EndSlot.
\* Every behaviour is a behaviour of Spec. A PASS would be exhaustive only
\* over continuations of this prefix.
Pre == << <<"hp",1,1>>, <<"fetch",2>>, <<"fork",2>>, <<"tick">>, <<"tick">>,
          <<"tick">>, <<"hp",1,1>>, <<"fetch",2>>, <<"tick">>, <<"tick">>,
          <<"tick">> >>
SNext == IF step < Len(Pre) THEN Do(Pre[step+1]) /\ step' = step + 1
         ELSE Next /\ UNCHANGED step
SSpec == Init /\ step = 0 /\ [][SNext]_<<vars,step>>
====
