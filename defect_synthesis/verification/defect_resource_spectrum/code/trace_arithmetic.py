"""Exact Presburger semantics for finite or ultimately periodic ant path schemas.

The input is a finite list of fixed words and heading-restoring powers. Counts
and seed coordinates may depend affinely on unbounded integer parameters. Only
specified schemas are analyzed; this does NOT decide arbitrary ant trajectories.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Sequence
from isl_bridge import Context, Obj

DIRS=((0,1),(1,0),(0,-1),(-1,0))

@dataclass(frozen=True)
class Aff:
    const: int=0
    terms: tuple[tuple[str,int],...]=()
    @staticmethod
    def var(name: str):
        if not name.isidentifier():raise ValueError('invalid parameter')
        return Aff(0,((name,1),))
    def __add__(self,other):
        if isinstance(other,int): other=Aff(other)
        if not isinstance(other,Aff):return NotImplemented
        d=dict(self.terms)
        for k,v in other.terms:d[k]=d.get(k,0)+v
        return Aff(self.const+other.const,tuple(sorted((k,v) for k,v in d.items() if v)))
    __radd__=__add__
    def __mul__(self,n):
        if type(n) is not int:raise ValueError('only integer scalar multiplication')
        return Aff(self.const*n,tuple((k,v*n) for k,v in self.terms if v*n))
    __rmul__=__mul__
    def __neg__(self):return self*-1
    def __sub__(self,other):return self+(-other)
    def __str__(self):return '('+' + '.join([str(self.const)]+[f'{v}*{k}' for k,v in self.terms])+')'
    def evaluate(self,values):return self.const+sum(v*values[k] for k,v in self.terms)

def affine(value):return value if isinstance(value,Aff) else Aff(value)

@dataclass(frozen=True)
class Block:
    word: str
    count: Aff | int | None=1 # None is an infinite last repetition
    def __post_init__(self):
        if not self.word or set(self.word)-{'R','L'}:raise ValueError('invalid word')
        if self.count is not None and not isinstance(self.count,(int,Aff)):raise ValueError('non-affine count')

class Schema:
    def __init__(self, params: Sequence[str], blocks: Sequence[Block], *,
                 heading=0, domain='true', start=(0,0), ctx=None):
        if heading not in range(4) or len(set(params))!=len(params):raise ValueError('invalid pose or parameters')
        if any(not s.isidentifier() or s in ('t','u','x','y','j') for s in params):raise ValueError('reserved parameter')
        self.ctx=ctx or Context();self.params=tuple(params);self.blocks=tuple(blocks)
        self.heading=heading;self.start=tuple(map(affine,start));self.domain_text=domain
        self.prefix='['+','.join(params)+'] -> '
        guards=[domain];x,y=self.start;time=Aff();h=heading
        clauses={'R':[],'L':[]};self.phase_count=0;self.infinite=False;self.events=[]
        for bi,block in enumerate(blocks):
            count=None if block.count is None else affine(block.count)
            if count is None:
                if bi!=len(blocks)-1:raise ValueError('only final block can be infinite')
                self.infinite=True
            else:guards.append(f'{count}>=0')
            p=(0,0);hh=h;points=[]
            for letter in block.word:
                points.append(p);hh=(hh+(1 if letter=='R' else -1))%4
                d=DIRS[hh];p=p[0]+d[0],p[1]+d[1]
            if hh!=h and not(count is not None and not count.terms and count.const==1):
                raise ValueError('variable/infinite power must restore heading')
            size=len(block.word)
            for i,(letter,(px,py)) in enumerate(zip(block.word,points)):
                bound='j>=0'+(f' and j<{count}' if count is not None else '')
                clauses[letter].append('[t] -> [x,y] : exists (j : '+bound+
                    f' and t={time}+{size}*j+{i} and x={x}+{px}+{p[0]}*j and y={y}+{py}+{p[1]}*j)')
                self.events.append((bi,i,letter,time,size,count,x+px,y+py,p))
                self.phase_count+=1
            if count is not None:
                x=x+p[0]*count;y=y+p[1]*count;time=time+size*count;h=hh
        self.endpoint=None if self.infinite else (x,y,h,time)
        self.domain=self.ctx.set(self.prefix+'{ : '+' and '.join(f'({g})' for g in guards)+' }')
        def mapping(letter):
            if not self.infinite:
                text='; '.join(clauses[letter]) or '[t] -> [x,y] : false'
                return self.ctx.map(self.prefix+'{ '+text+' }').restrict(self.domain).coalesce()
            result=self.ctx.map(self.prefix+'{ [t] -> [x,y] : false }')
            for text in clauses[letter]:
                result=result.union(self.ctx.map(self.prefix+'{ '+text+' }'))
            return result.restrict(self.domain)
        self.right=mapping('R');self.left=mapping('L')
        self.positions=self.right.union(self.left)
        if not self.infinite:self.positions=self.positions.coalesce()
        self.times=self.positions.domain()
    def field(self,condition: str):
        """Low-level initial-color predicate; finiteness is a separate input promise."""
        return self.ctx.set(self.prefix+'{ [x,y] : '+condition+' }').restrict(self.domain)
    def point_field(self,points):
        """Finite union of explicitly supplied affine-coordinate singleton cells."""
        return self.field(' or '.join(f'(x={affine(x)} and y={affine(y)})' for x,y in points) or 'false')
    def segment_field(self,segments,xor=False):
        """All segments have fixed integer strides and finite affine lengths."""
        result=self.field('false')
        for x,y,dx,dy,length in segments:
            if type(dx) is not int or type(dy) is not int:raise ValueError('constant strides required')
            length=affine(length)
            item=self.field(f'exists (j : 0<=j<{length} and x={affine(x)}+{dx}*j and y={affine(y)}+{dy}*j)')
            result=(result.subtract(item).union(item.subtract(result)) if xor else result.union(item))
        return result.coalesce()
    def reads(self):
        strict=self.ctx.map(self.prefix+'{ [t] -> [u] : t<u }')
        if len(self.blocks)==1 and self.events and self.events[0][-1]!=(0,0):
            # Direct expansion of the SAME relation for one translating power.
            # This avoids costly generic coalescing; it changes no constraint.
            d=self.events[0][-1];P=len(self.blocks[0].word);count=self.events[0][5]
            result=self.ctx.map(self.prefix+'{ [t] -> [u] : false }')
            for _,i,_,base,_,_,x,y,_ in self.events:
                for _,j,_,_,_,_,xx,yy,_ in self.events:
                    vx=xx-x;vy=yy-y
                    if vx.terms or vy.terms:raise AssertionError('nonconstant phase offset')
                    va=(vx.const,vy.const);axis=0 if d[0] else 1
                    if va[axis]%d[axis]:continue
                    k=va[axis]//d[axis]
                    if va!=(k*d[0],k*d[1]):continue
                    delta=j-i-k*P
                    if delta<=0:continue
                    bound=f'a>=0 and a>={k}'
                    if count is not None:bound+=f' and a<{count} and a-({k})<{count}'
                    text=self.prefix+f'{{ [t] -> [u] : exists (a : {bound} and t={P}*a+{i} and u=t+{delta}) }}'
                    result=result.union(self.ctx.map(text))
            return result
        return self.positions.then(self.positions.reverse()).intersect(strict).coalesce()
    def analyze(self,initial: Obj | None=None,method='composition',want_endpoint=True):
        same=self.reads()
        if method=='composition':
            successive=same.subtract(same.then(same)).coalesce()
        elif method=='lexmin':
            self.ctx._bind('isl_map_lexmin',[__import__('ctypes').c_void_p],__import__('ctypes').c_void_p)
            successive=same.op('lexmin').coalesce()
        else:raise ValueError('unknown successor method')
        rt=self.right.domain();lt=self.left.domain()
        bad=successive.on_domain(rt).on_range(rt).union(successive.on_domain(lt).on_range(lt)).params()
        first=self.times.subtract(same.range()).coalesce()
        first_left=first.intersect(lt)
        if initial is not None:
            hits=self.positions.on_range(initial).domain()
            bad=bad.union(first_left.subtract(hits).params())
            bad=bad.union(first.intersect(rt).intersect(hits).params())
        good=self.domain.subtract(bad).coalesce()
        output={'good':good,'same_cell_before':same,'successive':successive,
                'first_times':first,'required_initial_black':self.positions.on_domain(first_left).range().restrict(good).coalesce()}
        if initial is not None and not self.infinite and want_endpoint:
            last=self.times.subtract(same.domain())
            result=initial.subtract(self.positions.range()).union(self.positions.on_domain(last.intersect(rt)).range())
            output['final_black']=result.restrict(good).coalesce()
        return output
    def instantiate(self,values: Mapping[str,int],max_steps=100000):
        if self.infinite:raise ValueError('infinite word has no finite expansion')
        chunks=[]
        for b in self.blocks:
            n=affine(b.count).evaluate(values)
            if n<0:raise ValueError('negative count')
            if len(b.word)*n+sum(map(len,chunks))>max_steps:raise ValueError('expansion limit')
            chunks.append(b.word*n)
        return ''.join(chunks)
    def at(self,obj,values):
        if set(values)!=set(self.params):raise ValueError('complete assignment needed')
        fix=self.ctx.set(self.prefix+'{ : '+(' and '.join(f'{k}={v}' for k,v in values.items()) or 'true')+' }')
        return obj.restrict(fix)

    def defect_times(self, legal_factors: set[str]):
        """End times of wholly forward-contained factors outside a fixed whitelist."""
        if not legal_factors:raise ValueError('nonempty whitelist required')
        k=len(next(iter(legal_factors)))
        if k<1 or any(len(w)!=k or set(w)-{'R','L'} for w in legal_factors):raise ValueError('invalid whitelist')
        good=self.ctx.set(self.prefix+'{ [t] : false }')
        letter_times={'R':self.right.domain(),'L':self.left.domain()}
        shifts={}
        for c in 'RL':
            for j in range(k):
                move=self.ctx.map(self.prefix+f'{{ [t] -> [u] : u=t+{k-1-j} }}')
                shifts[c,j]=letter_times[c].apply(move)
        for word in sorted(legal_factors):
            part=self.times
            for j,c in enumerate(word):part=part.intersect(shifts[c,j])
            good=good.union(part)
        possible=self.times.intersect(self.ctx.set(self.prefix+f'{{ [t] : t>={k-1} }}'))
        return possible.subtract(good).coalesce()

    def cardinality_at_most(self, times: Obj, bound: int):
        """Exact parameter predicate |times|<=bound. bound is a supplied INTEGER.
        Uses ordered (bound+1)-tuples, not a count from finite sampling.
        """
        import ctypes as C
        if type(bound) is not int or bound<0:raise ValueError('nonnegative integer bound required')
        self.ctx._bind('isl_set_flat_product',[C.c_void_p,C.c_void_p],C.c_void_p)
        product=times
        for _ in range(bound):product=product.op('flat_product',times)
        names=[f'q{i}' for i in range(bound+1)]
        ordered=' and '.join(f'{names[i]}<{names[i+1]}' for i in range(bound)) or 'true'
        region=self.ctx.set(self.prefix+'{ ['+','.join(names)+'] : '+ordered+' }')
        too_many=product.intersect(region).params()
        return self.domain.subtract(too_many).coalesce()
