---- MODULE MC_c6_k1_10 ----
EXTENDS RegistryModelFast2
ShardSpec==Init /\ bitcoin=(0:>0 @@ 1:>1 @@ 2:>0) /\ [][Next]_vars
====
