#!/usr/bin/env python3
"""Reproducible bounded-CPU campaign. No network calls; no git operations."""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import multiprocessing as mp
import os
from pathlib import Path
import platform
import resource
import sys
import time

# Set these BEFORE importing numpy in every spawned process.
for variable in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[variable] = '1'
import numpy as np
from model import (BETAS, DELAYS, DENSITIES, K_GRID, B_GRID, barrier_gap,
                   strategic_race, d_events, derive, temporal_envelope_curve,
                   wilson, closure_witness, barrier_parameters)

HERE = Path(__file__).resolve().parent


def save_csv(path: Path, rows: list[dict]) -> None:
    keys = list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def estimate(x, n):
    lo,hi = wilson(x,n)
    return dict(events=x,samples=n,estimate=x/n,ci95_low=lo,ci95_high=hi,
                zero_events_exact_upper95=(1-.05**(1/n)) if x == 0 else None)


def simulate_cell(job: dict) -> dict:
    resource.setrlimit(resource.RLIMIT_CPU,(job['cpu_limit'],job['cpu_limit']+1))
    cpu0, wall0 = time.process_time(),time.monotonic()
    beta,u,delay = job['beta'],job['u'],job['delay']
    h = (1-beta)*u
    d = math.floor(delay)
    n,T = job['samples'],job['horizon']
    # Common random numbers across network delays, independent replicates.
    seed_parts = [job['seed'],1,job['beta_index'],job['u_index']]
    rng = np.random.default_rng(np.random.SeedSequence(seed_parts))
    ages,depths,gaps,barriers,growth,starts = [np.empty(n,dtype=np.int32) for _ in range(6)]
    de_counts = {(k,b):0 for k in K_GRID if k<T//2 for b in (32,2880)}
    de_stop = de_counts.copy()
    violations = 0
    examples = []
    for rep in range(n):
        uniforms = rng.random(T)
        labels = np.where(uniforms < beta,2,np.where(uniforms < beta+h,1,0)).astype(np.uint8)
        ties = rng.random(T)
        owners = rng.integers(0,64,T,dtype=np.int16)
        race = strategic_race(labels,ties,d,owners)
        gap,nbar = barrier_gap(labels,d)
        ages[rep],depths[rep] = race.max_age,race.max_blocks
        gaps[rep],barriers[rep] = gap,nbar
        growth[rep],starts[rep] = race.public_blocks,race.attacks
        # Independent implementations: any inside-window honest barrier
        # must obstruct the constructive successful fork.
        if race.max_age > gap+d+1:
            violations += 1
        seen,stopped = set(),set()
        for event in d_events(race,T):
            key = (event['k'],event['b'])
            if event['diverges']:
                (seen if event['adoptable'] else stopped).add(key)
        for key in seen:
            de_counts[key] += 1
        for key in stopped:
            de_stop[key] += 1
        if rep < 2:
            examples.append(dict(rep=rep,age=race.age_witness,depth=race.depth_witness))
    cell = f'b{beta:.2f}_u{u:.1f}_d{delay:.1f}'
    out = Path(job['out'])
    np.savez_compressed(out/f'{cell}.npz',max_age=ages,max_blocks=depths,
                        barrier_gap=gaps,barrier_count=barriers,public_blocks=growth,
                        favorable_starts=starts)
    curves = []
    analytic = {r['k']:r['upper_bound'] for r in temporal_envelope_curve(beta,u,delay,T)}
    for k in K_GRID:
        for kind,data in [('constructive_age',ages),('envelope_gap',gaps)]:
            row = dict(beta=beta,u=u,delay=delay,kind=kind,k=k,
                       analytical_temporal_upper=analytic[k])
            row.update(estimate(int((data>=k).sum()),n))
            curves.append(row)
    for b in B_GRID:
        row = dict(beta=beta,u=u,delay=delay,kind='constructive_disconnected',k=b,
                   analytical_temporal_upper=None)
        row.update(estimate(int((depths>=b).sum()),n))
        curves.append(row)
    de_rows = []
    for (k,b),count in de_counts.items():
        row = dict(beta=beta,u=u,delay=delay,k=k,registry_min_blocks=b,
                   deep_disagreement_stop_samples=de_stop[(k,b)])
        row.update(estimate(count,n))
        de_rows.append(row)
    summary = dict(cell=cell,parameters=barrier_parameters(beta,u,delay),
                   samples=n,horizon=T,seed_entropy=seed_parts,honest_active_identities=64,
                   max_age_quantiles=np.quantile(ages,[.5,.9,.95,.99,1]).tolist(),
                   max_blocks_quantiles=np.quantile(depths,[.5,.9,.95,.99,1]).tolist(),
                   mean_public_growth=float(growth.mean()/T),
                   mean_favorable_starts=float(starts.mean()),
                   envelope_violations=violations,examples=examples,
                   cpu_seconds=time.process_time()-cpu0,
                   wall_seconds=time.monotonic()-wall0)
    (out/f'{cell}.json').write_text(json.dumps(summary,indent=2)+'\n')
    return dict(summary=summary,curves=curves,d_curves=de_rows)


def analyze(out: Path, horizon: int) -> dict:
    begin = time.process_time()
    rows = [derive(b,u,d,e,horizon,q) for b,u,d,e,q in itertools.product(
        BETAS,DENSITIES,DELAYS,(1e-6,1e-9,1e-12),(1,256))]
    save_csv(out/'derivation.csv',rows)
    (out/'closure-witness.json').write_text(json.dumps(closure_witness(2880),indent=2)+'\n')
    # Compact human-readable rendering is separate from the full witness.
    (out/'closure-witness-small.json').write_text(json.dumps(closure_witness(8),indent=2)+'\n')
    return dict(rows=len(rows),conditional=sum(r['conditional_status']=='CONDITIONAL' for r in rows),
                cpu_seconds=time.process_time()-begin)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=HERE/'results')
    parser.add_argument('--samples',type=int,default=4096)
    parser.add_argument('--horizon',type=int,default=14400)
    parser.add_argument('--workers',type=int,default=8)
    parser.add_argument('--seed',type=int,default=20260930)
    parser.add_argument('--cell-cpu-limit',type=int,default=15)
    parser.add_argument('--prior-cpu-reservation',type=float,default=0.)
    parser.add_argument('--pilot',action='store_true')
    parser.add_argument('--analytical-only',action='store_true')
    args = parser.parse_args()
    if args.horizon < 16 or args.horizon%6:
        parser.error('horizon must be >=16 and divisible by 6')
    if args.samples < 1 or not 1 <= args.workers <= 14:
        parser.error('invalid samples/workers')
    cells = 1 if args.pilot else 64
    if cells*(args.cell_cpu_limit+1)+120+args.prior_cpu_reservation >= 1800:
        parser.error('worst-case per-process CPU reservations exceed 30 minutes')
    args.out.mkdir(parents=True,exist_ok=True)
    if (args.out/'campaign.json').exists():
        parser.error('completed output exists: use a fresh --out directory')
    begin_wall,begin_cpu = time.monotonic(),time.process_time()
    resource.setrlimit(resource.RLIMIT_CPU,(110,120))
    analysis = analyze(args.out,args.horizon)
    jobs = []
    for bi,b in enumerate(BETAS):
        for ui,u in enumerate(DENSITIES):
            for delay in DELAYS:
                jobs.append(dict(beta=b,u=u,delay=delay,beta_index=bi,u_index=ui,
                                 seed=args.seed,samples=args.samples,horizon=args.horizon,
                                 out=str(args.out.resolve()),cpu_limit=args.cell_cpu_limit))
    if args.pilot:
        jobs = jobs[:1]
    results = []
    if not args.analytical_only:
        with mp.get_context('spawn').Pool(processes=args.workers,maxtasksperchild=1) as pool:
            pending = [pool.apply_async(simulate_cell,(job,)) for job in jobs]
            for future in pending:
                # A killed worker must fail the campaign, not leave an
                # unbounded wait on a lost result. Never convert it to PASS.
                result = future.get(timeout=180)
                results.append(result)
                print(json.dumps({k:result['summary'][k] for k in ('cell','cpu_seconds','envelope_violations')}),flush=True)
    results.sort(key=lambda r:r['summary']['cell'])
    save_csv(args.out/'mc-curves.csv',[r for cell in results for r in cell['curves']])
    save_csv(args.out/'d-curves.csv',[r for cell in results for r in cell['d_curves']])
    own = resource.getrusage(resource.RUSAGE_SELF)
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    metadata = dict(seed=args.seed,samples_per_cell=args.samples,horizon=args.horizon,
                    workers=args.workers,cell_cpu_limit=args.cell_cpu_limit,
                    hard_total_reservation_seconds=cells*(args.cell_cpu_limit+1)+120+args.prior_cpu_reservation,
                    prior_cpu_reservation_seconds=args.prior_cpu_reservation,
                    cells=len(results),analysis=analysis,
                    wall_seconds=time.monotonic()-begin_wall,
                    parent_cpu_seconds=own.ru_utime+own.ru_stime,
                    children_cpu_seconds=children.ru_utime+children.ru_stime,
                    total_cpu_seconds=own.ru_utime+own.ru_stime+children.ru_utime+children.ru_stime,
                    python=sys.version,numpy=np.__version__,platform=platform.platform(),
                    cpu_count=os.cpu_count(),command=sys.argv,
                    source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in HERE.glob('*.py')},
                    envelope_violations=sum(c['summary']['envelope_violations'] for c in results),
                    summaries=[c['summary'] for c in results])
    (args.out/'campaign.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps({k:metadata[k] for k in ('cells','wall_seconds','total_cpu_seconds','envelope_violations')}),flush=True)


if __name__ == '__main__':
    main()
