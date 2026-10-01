#!/usr/bin/env python3
"""Independent tiny exhaustive oracle and boundary checks; no network/git."""
from itertools import product
import json
import math
from pathlib import Path
import time
import numpy as np
from model import (strategic_race,barrier_gap,support,closure_witness,
                   derive,catalan_pgf,trials_for_count,binomial_lower_bound)


def slow_race(labels,ties,d,owners=None):
    """Explicitly build all candidates; no prefix-balance optimization."""
    width = d+1
    size = len(labels)//width
    best_age = best_depth = 0
    for begin in range(size):
        for end in range(begin+1,size+1):
            public = []
            for g in range(begin,end):
                honest = [s for s in range(g*width,(g+1)*width) if labels[s] == 1]
                if honest:
                    if owners is None:
                        candidates = [[s] for s in honest]
                    else:
                        candidates = [[s for s in honest if owners[s]==owner]
                                      for owner in set(owners[s] for s in honest)]
                    public.extend(min(candidates,key=lambda ss:(-len(ss),tuple(ties[s] for s in ss))))
            private = [s for s in range(begin*width,end*width) if labels[s] == 2]
            if not public or not private:
                continue
            # Each branch is a sequence of blocks. N's score, then the
            # *whole* public tie sequence, is evaluated independently here.
            pr = (-len(public),tuple(ties[s] for s in public))
            ar = (-len(private),tuple(ties[s] for s in private))
            if ar < pr:
                best_depth = max(best_depth,len(public))
                best_age = max(best_age,end*width-1-min(public[0],private[0]))
    return best_age,best_depth


def main():
    cpu0 = time.process_time()
    tested = envelope_violations = 0
    rng = np.random.default_rng(9112026)
    for labels in product((0,1,2),repeat=6):
        labels = np.array(labels)
        for _ in range(2):
            ties = rng.random(6)
            for d in (0,1,2):
                owners = rng.integers(0,3,6)
                result = strategic_race(labels,ties,d,owners)
                expected = slow_race(labels,ties,d,owners)
                assert (result.max_age,result.max_blocks) == expected,(labels,ties,d,result,expected)
                gap,_ = barrier_gap(labels,d)
                if result.max_age > gap+d+1:
                    envelope_violations += 1
                tested += 1
    assert envelope_violations == 0
    # Strict raw cut, inclusive closing header, no genesis production count.
    chain = [(9,'old'),(10,'a'),(11,'b'),(12,'close'),(13,'after')]
    assert support(chain,10,12,3) == ('old',3)
    assert support(chain,10,12,4) == ('genesis',3)
    assert support(chain,10,15,1) == ('OPEN',None)
    assert support(chain,0,12,1)[0] == 'genesis'
    for b in (2,8,32,2880):
        assert closure_witness(b)['disconnected'] == 2
    # Exhaustive small binomial sums must lie BELOW the analytic bound.
    for m,p,b in product((10,20,40),(.2,.5,.8,1.),(1,5,10)):
        exact = sum(math.comb(m,i)*p**i*(1-p)**(m-i) for i in range(min(b,m+1)))
        assert exact <= binomial_lower_bound(m,p,b)+1e-14
    for p in (.1,.2,.3,.45):
        assert abs(catalan_pgf(1.,p)-1) < 1e-12
    for beta,u,d in product((.1,.2,.25,.3),(1.,.7,.4,.2),(0.,.5,1.,2.)):
        result = derive(beta,u,d,1e-9)
        if result['conditional_status'] == 'CONDITIONAL':
            assert result['composed_conditional_bound'] <= 1e-9*(1+1e-10)
    # Typical density must never be substituted for an integer guarantee.
    assert trials_for_count(20,.5,1e-9) > 40
    output = dict(status='PASS',exhaustive_race_cases=tested,
                  envelope_violations=envelope_violations,
                  cpu_seconds=time.process_time()-cpu0)
    Path(__file__).with_name('validation.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output))


if __name__ == '__main__':
    main()
