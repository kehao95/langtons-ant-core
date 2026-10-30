"""Exact finite controls for the all-a cyclic-descent theorem; no core imports."""
from collections import Counter
from itertools import permutations
from math import factorial
import json


def eulerian(n):
    row=[1]
    for m in range(2,n+1):
        row=[(k+1)*(row[k] if k<len(row) else 0)
             +(m-k)*(row[k-1] if k else 0) for k in range(m)]
    return row


def check():
    report={}
    for a in (4,6,8):
        hist=Counter(); excluded=0
        for row_order in permutations(range(a)):
            rank=[0]*a; xs=[]
            for row,e in enumerate(row_order):
                rank[e]=row
                xs.extend(sorted((e,(e+1)%a)))
            I=sum(xs[i]>xs[j] for i in range(2*a) for j in range(i+1,2*a))
            D=sum(rank[j]>rank[(j+1)%a] for j in range(a))
            assert I%2==D%2
            O={(x,2*y) for y in range(a) for x in xs[2*y:2*y+2]}
            assert len(O)==2*a
            assert all(sum((-1)**((x+y)%2) for xx,y in O if xx==x)%4==2 for x in range(a))
            assert all(sum((-1)**((x+y)%2) for x,yy in O if yy==y)==0 for y in range(0,2*a,2))
            hist[D]+=1; excluded+=I%2
        expected={k+1:a*v for k,v in enumerate(eulerian(a-1))}
        assert hist==expected
        assert excluded==a*sum(eulerian(a-1)[::2])
        report[str(a)]={'total':factorial(a),'excluded':excluded,
                        'not_excluded':factorial(a)-excluded,
                        'cyclic_descent_histogram':dict(sorted(hist.items()))}
    return {'schema':'axis-cycle-count-v1','cases':report,
            'total_assignments':sum(v['total'] for v in report.values())}

if __name__=='__main__': print(json.dumps(check(),indent=2,sort_keys=True))
