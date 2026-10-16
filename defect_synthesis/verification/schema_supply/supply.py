"""Exact full-cell flat-trace feasibility and certified unary supply counting.

The cardinality backend accepts only after proving exact interval-stride coverage.
Unsupported unary fibres raise Unsupported, never an infeasibility certificate.
"""
from dataclasses import dataclass
import re
from isl_core import Context
D=((0,1),(1,0),(0,-1),(-1,0))
W=('RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRL'
   'LRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR')
A='LLRRRRLRRLRRRRLLLLRLRRRRLRLL'
B=('RRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLRRRRLRLLLLRRRR'
   'LRRLRRRRLLLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRLL')
PULSE='RLRRRRLRRRRLLLLRLRRL'
LEGAL={(W*2)[i:i+10] for i in range(104)}
class Unsupported(RuntimeError):pass
@dataclass(frozen=True)
class Lin:
    cs: tuple
    def __add__(self,o):
        if isinstance(o,int):o=Lin((o,)+(0,)*(len(self.cs)-1))
        if not isinstance(o,Lin) or len(self.cs)!=len(o.cs):raise ValueError('affine dimension mismatch')
        return Lin(tuple(a+b for a,b in zip(self.cs,o.cs)))
    __radd__=__add__
    def __mul__(self,k):
        if type(k) is not int:raise ValueError('only constant multiplication')
        return Lin(tuple(k*a for a in self.cs))
    __rmul__=__mul__
    def expr(self,params):return '('+'+'.join([str(self.cs[0])]+[f'{v}*{n}' for n,v in zip(params,self.cs[1:]) if v])+')'
    def at(self,params):return self.cs[0]+sum(a*b for a,b in zip(self.cs[1:],params))
def geometry(w,h):
    if set(w)-{'R','L'}:raise ValueError('bad word')
    x=y=0;out=[]
    for ch in w:
        out.append((x,y,int(ch=='L')));h=(h+(1 if ch=='R' else -1))%4;dx,dy=D[h];x+=dx;y+=dy
    return out,(x,y),h
class Schema:
    def __init__(self,params,parts,domain='true',pose=(0,0,0)):
        self.params=tuple(params);self.parts=parts;self.pose=pose
        if len(set(params))!=len(params) or any(not re.fullmatch(r'[a-zA-Z]+',n) or n in {'x','y','t','b','j','s','v','c','d','lo','hi'} for n in params):raise ValueError('invalid/reserved parameter')
        self.header='['+','.join(params)+'] -> '
        self.guard=domain
        for w,k in parts:
            if k is not None:
                if len(k)!=len(params)+1 or any(type(a) is not int for a in k):raise ValueError('bad exponent')
                if not w or geometry(w,0)[2]!=0:raise ValueError('power must restore heading')
                self.guard+=' and '+Lin(tuple(k)).expr(params)+'>=0'
        x=Lin((pose[0],)+(0,)*len(params));y=Lin((pose[1],)+(0,)*len(params));time=Lin((0,)*(len(params)+1));h=pose[2];records=[]
        self.phase_terms=[]
        for word,ks in parts:
            phases,drift,endh=geometry(word,h)
            for i,(dx,dy,bit) in enumerate(phases):
                pos=f'x={(x+dx).expr(params)} and y={(y+dy).expr(params)} and t={(time+i).expr(params)} and b={bit}'
                if ks is not None:
                    count=Lin(tuple(ks)).expr(params)
                    pos=(f'exists (j: 0<=j<{count} and x={(x+dx).expr(params)}+{drift[0]}*j and '
                         f'y={(y+dy).expr(params)}+{drift[1]}*j and t={(time+i).expr(params)}+{len(word)}*j and b={bit})')
                records.append('[x,y] -> [t,b] : ('+self.guard+') and ('+pos+')')
            k=Lin(tuple(ks)) if ks is not None else Lin((1,)+(0,)*len(params))
            x=x+drift[0]*k;y=y+drift[1]*k;time=time+len(word)*k;h=endh
        self.length=time;self.end=(x,y,h)
        self.reads_text=self.header+'{ '+('; '.join(records) or '[x,y] -> [t,b]:false')+' }'
    def instantiate(self,values,cap=1000000):
        s=[];total=0
        for w,ks in self.parts:
            k=1 if ks is None else Lin(tuple(ks)).at(values)
            if k<0:raise ValueError('negative power')
            total+=k*len(w)
            if total>cap:raise ValueError('cap')
            s.append(w*k)
        return ''.join(s)
def compile(schema,ctx):
    H=schema.header;guard=ctx.set(H+'{ : '+schema.guard+' }');R=ctx.map(schema.reads_text)
    later=ctx.map(H+'{ [t,b]->[s,v]:s>t }');equal=ctx.map(H+'{ [t,b]->[s,v]:b=v }')
    bad=R.reverse().apply_range(R).intersect(later).lexmin().intersect(equal).params()
    feasible=guard.subtract(bad).coalesce()
    first=R.lexmin();firstL=first.intersect(ctx.map(H+'{ [x,y]->[t,b]:b=1 }'))
    # Count first-L TIMES, not two-dimensional positions; one first read per cell.
    times=firstL.range().project(3,1,1).intersect_params(feasible).coalesce()
    return {'feasible':feasible,'firstL':firstL.domain().intersect_params(feasible).coalesce(),'times':times,'reads':R}
def unary_count(ctx,H,domain,S,certificate=None,moduli=()):
    """Return exact count graph after proving each disjoint piece is an AP interval."""
    pieces=list(S.unary('make_disjoint').basic_sets())
    refined=[]
    def exact_progression(b):
        stride=b.stride()
        if stride<=0:return None
        bounds=b.lexmin().flat_product(b.lexmax())
        hull=bounds.apply(ctx.map(H+f'{{ [lo,hi]->[j]:lo<=j<=hi and (j-lo)%{stride}=0 }}'))
        return (stride,bounds) if hull.equal(b) else None
    def refine(b,remaining):
        if b.empty():return
        if exact_progression(b) is not None:refined.append(b);return
        if not remaining:raise Unsupported('unary fibre needs further residue splitting')
        q,*rest=remaining
        if type(q) is not int or not 1<=q<=10000:raise Unsupported('invalid/excessive split modulus')
        for r in range(q):
            sub=b.intersect(ctx.set(H+f'{{ [j]:(j-{r})%{q}=0 }}')).coalesce()
            for part in sub.unary('make_disjoint').basic_sets():refine(part,rest)
        if len(refined)>100000:raise Unsupported('count certificate cap')
    for b in pieces:refine(b,list(moduli))
    pieces=refined
    total=ctx.set(H+'{ [c]:c=0 }').intersect_params(domain)
    details=[]
    for b in pieces:
        if b.empty():continue
        stride=b.stride()
        if stride<=0:raise Unsupported('nonpositive stride')
        lo=b.lexmin();hi=b.lexmax();bounds=lo.flat_product(hi)
        hull=bounds.apply(ctx.map(H+f'{{ [lo,hi]->[j]:lo<=j<=hi and (j-lo)%{stride}=0 }}'))
        if not hull.equal(b):raise Unsupported('unary fibre is not covered by one exact progression')
        count=bounds.apply(ctx.map(H+f'{{ [lo,hi]->[c]:{stride}*(c-1)=hi-lo }}'))
        zeros=domain.subtract(b.params())
        count=count.union(ctx.set(H+'{ [c]:c=0 }').intersect_params(zeros))
        total=total.flat_product(count).apply(ctx.map(H+'{ [c,d]->[s]:s=c+d }')).coalesce()
        details.append({'set':str(b),'stride':stride,'count':str(count)})
    if not total.params().equal(domain):raise AssertionError('count graph lost parameters')
    if certificate is not None:certificate.extend(details)
    return total

def scan(hist,w):
    n=0
    for ch in w:
        s=hist+ch;n+=len(s)==10 and s not in LEGAL;hist=s[-9:]
    return hist,n

def defect_graph(schema,ctx,feasible):
    # Lexical computation only; no shortened word is assumed physically feasible.
    zero=Lin((0,)*(len(schema.params)+1));cases=[('true',zero,'')]
    for word,ks in schema.parts:
        new=[]
        for cond,count,hist in cases:
            if ks is None:
                h,n=scan(hist,word);new.append((cond,count+n,h));continue
            k=Lin(tuple(ks));q=(9+len(word)-1)//len(word)
            for r in range(q):
                h,n=scan(hist,word*r);new.append((cond+f' and {k.expr(schema.params)}={r}',count+n,h))
            h,n=scan(hist,word*q);h2,inc=scan(h,word)
            if h2!=h:raise AssertionError('suffix did not stabilize')
            new.append((cond+f' and {k.expr(schema.params)}>={q}',count+n+(k+(-q))*inc,h))
        cases=new
    txt='; '.join('[d]:('+schema.guard+') and ('+cond+') and d='+count.expr(schema.params) for cond,count,_ in cases)
    return ctx.set(schema.header+'{ '+txt+' }').intersect_params(feasible).coalesce()

def joint_relation(schema,ctx,certificate=None):
    c=compile(schema,ctx);supply=unary_count(ctx,schema.header,c['feasible'],c['times'],certificate,sorted({len(w) for w,k in schema.parts if k is not None},reverse=True))
    defects=defect_graph(schema,ctx,c['feasible'])
    c.update(supply=supply,defects=defects,joint=supply.flat_product(defects).coalesce())
    return c

def literal_minimal(word,pose=(0,0,0)):
    x,y,h=pose;previous={};seed=set();black=set()
    for t,ch in enumerate(word):
        bit=ch=='L';p=(x,y)
        if p in previous:
            if previous[p]==bit:return None
        else:
            if bit:seed.add(p);black.add(p)
        if (p in black)!=bit:raise AssertionError('model mismatch')
        black.symmetric_difference_update((p,));previous[p]=bit;h=(h+(1 if ch=='R' else -1))%4;dx,dy=D[h];x+=dx;y+=dy
    return seed,black,(x,y,h),scan('',word)[1]
