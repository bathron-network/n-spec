---- MODULE MC_fast_off_01 ----
EXTENDS RegistryModelFast2
ShardInit == Init /\ bitcoin = (0 :> 0 @@ 1 :> 0 @@ 2 :> 1)
ShardSpec == ShardInit /\ [][Next]_vars
====
