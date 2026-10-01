---------------- MODULE MC_spec_registryreorg_b01_v06 ----------------
EXTENDS NModel_v06
ShardInit == Init /\ bitcoin = (0 :> 0 @@ 1 :> 0 @@ 2 :> 1)
ShardSpec == ShardInit /\ [][Next]_vars
====================================================================
