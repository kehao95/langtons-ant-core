#!/usr/bin/env python3
"""Exact all-parameter finite-word certificate and full-field controls.

Only this supplied one-parameter family is certified. No search timeout, finite
simulation, or successful verification here is a global HC proof. Universal
coverage uses affine interval order stability proved in the accompanying note.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
DIRS = ((0,1),(1,0),(0,-1),(-1,0))
BASE = '11894a516e40fef9be730e266936071c7750142c'


def require(test, message):
    if not test:
        raise AssertionError(message)


def integer(n):
    if type(n) is not int or n < 0:
        raise ValueError('n must be a nonnegative integer')


def geometry(word, position=(0,0), heading=0):
    if not word or set(word)-{'L','R'}:
        raise ValueError('nonempty R/L word required')
    p,h=position,heading
    points=[]
    for letter in word:
        points.append(p)
        h=(h+(1 if letter=='R' else -1))%4
        dx,dy=DIRS[h];p=(p[0]+dx,p[1]+dy)
    return points,p,h


def literal(black, p, h, count):
    """Independent mutable integer-vector dynamics, complete input retained."""
    b=set(black); letters=[]; points=[]
    for _ in range(count):
        points.append(p)
        is_black=p in b
        letters.append('L' if is_black else 'R')
        if is_black:b.remove(p)
        else:b.add(p)
        h=(h+(-1 if is_black else 1))%4
        dx,dy=DIRS[h];p=p[0]+dx,p[1]+dy
    return b,p,h,''.join(letters),points


def inverse_suffix(black,p,h,count=9):
    b=set(black); backwards=[]
    for _ in range(count):
        dx,dy=DIRS[h];p=p[0]-dx,p[1]-dy
        was_right=p in b
        backwards.append('R' if was_right else 'L')
        if was_right:b.remove(p)
        else:b.add(p)
        h=(h+(-1 if was_right else 1))%4
    return ''.join(backwards[::-1])


def minimal_seed(word):
    points,p,h=geometry(word)
    prior={};black=set()
    for i,(q,c) in enumerate(zip(points,word)):
        if q in prior:
            require(c != prior[q], f'nonalternation at {q}, update {i}')
        elif c=='L':black.add(q)
        prior[q]=c
    return black


def power_word(blocks,n):
    integer(n)
    return ''.join(b['word']*(b['count'][0]*n+b['count'][1]) for b in blocks)


@dataclass(frozen=True)
class Record:
    """Reads of (x,r-4k), L(n)<=k<=U(n); order key is (block,order)."""
    x:int
    r:int
    low:tuple[int,int]
    high:tuple[int,int]
    block:int
    order:int
    letter:str
    time:tuple[int,int,int] # a*n+b*k+c


def ev(a,n):return a[0]*n+a[1]


def records(blocks):
    """Derive records from literal turn/move geometry, not a guessed path."""
    x,ya,yb,h,ta,tb=0,0,0,0,0,0
    out=[];boundaries=[]
    for bi,block in enumerate(blocks):
        word=block['word'];c,d=block['count']
        require(type(c) is int and type(d) is int and c in (0,1) and d>0,'count contract')
        require(c==1 or d==1,'fixed powers must be expanded')
        points,end,hh=geometry(word,(x,yb),h)
        dx,dy=end[0]-x,end[1]-yb
        P=len(word)
        if c:
            require(h==hh and dx==0 and dy in (-4,4),'variable block drift contract')
        for i,(px,py) in enumerate(points):
            require(ya%4==0,'nonintegral phase coefficient')
            r=py%4;alpha=-ya//4;beta=(r-py)//4
            if c and dy==-4:
                low=(alpha,beta);high=(alpha+1,beta+d-1)
                order=i-P*beta;time=(ta-P*alpha,P,tb+order)
            elif c:
                low=(alpha-1,beta-d+1);high=(alpha,beta)
                order=i+P*beta;time=(ta+P*alpha,-P,tb+order)
            else:
                low=high=(alpha,beta);order=i;time=(ta,0,tb+i)
            require(low[0] in (0,1) and high[0] in (0,1),'endpoint slopes must be 0 or 1')
            out.append(Record(px,r,low,high,bi,order,word[i],time))
        ta+=P*c;tb+=P*d
        if c:ya+=dy;yb+=d*dy
        else:x,yb,h=end[0],end[1],hh
        boundaries.append(dict(x=x,ya=ya,yb=yb,h=h,time=[ta,tb]))
    return out,boundaries


def grouped(recs):
    out=defaultdict(list)
    for r in recs:out[(r.x,r.r)].append(r)
    return {q:sorted(rs,key=lambda r:(r.block,r.order)) for q,rs in out.items()}


def bound_for_orders(groups, extras=None):
    """Past N every integer affine breakpoint has fixed ordering.

    Slopes 0 and 1 have only integral crossings; N is beyond ALL nonnegative
    crossings. Adding constant query-cell boundaries also freezes their bits.
    """
    maximum=0;pairs=0;functions=0
    for q,rs in groups.items():
        endpoints={r.low for r in rs}|{(r.high[0],r.high[1]+1) for r in rs}
        endpoints.update((extras or {}).get(q,()))
        functions+=len(endpoints)
        const={b for a,b in endpoints if a==0};moving={b for a,b in endpoints if a==1}
        require(all(a in (0,1) for a,b in endpoints),'unsupported slope')
        pairs+=len(const)*len(moving)
        for b0 in const:
            for b1 in moving:maximum=max(maximum,b0-b1)
    return maximum+1,functions,pairs


def sweep(groups,n):
    """Yield nonempty integer intervals with their complete chronological reads."""
    for q,rs in sorted(groups.items()):
        events=defaultdict(list)
        for j,r in enumerate(rs):
            lo,hi=ev(r.low,n),ev(r.high,n)
            require(lo<=hi,'empty read interval')
            events[lo].append((j,1));events[hi+1].append((j,-1))
        keys=sorted(events);active=set()
        for i,k in enumerate(keys[:-1]):
            for j,sgn in events[k]:
                if sgn==1:active.add(j)
                else:active.remove(j)
            if active and keys[i+1]>k:
                yield q,k,keys[i+1]-1,[rs[j] for j in sorted(active)]


def interval_fields(groups,n, fold_blocks=5):
    source=set();post=set();final=set();foot=set();checks=0
    for (x,r),lo,hi,rs in sweep(groups,n):
        pre=[z for z in rs if z.block<fold_blocks]
        if pre:
            bit=int(pre[0].letter=='L')
        else:
            bit=0
            require(rs[0].letter=='R','recovery demands unprovided initial black')
        v=bit
        for z in rs:
            require(v==int(z.letter=='L'),f'colour conflict n={n}, {(x,r,lo)}, {z}')
            v^=1;checks+=1
        # Post event is the first recovery read: index zero of block 5.
        num=sum(z.block<5 or (z.block==5 and z.order==0) for z in rs)
        post_bit=bit^(num%2)
        cells={(x,r-4*k) for k in range(lo,hi+1)}
        if pre:foot.update(cells)
        if bit:source.update(cells)
        if post_bit:post.update(cells)
        if v:final.update(cells)
    return source,post,final,foot,checks


def affine_mass(groups,n,which):
    """Coefficients of mass for n above all endpoint crossings."""
    total=[0,0]
    for q,rs in groups.items():
        funcs={r.low for r in rs}|{(r.high[0],r.high[1]+1) for r in rs}
        ordered=sorted(funcs,key=lambda a:(ev(a,n),a))
        for left,right in zip(ordered,ordered[1:]):
            k=ev(left,n)
            if ev(right,n)<=k:continue
            active=[z for z in rs if ev(z.low,n)<=k<=ev(z.high,n)]
            if not active:continue
            pre=[z for z in active if z.block<5]
            bit=int(bool(pre) and pre[0].letter=='L')
            if which=='post':bit^=sum(z.block<5 or (z.block==5 and z.order==0) for z in active)%2
            if which=='final':bit^=len(active)%2
            if bit:
                total[0]+=right[0]-left[0];total[1]+=right[1]-left[1]
    return total


def multiple(v,d):
    axis=0 if d[0] else 1
    if not d[axis] or v[axis]%d[axis]:return None
    k=v[axis]//d[axis]
    return k if (k*d[0],k*d[1])==v else None


def parity_tail(black,p,h,word):
    """Full infinite-tail parity at EVERY finite breakpoint and final ray."""
    pts,end,hh=geometry(word,p,h);d=(end[0]-p[0],end[1]-p[1])
    if hh!=h or d==(0,0):return False,0
    checks=0
    for i,q in enumerate(pts):
        thresholds=[]
        for j,z in enumerate(pts):
            a=multiple((z[0]-q[0],z[1]-q[1]),d)
            if a is not None and (a>0 or (a==0 and j<i)):thresholds.append(a)
        hits=set()
        for z in black:
            a=multiple((z[0]-q[0],z[1]-q[1]),d)
            if a is not None and a>=0:hits.add(a)
        for k in {0,*thresholds,*hits,*(a+1 for a in hits)}:
            checks+=1
            if (int(k in hits)+sum(a<=k for a in thresholds))%2 != int(word[i]=='L'):
                return False,checks
    return True,checks


def stable_class_tail(black,p,h,word):
    """Independent ordered-class criterion + finite clean-seed/ray comparison."""
    points,end,hh=geometry(word,p,h);d=end[0]-p[0],end[1]-p[1]
    if h!=hh or d==(0,0):return False
    groups=[]
    for i,q in enumerate(points):
        for anchor,items in groups:
            k=multiple((q[0]-anchor[0],q[1]-anchor[1]),d)
            if k is not None:
                items.append((k,i));break
        else:groups.append((q,[(0,i)]))
    needed=set()
    for anchor,items in groups:
        ordered=sorted(items,key=lambda z:(-z[0],z[1]))
        if any(word[i] != ('R' if j%2==0 else 'L') for j,(a,i) in enumerate(ordered)):
            return False
        low=min(a for a,i in items);high=max(a for a,i in items)
        for k in range(low,high):
            eligible=[(a,i) for a,i in ordered if a<=k]
            if eligible and word[eligible[0][1]]=='L':
                needed.add((anchor[0]+k*d[0],anchor[1]+k*d[1]))
    for q in black^needed:
        if any((k:=multiple((q[0]-z[0],q[1]-z[1]),d)) is not None and k>=0 for z in points):
            return False
    return True


def rot(p,r):
    x,y=p
    for _ in range(r):x,y=y,-x
    return x,y


def masks_and_caps(groups):
    source,post,final,foot,_=interval_fields(groups,1)
    I={};O={}
    for x in range(-5,3):
        for r in range(4):
            q=x,-12+r
            if q in foot:I[(x,r)]=int(q in source)
            O[(x,r)]=int(q in post)
    require(len(I)==28 and sum(I.values())==10 and sum(O.values())==18,'bulk mask')
    def caps(field):
        top=sorted(q for q in field if q[1]>=-8)
        bottom=sorted((x,y+4) for x,y in field if y<=-13)
        return {'top':top,'bottom':bottom}
    return I,O,caps(source),caps(post)


def field_template(n,mask,caps):
    result={tuple(q) for q in caps['top']}|{(x,y-4*n) for x,y in caps['bottom']}
    for j in range(n):
        for (x,r),bit in mask.items():
            if bit:result.add((x,-12-4*j+r))
    return result


def repair_table(I,O):
    tables={}
    for turn in (0,2):
        rows=[]
        for dx in range(-12,13):
            for dy in range(4):
                wrong=0
                for (x,r),bit in I.items():
                    xx,rr=rot((x,r),turn);xx+=dx;rr=(rr+dy)%4
                    wrong+=O.get((xx,rr),0)!=bit
                rows.append([dx,dy,wrong])
        require(min(v[2] for v in rows)==4,'parallel reset lower bound')
        tables[str(turn)]=rows
    return tables


def template_endpoints(I,O,sc,pc):
    extra=defaultdict(set)
    for mask,caps in ((I,sc),(O,pc)):
        for (x,r),bit in mask.items():
            # Include white visited cells too: the footprint is part of the claim.
            extra[x,r].update(((0,3),(1,3))) # k=3,...,n+2
        for moving,cap in ((0,caps['top']),(1,caps['bottom'])):
            for x,y in cap:
                r=y%4;b=(r-y)//4
                extra[x,r].update(((moving,b),(moving,b+1)))
    return extra


