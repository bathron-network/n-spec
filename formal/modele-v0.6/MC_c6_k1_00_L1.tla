---- MODULE MC_c6_k1_00_L1 ----
EXTENDS RegistryModelFast2_L1
ShardSpec==Init /\ bitcoin=(0:>0 @@ 1:>0 @@ 2:>0) /\ [][Next]_vars
====
