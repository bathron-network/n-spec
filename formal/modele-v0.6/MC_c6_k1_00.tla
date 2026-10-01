---- MODULE MC_c6_k1_00 ----
EXTENDS RegistryModelFast2
ShardSpec==Init /\ bitcoin=(0:>0 @@ 1:>0 @@ 2:>0) /\ [][Next]_vars
====
