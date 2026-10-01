---- MODULE MC_brake_live_mechanical ----
EXTENDS BrakeChecked
\* On Spec, the only nonstuttering action is Advance; it increments epoch.
\* Its only enabling guard is epoch<Horizon; its functional successor exists.
\* Thus this fairness predicate has the same enabling/truth values as Advance,
\* without recomputing the entire deterministic control transition for ENABLED.
ProgressStep == epoch<Horizon /\ epoch'=epoch+1
FairMechanical == Spec /\ WF_epoch(ProgressStep)
====
