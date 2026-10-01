from pathlib import Path
P=Path(__file__).resolve().parents[1]
s=(P/'RegistryModelFast.tla').read_text().replace('MODULE RegistryModelFast','MODULE RegistryModelFast2')
a=s.index('\nRegistry(c,e) ==')+1;b=s.index('Weight(r) ==',a)
s=s[:a]+'''Registry(c,e) == IF BrokenTipSnapshot /\\ e>0 THEN Weights(Ops(c))
 ELSE IF Support(c,e)= <<>> THEN InitialWeights ELSE Weights(Ops(Support(c,e)))
'''+s[b:]
(P/'RegistryModelFast2.tla').write_text(s)
for k in (1,2,4):
 base=f'MC_support_equivalence_{k}';name=f'MC_registry_equivalence_{k}'
 t=(P/(base+'.tla')).read_text().replace('MODULE '+base,'MODULE '+name).replace('EXTENDS RegistryModelFast','EXTENDS RegistryModelFast2')
 t=t.replace('Equivalent ==', 'RegistryEquivalent == \\A c\\in Universe,e\\in Es:Registry(c,e)=Weights(ReplayOps(c,e))\nEquivalent ==')
 (P/(name+'.tla')).write_text(t)
 (P/(name+'.cfg')).write_text((P/(base+'.cfg')).read_text().replace('INVARIANTS Equivalent','INVARIANTS Equivalent RegistryEquivalent'))
for f in P.glob('MC_*.tla'):
 if (P/'logs'/(f.stem+'.log')).exists() or 'equivalence' in f.stem:continue
 t=f.read_text()
 if 'EXTENDS RegistryModelFast\n' in t:f.write_text(t.replace('EXTENDS RegistryModelFast\n','EXTENDS RegistryModelFast2\n'))
