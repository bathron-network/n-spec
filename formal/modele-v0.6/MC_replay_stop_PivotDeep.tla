---- MODULE MC_replay_stop_PivotDeep ----
EXTENDS Replay_PivotDeep
\* Contrast: same shape, no common window block (fork at length 3), X has 5
\* honest post-fork blocks (4,5,7,13,14; closes at 14, count 5). Y: 6, 9,
\* early carrier 12 (count 3 < 4), 15, 18, 21. Y longer, but node 1 would
\* disconnect 5 > MaxReorg = 4: STOP_DEEP, not an adoption.
Path == << <<"hp",1,1>>, <<"fetch",2>>, <<"tick">>, <<"hp",2,1>>, <<"fetch",1>>,
           <<"fork",3>>, <<"tick">>, <<"tick">>, <<"hp",1,1>>, <<"fetch",2>>,
           <<"tick">>, <<"hp",2,1>>, <<"fetch",1>>, <<"tick">>, <<"ap",2,6,FALSE>>,
           <<"tick">>, <<"hp",1,1>>, <<"fetch",2>>, <<"tick">>, <<"tick">>,
           <<"ap",2,9,FALSE>> >> \o Ticks(4) \o
        << <<"hp",1,1>>, <<"fetch",2>>, <<"tick">>, <<"hp",2,1>>, <<"fetch",1>>,
           <<"ap",2,12,TRUE>>, <<"tick">>, <<"ap",2,15,TRUE>> >> \o Ticks(3) \o
        << <<"ap",2,18,TRUE>> >> \o Ticks(3) \o
        << <<"ap",2,21,TRUE>>, <<"rev",1>>, <<"fetch",1>> >>
ReplayNext == ReplayNextP(Path)
Replay == Init /\ step = 0 /\ [][ReplayNext]_<<vars,step>>
PathNotStuck == step < Len(Path) => ENABLED ReplayNext
====
