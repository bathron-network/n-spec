---- MODULE MC_replay_aftersig_PivotDeep ----
EXTENDS Replay_PivotDeep
\* Variant AFTER_SIG after start(E), no tie reliance: node 1 signs slot 17 on
\* X (calendar of R_pass); Y grows under its own calendar (R inherited):
\* adversary 18 and 21; node 2 (synchronized on X incl. 17) then sees Y
\* strictly longer (4 vs 3 post-fork blocks) and adopts with 3 disconnections.
Path == Common5 \o Race15 \o
        << <<"tick">>, <<"tick">>, <<"hp",1,1>>, <<"fetch",2>>, <<"tick">>,
           <<"ap",2,18,TRUE>>, <<"tick">>, <<"tick">>, <<"tick">>,
           <<"ap",2,21,TRUE>>, <<"rev",2>>, <<"fetch",2>> >>
ReplayNext == ReplayNextP(Path)
Replay == Init /\ step = 0 /\ [][ReplayNext]_<<vars,step>>
PathNotStuck == step < Len(Path) => ENABLED ReplayNext
====
