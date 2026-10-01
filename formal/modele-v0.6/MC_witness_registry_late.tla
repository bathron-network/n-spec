---- MODULE MC_witness_registry_late ----
EXTENDS RegistryWindowChecked
NoWitnessLate == ~(Carrier(chain)>0 /\ chain[Carrier(chain)].slot=5 /\ signed)
====
