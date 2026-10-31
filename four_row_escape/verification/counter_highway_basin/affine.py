"""Small integer kernel for ALL-parameter horizontal affine-strip replay.

No solver, symbolic engine, rounding approximation, or sampled cutoff. Fields
are full XOR sets of finite arithmetic intervals. Equality/inequality decisions
use Python integers, and the parameter domain is every k>=kmin.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass

@dataclass(frozen=True,order=True)
class Aff:
    a:int=0
    b:int=0
    def __post_init__(self):
        if type(self.a)is not int or type(self.b)is not int:raise ValueError('integer affine coefficients required')
    def __call__(self,k):return self.a*k+self.b
    def __add__(self,other):
        other=other if isinstance(other,Aff) else Aff(0,other)
        return Aff(self.a+other.a,self.b+other.b)
    __radd__=__add__
    def __neg__(self):return Aff(-self.a,-self.b)
    def __sub__(self,other):return self+-other if isinstance(other,Aff) else self+(-other)
    def __mul__(self,c):return Aff(c*self.a,c*self.b)
    __rmul__=__mul__
    def pair(self):return [self.a,self.b]

ZERO=Aff()
ONE=Aff(0,1)

def toggle(s,value):
    if value in s:s.remove(value)
    else:s.add(value)


def positive_domain(forms,kmin):
    """The exact integer k interval on which every affine form is >=0."""
    low,high=kmin,None
    for f in forms:
        if f.a>0:low=max(low,-(f.b//f.a))  # ceil(-b/a)
        elif f.a<0:
            h=f.b//(-f.a)
            high=h if high is None else min(high,h)
        elif f.b<0:return None
    return None if high is not None and low>high else (low,high)


def nonnegative(f,kmin):
    if f.a<0 or f(kmin)<0:raise AssertionError(('not nonnegative for all k',f,kmin))


def constant_zero_at_origin(edges,kmin):
    """Check XOR_[t in edges] [0>=t(k)] for every integer k>=kmin.

    Every affine sign is constant between consecutive roots. Singleton integer
    roots are separated by including floor(root) AND floor(root)+1 as starts.
    """
    starts={kmin}
    for f in edges:
        if f.a:
            z=(-f.b)//f.a
            starts.update(v for v in (z,z+1)if v>=kmin)
    for k in sorted(starts):
        if sum(f(k)<=0 for f in edges)%2:
            raise AssertionError(('incorrect read',k,0))
    return len(starts)


def zero_on_epochs(edges,count,kmin):
    """Prove XOR_[t] [j>=t(k)] == 0 for all k>=kmin, 0<=j<count(k).

    Distinct affine jump locations can coincide at at most one k per pair.
    For a jump to be harmless at EVERY interior epoch, its entire interior-k
    interval must be covered by exact even-multiplicity coincidences. This is
    checked exhaustively by finite integer intersections, not by a k cutoff.
    """
    nonnegative(count-1,kmin) # all delivered blocks have at least one repetition
    signs=constant_zero_at_origin(edges,kmin)
    intersections=interior_parameters=0
    ordered=sorted(edges)
    for i,f in enumerate(ordered):
        interval=positive_domain((f-1,count-1-f),kmin)
        if interval is None:continue
        lo,hi=interval
        if hi is None:raise AssertionError(('uncancelled infinite interior jump',f,lo))
        collisions=set()
        for g in ordered:
            if f==g or f.a==g.a:continue
            numerator=g.b-f.b;denominator=f.a-g.a
            if numerator%denominator==0:
                k=numerator//denominator
                if lo<=k<=hi:collisions.add(k)
        intersections+=len(collisions)
        if len(collisions)!=hi-lo+1:
            raise AssertionError(('interior jump interval not covered',f,lo,hi,sorted(collisions)))
        for k in collisions:
            interior_parameters+=1
            if sum(g(k)==f(k)for g in ordered)%2:
                raise AssertionError(('odd interior jump',k,f(k)))
    return {'origin_sign_regions':signs,'interior_coincidences':intersections,
            'interior_parameter_checks':interior_parameters}


class Field:
    """Full field: for row y and parity r, black at x=2z+r iff XOR[z>=e(k)]."""
    def __init__(self,kmin):self.kmin=kmin;self.ends=defaultdict(set)
    def interval(self,y,r,lo,hi):
        nonnegative(hi-lo+1,self.kmin)
        toggle(self.ends[y,r],lo);toggle(self.ends[y,r],hi+1)
    def point(self,x,y):
        if x.a%2:raise ValueError('parameter-dependent parity is outside this kernel')
        r=x.b%2;z=Aff(x.a//2,(x.b-r)//2)
        self.interval(y,r,z,z)
    def repeat(self,x,y,dx,count):
        if dx not in (-2,2)or x.a%2:raise ValueError('expected horizontal two-cell stride')
        r=x.b%2;z=Aff(x.a//2,(x.b-r)//2)
        if dx==2:self.interval(y,r,z,z+count-1)
        else:self.interval(y,r,z-count+1,z)
    def jump_set(self,x,y,dx=2):
        if dx not in (-2,2)or x.a%2:raise ValueError('unsupported query geometry')
        r=x.b%2;z=Aff(x.a//2,(x.b-r)//2);es=self.ends[y,r]
        if len(es)%2:raise AssertionError('field not finite in this row')
        return {e-z for e in es}if dx==2 else{z-e+1 for e in es}
    def read_constant(self,x,y,black):
        es=self.jump_set(x,y)
        if black:toggle(es,ZERO)
        return zero_on_epochs(es,ONE,self.kmin)
    def evaluate(self,k):
        if k<self.kmin:raise ValueError('parameter outside certified domain')
        out=set()
        for (y,r),es in self.ends.items():
            points=[]
            for e in es:points.append(e(k))
            points.sort();active=False;last=None
            for v in points:
                if active:out.update((2*z+r,y)for z in range(last,v))
                active=not active;last=v
            if active:raise AssertionError('unbounded row')
        return out
    def compact(self):
        return [[y,r,[e.pair()for e in sorted(es)]]for(y,r),es in sorted(self.ends.items())if es]
