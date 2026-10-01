---- MODULE MC_replay_sync_PivotDeep ----
EXTENDS Replay_PivotDeep
\* Variant SYNC before start(E): node 1, synchronized on X (installed raw at
\* 14), sees Y at 15 (equal length, toy tie favours Y: first post-fork slot
\* 12 < 13) and adopts it with 2 disconnections <= MaxReorg = 4.
Path == Common5 \o Race15 \o << <<"rev",1>>, <<"fetch",1>> >>
ReplayNext == ReplayNextP(Path)
Replay == Init /\ step = 0 /\ [][ReplayNext]_<<vars,step>>
PathNotStuck == step < Len(Path) => ENABLED ReplayNext
====
