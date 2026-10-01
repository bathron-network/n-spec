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
label=os.getenv('TLC_RUN_LABEL','')
if label and not re.fullmatch(r'[A-Za-z0-9_-]+',label): raise SystemExit('invalid run label')
output=P/'logs'/'reproductions'/label if label else P/'logs'
output.mkdir(parents=True,exist_ok=True)
for name in sys.argv[1:]:
 if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',name): raise SystemExit('invalid module')
 logpath=output/f'{name}.log'
 if logpath.exists(): raise SystemExit(f'Preserving existing run: {name}')
 started=time.monotonic();timeout=False;tool_abort=False
 sources={Path(name+'.cfg'),Path('run.py'),Path('tools/LocalTLC.java'),Path('tla2tools.jar')}
 todo=[Path(name+'.tla')]
 while todo:
  source=todo.pop()
  if source in sources: continue
  sources.add(source)
  for imports in re.findall(r'^EXTENDS ([\w, ]+)',source.read_text(),re.M):
   todo.extend(Path(m.strip()+'.tla') for m in imports.split(',') if Path(m.strip()+'.tla').is_file())
 hashes={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(sources)}
 with tempfile.TemporaryDirectory(prefix='n-v06-') as d, logpath.open('w') as out:
  compile=subprocess.run([java.removesuffix('java')+'javac','-cp','tla2tools.jar','-d',d,'tools/LocalTLC.java'],stdout=out,stderr=subprocess.STDOUT)
  if compile.returncode: rc=compile.returncode
  else:
   cmd=[java,'-XX:+UseParallelGC','-Xmx3g','-Djava.io.tmpdir='+d,'-cp',d+':tla2tools.jar','LocalTLC','-workers',str(workers),'-seed','1','-fp','0','-metadir',d+'/states','-config',name+'.cfg',name+'.tla']
   out.write('COMMAND '+json.dumps(cmd)+'\n');out.flush()
   p=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
   fatal_since=None
   while p.poll() is None:
    now=time.monotonic()
    tail=logpath.read_text()[-65536:]
    fatal=('Successor state is not completely specified' in tail or 'Semantic errors:' in tail or 'Parsing or semantic analysis failed' in tail)
    if fatal and fatal_since is None: fatal_since=now
    timeout=now-started>=569
    tool_abort=fatal_since is not None and now-fatal_since>=2
    if timeout or tool_abort:
     os.killpg(p.pid,signal.SIGTERM)
     try:p.wait(timeout=0.5)
     except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
     out.write('\nRUN INTERRUPTED => INCOMPLET: '+('570s ceiling (569s safety margin)' if timeout else 'fatal tool/model error')+'\n')
     break
    try:p.wait(timeout=0.2)
    except subprocess.TimeoutExpired:pass
   rc=p.returncode
  out.write(f'\nexit={rc}\n')
 log=logpath.read_text().replace('\u202f','').replace('\u00a0','');violations=re.findall(r'Invariant (\w+) is violated',log)
 complete='Model checking completed. No error has been found.' in log
 status='INCOMPLET' if timeout or tool_abort else 'FAIL' if rc==12 and violations else 'PASS' if rc==0 and complete else 'INCOMPLET'
 if not (timeout or tool_abort) and rc==12 and violations and all(v.startswith('NoWitness') for v in violations):status='TÉMOIN'
 stats=re.findall(r'([\d,]+) states generated, ([\d,]+) distinct states found, ([\d,]+) states left on queue',log)
 if not stats:stats=re.findall(r'Progress\([^)]*\).*?: ([\d,]+) states generated.*?, ([\d,]+) distinct states found.*?, ([\d,]+) states left on queue',log)
 depth=re.findall(r'The depth of the complete state graph search is (\d+)',log)
 cfg=Path(name+'.cfg').read_text()
 r=dict(name=name,status=status,exit=rc,timeout=timeout,seconds=round(time.monotonic()-started,2),workers=workers,heap='3g',limit_seconds=570,mode='BFS',violations=violations,generated=int(stats[-1][0].replace(',','')) if stats else None,distinct=int(stats[-1][1].replace(',','')) if stats else None,queue=int(stats[-1][2].replace(',','')) if stats else None,depth=int(depth[-1]) if depth else None,configuration=cfg,collision=[l for l in log.splitlines() if 'val =' in l or 'collision' in l],log=str(logpath.relative_to(P)))
 r.update(tool_abort=tool_abort,input_sha256=hashes)
 (output/f'{name}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
 print(json.dumps(r,ensure_ascii=False),flush=True)
 if violations:
  at=log.find('Error: Invariant')
  trace_dir=P/'traces'/'reproductions'/label if label else P/'traces'
  trace_dir.mkdir(parents=True,exist_ok=True)
  (trace_dir/f'{name}.txt').write_text(log[at:])
