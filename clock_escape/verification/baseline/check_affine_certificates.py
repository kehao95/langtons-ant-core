"""Verify finite-square additive clocks by exact integer inequalities.
The LP solver is not trusted. Every supplied coefficient is checked here.
The checker proves bounds for all fields, not only simulated seeds.
"""
import json
from pathlib import Path
from diagonal_clock import DIRS

ROOT=Path(__file__).resolve().parent

def check_one(cert):
    n=cert['n']; w=cert['weights']; pose=cert['pose_values']; bound=cert['escape_bound']
    assert len(w)==n and all(len(row)==n for row in w)
    assert all(type(v) is int for row in w for v in row)
    assert len(pose)==2*n*n and all(type(v) is int for v in pose)
    poses=[(x,y,h) for x in range(n) for y in range(n) for h in range(4)
           if h%2==(x+y)%2]
    original=dict(zip(poses,pose))
    span=sum(abs(v) for row in w for v in row)+max(pose)-min(pose)
    assert bound==span+1
    edges=0
    for sector in (1,-1):
        # Reflection (x,y)->(y,x), with color complementation, exchanges sectors.
        if sector==1:
            g=original
            weight=lambda x,y:w[x][y]
        else:
            g={(y,x,(1-h)%4):v for (x,y,h),v in original.items()}
            weight=lambda x,y:-w[y][x]
        for (x,y,h),v in g.items():
            for black in (False,True):
                nh=(h+(-1 if black else 1))%4
                dx,dy=DIRS[nh]; dest=(x+dx,y+dy,nh)
                if dest not in g: continue
                delta=g[dest]-v+(-1 if black else 1)*weight(x,y)
                assert delta>=1, (n,sector,(x,y,h),black,delta)
                edges+=1
    return {'n':n,'all_colorings_escape_by':bound,'exact_directed_inequalities':edges}

if __name__=='__main__':
    certs=json.loads((ROOT/'affine_clock_certificates.json').read_text())
    out=[check_one(c) for c in certs]
    result={'status':'PASS','certificate_count':len(out),
            'both_sigma_sectors_checked':True,
            'exact_directed_inequalities':sum(x['exact_directed_inequalities'] for x in out),
            'bounds':out,
            'scope':'First exit from a finite square; not permanent escape and not HIGHWAY.'}
    (ROOT/'affine_certificate_checks.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
