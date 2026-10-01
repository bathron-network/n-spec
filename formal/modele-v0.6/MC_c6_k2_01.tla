---- MODULE MC_c6_k2_01 ----
EXTENDS RegistryModelFast2
ShardSpec==Init /\ bitcoin=(0:>0 @@ 1:>0 @@ 2:>1) /\ [][Next]_vars
====
