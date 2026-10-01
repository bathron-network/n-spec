---------------- MODULE MC_spec_registryreorg_b11_w8_v06 ----------------
EXTENDS NModel_v06
ShardInit == Init /\ bitcoin = (0 :> 0 @@ 1 :> 1 @@ 2 :> 1)
ShardSpec == ShardInit /\ [][Next]_vars
====================================================================
