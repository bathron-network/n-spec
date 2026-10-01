---- MODULE MC_fast_on_11 ----
EXTENDS RegistryModelFast2
ShardInit == Init /\ bitcoin = (0 :> 0 @@ 1 :> 1 @@ 2 :> 1)
ShardSpec == ShardInit /\ [][Next]_vars
====
