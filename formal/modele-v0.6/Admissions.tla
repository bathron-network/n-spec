---- MODULE Admissions ----
EXTENDS Integers, FiniteSets, TLC
CONSTANT Mutation
States=={"ACTIVE","SUSPECT","QUEUED","EXCLUDED","BANNED"}
VARIABLES before,after,phase,ban,exclude,depth,reserved,consumed,priceOK,reference,react,audit
vars== <<before,after,phase,ban,exclude,depth,reserved,consumed,priceOK,reference,react,audit>>
Init== /\ before\in [state:States,reset:{2},queue:{3},active:{4},dormant:{0}]
 /\ after=before /\ phase=0 /\ ban\in BOOLEAN /\ exclude\in BOOLEAN
 /\ depth\in {59,60,61} /\ reserved\in BOOLEAN /\ consumed\in BOOLEAN
 /\ priceOK\in BOOLEAN /\ reference\in {"exact_dossier_x","foreign"}
 /\ react=FALSE /\ audit=TRUE
Add== /\ phase=0 /\ phase'=1
 /\ LET state==IF ban THEN "BANNED" ELSE IF exclude /\ before.state="QUEUED" THEN "EXCLUDED" ELSE before.state
        reset==IF Mutation="add_reset" THEN 0 ELSE before.reset
    IN /\ after'=[before EXCEPT !.state=state,!.reset=reset,
           !.active=IF state\in{"ACTIVE","SUSPECT","QUEUED"} THEN @+1 ELSE IF state="BANNED" THEN 0 ELSE @,
           !.dormant=IF state="EXCLUDED" THEN @+1 ELSE @]
       /\ audit'=audit /\ reset=before.reset
 /\ UNCHANGED <<before,ban,exclude,depth,reserved,consumed,priceOK,reference,react>>
ReactExam== /\ phase=1 /\ phase'=2
 /\ react'=(after.state="EXCLUDED" /\ ~ban /\ depth>=60 /\ ~reserved /\ ~consumed /\ priceOK /\ reference="exact_dossier_x")
 /\ UNCHANGED <<before,after,ban,exclude,depth,reserved,consumed,priceOK,reference,audit>>
Rollback== /\ phase=2 /\ phase'=3 /\ react'=FALSE
 /\ UNCHANGED <<before,after,ban,exclude,depth,reserved,consumed,priceOK,reference,audit>>
Next==Add \/ ReactExam \/ Rollback
Spec==Init /\ [][Next]_vars
AddNoReset==audit /\ after.queue=before.queue
ReactReference==react => reference="exact_dossier_x" /\ depth>=60 /\ ~reserved /\ ~consumed /\ priceOK /\ after.state="EXCLUDED"
NoWitnessReact==~react
====
