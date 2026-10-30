"""Complete sparse dynamics and an exact infinite-tail checker.

This implementation does not import the affine verifier or ISL.
"""
from __future__ import annotations
from collections import defaultdict

DIR=((0,1),(1,0),(0,-1),(-1,0))
STANDARD='RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR'
PHASES=frozenset(STANDARD[i:]+STANDARD[:i] for i in range(104))


def permanent(field,pose,word):
    """Check every epoch, including the final infinite interval, on full field."""
    x,y,h=pose;ph=[]
    for c in word:
        ph.append((x,y));h=(h+(1 if c=='R' else -1))%4
        dx,dy=DIR[h];x+=dx;y+=dy
    drift=(x-pose[0],y-pose[1])
    if h!=pose[2] or drift==(0,0):return False
    dx,dy=drift
    def epoch(q,p):
        a,b=q[0]-p[0],q[1]-p[1]
        if dx:
            if a%dx:return None
            k=a//dx
            if b!=k*dy:return None
        else:
            if a or b%dy:return None
            k=b//dy
        return k
    for i,p in enumerate(ph):
        changes=defaultdict(int);changes[0]=0
        for j,q in enumerate(ph):
            s=epoch(q,p)
            if s is not None and (s>0 or s==0 and j<i):changes[s]^=1
        for q in field:
            k=epoch(q,p)
            if k is not None and k>=0:changes[k]^=1;changes[k+1]^=1
        bit=0;want=int(word[i]=='L')
        for k in sorted(changes):
            bit^=changes[k]
            if bit!=want:return False
    return True


def run_until_highway(field,pose=(0,0,0),cap=2000000):
    """Return exact first permanent entrance and a complete certified checkpoint.

    A finite cap raises an exception, never a negative dynamical answer.
    """
    B=set(field);x,y,h=pose;turns=[]
    for t in range(cap+1):
        if t>=208 and t%104==0:
            last=''.join(turns[-104:])
            if last in PHASES and turns[-208:-104]==turns[-104:] and permanent(B,(x,y,h),last):
                start=t
                while start>0 and turns[start-1]==last[(start-1-t)%104]:start-=1
                return start,''.join(turns),B,(x,y,h),last
        if t==cap:break
        p=x,y
        if p in B:B.remove(p);h=(h-1)%4;turns.append('L')
        else:B.add(p);h=(h+1)%4;turns.append('R')
        dx,dy=DIR[h];x+=dx;y+=dy
    raise RuntimeError('INCONCLUSIVE: no certificate within the literal resource cap')


def rectangle(n,m):return {(x,y) for x in range(n) for y in range(m)}


def vector_replay(field,pose,steps):
    """Separate orientation representation: rotate the integer direction vector."""
    B=set(field);p=pose[:2];v=DIR[pose[2]];letters=[];footprint=set()
    for _ in range(steps):
        footprint.add(p)
        if p in B:B.remove(p);v=(-v[1],v[0]);letters.append('L')
        else:B.add(p);v=(v[1],-v[0]);letters.append('R')
        p=(p[0]+v[0],p[1]+v[1])
    return ''.join(letters),B,(*p,DIR.index(v)),footprint


def chronological_permanent(B,pose,word):
    """Second infinite criterion, using stable ordered full translation classes.

    It neither uses parity-change breakpoints nor imports the affine checker.
    """
    x,y,h=pose;ph=[]
    for i,c in enumerate(word):
        ph.append(((x,y),i,c));h=(h+(1 if c=='R' else -1))%4
        dx,dy=DIR[h];x+=dx;y+=dy
    d=(x-pose[0],y-pose[1]);dx,dy=d
    if h!=pose[2] or d==(0,0):return False
    def key(q):
        x,y=q
        return (dy*x-dx*y,x%abs(dx)) if dx else (x,y%abs(dy))
    groups={}
    for q,i,c in ph:groups.setdefault(key(q),[]).append((q,i,c))
    K=set();rays={}
    for k,events in groups.items():
        b=events[0][0];ordered=[]
        for q,i,c in events:
            a=(q[0]-b[0])//dx if dx else (q[1]-b[1])//dy
            if q!=(b[0]+a*dx,b[1]+a*dy):raise AssertionError('Wrong full class')
            ordered.append((a,i,c))
        ordered.sort(key=lambda z:(-z[0],z[1]))
        if any(c!=('R' if i%2==0 else 'L') for i,(a,j,c) in enumerate(ordered)):return False
        lo=min(a for a,i,c in ordered);hi=max(a for a,i,c in ordered)
        rays[k]=(b,lo)
        for a in range(lo,hi):
            available=[c for aj,i,c in ordered if aj<=a]
            if available and available[0]=='L':K.add((b[0]+a*dx,b[1]+a*dy))
    if not K<=B:return False
    for q in B-K:
        k=key(q)
        if k not in rays:continue
        b,lo=rays[k];a=(q[0]-b[0])//dx if dx else (q[1]-b[1])//dy
        if a>=lo:return False
    return True
