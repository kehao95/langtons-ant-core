"""Check only the new parity splice; old large searches are not replayed.

Every imported YES theorem keeps its original hypotheses and evidence boundary.
A passing formal wake is NOT a certified ant trajectory.
"""
from __future__ import annotations
from collections import Counter
from hashlib import sha1, sha256
import importlib.util
import json
from pathlib import Path
import sys


def load_prior():
    p=Path(__file__).resolve().parents[1]/'mixed_wake_parity/mixed_wake.py'
    raw=p.read_bytes()
    if sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!='7fb7e3d894b98f47ea34dd640bbe2b8e7df5a01f':
        raise ValueError('Mixed-wake source changed; review the interface first')
    spec=importlib.util.spec_from_file_location('prior_mixed',p)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def pair_count(wake):
    # Independent direct formula in the TOP-RAIL sigma=-1 frame.
    q=[t for t,r in wake if t%2]
    c=[t for t,r in wake if not t%2]
    return len(q),sum(u<v for u in q for v in c)


def main():
    if not __debug__:raise RuntimeError('Do not use Python -O')
    prior=load_prior();rows=[]
    for missing in (-9,-7,-5,-3,-1):
        levels=[t for t in range(-9,0) if t!=missing]
        outcomes=Counter()
        for mask in range(256):
            O={(-10,0),(-10,1),(0,0),(0,1)}|{(t,(mask>>i)&1) for i,t in enumerate(levels)}
            V,J=pair_count(O)
            assert (V,J)==(4,(missing+37)//2)
            direct=(J+V//2)%2
            normal=prior.validate(O,-1)
            assert sum(t%2==0 for t,r in normal)==V
            assert sum(u<v for u,r in normal for v,s in normal if u%2==0 and v%2)==J
            answer=prior.parity_screen(O,-1)
            if direct==0:assert answer['status']=='EXCLUDED'
            if answer['status']=='NOT_EXCLUDED':assert direct==1
            outcomes[answer['status']+':'+answer['reason']]+=1
        rows.append({'missing':missing,'V':V,'J':J,'index':direct,'masks':256,'outcomes':dict(outcomes)})
    assert [r['missing'] for r in rows if r['index']]==[-7,-3]
    # General single-missing layer formula: W=2k, k odd, missing=-2k+1+2j.
    general=0
    for k in range(1,100,2):
        for j in range(k):
            h=-2*k+1+2*j
            O={(-2*k,0),(-2*k,1),(0,0),(0,1)}|{(t,0)for t in range(-2*k+1,0)if t!=h}
            V,J=pair_count(O)
            assert V==k-1 and J==(k+2)*(k-1)//2+j
            assert (J+V//2)%2==j%2
            assert (j%2==1)==(h%4==1)
            general+=1
    # Countermodel only to the displayed necessary screens, not an HC seed.
    base={(1,0),(1,1),(2,0),(3,0),(5,1),(6,1),(11,0),(11,1)}
    growth_eight=[]
    for scale in (1,3,5,101,10**30+1):
        O={(scale*t,r)for t,r in base}
        result=prior.parity_screen(O,1)
        assert result['status']=='NOT_EXCLUDED'
        assert (result['growth'],result['vertical_odd_classes'],result['ordered_vertical_horizontal_pairs'])==(8,2,6)
        growth_eight.append({'scale':scale,'width':10*scale,'status':result['status']})
    # Full-vector restriction: dividing by gcd is forbidden.
    try:prior.parity_screen(base,1,(1,-1))
    except ValueError:pass
    else:raise AssertionError('Primitive drift wrongly substituted')
    report={'status':'passed','thin_case_masks':1280,'rows':rows,
            'general_single_gap_cases':general,'formal_growth8_controls':growth_eight,
            'scope':{'old_minus7_search_rerun':False,'old_standard_profile_search_rerun':False,
                     'drift_only_P104_proved':False,'formal_wakes_realized':False},
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(report,indent=2)+'\n',end='')

if __name__=='__main__':main()
