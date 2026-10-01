from pathlib import Path
P=Path(__file__).resolve().parent
old=P.parent/'modele-v0.5'
s=(old/'correctif-registre/NModel_v06.tla').read_text().replace('MODULE NModel_v06','MODULE RegistryModel')
s=s.replace('BrokenTipSnapshot, BrokenH1Promote','BrokenTipSnapshot, BrokenH1Promote, RuleA')
a=s.index('Support(c,e) =='); b=s.index('Supports(c,e)',a)
s=s[:a]+r'''\* Public maturity is reduced to epoch start; first carrier is branch-derived.
\* Separate RegistryWindow campaign explores delayed/withheld carriers.
RawSupport(c,e) == IF e = 0 \/ Cut(e) <= 0 THEN <<>>
                   ELSE SelectSeq(c,LAMBDA x: Slot(x) < Cut(e))
Carrier(c,e) == LET ks == {i \in 1..Len(c): Slot(c[i]) >= e*SlotsPerEpoch}
                IN IF ks = {} THEN 0 ELSE CHOOSE i \in ks: \A j \in ks: i <= j
WindowCount(c,e) == IF Carrier(c,e) = 0 THEN 0 ELSE
    Cardinality({i \in 1..Carrier(c,e): Slot(c[i]) >= Cut(e)})
RECURSIVE Support(_, _)
Support(c,e) == IF e = 0 THEN <<>>
  ELSE IF ~RuleA \/ (Carrier(c,e) # 0 /\ WindowCount(c,e) >= MaxReorg)
       THEN RawSupport(c,e) ELSE Support(c,e-1)
''' +s[b:]
s=s.replace('Owner(c,e,s) == LET r == Registry(c,e)',r'''Candidate(c,s) == IF Len(c)>0 /\ Slot(c[Len(c)])=s THEN c
                  ELSE Append(c,Block(0,s))
ProductionRegistry(c,e,s) == Registry(Candidate(c,s),e)
Owner(c,e,s) == LET r == ProductionRegistry(c,e,s)''')
s=s.replace('r == Registry(Prefix(c,i-1),e)','r == Registry(Prefix(c,i),e)')
s=s.replace('Registry(chains[b],Epoch(slot))','ProductionRegistry(chains[b],Epoch(slot),slot)')
s=s.replace('Supports(chains[b],Epoch(slot))','Supports(Candidate(chains[b],slot),Epoch(slot))')
s=s.replace('N-SPEC proposed v0.6: conditional registry guarantee; protocol unchanged.','N-SPEC v0.6 registry A mirror. Other submachines inherited v0.5.\n This is a focused mirror, NOT a claim of integrated v0.6 conformance.')
(P/'RegistryModel.tla').write_text(s)
base=(old/'MC_spec_registryreorg.cfg').read_text().replace('INVARIANTS TypeOK RegistryImmutable','INVARIANTS TypeOK RegistryImmutable RegistryStableOnCommonPrefix BlockMetadataCorrect')
for on in (False,True):
 tag='on' if on else 'off'
 for b1 in range(2):
  for b2 in range(2):
   name=f'MC_mirror_{tag}_{b1}{b2}'
   (P/(name+'.tla')).write_text(f'''---- MODULE {name} ----
EXTENDS RegistryModel
ShardInit == Init /\\ bitcoin = (0 :> 0 @@ 1 :> {b1} @@ 2 :> {b2})
ShardSpec == ShardInit /\\ [][Next]_vars
====
''')
   (P/(name+'.cfg')).write_text(base.replace('SPECIFICATION Spec','SPECIFICATION ShardSpec')+f'CONSTANT RuleA = {str(on).upper()}\n')
 for replay in ('spec','spec_adopt'):
  name=f'MC_replay_{replay}_{tag}'
  (P/(name+'.tla')).write_text((old/f'MC_replay_{replay}.tla').read_text().replace(f'MODULE MC_replay_{replay}',f'MODULE {name}').replace('EXTENDS NModel','EXTENDS RegistryModel'))
  (P/(name+'.cfg')).write_text((old/f'MC_replay_{replay}.cfg').read_text().replace('INVARIANTS TypeOK RegistryImmutable','INVARIANTS TypeOK RegistryImmutable RegistryStableOnCommonPrefix BlockMetadataCorrect')+f'CONSTANT RuleA = {str(on).upper()}\n')
