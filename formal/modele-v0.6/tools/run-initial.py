#!/usr/bin/env python3
"""One local TLC at a time, 3 GiB, <=4 workers, hard 570 second deadline."""
import fcntl,hashlib,json,os,re,signal,subprocess,sys,tempfile,time
from pathlib import Path
P=Path(__file__).resolve().parent
os.chdir(P)
java='/opt/homebrew/opt/openjdk@21/bin/java'
workers=int(os.getenv('TLC_WORKERS','4'))
if not 1<=workers<=4: raise SystemExit('workers must be 1..4')
lock=open(P/'logs/.run.lock','w');fcntl.flock(lock,fcntl.LOCK_EX)
for name in sys.argv[1:]:
 if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',name): raise SystemExit('invalid module')
 logpath=P/'logs'/f'{name}.log'
 if logpath.exists(): raise SystemExit(f'Preserving existing run: {name}')
 started=time.monotonic();timeout=False
 with tempfile.TemporaryDirectory(prefix='n-v06-') as d, logpath.open('w') as out:
  compile=subprocess.run([java.removesuffix('java')+'javac','-cp','tla2tools.jar','-d',d,'tools/LocalTLC.java'],stdout=out,stderr=subprocess.STDOUT)
  if compile.returncode: rc=compile.returncode
  else:
   cmd=[java,'-XX:+UseParallelGC','-Xmx3g','-Djava.io.tmpdir='+d,'-cp',d+':tla2tools.jar','LocalTLC','-workers',str(workers),'-seed','1','-metadir',d+'/states','-config',name+'.cfg',name+'.tla']
   out.write('COMMAND '+json.dumps(cmd)+'\n');out.flush()
   p=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
   try: rc=p.wait(timeout=max(1,570-(time.monotonic()-started)))
   except subprocess.TimeoutExpired:
    timeout=True;os.killpg(p.pid,signal.SIGTERM)
    try:p.wait(timeout=1)
    except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
    rc=p.returncode;out.write('\nTIMEOUT 570s => INCOMPLET\n')
  out.write(f'\nexit={rc}\n')
 log=logpath.read_text().replace('\u202f','').replace('\u00a0','');violations=re.findall(r'Invariant (\w+) is violated',log)
 complete='Model checking completed. No error has been found.' in log
 status='INCOMPLET' if timeout else 'FAIL' if rc==12 and violations else 'PASS' if rc==0 and complete else 'INCOMPLET'
 if violations and all(v.startswith('NoWitness') for v in violations):status='TÉMOIN'
 stats=re.findall(r'([\d,]+) states generated, ([\d,]+) distinct states found, ([\d,]+) states left on queue',log)
 if not stats:stats=re.findall(r'Progress\([^)]*\).*?: ([\d,]+) states generated.*?, ([\d,]+) distinct states found.*?, ([\d,]+) states left on queue',log)
 depth=re.findall(r'The depth of the complete state graph search is (\d+)',log)
 cfg=Path(name+'.cfg').read_text()
 r=dict(name=name,status=status,exit=rc,timeout=timeout,seconds=round(time.monotonic()-started,2),workers=workers,heap='3g',limit_seconds=570,mode='BFS',violations=violations,generated=int(stats[-1][0].replace(',','')) if stats else None,distinct=int(stats[-1][1].replace(',','')) if stats else None,queue=int(stats[-1][2].replace(',','')) if stats else None,depth=int(depth[-1]) if depth else None,configuration=cfg,collision=[l for l in log.splitlines() if 'val =' in l or 'collision' in l],log=str(logpath.relative_to(P)))
 (P/'logs'/f'{name}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
 print(json.dumps(r,ensure_ascii=False),flush=True)
 if violations:
  at=log.find('Error: Invariant'); (P/'traces'/f'{name}.txt').write_text(log[at:])
