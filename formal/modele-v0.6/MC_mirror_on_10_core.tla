---- MODULE MC_mirror_on_10_core ----
EXTENDS RegistryModelV6
ShardInit == Init /\ bitcoin = (0 :> 0 @@ 1 :> 1 @@ 2 :> 0)
ShardSpec == ShardInit /\ [][Next]_vars
====
