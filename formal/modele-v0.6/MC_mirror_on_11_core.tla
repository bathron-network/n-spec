---- MODULE MC_mirror_on_11_core ----
EXTENDS RegistryModelFast
ShardInit == Init /\ bitcoin = (0 :> 0 @@ 1 :> 1 @@ 2 :> 1)
ShardSpec == ShardInit /\ [][Next]_vars
====
