"""Tests for the exact-state decider and computable orbit section.
These tests do not claim to decide HIGHWAY.
"""
import json, random
from pathlib import Path
from diagonal_clock import *
ROOT=Path(__file__).resolve().parent
rng=random.Random(104)
counts={'inverse_round_trips':0,'signed_reachability_pairs':0,
        'normal_forms_checked':0,'equal_clock_negative_pairs':0}
for k in range(20):
    st=State(frozenset((x,y) for x in range(-1,2) for y in range(-1,2)
                       if rng.randrange(2)),(rng.randrange(-1,2),rng.randrange(-1,2)),
                       rng.randrange(4))
    nf=orbit_normal_form(st)
    assert clock(nf.representative)>=0>clock(inverse_step(nf.representative))
    for t in (-5,-1,0,1,7,16):
        target=st
        for _ in range(abs(t)):
            assert inverse_step(step(target))==target
            assert step(inverse_step(target))==target
            counts['inverse_round_trips']+=2
            target=step(target) if t>=0 else inverse_step(target)
        assert orbit_time(st,target)==t
        if t>=0: assert forward_time(st,target)==t
        else: assert forward_time(st,target) is None
        counts['signed_reachability_pairs']+=1
        tnf=orbit_normal_form(target)
        assert tnf.representative==nf.representative
        assert tnf.offset==nf.offset+t
        counts['normal_forms_checked']+=1
for i in range(1,13):
    x=State(frozenset({(-i,i+1)}))
    y=State(frozenset({(i+1,-i)}))
    assert x!=y and clock(x)==clock(y)
    assert orbit_time(x,y) is None
    counts['equal_clock_negative_pairs']+=1
blank=State(frozenset())
bnf=orbit_normal_form(blank)
assert bnf.offset==-2
assert forward_time(blank,bnf.representative)==2
out={'status':'PASS','counts':counts,
     'blank_normal_form':{'black':sorted(bnf.representative.black),
                         'position':bnf.representative.pos,
                         'heading':bnf.representative.heading,
                         'input_offset':bnf.offset,
                         'clock':str(clock(bnf.representative))},
     'scope':{'exact_state_reachability_total':True,
              'biinfinite_orbit_equivalence_total':True,
              'orbit_normal_form_total':True,
              'highway_decider':False}}
(ROOT/'orbit_decider_checks.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
