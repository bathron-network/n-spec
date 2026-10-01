"""CP-reg auteur 1. Models, not a N node implementation.

All times are integer slots; a branch has at most one block per slot.
See README.md and ../CP-REG-codex.md for the precise scopes of each model.
Only numpy and the Python standard library are required.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
import numpy as np

BETAS = (.10, .20, .25, .30)
DELAYS = (0., .5, 1., 2.)
DENSITIES = (1., .7, .4, .2)  # conditional honest availability u, not h
K_GRID = (4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 7200)
B_GRID = (8, 32, 128, 512, 2880)


def wilson(x: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    """Two-sided pointwise 95% Wilson; NOT a security bound."""
    p = x / n
    den = 1 + z*z/n
    mid = (p + z*z/(2*n))/den
    rad = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return max(0., mid-rad), min(1., mid+rad)


def kl(x: float, p: float) -> float:
    if p == 1:
        return 0. if x == 1 else math.inf
    if p == 0:
        return 0. if x == 0 else math.inf
    return ((x*math.log(x/p) if x else 0.) +
            ((1-x)*math.log((1-x)/(1-p)) if x != 1 else 0.))


def binomial_lower_bound(m: int, p: float, needed: int) -> float:
    """Chernoff upper bound on P[Bin(m,p) < needed]."""
    if needed <= 0:
        return 0.
    if m < needed or m*p <= needed-1:
        return 1.
    if p == 1:
        return 0.
    return math.exp(-m*kl((needed-1)/m, p))


def trials_for_count(needed: int, p: float, risk: float) -> int:
    if not 0 < p <= 1 or not 0 < risk < 1:
        raise ValueError((p, risk))
    if p == 1:
        return needed
    lo, hi = max(0, needed-1), max(needed, 1)
    while binomial_lower_bound(hi, p, needed) > risk:
        hi *= 2
    while lo+1 < hi:
        mid = (lo+hi)//2
        if binomial_lower_bound(mid, p, needed) <= risk:
            hi = mid
        else:
            lo = mid
    return hi


def catalan_pgf(z: float, p: float) -> float:
    """Explicit dominating PGF from KQR20 §5.1, only single honest leaders.

    p is BAD probability in the *compressed, conservatively reduced* string.
    Includes a stationary upper bound for private reach BEFORE the window.
    infinity means the argument is outside the convergence domain.
    """
    q = 1-p
    if not 0 < p < .5 or z < 1:
        return math.inf
    disc = 1-4*p*q*z*z
    if disc < 0:
        return math.inf
    descent = 2*q*z/(1+math.sqrt(disc))
    v = z*descent
    disc2 = 1-4*p*q*v*v
    if disc2 < 0:
        return math.inf
    ascent = 2*p*v/(1+math.sqrt(disc2))
    f = p*z*descent + q*z*ascent
    r = p/q
    if f >= 1 or r*descent >= 1:
        return math.inf
    return (1-r)*(q-p)*z / ((1-f)*(1-r*descent))


def pgf_grid(p: float, size: int = 2048) -> tuple[np.ndarray, np.ndarray]:
    lo, hi = 1., 2.
    for _ in range(64):
        mid = (lo+hi)/2
        if math.isfinite(catalan_pgf(mid, p)):
            lo = mid
        else:
            hi = mid
    # Strictly inside the convergence region, never at its singularity.
    zs = 1+(lo-1)*np.linspace(.0005, .9995, size)
    return zs, np.array([catalan_pgf(float(z), p) for z in zs])


def barrier_parameters(beta: float, u: float, delay: float) -> dict:
    h = (1-beta)*u
    f = h+beta
    # Production at fixed phase, deliveries at a reservation boundary may be
    # processed after reservation. Actual deployments must add phase/clock skew.
    d = math.floor(delay)
    good = (h/f)*(1-f)**d
    return dict(beta=beta, u=u, h=h, alpha=(1-beta)*(1-u), f=f,
                delay=delay, d=d, reduced_good=good, reduced_bad=1-good)


def _derive_fixed_horizon(beta: float, u: float, delay: float, epsilon: float,
                          horizon: int = 14400, q_paths: int = 1) -> dict:
    """Conditional conservative envelope, NOT qualified K_reg for N v0.6.

    Total risk has five allocations: block CP, first time barrier (two
    terms), second barrier (two terms), growth. Six equal budgets are used.
    Horizon counts possible choices of endpoints; the lookback law must
    hold over the full computed window even when it exceeds horizon.
    """
    row = barrier_parameters(beta, u, delay)
    row.update(epsilon=epsilon, horizon=horizon, q_paths=q_paths,
               N_v06_status="UNKNOWN", conditional_status="NO_CERTIFICATE")
    p, f, h, d = row['reduced_bad'], row['f'], row['h'], row['d']
    if p >= .5:
        row['reason'] = 'NO_HONEST_DRIFT' if h <= beta else 'DELAY_REDUCTION_LOOSE'
        return row
    budget = epsilon/(6*horizon*q_paths)
    zs, bs = pgf_grid(p)
    ns = np.ceil((np.log(bs)-math.log(budget))/np.log(zs)).astype(np.int64)
    idx = int(ns.argmin())
    n, z, bz = int(ns[idx]), float(zs[idx]), float(bs[idx])
    # One conservative boundary unit; one potential trailing delay per slot.
    blocks = n+d+1
    active_slots = trials_for_count(n, f, budget)
    barrier_slots = active_slots+d+1
    # Safe growth frames: d+1 production slots, d silent delivery guard slots.
    # Guards are in the proof only: actual production is NOT stopped.
    frame_length = 2*d+1
    frame_success = 1-(1-h)**(d+1)
    growth_frames = trials_for_count(blocks+1, frame_success, budget)
    growth_slots = growth_frames*frame_length
    window = 2*barrier_slots+growth_slots
    row.update(conditional_status="CONDITIONAL", reason="",
               active_barrier_n=n, z=z, pgf=bz,
               registry_min_blocks_conditional=blocks,
               K_barrier_slots=barrier_slots, growth_slots=growth_slots,
               K_reg_slots_guard0=window,
               K_reg_slots_guard6000=max(1, window-6000),
               K_reg_hours_tau6=window/600,
               cp_component_bound=horizon*q_paths*bz*z**(-n),
               active_count_component_bound=horizon*q_paths*binomial_lower_bound(active_slots,f,n),
               growth_component_bound=horizon*q_paths*binomial_lower_bound(growth_frames,frame_success,blocks+1))
    row['composed_conditional_bound'] = (3*row['cp_component_bound']+
                                        2*row['active_count_component_bound']+
                                        row['growth_component_bound'])
    return row


def derive(beta: float, u: float, delay: float, epsilon: float,
           horizon: int = 14400, q_paths: int = 1) -> dict:
    """Cover BOTH the lookback and the requested observation horizon.

    Solve the monotone sizing fixed point, instead of counting only one
    epoch's starting opportunities when the required lookback is longer.
    """
    total = horizon
    for iterations in range(100):
        row = _derive_fixed_horizon(beta,u,delay,epsilon,total,q_paths)
        row['observation_horizon'] = horizon
        row['horizon_iterations'] = iterations+1
        if row['conditional_status'] != 'CONDITIONAL':
            return row
        needed_total = horizon+row['K_reg_slots_guard0']+row['d']+2
        if needed_total <= total:
            return row
        total = needed_total
    raise RuntimeError('sizing fixed point did not converge')


def temporal_envelope_curve(beta: float, u: float, delay: float,
                            horizon: int, q_paths: int = 1) -> list[dict]:
    par = barrier_parameters(beta, u, delay)
    p, f, d = par['reduced_bad'], par['f'], par['d']
    if p < .5:
        zs, bs = pgf_grid(p, 256)
    out = []
    for k in K_GRID:
        bound = 1.
        if p < .5 and k > d+2:
            m = k-d-1
            # Optimize n by a finite deterministic grid. A suboptimal grid
            # loosens a valid bound; it never invalidates it.
            candidates = np.unique(np.linspace(1, max(1,int(m*f)),128).astype(int))
            for n in candidates:
                cp = float(np.exp(np.min(np.log(bs)-n*np.log(zs))))
                v = horizon*q_paths*(binomial_lower_bound(m,f,int(n))+cp)
                bound = min(bound, v)
        out.append(dict(k=k, upper_bound=min(1.,bound)))
    return out


def barrier_gap(labels: np.ndarray, d: int) -> tuple[int, int]:
    """All finite-horizon Catalan barriers of a dominating delta-fork string.

    0=empty, 1=honest, 2=adversarial. Keep H only if the following d
    slots are EMPTY (stronger than necessary); convert all other H to A.
    An unverified trailing guard is pessimistically bad.
    """
    n = len(labels)
    good = labels == 1
    for shift in range(1,d+1):
        following_empty = np.zeros(n,dtype=bool)
        following_empty[:-shift] = labels[shift:] == 0
        good &= following_empty
    increments = np.where(labels == 0,0,np.where(good,-1,1))
    walk = np.cumsum(increments)
    before = np.minimum.accumulate(np.r_[0,walk[:-1]])
    after = np.maximum.accumulate(walk[::-1])[::-1]
    slots = np.flatnonzero(good & (walk < before) & (walk >= after))+1
    gap = int(np.diff(np.r_[0,slots,n]).max())
    return gap, len(slots)


@dataclass
class RaceResult:
    max_age: int
    max_blocks: int
    attacks: int
    public_blocks: int
    age_witness: dict | None
    depth_witness: dict | None
    public_slots: np.ndarray
    adverse_slots: np.ndarray


def strategic_race(labels: np.ndarray, ties: np.ndarray, d: int,
                   owners: np.ndarray | None = None) -> RaceResult:
    """Exact all-start/all-reveal optimization in a constructive attack family.

    Honest broadcasts inside groups of d+1 slots are delivered together
    after the group's last reservation; different honest producers have
    the same parent. Repeated owners extend THEIR OWN earlier block.
    The public chain takes the longest owner-chain, then public tie.
    This is one legal delay scheduler,
    not a worst-case search over all networks or all strategies.

    The attacker withholds all its blocks on one fork, selected after
    seeing the WHOLE schedule. It may release once at any group end.
    Max age and max disconnected blocks may use different strategies.
    Empty groups do not add a block. Strict public tie-sequence ordering
    is used. An alternative content at each adverse slot can be signed
    too; its tie is identical and it adds NO score.
    """
    size = d+1
    groups = len(labels)//size
    labels = labels[:groups*size]
    ties = ties[:groups*size]
    mat = labels.reshape(groups,size)
    ts = ties.reshape(groups,size)
    own = (np.arange(groups*size) if owners is None else owners[:groups*size]).reshape(groups,size)
    honest = mat == 1
    scores = np.full((groups,size),-np.inf)
    for j in range(size):
        same = honest & (own == own[:,j:j+1])
        first = honest[:,j] & ~same[:,:j].any(axis=1)
        scores[:,j] = np.where(first,2*same.sum(axis=1)-ts[:,j],-np.inf)
    winner = np.argmax(scores,axis=1)
    selected = honest & (own == own[np.arange(groups),winner,None])
    hc = selected.sum(axis=1)
    ac = (mat == 2).sum(axis=1)
    public_slots = np.flatnonzero(selected.reshape(-1))
    adverse_slots = np.flatnonzero(labels == 2)
    H = np.r_[0,np.cumsum(hc)]
    A = np.r_[0,np.cumsum(ac)]
    balance = A-H
    idx = np.arange(groups+1)
    first_a = np.searchsorted(adverse_slots,np.arange(groups)*size)
    first_h = np.searchsorted(public_slots,np.arange(groups)*size)
    fa = np.r_[adverse_slots,len(labels)][first_a]
    fh = np.r_[public_slots,len(labels)][first_h]
    padded_ties = np.r_[ties,np.inf]
    tie_good = padded_ties[fa] < padded_ties[fh]
    offset = int(-balance.min())+2
    maximum = int(balance.max()+offset)+4
    last_at = np.full(maximum+1,-1,dtype=np.int64)
    np.maximum.at(last_at,balance+offset,idx)
    last_ge = np.maximum.accumulate(last_at[::-1])[::-1]
    threshold = balance[:-1]+offset+np.where(tie_good,0,1)
    release = last_ge[threshold]
    starts = np.arange(groups)
    valid = (release > starts) & (fa < len(labels)) & (fh < len(labels))
    safe_release = np.maximum(release,0)
    removed = H[safe_release]-H[starts]
    valid &= removed > 0
    first_diff = np.minimum(fa,fh)
    ages = np.where(valid,release*size-1-first_diff,0)
    depths = np.where(valid,removed,0)

    def witness(i: int) -> dict | None:
        if not valid[i]:
            return None
        return dict(start_group=int(i), start_slot=int(i*size),
                    release_slot=int(release[i]*size-1),
                    public_prefix_blocks=int(H[i]),
                    public_total_blocks=int(H[release[i]]),
                    private_added=int(A[release[i]]-A[i]),
                    disconnected=int(removed[i]),
                    first_difference=int(first_diff[i]),
                    age=int(ages[i]), tie_favorable=bool(tie_good[i]))
    age_i, depth_i = int(ages.argmax()), int(depths.argmax())
    return RaceResult(int(ages[age_i]),int(depths[depth_i]),int(valid.sum()),
                      int(H[-1]),witness(age_i),witness(depth_i),
                      public_slots,adverse_slots)


def support(chain: list[tuple[int, str]], cut: int, maturity: int,
            minimum: int) -> tuple[str, int | None]:
    """Exact §5.2 projection: references first engage maturity at slot >= m.

    Previous effective support is genesis; control operations are empty.
    Each ID uniquely commits to its prefix in this projection.
    """
    if cut <= 0:
        raw = 'genesis'
    else:
        raw = next((bid for slot,bid in reversed(chain) if slot < cut),'genesis')
    closure = next((slot for slot,_ in chain if slot >= maturity),None)
    if closure is None:
        return 'OPEN',None
    count = sum(cut <= slot <= closure for slot,_ in chain)
    return (raw if count >= minimum else 'genesis'),count


def d_events(race: RaceResult, horizon: int) -> list[dict]:
    """Actual D=(genesis,P_e) at two honest installations, two witnesses only.

    m=T/2 fixed independently of the schedule. Full D equality is encoded
    by collision-free prefix IDs; same control-free registry on both
    branches. Local maxreorg=b; deep releases are STOP, not adoption.
    This is a lower bound on achievable D divergence, NOT optimization
    over every attack or a simulation of changing registry lotteries.
    """
    m = horizon//2
    # First public honest engagement of e, at/after seed maturity.
    future = race.public_slots[race.public_slots >= m]
    if not len(future):
        return []
    first_commit = int(future[0])
    out = []
    for w in (race.age_witness,race.depth_witness):
        if w is None or w['release_slot'] < first_commit:
            continue
        # A selected strategy cannot retroactively fork after its release.
        pub = race.public_slots[race.public_slots <= w['release_slot']]
        prefix = pub[:w['public_prefix_blocks']]
        added = race.adverse_slots[(race.adverse_slots >= w['start_slot']) &
                                   (race.adverse_slots <= w['release_slot'])]
        priv = np.r_[prefix,added]
        priv_ids = np.r_[2*prefix+1,2*added+2]
        old = pub[pub <= first_commit]
        def project(slots,ids,cut,b):
            raw_i = int(np.searchsorted(slots,cut))-1
            close_i = int(np.searchsorted(slots,m))
            if close_i == len(slots):
                return -1,None
            count = close_i-int(np.searchsorted(slots,cut))+1
            raw = int(ids[raw_i]) if raw_i >= 0 and cut > 0 else 0
            return (raw if count >= b else 0),count
        for k in K_GRID:
            if k >= m:
                continue  # left-censored, no claim of zero failures
            cut = m-k
            for b in (32,2880):
                lhs,n1 = project(old,2*old+1,cut,b)
                rhs,n2 = project(priv,priv_ids,cut,b)
                if lhs == -1 or rhs == -1:
                    continue
                diverges = lhs != rhs
                out.append(dict(k=k,b=b,diverges=diverges,
                                adoptable=w['disconnected'] <= b,
                                count_public=n1,count_private=n2))
    return out


def closure_witness(minimum: int = 8) -> dict:
    """Executable threshold-pivot trace; no claim about its frequency in N.

    Before e starts: common window has b-2 blocks; adversarial E closes
    at b-1, equivocation L keeps an old reference. At e's first slot H
    extends E. Next A extends L and closes at b. E/L have equal public
    tie; the next A has a better tie than H. The private branch wins,
    with only TWO disconnected blocks and identical raw snapshot.
    Control-free supports keep the registry/lottery identical.
    """
    if minimum < 2:
        raise ValueError(minimum)
    cut = 7200
    raw = [(cut-3,'P')]
    common = raw+[(cut+i,f'W{i}') for i in range(minimum-2)]
    e_slot = 28800  # epoch e=2, freeze=14400, K_reg=7200
    if cut+minimum-2 >= e_slot-1:
        raise ValueError('witness window too short')
    early_slot = e_slot-1
    # ref booleans specify first inclusion of seed maturity.
    early = [(s,b,False) for s,b in common]+[(early_slot,'E',True),(e_slot,'H',True)]
    late = [(s,b,False) for s,b in common]+[(early_slot,'L',False),(e_slot+1,'A',True)]
    def derive_ref(chain):
        closing = next(s for s,_,mature in chain if mature)
        n = sum(cut <= s <= closing for s,_,_ in chain)
        return ('P' if n >= minimum else 'genesis'),n,closing
    left,right = derive_ref(early),derive_ref(late)
    assert left[0] != right[0] and left[1] == minimum-1 and right[1] == minimum
    # Prefix tie sequences: E and L at same slot/IID/seed => equal tie.
    # Body/ref content cannot break the tie; successor public ties do.
    left_ties,right_ties = (0.4,0.8),(0.4,0.2)
    assert len(early) == len(late) and right_ties < left_ties
    return dict(minimum=minimum,cut=cut,raw_support='P',inherited='genesis',
                epoch_start=e_slot,early=early,late=late,
                public_support=left,private_support=right,disconnected=2,
                private_wins_public_rank=True,registry_equal_no_control_ops=True,
                statement='CP_reg failure in a projected valid schedule; not a probability or full native block fixture')
