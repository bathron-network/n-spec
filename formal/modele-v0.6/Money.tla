---- MODULE Money ----
EXTENDS Integers, FiniteSets, TLC
CONSTANT Mutation
Empty==[alice|->0,bob|->0,fees|->0,imports|->{},spent|->{}]
Imported==[alice|->10,bob|->0,fees|->0,imports|->{"btc-outpoint"},spent|->{}]
Paid==[alice|->3,bob|->6,fees|->1,imports|->{"btc-outpoint"},spent|->{"alice-input"}]
Oracle(t)==IF t=0 THEN Empty ELSE IF t=1 THEN Imported ELSE Paid
Supply(x)==x.alice+x.bob+x.fees
Import(x)==IF "btc-outpoint"\in x.imports /\ Mutation#"duplicate" THEN x
 ELSE [x EXCEPT !.alice=@+10,!.imports=@\cup{"btc-outpoint"}]
Transfer(x)==IF "alice-input"\in x.spent THEN x ELSE
 [x EXCEPT !.alice=@-7,!.bob=@+6,!.fees=@+1,!.spent=@\cup{"alice-input"}]
VARIABLES tip,visible,work,target,phase,source,stop,audit,crashed,paths
vars== <<tip,visible,work,target,phase,source,stop,audit,crashed,paths>>
Init== /\ tip=0 /\ visible=Empty /\ work=Empty /\ target=0 /\ phase="idle"
 /\ source=TRUE /\ stop=FALSE /\ audit=TRUE /\ crashed={} /\ paths={0}
Begin(t)== /\ phase="idle" /\ ~stop /\ source
 /\ target'=t /\ work'=Empty /\ phase'="import"
 /\ UNCHANGED <<tip,visible,source,stop,audit,crashed,paths>>
Load== /\ phase="import" /\ work'=IF target=0 THEN work ELSE Import(work)
 /\ phase'="notify" /\ UNCHANGED <<tip,visible,target,source,stop,audit,crashed,paths>>
Notify== /\ phase="notify" /\ work'=IF target=0 THEN work ELSE Import(work)
 /\ phase'="spend" /\ UNCHANGED <<tip,visible,target,source,stop,audit,crashed,paths>>
Spend== /\ phase="spend" /\ work'=IF target=2 THEN Transfer(Transfer(work)) ELSE work
 /\ phase'="commit" /\ UNCHANGED <<tip,visible,target,source,stop,audit,crashed,paths>>
Commit== /\ phase="commit" /\ source
 /\ visible'=work /\ tip'=target /\ phase'="idle" /\ paths'=paths\cup{target}
 /\ audit'=audit /\ work=Oracle(target)
 /\ UNCHANGED <<work,target,source,stop,crashed>>
Crash== /\ phase#"idle" /\ phase\notin crashed /\ crashed'=crashed\cup{phase}
 /\ work'=Empty /\ phase'="idle" /\ UNCHANGED <<tip,visible,target,source,stop,audit,paths>>
Withdraw== /\ source /\ source'=FALSE /\ stop'=TRUE
 /\ UNCHANGED <<tip,visible,work,target,phase,audit,crashed,paths>>
Undo== /\ ~source /\ stop /\ tip'=0 /\ visible'=Empty /\ phase'="idle"
 /\ UNCHANGED <<work,target,source,stop,audit,crashed,paths>>
Next== (\E t\in 0..2:Begin(t)) \/ Load \/ Notify \/ Spend \/ Commit \/ Crash \/ Withdraw \/ Undo
Spec==Init /\ [][Next]_vars
MON1==Supply(visible)<=10
MON2==visible.imports\subseteq{"btc-outpoint"} /\ visible.spent\subseteq{"alice-input"} /\ Supply(visible)=10*Cardinality(visible.imports)
MON3==visible=Oracle(tip)
MON4==audit
MON5==~source => stop \/ Supply(visible)=0
NoWitnessMoney==~(paths={0,1,2} /\ Cardinality(crashed)=4 /\ ~source /\ tip=0)
====
