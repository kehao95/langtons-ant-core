"""Independent complete-field verifier for one supplied translating turn word.

This does not share event graph data, stable-rank constraints, or simulator source
with the native period enumeration. No finite-run repetition is treated as proof.
"""
from __future__ import annotations
from collections import defaultdict
DIR=((0,1),(1,0),(0,-1),(-1,0))

def walk(word, heading=1):
    if not word or set(word)-{'R','L'}:raise ValueError('nonempty R/L word')
    x=y=0;h=heading;reads=[]
    for c in word:
        reads.append((x,y))
        h=(h+(1 if c=='R' else -1))%4
        dx,dy=DIR[h];x+=dx;y+=dy
    return reads,(x,y),h

def finite_support_realization(word):
    reads,d,endh=walk(word)
    if d!=(2,-2) or endh!=1:raise ValueError('wrong heading or full drift')
    P=len(word)
    classes=defaultdict(list)
    for i,(x,y) in enumerate(reads):
        t=x+y;r=x%2;a=(x-r)//2
        classes[(t,r)].append((i,a,word[i]))
    source=set();odd=set()
    for (t,r),visits in classes.items():
        # At q=(r+2*n,t-r-2*n), visits are eligible when n>=a.
        # Exact chronology is by n*P+(i-P*a), thus by i-P*a.
        full=sorted(visits,key=lambda v:v[0]-P*v[1])
        if any(v[2]!=('R'if j%2==0 else'L') for j,v in enumerate(full)):
            raise ValueError('stabilized white chronology is impossible')
        if len(visits)%2:odd.add((t,r))
        for n in range(min(v[1]for v in visits),max(v[1]for v in visits)+1):
            available=sorted((v for v in visits if v[1]<=n),key=lambda v:v[0]-P*v[1])
            if available and available[0][2]=='L':source.add((r+2*n,t-r-2*n))
    # Independent breakpoint-parity checks for the COMPLETE infinite future.
    epochs=0
    for i,q in enumerate(reads):
        thresholds={0}
        for j,r in enumerate(reads):
            diff=(r[0]-q[0],r[1]-q[1])
            if diff[0]%2 or diff[1]!=-diff[0]:continue
            shift=diff[0]//2
            if shift>0 or shift==0 and j<i:thresholds.add(shift)
        for p in source:
            diff=(p[0]-q[0],p[1]-q[1])
            if diff[0]%2 or diff[1]!=-diff[0]:continue
            shift=diff[0]//2
            if shift>=0:thresholds.update((shift,shift+1))
        for k in sorted(thresholds):
            point=(q[0]+2*k,q[1]-2*k)
            black=point in source
            earlier=sum(1 for j,r in enumerate(reads)
                if (r[0]-q[0])%2==0 and r[1]-q[1]==-(r[0]-q[0])
                and ((r[0]-q[0])//2>0 or ((r[0]-q[0])//2==0 and j<i))
                and (r[0]-q[0])//2<=k)
            isL=black^bool(earlier%2)
            if isL != (word[i]=='L'):
                raise AssertionError(('infinite actual turn mismatch',i,k))
            epochs+=1
    return {'period':P,'growth':word.count('R')-word.count('L'),
            'odd_wake':sorted(odd),'minimum_initial_black':sorted(source),
            'infinite_breakpoint_checks':epochs}

if __name__=='__main__':
    from pathlib import Path
    import json,sys
    obj=finite_support_realization(sys.argv[1]);print(json.dumps({k:(len(v)if k=='minimum_initial_black'else v)for k,v in obj.items()}))
