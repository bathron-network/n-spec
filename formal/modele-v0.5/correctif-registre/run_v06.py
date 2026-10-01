#!/usr/bin/env python3
"""Run unchanged run.sh; enforce 570 s per run, preserve exit/timeout evidence."""
import os, signal, subprocess, time, json, re, hashlib
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)
names=['MC_replay_spec_adopt_v06','MC_replay_spec_adopt_strong_v06','MC_replay_spec_strong_v06','MC_broken_tipsnapshot_v06','MC_broken_h1promote_v06','MC_witness_empty_v06','MC_witness_twoempty_v06','MC_live_v06','MC_safe_v06','MC_spec_registryreorg_strong_v06','MC_spec_registryreorg_v06']
results=[]
for name in names:
 start=time.monotonic()
 p=subprocess.Popen(['./run.sh',name],env={**os.environ,'TLC_WORKERS':'4'},start_new_session=True)
 timeout=False
 try: rc=p.wait(timeout=570)
 except subprocess.TimeoutExpired:
  timeout=True
  os.killpg(p.pid,signal.SIGTERM)
  try: p.wait(timeout=2)
  except subprocess.TimeoutExpired: os.killpg(p.pid,signal.SIGKILL); p.wait()
  rc=p.returncode
  with open('logs/'+name+'.log','a') as f: f.write('\nRUNNER_TIMEOUT=570s; NOT A PASS\n')
 log=Path('logs/'+name+'.log').read_text()
 result={'name':name,'exit':rc,'timeout':timeout,'seconds':round(time.monotonic()-start,2),'completed': 'Model checking completed. No error has been found.' in log,'invariant_violations':re.findall(r'Invariant (\w+) is violated',log),'statistics':re.findall(r'[\d,]+ states generated, [\d,]+ distinct states found, [\d,]+ states left on queue\.',log)[-1:], 'depth':re.findall(r'The depth of the complete state graph search is (\d+)',log)[-1:]}
 results.append(result)
 Path('logs/RESULTATS_v06.json').write_text(json.dumps(results,indent=2))
 print(json.dumps(result),flush=True)
paths=[Path('NModel_v06.tla'),Path('run.sh'),Path('run_v06.py'),Path('tla2tools.jar'),Path('tools/LocalTLC.java')]+list(Path('.').glob('MC_*v06.*'))+list(Path('logs').glob('*v06.log'))
Path('logs/SHA256_v06.json').write_text(json.dumps({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()},indent=2))
