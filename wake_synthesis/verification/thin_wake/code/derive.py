"""Exact count reductions for thin width-ten wakes, drift (2,-2).

No candidate period or trajectory is declared realizable by these routines.
The modular tests are necessary conditions. Completion tables are exact lower
bounds for the remaining event counts, not substitutes for chronology.
"""
from __future__ import annotations
from functools import lru_cache
from itertools import product

RAILS=frozenset({(-10,0),(-10,1),(0,0),(0,1)})
HOLES=(-9,-7,-5,-3,-1)
ALPHA=(-50,32,-18,8,-2,0,-2,8,-18,32,-50)


def wake(hole: int, mask: int) -> frozenset[tuple[int,int]]:
    if type(hole) is not int or not -9<=hole<=-1:
        raise ValueError('hole must be an interior layer')
    if type(mask) is not int or not 0<=mask<256:
        raise ValueError('mask must have eight bits')
    rows=[t for t in range(-9,0) if t!=hole]
    return RAILS|frozenset((t,(mask>>i)&1) for i,t in enumerate(rows))


def density(hole: int) -> tuple[int,...]:
    return tuple(2 if t in(-10,0) else int(t!=hole) for t in range(-10,1))


def bound(hole: int) -> int:
    return -sum(a*b for a,b in zip(ALPHA,density(hole)))


@lru_cache(None)
def local_counts(parity: int, I: int, J: int, odd: int) -> tuple[int,...]:
    if parity not in(0,1) or odd not in(0,1) or min(I,J)<0:
        raise ValueError('invalid local count input')
    out=[]
    for a in range(I+1):
        m=2*(I+J-2*a)+odd if parity==0 else 2*(J-I+2*a)-odd
        if m>=0 and a<=(m+1)//2 and 0<=I-a<=m//2:
            out.append(m)
    return tuple(sorted(out))


def incoming(frontier, t):
    a,b,c,d=frontier
    return ((a,b),(d,c)) if t%2 else ((b,a),(c,d))


def transform(frontier,t):
    a,b,c,d=frontier
    return (c,d,b,a) if t%2 else(d,c,a,b)


def modular_trace(O, side='bottom'):
    if side not in('bottom','top'): raise ValueError('invalid side')
    f=(1,1,1,1); rows=range(-9,0) if side=='bottom' else range(-1,-10,-1)
    profile={-10:(1,1),0:(1,1)};history=[]
    for t in rows:
        I,J=incoming(f,t)
        m=tuple((2*(I[r]+J[r])+int((t,r)in O) if not t%2
                 else 2*(J[r]-I[r])-int((t,r)in O))%4 for r in (0,1))
        profile[t]=m
        f=tuple(x%4 for x in (m[0]-J[0],m[1]-J[1],m[0]-I[0],m[1]-I[1]))
        history.append([t,*m,*f])
    phase=tuple(sum(profile[t][r] for t in range(-10,1) for r in(0,1)
                    if 2*r+t%2==g)%4 for g in range(4))
    return {'frontier':list(f),'phase_residues':list(phase),'history':history,
            'possible':f==(1,1,1,1) and len(set(phase))==1,
            'period_mod16':4*phase[0] if len(set(phase))==1 else None}


def advance(frontier,t,O):
    I,J=incoming(frontier,t)
    for pair in product(*(local_counts(t%2,I[r],J[r],int((t,r)in O)) for r in(0,1))):
        a,b=pair
        f=(a-J[0],b-J[1],a-I[0],b-I[1])
        if min(f)>=0 and f[0]+f[1]>0: yield pair,f


def tables(cap: int,O,side: str):
    if type(cap) is not int or not 2<=cap<=856 or side not in('top','bottom'):
        raise ValueError('unsupported cap or direction')
    states={(1,1,1,1):2};out={-1 if side=='top' else -9:states.copy()}
    rows=range(-1,-10,-1) if side=='top' else range(-9,0)
    step=-1 if side=='top' else 1
    for t in rows:
        nxt={}
        for f,old in states.items():
            for pair,new in advance(f,t,O):
                cost=old+sum(pair)
                if cost<=cap and cost<nxt.get(new,cap+1):nxt[new]=cost
        states=nxt;out[t+step]={transform(f,t):c for f,c in states.items()}
    return out


def serialize(tab):
    return ''.join(' '.join(map(str,(t,*f,c)))+'\n' for t,rows in sorted(tab.items())
                   for f,c in sorted(rows.items()))


def survivors():
    return {h:[m for m in range(128,256) if modular_trace(wake(h,m))['possible']]
            for h in HOLES}
