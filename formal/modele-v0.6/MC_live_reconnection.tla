---- MODULE MC_live_reconnection ----
EXTENDS H1OrdersChecked
VARIABLES partition,absent
allvars==<<vars,partition,absent>>
Start==Init /\ partition=TRUE /\ absent=TRUE
Heal== /\ partition /\ partition'=FALSE /\ UNCHANGED <<vars,absent>>
Return== /\ absent /\ absent'=FALSE /\ UNCHANGED <<vars,partition>>
Receive(n,items)== /\ (~absent \/ n=1)
 /\ (~partition \/ items\subseteq(IF n=1 THEN {"C","BTC"} ELSE {"W","BTC"}))
 /\ Deliver(n,items) /\ UNCHANGED <<partition,absent>>
Step==Heal \/ Return \/ (\E n\in Nodes,items\in SUBSET Events:Receive(n,items))
Live==Start /\ [][Step]_allvars /\ WF_allvars(Heal) /\ WF_allvars(Return)
 /\ \A n\in Nodes:WF_allvars(Receive(n,Events\received[n]))
Resumed==<>[](\A n\in Nodes:received[n]=Events /\ auth[n]={"C"})
====
