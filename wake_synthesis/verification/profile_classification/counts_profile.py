"""Exact count relaxation for the 256 residue lifts of the standard layer profile."""
from functools import lru_cache
from itertools import product

LEVELS=(-9,-8,-7,-6,-5,-4,-2,-1)
STANDARD_MASK=sum(1<<i for i,t in enumerate(LEVELS) if t in (-9,-8,-4,-1))
def wake(mask):
    if type(mask) is not int or not 0 <= mask < 256:
        raise ValueError('mask must be an integer in 0..255')
    return frozenset({(-10,0),(-10,1),(0,0),(0,1)} | {(t,(mask>>i)&1) for i,t in enumerate(LEVELS)})

@lru_cache(None)
def counts(parity, incoming, outgoing, odd):
    if parity not in (0,1) or odd not in (0,1) or min(incoming,outgoing)<0:
        raise ValueError('invalid local count input')
    values=[]
    for a in range(incoming+1):
        m=2*(incoming+outgoing-2*a)+odd if parity==0 else 2*(outgoing-incoming+2*a)-odd
        if m>=0 and a<=(m+1)//2 and 0<=incoming-a<=m//2:
            values.append(m)
    return tuple(sorted(values))

def advance(frontier, row, W):
    o0,o1,i0,i1=frontier
    I=(o0,o1) if row%2 else (o1,o0)
    J=(i1,i0) if row%2 else (i0,i1)
    for pair in product(*(counts(row%2,I[r],J[r],int((row,r) in W)) for r in (0,1))):
        m0,m1=pair
        new=(m0-J[0],m1-J[1],m0-I[0],m1-I[1])
        if min(new)>=0 and new[0]+new[1]>0:
            yield pair,new

def transform(frontier, row):
    a,b,c,d=frontier
    return (c,d,b,a) if row%2 else (d,c,a,b)

def tables(cap,mask,side='bottom'):
    if type(cap) is not int or not 2 <= cap <= 168 or side not in ('top','bottom'):
        raise ValueError('cap must be 2..168; side must be top or bottom')
    W=wake(mask)
    states={(1,1,1,1):2}
    out={-1 if side=='top' else -9:{(1,1,1,1):2}}
    rows=range(-1,-10,-1) if side=='top' else range(-9,0)
    step=-1 if side=='top' else 1
    for row in rows:
        nxt={}
        for frontier,old in states.items():
            for pair,new in advance(frontier,row,W):
                cost=old+sum(pair)
                if cost<=cap and cost<nxt.get(new,cap+1):
                    nxt[new]=cost
        states=nxt
        out[row+step]={transform(k,row):v for k,v in states.items()}
    return out

def serialize(tab):
    return ''.join(' '.join(map(str,(t,*k,v)))+'\n' for t,states in sorted(tab.items()) for k,v in sorted(states.items()))
