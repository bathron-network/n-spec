---- MODULE MC_fast_on_00_L1 ----
EXTENDS RegistryModelFast2_L1
ShardInit == Init /\ bitcoin = (0 :> 0 @@ 1 :> 0 @@ 2 :> 0)
ShardSpec == ShardInit /\ [][Next]_vars
====
