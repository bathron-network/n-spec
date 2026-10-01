"""Independent readable reference of the reduced temporal-window brake scenario."""
import json
from pathlib import Path
weights=[680,120,190,5,5]
st=[dict(state='ACTIVE',reset=0,susp=-1,queue=-1) for _ in weights]
cal={0}; wf=[1000];used=[0];slow=[0];rows=[]
def canon(i,s):return i==0 and (s//5)%3<2
def samples(i,a,b):return [s for s in range(a,b+1) if s in cal and s%5==i]
def present(i,a,b):
 ss=samples(i,a,b);cc=sum(canon(i,s) for s in ss)
 return 2*cc>=len(ss) and 3*cc>=len(ss)
for e in range(1,21):
 c=e*5-1
 for s in range(1 if e==1 else (e-1)*5,c+1):
  if st[s%5]['state']!='EXCLUDED':cal.add(s)
  for i,x in enumerate(st):
   if x['state']=='SUSPECT' and s-x['susp']>=10 and len(samples(i,x['susp']+1,s))>=2:
    if present(i,x['susp']+1,s):x.update(state='ACTIVE',reset=s,susp=-1)
    else:x.update(state='QUEUED',queue=s)
   elif x['state']=='QUEUED' and s-9>x['queue'] and len(samples(i,s-9,s))>=2 and present(i,s-9,s):
    x.update(state='ACTIVE',reset=s,susp=-1,queue=-1)
   elif x['state']=='ACTIVE' and s-34>x['reset'] and len(samples(i,s-34,s))>=4 and not present(i,s-34,s):
    x.update(state='SUSPECT',susp=s)
 Q={i for i,x in enumerate(st) if x['state']=='QUEUED'}
 hs=[]
 for j in range(e-3,e):
  ss=[s for s in range(j*5,j*5+5) if s in cal and s%5 not in Q]
  hs.append(bool(ss) and 10*sum(canon(s%5,s) for s in ss)>=7*len(ss))
 health=e>=3 and all(hs)
 w=sum(x for i,x in enumerate(weights) if st[i]['state']!='EXCLUDED');wf.append(w)
 base=min(wf[max(0,e-6):e+1]);u=sum(used[max(0,e-6):e]);su=sum(slow[max(0,e-6):e])
 budget=min(2*w//100,max(0,5*base//100-u))
 if not health:budget=min(budget,max(0,base//100-su))
 remaining=budget;chosen=[]
 for i in sorted(Q,key=lambda i:(st[i]['queue'],i)):
  ss=samples(i,c-34,c)
  eligible=c-34>st[i]['reset'] and len(ss)>=4 and not any(canon(i,s) or (i==4 and s==44) for s in ss)
  if not health and not eligible:continue
  if weights[i]>remaining or weights[i]>=w:continue
  chosen.append(i+1);remaining-=weights[i];w-=weights[i];st[i]['state']='EXCLUDED'
 k=budget-remaining;used.append(k);slow.append(0 if health else k)
 rows.append(dict(epoch=e,cutoff=c,Q=[i+1 for i in sorted(Q)],health=health,weight=wf[-1],base=base,budget=budget,excluded=chosen,slow_weight=slow[-1],rotation=e==10))
Path(__file__).resolve().parents[1].joinpath('logs/brake-reference.json').write_text(json.dumps(rows,indent=2))
print(json.dumps([r for r in rows if r['excluded'] or r['rotation']],indent=2))
