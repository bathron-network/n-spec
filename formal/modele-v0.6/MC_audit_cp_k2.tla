---- MODULE MC_audit_cp_k2 ----
EXTENDS RegistryAudit
CPScenario == Init /\ bitcoin=(0:>0 @@ 1:>1 @@ 2:>1) /\ journal={} /\ [][AuditNext]_<<vars,journal>>
====
