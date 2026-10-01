------------------------------ MODULE RegistryModelFast ------------------------------
EXTENDS Naturals, Integers, Sequences, FiniteSets, TLC

(***************************************************************************
 N-SPEC v0.6 registry A mirror. Other submachines inherited v0.5.
 This is a focused mirror, NOT a claim of integrated v0.6 conformance.
 Sections 5, 7, 9, 11-12, 23. Finite interaction model.
 Two lanes share an INITIAL prefix, then can diverge; no common-prefix axiom
 or constraint removes a reachable state. ForkSlot bounds the scenario, not
 the implementation. MC_spec_registryreorg widens this bound to slot zero.
 Hashes/signatures and valid prepared ADDs are abstracted, not implemented.
 ***************************************************************************)
CONSTANTS Epochs, SlotsPerEpoch, EndSlot, KReg, MaxReorg, ForkSlot,
          BrokenTipSnapshot, BrokenH1Promote, RuleA
ASSUME /\ Epochs >= 2 /\ SlotsPerEpoch >= 2 /\ KReg > 0
       /\ ForkSlot \in {0, 1} /\ MaxReorg > 0
Nodes == {1, 2}
Branches == {1, 2}
Producers == {1, 2, 3}                 \* 3 is Byzantine
Es == 0..(Epochs-1)
LastSlot == EndSlot
Epoch(s) == s \div SlotsPerEpoch
Base == LastSlot + 2
Block(b,s) == 1 + b * Base + s
Slot(x) == (x-1) % Base
Lane(x) == (x-1) \div Base
Prefix(c,k) == SubSeq(c,1,k)
InitialChain == IF ForkSlot = 1 THEN <<Block(0,0)>> ELSE <<>>
InitialWeights == <<2,1,1>>            \* four individually owned tickets
IsPrefix(a,b) == /\ Len(a) <= Len(b) /\ a = Prefix(b,Len(a))
LCA(a,b) == CHOOSE k \in 0..Len(a):
             /\ k <= Len(b) /\ Prefix(a,k) = Prefix(b,k)
             /\ \A j \in (k+1)..Len(a):
                    j > Len(b) \/ Prefix(a,j) # Prefix(b,j)
Cut(e) == (e-1) * SlotsPerEpoch - KReg
\* Public maturity is reduced to epoch start; first carrier is branch-derived.
\* Separate RegistryWindow campaign explores delayed/withheld carriers.
RawSupport(c,e) == IF e = 0 \/ Cut(e) <= 0 THEN <<>>
                   ELSE SelectSeq(c,LAMBDA x: Slot(x) < Cut(e))
Carrier(c,e) == LET ks == {i \in 1..Len(c): Slot(c[i]) >= e*SlotsPerEpoch}
                IN IF ks = {} THEN 0 ELSE CHOOSE i \in ks: \A j \in ks: i <= j
WindowCount(c,e) == IF Carrier(c,e) = 0 THEN 0 ELSE
    Cardinality({i \in 1..Carrier(c,e): Slot(c[i]) >= Cut(e)})
RECURSIVE Support(_, _)
Support(c,e) == IF e = 0 \/ Cut(e)<=0 THEN <<>>
  ELSE IF RuleA /\ Len(c)<MaxReorg THEN Support(c,e-1)
  ELSE IF ~RuleA \/ (Carrier(c,e) # 0 /\ WindowCount(c,e) >= MaxReorg)
       THEN RawSupport(c,e) ELSE Support(c,e-1)
RECURSIVE ReferenceSupport(_, _)
ReferenceSupport(c,e) == IF e = 0 THEN <<>>
  ELSE IF ~RuleA \/ (Carrier(c,e) # 0 /\ WindowCount(c,e) >= MaxReorg)
       THEN RawSupport(c,e) ELSE ReferenceSupport(c,e-1)

Supports(c,e) == [j \in 0..e |-> Support(c,j)]
Ops(c) == {c[i]: i \in {j \in 1..Len(c): Slot(c[j]) \in {0,ForkSlot}}}
Recipient(x) == IF Lane(x) = 2 THEN 2 ELSE 1
Weights(ops) == [p \in Producers |-> InitialWeights[p] +
                              Cardinality({x \in ops: Recipient(x) = p})]
RECURSIVE ReplayOps(_, _)
ReplayOps(c,e) == IF e = 0 THEN {} ELSE ReplayOps(c,e-1) \cup Ops(Support(c,e))
ReferenceRegistry(c,e) == Weights(Ops(Support(c,e)))
Registry(c,e) == IF BrokenTipSnapshot /\ e > 0 THEN Weights(Ops(c))
                ELSE Weights(ReplayOps(c,e))
Weight(r) == r[1]+r[2]+r[3]
Root(r) == r[1] + 8*r[2] + 64*r[3]  \* injective for these ticket bounds

VARIABLES slot, chains, blockTie, local, bitcoin, ready, partition, absent,
          evidence, audit, recoveryUsed
vars == <<slot,chains,blockTie,local,bitcoin,ready,partition,absent,evidence,
          audit,recoveryUsed>>

(***************************************************************************
 A seed commits to epoch, Bitcoin fact, AND registry root (5.4).
 Toy lottery cycles over individual tickets; it is not a random oracle or
 a claimed unbiased cryptographic instantiation. All 2^(Epochs-1) BTC vectors (genesis BTC fixed)
 are enumerated in Init. Seed readiness abstracts guard + confirmations.
 ***************************************************************************)
Seed(r,e) == <<e,bitcoin[e],Root(r)>>
Candidate(c,s) == IF Len(c)>0 /\ Slot(c[Len(c)])=s THEN c
                  ELSE Append(c,Block(0,s))
ProductionRegistry(c,e,s) == Registry(Candidate(c,s),e)
Owner(c,e,s) == LET r == ProductionRegistry(c,e,s)
                   j == (s + bitcoin[e] + Root(r) + 1) % Weight(r)
               IN IF j < r[1] THEN 1 ELSE IF j < r[1]+r[2] THEN 2 ELSE 3
ComputedTie(c,i) == LET e == Epoch(Slot(c[i]))
               r == Registry(Prefix(c,i),e)
           IN ((e*2 + bitcoin[e])*512 + Root(r))*Base*4
              + Slot(c[i])*4 + Owner(Prefix(c,i-1),e,Slot(c[i]))
Tie(c,i) == blockTie[c[i]]
BlockIds(c) == {c[i]: i \in 1..Len(c)}
TieMap(cs) == [x \in 1..(3*Base) |->
               IF x \in BlockIds(cs[1]) THEN
                 ComputedTie(cs[1],CHOOSE i \in 1..Len(cs[1]): cs[1][i] = x)
               ELSE IF x \in BlockIds(cs[2]) THEN
                 ComputedTie(cs[2],CHOOSE i \in 1..Len(cs[2]): cs[2][i] = x)
               ELSE 0]
Better(a,b) == \/ Len(a) > Len(b)
               \/ /\ Len(a) = Len(b)
                  /\ \E i \in 1..Len(a):
                        /\ Tie(a,i) < Tie(b,i)
                        /\ \A j \in 1..(i-1): Tie(a,j) = Tie(b,j)
Candidates(seen) == {Prefix(chains[b],seen[b]): b \in Branches}
Maxima(seen) == {c \in Candidates(seen):
                         ~\E d \in Candidates(seen): Better(d,c)}
Deep(n,c) == \/ ~IsPrefix(local[n].anchor,c)
             \/ Len(local[n].tip)-LCA(local[n].tip,c) > MaxReorg
BaseAdoptable(n,seen) == LET m == Maxima(seen)
                       IN IF Cardinality(m) = 1 /\
                             ~\E c \in m: Deep(n,c)
                          THEN m ELSE {}
Relevant(n,seen) == LET m == Maxima(seen)
                       pairs == m \cup {local[n].tip}
                   IN \E a,b \in pairs:
                        /\ a \in m \/ b \in m
                        /\ ~IsPrefix(a,b) /\ ~IsPrefix(b,a)
                        /\ \/ ~IsPrefix(local[n].anchor,a)
                           \/ ~IsPrefix(local[n].anchor,b)
                           \/ Len(a)-LCA(a,b) > MaxReorg
                           \/ Len(b)-LCA(a,b) > MaxReorg
Decision(n,seen) ==
  LET m == Maxima(seen)
      base == BaseAdoptable(n,seen)
      \* BUG: evidence is misused as positive authority, even over base HALT.
      promote == BrokenH1Promote /\ evidence = "LAG" /\ Relevant(n,seen)
      promoted == Prefix(chains[2],seen[2])
  IN IF Epoch(slot) \notin ready THEN [mode |-> "WAIT_SEED", adopt |-> {}]
     ELSE IF promote THEN [mode |-> "RUN", adopt |-> {promoted}]
     ELSE IF \E c \in m: Deep(n,c)
          THEN [mode |-> "STOP_DEEP", adopt |-> {}]
     ELSE IF Relevant(n,seen) /\ evidence # "NONE"
          THEN [mode |-> IF evidence = "UNKNOWN" THEN "WAIT_H1" ELSE "STOP_H1",
                adopt |-> {}]
     ELSE IF Cardinality(m) > 1 THEN [mode |-> "STOP_TIE", adopt |-> {}]
     ELSE [mode |-> "RUN", adopt |-> base]

Online(n) == n = 1 \/ ~absent
Visible(n,b) == ~partition \/ n = b
NewSeen(n) == [b \in Branches |-> IF Visible(n,b) THEN Len(chains[b])
                                                    ELSE local[n].seen[b]]
AnchorAfter(n,c) == LET k == Len(c)-MaxReorg
                   IN IF k > Len(local[n].anchor) THEN Prefix(c,k)
                      ELSE local[n].anchor
Stops == {"STOP_DEEP","STOP_H1","STOP_TIE"}
Modes == Stops \cup {"RUN","WAIT_SEED","WAIT_H1"}
EmptyHistory == [epoch |-> -1, registry |-> <<>>, supports |-> <<>>]
Init ==
  /\ slot = ForkSlot
  /\ chains = [b \in Branches |-> InitialChain]
  /\ bitcoin \in [Es -> {0,1}] /\ bitcoin[0] = 0
  /\ blockTie = TieMap(chains)
  /\ ready = {0}
  /\ partition = TRUE /\ absent = TRUE
  /\ evidence = "NONE"
  /\ local = [n \in Nodes |->
       [seen |-> [b \in Branches |-> Len(InitialChain)], tip |-> InitialChain,
        anchor |-> <<>>, registry |-> Registry(InitialChain,0), epoch |-> 0,
        origin |-> 0, mode |-> "RUN", signed |-> -1,
        history |-> IF ForkSlot = 1
                     THEN [epoch |-> 0, registry |-> Registry(InitialChain,0),
                            supports |-> Supports(InitialChain,0)]
                     ELSE EmptyHistory]]
  /\ audit = [conditional |-> TRUE, immutable |-> TRUE, h1 |-> TRUE, bootstrap |-> TRUE,
               anchor |-> TRUE, recovery |-> TRUE]
  /\ recoveryUsed = {}

(***************************************************************************
 Delivery, full validation/replay and adoption form one atomic abstraction.
 Hidden/lost messages can be fetched later. Stuttering Fetch is excluded.
 Epoch history is a MONITOR, never an adoption guard or registry lock.
 An epoch is engaged only when an adopted block actually uses that epoch.
 ***************************************************************************)
Fetch(n) ==
  /\ Online(n)
  /\ LET seen == NewSeen(n)
         d == Decision(n,seen)
         adopts == d.adopt # {}
         c == IF adopts THEN CHOOSE x \in d.adopt: TRUE ELSE local[n].tip
         install == adopts /\ (~RuleA \/ Epoch(slot)=0 \/ Carrier(c,Epoch(slot))#0)
         e == IF install THEN Epoch(slot) ELSE local[n].epoch
         r == IF install THEN Registry(c,e) ELSE local[n].registry
         engaged == install /\ \E i \in 1..Len(c): Epoch(Slot(c[i])) = e
         old == IF local[n].history.epoch = e THEN local[n].history.registry ELSE <<>>
         updated == [local[n] EXCEPT
                        !.seen = seen, !.tip = c, !.epoch = e, !.registry = r,
                        !.mode = d.mode,
                        !.anchor = IF adopts THEN AnchorAfter(n,c) ELSE @,
                        !.history = IF engaged THEN [epoch |-> e, registry |-> r, supports |-> Supports(c,e)] ELSE @]
     IN /\ updated # local[n]
        /\ local' = [local EXCEPT ![n] = updated]
        /\ audit' = [audit EXCEPT
              !.conditional = @ /\ (~install \/ old = <<>> \/
                  local[n].history.supports # Supports(c,e) \/ old = r),
              !.immutable = @ /\ (~install \/ old = <<>> \/ old = r),
              !.h1 = @ /\ (d.adopt \subseteq BaseAdoptable(n,seen)),
              !.anchor = @ /\ (~adopts \/ IsPrefix(local[n].anchor,c))]
  /\ UNCHANGED <<blockTie,slot,chains,bitcoin,ready,partition,absent,evidence,
                  recoveryUsed>>

CanProduce(b) ==
  LET c == chains[b]
      p == Owner(c,Epoch(slot),slot)
  IN /\ Epoch(slot) \in ready
     /\ ~\E i \in 1..Len(c): Slot(c[i]) = slot
     /\ IF p = 3 THEN TRUE ELSE
           /\ Online(p)
           /\ slot # local[p].signed
           /\ local[p].seen[b] = Len(c)
           /\ c \in Maxima(local[p].seen)
           /\ ~Deep(p,c)
           /\ Decision(p,local[p].seen).mode \in {"RUN","STOP_TIE"}
Produce(b) ==
  /\ CanProduce(b)
  /\ LET p == Owner(chains[b],Epoch(slot),slot)
     IN /\ chains' = [chains EXCEPT ![b] = Append(@,Block(b,slot))]
        /\ blockTie' = [blockTie EXCEPT ![Block(b,slot)] =
                          ComputedTie(Append(chains[b],Block(b,slot)),Len(chains[b])+1)]
        /\ local' = IF p = 3 THEN local ELSE
                      [local EXCEPT ![p].signed = slot,
                                    ![p].seen[b] = Len(chains[b])+1,
                                    ![p].history = [epoch |-> Epoch(slot),
                                      registry |-> ProductionRegistry(chains[b],Epoch(slot),slot),
                                      supports |-> Supports(Candidate(chains[b],slot),Epoch(slot))]]
        /\ audit' = IF p = 3 THEN audit ELSE
             [audit EXCEPT
                 !.conditional = @ /\
                   (local[p].history.epoch # Epoch(slot) \/
                    local[p].history.supports # Supports(Candidate(chains[b],slot),Epoch(slot)) \/
                    local[p].history.registry = ProductionRegistry(chains[b],Epoch(slot),slot)),
                 !.immutable = @ /\
                 (local[p].history.epoch # Epoch(slot) \/
                  local[p].history.registry = ProductionRegistry(chains[b],Epoch(slot),slot))]
  /\ UNCHANGED <<slot,bitcoin,ready,partition,absent,evidence,recoveryUsed>>

Tick == /\ slot < LastSlot /\ slot' = slot+1
        /\ local' = [n \in Nodes |-> [local[n] EXCEPT !.signed = -1,
                        !.history = IF Epoch(slot+1) # Epoch(slot)
                                    THEN EmptyHistory ELSE @]]
        /\ UNCHANGED <<blockTie,chains,bitcoin,ready,partition,absent,evidence,
                        audit,recoveryUsed>>
Reveal == /\ ready # Es /\ ready' = Es
          /\ UNCHANGED <<blockTie,slot,chains,local,bitcoin,partition,absent,evidence,
                          audit,recoveryUsed>>
Heal == /\ partition /\ partition' = FALSE
        /\ UNCHANGED <<blockTie,slot,chains,local,bitcoin,ready,absent,evidence,
                        audit,recoveryUsed>>
Return == /\ absent /\ absent' = FALSE
          /\ UNCHANGED <<blockTie,slot,chains,local,bitcoin,ready,partition,evidence,
                          audit,recoveryUsed>>
Evidence(v) ==
  /\ v \in {"NONE","UNKNOWN","LAG"} /\ evidence # v
  \* Environment eventually settles at the finite horizon.
  /\ slot < LastSlot \/ v = "NONE"
  /\ evidence' = v
  /\ UNCHANGED <<blockTie,slot,chains,local,bitcoin,ready,partition,absent,audit,
                  recoveryUsed>>

SafetyState(n) == <<local[n],Candidates(local[n].seen),Maxima(local[n].seen)>>
Bootstrap(n) ==
  /\ local[n].origin \in {0,1,2}   \* always has a local origin, even absent/STOP
  /\ UNCHANGED <<blockTie,slot,chains,local,bitcoin,ready,partition,absent,evidence,
                  recoveryUsed>>
  /\ audit' = [audit EXCEPT !.bootstrap = @ /\ (SafetyState(n)' = SafetyState(n))]

(***************************************************************************
 ExplicitAccept is the external human act for the exact freshly prepared
 dossier <n, old safety state, target>. No timeout/BOOTSTRAP invokes it.
 At most one accepted dossier per node; atomic preparation+acceptance here
 abstracts the UI/journal protocol, not its crash/replay proof.
 ***************************************************************************)
ExplicitAccept(n,b) ==
  /\ n \notin recoveryUsed /\ Online(n)
  /\ local[n].mode = "STOP_DEEP" /\ slot = LastSlot
  /\ local[n].seen[b] = Len(chains[b])
  /\ LET c == chains[b]
         e == Epoch(slot)
         r == Registry(c,e)
     IN /\ local' = [local EXCEPT ![n].tip = c, ![n].anchor = c,
                         ![n].origin = b, ![n].registry = r, ![n].epoch = e,
                         ![n].history = EmptyHistory, ![n].mode = "RUN"]
        /\ audit' = [audit EXCEPT !.recovery = @ /\ n \notin recoveryUsed]
  /\ recoveryUsed' = recoveryUsed \cup {n}
  /\ UNCHANGED <<blockTie,slot,chains,bitcoin,ready,partition,absent,evidence>>

Next == \/ \E n \in Nodes: Fetch(n)
        \/ \E b \in Branches: Produce(b)
        \/ Tick \/ Reveal \/ Heal \/ Return
        \/ \E v \in {"NONE","UNKNOWN","LAG"}: Evidence(v)
        \/ \E n \in Nodes: Bootstrap(n)
        \/ \E n \in Nodes,b \in Branches: ExplicitAccept(n,b)

TypeOK ==
  /\ slot \in ForkSlot..LastSlot /\ bitcoin \in [Es -> {0,1}] /\ ready \subseteq Es
  /\ partition \in BOOLEAN /\ absent \in BOOLEAN
  /\ evidence \in {"NONE","UNKNOWN","LAG"}
  /\ \A b \in Branches: chains[b] \in Seq(1..(3*Base))
  /\ \A n \in Nodes:
       /\ local[n].mode \in Modes /\ local[n].epoch \in Es
       /\ local[n].registry \in [Producers -> 0..7]
       /\ local[n].origin \in {0,1,2}
       /\ \A b \in Branches: local[n].seen[b] \in 0..Len(chains[b])
  /\ recoveryUsed \subseteq Nodes

BlockMetadataCorrect == \A b \in Branches: \A i \in 1..Len(chains[b]):
                            Tie(chains[b],i) = ComputedTie(chains[b],i)

\* 1. Conditional agreement is a lemma; this does not assert common prefix.
Agreement == \A n,m \in Nodes:
  (local[n].epoch = local[m].epoch /\
   Supports(local[n].tip,local[n].epoch) = Supports(local[m].tip,local[m].epoch))
   => local[n].registry = local[m].registry

\* 2. Independent direct fold vs incremental replay, including empty epochs.
Determinism ==
  /\ \A b \in Branches,e \in Es:
         Weights(ReplayOps(chains[b],e)) = ReferenceRegistry(chains[b],e)
  /\ \A n \in Nodes:
         local[n].registry = ReferenceRegistry(local[n].tip,local[n].epoch)
  /\ \A a,b \in Branches,e \in Es:
       Supports(chains[a],e) = Supports(chains[b],e) =>
         /\ Seed(Registry(chains[a],e),e) = Seed(Registry(chains[b],e),e)
         /\ \A s \in (e*SlotsPerEpoch)..((e+1)*SlotsPerEpoch-1):
                    Owner(chains[a],e,s) = Owner(chains[b],e,s)

UpToDate(n) == /\ local[n].seen = [b \in Branches |-> Len(chains[b])]
              /\ ~ENABLED Fetch(n)
\* 3. No settled split-brain labelled RUN after the complete data are shared.
Recovery == (~partition /\ ~absent /\ Epoch(slot) \in ready /\
             evidence = "NONE" /\ \A n \in Nodes: UpToDate(n)) =>
              (local[1].tip = local[2].tip \/
               local[1].mode \in Stops \/ local[2].mode \in Stops)

\* 4. A ready, compatible honest slot has an actual production transition.
\* Missing slots/density/depth cannot create an extra production gate.
NoAccidentalHalt == \A n \in Nodes,b \in Branches:
  LET c == chains[b] IN
  (/\ Online(n) /\ Epoch(slot) \in ready
   /\ local[n].seen[b] = Len(c) /\ c \in Maxima(local[n].seen)
   /\ (\A d \in Maxima(local[n].seen): ~Deep(n,d))
   /\ (~Relevant(n,local[n].seen) \/ evidence = "NONE")
   /\ Owner(c,Epoch(slot),slot) = n /\ slot # local[n].signed
   /\ ~\E i \in 1..Len(c): Slot(c[i]) = slot)
  => ENABLED Produce(b)

\* 5/6. Transition monitors compare pre/post without restricting Next.
H1Detector == audit.h1
\* Instrumentation only: never used by guards, ranking, derivation or H1.
\* Adjacent engagements in the same epoch: unchanged authorized supports
\* imply unchanged registry. Global common-prefix safety remains an obligation.
RegistryStableOnCommonPrefix == audit.conditional
RegistryImmutable == audit.immutable
BootstrapNoEffect == audit.bootstrap
AnchorProtected == audit.anchor
RecoveryExplicit == audit.recovery

\* Fairness is environmental and local; never fairness of acceptance.
Spec == Init /\ [][Next]_vars
FairSpec == Spec /\ WF_vars(Tick) /\ WF_vars(Reveal) /\ WF_vars(Heal)
                 /\ WF_vars(Return) /\ WF_vars(Evidence("NONE"))
                 /\ \A n \in Nodes: WF_vars(Fetch(n))
ConvergedOrStopped == local[1].tip = local[2].tip \/
                      local[1].mode \in Stops \/ local[2].mode \in Stops
RecoveryProgress == <>[]ConvergedOrStopped
ResumptionProgress ==
  (slot = LastSlot /\ ~partition /\ ~absent /\ ready = Es /\ evidence = "NONE")
  ~> (\A n \in Nodes: local[n].mode \in {"RUN","STOP_TIE","STOP_DEEP"})

\* Reachability traps, checked separately with INVARIANT to obtain witnesses.
LateHonestBlock == \E b \in Branches: \E i \in 1..Len(chains[b]):
                    /\ Epoch(Slot(chains[b][i])) = 2
                    /\ Owner(Prefix(chains[b],i-1),2,Slot(chains[b][i])) \in Nodes
EmptyMiddle == \A b \in Branches: \A i \in 1..Len(chains[b]):
                   Epoch(Slot(chains[b][i])) # 1
NoEmptyEpochWitness == ~(slot = LastSlot /\ ~partition /\ ~absent /\
                         LateHonestBlock /\ EmptyMiddle)
NoEquivocationWitness == ~\E s \in ForkSlot..LastSlot:
                   /\ Block(1,s) \in {chains[1][i]: i \in 1..Len(chains[1])}
                   /\ Block(2,s) \in {chains[2][i]: i \in 1..Len(chains[2])}

NoTwoEmptyEpochsWitness == ~(~partition /\ ~absent /\ LateHonestBlock /\
                         (\A b \in Branches: \A i \in 1..Len(chains[b]):
                            Epoch(Slot(chains[b][i])) = 2))
NoRecoveryWitness == recoveryUsed = {}

(***************************************************************************
 Focused temporal suffix campaign, not the Init of MC_safe.
 Valid histories: H1 at slot 1, H2 at slot 2, Byzantine at slot 3 (possibly
 equivocation). Tests both shallow convergence and incompatible anchors.
 Environment is quiescent; no new blocks, no RECOVERY approval assumed.
 ***************************************************************************)
RecoveryInit ==
  /\ slot = LastSlot /\ bitcoin = [e \in Es |-> IF e = 0 THEN 0 ELSE 1]
  /\ chains \in {
       << <<Block(0,0),Block(1,1),Block(1,3)>>,
          <<Block(0,0),Block(2,2)>> >>,
       << <<Block(0,0),Block(1,1),Block(1,3)>>,
          <<Block(0,0),Block(2,2),Block(2,3)>> >> }
  /\ blockTie = TieMap(chains)
  /\ ready \in {{0},Es} /\ partition \in BOOLEAN /\ absent \in BOOLEAN
  /\ evidence \in {"NONE","UNKNOWN","LAG"}
  /\ local = [n \in Nodes |->
       [seen |-> [b \in Branches |-> IF b = n THEN Len(chains[b]) ELSE 1],
        tip |-> chains[n], anchor |-> Prefix(chains[n],Len(chains[n])-MaxReorg),
        registry |-> Registry(chains[n],Epoch(slot)), epoch |-> Epoch(slot),
        origin |-> 0, mode |-> "RUN", signed |-> -1, history |-> EmptyHistory]]
  /\ audit = [conditional |-> TRUE, immutable |-> TRUE, h1 |-> TRUE, bootstrap |-> TRUE,
               anchor |-> TRUE, recovery |-> TRUE]
  /\ recoveryUsed = {}
RecoveryNext == (\E n \in Nodes: Fetch(n)) \/ Heal \/ Return \/ Reveal \/ Evidence("NONE")
RecoverySpec == RecoveryInit /\ [][RecoveryNext]_vars
              /\ WF_vars(Reveal) /\ WF_vars(Heal) /\ WF_vars(Return)
              /\ WF_vars(Evidence("NONE"))
              /\ \A n \in Nodes: WF_vars(Fetch(n))
=============================================================================
