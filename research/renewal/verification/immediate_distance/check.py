#!/usr/bin/env python3
"""Scoped controls; all-n claims rely on the written geometric proof."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import random
from distance import (STANDARD, DRIFTS, PSTAR, phases, read_member, scores,
                      direct_scores, step, padding, seed)
from baseline.periodic_verify import verify_forever, geometry, multiple

ROOT = Path(__file__).resolve().parent
BASELINE_SHA = '50186c42b6caa35b51a1d3449d33a340272bbc71daab0a4ed55582fa1ba7f29f'


def independent_update(black, pos, direction):
    """Integer direction-pair implementation, independent of heading arithmetic."""
    x, y = pos
    u, v = direction
    if pos in black:
        black.remove(pos)
        direction = (-v, u)
        letter = 'L'
    else:
        black.add(pos)
        direction = (v, -u)
        letter = 'R'
    return (x+direction[0], y+direction[1]), direction, letter


def future_clean_test(black, pos, heading, word):
    from baseline.periodic_verify import reconstruct
    clean, geo = reconstruct(word, heading)
    actual = {(x-pos[0], y-pos[1]) for x, y in black}
    for x, y in actual ^ clean:
        for u, v in geo['q']:
            k = multiple((x-u, y-v), geo['drift'])
            if k is not None and k >= 0:
                return False
    return True


def run():
    if not __debug__:
        raise RuntimeError('checks require assertions; do not use -O')
    raw = (ROOT/'baseline/periodic_verify.py').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == BASELINE_SHA
    frozen = json.loads((ROOT/'base_positive.json').read_text())
    K = set(phases(1)[0][0])
    assert len(K) == 19 and (0, 0) not in K and (1, 1) not in K
    geo = geometry(STANDARD, 1)
    assert geo[2] == (2, -2)
    assert (min(x+y for x,y in geo[0]), max(x+y for x,y in geo[0])) == (-10, 0)
    assert all(any(STANDARD[i] != STANDARD[(i+d)%104] for i in range(104))
               for d in range(1,104) if 104%d == 0)

    # Full base orbit, not only its poses; independent integer update logic.
    B = seed(0); C = set(B); p = (0,0); h = 1; q = p; direction = (1,0)
    words = []; maxnorm = 0; field_comparisons = 0; third = None
    for t in range(frozen['time']):
        maxnorm = max(maxnorm, abs(p[0]), abs(p[1]))
        p,h,a = step(B,p,h); q,direction,b = independent_update(C,q,direction)
        assert a == b and p == q and direction == ((0,1),(1,0),(0,-1),(-1,0))[h]
        if t%97 == 0 or t in (2,103,frozen['time']-1):
            assert B == C; field_comparisons += 1
        words.append(a)
        if t == 2:
            third = (set(B),p,h)
    text = ''.join(words)
    assert text[:3] == 'LRL'
    assert not any(text[:104] == STANDARD[j:]+STANDARD[:j] for j in range(104))
    assert third == (K | {(0,1)}, PSTAR, 0)
    assert B == set(map(tuple,frozen['black'])) and p == tuple(frozen['pos']) and h == frozen['heading']
    assert maxnorm == frozen['finite_path_maxnorm'] == 37
    word = frozen['word']
    good, parity = verify_forever({(x-p[0],y-p[1]) for x,y in B},word,h)
    assert good and future_clean_test(B,p,h,word)
    phase_points, _, drift = geometry(word,h)
    transverse = [p[0]+x-p[1]-y for x,y in phase_points]
    assert drift == (-2,-2)
    assert [min(transverse),max(transverse)] == [-29,-19]
    last_bad = max(t for t,c in enumerate(text) if c != word[(t-len(text))%104])
    assert last_bad+1 == frozen['first_entry'] == 12440
    assert text[last_bad] == 'L' and word[(last_bad-len(text))%104] == 'R'
    assert all(text[t] == word[(t-len(text))%104] for t in range(last_bad+1,len(text)))

    # The actual first source-black contacts in the singleton shadow.
    residual = seed(0)-{(0,0)}; shadow = {(0,0)}; sp=(0,0); sh=1
    assert (0,0) in seed(0)   # Primary is immediate on the blank reference.
    for t in range(2):
        assert sp not in residual
        sp,sh,_ = step(shadow,sp,sh)
    assert sp == (1,1) and sp in residual and sp not in shadow

    lib_count=0; member_checks=0; max_clean_radius=0
    for heading in range(4):
        for phase in phases(heading):
            clean, d, _, _, positions, w = phase
            assert d in DRIFTS
            assert verify_forever(set(clean),w,heading)[0]
            assert all(read_member(z,phase) for z in clean)
            max_clean_radius=max(max_clean_radius,max(max(abs(x),abs(y)) for x,y in clean))
            lib_count+=1
            # Exact finite checks of the general opposite/perpendicular-ray argument.
            for M in (1000,10**60,10**150):
                for other in DRIFTS:
                    z=(M*other[0],M*other[1])
                    assert read_member(z,phase) == (d == other)
                    assert z not in clean
                    member_checks+=1

    base_scores=scores(K|{(0,1)},PSTAR,0)
    assert base_scores == direct_scores(K|{(0,1)},PSTAR,0)
    assert min(base_scores) == 10
    padded_controls=[]
    for M in (1000,10**60,10**150):
        for n in (0,1,2,7,31,100):
            E=padding(n,M)
            assert len(E) == 4*n
            assert all(x+y>0 or x+y < -10 for x,y in E)
            assert all(max(abs(x),abs(y)) >37 and not (-29<=x-y<=-19) for x,y in E)
            X=seed(n,M); X0=set(X); pp=(0,0); hh=1
            for _ in range(3):pp,hh,_=step(X,pp,hh)
            assert (pp,hh)==(PSTAR,0) and X==K|{(0,1)}|E
            initial_scores=scores(X0,(0,0),1); final_scores=scores(X,pp,hh)
            assert min(initial_scores)==1 and final_scores==[v+n for v in base_scores]
            assert verify_forever(K|{(1,1)}|E,STANDARD,1)[0]
            # Full field at the certified endpoint, including all inert padding.
            assert verify_forever({(x-p[0],y-p[1]) for x,y in B|E},word,h)[0]
            assert future_clean_test(B|E,p,h,word)
            if n<=2:
                assert initial_scores == direct_scores(X0,(0,0),1)
                assert final_scores == direct_scores(X,pp,hh)
            padded_controls.append({'n':n,'start':str(M),'source_distance':1,
                                    'post_macro_distance':n+10,'first_standard_entry':12440})

    rng=random.Random(2026101507); oracle_cases=0
    grid=[(x,y) for x in range(-8,9) for y in range(-8,9)]
    for _ in range(48):
        S=set(rng.sample(grid,rng.randrange(25))); pp=rng.choice(grid); hh=rng.randrange(4)
        S.add((10**150+rng.randrange(20),-(10**150)))
        assert scores(S,pp,hh)==direct_scores(S,pp,hh);oracle_cases+=1
    invalid=0
    for args in ((-1,1000),(1,999),(True,1000),(1,False)):
        try:padding(*args)
        except ValueError:invalid+=1
        else:raise AssertionError('bad parameters accepted')
    # Explicit first-prefix control of one padded example; the all-n guarantee
    # is by speed and the far coordinates, not by extrapolating this replay.
    X=seed(7);pp=(0,0);hh=1;ww=[]
    for _ in range(104):pp,hh,c=step(X,pp,hh);ww.append(c)
    assert ''.join(ww)==text[:104]

    report={'schema':'langtons-ant-immediate-distance-obstruction-v1',
      'scope':'analytic all-n proof plus finite controls; no new HC basin coverage or counterexample',
      'remote_base':'0ef3f0e149044c64f5a4b2b2ea9e192300fbe4f6',
      'macro':{'updates':3,'word':'LRL','primary':[0,0],'secondary':[1,1],
               'source_distance':1,'target_distance_formula':'n+10','target_pose':[[1,2],0]},
      'base_positive':{'certified_boundary':12544,'first_standard_entry':12440,
            'endpoint_black_count':len(B),'endpoint_pose':[list(p),h],
            'tail_word':word,'tail_drift':list(drift),'tail_x_minus_y':[-29,-19],
            'prelude_maxnorm':maxnorm,'last_bad_index':last_bad,
            'prelude_sha256':hashlib.sha256(text.encode()).hexdigest(),
            'source_104_prefix':text[:104],'parity_evaluations':parity['evaluations']},
      'base_target_all_104_scores':base_scores,
      'controls':{'two_implementation_updates':len(text),'full_field_comparisons':field_comparisons,
           'phase_heading_forever_checks':lib_count,'phase_ray_direction_checks':member_checks,
           'largest_clean_radius':max_clean_radius,'random_complete_field_oracles':oracle_cases,
           'invalid_parameters_rejected':invalid},
      'padded_controls':padded_controls,
      'universal_boundary':'Padding is unread by the ACTUAL infinite trajectory; it blocks only hypothetical immediate standard futures.',
      'sources_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
          for name in ('distance.py','check.py','baseline/periodic_verify.py','base_positive.json')}}
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--compare',type=Path)
    args=parser.parse_args();report=run()
    if args.compare and report != json.loads(args.compare.read_text()):
        raise SystemExit('deterministic report mismatch')
    text=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
