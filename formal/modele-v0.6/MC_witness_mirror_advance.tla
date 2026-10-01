---- MODULE MC_witness_mirror_advance ----
EXTENDS RegistryModelV6
NoWitnessMirror == ~(\E b\in Branches,e\in Es: Support(chains[b],e)# <<>>)
====
