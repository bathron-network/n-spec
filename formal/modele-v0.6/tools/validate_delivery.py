"""Audit the delivered evidence without rerunning the model checker."""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parents[1]
rows=json.loads((P/'RESULTATS.json').read_text())
issues=[]
for r in rows:
 log=(P/r['log']).read_text()
 if r['status']=='PASS' and not (r['exit']==0 and not r['timeout'] and r['queue']==0 and 'Model checking completed. No error has been found.' in log):issues.append((r['name'],'invalid PASS'))
 if r['status'] in {'FAIL','TÉMOIN'} and not (r['exit']==12 and r['violations'] and not r['timeout']):issues.append((r['name'],'invalid counterexample'))
 for source,expected in r.get('input_sha256',{}).items():
  if source=='run.py':continue # queued driver vs file on disk; command recorded separately
  f=P/source
  if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest()!=expected:issues.append((r['name'],'source changed: '+source))
for cfg in P.glob('MC_*.cfg'):
 if not (P/'logs'/(cfg.stem+'.json')).exists():issues.append((cfg.stem,'missing execution record'))
for href in re.findall(r'\]\(([^)]+)\)',(P/'RAPPORT-TLA-N-v0.6.md').read_text()):
 if not (P/href).exists():issues.append(('report','missing link '+href))
mut=json.loads((P/'MUTATIONS.json').read_text())
if len(mut)!=13 or not all(r['sensitive'] for r in mut):issues.append(('mutations','not all 13 detected'))
integrity=json.loads((P/'INTEGRITE-ORIGINAUX.json').read_text())
if not all(r['same'] for r in integrity['comparisons']):issues.append(('historical','copy mismatch'))
result=dict(execution_records=len(rows),all_configs_executed=not any(i[1]=='missing execution record' for i in issues),mutation_controls=sum(r['sensitive'] for r in mut),issues=issues,note='Checks evidence consistency, not completeness of the protocol model. INCOMPLET and declared NT remain unresolved.')
(P/'VALIDATION-LIVRAISON.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(bool(issues))
