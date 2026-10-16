"""Exact Presburger compiler for heading-resetting bounded-power LR traces.

This module compiles ONE supplied schema, not an unbounded-event HC query.
All read identities, including nonadjacent blocks, enter a lexicographic
same-cell successor relation. All unqueried initial black cells are retained.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
import re
from typing import Iterable
from isl_exact import Context, Object

DIRS = ((0,1),(1,0),(0,-1),(-1,0))
W = ('RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRL'
     'LRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR')
A = 'LLRRRRLRRLRRRRLLLLRLRRRRLRLL'
B = ('RRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLRRRRLRLLLLRRRR'
     'LRRLRRRRLLLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRLL')
T = 'RRRRLLRLLRRRRLLRRRRLLRLL'
L10 = frozenset((W*2)[i:i+10] for i in range(104))

@dataclass(frozen=True)
class Affine:
    const: int = 0
    terms: tuple[tuple[str,int], ...] = ()
    def __post_init__(self):
        if type(self.const) is not int:
            raise TypeError('integer constant required')
        names = []
        for v,c in self.terms:
            if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_]*', v) or type(c) is not int:
                raise ValueError('invalid affine coefficient')
            names.append(v)
        if len(names)!=len(set(names)):
            raise ValueError('duplicate affine variables')
    def __add__(self, other):
        other = as_affine(other)
        d = dict(self.terms)
        for v,c in other.terms: d[v]=d.get(v,0)+c
        return Affine(self.const+other.const, tuple(sorted((v,c) for v,c in d.items() if c)))
    __radd__=__add__
    def __neg__(self): return self*-1
    def __sub__(self, other): return self+-as_affine(other)
    def __mul__(self, c):
        if type(c) is not int: raise TypeError('only multiplication by a fixed integer is allowed')
        return Affine(self.const*c, tuple((v,c*a) for v,a in self.terms if c*a))
    __rmul__=__mul__
    def evaluate(self, values): return self.const+sum(c*values[v] for v,c in self.terms)
    def __str__(self):
        return '('+' + '.join([str(self.const)]+[f'{c}*{v}' for v,c in self.terms])+')'

def as_affine(v):
    if isinstance(v,Affine): return v
    if type(v) is int: return Affine(v)
    raise TypeError('expected Affine or integer')

def var(name): return Affine(0, ((name,1),))

def geometry(word: str, heading: int = 0):
    if set(word)-{'R','L'} or type(heading) is not int or heading not in range(4):
        raise ValueError('invalid word or heading')
    p=(0,0); h=heading; phases=[]
    for ch in word:
        phases.append((p,h,ch))
        h=(h+(1 if ch=='R' else -1))%4
        d=DIRS[h]; p=(p[0]+d[0],p[1]+d[1])
    return phases,p,h

@dataclass(frozen=True)
class Power:
    word: str
    exponent: Affine
    def __post_init__(self):
        if not self.word or set(self.word)-{'R','L'}:
            raise ValueError('nonempty R/L repeat word required')
        if geometry(self.word)[2] != 0:
            raise ValueError('each powered word must restore heading')
        object.__setattr__(self,'exponent',as_affine(self.exponent))

class Schema:
    def __init__(self, parameters: Iterable[str], parts: Iterable[str|Power], *,
                 heading: int = 0, pose=(0,0), domain: str = '1=1'):
        self.parameters=tuple(parameters); self.parts=tuple(parts)
        if len(self.parameters)!=len(set(self.parameters)):
            raise ValueError('duplicate parameter')
        for p in self.parameters:
            if not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_]*',p) or p in {'x','y','t','b','s','d','j','out_t','out_x','out_y','out_h'}:
                raise ValueError(f'invalid or reserved parameter {p}')
        if type(heading) is not int or heading not in range(4):
            raise ValueError('heading must be 0..3')
        self.heading=heading; self.pose=tuple(map(as_affine,pose))
        if len(self.pose)!=2: raise ValueError('pose must have two coordinates')
        powers=[]
        for part in self.parts:
            if isinstance(part,Power): powers.append(part.exponent)
            elif not isinstance(part,str) or set(part)-{'R','L'}: raise ValueError('bad fixed word')
        for e in [*powers,*self.pose]:
            if set(dict(e.terms))-set(self.parameters): raise ValueError('undeclared parameter')
        self.guard=' and '.join([f'({domain})']+[f'{e}>=0' for e in powers])
        self.header='['+','.join(self.parameters)+'] -> '
        x,y=self.pose; time=Affine(); h=heading; records=[]
        for part in self.parts:
            word=part.word if isinstance(part,Power) else part
            phases,drift,end_h=geometry(word,h)
            for i,(p,_,ch) in enumerate(phases):
                if isinstance(part,Power):
                    cond=(f'exists (j: 0<=j<{part.exponent} and '
                          f'x={x+p[0]}+{drift[0]}*j and y={y+p[1]}+{drift[1]}*j and '
                          f't={time+i}+{len(word)}*j and b={int(ch=="L")})')
                else:
                    cond=f'x={x+p[0]} and y={y+p[1]} and t={time+i} and b={int(ch=="L")}'
                records.append('[x,y] -> [t,b] : '+self.guard+' and ('+cond+')')
            exponent=part.exponent if isinstance(part,Power) else Affine(1)
            x=x+drift[0]*exponent; y=y+drift[1]*exponent; time=time+len(word)*exponent
            h=end_h
        self.end_pose=(x,y); self.end_heading=h; self.length=time
        self.read_text=self.header+'{ '+('; '.join(records) if records else '[x,y] -> [t,b] : false')+' }'
        self.record_count=len(records)
    def param_set(self, ctx, extra='1=1'):
        return ctx.set(self.header+'{ : '+self.guard+' and ('+extra+') }')
    def black_set(self, ctx, formula):
        return ctx.set(self.header+'{ [x,y] : '+self.guard+' and ('+formula+') }')
    def endpoint_map(self, ctx, domain: Object):
        x,y=self.end_pose
        return ctx.map(self.header+f'{{ [] -> [out_t,out_x,out_y,out_h] : '
                       f'out_t={self.length} and out_x={x} and out_y={y} and out_h={self.end_heading} }}').intersect_params(domain)
    def expand(self, values, limit=1000000):
        length=self.length.evaluate(values)
        if length<0 or length>limit: raise ValueError('literal expansion exceeds cap or has negative length')
        words=[]
        for p in self.parts:
            if isinstance(p,Power):
                k=p.exponent.evaluate(values)
                if k<0: raise ValueError('negative power')
                words.append(p.word*k)
            else: words.append(p)
        return ''.join(words)

@dataclass
class Compiled:
    schema: Schema
    reads: Object
    feasible: Object
    first_black: Object
    first_white: Object
    visited: Object
    last_white: Object
    source: Object
    endpoint: Object
    conflicts: Object
    def endpoint_query(self):
        return self.endpoint.intersect_params(self.feasible)
    def endpoint_identity_domain(self, target: Object):
        mismatches=self.endpoint.subtract(target).union(target.subtract(self.endpoint)).params()
        return self.feasible.subtract(mismatches).coalesce()

def compile_schema(schema: Schema, ctx: Context, source: Object|None=None) -> Compiled:
    """Use source=None to synthesize the minimal first-L field for each parameter.

    Supplying an explicit source checks BOTH first-black and first-white reads.
    Every returned domain is exact for this supplied schema. It is never labelled
    as an all-schema/all-input exclusion by this function.
    """
    R=ctx.map(schema.read_text)
    guard=schema.param_set(ctx)
    pairs=R.reverse().apply_range(R)
    later=ctx.map(schema.header+'{ [t,b] -> [s,d] : s>t }')
    equal=ctx.map(schema.header+'{ [t,b] -> [s,d] : b=d }')
    bad=pairs.intersect(later).lexmin().intersect(equal).params()
    feasible=guard.subtract(bad)
    first=R.lexmin()
    black_mask=ctx.map(schema.header+'{ [x,y] -> [t,b] : b=1 }')
    white_mask=ctx.map(schema.header+'{ [x,y] -> [t,b] : b=0 }')
    first_black=first.intersect(black_mask).domain().coalesce()
    first_white=first.intersect(white_mask).domain().coalesce()
    visited=R.domain().coalesce()
    last_white=R.lexmax().intersect(white_mask).domain().coalesce()
    if source is None:
        source=first_black
    else:
        source=source.intersect_params(guard)
        bad_source=first_black.subtract(source).union(first_white.intersect(source)).params()
        feasible=feasible.subtract(bad_source)
    endpoint=source.subtract(visited).union(last_white).coalesce()
    return Compiled(schema,R,feasible.coalesce(),first_black,first_white,visited,
                    last_white,source,endpoint,bad.coalesce())

def exact_seed_formula(coordinates):
    pairs=list(coordinates)
    black=' or '.join(f'(x={a} and y={b})' for a,b in pairs) or 'false'
    distinct=' and '.join(f'({a}!={c} or {b}!={d})'
             for i,(a,b) in enumerate(pairs) for c,d in pairs[:i]) or '1=1'
    return black,distinct

def scan_factors(history: str, word: str):
    if len(history)>9 or set(history+word)-{'L','R'}: raise ValueError('invalid factor input')
    count=0; last=False
    for ch in word:
        w=history+ch
        last=len(w)==10 and w not in L10
        count+=last; history=w[-9:]
    return history,count,last

@dataclass(frozen=True)
class FactorCase:
    condition: str
    count: Affine
    history: str
    last_bad: bool
    nonempty: bool

def factor_cases(schema: Schema):
    """Exact forward-contained defect counts, including zero/short powers.

    After ceil(9/|u|) copies of u, the suffix register is fixed at its
    end-of-u phase. Each additional copy contributes one constant defect count.
    No claim is made that removing copies preserves physical feasibility.
    """
    cases=[FactorCase('1=1',Affine(),'',False,False)]
    for part in schema.parts:
        new=[]
        for c in cases:
            if isinstance(part,str):
                if not part: new.append(c); continue
                h,d,last=scan_factors(c.history,part)
                new.append(FactorCase(c.condition,c.count+d,h,last,True))
                continue
            q=(9+len(part.word)-1)//len(part.word)
            for k in range(q):
                h,d,last=scan_factors(c.history,part.word*k)
                new.append(FactorCase(c.condition+f' and {part.exponent}={k}',c.count+d,h,
                                      last if k else c.last_bad,c.nonempty or k>0))
            h,d,last=scan_factors(c.history,part.word*q)
            h2,inc,last2=scan_factors(h,part.word)
            if h!=h2: raise AssertionError('suffix stabilization failed')
            # At the q-copy boundary, the final window may be absent (length=9).
            # Split k=q from k>q if the last-event flag differs.
            tail=c.count+d+(part.exponent-q)*inc
            if last==last2:
                new.append(FactorCase(c.condition+f' and {part.exponent}>={q}',tail,h,last,True))
            else:
                new.append(FactorCase(c.condition+f' and {part.exponent}={q}',c.count+d,h,last,True))
                new.append(FactorCase(c.condition+f' and {part.exponent}>={q+1}',tail,h,last2,True))
        cases=new
    return cases

def defect_domain(schema: Schema, ctx: Context, number: int, *,
                  exact: bool=False, ends_bad: bool=False):
    if type(number) is not int or number<0: raise ValueError('nonnegative count required')
    conditions=[]
    for c in factor_cases(schema):
        if ends_bad and not (c.last_bad and c.nonempty): continue
        relation='=' if exact else '>='
        conditions.append(f'({c.condition} and {c.count}{relation}{number})')
    return schema.param_set(ctx,' or '.join(conditions) or 'false').coalesce()
