---- MODULE Authorities ----
EXTENDS Integers, FiniteSets, TLC, Sequences
VARIABLES origin,anchor,channels,valid,request,approval,used,nonce,contextLost,audit
vars== <<origin,anchor,channels,valid,request,approval,used,nonce,contextLost,audit>>
Init== /\ origin\in {"none","old"} /\ anchor=origin /\ channels\in {<<>>,<<"A">>,<<"A","A">>,<<"A","B">>}
 /\ valid\in BOOLEAN /\ request= <<>> /\ approval= <<>> /\ used={} /\ nonce=0
 /\ contextLost\in BOOLEAN /\ audit=TRUE
Bootstrap==
 /\ LET ok==origin="none" /\ Len(channels)>=2 /\ channels[1]=channels[2] /\ valid
    IN /\ origin'=IF ok THEN "new" ELSE origin
       /\ anchor'=IF ok THEN "new" ELSE anchor
       /\ audit'=audit /\ (origin="none" \/ (origin'=origin /\ anchor'=anchor))
 /\ UNCHANGED <<channels,valid,request,approval,used,nonce,contextLost>>
Prepare== /\ nonce<2 /\ nonce'=nonce+1 /\ request'= <<nonce+1,origin,anchor,contextLost,"target">>
 /\ UNCHANGED <<origin,anchor,channels,valid,approval,used,contextLost,audit>>
ExplicitApprove== /\ request# <<>> /\ approval'=request
 /\ UNCHANGED <<origin,anchor,channels,valid,request,used,nonce,contextLost,audit>>
Recover== /\ request# <<>> /\ approval=request /\ approval\notin used /\ valid
 /\ request= <<nonce,origin,anchor,contextLost,"target">>
 /\ origin'="target" /\ anchor'="target" /\ contextLost'=FALSE /\ used'=used\cup{approval}
 /\ audit'=audit /\ approval=request /\ approval\notin used
 /\ UNCHANGED <<channels,valid,request,approval,nonce>>
Next==Bootstrap \/ Prepare \/ ExplicitApprove \/ Recover
Spec==Init /\ [][Next]_vars
AuthoritiesSafe==audit /\ (origin="target" => valid /\ used#{})
NoWitnessRecovery==~(origin="target")
====
