"""Run after every TLC process has completed; no original is modified."""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
comparisons=[]
for copy in sorted((P/'historical').rglob('*')):
 if not copy.is_file():continue
 rel=copy.relative_to(P/'historical')
 if rel.parts[0]=='correctif-D':original=P.parent/'modele-v0.5'/'correctif-registre'/Path(*rel.parts[1:])
 else:original=P.parent/'modele-v0.5'/rel
 comparisons.append(dict(copy=str(copy.relative_to(P)),original=str(original),exists=original.is_file(),same=original.is_file() and sha(copy)==sha(original),sha256=sha(copy)))
for rel in ['tla2tools.jar','tools/LocalTLC.java']:
 copy=P/rel;original=P.parent/'modele-v0.5'/rel
 comparisons.append(dict(copy=rel,original=str(original),exists=original.is_file(),same=original.is_file() and sha(copy)==sha(original),sha256=sha(copy)))
norm=P.parents[1]
provenance={str(p):sha(p) for p in [norm/'MANDAT-TLA-v0.6.md',norm/'N-SPEC-v0.6.md']}
(P/'INTEGRITE-ORIGINAUX.json').write_text(json.dumps(dict(comparisons=comparisons,normative_sources=provenance,note='Comparaison des copies initiales conservées aux sources actuellement présentes ; aucune assertion sur des fichiers non copiés.'),ensure_ascii=False,indent=2))
missing=[p.stem for p in P.glob('MC_*.cfg') if not (P/'logs'/(p.stem+'.json')).is_file()]
(P/'EN-ATTENTE.txt').write_text('\n'.join(sorted(missing))+ ('\n' if missing else ''))
files={str(p.relative_to(P)):sha(p) for p in sorted(P.rglob('*')) if p.is_file() and p.name not in {'SHA256.json','.run.lock'} and '__pycache__' not in p.parts}
(P/'SHA256.json').write_text(json.dumps(files,ensure_ascii=False,indent=2))
print('files:',len(files),'unrun:',len(missing),'original mismatches:',[c['copy'] for c in comparisons if not c['same']])
