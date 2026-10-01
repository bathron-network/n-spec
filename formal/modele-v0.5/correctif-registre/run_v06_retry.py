#!/usr/bin/env python3
"""Retry the expensive b10 partition with eight workers; same model and bounds."""
import os,signal,subprocess,time,json,re,hashlib
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)
results=[]
for b1 in [1]:
 for b2 in [0]:
  name=f'MC_spec_registryreorg_b{b1}{b2}_w8_v06'
  Path(name+'.tla').write_text(f'''---------------- MODULE {name} ----------------
EXTENDS NModel_v06
ShardInit == Init /\\ bitcoin = (0 :> 0 @@ 1 :> {b1} @@ 2 :> {b2})
ShardSpec == ShardInit /\\ [][Next]_vars
====================================================================
''')
  Path(name+'.cfg').write_text(Path('MC_spec_registryreorg_v06.cfg').read_text().replace('SPECIFICATION Spec','SPECIFICATION ShardSpec'))
  start=time.monotonic()
  p=subprocess.Popen(['./run.sh',name],env={**os.environ,'TLC_WORKERS':'8'},start_new_session=True)
  timeout=False
  try: rc=p.wait(timeout=570)
  except subprocess.TimeoutExpired:
   timeout=True;os.killpg(p.pid,signal.SIGTERM)
   try: p.wait(timeout=2)
   except subprocess.TimeoutExpired: os.killpg(p.pid,signal.SIGKILL);p.wait()
   rc=p.returncode
   with open('logs/'+name+'.log','a') as f:f.write('\nRUNNER_TIMEOUT=570s; NOT A PASS\n')
  log=Path('logs/'+name+'.log').read_text()
  result={'name':name,'bitcoin':[0,b1,b2],'exit':rc,'timeout':timeout,'seconds':round(time.monotonic()-start,2),'completed':'Model checking completed. No error has been found.' in log,'invariant_violations':re.findall(r'Invariant (\w+) is violated',log),'statistics':re.findall(r'[\d,]+ states generated, [\d,]+ distinct states found, [\d,]+ states left on queue\.',log)[-1:],'depth':re.findall(r'The depth of the complete state graph search is (\d+)',log)[-1:]}
  results.append(result);Path('logs/RESULTATS_retry_v06.json').write_text(json.dumps(results,indent=2));print(json.dumps(result),flush=True)
