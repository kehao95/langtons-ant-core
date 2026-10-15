"""Independent modular and local-string audits for profile classification."""
from collections import Counter
from itertools import product
import json,time
from pathlib import Path
import counts_profile as c

def modular(mask):
    W=c.wake(mask);f=(1,1,1,1);res={0:(1,1),-10:(1,1)}
    for t in range(-1,-10,-1):
        o0,o1,i0,i1=f
        I=(o0,o1) if t%2 else (o1,o0)
        J=(i1,i0) if t%2 else (i0,i1)
        m=tuple((2*(I[r]+J[r])+(-1 if t%2 else 1)*int((t,r) in W))%4 for r in (0,1))
        res[t]=m
        f=tuple(v%2 for v in (m[0]-J[0],m[1]-J[1],m[0]-I[0],m[1]-I[1]))
    S=[sum(res[t][r] for t in range(-10,1) if t%2==parity)%4 for r in range(2) for parity in range(2)]
    status='boundary_parity_rejection' if f!=(1,1,1,1) else 'phase_mod4_rejection' if len(set(S))!=1 else 'pass'
    return {'mask':mask,'status':status,'bottom_boundary_mod2':f,'phase_sums_mod4':S,'period_residue_mod16':4*S[0] if status=='pass' else None}

def local_audit(max_m=12):
    """Truth table of every binary arrival string; no count formula generates it."""
    actual={}
    strings=0
    for m in range(max_m+1):
        for arrivals in product((0,1),repeat=m):
            strings+=1
            I=sum(arrivals)
            for parity in (0,1):
                J=sum((a^(k%2))^parity for k,a in enumerate(arrivals))
                actual.setdefault((parity,I,J,m%2),set()).add(m)
    cases=0
    for parity,I,J,odd in product(range(2),range(max_m+1),range(max_m+1),range(2)):
        expected={m for m in c.counts(parity,I,J,odd) if m<=max_m}
        assert expected==actual.get((parity,I,J,odd),set()),(parity,I,J,odd)
        cases+=1
    return {'arrival_strings':strings,'formula_cases':cases,'maximum_class_length':max_m}

def audit(lower):
    rows=[modular(m) for m in range(256)]
    dist=Counter(r['status'] for r in rows)
    assert dist=={'boundary_parity_rejection':128,'phase_mod4_rejection':88,'pass':40}
    assert all((r['status']=='pass')==(s['lower_bound'] is not None) for r,s in zip(rows,lower))
    for r in lower:
        if r['lower_bound'] is None:continue
        table=c.tables(168,r['mask'],'top')
        assert table[-10][(1,1,1,1)]+2==r['lower_bound']
    return {'modular_distribution':dict(dist),'masks':rows,'local_counts':local_audit(),
            'top_bottom_minimum_crosschecks':40}
