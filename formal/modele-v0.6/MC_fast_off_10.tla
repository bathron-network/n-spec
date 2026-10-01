---- MODULE MC_fast_off_10 ----
EXTENDS RegistryModelFast2
ShardInit == Init /\ bitcoin = (0 :> 0 @@ 1 :> 1 @@ 2 :> 0)
ShardSpec == ShardInit /\ [][Next]_vars
====
