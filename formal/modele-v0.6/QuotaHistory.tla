---- MODULE QuotaHistory ----
EXTENDS Integers, Sequences, TLC
VARIABLES epoch,wf,excluded,capAtDecision,ban
vars==<<epoch,wf,excluded,capAtDecision,ban>>
Min(a,b)==IF a<b THEN a ELSE b
Max(a,b)==IF a>b THEN a ELSE b
RECURSIVE Sum(_)
Sum(q)==IF Len(q)=0 THEN 0 ELSE Head(q)+Sum(Tail(q))
Init== /\ epoch=0 /\ wf= <<1000>> /\ excluded= <<0>> /\ capAtDecision= <<0>>
 /\ ban\in {0,490,900}
Advance== /\ epoch<9
 /\ LET e==epoch+1
        w==IF e=1 THEN 1000 ELSE 990-ban
        fs==Append(wf,w)
        base==CHOOSE x\in {fs[j+1]:j\in Max(0,e-6)..e}:\A j\in Max(0,e-6)..e:x<=fs[j+1]
        used==Sum(SubSeq(excluded,Max(0,e-6)+1,e))
        cap==Min((2*w)\div 100,Max(0,(5*base)\div 100-used))
    IN /\ epoch'=e /\ wf'=fs /\ capAtDecision'=Append(capAtDecision,cap)
       /\ excluded'=Append(excluded,IF e=1 THEN 10 ELSE 0)
 /\ UNCHANGED ban
Next==Advance
Spec==Init /\ [][Next]_vars
Prospective==\A j\in 1..Len(excluded):excluded[j]<=capAtDecision[j]
BanBlocksNext==epoch>=2 /\ ban=900 => capAtDecision[3]=0
NoWitnessProspective==~(epoch=2 /\ ban=900 /\ excluded[2]=10 /\ capAtDecision[3]=0)
====
