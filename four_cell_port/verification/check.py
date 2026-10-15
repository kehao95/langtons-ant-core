#!/usr/bin/env python3
"""Reproducible finite proof verifier: optimal 4-black half-plane gate.

Requires Python>=3.10 stdlib; no -O (uses explicit require checks).
The unbounded future is checked algebraically, not by finite simulation.
Run in the directory containing this file's evidence files.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
V=((0,1),(1,0),(0,-1),(-1,0)) # N,E,S,W
GATE=tuple(sorted(((0,-1),(1,1),(1,3),(2,2))))
SHARP=tuple(sorted(((0,-1),(2,1),(3,3))))
CANON='LRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLR'

def require(flag, message):
    if not flag: raise AssertionError(message)

def step(b,p,h):
    black=p in b
    if black: b.remove(p);h=(h-1)%4
    else: b.add(p);h=(h+1)%4
    return (p[0]+V[h][0],p[1]+V[h][1]),h,('L' if black else 'R')

def path(seed, n, start=(0,0), heading=1, halfplane=False):
    b=set(seed);p=start;h=heading;turns=[];read=[]
    for i in range(n):
        if halfplane: require(p[0]>=0, f'escaped before step {i}: {p}')
        read.append(p)
        p,h,c=step(b,p,h);turns.append(c)
    if halfplane: require(p[0]>=0, f'escaped at {n}: {p}')
    return b,p,h, ''.join(turns),read

def first_exit(seed, cap=920):
    b=set(seed);p=(0,0);h=1;first=[];seen=set()
    for t in range(cap+1):
        if p[0]<0:return t,p,tuple(sorted(first))
        if p not in seen:
            seen.add(p)
            if p not in seed:first.append(p)
        p,h,_=step(b,p,h)
    raise AssertionError(f'no first exit within {cap}: {seed}')

def list_escapes():
    layers=[(frozenset(),)]
    table=[]
    for depth in range(4):
        layer=layers[depth]
        vals=[];next_seeds=set()
        for s in layer:
            t,p,first=first_exit(s)
            vals.append({'seed': [list(q) for q in sorted(s)],'time':t,'exit':list(p)})
            for q in first:
                next_seeds.add(s|{q})
        vals.sort(key=lambda v:v['seed'])
        table.append(vals)
        if depth!=3: layers.append(tuple(sorted(next_seeds,key=lambda s: tuple(sorted(s)))))
    return table

def multiple(v,d):
    if d[0]!=0:
        if v[0]%d[0]: return None
        k=v[0]//d[0]
        return k if v[1]==k*d[1] else None
    if d[1]==0 or v[0] or v[1]%d[1]:return None
    return v[1]//d[1]

def geometry(p,h,w):
    q=[];a=p;heading=h
    for c in w:
        q.append(a)
        heading=(heading + (1 if c=='R' else -1))%4
        a=(a[0]+V[heading][0],a[1]+V[heading][1])
    d=a[0]-p[0],a[1]-p[1]
    require(heading==h and d!=(0,0),'not a nonzero translating word')
    return q,d

def validate_forever(b,p,h,w,halfplane=False):
    """Direct time-ordered XOR of ALL prescribed past reads at EACH phase ray.
    All colour changes are finite integer threshold/hit breakpoints; this exact
    check logically covers every k>=0 (including all untested large k).
    """
    q,d=geometry(p,h,w);total=0
    if halfplane: require(d[0]>0 and all(v[0]>=0 for v in q),'future outside halfplane')
    for i,qi in enumerate(q):
        thresholds=[];breaks={0}
        for j,qj in enumerate(q):
            s=multiple((qj[0]-qi[0],qj[1]-qi[1]),d)
            if s is not None and (s>0 or (s==0 and j<i)):
                thresholds.append(s);breaks.add(s)
        for q0 in b:
            k=multiple((q0[0]-qi[0],q0[1]-qi[1]),d)
            if k is not None and k>=0:breaks.add(k);breaks.add(k+1)
        for k in sorted(breaks):
            pos=qi[0]+k*d[0],qi[1]+k*d[1]
            black=(pos in b)^(sum(s<=k for s in thresholds)%2!=0)
            require(black==(w[i]=='L'),f'phase {i} epoch {k}: wrong colour')
            total+=1
    return {'drift':list(d),'breakpoint_tests':total,'phase_min_x':min(v[0] for v in q),'phase_max_x':max(v[0] for v in q)}

def minimal_seed(p,h,w):
    """Different all-future test: translation-class first-visit chronology."""
    q,d=geometry(p,h,w);groups=[]
    for i,qi in enumerate(q):
        for g in groups:
            anchor=g[0][1]
            a=multiple((qi[0]-anchor[0],qi[1]-anchor[1]),d)
            if a is not None:
                g.append((i,qi,a));break
        else:groups.append([(i,qi,0)])
    K=set()
    for g in groups:
        order=sorted(g,key=lambda v:(-v[2],v[0]))
        for index,(i,qi,a) in enumerate(order):
            require(w[i]==('R' if index%2==0 else 'L'),
                    f'wrong stable alternation {[(j,v) for j,_,v in order]}')
        levels=[x[2] for x in order]
        anchor=g[0][1]
        for n in range(min(levels),max(levels)):
            available=[item for item in order if item[2]<=n]
            require(bool(available),'empty finite boundary suffix')
            if w[available[0][0]]=='L':
                K.add((anchor[0]+n*d[0],anchor[1]+n*d[1]))
    return K,q,d,len(groups)

def validate_by_class(b,p,h,w):
    K,q,d,nclasses=minimal_seed(p,h,w)
    difference=set(b)^K
    for x in difference:
        for qi in q:
            k=multiple((x[0]-qi[0],x[1]-qi[1]),d)
            require(k is None or k<0, f'residual actually read: {x}')
    return {'canonical_black':len(K),'dormant_difference':len(difference),
            'classes':nclasses,'minimal_seed':[list(v) for v in sorted(K)]}

def verify():
    b,p,h,_,_=path([],9977,start=(0,0),heading=0)
    _,end,eh,w,_=path(b,104,start=p,heading=h)
    require(w==CANON,'pinned word changed')
    require(eh==h and (end[0]-p[0],end[1]-p[1])==(-2,-2),'wrong blank drift')
    blank=validate_forever(b,p,h,w)
    blank_class=validate_by_class(b,p,h,w)
    # Independent of the reference: certify every 0--3 support case by a
    # finite first-visit branching tree, not by enumerating a coordinate box.
    esc=list_escapes()
    counts=[len(x) for x in esc]
    maxes=[max(row['time'] for row in x) for x in esc]
    require(counts==[1,2,20,261],f'incomplete tree: {counts}')
    require(maxes==[2,38,106,918],f'bound failed: {maxes}')
    require(any(set(map(tuple,row['seed']))==set(SHARP) and row['time']==918 for row in esc[3]),
            'missing sharpness witness')
    # Deep test the exact winning four-black trajectory from (0,0),E.
    B,head,heading,word,reads=path(GATE,182,halfplane=True)
    require(head==(5,1) and heading==1 and len(B)==36,'wrong complete 182-state')
    require(all(x>=0 for x,y in reads),'invalid prefix guard')
    phase=CANON
    direct=validate_forever(B,head,heading,phase,halfplane=True)
    byclass=validate_by_class(B,head,heading,phase)
    require(direct['drift']==[2,2], 'not outward standard drift')
    # A remote marker ten trillion periods ahead must be detected symbolically:
    # a 104-step finite replay would NOT detect this corruption.
    qs,d=geometry(head,heading,phase)
    distant=qs[0][0]+10**13*d[0],qs[0][1]+10**13*d[1]
    require(distant not in B,'bad adversarial marker placement')
    try:
        validate_forever(B|{distant},head,heading,phase,halfplane=True)
    except AssertionError:pass
    else:raise AssertionError('remote black blocker went undetected')
    # Geometric rotation/translation of both physical port and orientation.
    for r in range(4):
        def transform(v):
            x,y=v
            for _ in range(r):x,y=y,-x
            return x+1000,y-1000
        rotated={transform(v) for v in GATE}
        rp=transform((0,0));rh=(1+r)%4
        rb,ep,eh,_,_=path(rotated,182,start=rp,heading=rh)
        require(ep==transform(head) and eh==(heading+r)%4 and
                rb=={transform(v) for v in B}, 'rotation equivariance failed')
    require((byclass['canonical_black'],byclass['dormant_difference'],byclass['classes'])==(13,23,22),
            'wrong tail decomposition')
    witness={'schema':'langtons-ant-4cell-port-v1',
             'seed':[list(q) for q in GATE],
             'reference':{'blank_entry':9977,'period':104,'word':CANON,'verified':blank,'classes':blank_class['classes']},
             'gate':{'updates_before_tail':182,'head':list(head),'heading':'E',
                     'black_after_182':[list(v) for v in sorted(B)],
                     'future':direct,'canonical_tail':byclass},
             'halfplane_exit':{'layers':counts,'max_first_exit':maxes,
                    'sharp_seed':[list(q) for q in SHARP],'sharp_time':918}}
    with open(HERE/'escapes.json','w') as f: json.dump(esc,f,ensure_ascii=False,indent=2);f.write('\n')
    with open(HERE/'witness.json','w') as f: json.dump(witness,f,ensure_ascii=False,indent=2);f.write('\n')
    out={'status':'PASS','layers':counts,'max_first_exit':maxes,
         'blank_tail_checks':blank,'gate_tail_checks':direct,
         'gate_certified_updates':182,'gate_black_after_182':len(B),
         'gate_dormant_residue':byclass['dormant_difference'],
         'far_future_blocker_rejected':True,'rotations_checked':4,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'escape_sha256':hashlib.sha256((HERE/'escapes.json').read_bytes()).hexdigest(),
         'witness_sha256':hashlib.sha256((HERE/'witness.json').read_bytes()).hexdigest()}
    with open(HERE/'report.json','w') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps(out,ensure_ascii=False))

if __name__=='__main__':verify()
