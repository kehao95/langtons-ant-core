"""Exact birth-filtered exterior stale reads of the classical finite-support ant.

All coordinates and lengths are integers.  The complete black field is an XOR
of finite segments; nothing is deleted as "inactive".  Resource limits are
optional and yield INCONCLUSIVE, never a negative mathematical answer.

The new birth filter uses the pre-existing next-S_D and fixed-region burst
lemmas. The isolated implementation also records ALL skipped reads with times.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from math import gcd, lcm
from typing import Iterable

Point = tuple[int, int]
DIR = ((0, 1), (1, 0), (0, -1), (-1, 0))

def add(a, b): return a[0]+b[0], a[1]+b[1]
def sub(a, b): return a[0]-b[0], a[1]-b[1]
def mul(a, n): return a[0]*n, a[1]*n

def multiple(a: Point, b: Point):
    if b == (0, 0): raise ValueError('nonzero vector required')
    j = 0 if b[0] else 1
    if a[j] % b[j]: return None
    k = a[j] // b[j]
    return k if mul(b, k) == a else None

def ceildiv(a: int, b: int):
    if b <= 0: raise ValueError('positive denominator required')
    return -((-a)//b)

@dataclass(frozen=True)
class Segment:
    start: Point
    stride: Point = (0, 0)
    length: int = 1
    def __post_init__(self):
        if type(self.length) is not int or self.length < 1:
            raise ValueError('positive finite length required')
        if any(not isinstance(v, tuple) or len(v)!=2 or
               any(type(a) is not int for a in v) for v in (self.start,self.stride)):
            raise ValueError('integer coordinate pairs required')
        if self.stride == (0, 0) and self.length != 1:
            raise ValueError('a zero-stride segment is one singleton')
    def index(self, p):
        if self.stride == (0, 0): return 0 if p == self.start else None
        k = multiple(sub(p, self.start), self.stride)
        return k if k is not None and 0 <= k < self.length else None

class Field:
    def __init__(self, terms: Iterable[Segment] = ()):
        self.terms = list(terms)
    @classmethod
    def explicit(cls, black):
        return cls(Segment(p) for p in sorted(set(black)))
    def copy(self): return Field(self.terms)
    def bit(self, p): return sum(s.index(p) is not None for s in self.terms) & 1
    def toggle(self, p): self.terms.append(Segment(p))
    def materialize(self, limit=1000000):
        if sum(s.length for s in self.terms) > limit:
            raise ValueError('materialization resource limit, not a mathematical rejection')
        out = set()
        for s in self.terms:
            for j in range(s.length):
                p = add(s.start,mul(s.stride,j))
                if p in out: out.remove(p)
                else: out.add(p)
        return out

@dataclass(frozen=True)
class Write:
    segment: Segment
    time0: int
    time_stride: int
    letter: str
    def read_at(self, p):
        j = self.segment.index(p)
        return None if j is None else (self.time0+j*self.time_stride, self.letter)

@dataclass
class State:
    field: Field
    pos: Point = (0, 0)
    heading: int = 0
    def __post_init__(self):
        if self.heading not in range(4) or any(type(x) is not int for x in self.pos):
            raise ValueError('invalid pose')
    @classmethod
    def explicit(cls, black, pos=(0,0), heading=0):
        return cls(Field.explicit(black), pos, heading)
    def copy(self): return State(self.field.copy(), self.pos, self.heading)

class Exhausted(Exception): pass
@dataclass(frozen=True)
class Limits:
    suffix_states: int | None = None
    event_calls: int | None = None
    residue_modulus: int | None = None
    def __post_init__(self):
        for v in (self.suffix_states,self.event_calls,self.residue_modulus):
            if v is not None and (type(v) is not int or v < 0):
                raise ValueError('limits are nonnegative integers or None')


def geometry(word, p=(0,0), h=0):
    pts=[]; hs=[]; start=p
    for c in word:
        if c not in 'RL': raise ValueError('turn alphabet')
        pts.append(p); hs.append(h)
        h=(h+(1 if c=='R' else -1))%4
        p=add(p,DIR[h])
    return pts,hs,sub(p,start),h

@lru_cache(maxsize=100000)
def predict(history: str):
    pts,_,end,_=geometry(history)
    for p,c in zip(reversed(pts),reversed(history)):
        if p==end: return 'L' if c=='R' else 'R'
    return 'R'


def inverse(x: State):
    q=sub(x.pos,DIR[x.heading]); old_after=x.field.bit(q)
    c='R' if old_after else 'L'
    x.field.toggle(q); x.pos=q
    x.heading=(x.heading+(-1 if old_after else 1))%4
    return c


def history_of(x: State, D: int):
    if type(D) is not int or D < 1: raise ValueError('positive integer D')
    tmp=x.copy(); ans=[inverse(tmp) for _ in range(D)]
    return ''.join(reversed(ans))


def literal(x: State, time: int, writes: list[Write]):
    c='L' if x.field.bit(x.pos) else 'R'
    writes.append(Write(Segment(x.pos),time,1,c))
    x.field.toggle(x.pos)
    x.heading=(x.heading+(1 if c=='R' else -1))%4
    x.pos=add(x.pos,DIR[x.heading])
    return c


def ray_intersection(s: Segment, q: Point, d: Point):
    """Return (first epoch, positive step, count), or None, for q+k*d in s."""
    if d==(0,0): raise ValueError('nonzero ray direction')
    if s.stride==(0,0):
        k=multiple(sub(s.start,q),d)
        return (k,1,1) if k is not None and k>=0 else None
    v=s.stride; a=sub(s.start,q)
    det=d[0]*v[1]-d[1]*v[0]
    if det:
        nk=a[0]*v[1]-a[1]*v[0]
        nj=a[0]*d[1]-a[1]*d[0]
        if nk%det or nj%det: return None
        k=nk//det; j=nj//det
        return (k,1,1) if k>=0 and 0<=j<s.length else None
    g=gcd(abs(d[0]),abs(d[1])); unit=(d[0]//g,d[1]//g)
    c=multiple(a,unit); h=multiple(v,unit)
    if c is None or h is None: return None
    g0=gcd(g,abs(h))
    if c%g0: return None
    modulus=g//g0
    j0=0 if modulus==1 else ((-c//g0)*pow(h//g0,-1,modulus))%modulus
    if j0>=s.length: return None
    count=(s.length-1-j0)//modulus+1
    k0=(c+h*j0)//g; step=h//g0
    if step<0:
        k0+=step*(count-1); step=-step
    if k0<0:
        skipped=ceildiv(-k0,step); k0+=skipped*step; count-=skipped
    return (k0,step,count) if count>0 else None


def first_bad_epoch(field: Field, q, d, thresholds, expected: int, limits: Limits):
    aps=[ap for s in field.terms if (ap:=ray_intersection(s,q,d)) is not None]
    modulus=lcm(*(ap[1] for ap in aps)) if aps else 1
    if limits.residue_modulus is not None and modulus>limits.residue_modulus:
        raise Exhausted('epoch residue modulus')
    best=None
    for r in range(modulus):
        changes={0:0}
        def flip(z): changes[z]=changes.get(z,0)^1
        for a,m,count in aps:
            last=a+m*(count-1)
            if (r-a)%m: continue
            lo=max(0,ceildiv(a-r,modulus)); hi=(last-r)//modulus
            if lo<=hi: flip(lo); flip(hi+1)
        for s in thresholds: flip(max(0,ceildiv(s-r,modulus)))
        bit=0
        for z in sorted(changes):
            bit ^= changes[z]
            if bit != expected:
                k=r+modulus*z
                best=k if best is None else min(best,k)
                break
    return best


def period_mismatch(x: State, word: str, limits: Limits = Limits()):
    points,_,d,h=geometry(word,x.pos,x.heading)
    if h!=x.heading or d==(0,0): raise ValueError('nonzero heading-reset cycle required')
    P=len(word); first=None
    for i,q in enumerate(points):
        thresholds=[]
        for j,z in enumerate(points):
            a=multiple(sub(z,q),d)
            if a is not None and (a>0 or (a==0 and j<i)): thresholds.append(a)
        k=first_bad_epoch(x.field,q,d,thresholds,word[i]=='L',limits)
        if k is not None:
            t=k*P+i; first=t if first is None else min(first,t)
    return first


def append_cycles(x: State, word: str, repetitions: int, time: int, writes: list[Write]):
    if repetitions<0: raise ValueError('negative repetition')
    if not repetitions: return
    points,_,d,h=geometry(word,x.pos,x.heading)
    if h!=x.heading or d==(0,0): raise ValueError('nonzero heading-reset cycle required')
    for i,(p,c) in enumerate(zip(points,word)):
        s=Segment(p,d,repetitions)
        x.field.terms.append(s); writes.append(Write(s,time+i,len(word),c))
    x.pos=add(x.pos,mul(d,repetitions))


def next_stale(start: State, D: int, *, time0=0, limits: Limits=Limits()):
    """EVENT returns complete post-state and every skipped read, not only a time."""
    history=history_of(start,D); x=start.copy(); writes=[]; seen={}; letters=[]
    t=time0
    while history not in seen:
        if limits.suffix_states is not None and len(seen)>=limits.suffix_states:
            raise Exhausted('suffix states')
        actual='L' if x.field.bit(x.pos) else 'R'
        if actual!=predict(history):
            if actual!='L' or predict(history)!='R': raise AssertionError('suffix mismatch')
            point=x.pos; literal(x,t,writes)
            return dict(kind='EVENT',time=t,point=point,post=x,writes=writes)
        seen[history]=len(letters)
        c=literal(x,t,writes); letters.append(c); t+=1
        history=history[1:]+c
    cycle=''.join(letters[seen[history]:]); pts,hs,d,h=geometry(cycle,x.pos,x.heading)
    rotation=(h-x.heading)%4
    if rotation or d==(0,0):
        full=cycle*(1 if rotation==0 else (2 if rotation==2 else 4))
        for i in range(2*len(full)):
            actual='L' if x.field.bit(x.pos) else 'R'
            if actual!=full[i%len(full)]:
                if actual!='L' or full[i%len(full)]!='R': raise AssertionError('closed mismatch')
                point=x.pos; literal(x,t,writes)
                return dict(kind='EVENT',time=t,point=point,post=x,writes=writes)
            literal(x,t,writes); t+=1
        raise AssertionError('would be a forbidden complete-state recurrence')
    first=period_mismatch(x,cycle,limits)
    if first is None:
        return dict(kind='FREE',entry=t,state=x,word=cycle,drift=d,writes=writes)
    n,i=divmod(first,len(cycle))
    append_cycles(x,cycle,n,t,writes); t+=n*len(cycle)
    for c in cycle[:i]:
        if literal(x,t,writes)!=c: raise AssertionError('premature mismatch')
        t+=1
    if cycle[i]!='R' or not x.field.bit(x.pos): raise AssertionError('not stale black')
    point=x.pos; literal(x,t,writes)
    return dict(kind='EVENT',time=t,point=point,post=x,writes=writes)


def last_read(writes: Iterable[Write], point, before: int):
    answer=None
    for w in writes:
        hit=w.read_at(point)
        if hit is not None and hit[0]<before and (answer is None or hit[0]>answer[0]):
            answer=hit
    return answer


def fresh_feedback(start: State, D: int, region: set[Point] | frozenset[Point],
                   limits: Limits=Limits()):
    """First exterior S_D whose current black lifetime was born at time >=0.

    The negative answer is NO_FRESH_EXTERNAL, and certifies ETC, not NO_HIGHWAY.
    Initial black cells re-created later DO qualify. Region is fixed during a
    call; separate calls may reset it arbitrarily.
    """
    history_of(start,D)  # validate D and pose before making a result
    if any(not isinstance(p,tuple) or len(p)!=2 or any(type(z) is not int for z in p)
           for p in region): raise ValueError('region must contain integer pairs')
    x=start.copy(); t=0; reads=[]; calls=0; rejected=[]
    try:
        while True:
            if limits.event_calls is not None and calls>=limits.event_calls:
                raise Exhausted('event calls')
            result=next_stale(x,D,time0=t,limits=limits); calls+=1
            reads.extend(result['writes'])
            if result['kind']=='FREE':
                return dict(kind='NO_FRESH_EXTERNAL',event_calls=calls,
                            ignored_initial=rejected,certificate=result,reads=reads)
            e=result['point']; death=result['time']
            if e not in region:
                birth=last_read(reads,e,death)
                if birth is not None:
                    if birth[1]!='R' or death-birth[0]<=D:
                        raise AssertionError('not the claimed black lifetime')
                    return dict(kind='FRESH_EXTERNAL',point=e,birth=birth[0],
                                death=death,age=death-birth[0],post=result['post'],
                                event_calls=calls,ignored_initial=rejected,reads=reads)
                if not start.field.bit(e): raise AssertionError('uncreated black cell')
                if e in [p for p,at in rejected]: raise AssertionError('initial cohort consumed twice')
                rejected.append((e,death))
            x=result['post']; t=death+1
    except Exhausted as err:
        return dict(kind='INCONCLUSIVE',reason=str(err),event_calls=calls,
                    ignored_initial=rejected)


def diameter(points):
    ps=list(points)
    if not ps: return 0
    return max(max(p[j] for p in ps)-min(p[j] for p in ps) for j in (0,1))


def deadline_parts(black: Iterable[Point], pos: Point, D: int, region: Iterable[Point]):
    """Return the exact symbolic bound A + C*3**exponent; do not expand it."""
    if type(D) is not int or D<1: raise ValueError('positive D')
    B=set(black); K=set(region); Q=1<<D; n=len(B)+1
    W=diameter(B|K|{pos})
    ell=diameter(K)+2*(3*Q+2)+1 if K else 0
    A=n*(2*Q*W+20*Q*Q+(1 if K else 0))+18*Q*Q*n*(n-1)
    return {'A':A,'C':8*n*ell if K else 0,'exponent':ell,
            'initial_black_count':len(B),'exterior_calls':n,'width':W,'Q':Q}


def renewal_deadline(black: Iterable[Point], pos: Point, D: int,
                     region: Iterable[Point], *, max_exponent=100000):
    """Evaluate the conditional post-event bound only if the exponent is modest.

    For a huge bound, use deadline_parts(). This helper's resource refusal is
    NOT an answer to the ant question. The decision algorithm never evaluates
    its enormous worst-case bound.
    """
    p=deadline_parts(black,pos,D,region)
    if p['C'] and p['exponent']>max_exponent:
        raise Exhausted('deadline exponent; use the symbolic deadline_parts')
    return p['A']+p['C']*3**p['exponent']


def summary(result):
    keys=('kind','point','birth','death','age','event_calls','ignored_initial','reason')
    out={k:result[k] for k in keys if k in result}
    if result['kind']=='FRESH_EXTERNAL':
        x=result['post']; out['post_pose']=[list(x.pos),x.heading]
        out['post_terms']=len(x.field.terms)
        out['total_written_reads']=sum(w.segment.length for w in result['reads'])
    elif result['kind']=='NO_FRESH_EXTERNAL':
        out['periodic_entry']=result['certificate']['entry']
        out['period']=len(result['certificate']['word'])
        out['drift']=list(result['certificate']['drift'])
    return out


def growing_scale_floor(initial_mass: int, initial_width: int, horizon: int):
    """Exact lower bound conditional on NON-ETC; never diagnoses that premise.

    The region is a square about the source pose and is frozen for the whole
    application at this horizon. No dynamic singleton {p_t} is used.
    """
    from math import isqrt
    if min(initial_mass,initial_width)<0 or horizon<3**64:
        raise ValueError('nonnegative source data and horizon >= 3**64 required')
    L=0;power=1
    while power*3<=horizon:power*=3;L+=1
    D=L.bit_length()-1-5;Q=1<<D;R=L//16
    ell=2*R+6*Q+5;burst=8*ell*3**ell+1
    W=initial_width+2*R
    a=18*Q*Q;c=2*Q*W+20*Q*Q+burst-a
    # a*n*n+c*n <= H. A short integer bisection avoids signed-root rounding.
    lo=0;hi=isqrt(horizon//a)+1
    while lo+1<hi:
        m=(lo+hi)//2
        if a*m*m+c*m<=horizon:lo=m
        else:hi=m
    late=isqrt(isqrt(horizon))
    return {'L':L,'D':D,'Q':Q,'radius':R,'ell':ell,'burst':burst,
            'n':lo,'late_birth':late,'count':max(0,lo-initial_mass-2*late),
            'quadratic_coefficient':a,'linear_coefficient':c}
