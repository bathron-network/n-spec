---- MODULE MC_c6_k2_11 ----
EXTENDS RegistryModelFast2
ShardSpec==Init /\ bitcoin=(0:>0 @@ 1:>1 @@ 2:>1) /\ [][Next]_vars
====
