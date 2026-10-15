"""Exact finite checks for the new event-geometry bounds. Run without -O.

The universal geometric proof is PROOF.md. Enumerating these finite instances
is not the proof and gives no global event-count budget.
"""
from __future__ import annotations
from collections import deque
from dataclasses import asdict
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import sys

from event_geometry import (State, convex_hull, contains, enlarged_hull,
    support_diameter, macro_halo, event_deadline, halt_deadline,
    mandatory_event_count, periodic_envelope, prefix_extreme_points)
from memory_delay import DIRS, geometry, multiple, verify_period
from symbolic_stale import SymbolicState, next_stale_macro

# Separate reference: direction vectors, not the production heading table.
class Reference:
    def __init__(self, state):
        self.B = set(state.black); self.p = state.pos; self.v = DIRS[state.heading]
    def state(self):
        return State(frozenset(self.B), self.p, DIRS.index(self.v))
    def step(self):
        p = self.p; vx, vy = self.v; black = p in self.B
        self.B.symmetric_difference_update((p,))
        self.v = (-vy, vx) if black else (vy, -vx)
        self.p = (p[0]+self.v[0], p[1]+self.v[1])
        return 'L' if black else 'R'
    def back(self):
        vx, vy = self.v; p = (self.p[0]-vx, self.p[1]-vy)
        was_white = p in self.B
        self.B.symmetric_difference_update((p,))
        self.v = (-vy, vx) if was_white else (vy, -vx)
        self.p = p
        return p


def reference_event(state, D, cap=200000):
    past = Reference(state)
    history = [past.back() for _ in range(D)]
    recent = deque(reversed(history), maxlen=D)
    x = Reference(state); visited = {x.p}
    for t in range(cap):
        p = x.p
        if p in x.B and p not in recent:
            before = x.state(); assert x.step() == 'L'; visited.add(x.p)
            return t+1, before, x.state(), visited
        recent.append(p); x.step(); visited.add(x.p)
    raise RuntimeError('finite reference cap; not a theorem verdict')


def same_state(a, b):
    return a.black == b.black and a.pos == b.pos and a.heading == b.heading


def plan_check(state, word, cap=10000):
    env = periodic_envelope(state, word)
    check = verify_period(state, word)
    if check['valid']:
        return False
    t = check['first_bad_offset']
    assert t < env.first_mismatch_strict_deadline
    bounds = enlarged_hull([state.pos, *state.black], 3*len(word))
    # Includes the pre-update point of the first bad read, not its planned exit.
    extreme = prefix_extreme_points(state, word, t+1, include_terminal=False)
    assert all(contains(bounds, p) for p in extreme)
    if t < cap:
        x = Reference(state)
        for s in range(t):
            assert x.step() == word[s % len(word)]
        assert ('L' if x.p in x.B else 'R') != word[t % len(word)]
    return True


def main():
    if sys.flags.optimize:
        raise SystemExit('Run without -O; exact checkers use assertions.')
    report = {'schema': 'langtons-ant-event-geometry-checks-v1',
              'date': '2026-10-12', 'status': 'passed', 'counts': {},
              'scope': {'analytic_unformalized': True, 'global_event_budget': False,
                        'nonuniversality_proved': False, 'third_party_review': False,
                        'old_repository_suite_rerun': False}}
    counts = report['counts']
    cells = list(product(range(-1, 2), repeat=2))
    count = updates = footprint_checks = 0
    for mask in range(512):
        B = frozenset(p for i, p in enumerate(cells) if mask >> i & 1)
        for h in range(4):
            start = State(B, (0, 0), h)
            for D in (1, 2, 4, 8):
                symbolic = next_stale_macro(SymbolicState.explicit(start), D)
                assert symbolic['kind'] == 'stale_read'
                duration, before, after, visited = reference_event(start, D)
                assert duration == symbolic['duration']
                assert same_state(before, symbolic['before'].materialize())
                assert same_state(after, symbolic['after'].materialize())
                bounds = enlarged_hull([start.pos, *start.black], macro_halo(D))
                assert all(contains(bounds, p) for p in visited | set(after.black))
                assert duration <= event_deadline(D, 1, support_diameter(start))
                count += 1; updates += duration; footprint_checks += len(visited)
    counts.update(first_event_cases=count, reference_updates=updates,
                  finite_footprint_points=footprint_checks)

    chains = 0; chain_points = 0
    for mask in (0, 1, 19, 85, 170, 255, 341, 511):
        for h in range(4):
            original = State(frozenset(p for i,p in enumerate(cells) if mask >> i & 1),
                             (0, 0), h)
            for D in (1, 2, 4, 8):
                x = SymbolicState.explicit(original); elapsed = 0
                for n in range(1, 9):
                    src = x.materialize()
                    out = next_stale_macro(x, D)
                    assert out['kind'] == 'stale_read'
                    dt, _, dst, visits = reference_event(src, D)
                    elapsed += dt; x = out['after']
                    assert same_state(x.materialize(), dst)
                    assert elapsed <= event_deadline(D, n, support_diameter(original))
                    hull = enlarged_hull([original.pos,*original.black], n*macro_halo(D))
                    assert all(contains(hull, p) for p in visits | set(dst.black))
                    assert support_diameter(dst) <= support_diameter(original)+2*n*macro_halo(D)
                    chains += 1; chain_points += len(visits)
    counts.update(consecutive_macros=chains, chain_footprint_points=chain_points)

    randomizer = random.Random(1042026)
    words = []
    for P in (4, 6, 8, 10):
        for letters in product('RL', repeat=P):
            word = ''.join(letters)
            ps,h,d = geometry(State(frozenset()), word)
            if h == 0 and d != (0, 0):
                words.append(word)
    count = 0
    for word in words:
        ps,_,d = geometry(State(frozenset()), word)
        candidates = list(set((p[0]+k*d[0], p[1]+k*d[1]) for p in ps for k in range(4)))
        for _ in range(3):
            B = frozenset(p for p in candidates if randomizer.randrange(2))
            count += int(plan_check(State(B), word))
    counts['generic_translating_plan_mismatches'] = count
    # A long preinstalled RLLR rail is a plan control, not an S_D-free plan.
    for L in (1, 2, 3, 10, 100, 10000):
        s = State(frozenset((x,-1) for x in range(2*L)), (0,0), 1)
        assert plan_check(s, 'RLLR')
        assert verify_period(s, 'RLLR')['first_bad_offset'] == 4*L+1
    counts['arbitrary_length_rail_controls'] = 6

    # Closed-pose plans check the geometric argument used by the macro bound.
    closed = 0
    for P in range(1, 9):
        for letters in product('RL', repeat=P):
            w = ''.join(letters); s = State(frozenset())
            ps,h,d = geometry(s,w)
            if h == 0 and d != (0,0):
                continue
            copies = 2 if h == 2 else (4 if h else 1)
            path, endh, endd = geometry(s,w*copies)
            assert endh == 0 and endd == (0,0)
            assert max(max(abs(x),abs(y)) for x,y in path) <= 2*P
            closed += 1
    counts['closed_geometry_controls'] = closed

    # A real P104 tail, then a first collision a trillion periods away.
    x = Reference(State(frozenset()))
    for _ in range(12000): x.step()
    base = x.state(); u = Reference(base)
    word = ''.join(u.step() for _ in range(104))
    assert verify_period(base, word)['valid']
    ps,_,d = geometry(base,word)
    phase = None
    for i,p in enumerate(ps):
        links = [r for j,q in enumerate(ps)
                 if (r:=multiple((q[0]-p[0],q[1]-p[1]),d)) is not None
                 and r >= 0 and (r > 0 or j < i)]
        if word[i] == 'R' and not links:
            phase = i; break
    assert phase is not None
    k = 10**12
    p = ps[phase]; marker = (p[0]+k*d[0],p[1]+k*d[1])
    start = State(base.black | {marker},base.pos,base.heading)
    cert = verify_period(start,word); t = cert['first_bad_offset']
    assert t == 104*k+phase
    env = periodic_envelope(start,word)
    assert t < env.first_mismatch_strict_deadline
    hull = enlarged_hull([start.pos,*start.black],3*len(word))
    extreme = prefix_extreme_points(start,word,t+1,include_terminal=False)
    assert all(contains(hull,p) for p in extreme)
    # False over-extension control: an event-free tail eventually leaves any
    # fixed source halo. Do not apply a finite-event envelope after termination.
    small_hull = enlarged_hull([base.pos,*base.black],3*len(word))
    far = (base.pos[0]+10**6*d[0],base.pos[1]+10**6*d[1])
    assert not contains(small_hull,far)
    report['huge_plan_control'] = {'period':104,'first_bad_offset':t,
        'marker':list(marker),'cutoff_epoch':env.cutoff_epoch,
        'geometry_extreme_points_checked':len(extreme),
        'halo_radius':312,'literal_simulation_to_collision':False,
        'event_free_tail_is_not_confined':True}

    # Finite positive-instance local HALT controls, with pre-update HALT priority.
    # The observer samples offset (1,1), remembers time modulo 17, and halts
    # when its state is 5 and the observed cell is black. The ant is unaffected.
    positive = unresolved = simultaneous = 0
    for mask in range(0, 512, 4):
        for h in range(4):
            seed = State(frozenset(p for i,p in enumerate(cells) if mask >> i & 1),
                         (0,0), h)
            for D in (1,2,4,8):
                inv = Reference(seed)
                recent = deque(reversed([inv.back() for _ in range(D)]),maxlen=D)
                ant = Reference(seed); events = 0
                for t in range(4096):
                    stale = ant.p in ant.B and ant.p not in recent
                    sample = (ant.p[0]+1,ant.p[1]+1) in ant.B
                    if t % 17 == 5 and sample:
                        assert t < halt_deadline(D,events,support_diameter(seed),1,17)
                        positive += 1; simultaneous += int(stale)
                        break
                    events += int(stale)
                    recent.append(ant.p); ant.step()
                else:
                    unresolved += 1
    counts.update(positive_local_halt_controls=positive,
                  finite_halt_reference_caps=unresolved,
                  simultaneous_halt_stale_controls=simultaneous)

    # Numerically stable inversion, positive-budget deadlines, and input checks.
    deadline_cases = 0
    for D in (1,2,8,128):
        for W in (0,1,10,10**12):
            for n in (0,1,2,10,1000):
                t = event_deadline(D,n,W)
                assert mandatory_event_count(D,t,W) == n
                if n:
                    assert mandatory_event_count(D,t-1,W) == n-1
                expected = t+(1<<D)*(W+10*(1<<D)*n+2*(1<<D)+10+3+7)
                assert halt_deadline(D,n,W,3,7) == expected
                deadline_cases += 1
    counts['exact_deadline_algebra_cases'] = deadline_cases
    invalid = 0
    for fn,args in [(macro_halo,(0,)),(macro_halo,(True,)),
                    (event_deadline,(1,-1,0)),(event_deadline,(1,0,-1)),
                    (halt_deadline,(1,0,0,0,0)),
                    (mandatory_event_count,(1,-1,0)),
                    (periodic_envelope,(State(frozenset()),'RRRR')),
                    (enlarged_hull,([(0,0)],-1))]:
        try: fn(*args)
        except ValueError: invalid += 1
        else: raise AssertionError('invalid argument was accepted')
    counts['invalid_input_controls'] = invalid
    report['baseline_git_blobs'] = {}
    for name in ('memory_delay.py','symbolic_stale.py'):
        data = (Path(__file__).parent/'baseline'/name).read_bytes()
        report['baseline_git_blobs'][name] = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    report['source_sha256'] = {name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                               for name in ('event_geometry.py','check.py')}
    text = json.dumps(report,indent=2,ensure_ascii=False)+'\n'
    (Path(__file__).parent/'check_results.json').write_text(text,encoding='utf-8')
    print(text)

if __name__ == '__main__': main()
