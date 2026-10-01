---- MODULE RegistryCommitments ----
EXTENDS Integers, Sequences, FiniteSets, TLC
CONSTANT Mutation, MaxReorg
\* Validated pre-built histories, common raw prefix; carrier at 3 or 4.
\* IDs 0=common ADD, others distinguish branches; genesis is empty prefix.
Histories == {<<0,11,13>>,<<0,23>>,<<0,12,14>>,<<0,24>>,<<31,33>>}
Slot(b) == b%10
Raw(c) == SelectSeq(c,LAMBDA b:Slot(b)<1)
Carrier(c) == Len(c)
Count(c) == Cardinality({i\in 1..Carrier(c):Slot(c[i])>=1})
Support(c) == IF Count(c)>=MaxReorg THEN Raw(c) ELSE <<>>
D(c) == <<<<>>,<<>>,Support(c)>>
R(c) == <<2+Len(Support(c)),1,1>>
Control(c) == [ops|->{b:b\in {Support(c)[i]:i\in 1..Len(Support(c))}},weights|->R(c)]
Calendar(c) == [s\in 4..5 |-> (s+R(c)[1])%4]
Prefix(c,k) == SubSeq(c,1,k)
LCA(a,b) == CHOOSE k\in 0..Len(a): k<=Len(b) /\ Prefix(a,k)=Prefix(b,k) /\
 \A j\in (k+1)..Len(a):j>Len(b) \/ Prefix(a,j)#Prefix(b,j)
VARIABLES tip,journal,audit
vars== <<tip,journal,audit>>
Entry(c,n,k) == [X|-><<"rules",0,<<0,1,1>>>>,epoch|->2,D|->D(c),R|->R(c),
 control|->Control(c),calendar|->Calendar(c),node|->n,kind|->k,chain|->c]
Init == /\ tip=[n\in 1..2 |-> <<>>] /\ journal={} /\ audit=TRUE
Allowed(n,c) == Len(tip[n])-LCA(tip[n],c)<=MaxReorg
Commit(n,c,k) == /\ Cardinality({x\in journal:x.node=n})<2 /\ Allowed(n,c) /\ Entry(c,n,k)\notin journal
 /\ LET blocked==Mutation="journal_veto" /\ \E x\in journal:x.node=n /\ x.R#R(c)
    IN /\ tip'=IF blocked THEN tip ELSE [tip EXCEPT ![n]=c]
       /\ journal'=journal\cup{Entry(c,n,k)}
       /\ audit'=audit /\ ~blocked
Next == \E n\in 1..2,c\in Histories,k\in {"signature","adoption","installation"}:Commit(n,c,k)
Spec == Init /\ [][Next]_vars
C6 == \A a,b\in journal:
 (a.epoch=b.epoch /\ a.X=b.X /\ a.D=b.D) => a.R=b.R /\ a.control=b.control /\ a.calendar=b.calendar
CPreg == \A a,b\in journal:a.epoch=b.epoch /\ a.X=b.X => a.D=b.D
RegistryImmutable == \A a,b\in journal:a.epoch=b.epoch /\ a.X=b.X => a.R=b.R
NoJournalVeto == audit
====
