"""Eight-factor counterfamily; infinite precolouring is NOT a finite HC input."""
from __future__ import annotations
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'immediate_distance/baseline'))
from periodic_verify import D, STANDARD, geometry, multiple

WORD='LLLLRRLLRRRRLLRRLRLLRR'
BOUNDARY={(0,-1),(1,-1),(2,-1)}
RAYS=[(-1,1),(-2,1),(0,0),(-1,0),(-1,-1)]
DRIFT=(-3,1)

def data(word):
    P=len(word);q,heads,d=geometry(word,0)
    if d==(0,0):raise ValueError('nonzero drift required')
    groups={}
    for i,(x,y) in enumerate(q):
        key=(d[0]*y-d[1]*x,x%abs(d[0])) if d[0] else (x,y%abs(d[1]))
        groups.setdefault(key,[]).append(i)
    boundary=set();rays=[];first_phases=[];class_data=[]
    for key,indices in sorted(groups.items()):
        b=q[indices[0]]
        shifts={i:multiple((q[i][0]-b[0],q[i][1]-b[1]),d) for i in indices}
        order=sorted(indices,key=lambda i:i-P*shifts[i])
        if any(word[a]==word[c] for a,c in zip(order,order[1:])):
            raise ValueError('nonalternating full-drift class')
        lo,hi=min(shifts.values()),max(shifts.values())
        for k in range(lo,hi):
            active=[i for i in order if shifts[i]<=k]
            if word[active[0]]=='L':boundary.add((b[0]+k*d[0],b[1]+k*d[1]))
        first=order[0]
        if word[first]=='L':
            assert shifts[first]==hi
            origin=(b[0]+hi*d[0],b[1]+hi*d[1])
            rays.append(origin);first_phases.append(first)
        class_data.append({'key':list(key),'indices':order,'stable_word':''.join(word[i] for i in order),
                           'first_is_L':word[first]=='L'})
    return q,d,boundary,rays,first_phases,class_data


def epoch_check(word, boundary, rays, n=None):
    """Initial field = boundary plus rays (or exactly n sites per ray).

    Return first mismatch by all breakpoints, or certify the complete infinite
    execution. When n is finite even astronomically large, this represents a
    COMPLETE FINITE input with white exterior, not infinite storage.
    """
    P=len(word);q,_,d=geometry(word,0);first=None;evaluations=0
    for i,z in enumerate(q):
        hits=set()
        for b in boundary:
            k=multiple((b[0]-z[0],b[1]-z[1]),d)
            if k is not None and k>=0:hits.add(k)
        intervals=[]
        for a in rays:
            start=multiple((a[0]-z[0],a[1]-z[1]),d)
            if start is not None:intervals.append((start,None if n is None else start+n))
        links=[]
        for j,a in enumerate(q):
            s=multiple((a[0]-z[0],a[1]-z[1]),d)
            if s is not None and (s>0 or (s==0 and j<i)):links.append(s)
        breaks={0}|hits|{k+1 for k in hits}|set(links)
        for a,b in intervals:
            if a>=0:breaks.add(a)
            if b is not None and b>=0:breaks.add(b)
        for k in sorted(breaks):
            initial=(k in hits) or any(a<=k and (b is None or k<b) for a,b in intervals)
            colour=(int(initial)+sum(s<=k for s in links))%2
            evaluations+=1
            if colour!=int(word[i]=='L'):
                bad=k*P+i
                if first is None or bad<first:first=bad
    return {'valid_forever':first is None,'first_mismatch':first,'evaluations':evaluations}


def literal(seed, word, stop):
    black=set(seed);p=(0,0);h=0
    for t in range(stop+1):
        c='L' if p in black else 'R'
        if c!=word[t%len(word)]:return t,black,p,h,c
        if t==stop:break
        black.symmetric_difference_update((p,));h=(h+(1 if c=='R' else -1))%4
        p=(p[0]+D[h][0],p[1]+D[h][1])
    return None,black,p,h,None


def verify():
    word=WORD;P=len(word)
    q,d,boundary,rays,phases,classes=data(word)
    assert P==22 and d==DRIFT and boundary==BOUNDARY and rays==RAYS
    assert min(phases)==0 and (0,0) in rays and len(classes)==8
    assert word.count('R')==word.count('L')==11
    assert not any(P%k==0 and word==word[:k]*(P//k) for k in range(1,P))
    assert all(multiple((b[0]-a[0],b[1]-a[1]),d) is None or
               multiple((b[0]-a[0],b[1]-a[1]),d)<0 for b in boundary for a in rays)
    assert len({(d[0]*a[1]-d[1]*a[0],a[0]%abs(d[0])) for a in rays})==5
    allowed={(STANDARD*2)[i:i+8] for i in range(104)}
    assert all((word*2)[i:i+8] in allowed for i in range(P))
    nine={(STANDARD*2)[i:i+9] for i in range(104)}
    bad9=sum((word*2)[i:i+9] not in nine for i in range(P));assert bad9>0
    infinite=epoch_check(word,boundary,rays);assert infinite['valid_forever']
    controls=[];literal_updates=0
    for n in (0,1,2,3,5,12,32,1000,10**60):
        result=epoch_check(word,boundary,rays,n)
        assert not result['valid_forever'] and result['first_mismatch']==22*n
        item={'n':str(n),'complete_initial_black_count':str(3+5*n),
              'first_mismatch':str(22*n),'mass_deficit':str(66*n),
              'epoch_breakpoints':result['evaluations']}
        if n<=32:
            seed=set(boundary)|{(a[0]+k*d[0],a[1]+k*d[1]) for a in rays for k in range(n)}
            assert len(seed)==3+5*n
            mismatch,B,p,h,actual=literal(seed,word,22*n)
            assert mismatch==22*n and actual=='R' and p==(-3*n,n) and h==0
            assert len(B)==len(seed)
            # Second simulator uses complex rotations and integer-valued complex coordinates.
            C={complex(x,y) for x,y in seed};z=0j;v=1j
            for t in range(22*n):
                occupied=z in C
                assert ('L' if occupied else 'R')==word[t%P]
                if occupied:C.remove(z);v*=1j
                else:C.add(z);v*=-1j
                z+=v
            assert C=={complex(x,y) for x,y in B} and z==complex(*p) and v==1j
            literal_updates+=44*n;item['two_literal_replays']=True
        controls.append(item)
    return {'word':word,'period':P,'heading':0,'drift':list(d),'R':11,'L':11,
        'eight_legal':True,'cyclic_nine_illegal_count':bad9,
        'finite_boundary':sorted(boundary),'required_infinite_black_ray_origins':rays,
        'full_translation_classes':classes,'infinite_epoch_certificate':infinite,
        'finite_truncations':controls,'independent_literal_updates':literal_updates,
        'scope':'3+5n FINITE black cells give a 22n-step prefix, not a permanent nonstandard highway; no HC negative is asserted.'}
