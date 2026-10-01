#!/usr/bin/env python3
"""Invoke the delivered launcher unchanged; archive its results here."""
from pathlib import Path
import json,os,subprocess,shutil
p=Path(__file__).resolve().parent.parent
out=p/'lemme-L1';label='lemme_L1_codex'
env=dict(os.environ,TLC_RUN_LABEL=label)
for name in json.loads((out/'campaign.json').read_text()):
 result=p/'logs/reproductions'/label/(name+'.json')
 if not result.exists():
  subprocess.run(['./run.sh',name],cwd=p,env=env,check=True)
 for ext in ['json','log']:
  f=p/'logs/reproductions'/label/(name+'.'+ext)
  if f.exists(): shutil.copy2(f,out/f.name)
 f=p/'traces/reproductions'/label/(name+'.txt')
 if f.exists():shutil.copy2(f,out/f.name)
