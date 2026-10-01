from pathlib import Path
P=Path(__file__).resolve().parents[1]
s=(P/'RegistryModelV6.tla').read_text().replace('MODULE RegistryModelV6','MODULE RegistryModelFast')
start=s.index('RECURSIVE Support(_, _)');end=s.index('Supports(c,e)',start)
reference=s[start:end].replace('Support','ReferenceSupport').replace('RawReferenceSupport','RawSupport')
s=s.replace('Support(c,e) == IF e = 0 THEN <<>>','Support(c,e) == IF e = 0 \\/ Cut(e)<=0 THEN <<>>\n  ELSE IF RuleA /\\ Len(c)<MaxReorg THEN Support(c,e-1)')
s=s.replace('Supports(c,e) ==',reference+'\nSupports(c,e) ==')
(P/'RegistryModelFast.tla').write_text(s)
for k in (1,2,4):
 name=f'MC_support_equivalence_{k}'
 (P/(name+'.tla')).write_text('''---- MODULE __NAME__ ----
EXTENDS RegistryModelFast
AllSlots == 0..EndSlot
Full(b) == [i\\in 1..(EndSlot+1)|->Block(b,i-1)]
Universe == UNION {{SelectSeq(Full(b),LAMBDA x: Slot(x)\\in ss):ss\\in SUBSET AllSlots}:b\\in Branches}
Equivalent == \\A c\\in Universe,e\\in Es:Support(c,e)=ReferenceSupport(c,e)
Static == Init /\\ [][UNCHANGED vars]_vars
====
'''.replace('__NAME__',name))
 cfg=(P/'MC_v6_mirror_on_00.cfg').read_text().replace('SPECIFICATION ShardSpec','SPECIFICATION Static').replace('MaxReorg = 4',f'MaxReorg = {k}').replace('TypeOK RegistryImmutable RegistryStableOnCommonPrefix','Equivalent')
 (P/(name+'.cfg')).write_text(cfg)
for v in ('00','01','10','11'):
 for on in (False,True):
  tag='on' if on else 'off';name=f'MC_fast_{tag}_{v}'
  (P/(name+'.tla')).write_text((P/f'MC_mirror_{tag}_{v}.tla').read_text().replace('MODULE MC_mirror_'+tag+'_'+v,'MODULE '+name).replace('EXTENDS RegistryModel','EXTENDS RegistryModelFast'))
  (P/(name+'.cfg')).write_text((P/f'MC_mirror_{tag}_{v}.cfg').read_text().replace(' BlockMetadataCorrect',''))
