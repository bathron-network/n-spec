---- MODULE MC_mirror_on_10 ----
EXTENDS RegistryModel
ShardInit == Init /\ bitcoin = (0 :> 0 @@ 1 :> 1 @@ 2 :> 0)
ShardSpec == ShardInit /\ [][Next]_vars
====
