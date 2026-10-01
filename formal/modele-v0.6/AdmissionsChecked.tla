---- MODULE AdmissionsChecked ----
EXTENDS Integers, FiniteSets, TLC
CONSTANT Mutation
States=={"ACTIVE","SUSPECT","QUEUED","EXCLUDED","BANNED"}
VARIABLES before,after,phase,ban,exclude,depth,reserved,consumed,priceOK,reference,react,audit,currentPrice,burnAmount
vars== <<before,after,phase,ban,exclude,depth,reserved,consumed,priceOK,reference,react,audit,currentPrice,burnAmount>>
Init== /\ \E st\in States: before=[state|->st,reset|->2,queue|->3,active|->IF st\in {"ACTIVE","SUSPECT","QUEUED"} THEN 4 ELSE 0,dormant|->IF st="EXCLUDED" THEN 4 ELSE 0]
 /\ after=before /\ phase=0 /\ ban\in BOOLEAN /\ exclude\in BOOLEAN
 /\ depth\in {59,60,61} /\ reserved\in BOOLEAN /\ consumed\in BOOLEAN
 /\ burnAmount\in {9,10} /\ currentPrice=10 /\ priceOK=(burnAmount>=10) /\ reference\in {"exact_dossier_x","foreign"}
 /\ react=FALSE /\ audit=TRUE
Add== /\ phase=0 /\ phase'=1
 /\ LET state==IF ban THEN "BANNED" ELSE IF exclude /\ before.state="QUEUED" THEN "EXCLUDED" ELSE before.state
        reset==IF Mutation="add_reset" THEN 0 ELSE before.reset
    IN /\ after'=[before EXCEPT !.state=state,!.reset=reset,
           !.active=IF state\in{"ACTIVE","SUSPECT","QUEUED"} THEN @+1 ELSE 0,
           !.dormant=IF state="EXCLUDED" THEN @+before.active+1 ELSE IF state="BANNED" THEN 0 ELSE @]
       /\ audit'=(audit /\ reset=before.reset)
 /\ UNCHANGED <<before,ban,exclude,depth,reserved,consumed,priceOK,reference,react,currentPrice,burnAmount>>
ReactExam== /\ phase=1 /\ phase'=2
 /\ react'=(after.state="EXCLUDED" /\ ~ban /\ depth>=60 /\ ~reserved /\ ~consumed /\ priceOK /\ reference="exact_dossier_x")
 /\ UNCHANGED <<before,after,ban,exclude,depth,reserved,consumed,priceOK,reference,audit,currentPrice,burnAmount>>
Rollback== /\ phase=2 /\ phase'=3 /\ react'=FALSE
 /\ UNCHANGED <<before,after,ban,exclude,depth,reserved,consumed,priceOK,reference,audit,currentPrice,burnAmount>>
Reprice== /\ phase=1 /\ currentPrice=10 /\ currentPrice'=20
 /\ UNCHANGED <<before,after,phase,ban,exclude,depth,reserved,consumed,priceOK,reference,react,audit,burnAmount>>
Reopen== /\ phase=3 /\ phase'=1
 /\ UNCHANGED <<before,after,ban,exclude,depth,reserved,consumed,priceOK,reference,react,audit,currentPrice,burnAmount>>
Next==Add \/ ReactExam \/ Rollback \/ Reprice \/ Reopen
Spec==Init /\ [][Next]_vars
AddNoReset==audit /\ after.queue=before.queue
ReactReference==react => reference="exact_dossier_x" /\ depth>=60 /\ ~reserved /\ ~consumed /\ priceOK /\ after.state="EXCLUDED"
AddedRights== /\ (after.state\in {"EXCLUDED","BANNED"} => after.active=0)
 /\ (phase>0 /\ after.state="EXCLUDED" => after.dormant=before.dormant+before.active+1)
HistoricalPrice==priceOK=(burnAmount>=10)
NoWitnessLatePrice==~(currentPrice=20 /\ react /\ burnAmount=10)
NoWitnessReact==~react
====
