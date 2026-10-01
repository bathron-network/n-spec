---- MODULE MC_mirror_on_01 ----
EXTENDS RegistryModel
ShardInit == Init /\ bitcoin = (0 :> 0 @@ 1 :> 0 @@ 2 :> 1)
ShardSpec == ShardInit /\ [][Next]_vars
====
