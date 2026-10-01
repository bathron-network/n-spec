from pathlib import Path
import hashlib,json,shutil,re
out=Path(__file__).resolve().parent;p=out.parent
rows=[]
for name in json.loads((out/'campaign.json').read_text()):
 src=p/'logs/reproductions/lemme_L1_codex'
 for ext in ['log','json']:
  f=src/(name+'.'+ext)
  if f.exists():shutil.copy2(f,out/f.name)
 f=p/'traces/reproductions/lemme_L1_codex'/(name+'.txt')
 if f.exists():shutil.copy2(f,out/f.name)
 f=out/(name+'.json')
 if not f.exists():raise SystemExit('Still pending: '+name)
 rows.append(json.loads(f.read_text()))
(out/'RESULTATS.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
lines=['| Sonde | Statut | États distincts | Durée (s) |','|---|---|---:|---:|']
for d in rows:lines.append(f"| `{d['name']}` | {d['status']} | {d['distinct']} | {d['seconds']} |")
lines+=['','Les PASS des replays sont limités au chemin fixé. Les explorations interrompues restent INCOMPLET, indépendamment des invariants non violés jusque-là. Pour INCOMPLET, les compteurs proviennent du dernier relevé TLC disponible. La première tentative interrompue est conservée en plus de ce tableau.']
table='\n'.join(lines)
(out/'RESULTATS.md').write_text(table+'\n')
r=p.parent.parent/'cp-reg/LEMME-L1-codex.md'
s=r.read_text();s=s.replace('<!-- RESULTS_L1 -->',table);r.write_text(s)
original=json.loads((out/'originals-before.json').read_text())
bad=[n for n,h in original.items() if hashlib.sha256((p/n).read_bytes()).hexdigest()!=h]
(out/'integrity.json').write_text(json.dumps({'original_files_checked':len(original),'modified_original_files':bad},indent=2))
assert not bad,bad
print(table)
