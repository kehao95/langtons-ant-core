"""Independent literal geometry and all-future breakpoint verification."""
from collections import defaultdict
from math import lcm
D=((0,1),(1,0),(0,-1),(-1,0))
STANDARD='RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR'

def geometry(word,h=1):
    if not word or any(c not in 'RL' for c in word):raise ValueError('nonempty RL word required')
    p=(0,0);q=[];hs=[]
    for c in word:
        q.append(p);hs.append(h);h=(h+(1 if c=='R' else -1))%4
        p=(p[0]+D[h][0],p[1]+D[h][1])
    if h!=hs[0] or p==(0,0):raise ValueError('heading or nonzero drift')
    return q,hs,p

def multiple(v,d):
    j=0 if d[0] else 1
    if v[j]%d[j]:return None
    k=v[j]//d[j]
    return k if v==(k*d[0],k*d[1]) else None

def reconstruct(word,h=1):
    q,hs,d=geometry(word,h);P=len(word);groups=defaultdict(list)
    for i,(x,y) in enumerate(q):
        key=(d[0]*y-d[1]*x,x%abs(d[0])) if d[0] else (x,y%abs(d[1]))
        groups[key].append(i)
    B=set();ranks={};odd=[]
    for ids in groups.values():
        b=q[ids[0]];a={i:multiple((q[i][0]-b[0],q[i][1]-b[1]),d) for i in ids}
        assert all(v is not None for v in a.values())
        order=sorted(ids,key=lambda i:i-P*a[i])
        for k,i in enumerate(order):
            if word[i]!=('R' if k%2==0 else 'L'):raise ValueError('inconsistent stable class chronology')
            ranks[i]=k
        if len(ids)%2:odd.append(b)
        for n in range(min(a.values()),max(a.values())):
            available=[i for i in order if a[i]<=n]
            if available and word[available[0]]=='L':B.add((b[0]+n*d[0],b[1]+n*d[1]))
    return B,{'q':q,'headings':hs,'drift':d,'ranks':ranks,'odd_representatives':odd}

def verify_forever(B,word,h=1):
    q,hs,d=geometry(word,h); evaluations=0
    for i,v in enumerate(q):
        flips=[];hits=set();epochs={0}
        for j,w in enumerate(q):
            s=multiple((w[0]-v[0],w[1]-v[1]),d)
            if s is not None and (s>0 or s==0 and j<i):
                flips.append(s);epochs.update((s,s+1))
        for b in B:
            k=multiple((b[0]-v[0],b[1]-v[1]),d)
            if k is not None and k>=0:hits.add(k);epochs.update((k,k+1))
        for k in epochs:
            read=(int(k in hits)+sum(s<=k for s in flips))%2
            if read!=int(word[i]=='L'):return False,{'phase':i,'epoch':k,'read':read}
            evaluations+=1
    return True,{'evaluations':evaluations}

def is_standard(word):
    n=lcm(len(word),104)
    return [s for s in range(104) if all(word[i%len(word)]==STANDARD[(s+i)%104] for i in range(n))]

