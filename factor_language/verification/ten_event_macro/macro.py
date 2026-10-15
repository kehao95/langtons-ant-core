"""Exact first-J10 macros; all finite black history is retained as XOR segments.

The folded graph has five simple cyclic components. The proof of the lift uses
only the pinned ten-factor coverage and the all-parameter three-fold conflict.
An unbounded sequence of these terminating calls is NOT a HIGHWAY decider.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from functools import lru_cache
import hashlib
from pathlib import Path
import sys
from typing import Optional

TEN = Path(__file__).resolve().parent.parent / 'ten'
sys.path.insert(0, str(TEN))
import kernel as base
r = base.r
Point = tuple[int, int]
Node = tuple[str, int]
STRIDES = frozenset({(0,0), (2,2), (2,-2), (-2,2), (-2,-2),
                    (0,2), (0,-2), (2,0), (-2,0),
                    (0,4), (0,-4), (4,0), (-4,0)})
L10 = r.factors(r.W, 10)


def add(a: Point, b: Point) -> Point: return a[0]+b[0], a[1]+b[1]
def sub(a: Point, b: Point) -> Point: return a[0]-b[0], a[1]-b[1]
def scale(k: int, a: Point) -> Point: return k*a[0], k*a[1]
def det(a: Point, b: Point) -> int: return a[0]*b[1]-a[1]*b[0]
def ceildiv(a: int, b: int) -> int: return -((-a)//b)

def sha(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()

@dataclass(frozen=True)
class Segment:
    start: Point
    stride: Point = (0,0)
    length: int = 1
    def __post_init__(self):
        if self.stride not in STRIDES or self.length < 1 or (self.stride == (0,0) and self.length != 1):
            raise ValueError('unsupported or empty finite segment')
    def contains(self, p: Point) -> bool:
        if self.stride == (0,0): return p == self.start
        n = r.multiple(sub(p, self.start), self.stride)
        return n is not None and 0 <= n < self.length

@dataclass(frozen=True)
class State:
    terms: tuple[Segment, ...]
    head: Point = (0,0)
    heading: int = 0
    def __post_init__(self):
        if self.heading not in range(4): raise ValueError('heading must be 0..3')
    def black(self, p: Point) -> bool:
        return bool(sum(s.contains(p) for s in self.terms) % 2)

def from_cells(B, head=(0,0), heading=0) -> State:
    return State(tuple(Segment(p) for p in sorted(set(B))), head, heading)

def step(X: State):
    c = 'L' if X.black(X.head) else 'R'
    h = (X.heading + (1 if c == 'R' else -1)) % 4
    return State(X.terms+(Segment(X.head),), add(X.head, r.DIR[h]), h), c

def inverse(X: State):
    p = sub(X.head, r.DIR[X.heading]); c = 'R' if X.black(p) else 'L'
    h = (X.heading - (1 if c == 'R' else -1)) % 4
    return State(X.terms+(Segment(p),), p, h), c

def past(X: State, n: int = 149) -> str:
    letters=[]
    for _ in range(n): X,c=inverse(X); letters.append(c)
    return ''.join(reversed(letters))

def defect(X: State) -> bool:
    return past(X,9)+('L' if X.black(X.head) else 'R') not in L10


def ray_intersection(q: Point, d: Point, seg: Segment):
    """All k>=0 with q+k*d in seg: (first,last,stride), or None.

    Unlike the older J13 macro, axis strides two AND four are supported.
    In this closed stride family the epoch stride is one or two.
    """
    if d == (0,0): raise ValueError('ray direction must be nonzero')
    v=seg.stride; delta=sub(seg.start,q)
    if v == (0,0):
        k=r.multiple(delta,d)
        return (k,k,1) if k is not None and k>=0 else None
    den=det(d,v)
    if den:
        kn,jn=det(delta,v),det(delta,d)
        if kn % den or jn % den: return None
        k,j=kn//den,jn//den
        return (k,k,1) if k>=0 and 0<=j<seg.length else None
    if det(delta,d): return None
    import math
    axis=0 if d[0] else 1
    a,b,c=d[axis],v[axis],delta[axis]; g=math.gcd(abs(a),abs(b))
    if c%g: return None
    modulus=abs(b)//g
    if modulus not in (1,2): raise ValueError('ray outside closed stride family')
    residue=0 if modulus==1 else ((c//g)*pow(a//g,-1,modulus))%modulus
    lo,hi=sorted((c,c+b*(seg.length-1)))
    if a<0: a,lo,hi=-a,-hi,-lo
    low=max(0,ceildiv(lo,a)); high=hi//a
    first=low+(residue-low)%modulus
    last=high-(high-residue)%modulus
    return (first,last,modulus) if first<=last else None


def first_mismatch(X: State, word: str) -> Optional[int]:
    """First mismatch with word^omega, checking both residue classes of epochs."""
    qs,d,_,dh=r.geometry(word)
    if dh or d==(0,0): raise ValueError('plan must restore heading and translate')
    d=r.rotate(d,X.heading); qs=[add(X.head,r.rotate(q,X.heading)) for q in qs]
    P=len(word); first=None
    for i,q in enumerate(qs):
        changes=[{0:int(word[i]=='L')},{0:int(word[i]=='L')}]
        def toggle(parity, index):
            changes[parity][index]=changes[parity].get(index,0)^1
        for j,z in enumerate(qs):
            s=r.multiple(sub(z,q),d)
            if s is not None and (s>0 or s==0 and j<i):
                for parity in (0,1): toggle(parity,max(0,ceildiv(s-parity,2)))
        for seg in X.terms:
            hit=ray_intersection(q,d,seg)
            if hit is None: continue
            lo,hi,stride=hit
            for parity in (0,1):
                if stride==2 and lo%2!=parity: continue
                a=max(0,ceildiv(lo-parity,2)); b=(hi-parity)//2
                if a<=b: toggle(parity,a);toggle(parity,b+1)
        for parity in (0,1):
            value=0
            for j in sorted(changes[parity]):
                value^=changes[parity][j]
                if value:
                    t=P*(2*j+parity)+i
                    if first is None or t<first: first=t
                    break
    return first


def skip(X: State, word: str, time: int) -> State:
    """Append every skipped write; caller proves the planned prefix is valid."""
    if time<0: raise ValueError('negative skip')
    qs,d,hs,dh=r.geometry(word)
    if dh: raise ValueError('heading not restored')
    n,j=divmod(time,len(word)); d=r.rotate(d,X.heading)
    qs=[add(X.head,r.rotate(q,X.heading)) for q in qs];terms=list(X.terms)
    if n: terms.extend(Segment(q,d,n) for q in qs)
    terms.extend(Segment(add(qs[i],scale(n,d))) for i in range(j))
    return State(tuple(terms),add(qs[j],scale(n,d)),(X.heading+hs[j])%4)


@lru_cache(maxsize=1)
def graph_data():
    """Rebuild and check the pinned kernel, then the new finite unfolding."""
    words,_=base.enumerate_words(10,150)
    raw=('\n'.join(words)+'\n').encode()
    if sha(raw)!='6b76e51621e15d2304f1c0baa28790cc267cabafca3fc03250dea8721b2b4794':
        raise ValueError('base enumeration differs from its immutable witness')
    adj,rev=base.graph(words); H=next(c for c in base.sccs(adj,rev) if len(c)==366)
    wit=base.load_witness(TEN/'certificates'); B=wit['B']; mapping={}
    for v in sorted(H):
        states=set(range(102))
        for c in v:
            states={((q+1)%102) for q in states if B[q]==c}|({75} if 0 in states and c=='L' else set())
        if len(states)!=1: raise ValueError('ambiguous quotient phase')
        mapping[v]=states.pop()
    raw=''.join(v+'\t'+str(mapping[v])+'\n' for v in sorted(mapping)).encode()
    if sha(raw)!='f6d5502737c0ce931c1f9ca62a62ad8307157b4133c8f087f7ac0268b0d05682':
        raise ValueError('quotient differs from immutable witness')
    model={(i,B[i]):(i+1)%102 for i in range(102)}; model[0,'L']=75
    for v in H:
        for u in adj[v]&H:
            if model.get((mapping[v],u[-1]))!=mapping[u]: raise ValueError('invalid quotient edge')
    lift={}
    for v in sorted(adj):
        for count in (range(4) if v in H else [0]):
            if count==3 and mapping[v]==0: continue
            src=(v,count); lift[src]=set()
            for u in adj[v]:
                n=(count+int(mapping[v]==0 and u[-1]=='R')) if v in H and u in H else 0
                if u in H and (n>3 or n==3 and mapping[u]==0): continue
                lift[src].add((u,n))
    back={v:set() for v in lift}
    for v,outs in lift.items():
        for u in outs: back[u].add(v)
    comps=base.sccs(lift,back); ids={v:i for i,c in enumerate(comps) for v in c}
    cyclic={i for i,c in enumerate(comps) if len(c)>1 or any(v in lift[v] for v in c)}
    if sorted(len(comps[i]) for i in cyclic)!=[24,28,28,28,104]:
        raise ValueError('unexpected lifted cyclic components')
    plans={}; rings={}; phase={}
    for i in cyclic:
        comp=comps[i]
        if any(len(lift[v]&comp)!=1 for v in comp): raise ValueError('nonsimple lifted cycle')
        start=min(comp); order=[start];v=start
        while True:
            v=next(iter(lift[v]&comp))
            if v==start:break
            order.append(v)
        word=''.join(order[(j+1)%len(order)][0][-1] for j in range(len(order)))
        qs,d,hs,dh=r.geometry(word)
        if dh or d==(0,0) or d not in STRIDES:raise ValueError('unsupported cycle geometry')
        if len(word)==104 and word not in r.factors(r.W,104):raise ValueError('nonstandard 104-cycle')
        if len(word)==28 and word not in r.factors(wit['A'],28):raise ValueError('wrong 28-cycle')
        if len(word)==24 and word not in r.factors(wit['T'],24):raise ValueError('wrong 24-cycle')
        rings[i]=order
        for j,v in enumerate(order): plans[v]=word[j:]+word[:j];phase[v]=j
    dag={i:set() for i in range(len(comps))}
    for v,outs in lift.items():
        for u in outs:
            if ids[v]!=ids[u]:dag[ids[v]].add(ids[u])
    top=base.topological(dag,set(dag));budget={}
    for i in reversed(top):
        cweight=int(i in cyclic); oweight=int(i not in cyclic); pweight=len(comps[i]) if i in cyclic else 0
        budget[i]=(cweight+max([budget[j][0]for j in dag[i]]+[0]),
                   oweight+max([budget[j][1]for j in dag[i]]+[0]),
                   pweight+max([budget[j][2]for j in dag[i]]+[0]))
    maximum=tuple(max(b[j] for b in budget.values()) for j in range(3))
    if (len(lift),sum(map(len,lift.values())),maximum)!=(7595,7763,(5,956,212)):
        raise ValueError('unexpected finite budget')
    # The computed values are checked again by local inequalities, separately
    # from topological construction. For internal cycle edges the weights are 0.
    for v,outs in lift.items():
        i=ids[v]
        for u in outs:
            j=ids[u]
            if i==j:
                if i not in cyclic:raise ValueError('unclassified recurrent edge')
            else:
                weights=(int(i in cyclic),int(i not in cyclic),len(comps[i]) if i in cyclic else 0)
                if any(budget[i][k]<weights[k]+budget[j][k] for k in range(3)):
                    raise ValueError('bad local rank inequality')
    return dict(adj=adj,lift=lift,ids=ids,comps=comps,cyclic=cyclic,plans=plans,
                rings=rings,phase=phase,budget=budget,maximum=maximum,mapping=mapping,
                words=words)

@dataclass(frozen=True)
class Result:
    time: Optional[int]
    post_state: Optional[State]
    tail_word: Optional[str]
    tail_offset: Optional[int]
    ordinary_updates: int
    periodic_plans: int
    added_terms: int


def next_event(X: State) -> Result:
    """Exact first future J10 and full post-state, or certified permanent absence.

    No call uses a user-supplied event count, radius, or time horizon.
    Initial recent history is recovered from the literal inverse, not guessed.
    """
    data=graph_data();hist=past(X); elapsed=ordinary=plans=0;original_terms=len(X.terms)
    node=(hist,0) if hist in data['adj'] else None
    while True:
        c='L' if X.black(X.head) else 'R'
        if hist[-9:]+c not in L10:
            post,_=step(X);ordinary+=1
            if ordinary>1111 or plans>5 or len(post.terms)-original_terms>1530:
                raise AssertionError('proved call budget exceeded')
            return Result(elapsed,post,None,None,ordinary,plans,len(post.terms)-original_terms)
        word=data['plans'].get(node)
        if word is None:
            oldnode=node;X,c=step(X);hist=hist[1:]+c;elapsed+=1;ordinary+=1
            if oldnode is None:node=(hist,0) if hist in data['adj'] else None
            else:
                choices=[u for u in data['lift'][oldnode] if u[0]==hist]
                if len(choices)!=1:raise AssertionError('real legal transition missing from lift')
                node=choices[0]
            if ordinary>1110:raise AssertionError('ordinary-update budget exceeded')
            continue
        plans+=1
        if plans>5:raise AssertionError('cyclic-component budget exceeded')
        t=first_mismatch(X,word)
        if t is None:
            if len(word)!=104:raise AssertionError('finite field sustained a black-ray mode')
            return Result(None,None,word,elapsed,ordinary,plans,len(X.terms)-original_terms)
        X=skip(X,word,t);elapsed+=t
        cid=data['ids'][node];ring=data['rings'][cid]
        node=ring[(data['phase'][node]+t)%len(ring)];hist=node[0]
        actual='L' if X.black(X.head) else 'R'
        if actual==word[t%len(word)]:raise AssertionError('false mismatch')
        if hist[-9:]+actual not in L10:
            post,_=step(X);ordinary+=1
            if ordinary>1111 or len(post.terms)-original_terms>1530:
                raise AssertionError('proved call budget exceeded')
            return Result(elapsed,post,None,None,ordinary,plans,len(post.terms)-original_terms)
        old=node;X,c=step(X);hist=hist[1:]+c;elapsed+=1;ordinary+=1
        choices=[u for u in data['lift'][old] if u[0]==hist]
        if len(choices)!=1:raise AssertionError('legal cycle exit missing from lift')
        node=choices[0]
        if data['ids'][node]==cid:raise AssertionError('mismatch did not leave a simple component')
        if ordinary>1110:raise AssertionError('ordinary-update budget exceeded')


def expand(X: State, cap: int=1000000):
    if sum(s.length for s in X.terms)>cap:raise ValueError('test-only expansion limit')
    B=set()
    for s in X.terms:
        for j in range(s.length):B.symmetric_difference_update({add(s.start,scale(j,s.stride))})
    return B,X.head,X.heading


def same_complete_state(X: State, Y: State) -> bool:
    """Exact extensional equality, including canceled and differently split terms."""
    if (X.head,X.heading)!=(Y.head,Y.heading):return False
    terms=X.terms+Y.terms
    for probe in terms:
        if probe.stride==(0,0):
            if sum(s.contains(probe.start) for s in terms)%2:return False
            continue
        changes=[{},{}]
        for seg in terms:
            hit=ray_intersection(probe.start,probe.stride,seg)
            if hit is None:continue
            lo,hi,stride=hit;hi=min(hi,probe.length-1)
            if lo>hi:continue
            for parity in (0,1):
                if stride==2 and lo%2!=parity:continue
                a=max(0,ceildiv(lo-parity,2));b=(hi-parity)//2
                if a<=b:
                    for j in (a,b+1):changes[parity][j]=changes[parity].get(j,0)^1
        for parity in (0,1):
            value=0
            for j in sorted(changes[parity]):
                value^=changes[parity][j]
                if value:return False
    return True
