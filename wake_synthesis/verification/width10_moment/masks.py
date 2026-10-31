"""Complete 11-layer full-drift (2,-2) odd-wake generator, exact integers.

The port-count DP is supplied separately by count_screen.cpp. Here every
acceptance is only NOT_EXCLUDED; it is NEVER a constructed ant trajectory.
"""
from __future__ import annotations
from collections import Counter
import hashlib,json
from pathlib import Path

DIR=Path(__file__).parent

def screen(a,b):
    if type(a)!=int or type(b)!=int or not 0<=a<2048 or not 0<=b<2048:raise ValueError('11-bit masks required')
    # At least one extreme class at bottom, and top r=0 is the phase anchor.
    if not a&1024 or not (a|b)&1:return None
    bits=([a>>j&1 for j in range(11)],[b>>j&1 for j in range(11)])
    c=[sum(row[::2]) for row in bits];q=[sum(row[1::2]) for row in bits]
    if any((c[r]-q[s])%4!=2 for r in range(2) for s in range(2)):return None
    growth=sum(c)+sum(q); V=sum(q)
    if growth not in (8,12,16) or V%2:return None
    pop=[bits[0][j]+bits[1][j] for j in range(11)]
    J=sum(pop[s]*pop[t] for s in range(1,10,2) for t in range(s+1,11,2))
    if (J+V//2)%2!=1:return None
    K=2*sum(((-1)**j)*(j-5)**2*pop[j] for j in range(11))
    if K>244 or K%4:raise AssertionError('moment exceeds inherited relaxed cap')
    return growth,K

def raw_masks():
    lane=[i for i in range(2048) if sum(((-1)**j)*(i>>j&1) for j in range(11))%4==2]
    masks=[]
    for a in lane:
        for b in lane:
            result=screen(a,b)
            if result is not None:masks.append((a,b,*result))
    if len(masks)!=13216:raise AssertionError('screen count changed')
    if Counter(g for a,b,g,k in masks)!=Counter({8:2676,12:8424,16:2116}):
        raise AssertionError('growth distribution changed')
    return masks

def canonical(accepted,allraw=None):
    # Each row is (lane0,lane1,g,K,min_count_period). Rows are exact count
    # relaxations, not physics. Translation by (1,-1) swaps lanes, keeping
    # t, full drift, parity sector and all physical turns unchanged.
    if allraw is None:allraw=set(raw_masks())
    rawpairs={(a,b)for a,b,*_ in allraw}
    seen={};swapped=0
    for a,b,g,k,P in accepted:
        if (a,b,g,k) not in allraw:raise AssertionError('accepted invalid wake')
        if P>k or P<4 or P%4:raise AssertionError('bad count lower bound')
        choice=(min(a,b),max(a,b)) if (a&1024 and b&1024) else (a,b)
        if a&1024 and b&1024 and a>b:swapped+=1
        prior=seen.setdefault(choice,(a,b,g,k,P))
        if prior[2:]!=(g,k,P):raise AssertionError('lane symmetry inconsistency')
    if len(accepted)!=2790 or len(seen)!=1914 or swapped!=876:
        raise AssertionError(('count or symmetry changed',len(accepted),len(seen),swapped))
    return sorted((a,b,g,k,P) if (a,b)==key else (*key,g,k,P) for key,(a,b,g,k,P) in seen.items())

def sha(obj):return hashlib.sha256(json.dumps(obj,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()

if __name__=='__main__':
    m=raw_masks();print(json.dumps({'normalized_screen':len(m),'by_growth':dict(Counter(g for _,_,g,_ in m)),'screen_digest':sha(m)},sort_keys=True))
