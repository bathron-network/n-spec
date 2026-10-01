#!/usr/bin/env python3
"""Evaluate 7200/2880 AFTER deriving the risk-dependent quantities.

This does not calibrate a risk formula to justify the existing pair.
Every conclusion remains conditional on H_ref, Q=1, and G=6000.
"""
import itertools
from pathlib import Path
from model import BETAS,DELAYS,DENSITIES,_derive_fixed_horizon,trials_for_count
from run import save_csv


def main():
    rows=[]
    for beta,u,delay,eps in itertools.product(BETAS,DENSITIES,DELAYS,(1e-6,1e-9,1e-12)):
        window=7200+6000
        d=int(delay)
        total=14400+window+d+2
        row=_derive_fixed_horizon(beta,u,delay,eps,total,1)
        result=dict(beta=beta,u=u,delay=delay,epsilon=eps,current_K=7200,current_b=2880,
                    history_horizon=total,status='NO_CERTIFICATE',N_v06_status='UNKNOWN')
        if row['conditional_status']=='CONDITIONAL':
            budget=eps/(6*total)
            h=(1-beta)*u
            growth=trials_for_count(2881,1-(1-h)**(d+1),budget)*(2*d+1)
            need_window=2*row['K_barrier_slots']+growth
            need_b=row['registry_min_blocks_conditional']
            result.update(required_window_with_current_b=need_window,
                          required_b_for_block_risk=need_b,
                          status=('SUFFICIENT_IN_H_REF' if need_window<=window and need_b<=2880
                                  else 'NOT_CERTIFIED_BY_THIS_BOUND'))
        else:
            result['reason']=row['reason']
        rows.append(result)
    out=Path(__file__).resolve().parent/'results'/'existing-pair.csv'
    save_csv(out,rows)
    print(f'{len(rows)} comparisons saved to {out}')


if __name__=='__main__':
    main()
