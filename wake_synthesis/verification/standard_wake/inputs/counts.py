"""Exact integer completion costs. These are necessary relaxations, not trajectories."""
from functools import lru_cache
from itertools import product

WAKE = frozenset({(-10,0),(-10,1),(-9,1),(-8,1),(-7,0),(-6,0),
                  (-5,0),(-4,1),(-2,0),(-1,1),(0,0),(0,1)})
O = WAKE
RESIDUES = ((1,1),(0,3),(2,3),(1,2),(1,0),(3,0),
            (2,3),(2,2),(3,2),(0,3),(1,1))

@lru_cache(None)
def counts(parity: int, incoming: int, outgoing: int, odd: int) -> tuple[int,...]:
    if parity not in (0,1) or odd not in (0,1) or min(incoming,outgoing)<0:
        raise ValueError('Invalid local count input')
    values=[]
    for a in range(incoming+1):
        m=(2*(incoming+outgoing-2*a)+odd if parity==0
           else 2*(outgoing-incoming+2*a)-odd)
        if m>=0 and a<=(m+1)//2 and 0<=incoming-a<=m//2:
            values.append(m)
    return tuple(sorted(values))

def transform(frontier, row):
    a,b,c,d=frontier
    return (c,d,b,a) if row%2 else (d,c,a,b)

def advance(frontier, row):
    o0,o1,i0,i1=frontier
    I=(o0,o1) if row%2 else (o1,o0)
    J=(i1,i0) if row%2 else (i0,i1)
    for pair in product(*(counts(row%2,I[r],J[r],int((row,r) in WAKE))
                          for r in (0,1))):
        m0,m1=pair
        new=(m0-J[0],m1-J[1],m0-I[0],m1-I[1])
        if min(new)>=0 and new[0]+new[1]>0:
            yield pair,new

def tables(cap: int, side: str='top'):
    """Cost of the unbuilt region. Retain the cheapest complete history per frontier."""
    if type(cap) is not int or not 1<=cap<=856 or side not in ('top','bottom'):
        raise ValueError('cap must be in 1..856; side top or bottom')
    states={(1,1,1,1):2}
    out={-1 if side=='top' else -9:{(1,1,1,1):2}}
    rows=range(-1,-10,-1) if side=='top' else range(-9,0)
    step=-1 if side=='top' else 1
    for row in rows:
        nxt={}
        for frontier,old in states.items():
            for pair,new in advance(frontier,row):
                cost=old+sum(pair)
                if cost<=cap and cost<nxt.get(new,cap+1):
                    nxt[new]=cost
        states=nxt
        out[row+step]={transform(k,row):v for k,v in states.items()}
    return out

def make(cap=104):
    return tables(cap,'top')

def serialize(tab):
    return ''.join(' '.join(map(str,(t,*k,v)))+'\n'
                   for t,states in sorted(tab.items()) for k,v in sorted(states.items()))

def optimal_profiles(cap=104, side='top'):
    """All minimum-cost count profiles, not all chronological realizations."""
    states={(1,1,1,1):(2,[[(1,1)]])}
    rows=range(-1,-10,-1) if side=='top' else range(-9,0)
    for row in rows:
        nxt={}
        for frontier,(old,paths) in states.items():
            for pair,new in advance(frontier,row):
                cost=old+sum(pair)
                if cost>cap: continue
                extensions=[path+[pair] for path in paths]
                if new not in nxt or cost<nxt[new][0]:nxt[new]=(cost,extensions)
                elif cost==nxt[new][0]:nxt[new][1].extend(extensions)
        states=nxt
    ans=states.get((1,1,1,1))
    if ans is None:return None,[]
    cost,paths=ans
    profiles=[path+[(1,1)] for path in paths]
    if side=='top':profiles=[p[::-1] for p in profiles]
    return cost+2,sorted(profiles)
