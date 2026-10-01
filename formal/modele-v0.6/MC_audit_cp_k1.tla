---- MODULE MC_audit_cp_k1 ----
EXTENDS RegistryAudit
CPScenario == Init /\ bitcoin=(0:>0 @@ 1:>0 @@ 2:>1) /\ journal={} /\ [][AuditNext]_<<vars,journal>>
====
