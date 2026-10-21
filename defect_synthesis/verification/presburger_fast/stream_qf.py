"""Quantifier-free linear-integer encoding of complete bounded-power ant traces.

Loops must restore heading and have one of the fixed nonzero strides below.
The initial field is a finite XOR of finite arithmetic segments and singletons.
All exponent/coordinate domains remain unbounded. No sampled cutoff is used.

The arithmetic circuit checks only parity-change boundaries on each read stream.
It does not build the quadratic global same-cell successor relation or run QE.
It is an exact supplied-schema encoding, NOT a complete HC decision procedure.
"""
from __future__ import annotations
import _paths  # Pin and load the unchanged sibling schema syntax.
from dataclasses import dataclass
from math import gcd
import re
from typing import Iterable
from compiler import Affine, Power, Schema, as_affine, geometry

STRIDES=frozenset({(2,2),(2,-2),(-2,2),(-2,-2),
                   (2,0),(-2,0),(0,2),(0,-2),
                   (4,0),(-4,0),(0,4),(0,-4)})
Expr=int|bool|str

def atom(x: Expr) -> str:
    if x is True:return 'true'
    if x is False:return 'false'
    if type(x) is int:return str(x) if x>=0 else f'(- {-x})'
    return x

class Circuit:
    """Hash-consed definitional DAG. Constant division uses linear inequalities."""
    def __init__(self, parameters: Iterable[str]):
        self.parameters=tuple(parameters)
        if len(set(self.parameters))!=len(self.parameters):raise ValueError('duplicate parameter')
        if any(not re.fullmatch('[a-zA-Z][a-zA-Z0-9_]*',p) or p.startswith('aux') for p in self.parameters):
            raise ValueError('invalid parameter or reserved aux prefix')
        self.lines=[f'(declare-const {p} Int)' for p in self.parameters]
        self.cache={};self.nodes=0;self.divisions=0
    def fresh(self,sort):
        name=f'aux{self.nodes}';self.nodes+=1
        self.lines.append(f'(declare-const {name} {sort})');return name
    def node(self,sort,op,args):
        key=(sort,op,tuple(atom(a) for a in args))
        if key in self.cache:return self.cache[key]
        name=self.fresh(sort)
        self.lines.append(f'(assert (= {name} ({op} '+ ' '.join(key[2])+')))')
        self.cache[key]=name;return name
    def add(self,*args):
        const=sum(x for x in args if type(x) is int)
        rest=[x for x in args if type(x) is not int]
        if const:rest.append(const)
        if not rest:return 0
        if len(rest)==1:return rest[0]
        return self.node('Int','+',rest)
    def mul(self,c:int,x):
        if type(c) is not int:raise TypeError('fixed integer coefficient required')
        if c==0:return 0
        if c==1:return x
        if type(x) is int:return c*x
        return self.node('Int','*',[c,x])
    def sub(self,a,b):
        if a==b:return 0
        return self.add(a,self.mul(-1,b))
    def eq(self,a,b):
        if a==b:return True
        if type(a) in (int,bool) and type(b) in (int,bool):return a==b
        return self.node('Bool','=',[a,b])
    def le(self,a,b):
        if a==b:return True
        if type(a) is int and type(b) is int:return a<=b
        return self.node('Bool','<=',[a,b])
    def lt(self,a,b):return self.le(self.add(a,1),b)
    def not_(self,a):
        if type(a) is bool:return not a
        return self.node('Bool','not',[a])
    def and_(self,*args):
        if any(a is False for a in args):return False
        args=list(dict.fromkeys(a for a in args if a is not True))
        if not args:return True
        if len(args)==1:return args[0]
        return self.node('Bool','and',args)
    def or_(self,*args):
        if any(a is True for a in args):return True
        args=list(dict.fromkeys(a for a in args if a is not False))
        if not args:return False
        if len(args)==1:return args[0]
        return self.node('Bool','or',args)
    def ite(self,cond,yes,no,sort='Int'):
        if cond is True:return yes
        if cond is False:return no
        if yes==no:return yes
        return self.node(sort,'ite',[cond,yes,no])
    def xor(self,args):
        parity=False; terms=set()
        for x in args:
            if type(x) is bool:parity^=x
            elif x in terms:terms.remove(x)
            else:terms.add(x)
        vals=sorted(terms)
        if not vals:return parity
        result=vals[0] if len(vals)==1 else self.node('Bool','xor',vals)
        return self.not_(result) if parity else result
    def implies(self,a,b):return self.or_(self.not_(a),b)
    def floor(self,a,d:int):
        if type(d) is not int or d<=0:raise ValueError('positive fixed divisor required')
        if d==1:return a
        if type(a) is int:return a//d
        key=('floor',atom(a),d)
        if key in self.cache:return self.cache[key]
        q=self.fresh('Int');self.divisions+=1
        self.lines.append(f'(assert (and (<= (* {d} {q}) {atom(a)}) (< {atom(a)} (* {d} (+ {q} 1)))))')
        self.cache[key]=q;return q
    def ceil(self,a,d):return self.mul(-1,self.floor(self.mul(-1,a),d))
    def affine(self,a):
        a=as_affine(a)
        if set(dict(a.terms))-set(self.parameters):raise ValueError('undeclared affine parameter')
        return self.add(a.const,*(self.mul(c,p) for p,c in a.terms))
    def affine_quotient(self,a,d:int):
        a=as_affine(a)
        if d<0:a=-a;d=-d
        if d==0:raise ValueError('zero divisor')
        if all(co%d==0 for _,co in a.terms):
            return self.affine(Affine(a.const//d,tuple((v,co//d) for v,co in a.terms))),a.const%d==0
        value=self.affine(a);q=self.floor(value,d)
        return q,self.eq(self.mul(d,q),value)
    def text(self,assertion=None):
        out='\n'.join(self.lines)+'\n'
        if assertion is not None:out+='(assert '+atom(assertion)+')\n'
        return out

@dataclass(frozen=True)
class Segment:
    anchor:tuple[Affine,Affine]
    stride:tuple[int,int]=(0,0)
    length:Affine=Affine(1)
    def __post_init__(self):
        if len(self.anchor)!=2:raise ValueError('two-dimensional anchor required')
        object.__setattr__(self,'anchor',tuple(map(as_affine,self.anchor)))
        object.__setattr__(self,'length',as_affine(self.length))
        if self.stride not in STRIDES and self.stride!=(0,0):raise ValueError('unsupported fixed stride')
        if self.stride==(0,0) and self.length!=Affine(1):
            raise ValueError('zero stride is exactly one cell, not a repeated XOR')

@dataclass(frozen=True)
class Read:
    segment:Segment
    block:int
    phase:int
    period:int
    bit:bool

@dataclass(frozen=True)
class Interval:
    active:Expr
    lo:Expr
    hi:Expr


def records(schema:Schema):
    """Disjoint chronological blocks; same-power phases retain epoch order."""
    x,y=schema.pose;h=schema.heading;out=[];block=0
    for part in schema.parts:
        word=part.word if isinstance(part,Power) else part
        phases,d,nh=geometry(word,h)
        if isinstance(part,Power):
            if d not in STRIDES:raise ValueError('powered words need an approved NONZERO drift')
            for i,(p,_,ch) in enumerate(phases):
                out.append(Read(Segment((x+p[0],y+p[1]),d,part.exponent),block,i,len(word),ch=='L'))
            x=x+d[0]*part.exponent;y=y+d[1]*part.exponent;block+=1
        else:
            for i,(p,_,ch) in enumerate(phases):
                out.append(Read(Segment((x+p[0],y+p[1])),block,0,1,ch=='L'));block+=1
            x=x+d[0];y=y+d[1]
        h=nh
    return out

class Encoder:
    def __init__(self,schema:Schema,source:Iterable[Segment],*,method='jumps'):
        if method not in ('jumps','values'):raise ValueError('unknown parity encoding')
        self.method=method
        # Arbitrary ISL/quantified source domains are deliberately NOT silently parsed.
        canonical=' and '.join(['(1=1)']+[f'{p.exponent}>=0' for p in schema.parts if isinstance(p,Power)])
        if schema.guard!=canonical:raise ValueError('use domain=1=1; add QF domain constraints at solver call')
        self.schema=schema;self.source=tuple(source);self.reads=records(schema)
        for seg in self.source:
            for value in (*seg.anchor,seg.length):
                if set(dict(value.terms))-set(schema.parameters):
                    raise ValueError('undeclared source parameter')
        self.c=Circuit(schema.parameters);self.interval_count=0;self.probe_count=0
        blocks={}
        for r in self.reads:blocks.setdefault(r.block,[]).append(r)
        earlier={};net=set()
        for b,rs in blocks.items():
            earlier[b]=tuple(sorted(net,key=repr))
            for r in rs:
                if r.segment in net:net.remove(r.segment)
                else:net.add(r.segment)
        srcnet=set()
        for s in self.source:
            if s in srcnet:srcnet.remove(s)
            else:srcnet.add(s)
        srcnet=tuple(sorted(srcnet,key=repr))
        self.prefix_net_terms=sum(len(v) for v in earlier.values())
        guards=[self.c.le(0,self.c.affine(s.length)) for s in self.source]
        guards += [self.c.le(0,self.c.affine(p.exponent)) for p in schema.parts if isinstance(p,Power)]
        for i,read in enumerate(self.reads):
            if read.segment.stride==(0,0):
                terms=[self.member(s,read.segment.anchor) for s in srcnet]
                terms += [self.member(seg,read.segment.anchor) for seg in earlier[read.block]]
                guards.append(self.c.eq(self.c.xor(terms),read.bit));self.probe_count+=1
                continue
            for residue in (0,1):
                ivals=[self.intersection(read.segment,s,residue) for s in (*srcnet,*earlier[read.block])]
                for r in blocks[read.block]:
                    if r.block==read.block:
                        # l=j+shift, so the time comparison is the fixed integer
                        # period*shift+earlier_phase < current_phase.
                        delta=tuple(a-b for a,b in zip(read.segment.anchor,r.segment.anchor))
                        if any(z.terms for z in delta):raise AssertionError('same-block anchors lost cancellation')
                        ds=read.segment.stride;axis=0 if ds[0] else 1
                        num=delta[axis].const
                        if num%ds[axis]:continue
                        shift=num//ds[axis]
                        if tuple(shift*d for d in ds)!=tuple(z.const for z in delta):continue
                        if r.period*shift+r.phase>=read.phase:continue
                        lo=self.c.ceil(-shift-residue,2)
                        hi=self.c.floor(self.c.add(self.c.affine(r.segment.length),-1-shift-residue),2)
                        ivals.append(Interval(True,lo,hi))
                ivals=[v for v in ivals if v.active is not False]
                self.interval_count+=len(ivals)
                end=self.c.floor(self.c.add(self.c.affine(read.segment.length),-1-residue),2)
                if method=='values':
                    probes=list(dict.fromkeys([0]+[a for v in ivals for a in (v.lo,self.c.add(v.hi,1))]))
                    for p in probes:
                        inrange=self.c.and_(self.c.le(0,p),self.c.le(p,end))
                        if inrange is False:continue
                        parity=self.c.xor(self.c.and_(v.active,self.c.le(v.lo,p),self.c.le(p,v.hi)) for v in ivals)
                        guards.append(self.c.implies(inrange,self.c.eq(parity,read.bit)))
                        self.probe_count+=1
                else:
                    # A step function is constant exactly when its initial value
                    # is right and every interior XOR jump vanishes. Coincident
                    # syntactic endpoints are combined BEFORE any pair tests.
                    initial=self.c.xor(self.c.and_(v.active,self.c.le(v.lo,0),self.c.le(0,v.hi)) for v in ivals)
                    guards.append(self.c.implies(self.c.le(0,end),self.c.eq(initial,read.bit)))
                    self.probe_count+=1
                    changes={}
                    for v in ivals:
                        active=self.c.and_(v.active,self.c.le(v.lo,v.hi))
                        if active is False:continue
                        for p in (v.lo,self.c.add(v.hi,1)):changes.setdefault(p,[]).append(active)
                    changes={p:self.c.xor(bits) for p,bits in changes.items()}
                    changes={p:bits for p,bits in changes.items() if bits is not False}
                    for p,active in changes.items():
                        inrange=self.c.and_(active,self.c.lt(0,p),self.c.le(p,end))
                        if inrange is False:continue
                        jump=self.c.xor(self.c.and_(bits,self.c.eq(p,q)) for q,bits in changes.items())
                        guards.append(self.c.implies(inrange,self.c.not_(jump)))
                        self.probe_count+=1
        self.valid=self.c.and_(*guards)
    def member(self,s:Segment,point:tuple[Affine,Affine]):
        c=self.c;delta=tuple(c.affine(a-b) for a,b in zip(point,s.anchor))
        if s.stride==(0,0):return c.and_(c.eq(delta[0],0),c.eq(delta[1],0))
        axis=0 if s.stride[0] else 1;a=s.stride[axis]
        q=c.floor(c.mul(1 if a>0 else -1,delta[axis]),abs(a))
        return c.and_(c.le(0,q),c.lt(q,c.affine(s.length)),
                      c.eq(delta[0],c.mul(s.stride[0],q)),c.eq(delta[1],c.mul(s.stride[1],q)))
    def intersection(self,s:Segment,r:Segment,residue:int):
        """All z with s(2z+residue) in r; one guarded integer interval.

        Current-domain clipping is done at probes, not approximated here.
        """
        c=self.c;ds=s.stride;dr=r.stride
        da=tuple(a-b for a,b in zip(r.anchor,s.anchor))
        delta=tuple(c.affine(a) for a in da)
        axis=0 if ds[0] else 1
        if dr==(0,0):
            a=ds[axis];j,exact=c.affine_quotient(da[axis],a)
            collinear=c.eq(c.affine(ds[1]*da[0]-ds[0]*da[1]),0)
            if exact is False or collinear is False:return Interval(False,0,-1)
            z=c.floor(c.add(j,-residue),2)
            active=c.and_(exact,collinear,c.eq(j,c.add(c.mul(2,z),residue)))
            return Interval(active,z,z)
        den=ds[0]*dr[1]-ds[1]*dr[0]
        if den:
            ja=dr[1]*da[0]-dr[0]*da[1];la=ds[1]*da[0]-ds[0]*da[1]
            j,jexact=c.affine_quotient(ja,den);l,lexact=c.affine_quotient(la,den)
            if jexact is False or lexact is False:return Interval(False,0,-1)
            z=c.floor(c.add(j,-residue),2)
            active=c.and_(jexact,lexact,
                          c.le(0,l),c.lt(l,c.affine(r.length)),c.eq(j,c.add(c.mul(2,z),residue)))
            return Interval(active,z,z)
        alpha,beta=ds[axis],dr[axis];g=gcd(abs(alpha),abs(beta));mod=abs(beta)//g
        if mod not in (1,2):raise AssertionError('closed-stride modulus exceeded')
        dc=delta[axis];quot,exact=c.affine_quotient(da[axis],g)
        collinear=c.eq(c.affine(ds[1]*da[0]-ds[0]*da[1]),0)
        if collinear is False or exact is False:return Interval(False,0,-1)
        active=c.and_(collinear,exact,c.lt(0,c.affine(r.length)))
        if mod==2:
            # alpha/g is odd, inverse modulo 2 is 1 even if alpha is negative.
            active=c.and_(active,c.eq(c.sub(quot,c.mul(2,c.floor(quot,2))),residue))
        last=c.add(dc,c.mul(beta,c.add(c.affine(r.length),-1)))
        low,high=(dc,last) if beta>0 else (last,dc)
        if alpha<0:low,high=c.mul(-1,high),c.mul(-1,low)
        a=abs(alpha)
        lo=c.ceil(c.add(low,-a*residue),2*a);hi=c.floor(c.add(high,-a*residue),2*a)
        return Interval(active,lo,hi)
    def black_at(self,point:tuple[Affine,Affine]):
        """Exact complete endpoint membership, even for untouched input debris."""
        return self.c.xor([self.member(s,point) for s in self.source]+
                          [self.member(r.segment,point) for r in self.reads])
    def stats(self):
        return dict(read_streams=len(self.reads),source_segments=len(self.source),
                    intervals=self.interval_count,probes=self.probe_count,
                    prefix_net_terms=self.prefix_net_terms,
                    circuit_nodes=self.c.nodes,constant_divisions=self.c.divisions,
                    smt_bytes=len(self.c.text(self.valid).encode()))
    def smt(self):return self.c.text(self.valid)


def point_source(points):return tuple(Segment(tuple(map(as_affine,p))) for p in points)

def distinct_formula(points):
    """A sparse LIST needs this condition; general segment inputs denote XOR."""
    def af(a):
        a=as_affine(a);terms=[atom(a.const)]+[f'(* {atom(c)} {p})' for p,c in a.terms]
        return '(+ '+' '.join(terms)+')'
    out=[]
    for i,(x,y) in enumerate(points):
        for u,v in points[:i]:out.append(f'(or (distinct {af(x)} {af(u)}) (distinct {af(y)} {af(v)}))')
    return '(and '+' '.join(out)+')' if out else 'true'
