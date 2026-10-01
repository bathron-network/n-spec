---- MODULE MC_v6_mirror_on_01 ----
EXTENDS RegistryModelFast2
ShardInit == Init /\ bitcoin = (0 :> 0 @@ 1 :> 0 @@ 2 :> 1)
ShardSpec == ShardInit /\ [][Next]_vars
====
