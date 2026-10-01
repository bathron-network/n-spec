---- MODULE NonInterference_Deliv ----
(***************************************************************************)
(* NEW module (01/10, Q3). No delivered file is changed.                   *)
(*                                                                         *)
(* Question: does the application delivery threshold of N-SPEC v0.7 §14.2  *)
(* (profile parameter rho, IDs 6-7 of §3.3) interfere with consensus?      *)
(*                                                                         *)
(* Method: self-composition. Two copies c1, c2 of the SAME observer node   *)
(* are driven in lockstep by ONE environment (block tree, publication,     *)
(* eclipse, adversary, honest abstention, clock). Copy i runs with the     *)
(* client policy Pol(i) = [maxreorg |-> MaxReorg, rho |-> r_i]. r1 is the  *)
(* laboratory value 7/10; r2 is chosen in Init among Rhos, which contains  *)
(* every threshold class distinguishable on these windows (all fractions   *)
(* k/w, w <= MaxSlot, plus 0 and > 1). Every consensus operator receives   *)
(* the whole policy record, so a dependence on rho is expressible; only    *)
(* the mutations below actually read it.                                   *)
(*                                                                         *)
(* Because each product step is one step of both copies under identical    *)
(* environment choices, the state invariant ConsEqual over the product is  *)
(* exactly "the two runs have the same consensus trace":                   *)
(*   tip / adoptions (Select, BaseNDecision, §9.5), anchor (§9.6),         *)
(*   STOP modes HALTED_DEEP_REORG / EQUIVOCATION_TIE (§9.5),               *)
(*   brake health, ordinary and slow-lane exclusions (§6.6),               *)
(*   own production decisions (§5.9, §7.3).                                *)
(* Transitivity: forall rho: trace(rho) = trace(7/10)  =>  any two equal.  *)
(*                                                                         *)
(* Abstractions (all NT elsewhere, stated in LIVRAISON-HN.md): score =     *)
(* length; no H1, no Bitcoin, registry = exclusion set over a fixed public *)
(* calendar; one object carried by the block of slot ObjSlot; density      *)
(* windows WShort/WLong stand for 100/1000; KDepth stands for N = 77.      *)
(***************************************************************************)
EXTENDS Naturals, Sequences, FiniteSets

CONSTANTS MaxSlot, MaxReorg, EpochLen, Owner, Ids,
          WShort, WLong, KDepth, ObjSlot,
          RhoRef, Rhos, HealthNum, HealthDen, Mutation

ASSUME Mutation \in {"NONE", "SELECT_GATED", "BRAKE_SHARED", "STOP_BYPASS"}

VARIABLES now, tree, public, seen, r1, r2, c1, c2
vars == <<now, tree, public, seen, r1, r2, c1, c2>>

Slots == 1..MaxSlot
Prefixes(c) == {SubSeq(c, 1, k) : k \in 0..Len(c)}
LastSlot(c) == IF c = <<>> THEN 0 ELSE c[Len(c)][1]
Extends(c, a) == Len(a) <= Len(c) /\ SubSeq(c, 1, Len(a)) = a
CommonLen(a, b) ==
  LET K == {k \in 0..Len(a) : k <= Len(b) /\ SubSeq(a, 1, k) = SubSeq(b, 1, k)}
  IN CHOOSE k \in K : \A j \in K : j <= k
Disconnect(tip, c) == Len(tip) - CommonLen(tip, c)
Maxima(S) == {c \in S : \A d \in S : Len(d) <= Len(c)}
Pol(r) == [maxreorg |-> MaxReorg, rho |-> r]

OnChain(tip, s) == \E i \in 1..Len(tip) : tip[i][1] = s
Filled(tip, a, b) == Cardinality({i \in 1..Len(tip) : tip[i][1] \in a..b})
\* Exact §14.2 inequality den*filled >= num*len ; incomplete window = UNKNOWN = fail.
DensOK(tip, a, b, rho) ==
  /\ a >= 1 /\ a <= b
  /\ rho[2] * Filled(tip, a, b) >= rho[1] * (b - a + 1)

(***************************************************************************)
(* Application delivery (§14.2), evaluated by a copy with its own rho.     *)
(* Pure output: never assigned to a state variable, never read by Next    *)
(* except in the mutations.                                                *)
(***************************************************************************)
DeliverableTip(tip, mode, rho, t) ==
  LET last == t - 1 IN
  /\ mode = "RUN"
  /\ \E i \in 1..Len(tip) :
        /\ tip[i][1] = ObjSlot
        /\ Len(tip) - i + 1 >= KDepth
  /\ DensOK(tip, last - WShort + 1, last, rho)
  /\ DensOK(tip, last - WLong + 1, last, rho)
  /\ DensOK(tip, ObjSlot, last, rho)
Deliverable(c, r) == DeliverableTip(c.tip, c.mode, r, now)

(***************************************************************************)
(* Consensus of one copy. BaseNDecision without H1/BTC (§9.5).             *)
(***************************************************************************)
\* Candidate set seen by BaseNDecision. Only SELECT_GATED lets delivery filter it.
Cand(c, pol, S) ==
  IF Mutation = "SELECT_GATED"
  THEN {x \in Maxima(S) : DeliverableTip(x, "RUN", pol.rho, now)}
  ELSE Maxima(S)

BaseN(c, pol, S) ==
  LET M == Cand(c, pol, S)
      deep == \E x \in M : ~Extends(x, c.anchor)
                            \/ Disconnect(c.tip, x) > pol.maxreorg
      bypass == Mutation = "STOP_BYPASS" /\ Deliverable(c, pol.rho)
  IN IF M = {} THEN "WAIT"
     ELSE IF deep /\ ~bypass THEN "HALTED_DEEP_REORG"
     ELSE IF Cardinality(M) > 1 THEN "EQUIVOCATION_TIE"
     ELSE "UNIQUE"

NextAnchor(old, t) ==
  LET nb == SubSeq(t, 1, IF Len(t) > MaxReorg THEN Len(t) - MaxReorg ELSE 0)
  IN IF Len(nb) > Len(old) THEN nb ELSE old

SelectCopy(c, pol, S) ==
  LET d == BaseN(c, pol, S) IN
  CASE d = "UNIQUE" ->
         LET win == CHOOSE x \in Cand(c, pol, S) : TRUE IN
         [c EXCEPT !.tip = win, !.anchor = NextAnchor(c.anchor, win), !.mode = "RUN",
                   !.adoptions = c.adoptions + (IF win # c.tip THEN 1 ELSE 0),
                   !.maxDisc = IF Disconnect(c.tip, win) > c.maxDisc
                               THEN Disconnect(c.tip, win) ELSE c.maxDisc]
    [] d = "WAIT" -> c
    [] OTHER -> [c EXCEPT !.mode = d]           \* no adoption; re-evaluated later

Rank(id) == CASE id = "A" -> 1 [] id = "H" -> 2 [] OTHER -> 3

(* Brake (§6.6) at the end of epoch e on the adopted chain.                *)
(* Health threshold HealthNum/HealthDen is a consensus constant (7/10).    *)
EpochEnd(c, pol, e) ==
  LET es == ((e - 1) * EpochLen + 1)..(e * EpochLen)
      att(id) == {s \in es : Owner[s] = id}
      queued == {id \in Ids \ c.excluded :
                   att(id) # {} /\ \A s \in att(id) : ~OnChain(c.tip, s)}
      elig == {s \in es : Owner[s] \notin queued \cup c.excluded}
      fil == {s \in elig : OnChain(c.tip, s)}
      hn == IF Mutation = "BRAKE_SHARED" THEN pol.rho[1] ELSE HealthNum
      hd == IF Mutation = "BRAKE_SHARED" THEN pol.rho[2] ELSE HealthDen
      ok == elig # {} /\ hd * Cardinality(fil) >= hn * Cardinality(elig)
      active == Ids \ c.excluded
      cand == {id \in queued : active \ {id} # {}}      \* never the last weight
      first == CHOOSE id \in cand : \A j \in cand : Rank(id) <= Rank(j)
      slowAllowed == c.slowLast = 0                     \* slow quota: 1 per 2 epochs
  IN IF cand = {} THEN [c EXCEPT !.health = ok, !.slowLast = 0]
     ELSE IF ok THEN [c EXCEPT !.health = TRUE, !.excluded = @ \cup {first},
                               !.ordinary = @ + 1, !.slowLast = 0]
     ELSE IF slowAllowed
          THEN [c EXCEPT !.health = FALSE, !.excluded = @ \cup {first},
                         !.slow = @ + 1, !.slowLast = 1]
          ELSE [c EXCEPT !.health = FALSE, !.slowLast = 0]

InitCopy == [tip |-> <<>>, anchor |-> <<>>, mode |-> "RUN", adoptions |-> 0,
             maxDisc |-> 0, excluded |-> {}, health |-> TRUE, ordinary |-> 0,
             slow |-> 0, slowLast |-> 0, produced |-> {}]

(***************************************************************************)
(* Environment (shared, lockstep).                                         *)
(***************************************************************************)
Init == /\ now = 1 /\ tree = {<<>>} /\ public = {<<>>} /\ seen = {<<>>}
        /\ r1 = RhoRef /\ r2 \in Rhos
        /\ c1 = InitCopy /\ c2 = InitCopy

Live == now <= MaxSlot
NoBlockAt(tag) == ~\E c \in tree : Len(c) > 0 /\ c[Len(c)] = <<now, tag>>

\* Delivery + full validation + Select are one atomic abstraction (as in
\* RegistryModelV6): whenever the observer's view changes, both copies run
\* SelectCopy on the same new view.
SelectBoth(S) == /\ c1' = SelectCopy(c1, Pol(r1), S)
                 /\ c2' = SelectCopy(c2, Pol(r2), S)

\* `public` = honest network view (honest and observer blocks; D = 0). The
\* adversary never publishes to it: its blocks reach the observer only via
\* Show (eclipse / selective delivery). Other honest producer: extends a
\* longest public chain, or abstains (no action).
HonestProduce ==
  /\ Live /\ Owner[now] = "H" /\ NoBlockAt("h")
  /\ \E p \in Maxima(public) :
       LET b == Append(p, <<now, "h">>) IN
       /\ tree' = tree \cup {b} /\ public' = public \cup {b}
       /\ seen' = seen \cup {b}            \* honest blocks reach the observer (D = 0)
       /\ SelectBoth(seen')
       /\ UNCHANGED <<now, r1, r2>>

\* Observer's own slot: production decision is part of its consensus trace.
\* The shared block is built on copy 1's tip; ConsEqual makes this harmless.
ObserverProduce ==
  /\ Live /\ Owner[now] = "O" /\ NoBlockAt("o")
  /\ c1.mode # "HALTED_DEEP_REORG"
  /\ LET b == Append(c1.tip, <<now, "o">>)
         p1 == [c1 EXCEPT !.produced = @ \cup {now}]
         p2 == IF c2.mode # "HALTED_DEEP_REORG"
               THEN [c2 EXCEPT !.produced = @ \cup {now}] ELSE c2
     IN /\ tree' = tree \cup {b} /\ public' = public \cup {b}
        /\ seen' = seen \cup {b}
        /\ c1' = SelectCopy(p1, Pol(r1), seen')
        /\ c2' = SelectCopy(p2, Pol(r2), seen')
        /\ UNCHANGED <<now, r1, r2>>

\* Adversary: any parent, equivocation (two tags), never public.
AdvProduce ==
  /\ Live /\ Owner[now] = "A"
  /\ \E p \in tree, tag \in {"a1", "a2"} :
       /\ LastSlot(p) < now /\ NoBlockAt(tag)
       /\ tree' = tree \cup {Append(p, <<now, tag>>)}
       /\ UNCHANGED <<now, public, seen, r1, r2, c1, c2>>

\* Eclipse: the observer is shown a private chain without publication.
\* Only current leaves are shown (a prefix is shown with its leaf).
Show == \E c \in tree :
          /\ ~(c \in seen)
          /\ ~(\E d \in tree : d # c /\ Extends(d, c))
          /\ seen' = seen \cup Prefixes(c)
          /\ SelectBoth(seen')
          /\ UNCHANGED <<now, tree, public, r1, r2>>

Tick == /\ Live
        /\ now' = now + 1
        /\ IF now % EpochLen = 0
           THEN /\ c1' = SelectCopy(EpochEnd(c1, Pol(r1), now \div EpochLen), Pol(r1), seen)
                /\ c2' = SelectCopy(EpochEnd(c2, Pol(r2), now \div EpochLen), Pol(r2), seen)
           ELSE SelectBoth(seen)
        /\ UNCHANGED <<tree, public, seen, r1, r2>>

Next == HonestProduce \/ ObserverProduce \/ AdvProduce \/ Show \/ Tick
Spec == Init /\ [][Next]_vars

(***************************************************************************)
(* Properties                                                              *)
(***************************************************************************)
Cons(c) == c    \* every field of a copy is consensus state; delivery is not stored
ConsEqual == Cons(c1) = Cons(c2)

\* No incompatible adoption, in each copy, whatever its threshold.
AdoptSafe == \A c \in {c1, c2} : Extends(c.tip, c.anchor) /\ c.maxDisc <= MaxReorg
\* STOP is never bypassed by delivery: a halted copy delivers nothing.
StopRespected == \A x \in {<<c1, r1>>, <<c2, r2>>} :
                   x[1].mode # "RUN" => ~Deliverable(x[1], x[2])
TypeOK == /\ now \in 1..(MaxSlot + 1) /\ r2 \in Rhos
          /\ c1.mode \in {"RUN", "HALTED_DEEP_REORG", "EQUIVOCATION_TIE"}

(* Non-vacuity traps (status TÉMOIN when violated).                        *)
NoWitnessDeliveryDiffers == Deliverable(c1, r1) = Deliverable(c2, r2)
NoWitnessHalted == c1.mode # "HALTED_DEEP_REORG"
NoWitnessSlowLane == c1.slow = 0
NoWitnessReorgAdoption == c1.maxDisc = 0
NoWitnessDeliveredLowDensity == ~(Deliverable(c2, r2) /\ ~Deliverable(c1, r1))
====
