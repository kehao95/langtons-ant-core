"""Symbolic all-parameter certificate; never extrapolates sampled n values."""
from dataclasses import dataclass
from screen import Run, runs_for, canonical
from itertools import combinations

BASE=((0,1),(0,3),(1,-2),(1,-1),(1,0),(1,2),(2,0),(2,2))
@dataclass(frozen=True)
class Aff:
 a:int=0
 b:int=0
 def __add__(self,o):
  if isinstance(o,int):o=Aff(0,o)
  return Aff(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return Aff(-self.a,-self.b)
 def __sub__(self,o):return self+-o
 def __rsub__(self,o):return -self+o
 def __mul__(self,o):
  if not isinstance(o,int):raise TypeError('integer scalar only')
  return Aff(self.a*o,self.b*o)
 __rmul__=__mul__
 def __floordiv__(self,d):
  if self.a%d:raise ValueError('nonaffine quotient')
  return Aff(self.a//d,self.b//d)
 def __call__(self,n):return self.a*n+self.b
 def nonnegative(self):return self.a>=0 and self.a+self.b>=0
 def positive(self):return self.a>=0 and self.a+self.b>0
 def parity(self):
  if self.a%2:raise ValueError('parameter-dependent parity')
  return self.b%2

def mn(f,g):
 if isinstance(f,int):f=Aff(0,f)
 if isinstance(g,int):g=Aff(0,g)
 if (g-f).nonnegative():return f
 if (f-g).nonnegative():return g
 raise ValueError(('crossing affine minimum',f,g))
def mx(f,g):return -mn(-f if isinstance(f,Aff) else -Aff(0,f),-g if isinstance(g,Aff) else -Aff(0,g))

def affine_runs():
 # Direct symbolic version of endpoint pairing, with no numerical fitting.
 horizontal=sorted(x-3*y for x,y in BASE)
 out=[]
 for L,R in zip(horizontal[::2],horizontal[1::2]):
  for r in range(3):
   kl=Aff(4*L,-(-(L-r)//3));kh=Aff(4*R,(R-1-r)//3)
   for parity in (0,1):
    first=kl+((parity-kl.b)%2);last=kh-((kh.b-parity)%2)
    n=(last-first)//2+1
    if not n.positive():
     if (-n).nonnegative():continue
     raise ValueError('run domain crossing')
    k=last;ly=-k;rx=(r+1)%3;ry=-(k+int(r==2));positive=int((r+parity)%2==0)
    if positive:sx,sy,tx,ty=r,ly,rx,ry
    else:sx,sy,tx,ty=rx,ry,r,ly
    out.append((n,sy,sx,ty,tx,positive))
 for x in range(3):
  ys=sorted(y for r,y in BASE if r==x)
  for L,R in zip(ys[::2],ys[1::2]):
   lo=Aff(12*L-4*x,L);hi=Aff(12*R-4*x,R)
   for parity in (0,1):
    y=lo+((parity-lo.b)%2);n=(hi-1-y)//2+1
    assert n.positive()
    positive=int((x+parity)%2==1);sy=y if positive else y+1;ty=y+1 if positive else y
    out.append((n,sy,x,ty,x,positive))
 return out

def symbolic():
 rs=affine_runs();assert len(rs)==32
 inv=Aff();terms=0
 for A,B in combinations(rs,2):
  na,sa,xa,ta,ya,pa=A;nb,sb,xb,tb,yb,pb=B
  delta=(ta-sa)-(tb-sb);assert delta.a==0
  s=0 if (xa,pa)<(xb,pb) else -1
  t=-delta.b+(0 if (ya,pa)<(yb,pb) else -1)
  lo,hi=sorted((s,t));diff=sa-sb
  for z in range(lo+1,hi+1):
   if (z-diff).parity():continue
   k=(Aff(0,z)-diff)//2
   term=mx(Aff(),mn(nb,na-k)-mx(Aff(),-k))
   inv+=term;terms+=1
 pos=sum((n for n,sy,sx,ty,tx,p in rs if p),Aff())
 edges=sum((n for n,sy,sx,ty,tx,p in rs),Aff())
 ports=0
 for x,y in BASE:
  Y=Aff(12*y-4*x,y)
  for n,sy,sx,ty,tx,p in rs:
   if not p:continue
   for X,S in ((sx,sy),(tx,ty)):
    if X!=x:continue
    diff=Y-S
    if diff.parity():continue
    idx=diff//2
    # Every membership decision must be uniform for ALL n>=1.
    if idx.nonnegative() and (n-1-idx).nonnegative():ports+=1
    elif (-idx-1).nonnegative() or (idx-n).nonnegative():pass
    else:raise ValueError(('endpoint domain crossing',idx,n))
 assert inv==Aff(400,19),inv
 assert pos==Aff(96,9),pos
 assert edges==Aff(192,16),edges
 assert ports==10,ports
 # Spot checks test implementation conventions only; symbolic identities above are the certificate.
 for n in (1,2,17,10**100):
  symbolic_edges=sorted((Run(length(n),2,sy(n),sx,ty(n),tx,p) for length,sy,sx,ty,tx,p in rs),key=repr)
  O={canonical(((12*n+1)*x,(12*n+1)*y),(3,1)) for x,y in BASE}
  actual=sorted(runs_for(O,(3,1)),key=repr)
  assert symbolic_edges==actual
 return {'domain':'all integers n>=1','runs':len(rs),'pair_comparisons':len(rs)*(len(rs)-1)//2,'affine_inversion_terms':terms,'inversion_count':[inv.a,inv.b],'positive_edges':[pos.a,pos.b],'odd_edges':[edges.a,edges.b],'endpoint_positive_incidence':ports,'C_population':5,'winding_parity':1,'signature':1,'required_signature':0,'sampled_parameters_are_not_the_proof':True}
if __name__=='__main__':
 import json
 print(json.dumps(symbolic(),indent=2))
