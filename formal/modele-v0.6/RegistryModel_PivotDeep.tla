---- MODULE RegistryModel_PivotDeep ----
EXTENDS Naturals, Integers, Sequences, FiniteSets, TLC

(***************************************************************************
 Focused N-SPEC v0.6 mirror for the "deep pivot" (LEMME-L1-opus 4.4).
 NEW module; no delivered file is changed. Derived from RegistryModelFast2
 (block encoding, lottery formula, rank = length then tie sequence, maxreorg
 test Len(tip)-LCA > MaxReorg, anchor at MaxReorg links) with ONE deliberate
 difference: seed maturity is an explicit per-block fact (5.2, 8.4) instead of
 being reduced to the epoch start. Fast2's reduction makes every carrier the
 first block >= start(e), which structurally excludes early closure.

 Target epoch E = 2 only (epochs 0 and 1 have Cut <= 0: support = genesis).
   window(C) = [Cut(E), slot(first carrier of m_E in C)], inclusive (5.2)
   A_E(C)    = raw(C) if window count >= registry_min_blocks, else A_1 = genesis
   registry_min_blocks = maxreorg = MaxReorg (profile 3.3: equality imposed)
 Maturity legality (8.4 + 5.4):
   * a block may carry m_E only if its slot >= MatMin (MTP margin bound:
     real value freeze + 6000 slots = cut + 13 200);
   * m_E exists in Bitcoin only from wall-clock slot BtcMat on; honest
     producers include it from BtcMat on (d_ref discipline); the adversary may
     sign a block for a PAST slot s' >= MatMin once slot >= BtcMat (backdating
     is not forbidden by historical validity, 8.4 bounds only the reference);
   * ref extends parent.ref: descendants of a carrier carry it;
   * every block of epoch E carries it (no block precedes its own carrier).
 Abstractions (NOT captured): toy periodic lottery instead of a random oracle,
 toy tie = (epoch, root, slot, producer) instead of a hash, no probability,
 no delay bound Delta (delivery is adversarial and selective), anchor uses
 Nbound only (Bbound <= Nbound would only LOWER the anchor), no H1/evidence,
 single target epoch, single ADD op (common block at slot 0, +1 ticket to 1).
 ***************************************************************************)
CONSTANTS SlotsPerEpoch, KReg, MaxReorg, MatMin, BtcMat, EndSlot
E == 2
Start(e) == e * SlotsPerEpoch
Freeze(e) == (e-1) * SlotsPerEpoch
Cut(e) == Freeze(e) - KReg
ASSUME /\ SlotsPerEpoch >= 2 /\ KReg >= 1 /\ MaxReorg >= 1
       /\ Cut(1) <= 0 /\ Cut(E) > 0
       /\ Freeze(E) <= MatMin /\ MatMin <= BtcMat /\ BtcMat <= Start(E)
       /\ EndSlot >= Start(E)
Nodes == {1, 2}
Branches == {1, 2}              \* lane 1 public; lane 2 adversarial/private
Producers == {1, 2, 3}          \* producer n = honest node n; 3 Byzantine
Epoch(s) == s \div SlotsPerEpoch
Base == EndSlot + 2
Block(b,s) == 1 + b * Base + s
Slot(x) == (x-1) % Base
Prefix(c,k) == SubSeq(c,1,k)
Last(c) == c[Len(c)]
InitialChain == <<Block(0,0)>>  \* common ADD op at slot 0 < Cut(E)
InitialWeights == <<1,1,1>>
IsPrefix(a,b) == /\ Len(a) <= Len(b) /\ a = Prefix(b,Len(a))
LCA(a,b) == CHOOSE k \in 0..Len(a):
             /\ k <= Len(b) /\ Prefix(a,k) = Prefix(b,k)
             /\ \A j \in (k+1)..Len(a):
                    j > Len(b) \/ Prefix(a,j) # Prefix(b,j)

\* ---- Rule A with explicit maturity (M = set of blocks carrying m_E) ----
CarrierM(c,M) == LET ks == {i \in 1..Len(c): c[i] \in M}
                 IN IF ks = {} THEN 0 ELSE CHOOSE i \in ks: \A j \in ks: i <= j
Raw(c) == SelectSeq(c, LAMBDA x: Slot(x) < Cut(E))
CountM(c,M) == IF CarrierM(c,M) = 0 THEN 0 ELSE
    Cardinality({i \in 1..CarrierM(c,M): Slot(c[i]) >= Cut(E)})
PassM(c,M) == CarrierM(c,M) # 0 /\ CountM(c,M) >= MaxReorg
SupportM(c,M) == IF PassM(c,M) THEN Raw(c) ELSE <<>>   \* A_1 = genesis
Ops(sup) == {sup[i]: i \in {j \in 1..Len(sup): Slot(sup[j]) = 0}}
Weights(ops) == [p \in Producers |->
                   InitialWeights[p] + (IF p = 1 THEN Cardinality(ops) ELSE 0)]
RegistryM(c,e,M) == IF e = E THEN Weights(Ops(SupportM(c,M))) ELSE InitialWeights
Weight(r) == r[1] + r[2] + r[3]
Root(r) == r[1] + 8*r[2] + 64*r[3]
Owner(r,s) == LET j == (s + Root(r) + 1) % Weight(r)   \* Fast2 formula, btc = 0
              IN IF j < r[1] THEN 1 ELSE IF j < r[1]+r[2] THEN 2 ELSE 3

VARIABLES slot, chains, mature, forked, vis, local, journal
vars == <<slot, chains, mature, forked, vis, local, journal>>

Carrier(c) == CarrierM(c,mature)
CarrierSlot(c) == IF Carrier(c) = 0 THEN -1 ELSE Slot(c[Carrier(c)])
Count(c) == CountM(c,mature)
Pass(c) == PassM(c,mature)
D(c) == SupportM(c,mature)          \* P_0 and P_1 are genesis on every branch
Closed(c) == Carrier(c) # 0
OwnerIn(c,i) == Owner(RegistryM(Prefix(c,i),Epoch(Slot(c[i])),mature),Slot(c[i]))
TieAt(c,i) == LET s == Slot(c[i]) e == Epoch(s)
                  r == RegistryM(Prefix(c,i),e,mature)
              IN ((e*2)*512 + Root(r))*Base*4 + s*4 + Owner(r,s)
Better(a,b) == \/ Len(a) > Len(b)
               \/ /\ Len(a) = Len(b)
                  /\ \E i \in 1..Len(a):
                        /\ TieAt(a,i) < TieAt(b,i)
                        /\ \A j \in 1..(i-1): TieAt(a,j) = TieAt(b,j)
Candidates(seen) == {Prefix(chains[b],seen[b]): b \in Branches}
Maxima(seen) == {c \in Candidates(seen): ~\E d \in Candidates(seen): Better(d,c)}
Disc(tip,c) == Len(tip) - LCA(tip,c)
Deep(n,c) == \/ ~IsPrefix(local[n].anchor,c)
             \/ Disc(local[n].tip,c) > MaxReorg
\* BaseNDecision (9.5) without H1/BTC branches.
Decision(n,seen) ==
  LET m == Maxima(seen)
  IN IF \E c \in m: Deep(n,c) THEN [mode |-> "STOP_DEEP", adopt |-> {}]
     ELSE IF Cardinality(m) > 1 THEN [mode |-> "STOP_TIE", adopt |-> {}]
     ELSE [mode |-> "RUN", adopt |-> m]
AnchorAfter(n,c) == LET k == Len(c) - MaxReorg
                   IN IF k > Len(local[n].anchor) THEN Prefix(c,k)
                      ELSE local[n].anchor
NewSeen(n) == [b \in Branches |-> IF <<n,b>> \in vis THEN Len(chains[b])
                                  ELSE local[n].seen[b]]
HasEpochBlock(c) == \E i \in 1..Len(c): Epoch(Slot(c[i])) = E
\* M = maturity set AFTER the step (the producer's own carrier included).
EntryM(n,k,c,prev,M) ==
  [t |-> Cardinality(journal), node |-> n, kind |-> k, slot |-> slot,
   D |-> SupportM(c,M), chain |-> c, prev |-> prev, disc |-> Disc(prev,c),
   prevD |-> IF CarrierM(prev,M) # 0 THEN SupportM(prev,M) ELSE <<0>>]   \* <<0>>: window still open (no block id is 0)
Entry(n,k,c,prev) == EntryM(n,k,c,prev,mature)

Init ==
  /\ slot = 1
  /\ chains = [b \in Branches |-> InitialChain]
  /\ mature = {}
  /\ forked = FALSE
  /\ vis = {<<n,1>>: n \in Nodes}
  /\ local = [n \in Nodes |-> [seen |-> [b \in Branches |-> 1],
               tip |-> InitialChain, anchor |-> <<>>, mode |-> "RUN",
               signed |-> -1]]
  /\ journal = {}

(* Fetch = delivery + full validation + BaseNDecision + adoption, atomic.
   An adoption of a chain whose m_E window is closed installs R_E (5.2:
   "aucune nouvelle valeur definitive de R_e n'est installee" before it).
   kind "adoption" if the chain has a block of E (engagement), else
   "installation" (counted by CP_reg, 5.7.2). *)
Fetch(n) ==
  LET seen == NewSeen(n)
      d == Decision(n,seen)
      adopts == d.adopt # {}
      c == IF adopts THEN CHOOSE x \in d.adopt: TRUE ELSE local[n].tip
      changed == c # local[n].tip
      upd == [local[n] EXCEPT !.seen = seen, !.tip = c, !.mode = d.mode,
                              !.anchor = IF adopts THEN AnchorAfter(n,c) ELSE @]
  IN /\ upd # local[n]
     /\ local' = [local EXCEPT ![n] = upd]
     /\ journal' = IF changed /\ Closed(c)
                   THEN journal \cup {Entry(n, IF HasEpochBlock(c) THEN "adoption"
                                                ELSE "installation", c, local[n].tip)}
                   ELSE journal
     /\ UNCHANGED <<slot, chains, mature, forked, vis>>

(* Honest production on the adopted tip, current slot only; ref discipline:
   carries m_E iff slot >= BtcMat or the parent carries it. Closing the
   window in the candidate derives R_E before signing (5.2). *)
HProduce(p,b) ==
  LET c == local[p].tip
      x == Block(b,slot)
      m == slot >= BtcMat \/ Closed(c)
      M2 == IF m THEN mature \cup {x} ELSE mature
      nc == Append(c,x)
  IN /\ <<p,b>> \in vis
     /\ chains[b] = c /\ local[p].seen[b] = Len(c)
     /\ Slot(Last(c)) < slot /\ local[p].signed # slot
     /\ local[p].mode = "RUN" /\ c \in Maxima(local[p].seen) /\ ~Deep(p,c)
     /\ Owner(RegistryM(nc,Epoch(slot),M2),slot) = p
     /\ chains' = [chains EXCEPT ![b] = nc]
     /\ mature' = M2
     /\ local' = [local EXCEPT ![p].tip = nc, ![p].signed = slot,
                               ![p].seen[b] = Len(nc),
                               ![p].anchor = AnchorAfter(p,nc)]
     /\ journal' = IF Epoch(slot) = E
                   THEN journal \cup {EntryM(p,"signature",nc,c,M2)}
                   ELSE IF Closed(c) \/ ~m THEN journal
                   ELSE journal \cup {EntryM(p,"installation",nc,c,M2)}
     /\ UNCHANGED <<slot, forked, vis>>

(* Byzantine production. Lane 1 (public): current slot only. Lane 2
   (private): any slot s with last slot < s <= current slot (backdating).
   Maturity choice mm only if the parent does not already carry it and s is
   not in E; legal only if s >= MatMin and m_E exists (slot >= BtcMat). *)
AProduce(b,s,mm) ==
  LET c == chains[b]
      x == Block(b,s)
      m == IF Closed(c) \/ Epoch(s) = E THEN TRUE ELSE mm
      M2 == IF m THEN mature \cup {x} ELSE mature
      nc == Append(c,x)
  IN /\ IF b = 1 THEN s = slot ELSE s <= slot
     /\ Slot(Last(c)) < s
     /\ m => (s >= MatMin /\ slot >= BtcMat)
     /\ Owner(RegistryM(nc,Epoch(s),M2),s) = 3
     /\ chains' = [chains EXCEPT ![b] = nc]
     /\ mature' = M2
     /\ UNCHANGED <<slot, forked, vis, local, journal>>

\* The adversary roots its private lane on a prefix of the public lane, once,
\* before revealing it to anyone and before owning a block of its own.
Fork(k) ==
  /\ ~forked /\ chains[2] = InitialChain
  /\ \A n \in Nodes: <<n,2>> \notin vis
  /\ k \in 1..Len(chains[1])
  /\ chains' = [chains EXCEPT ![2] = Prefix(chains[1],k)]
  /\ forked' = TRUE
  /\ UNCHANGED <<slot, mature, vis, local, journal>>
\* Selective, monotone delivery of the private lane to one honest node.
Reveal(n) == /\ <<n,2>> \notin vis /\ vis' = vis \cup {<<n,2>>}
             /\ UNCHANGED <<slot, chains, mature, forked, local, journal>>
Tick == /\ slot < EndSlot /\ slot' = slot + 1
        /\ UNCHANGED <<chains, mature, forked, vis, local, journal>>

Next == \/ \E n \in Nodes: Fetch(n)
        \/ \E p \in Nodes, b \in Branches: HProduce(p,b)
        \/ \E b \in Branches, s \in 1..EndSlot, mm \in BOOLEAN: AProduce(b,s,mm)
        \/ \E k \in 1..(EndSlot+1): Fork(k)
        \/ \E n \in Nodes: Reveal(n)
        \/ Tick
Spec == Init /\ [][Next]_vars

\* ---------------------------- Sanity invariants ---------------------------
TypeOK == /\ slot \in 1..EndSlot
          /\ \A b \in Branches: chains[b] \in Seq(1..(3*Base))
          /\ \A n \in Nodes: local[n].mode \in {"RUN","STOP_DEEP","STOP_TIE"}
MaturityLegal == \A b \in Branches: \A i \in 1..Len(chains[b]):
   /\ chains[b][i] \in mature => Slot(chains[b][i]) >= MatMin
   /\ Epoch(Slot(chains[b][i])) = E => chains[b][i] \in mature
   /\ (i > 1 /\ chains[b][i-1] \in mature) => chains[b][i] \in mature
AdoptWithinMaxreorg == \A a \in journal: a.disc <= MaxReorg

\* ----------------------------- Monitors (L1) ------------------------------
\* Structural class of two honest commitments (same partition as _L1).
Class(a,b) == IF a.D = b.D THEN "none"
              ELSE IF Raw(a.chain) # Raw(b.chain) THEN "i_raw"
              ELSE IF Pass(a.chain) # Pass(b.chain) THEN "ii_pivot" ELSE "other"
NoOtherStructural == \A a,b \in journal: Class(a,b) # "other"
NoWitnessPivot == \A a,b \in journal: Class(a,b) # "ii_pivot"

(* Deep-pivot SHAPE on two chains: x passes rule A, y does not, same raw
   prefix, y closed its window EARLY (before x) at a slot that no honest
   producer can use (< BtcMat: only a backdated maturity reaches it), and
   every block of y after the fork is Byzantine (private branch). The shallow
   pivot (count zone) has both closures under honest discipline. *)
\* Honest blocks alone reach the threshold in x's window (robust pass: the
\* pass does not depend on a Byzantine block, i.e. NOT the count zone).
HonestCount(x) == IF ~Closed(x) THEN 0 ELSE
  Cardinality({i \in 1..Carrier(x): Slot(x[i]) >= Cut(E) /\ OwnerIn(x,i) # 3})
MixedShapeChains(x,y) ==
  /\ Closed(x) /\ Closed(y)
  /\ Raw(x) = Raw(y)
  /\ Pass(x) /\ ~Pass(y)
  /\ CarrierSlot(y) < CarrierSlot(x)
  /\ CarrierSlot(y) < BtcMat
  /\ \A i \in (LCA(x,y)+1)..Len(y): OwnerIn(y,i) = 3
DeepShapeChains(x,y) == MixedShapeChains(x,y) /\ HonestCount(x) >= MaxReorg
DeepShape(a,b) == a.D # b.D /\ DeepShapeChains(a.chain,b.chain)
MixedShape(a,b) == a.D # b.D /\ MixedShapeChains(a.chain,b.chain)
\* Weaker variant (x may pass thanks to Byzantine blocks): early closure
\* combined with the count zone.
MixedSync(a,b) == /\ MixedShape(a,b) /\ b.kind \in {"installation","adoption"}
                  /\ b.disc > 0 /\ b.prevD = a.D /\ a.t < b.t
NoWitnessMixedSync == ~\E a,b \in journal: MixedSync(a,b)
Installs(b) == b.kind \in {"installation","adoption"}
\* Variant SYNC: an honest synchronized on the passing side (its previous tip
\* was closed with a's D) switches to y with disconnection > 0.
DeepSync(a,b) == /\ DeepShape(a,b) /\ Installs(b)
                 /\ b.disc > 0 /\ b.prevD = a.D /\ a.t < b.t
\* Variant AFTER_SIG: y installed by an honest after another honest signed
\* a block of E on the passing side.
DeepAfterSig(a,b) == /\ DeepShape(a,b) /\ Installs(b)
                     /\ a.kind = "signature" /\ a.node # b.node /\ a.t < b.t
DeepAny(a,b) == DeepSync(a,b) \/ DeepAfterSig(a,b)
NoWitnessDeepSync == ~\E a,b \in journal: DeepSync(a,b)
NoWitnessDeepSyncBeforeStart ==
  ~\E a,b \in journal: DeepSync(a,b) /\ b.slot < Start(E)
NoWitnessDeepAfterSig == ~\E a,b \in journal: DeepAfterSig(a,b)
\* Same property as a plain invariant (a violation would be FAIL, not TEMOIN).
DeepAbsent == ~\E a,b \in journal: DeepAny(a,b)
\* Contrast: a synchronized honest that installed the passing side sees a
\* deep-pivot-shaped maximum and maxreorg turns it into STOP_DEEP.
DeepStop == \E n \in Nodes:
  /\ local[n].mode = "STOP_DEEP" /\ Closed(local[n].tip) /\ Pass(local[n].tip)
  /\ \E y \in Maxima(local[n].seen):
        /\ DeepShapeChains(local[n].tip,y)
        /\ Disc(local[n].tip,y) > MaxReorg
NoWitnessDeepStop == ~DeepStop
====
