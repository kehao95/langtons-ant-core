"""Exact whole-state random access on the certified two-counter P104 basin.

No finite-future approximation: a field is a finite XOR of finite arithmetic
segments. Big counters/times stay integers; explicit expansion has a guard.
The universal trajectory coverage is imported from counter_highway_basin.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from math import isqrt
from pathlib import Path
import hashlib
import gzip
import json

BASE=Path(__file__).resolve().parents[1]/'counter_highway_basin'
# Set after the unchanged inherited files have been checked at packaging time.
PINS={'witness.json': 'b0165e849a723e9ed77168e2a5cce36ce1acc80f983b0b674720b5bd67124e52'}
DIR=((0,1),(1,0),(0,-1),(-1,0))
A=(6,5);B=(10,9);C=(6,10,12,17);V=(18,29)
P='RLLR';K='RLRLRRRRLLLLRLLRLRLLRLLRLRRLLR';Q='RLRLRRRRLLLLRLLR'
SWAP=str.maketrans('RL','LR')
MAX_TERMS=20000


def natural(*xs):
    if any(type(x)is not int or x<0 for x in xs):
        raise ValueError('nonnegative Python integer counters and time required')


@lru_cache(maxsize=1)
def certificate():
    raw={}
    for name,digest in PINS.items():
        path=BASE/name
        raw[name]=path.read_bytes() if path.exists() else gzip.decompress((BASE/(name+'.gz')).read_bytes())
        if hashlib.sha256(raw[name]).hexdigest()!=digest:
            raise RuntimeError('changed inherited input requires a fresh audit: '+name)
    data=json.loads(raw['witness.json'])
    return data


def prediction(l,r):
    natural(l,r);w=certificate()
    if r<=l:
        t=8*r*r+60*r+16;d=l-r
        delay=w['balanced_exceptions'][r] if d==0 and r<2 else (40*r+1031 if d==0 else 32*r+(883 if d==1 else 799))
    else:
        t=8*l*l+68*l+48;d=r-l
        if l<9:
            row=w['left_exhausted_small_delays'][l];delay=row[min(d,len(row))-1]
        else:
            a,b=((72,1427),(128,2611),(144,3011),(176,3658),(176,3678),(176,3570))[min(d,6)-1]
            delay=a*l+b
    return t,delay,t+delay


@dataclass(frozen=True,order=True)
class Segment:
    x:int; y:int; dx:int; dy:int; n:int
    def point(self,j):return self.x+j*self.dx,self.y+j*self.dy
    def contains(self,p):
        a,b=p[0]-self.x,p[1]-self.y
        if a%self.dx:return False
        j=a//self.dx
        return 0<=j<self.n and b==j*self.dy


class Field:
    """XOR multiset, not a union or a deletion of unqueried old cells."""
    def __init__(self):self.terms=set()
    def add(self,x,y,dx,dy,n):
        if not n:return
        if n<0:raise ValueError('negative segment length')
        if dx==dy==0:
            if not n%2:return
            n=1
        if n==1:dx,dy=2,0
        elif dx<0:x+=dx*(n-1);y+=dy*(n-1);dx=-dx;dy=-dy
        if dx!=2 or dy not in (-2,0,2):raise ValueError('unsupported exact segment geometry')
        s=Segment(x,y,dx,dy,n)
        if s in self.terms:self.terms.remove(s)
        else:self.terms.add(s)
    def toggle(self,p):self.add(*p,2,0,1)
    def xor(self,other):self.terms.symmetric_difference_update(other.terms);return self
    def copy(self):
        out=Field();out.terms=set(self.terms);return out
    def translate(self,dx,dy):
        out=Field()
        for s in self.terms:out.add(s.x+dx,s.y+dy,s.dx,s.dy,s.n)
        return out
    def contains(self,p):return bool(sum(s.contains(p)for s in self.terms)%2)
    def materialize(self,limit=1000000):
        natural(limit)
        if sum(s.n for s in self.terms)>limit:
            raise ValueError('explicit expansion limit; use contains/cardinality/compressed export')
        out=set()
        for s in self.terms:
            for j in range(s.n):
                p=s.point(j)
                if p in out:out.remove(p)
                else:out.add(p)
        return out
    def disjoint_lines(self):
        """Cancel overlaps along each exact parity line, with integer endpoints."""
        groups=defaultdict(set)
        for s in self.terms:
            residue=s.x%2;level=(s.x-residue)//2
            key=(s.dy,residue,s.y-level*s.dy)
            events=groups[key]
            for a in (level,level+s.n):
                if a in events:events.remove(a)
                else:events.add(a)
        answer=[]
        for (dy,x,y),es in sorted(groups.items()):
            bounds=sorted(es)
            if len(bounds)%2:raise AssertionError('nonfinite line')
            for lo,hi in zip(bounds[::2],bounds[1::2]):
                if lo<hi:answer.append(Segment(x+2*lo,y+dy*lo,2,dy,hi-lo))
        return answer
    def cardinality(self):
        """Exact full black mass without expanding even a single long segment.

        Same-line overlaps are canceled first. Distinct nonparallel lines meet
        at at most one cell. At a crossing of m retained segments, replace its
        m contributions by m mod 2. All determinants are exact integers.
        """
        rows=self.disjoint_lines();total=sum(s.n for s in rows);hits=defaultdict(set)
        directions=defaultdict(list)
        for i,a in enumerate(rows):directions[a.dy].append((i,a))
        kinds=sorted(directions)
        for ai,da in enumerate(kinds):
            for db in kinds[:ai]:
                for i,a in directions[da]:
                    for j,b in directions[db]:
                        det=a.dx*b.dy-a.dy*b.dx
                        x,y=b.x-a.x,b.y-a.y
                        na=x*b.dy-y*b.dx;nb=x*a.dy-y*a.dx
                        if na%det or nb%det:continue
                        u,v=na//det,nb//det
                        if 0<=u<a.n and 0<=v<b.n:
                            hits[a.point(u)].update((i,j))
        return total-sum(len(ids)-(len(ids)%2)for ids in hits.values())
    def equal(self,other):return self.copy().xor(other).cardinality()==0
    def as_lists(self):return [[s.x,s.y,s.dx,s.dy,s.n]for s in sorted(self.terms)]


def add_columns(field,x,columns,count=1):
    natural(count);width=len(columns)
    if count==0:return x
    if count!=1 and width!=2:raise ValueError('repeated source blocks must have width two')
    for i,b in enumerate(columns):
        for y in range(5):
            if b>>y&1:field.add(x+i,y,width,0,count)
    return x+width*count


def mirrored_blocks(blocks):
    return [(tuple(31-b for b in reversed(cols)),n)for cols,n in reversed(blocks)]


def columns_field(blocks):
    field=Field();x=0
    for cols,n in blocks:x=add_columns(field,x,cols,n)
    return field,x


def source_field(l,r):
    natural(l,r)
    return columns_field(mirrored_blocks([((5,),1),(C,1),(V,l)])+[(C,1),(V,r)])[0]


def checkpoint(l,r,j):
    if not 0<=j<=min(l,r):raise ValueError('checkpoint outside physical rounds')
    blocks=mirrored_blocks([((5,),1),(A,j),(C,1),(V,l-j)])+[(A,j),(C,1),(V,r-j)]
    return columns_field(blocks)[0],(2*l+5,3,1)


def post_exit(l,r):
    if r<=l:
        blocks=mirrored_blocks([((5,),1),(A,r),(C,1),(V,l-r)])+[(B,r+1),((10,18),1)]
        field,width=columns_field(blocks);return field,(width,1,1)
    blocks=mirrored_blocks([((9,),1),(B,l+1),((10,18),1)])+[(A,l+1),(C,1),(V,r-l-1)]
    field,_=columns_field(blocks);return field,(-1,1,3)


def advance(field,pose,word,count,stats):
    if not count:return pose
    x,y,h=pose;xx=yy=0;hh=h;points=[]
    for c in word:
        points.append((xx,yy));hh=(hh+(1 if c=='R'else-1))%4
        dx,dy=DIR[hh];xx+=dx;yy+=dy
    if count>1 and hh!=h:raise AssertionError('powered word changes heading')
    for px,py in points:field.add(x+px,y+py,xx,yy,count)
    stats['phase_points']+=len(points)
    return x+count*xx,y+count*yy,hh


def prefix(field,pose,stages,t,stats):
    for word,n in stages:
        if not t:break
        steps=min(t,len(word)*n);q,r=divmod(steps,len(word))
        pose=advance(field,pose,word,q,stats)
        pose=advance(field,pose,word[:r],int(r>0),stats)
        t-=steps
    if t:raise AssertionError('finite program shorter than requested time')
    return pose


def counter_state(l,r,t,stats):
    j=min(min(l,r),(isqrt(t//2+49)-7)//2)
    base=8*j*j+56*j
    if base>t:raise AssertionError('invalid integer root')
    field,pose=checkpoint(l,r,j);remaining=t-base
    stats['rounds_skipped']=j
    if r<=l and j==r:stages=[(P,j),(Q,1)]
    else:
        stages=[(P,j),(K,1),(P,j)]
        if j<l:
            left=[('LR',1),(P,j),(K,1),(P,j),('RL',1)]
        else:left=[('LR',1),(P,j),(Q,1)]
        stages += [(w.translate(SWAP),n)for w,n in left]
    pose=prefix(field,pose,stages,remaining,stats)
    return field,pose


@lru_cache(maxsize=64)
def small_recovery(l,r):
    """Only the 59 finite base cases. The bound is independent of query size."""
    if max(l,r)>18 or min(l,r)>8:raise AssertionError('not a bounded exception')
    field,pose=post_exit(l,r);black=field.materialize();_,delay,_=prediction(l,r)
    x,y,h=pose;word=[]
    for _ in range(delay+104):
        p=x,y;c='L'if p in black else 'R';word.append(c)
        if p in black:black.remove(p)
        else:black.add(p)
        h=(h+(1 if c=='R'else-1))%4;dx,dy=DIR[h];x+=dx;y+=dy
    return ''.join(word[:delay]),''.join(word[delay:])


def clip(l,r):
    if r<=l:return min(l,r+2),r
    row=certificate()['left_exhausted_small_delays']
    cap=len(row[l])if l<9 else 6
    return l,min(r,l+cap)


@dataclass
class Result:
    field:Field
    pose:tuple[int,int,int]
    first_exit:int
    first_standard:int
    phase:str
    stats:dict
    def next_turn(self):return 'L'if self.field.contains(self.pose[:2])else 'R'


def state_at(l,r,t,*,protected_toggles=()):
    natural(l,r,t);lc,rc=clip(l,r);shift=2*(l-lc)
    exit_time,delay,tau=prediction(l,r)
    stats={'rounds_skipped':0,'standard_cycles_skipped':0,'phase_points':0,
           'bounded_exception_steps':0}
    if t<exit_time:
        field,pose=counter_state(lc,rc,t,stats);phase='counter'
    else:
        field,pose=post_exit(lc,rc);k=min(lc,rc);d=abs(lc-rc)
        sc=certificate()['all_parameter_schemata']
        name=('east'if rc<=lc else 'west')+'-'+str(d)
        exceptional=(lc==rc and lc<2)or(lc<rc and lc<9)
        if exceptional:
            word,tail=small_recovery(lc,rc)
            stages=[(word,1)];stats['bounded_exception_steps']=len(word)+104
        else:
            record=sc[name]
            stages=[(s['word'],s['a']*k+s['b'])for s in record['stages']];tail=record['tail']
        pose=prefix(field,pose,stages,min(t-exit_time,delay),stats)
        phase='recovery'if t<tau else 'standard'
        if t>=tau:
            n,z=divmod(t-tau,104);stats['standard_cycles_skipped']=n
            pose=advance(field,pose,tail,n,stats)
            pose=advance(field,pose,tail[:z],int(z>0),stats)
    field=field.translate(shift,0);pose=(pose[0]+shift,pose[1],pose[2])
    # This is exactly the whole retained unqueried difference, not a deletion.
    if (lc,rc)!=(l,r):field.xor(source_field(l,r)).xor(source_field(lc,rc).translate(shift,0))
    toggles=set()
    for p in protected_toggles:
        if len(p)!=2 or any(type(z)is not int for z in p):raise ValueError('integer toggle coordinates required')
        p=tuple(p)
        if p in toggles:raise ValueError('duplicate toggle coordinates')
        toggles.add(p)
        left=rc<=lc and lc==rc+2 and p[0]<shift
        cap=len(certificate()['left_exhausted_small_delays'][lc])if lc<9 else 6
        right=lc<rc and rc-lc==cap and p[0]>=2*(lc+rc)+9
        if not 0<=p[1]<5 or not(left or right):raise ValueError('toggle outside the proved protected half-strip')
        field.toggle(p)
    stats['segments']=len(field.terms);stats['protected_toggles']=len(toggles)
    if len(field.terms)>MAX_TERMS+len(toggles):raise AssertionError('universal segment-size bound')
    return Result(field,pose,exit_time,tau,phase,stats)
