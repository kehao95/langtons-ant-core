"""Separate exact infinite-tail verifier; no enumeration graph or pruning is used."""
from collections import defaultdict
MOVES=((0,1),(1,0),(0,-1),(-1,0))
STANDARD='RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR'

def plan(word, heading=1):
    if not word or set(word)-set('RL') or heading not in range(4):
        raise ValueError('invalid word or heading')
    x=y=0;h=heading;points=[]
    for turn in word:
        points.append((x,y))
        h=(h+(1 if turn=='R' else -1))%4
        dx,dy=MOVES[h];x+=dx;y+=dy
    if h!=heading or (x,y)==(0,0):raise ValueError('not a heading-restoring drift word')
    return points,(x,y)

def synthesize(word):
    points,d=plan(word)
    if d!=(2,-2):raise ValueError('expected drift (2,-2)')
    P=len(word);classes=defaultdict(list)
    for i,(x,y) in enumerate(points):classes[x+y,x%2].append((i-P*(x//2),i,x//2))
    wake=set();seed=set()
    for (t,r),visits in classes.items():
        chronological=sorted(visits)
        if any(word[i]!=('R' if k%2==0 else 'L') for k,(_,i,_) in enumerate(chronological)):
            raise ValueError('fails stabilized alternating criterion')
        if len(visits)%2:wake.add((t,r))
        offsets=[a for _,_,a in visits]
        for n in range(min(offsets),max(offsets)):
            if sum(a>n for a in offsets)%2:seed.add((r+2*n,t-r-2*n))
    return seed,wake,d

def multiple(v,d):
    x,y=v;a,b=d
    if a:
        if x%a:return None
        k=x//a
        return k if y==k*b else None
    if x or y%b:return None
    return y//b

def forever(seed,word,heading=1):
    """Check all constant intervals of the exact epoch-color formula, including infinity."""
    points,d=plan(word);B=set(seed)
    for i,p in enumerate(points):
        old_hits=set();thresholds=[]
        for z in B:
            s=multiple((z[0]-p[0],z[1]-p[1]),d)
            if s is not None and s>=0:old_hits.add(s)
        for j,q in enumerate(points):
            s=multiple((q[0]-p[0],q[1]-p[1]),d)
            if s is not None and (s>0 or s==0 and j<i):thresholds.append(s)
        probes={0,*thresholds,*old_hits,*(s+1 for s in old_hits)}
        for epoch in probes:
            color=int(epoch in old_hits)^ (sum(s<=epoch for s in thresholds)%2)
            if color!=int(word[i]=='L'):return False
    return True

def primitive_period(word):
    return next(p for p in range(1,len(word)+1) if len(word)%p==0 and word==word[:p]*(len(word)//p))
