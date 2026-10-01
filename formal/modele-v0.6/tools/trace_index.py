from pathlib import Path
import json,re
P=Path(__file__).resolve().parents[1]
rows=json.loads((P/'RESULTATS.json').read_text())
lines=['# Traces et témoins lisibles','', 'Les traces brutes gardent tous les champs et les actions TLC. Les états du tableau comptent les états imprimés de la trace, et non la taille du graphe exploré. Un témoin est un échec volontaire de NoWitness…, distinct d’un invariant normatif. Les premiers essais de développement sont exclus de cet index, mais conservés sur disque.','', '| Campagne | Statut | Propriété | États de trace | Lecture brute |','|---|---|---|---:|---|']
for r in rows:
 path=P/'traces'/(r['name']+'.txt')
 if r['development'] or not path.exists():continue
 content=path.read_text();states=re.findall(r'^State (\d+):',content,re.M)
 lines.append(f"| {r['name']} | {r['status']} | {', '.join(r['violations'])} | {len(states) if states else 'NP (initial)'} | [trace](traces/{path.name}) |")
lines+=['','## Parcours des contre-exemples de production A active','', 'Les numéros de ligne d’action dans la trace renvoient aux sources livrées. Les registres et préfixes complets sont conservés dans chaque état brut.']
for name in ['MC_replay_general_k1','MC_replay_general_k2','MC_min_general_k1','MC_min_general_k2','MC_replay_audit_cp','MC_replay_audit_min_k1']:
 path=P/'traces'/(name+'.txt')
 if not path.exists():continue
 lines+=['', '### '+name,'','| État | Action | Slot |','|---:|---|---:|']
 for match in re.finditer(r'^State (\d+): <([^\n]+)>\n(.*?)(?=^State \d+:|\Z)',path.read_text(),re.M|re.S):
  index,action,body=match.groups();slot=re.search(r'^/\\ slot = (\d+)',body,re.M)
  lines.append(f'| {index} | {action.split(" line ")[0]} | {slot.group(1) if slot else "—"} |')
(P/'TRACES-LECTURE.md').write_text('\n'.join(lines)+'\n')
