---- MODULE H1Scan ----
EXTENDS Integers, FiniteSets, TLC
CONSTANT Scenario
VARIABLES scan,objects,btcHeight,cache,rank
vars== <<scan,objects,btcHeight,cache,rank>>
Refs=={"C0","C5","W5","foreign-x"}
Blocks=={"C0","C5","W5"}
Exclusions=={"xC","xW"}
G==2
Depth==1
Proofs==IF Scenario="stale" THEN
 {[branch|->"C",height|->1,slot|->0],[branch|->"C",height|->2,slot|->0],
  [branch|->"C",height|->3,slot|->0],[branch|->"W",height|->1,slot|->5]}
 ELSE {[branch|->"W",height|->1,slot|->5],[branch|->"C",height|->3,slot|->5]}
Progress(c,h)==LET v=={p.slot:p\in {p\in Proofs:p.branch=c /\ p.height<=h}}
 IN IF v={} THEN -1 ELSE CHOOSE s\in v: \A t\in v:s>=t
Steps(w)=={p.height:p\in {p\in Proofs:p.branch=w /\ p.slot>Progress(w,p.height-1)}}
Relevant(x)==x\in Blocks\cup Exclusions
Needed==IF Scenario="foreign" THEN {} ELSE {"xC","xW"}
Complete==scan=1..3 /\ Needed\subseteq objects
RawLag(c,w)==IF btcHeight<1+G+Depth THEN "FALSE"
 ELSE IF ~Complete THEN "UNKNOWN"
 ELSE IF \E b\in Steps(w):b+G+Depth<=btcHeight /\ Progress(w,b)>Progress(c,b+G) THEN "TRUE"
 ELSE "FALSE"
Init== /\ scan={} /\ objects={} /\ btcHeight=2 /\ cache=FALSE /\ rank="C"
Scan(h)== /\ h\in 1..3 /\ scan'=scan\cup{h}
 /\ UNCHANGED <<objects,btcHeight,cache,rank>>
Resolve(x)== /\ x\in {"xC","xW","foreign-x"} /\ objects'=objects\cup{x}
 /\ UNCHANGED <<scan,btcHeight,cache,rank>>
Bitcoin(h)== /\ h\in {2,4,5} /\ btcHeight'=h
 /\ UNCHANGED <<scan,objects,cache,rank>>
Evict== /\ cache'=~cache /\ UNCHANGED <<scan,objects,btcHeight,rank>>
RankChange== /\ rank'=IF rank="C" THEN "W" ELSE "C"
 /\ UNCHANGED <<scan,objects,btcHeight,cache>>
Next==(\E h\in 1..3:Scan(h)) \/ (\E x\in {"xC","xW","foreign-x"}:Resolve(x)) \/
 (\E h\in {2,4,5}:Bitcoin(h)) \/ Evict \/ RankChange
Spec==Init /\ [][Next]_vars
TrueComplete==RawLag("C","W")="TRUE" => Complete /\ btcHeight>=4
ForeignIrrelevant==~Relevant("foreign-x") /\
 (Scenario="foreign" /\ scan=1..3 => RawLag("C","W")#"UNKNOWN")
ResolvedDecidable==Complete => RawLag("C","W")#"UNKNOWN"
NoStaleVeto==Scenario="stale" => RawLag("C","W")#"TRUE"
NoWitnessUnknown==~(btcHeight>=4 /\ RawLag("C","W")="UNKNOWN")
NoWitnessDecidable==~(Complete /\ btcHeight>=4 /\ RawLag("C","W")="FALSE")
====
