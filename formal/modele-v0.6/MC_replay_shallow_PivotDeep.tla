---- MODULE MC_replay_shallow_PivotDeep ----
EXTENDS Replay_PivotDeep
\* Control: count-zone pivot (no early closure). Private lane gets a
\* Byzantine block at 12 without m_E, revealed to node 1 only; node 1 builds
\* 13 on it; node 2 closes X at 14 (count 3 < 4, inherits); node 1 closes Y
\* at 17 (count 5, raw) and signs. Pivot (ii) with both carriers honest.
Path == Common5 \o Ticks(7) \o
        << <<"ap",2,12,FALSE>>, <<"rev",1>>, <<"fetch",1>>, <<"tick">>,
           <<"hp",1,2>>, <<"tick">>, <<"hp",2,1>> >> \o Ticks(3) \o
        << <<"fetch",1>>, <<"hp",1,2>> >>
ReplayNext == ReplayNextP(Path)
Replay == Init /\ step = 0 /\ [][ReplayNext]_<<vars,step>>
PathNotStuck == step < Len(Path) => ENABLED ReplayNext
====
