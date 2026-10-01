---------------- MODULE Brake ----------------
EXTENDS Integers, Sequences, FiniteSets, TLC
CONSTANTS W, Scenario, Mutation, Horizon
I == 1..5
L == 5
Min(a,b) == IF a<b THEN a ELSE b
Max(a,b) == IF a>b THEN a ELSE b
RECURSIVE Sum(_)
Sum(q) == IF Len(q)=0 THEN 0 ELSE Head(q)+Sum(Tail(q))
Weights == IF W=1000 THEN <<680,120,190,5,5>>
           ELSE IF W=100 THEN <<68,12,18,1,1>> ELSE <<6,1,1,1,1>>
Assigned(i,s) == (s%5)+1=i
Canonical(i,s) == i=1 /\ (Scenario="068" \/ (s\div 5)%3<2)
Header(i,s) == Canonical(i,s) \/ (Scenario="slow" /\ i=5 /\ s=44)
Samples(i,a,b,cal) == {s\in a..b: Assigned(i,s) /\ s\in cal}
Present(i,a,b,cal) == LET m==Cardinality(Samples(i,a,b,cal))
 c==Cardinality({s\in Samples(i,a,b,cal): Canonical(i,s)})
 IN 2*c>=m /\ 3*c>=m
Initial == [i\in I |-> [state|->"ACTIVE",reset|->0,susp|->-1,queue|->-1]]
Observe(st,s,cal) == [i\in I |->
 LET x==st[i]
     a==Cardinality(Samples(i,x.susp+1,s,cal))
     q==Cardinality(Samples(i,Max(x.queue+1,s-2*L+1),s,cal))
 IN IF x.state="SUSPECT" /\ (s-x.susp>=2*L /\ a>=2)
       THEN IF Present(i,x.susp+1,s,cal)
            THEN [x EXCEPT !.state="ACTIVE",!.reset=s,!.susp=-1]
            ELSE [x EXCEPT !.state="QUEUED",!.queue=s]
    ELSE IF x.state="QUEUED" /\ s-2*L+1>x.queue /\ q>=2 /\ Present(i,s-2*L+1,s,cal)
       THEN [x EXCEPT !.state="ACTIVE",!.reset=s,!.susp=-1,!.queue=-1]
    ELSE IF x.state="ACTIVE" /\ s-7*L+1>x.reset /\
            Cardinality(Samples(i,s-7*L+1,s,cal))>=4 /\ ~Present(i,s-7*L+1,s,cal)
       THEN [x EXCEPT !.state="SUSPECT",!.susp=s]
    ELSE x]
RECURSIVE Replay(_,_,_,_)
Replay(st,a,b,cal) == IF a>b THEN st ELSE Replay(Observe(st,a,cal),a+1,b,cal)
VARIABLES epoch, cursor, control, wf, used, slow, rotation, audit, everSlow, released, calendar
vars == <<epoch,cursor,control,wf,used,slow,rotation,audit,everSlow,released,calendar>>
Active(st) == {i\in I: st[i].state#"EXCLUDED"}
Weight(st) == Sum([i\in 1..5 |-> IF i\in Active(st) THEN Weights[i] ELSE 0])
Health(st,c,cal) == LET Q=={i\in I: st[i].state="QUEUED"}
 end==((c+1)\div L)-1
 IN end>=2 /\ \A j\in (end-2)..end:
   LET eligible=={s\in (j*L)..((j+1)*L-1): (s%5)+1\notin Q /\ s\in cal}
       filled=={s\in eligible: Canonical((s%5)+1,s)}
   IN Cardinality(eligible)>0 /\ 10*Cardinality(filled)>=7*Cardinality(eligible)
Eligible(st,i,c,cal) == st[i].state="QUEUED" /\ c-7*L+1>st[i].reset /\
 Cardinality(Samples(i,c-7*L+1,c,cal))>=4 /\ ~\E s\in Samples(i,c-7*L+1,c,cal): Header(i,s)
RECURSIVE Order(_,_)
Order(st,ids) == IF ids={} THEN <<>> ELSE
 LET i==CHOOSE k\in ids: \A j\in ids: k=j \/
              st[k].queue<st[j].queue \/ (st[k].queue=st[j].queue /\ k<j)
 IN <<i>>\o Order(st,ids\{i})
RECURSIVE Select(_,_,_,_,_,_,_)
Select(st,q,b,w,c,h,cal) == IF Len(q)=0 THEN {} ELSE
 LET i==Head(q)
     take==(h \/ Eligible(st,i,c,cal)) /\ Weights[i]<=b /\ Weights[i]<w
 IN (IF take THEN {i} ELSE {}) \cup
      Select(st,Tail(q),IF take THEN b-Weights[i] ELSE b,
                         IF take THEN w-Weights[i] ELSE w,c,h,cal)
Init == /\ epoch=0 /\ cursor=0 /\ control=Initial
 /\ wf= <<W>> /\ used= <<0>> /\ slow= <<0>> /\ rotation=0
 /\ audit=TRUE /\ everSlow=FALSE /\ released=FALSE /\ calendar={0}
Advance == /\ epoch<Horizon
 /\ LET e==epoch+1
        unchanged==Scenario="inherited" /\ e\in {2,3,4}
        c==IF unchanged THEN cursor ELSE e*L-1
        cal==calendar\cup{s\in (cursor+1)..c: (s%5)+1\in Active(control)}
        st==Replay(control,cursor+1,c,cal)
        w==Weight(st)
        fs==Append(wf,w)
        base==CHOOSE z\in {fs[j+1]:j\in Max(0,e-6)..e}:
                     \A j\in Max(0,e-6)..e: z<=fs[j+1]
        u==Sum(SubSeq(used,Max(0,e-6)+1,e))
        su==Sum(SubSeq(slow,Max(0,e-6)+1,e))
        b==Min((2*w)\div 100,Max(0,(5*base)\div 100-u))
        h==Health(st,c,cal)
        cap==IF unchanged THEN 0 ELSE IF h THEN b ELSE Min(b,Max(0,base\div 100-su))
        budget==IF Mutation="zero_brake" /\ ~h THEN 0 ELSE cap
        chosen==Select(st,Order(st,{i\in I: st[i].state="QUEUED"}),budget,w,c,h,cal)
        k==Sum([i\in I |-> IF i\in chosen THEN Weights[i] ELSE 0])
        expected==Select(st,Order(st,{i\in I: st[i].state="QUEUED"}),cap,w,c,h,cal)
    IN /\ calendar'=cal /\ epoch'=e /\ cursor'=c /\ wf'=fs /\ used'=Append(used,k)
       /\ slow'=Append(slow,IF h THEN 0 ELSE k)
       /\ control'=[i\in I |-> IF i\in chosen THEN [st[i] EXCEPT !.state="EXCLUDED"] ELSE st[i]]
       /\ rotation'=IF ~unchanged /\ e=10 THEN rotation+1 ELSE rotation
       /\ everSlow'=everSlow \/ (~h /\ k>0)
       /\ released'=released \/ (everSlow /\ ~h /\ k>0 /\ e>=16)
       /\ audit'=audit /\ chosen=expected /\ k<=cap /\ k<w /\
              (unchanged=>k=0) /\ (h \/ \A i\in chosen: Eligible(st,i,c,cal))
Next == Advance
Spec == Init /\ [][Next]_vars
Mechanical == audit
RotationUnderBrake == epoch>=10 => rotation=1
NoWitnessSlow == ~everSlow
NoWitnessRelease == ~released
NoWitness068 == ~(Scenario="068" /\ epoch>=10 /\ Health(control,cursor,calendar))
IntentionalRounding == W<100 => used=[j\in 1..Len(used)|->0]
SlowProgress == (epoch=Horizon /\ Scenario="slow" /\ W=1000) => everSlow /\ released
FairSpec == Spec /\ WF_vars(Advance)
EventuallySlow == <>(everSlow)
====
