"""Preserve first-pass modules; make boolean monitor RHS explicit (TLA precedence)."""
from pathlib import Path
import re
P=Path(__file__).resolve().parent
modules=['H1Orders','Brake','RegistryWindow','RegistryCommitments','AnchorBTC','Money','Admissions','Authorities']
for m in modules:
 s=(P/(m+'.tla')).read_text().replace('MODULE '+m,'MODULE '+m+'Checked')
 def wrap(match):
  prefix,rhs=match.groups()
  return prefix+'('+rhs+')' if not rhs.rstrip().endswith('/\\') else prefix+rhs
 s=re.sub(r"(?m)^(\s*/\\ (?:audit|everSlow|released|signed)'=)([^\n]+)$",wrap,s)
 s=s.replace("audit'=audit /\\ chosen=expected", "audit'=(audit /\\ chosen=expected")
 s=s.replace('(unchanged=>k=0) /\\ (h \\/ \\A i\\in chosen: Eligible(st,i,c,cal))','(unchanged=>k=0) /\\ (h \\/ \\A i\\in chosen: Eligible(st,i,c,cal)))')
 (P/(m+'Checked.tla')).write_text(s)
names=[]
for f in sorted(P.glob('MC_*.tla')):
 if f.stem.endswith('_checked'):continue
 s=f.read_text();modified=False
 for m in modules:
  if re.search(r'EXTENDS '+m+r'\b',s):
   s=s.replace('EXTENDS '+m,'EXTENDS '+m+'Checked');modified=True
 if not modified:continue
 name=f.stem+'_checked';s=s.replace('MODULE '+f.stem,'MODULE '+name)
 (P/(name+'.tla')).write_text(s);(P/(name+'.cfg')).write_text(f.with_suffix('.cfg').read_text());names.append(name)
(P/'campaign-checked.txt').write_text('\n'.join(names)+'\n')
