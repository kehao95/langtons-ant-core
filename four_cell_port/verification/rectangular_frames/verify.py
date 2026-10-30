"""Acceptance-only, all-parameter, complete-field verifier.

Input certificates describe finite solid rectangles and affine powered words.
No finite parameter sampling, inferred physical cleaning, or numerical fitting
is used to accept a certificate. ISL/GMP remains in the trusted computing base.
"""
from __future__ import annotations
import argparse,ast,collections,hashlib,json,re,time
from dataclasses import dataclass
from pathlib import Path
from exact_sets import Context,xor

DIR=((0,1),(1,0),(0,-1),(-1,0))
STANDARD='RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR'

def require(condition,message):
    if not condition:raise ValueError(message)

@dataclass(frozen=True)
class Aff:
    c:tuple[int,...]
    def __add__(self,other):
        if type(other) is int:other=Aff((other,)+(0,)*(len(self.c)-1))
        if not isinstance(other,Aff) or len(other.c)!=len(self.c):raise TypeError('Incompatible affine expressions')
        return Aff(tuple(a+b for a,b in zip(self.c,other.c)))
    __radd__=__add__
    def __neg__(self):return Aff(tuple(-x for x in self.c))
    def __sub__(self,other):return self+-other
    def __mul__(self,n):
        if type(n) is not int:raise TypeError('Only fixed integer multiplication is supported')
        return Aff(tuple(n*x for x in self.c))
    __rmul__=__mul__
    def text(self,names):
        require(len(names)+1==len(self.c),'Wrong affine dimension')
        return '('+str(self.c[0])+''.join(f'{c:+d}*{n}' for c,n in zip(self.c[1:],names) if c)+')'
    def constant(self):return not any(self.c[1:])
    def evaluate(self,values):return self.c[0]+sum(a*b for a,b in zip(self.c[1:],values))

def parse(value,names):
    def visit(n):
        if isinstance(n,ast.Constant) and type(n.value) is int:return Aff((n.value,)+(0,)*len(names))
        if isinstance(n,ast.Name) and n.id in names:return Aff((0,)+tuple(int(x==n.id) for x in names))
        if isinstance(n,ast.UnaryOp):
            if isinstance(n.op,ast.USub):return -visit(n.operand)
            if isinstance(n.op,ast.UAdd):return visit(n.operand)
        if isinstance(n,ast.BinOp):
            a,b=visit(n.left),visit(n.right)
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):
                if a.constant():return b*a.c[0]
                if b.constant():return a*b.c[0]
        raise ValueError('Not an integer affine expression: '+str(value))
    return visit(ast.parse(str(value),mode='eval').body)

def trace(word,h):
    require(isinstance(word,str) and word and set(word)<=set('RL'),'Invalid turn word')
    x=y=0;out=[]
    for i,c in enumerate(word):
        out.append((x,y,c,i));h=(h+(1 if c=='R' else -1))%4
        dx,dy=DIR[h];x+=dx;y+=dy
    return out,(x,y),h

def scale(q,d):
    x,y=q
    if d[0]:
        if x%d[0]:return None
        n=x//d[0];return n if y==n*d[1] else None
    if x or not d[1] or y%d[1]:return None
    return y//d[1]

class Checker:
    def __init__(self,cert,frame_guard=True):
        self.cert=cert;self.names=cert['parameters'];self.guard=frame_guard
        require(len(STANDARD)==104 and all(STANDARD!=STANDARD[s:]+STANDARD[:s] for s in range(1,104)),'Invalid standard reference')
        require(len(cert['tail'])==104 and cert['tail'] in STANDARD*2,'Nonstandard tail')
        require(len(set(self.names))==len(self.names) and all(isinstance(x,str) and re.fullmatch('[A-Za-z][A-Za-z0-9_]*',x) and x not in ('x','y','k','r') for x in self.names),'Invalid parameter names')
        self.ctx=Context();self.header='['+','.join(self.names)+'] -> '
        self.P=self.ctx.set(self.header+'{ : '+cert['domain']+' }')
        require(not self.P.empty(),'Empty domain')
        self.x=parse(cert['head'][0],self.names);self.y=parse(cert['head'][1],self.names);self.h=cert['head'][2]
        require(type(self.h) is int and self.h in range(4),'Invalid heading')
        self.elapsed=parse(0,self.names);self.checks=0;self.geometry_checks=0
        self.rect=[parse(v,self.names) for v in cert['rect']]
        r=[v.text(self.names) for v in self.rect]
        require(self.ctx.set(self.header+f'{{ : {r[0]}>{r[1]} or {r[2]}>{r[3]} }}').intersect(self.P).empty(),'Empty rectangle')
        self.B=self.ctx.set(self.header+f'{{ [x,y]:{r[0]}<=x<={r[1]} and {r[2]}<=y<={r[3]} }}').intersect_params(self.P)
        self.interior=self.ctx.set(self.header+f'{{ [x,y]:{r[0]}+4<=x<={r[1]}-4 and {r[2]}+4<=y<={r[3]}-4 }}').intersect_params(self.P)
    def points(self,points):
        xs,ys=self.x.text(self.names),self.y.text(self.names)
        clauses=[f'[x,y]:x={xs}+({x}) and y={ys}+({y})' for x,y in sorted(points)]
        return self.ctx.set(self.header+'{ '+(';'.join(clauses) if clauses else '[x,y]:false')+' }').intersect_params(self.P)
    def verify_fixed(self,word):
        ph,d,h=trace(word,self.h);first={};last={};odd=set()
        for x,y,c,i in ph:
            q=x,y;require(q not in last or last[q]!=c,'Internal repeated colour')
            first.setdefault(q,c);last[q]=c
            if q in odd:odd.remove(q)
            else:odd.add(q)
        black={q for q,c in first.items() if c=='L'};white=set(first)-black
        require(self.points(black).subtract(self.B).union(self.points(white).intersect(self.B)).empty(),'Fixed-block read mismatch')
        self.checks+=len(first)
        if self.guard:
            require(self.points(first).intersect(self.interior).empty(),'Fixed block reads deep interior')
            self.geometry_checks+=len(first)
        self.B=xor(self.B,self.points(odd)).coalesce()
        self.x+=d[0];self.y+=d[1];self.h=h;self.elapsed+=len(word)
    def verify_repeat(self,word,count,tail=False):
        ph,d,h=trace(word,self.h)
        require(h==self.h and d!=(0,0),'Repeated block does not translate with restored heading')
        co=None if tail else parse(count,self.names)
        if co is not None:require(self.ctx.set(self.header+'{ : '+co.text(self.names)+'<0 }').intersect(self.P).empty(),'Negative exponent')
        con='k>=0'+('' if tail else ' and k<'+co.text(self.names))
        dom=self.ctx.set(self.header+'{ [k]:'+con+' }').intersect_params(self.P)
        xs,ys=self.x.text(self.names),self.y.text(self.names)
        for qx,qy,c,i in ph:
            query=self.ctx.map(self.header+f'{{ [k]->[x,y]:{con} and x={xs}+({qx})+{d[0]}*k and y={ys}+({qy})+{d[1]}*k }}').intersect_params(self.P)
            actual=query.intersect_range(self.B).domain();expected=dom if c=='L' else dom.subtract(dom)
            parity=collections.Counter()
            for rx,ry,rc,j in ph:
                s=scale((rx-qx,ry-qy),d)
                if s is not None and (s>0 or s==0 and j<i):parity[s]^=1
            for s,bit in parity.items():
                if bit:expected=xor(expected,dom.intersect(self.ctx.set(self.header+f'{{ [k]:k>={s} }}')))
            require(xor(actual,expected).empty(),f'Repeated/tail read mismatch at phase {i}')
            self.checks+=1
            if self.guard:
                require(query.intersect_range(self.interior).empty(),f'Repeated/tail block reads interior at phase {i}')
                self.geometry_checks+=1
        if not tail:
            odd=set()
            for x,y,c,i in ph:
                q=x,y
                if q in odd:odd.remove(q)
                else:odd.add(q)
            for x,y in sorted(odd):
                writes=self.ctx.set(self.header+f'{{ [x,y]:exists(k: {con} and x={xs}+({x})+{d[0]}*k and y={ys}+({y})+{d[1]}*k) }}').intersect_params(self.P)
                self.B=xor(self.B,writes)
            self.B=self.B.coalesce();self.x+=co*d[0];self.y+=co*d[1];self.elapsed+=co*len(word)
    def run(self,progress=False):
        for j,spec in enumerate(self.cert['blocks']):
            co=parse(spec['repeat'],self.names)
            if co.constant() and co.c[0]==1:self.verify_fixed(spec['word'])
            else:self.verify_repeat(spec['word'],spec['repeat'])
            if progress:print(json.dumps({'block':j,'read_checks':self.checks}),flush=True)
        self.verify_repeat(self.cert['tail'],None,True)
        last=self.cert['blocks'][-1];suffix=None
        if parse(last['repeat'],self.names)==parse(1,self.names):
            suffix=0
            for c in reversed(last['word']):
                if c!=self.cert['tail'][(-suffix-1)%104]:break
                suffix+=1
            if suffix==len(last['word']):suffix=None
        require(suffix is not None,'No finite preceding-letter witness for first entrance')
        return {'accepted':True,'name':self.cert['name'],'blocks':len(self.cert['blocks']),
                'read_checks':self.checks,'geometry_checks':self.geometry_checks,'deep_interior_never_read':self.guard,
                'tail_boundary':self.elapsed.text(self.names),'first_entrance':(self.elapsed-suffix).text(self.names),
                'matching_suffix':suffix,'tail_pose':[self.x.text(self.names),self.y.text(self.names),self.h],
                'drift':trace(self.cert['tail'],self.h)[1],
                'certificate_sha256':hashlib.sha256(json.dumps(self.cert,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                'isl_version':self.ctx.version}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('certificate');parser.add_argument('--no-frame-guard',action='store_true');parser.add_argument('--progress',action='store_true')
    args=parser.parse_args();data=json.loads(Path(args.certificate).read_text())
    result=Checker(data,not args.no_frame_guard).run(args.progress)
    print(json.dumps(result,sort_keys=True),flush=True)
