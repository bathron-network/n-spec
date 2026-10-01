"""Normalize TLC counters (including French thin spaces), retain incomplete runs."""
import hashlib,json,re
from pathlib import Path
P=Path(__file__).resolve().parents[1]
results=[]
for f in sorted((P/'logs').glob('MC_*.json')):
 if f.name.endswith('.interruption.json'):continue
 r=json.loads(f.read_text())
 if 'name' not in r:continue
 log=(P/r['log']).read_text().replace('\u202f','').replace('\u00a0','')
 final=re.findall(r'([\d,]+) states generated, ([\d,]+) distinct states found, ([\d,]+) states left on queue',log)
 progress=re.findall(r'Progress\((\d+)\) at ([^\n]+?): ([\d,]+) states generated.*?, ([\d,]+) distinct states found.*?, ([\d,]+) states left on queue',log)
 if final:
  r.update(zip(['generated','distinct','queue'],[int(x.replace(',','')) for x in final[-1]]));r['counters']='final'
 elif progress:
  d,t,g,s,q=progress[-1];r.update(generated=int(g.replace(',','')),distinct=int(s.replace(',','')),queue=int(q.replace(',','')),depth=int(d),counters='last_progress',last_progress=t)
 else:r['counters']='unavailable'
 r['mode']='BFS-checkpoint' if 'previous_segment' in r else 'replay' if 'SPECIFICATION Replay' in r['configuration'] else 'BFS'
 command=re.search(r'^COMMAND (.*)$',log,re.M)
 r['executed_command']=json.loads(command.group(1)) if command else None
 if 'input_sha256' in r:r['hash_scope']='Files on disk when this run began; a queued Python process may have loaded an earlier runner before acquiring the lock. The executed Java command is authoritative. TLA modules/configuration/JAR were read for this run.'
 fp=re.search(r'with fp (\d+) and seed',log)
 r['fingerprint_index']=int(fp.group(1)) if fp else None
 r['configuration_sha256']=hashlib.sha256(r['configuration'].encode()).hexdigest()
 r['trace_states']=len(re.findall(r'^State \d+:',log,re.M))
 r['error_messages']=re.findall(r'^Error: (.*)',log,re.M)
 if r['status']=='INCOMPLET':r['reason']='timeout' if r['timeout'] else 'tool_or_model_error'
 elif r['status']=='FAIL':r['reason']='invariant_counterexample'
 elif r['status']=='TÉMOIN':r['reason']='existence_trap_reached'
 else:r['reason']='exhausted_bounded_graph' if r['mode']=='BFS' else 'replay_completed'
 # First-pass models with ambiguous boolean assignments remain development artifacts.
 r['development']=not r['name'].endswith('_checked') and any('module '+m+'\n' in log for m in ['Brake','H1Orders','RegistryWindow','RegistryCommitments','AnchorBTC','Money','Admissions','Authorities','Persistence'])
 if r['name'].startswith(('MC_mirror_off_','MC_mirror_on_','MC_replay_spec')) and not r['name'].endswith('_core'):r['development']=True
 if r['name'] in {'MC_replay_closure_checked','MC_replay_anchor_split_checked'}:r['development']=True
 r['source_modules']=re.findall(r'Parsing file .*/([^/\n]+\.tla)',log)
 results.append(r)
(P/'RESULTATS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
header='| Run | Résultat | Code | Générés | Distincts | Profondeur | File | Durée s | Propriété violée / motif |\n|---|---|---:|---:|---:|---:|---:|---:|---|\n'
lines=[]
for r in results:
 counter_note=' (dernier point publié)' if r['counters']=='last_progress' else ''
 lines.append(f"| [{r['name']}]({r['log']}) | {r['status']}{' (développement)' if r['development'] else ''} | {r['exit']} | {r['generated']} | {r['distinct']} | {r['depth']} | {r['queue']}{counter_note} | {r['seconds']} | {', '.join(r['violations']) or r['reason']} |")
(P/'RESULTATS-DETAILLES.md').write_text('# Résultats bruts et provenance\n\nLes valeurs `None` sont indisponibles. En timeout, les compteurs peuvent être ceux du dernier point publié, pas ceux de l’arrêt. Un PASS de développement ne qualifie pas la version corrigée. Les constantes, propriétés, empreintes TLC et motifs complets figurent dans RESULTATS.json et les .cfg.\n\n'+header+'\n'.join(lines)+'\n')
print('runs',len(results),'final',len([r for r in results if not r['development']]))
