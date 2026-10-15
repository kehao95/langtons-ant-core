"""Exact finite-support LR macros with complete XOR segment histories.

A segment is FINITE: a+j*v for 0<=j<n. Overlap means XOR, never union.
This is an exact representation/acceleration, not a finite-state quotient,
future-live deletion, bounded-memory theorem, or a global halting decider.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import gcd, lcm
from typing import Iterable
from memory_delay import DIRS, State, multiple, suffix_predict

Point = tuple[int, int]

def add(a: Point, b: Point) -> Point:
    return a[0]+b[0], a[1]+b[1]

def sub(a: Point, b: Point) -> Point:
    return a[0]-b[0], a[1]-b[1]

def mul(k: int, a: Point) -> Point:
    return k*a[0], k*a[1]

def cross(a: Point, b: Point) -> int:
    return a[0]*b[1]-a[1]*b[0]

def ceil_div(a: int, b: int) -> int:
    if b<=0: raise ValueError('positive denominator required')
    return -((-a)//b)

@dataclass(frozen=True)
class Segment:
    start: Point
    stride: Point
    length: int

    def __post_init__(self) -> None:
        if type(self.length) is not int or self.length<1:
            raise ValueError('segment length must be a positive integer')
        if any(type(z) is not int for p in (self.start,self.stride) for z in p):
            raise ValueError('integer coordinates required')
        if len(self.start)!=2 or len(self.stride)!=2:
            raise ValueError('two coordinates required')
        if self.length>1 and self.stride==(0,0):
            raise ValueError('nontrivial segment needs nonzero stride')

    def contains(self, p: Point) -> bool:
        if self.length==1: return p==self.start
        k=multiple(sub(p,self.start), self.stride)
        return k is not None and 0<=k<self.length

@dataclass(frozen=True)
class SymbolicState:
    terms: tuple[Segment,...]
    pos: Point=(0,0)
    heading: int=0

    def __post_init__(self) -> None:
        if type(self.heading) is not int or self.heading not in range(4):
            raise ValueError('invalid heading')
        if len(self.pos)!=2 or any(type(z) is not int for z in self.pos):
            raise ValueError('invalid position')

    def black(self, p: Point) -> bool:
        return bool(sum(s.contains(p) for s in self.terms)%2)

    @staticmethod
    def explicit(state: State) -> SymbolicState:
        return SymbolicState(tuple(Segment(q,(0,0),1) for q in sorted(state.black)),
                             state.pos,state.heading)

    def radius_upper(self) -> int:
        return max((max(abs(z-self.pos[i]) for i,z in enumerate(p))
                    for s in self.terms
                    for p in (s.start,add(s.start,mul(s.length-1,s.stride)))),default=0)

    def materialize(self, max_points: int=1_000_000) -> State:
        if sum(s.length for s in self.terms)>max_points:
            raise ValueError('explicit expansion cap exceeded')
        b=set()
        for s in self.terms:
            for j in range(s.length):
                p=add(s.start,mul(j,s.stride))
                if p in b: b.remove(p)
                else: b.add(p)
        return State(frozenset(b),self.pos,self.heading)

    def flip(self,p: Point, new_pos: Point, new_heading: int) -> SymbolicState:
        term=Segment(p,(0,0),1)
        terms=list(self.terms)
        if term in terms: terms.remove(term)
        else: terms.append(term)
        return SymbolicState(tuple(terms),new_pos,new_heading)


def step(x: SymbolicState) -> tuple[SymbolicState,str]:
    ch='L' if x.black(x.pos) else 'R'
    h=(x.heading+(-1 if ch=='L' else 1))%4
    return x.flip(x.pos,add(x.pos,DIRS[h]),h), ch


def predecessor(x: SymbolicState) -> tuple[SymbolicState,str]:
    q=sub(x.pos,DIRS[x.heading]); ch='R' if x.black(q) else 'L'
    h=(x.heading+(-1 if ch=='R' else 1))%4
    return x.flip(q,q,h),ch


def preceding_turns(x: SymbolicState,D: int) -> str:
    chars=[]
    for _ in range(D): x,ch=predecessor(x);chars.append(ch)
    return ''.join(reversed(chars))


def geometry(x: SymbolicState, word: str):
    if not word or set(word)-{'R','L'}: raise ValueError('nonempty R/L word required')
    p=x.pos;h=x.heading;ps=[];hs=[]
    for ch in word:
        ps.append(p);hs.append(h)
        h=(h+(1 if ch=='R' else -1))%4;p=add(p,DIRS[h])
    return ps,hs,h,sub(p,x.pos)


def ray_segment_epochs(q: Point,d: Point,s: Segment) -> tuple[int,int,int,int]|None:
    """All k>=0 with q+k*d in s: lo<=k<=hi and k==residue mod modulus."""
    if d==(0,0): raise ValueError('nonzero ray direction required')
    if s.length==1:
        k=multiple(sub(s.start,q),d)
        return None if k is None or k<0 else (k,k,0,1)
    v=s.stride; c=sub(s.start,q); det=cross(d,v)
    if det:
        kn=cross(c,v);jn=cross(c,d)
        if kn%det or jn%det: return None
        k,j=kn//det,jn//det
        return (k,k,0,1) if k>=0 and 0<=j<s.length else None
    if cross(c,d): return None
    axis=0 if d[0] else 1
    A,B,C=d[axis],v[axis],c[axis]
    if A<0: A,B,C=-A,-B,-C
    g=gcd(A,abs(B))
    if C%g: return None
    modulus=abs(B)//g
    residue=0 if modulus==1 else ((C//g)*pow(A//g,-1,modulus))%modulus
    lo=max(0,ceil_div(min(C,C+B*(s.length-1)),A))
    hi=max(C,C+B*(s.length-1))//A
    lo+= (residue-lo)%modulus
    return None if lo>hi else (lo,hi,residue,modulus)


def verify_period(x: SymbolicState,word: str,max_residue_checks: int|None=None) -> dict:
    """Exact first disagreement with word^omega, including all XOR collisions.

    Finite arithmetic-progressions on each phase ray plus self-read thresholds.
    Between endpoints, parity is periodic with the lcm of active moduli. A full
    residue period or the shorter finite interval is exhaustive, not sampling.
    Runtime can depend on that lcm: no polynomial-time claim for this encoding.
    """
    if max_residue_checks is not None and (type(max_residue_checks) is not int or max_residue_checks<0):
        raise ValueError('nonnegative residue-check cap required')
    ps,hs,h,d=geometry(x,word);P=len(word)
    if h!=x.heading or d==(0,0):
        raise ValueError('period must restore heading and translate nontrivially')
    first=None;checked=0;intervals=0
    for i,p in enumerate(ps):
        thresholds=[]
        for j,q in enumerate(ps):
            r=multiple(sub(q,p),d)
            if r is not None and r>=0 and (r>0 or j<i): thresholds.append(r)
        aps=[a for s in x.terms if (a:=ray_segment_epochs(p,d,s)) is not None]
        breaks=sorted({0,*thresholds,*[a[0] for a in aps],*[a[1]+1 for a in aps]})
        for bi,lo in enumerate(breaks):
            if first is not None and lo*P+i>=first: break
            hi=breaks[bi+1]-1 if bi+1<len(breaks) else None
            active=[a for a in aps if a[0]<=lo<=a[1]]
            modulus=lcm(*(a[3] for a in active)) if active else 1
            count=modulus if hi is None else min(modulus,hi-lo+1)
            self_parity=sum(r<=lo for r in thresholds)%2;intervals+=1
            for k in range(lo,lo+count):
                if first is not None and k*P+i>=first: break
                if max_residue_checks is not None and checked>=max_residue_checks:
                    return dict(kind='inconclusive',reason='caller residue cap',checks=checked)
                checked+=1
                black=(self_parity+sum(k%a[3]==a[2] for a in active))%2
                if black!=int(word[i]=='L'):
                    first=k*P+i if first is None else min(first,k*P+i);break
    return dict(kind='verified',valid=first is None,first_bad_offset=first,
                period=P,drift=list(d),checks=checked,intervals=intervals)


def apply_periodic_prefix(x: SymbolicState,word: str,n: int) -> SymbolicState:
    """Apply its exact prescribed finite writes; caller must establish read validity.

    No claim that an arbitrary supplied word is physically valid is implicit.
    This helper remains exact as the algebra of a specified geometric write path.
    """
    if type(n) is not int or n<0: raise ValueError('nonnegative prefix length required')
    ps,hs,h,d=geometry(x,word);P=len(word)
    if h!=x.heading or d==(0,0): raise ValueError('translating word required')
    terms=list(x.terms)
    for i,q in enumerate(ps):
        count=0 if n<=i else (n-1-i)//P+1
        if count: terms.append(Segment(q,d,count))
    k,i=divmod(n,P)
    return SymbolicState(tuple(terms),add(ps[i],mul(k,d)),hs[i])


def next_stale_macro(x: SymbolicState,D: int, max_suffix_states: int|None=None,
                     max_residue_checks: int|None=None) -> dict:
    """Return the exact full state JUST AFTER the next stale-D read, or a tail.

    All represented sets remain finite. Source supports and generated writes
    are retained with XOR; no unwritten future-activity deletion is performed.
    The unbounded-call algorithm is total per macro, not over infinitely many macros.
    """
    if type(D) is not int or D<1: raise ValueError('positive integer D required')
    if max_suffix_states is not None and (type(max_suffix_states) is not int or max_suffix_states<0):
        raise ValueError('nonnegative suffix cap required')
    start=x;w=preceding_turns(x,D);seen={};turns=[];Q=1<<D
    def event(y: SymbolicState,t: int,explicit: int,**extra):
        if not y.black(y.pos): raise AssertionError('event must read black')
        after,ch=step(y)
        if ch!='L': raise AssertionError('stale read must turn left')
        if len(after.terms)>len(start.terms)+9*Q+1:
            raise AssertionError('term bound failed')
        return dict(kind='stale_read',event_time=t,duration=t+1,before=y,after=after,
                    explicit_updates=explicit,source_terms=len(start.terms),
                    target_terms=len(after.terms),**extra)
    while w not in seen:
        if max_suffix_states is not None and len(seen)>=max_suffix_states:
            return dict(kind='inconclusive',reason='caller suffix cap')
        actual='L' if x.black(x.pos) else 'R';want=suffix_predict(w)
        if actual!=want:
            if (want,actual)!=('R','L'): raise AssertionError('bad prediction identity')
            return event(x,len(turns),len(turns))
        seen[w]=len(turns);turns.append(actual);x,_=step(x);w=w[1:]+actual
    j=len(turns);cycle=''.join(turns[seen[w]:]);ps,hs,h,d=geometry(x,cycle)
    rot=(h-x.heading)%4
    if rot or d==(0,0):
        repeats=2 if rot==2 else (4 if rot else 1);block=cycle*repeats
        for k in range(2*len(block)):
            actual='L' if x.black(x.pos) else 'R'
            if actual!=block[k%len(block)]: return event(x,j+k,j+k,cycle=cycle)
            x,_=step(x)
        raise AssertionError('bounded infinite literal orbit would result')
    check=verify_period(x,cycle,max_residue_checks)
    if check['kind']=='inconclusive': return check
    if check['valid']:
        return dict(kind='permanent_no_stale',entry=j,start=x,cycle=cycle,
                    certificate=check,explicit_updates=j)
    n=check['first_bad_offset'];y=apply_periodic_prefix(x,cycle,n)
    if cycle[n%len(cycle)]!='R': raise AssertionError('first disagreement is predicted R')
    # The whole earlier history follows the autonomous suffix rule. At its first
    # mismatch the intrinsic D-local predicate is therefore the stale-black read.
    return event(y,j+n,j,cycle=cycle,certificate=check,periodic_steps=n)


def state_data(x: SymbolicState) -> dict:
    """Lossless JSON-compatible full colouring representation, not a sketch."""
    return {'schema':'langtons-ant-xor-segments-v1', 'pos':list(x.pos),
            'heading':x.heading,
            'terms':[{'start':list(s.start),'stride':list(s.stride),'length':s.length}
                     for s in x.terms]}


def state_from_data(data: dict) -> SymbolicState:
    if data.get('schema')!='langtons-ant-xor-segments-v1':
        raise ValueError('unknown symbolic-state schema')
    return SymbolicState(tuple(Segment(tuple(s['start']),tuple(s['stride']),s['length'])
                               for s in data['terms']),tuple(data['pos']),data['heading'])


def event_prefix(x: SymbolicState, D: int, n: int, **limits) -> dict:
    """Compute at most n complete events, stopping earlier on a certified tail.

    'event_budget_reached' reports only that the requested finite prefix is done;
    it is not a verdict on infinite continuation or eventual P104 membership.
    Optional suffix/residue caps propagate 'inconclusive', never a false NO.
    """
    if type(n) is not int or n<0: raise ValueError('nonnegative event count required')
    if type(D) is not int or D<1: raise ValueError('positive integer D required')
    elapsed=0;events=[]
    for _ in range(n):
        out=next_stale_macro(x,D,**limits)
        if out['kind']!='stale_read':
            return dict(kind=out['kind'],events=events,elapsed=elapsed,state=x,terminal=out)
        events.append({'time':elapsed+out['event_time'],'pos':list(out['before'].pos),
                       'duration':out['duration'],'explicit_updates':out['explicit_updates'],
                       'target_terms':out['target_terms']})
        elapsed+=out['duration'];x=out['after']
    return dict(kind='event_budget_reached',events=events,elapsed=elapsed,state=x)
