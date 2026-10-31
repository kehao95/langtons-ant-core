"""Exact finite trace interfaces; no HC or future-active deletion oracle.

The proofs of the all-m prefix bounds and Cantor--Bendixson derivative
are analytic. This module checks their finite semantics and the concrete
protected coding kernel. Initial fields are always complete.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
from math import comb
from typing import Iterable

Point=tuple[int,int]
DIR=((0,1),(1,0),(0,-1),(-1,0))
HERE=Path(__file__).resolve().parent
STANDARD_WORD=('RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRL'
               'LRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR')

@dataclass
class Run:
    field:set[Point]
    head:Point
    heading:int
    word:str
    reads:list[Point]

def move(p:Point,h:int)->Point:
    a,b=DIR[h];return p[0]+a,p[1]+b

def translate(field:Iterable[Point],v:Point)->set[Point]:
    return {(x+v[0],y+v[1])for x,y in field}

def simulate(initial:Iterable[Point],steps:int,head:Point=(0,0),heading:int=0)->Run:
    if type(steps)is not int or steps<0 or heading not in range(4):
        raise ValueError('invalid finite run')
    B=set(initial);p=head;h=heading;word=[];reads=[]
    for _ in range(steps):
        reads.append(p);black=p in B;word.append('L'if black else'R')
        B.symmetric_difference_update({p});h=(h+(3 if black else 1))%4;p=move(p,h)
    return Run(B,p,h,''.join(word),reads)

def first_black_code(word:str):
    """Same-cell alternation and its unique finite-prefix minimal source."""
    if set(word)-set('RL'):raise ValueError('not a turn word')
    last={};source=set();times=[];p=(0,0);h=0
    for t,c in enumerate(word):
        if p in last:
            if last[p]==c:raise ValueError('same-cell alternation conflict')
        elif c=='L':source.add(p);times.append(t)
        last[p]=c;h=(h+(1 if c=='R'else-1))%4;p=move(p,h)
    return tuple(times),source

def decode(length:int,times:Iterable[int])->Run:
    """Decode FIRST-black times; a marked revisit is rejected, not ignored."""
    marks=tuple(times)
    if type(length)is not int or length<0 or any(type(t)is not int for t in marks):
        raise ValueError('invalid clock data')
    if marks!=tuple(sorted(set(marks))) or any(t<0 or t>=length for t in marks):
        raise ValueError('times must be strictly increasing in the prefix')
    markset=set(marks);seen=set();B=set();p=(0,0);h=0;word=[];reads=[]
    for t in range(length):
        reads.append(p)
        if p in seen:
            if t in markset:raise ValueError('a first-black time marks a revisit')
        else:
            seen.add(p)
            if t in markset:B.add(p)
        black=p in B;word.append('L'if black else'R');B.symmetric_difference_update({p})
        h=(h+(3 if black else 1))%4;p=move(p,h)
    return Run(B,p,h,''.join(word),reads)

def kernel():
    w=json.loads((HERE/'witness.json').read_text())
    for key in ('p0','d','q'):w[key]=tuple(w[key])
    for key in ('C','Wres','Sres'):w[key]={tuple(p)for p in w[key]}
    return w

def zero_word(w):return w['W']*2

def source(bits:Iterable[int],w=None):
    w=kernel()if w is None else w;bits=tuple(bits)
    if any(type(b)is not int or b not in (0,1)for b in bits):raise ValueError('binary input required')
    x,y=w['p0'];qx,qy=w['q'];dx,dy=w['d']
    return {(x+qx+2*i*dx,y+qy+2*i*dy)for i,b in enumerate(bits)if b}

def predicted_word(bits:Iterable[int],w=None):
    w=kernel()if w is None else w;bits=tuple(bits)
    if any(type(b)is not int or b not in (0,1)for b in bits):raise ValueError('binary input required')
    return ''.join(w['S']if b else zero_word(w)for b in bits)

def predicted_endpoint(bits:Iterable[int],blank:Run,w=None)->Run:
    """Complete endpoint, including the entire untouched blank startup field."""
    w=kernel()if w is None else w;bits=tuple(bits);p0=w['p0'];d=w['d'];C=w['C']
    C0=translate(C,p0);B=blank.field-C0
    R0=w['Wres'] | translate(w['Wres'],d)
    for i,b in enumerate(bits):
        shift=p0[0]+2*i*d[0],p0[1]+2*i*d[1]
        residue=translate(w['Sres']if b else R0,shift)
        if B&residue:raise AssertionError('protected residual slabs overlap')
        B.update(residue)
    p=p0[0]+2*len(bits)*d[0],p0[1]+2*len(bits)*d[1]
    front=translate(C,p)
    if B&front:raise AssertionError('residual meets terminal front')
    B.update(front)
    return Run(B,p,w['h'],predicted_word(bits,w),[])

def verify_kernel(w=None):
    w=kernel()if w is None else w;C=w['C'];q=w['q'];d=w['d'];h=w['h']
    if len(C)!=21 or q in C or d!=(-2,-2)or h!=3:raise AssertionError('kernel data changed')
    if w['W']!=(STANDARD_WORD*2)[57:161]:raise AssertionError('wrong standard cycle phase')
    W=simulate(C,104,heading=h);S=simulate(C|{q},228,heading=h)
    for trial,word,factor,residue in ((W,w['W'],1,w['Wres']),(S,w['S'],2,w['Sres'])):
        end=factor*d[0],factor*d[1]
        if trial.word!=word or trial.head!=end or trial.heading!=h:raise AssertionError('kernel execution')
        if max(map(sum,trial.reads))>0:raise AssertionError('reads outside incoming half-plane')
        front=translate(C,end)
        if trial.field!=front|residue or front&residue:raise AssertionError('wrong complete output')
        if not all(sum(p)>sum(end)and sum(p)<=0 for p in residue):raise AssertionError('unsafe residue')
    A=simulate(C,208,heading=h)
    if A.word!=zero_word(w):raise AssertionError('two standard cycles changed')
    hits=[]
    for b,trial in ((0,A),(1,S)):
        # All nonnegative marker indices are covered without a guessed cutoff.
        for p in trial.reads:
            x=p[0]-q[0];y=p[1]-q[1]
            if x==y and x%(-4)==0 and x//(-4)>=0:
                hits.append((b,x//(-4)))
                if x//(-4)!=0:raise AssertionError('reads a later input marker')
        first=trial.reads.index(q)
        if first!=13:raise AssertionError('wrong decisive offset')
    if next(i for i,(a,b)in enumerate(zip(A.word,S.word))if a!=b)!=13:
        raise AssertionError('code is not distinguishable at claimed offset')
    blank=simulate(set(),w['t0'])
    if (blank.head,blank.heading)!=(w['p0'],h):raise AssertionError('startup pose')
    C0=translate(C,w['p0'])
    if {p for p in blank.field if sum(p)<=sum(w['p0'])}!=C0:
        raise AssertionError('startup front')
    q0=w['p0'][0]+q[0],w['p0'][1]+q[1]
    for p in blank.reads:
        x=p[0]-q0[0];y=p[1]-q0[1]
        if x==y and x%(-4)==0 and x//(-4)>=0:raise AssertionError('startup touches a marker')
    return blank,{'standard_phase_index':57,'front_cells':len(C),'startup_updates':w['t0'],'startup_black_cells':len(blank.field),
                  'standard_block':208,'marker_block':228,'common_displacement':[-4,-4],
                  'first_divergence_offset':13,'standard_residue_cells':24,'marker_residue_cells':25,
                  'whole_marker_ray_checked':True,'complete_endpoint_identities':True}

def prefix_upper(n:int,m:int)->int:
    if min(n,m)<0:raise ValueError('nonnegative inputs required')
    return sum(comb(n,j)for j in range(min(n,m)+1))

def positive_lower(n:int,m:int)->int:
    if min(n,m)<0:raise ValueError('nonnegative inputs required')
    length=max(0,(n-11017-20*m)//208)
    return prefix_upper(length,m)
