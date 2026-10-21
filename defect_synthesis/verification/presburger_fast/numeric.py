"""Independent integer sweep checker for a supplied compressed witness.

Uses ordinary integer tuples, time inequalities and sorted XOR toggles; no SMT,
ISL, affine circuit, or literal expansion of huge powers. This validates a chosen
parameter assignment, not an all-parameter UNSAT statement.
"""
from __future__ import annotations
import _paths  # Pin and load the unchanged sibling schema syntax.
from math import gcd
from compiler import Power, geometry


def det(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def mul(a,k):return a[0]*k,a[1]*k

def member(point,seg):
    a,d,n=seg
    if n<=0:return False
    diff=sub(point,a)
    if d==(0,0):return point==a
    axis=0 if d[0] else 1
    return diff[axis]%d[axis]==0 and 0<=diff[axis]//d[axis]<n and mul(d,diff[axis]//d[axis])==diff


def intersect(s,r):
    """Indices of s in r as a finite arithmetic progression, without time."""
    a,d,n=s;b,v,m=r
    if n<=0 or m<=0:return None
    if d==(0,0):return (0,0,1) if member(a,r) else None
    delta=sub(b,a)
    if v==(0,0):
        axis=0 if d[0] else 1
        if delta[axis]%d[axis]:return None
        k=delta[axis]//d[axis]
        return (k,k,1) if 0<=k<n and mul(d,k)==delta else None
    den=det(d,v)
    if den:
        kn,jn=det(delta,v),det(delta,d)
        if kn%den or jn%den:return None
        k,j=kn//den,jn//den
        return (k,k,1) if 0<=k<n and 0<=j<m else None
    if det(delta,d):return None
    axis=0 if d[0] else 1;aa,bb,cc=d[axis],v[axis],delta[axis]
    g=gcd(abs(aa),abs(bb))
    if cc%g:return None
    mod=abs(bb)//g
    residue=0 if mod==1 else ((cc//g)*pow(aa//g,-1,mod))%mod
    lo,hi=sorted((cc,cc+bb*(m-1)))
    if aa<0:aa,lo,hi=-aa,-hi,-lo
    lo=max(0,-((-lo)//aa));hi=min(n-1,hi//aa)
    first=lo+(residue-lo)%mod;last=hi-(hi-residue)%mod
    return (first,last,mod) if first<=last else None


def streams(schema,values):
    # Reconstruct coordinates and times independently of stream_qf.records.
    p=tuple(a.evaluate(values) for a in schema.pose);h=schema.heading;t=0;out=[]
    for part in schema.parts:
        word=part.word if isinstance(part,Power) else part
        k=part.exponent.evaluate(values) if isinstance(part,Power) else 1
        if k<0:raise ValueError('negative exponent')
        qs,d,nh=geometry(word,h)
        allowed={(2,2),(2,-2),(-2,2),(-2,-2),(2,0),(-2,0),(0,2),(0,-2),(4,0),(-4,0),(0,4),(0,-4)}
        if isinstance(part,Power) and d not in allowed:raise ValueError('unsupported powered stride')
        for i,(q,_,ch) in enumerate(qs):
            if isinstance(part,Power):seg=((p[0]+q[0],p[1]+q[1]),d,k);period=len(word)
            else:seg=((p[0]+q[0],p[1]+q[1]),(0,0),1);period=0
            out.append((seg,t+i,period,ch=='L'))
        p=p[0]+k*d[0],p[1]+k*d[1];h=nh;t+=k*len(word)
    return out,p,h,t


def previous(current,prior):
    """Intersection restricted by the actual integer timestamps, not block IDs."""
    cs,ct,cp,_=current;rs,rt,rp,_=prior
    hit=intersect(cs,rs)
    if hit is None:return None
    lo,hi,step=hit
    def delta_time(k):
        point=cs[0][0]+k*cs[1][0],cs[0][1]+k*cs[1][1]
        if rs[1]==(0,0):j=0
        else:
            ax=0 if rs[1][0] else 1
            j=(point[ax]-rs[0][ax])//rs[1][ax]
        return rt+rp*j-ct-cp*k
    d0=delta_time(lo)
    if lo==hi:return hit if d0<0 else None
    slope=delta_time(lo+step)-d0
    u0=0;u1=(hi-lo)//step
    if slope==0:
        if d0>=0:return None
    elif slope>0:u1=min(u1,(-1-d0)//slope)
    else:
        # -a*u <= -1-d0  iff u >= ceil((d0+1)/a).
        u0=max(u0,-((-(d0+1))//(-slope)))
    return (lo+u0*step,lo+u1*step,step) if u0<=u1 else None


def verify(schema,source,values):
    rs,p,h,t=streams(schema,values)
    initial=[(tuple(a.evaluate(values) for a in s.anchor),s.stride,s.length.evaluate(values)) for s in source]
    if any(n<0 for _,_,n in initial):raise ValueError('negative source length')
    first=None;checks=0
    for current in rs:
        seg,start,period,bit=current
        if seg[2]==0:continue
        hits=[intersect(seg,r) for r in initial]+[previous(current,r) for r in rs]
        for e in (0,1):
            end=(seg[2]-1-e)//2
            if end<0:continue
            events={0:int(bit)}
            for hit in hits:
                if hit is None:continue
                lo,hi,step=hit
                if step not in (1,2):raise ValueError('outside parity-two closed strides')
                if step==2 and lo%2!=e:continue
                a=max(0,-((-(lo-e))//2));b=min(end,(hi-e)//2)
                if a>b:continue
                events[a]=events.get(a,0)^1;events[b+1]=events.get(b+1,0)^1
            parity=0
            for z in sorted(events):
                if z>end:break
                parity^=events[z];checks+=1
                if parity:
                    time=start+period*(2*z+e)
                    first=time if first is None else min(first,time)
                    break
    return dict(valid=first is None,first_bad=first,post_time=t,post_position=p,post_heading=h,
                checks=checks,streams=len(rs))


def endpoint_bit(schema,source,values,point):
    rs,_,_,_=streams(schema,values)
    initial=[(tuple(a.evaluate(values) for a in s.anchor),s.stride,s.length.evaluate(values)) for s in source]
    return bool(sum(member(point,s) for s in initial+[r[0] for r in rs])%2)


def factor_count(schema, values):
    """Independent compressed lexical check, including the final event flag.

    Explicitly reads a bounded number of copies; the rest add the cyclic
    increment. This checks a numerical witness, never a parameter cutoff.
    """
    from compiler import L10
    history='';count=0;last=False
    def scan(h,word):
        number=0;bad=False
        for letter in word:
            window=h+letter;bad=len(window)==10 and window not in L10
            number+=bad;h=window[-9:]
        return h,number,bad
    for part in schema.parts:
        if isinstance(part,str):
            if part:
                history,inc,last=scan(history,part);count+=inc
            continue
        copies=part.exponent.evaluate(values)
        if copies<0:raise ValueError('negative exponent')
        warm=min(copies,1+(9+len(part.word)-1)//len(part.word))
        if warm:
            history,inc,last=scan(history,part.word*warm);count+=inc
        if copies>warm:
            next_history,inc,last=scan(history,part.word)
            if next_history!=history:raise AssertionError('lexical cycle not stabilized')
            count+=(copies-warm)*inc
    return int(count),bool(last)
