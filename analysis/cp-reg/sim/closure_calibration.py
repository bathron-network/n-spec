#!/usr/bin/env python3
"""Calibrated abstention + two equivocations, conditional late-BTC scenario.

Different question from a private race: deliberately place the rule-A
count on b-2 using the PUBLIC schedule, reveal E, retain L, then reveal
L+A after an honest H on E. The first carrier closes on b-1 versus b.
All broadcasts are instantaneous, which is permitted for EVERY Delta.
Only conditional probabilities given the documented common history and
late maturity scenario are estimated. No Bitcoin timing law is invented.
"""
import argparse
import json
import math
import multiprocessing as mp
from pathlib import Path
import resource
import time
import numpy as np
from model import BETAS,DENSITIES,DELAYS,K_GRID,wilson
from run import save_csv,estimate


def job(args):
    bi,ui,n,seed = args
    resource.setrlimit(resource.RLIMIT_CPU,(18,19))
    start = time.process_time()
    beta,u = BETAS[bi],DENSITIES[ui]
    h = (1-beta)*u
    rng = np.random.default_rng(np.random.SeedSequence([seed,2,bi,ui]))
    counts = {k:[0,0] for k in K_GRID}
    for offset in range(0,n,8192):
        size = min(8192,n-offset)
        # The A-H-A and favorable successor public-tie events are sampled
        # separately and kept fixed across K (common random numbers).
        suffix = ((rng.random(size)<beta) & (rng.random(size)<h) &
                  (rng.random(size)<beta) & (rng.random(size)<.5))
        # At freeze_slot=start(e-1), its whole calendar is known. Earlier
        # adverse slots were all withheld. Only future A slots of e-1
        # may now be selected for public filling: no foreknowledge of an
        # unrevealed later epoch seed is required for this calibration.
        future = rng.multinomial(14399,[h,beta,max(0.,1-h-beta)],size=size)
        honest = future[:,0].astype(np.int32)
        adverse = future[:,1].astype(np.int32)
        previous = 0
        for k in K_GRID:
            honest += rng.binomial(k-previous,h,size=size)
            # Exact number of PUBLIC adverse blocks to produce, chosen
            # using future honest assignments. Other own slots abstain.
            publish = 2880-2-honest
            calibrated = (publish>=0) & (publish<=adverse)
            counts[k][0] += int(calibrated.sum())
            counts[k][1] += int((calibrated & suffix).sum())
            previous = k
    rows = []
    for k,(feasible,failures) in counts.items():
        row = dict(beta=beta,u=u,k=k,registry_min_blocks=2880,
                   condition='shared control-free history; seed(e-1) known at freeze; seed(e) first mature at epoch_start-1',
                   allowed_delay_grid='0;0.5;1;2',actual_delay=0,
                   calibrated_samples=feasible,calibrated_probability=feasible/n,
                   suffix_probability=beta*beta*h/2,
                   analytic_given_counts=(feasible/n)*beta*beta*h/2,
                   disconnected_blocks_on_success=2)
        row.update(estimate(failures,n))
        rows.append(row)
    return dict(rows=rows,cpu_seconds=time.process_time()-start)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--samples',type=int,default=1000000)
    p.add_argument('--seed',type=int,default=20260930)
    p.add_argument('--workers',type=int,default=8)
    p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'results')
    args = p.parse_args()
    wall = time.monotonic()
    resource.setrlimit(resource.RLIMIT_CPU,(19,20))
    with mp.get_context('spawn').Pool(args.workers,maxtasksperchild=1) as pool:
        pending = [pool.apply_async(job,((bi,ui,args.samples,args.seed),))
                   for bi in range(4) for ui in range(4)]
        outputs = [future.get(timeout=90) for future in pending]
    rows = [r for result in outputs for r in result['rows']]
    args.out.mkdir(exist_ok=True,parents=True)
    save_csv(args.out/'closure-calibration.csv',rows)
    own,kids = resource.getrusage(resource.RUSAGE_SELF),resource.getrusage(resource.RUSAGE_CHILDREN)
    result = dict(samples_per_beta_u=args.samples,seed=args.seed,workers=args.workers,
                  independent_samples=16*args.samples,rows=len(rows),
                  wall_seconds=time.monotonic()-wall,
                  total_cpu_seconds=own.ru_utime+own.ru_stime+kids.ru_utime+kids.ru_stime,
                  hard_cpu_reservation=16*19+20,
                  note='Conditional scenario. Four Delta values share the same instantaneous-delivery experiment.')
    (args.out/'closure-campaign.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
