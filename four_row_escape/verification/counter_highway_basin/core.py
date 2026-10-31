"""Complete-field post-counter basin certificates, not a full HC theorem."""
from __future__ import annotations
from collections import Counter
from affine import Aff,Field,ONE,ZERO,toggle,nonnegative,zero_on_epochs
DIR=((0,1),(1,0),(0,-1),(-1,0))
A=(6,5);B=(10,9);C=(6,10,12,17);V=(18,29)
# The exact standard word below is deliberately checked against a literal blank
# witness by the dedicated checker, not trusted from its name.
W=('RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRL'
   'LRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR')
PHASES={W[i:]+W[:i]for i in range(len(W))}


def mirror(cols):return tuple(31-b for b in reversed(cols))
def right(j,k):return A*j+C+V*k

def source(l,r):
    if type(l)is not int or type(r)is not int or min(l,r)<0:raise ValueError('nonnegative integer counters required')
    cols=mirror((5,)+right(0,l))+right(0,r)
    return cols,(2*l+5,3,1)

def after(l,r):
    if r<=l:
        cols=mirror((5,)+right(r,l-r))+B*(r+1)+(10,18)
        return cols,(len(cols),1,1),8*r*r+60*r+16
    cols=mirror((9,)+B*(l+1)+(10,18))+right(l+1,r-l-1)
    return cols,(-1,1,3),8*l*l+68*l+48

def black_field(cols):return {(x,y)for x,b in enumerate(cols)for y in range(5)if (b>>y)&1}

def source_field(mode,d,kmin):
    k=Aff(1,0)
    if mode=='east':
        blocks=[(mirror(V),Aff(0,d)),(mirror(C),ONE),(mirror(A),k),((26,),ONE),
                (B,k+1),((10,18),ONE)]
        pose=(Aff(4,2*d+9),1,1)
    elif mode=='west' and d>=1:
        blocks=[((13,21),ONE),(mirror(B),k+1),((22,),ONE),(A,k+1),(C,ONE),(V,Aff(0,d-1))]
        pose=(Aff(0,-1),1,3)
    else:raise ValueError('unsupported family')
    field=Field(kmin);x=ZERO
    for cols,count in blocks:
        nonnegative(count,kmin)
        if count.a==0:
            for _ in range(count.b):
                for b in cols:
                    for y in range(5):
                        if b>>y&1:field.point(x,y)
                    x=x+1
        else:
            if len(cols)!=2:raise ValueError('only two-column parameter powers are supported')
            for i,b in enumerate(cols):
                for y in range(5):
                    if b>>y&1:field.repeat(x+i,y,2,count)
            x=x+2*count
    if x!=Aff(4,2*d+9):raise AssertionError('width formula')
    return field,pose,x


def geometry(word,heading):
    x=y=0;h=heading;ps=[]
    if not word or set(word)-{'R','L'}:raise ValueError('nonempty LR word required')
    for c in word:
        ps.append((x,y));h=(h+(1 if c=='R'else-1))%4;dx,dy=DIR[h];x+=dx;y+=dy
    return ps,(x,y),h


def ray_thresholds(ps,delta,i):
    dx,dy=delta;axis=0 if dx else 1;den=delta[axis]
    if not den:raise ValueError('zero displacement')
    offsets=[]
    for j,p in enumerate(ps):
        diff=(p[0]-ps[i][0],p[1]-ps[i][1])
        if diff[axis]%den:continue
        n=diff[axis]//den
        if diff!=(n*dx,n*dy):continue
        if n>0 or n==0 and j<i:offsets.append(n)
    return offsets


def guard_point(x,y,width,kmin,side):
    if not 0<=y<5 or side is None:return
    nonnegative(x if side=='left'else width-1-x,kmin)


def verify_schema(record):
    mode,d,kmin=record['mode'],record['d'],record['kmin']
    if type(kmin)is not int or kmin<0:raise ValueError('invalid domain')
    field,(x,y,h),width=source_field(mode,d,kmin)
    # Adding unused V columns changes only this complete half-strip.
    side='left'if mode=='east'and d==2 else 'right'if mode=='west'and d==6 else None
    stats=Counter();time=ZERO;footprint=[]
    for item in record['stages']:
        word=item['word'];count=Aff(item['a'],item['b'])
        ps,delta,eh=geometry(word,h);period=len(word)
        nonnegative(count-1,kmin)
        if item['a']==0:
            if item['b']!=1:raise ValueError('fixed block must have one copy')
            for c in word:
                guard_point(x,y,width,kmin,side)
                stats.update(field.read_constant(x,y,c=='L'));stats['read_obligations']+=1
                footprint.append((x,y))
                field.point(x,y);h=(h+(1 if c=='R'else-1))%4;dx,dy=DIR[h];x=x+dx;y+=dy
            time=time+period
        else:
            if eh!=h or delta[1]!=0 or abs(delta[0])!=2:
                raise ValueError('variable block must restore heading and drift horizontally by two')
            for i,((px,py),c) in enumerate(zip(ps,word)):
                q=x+px;yy=y+py
                guard_point(q,yy,width,kmin,side)
                guard_point(q+delta[0]*(count-1),yy,width,kmin,side)
                es=field.jump_set(q,yy,delta[0])
                for threshold in ray_thresholds(ps,delta,i):toggle(es,Aff(0,threshold))
                if c=='L':toggle(es,ZERO)
                stats.update(zero_on_epochs(es,count,kmin));stats['read_obligations']+=1
                footprint.extend(((q,yy),(q+delta[0]*(count-1),yy)))
            # Append ALL loop writes only after verifying the actual chronology.
            for px,py in ps:field.repeat(x+px,y+py,delta[0],count)
            x=x+delta[0]*count;time=time+period*count
            stats['variable_blocks']+=1
    word=record['tail']
    if len(word)!=104 or word not in PHASES:raise AssertionError('not the inherited standard phase')
    if not record['stages'][-1]['word'] or record['stages'][-1]['word'][-1]==word[-1]:
        raise AssertionError('earliest permanent onset not established')
    tailps,delta,eh=geometry(word,h)
    if eh!=h or abs(delta[0])!=2 or abs(delta[1])!=2:raise AssertionError('bad standard geometry')
    rows={yy for (yy,r),es in field.ends.items()if es}
    for i,((px,py),c) in enumerate(zip(tailps,word)):
        thresholds=ray_thresholds(tailps,delta,i)
        points={0,*thresholds}
        for yy in rows:
            v=yy-y-py
            if v%delta[1]==0 and v//delta[1]>=0:
                n=v//delta[1];points.update((n,n+1))
        points.add(max(points)+1)
        for n in sorted(points):
            q=x+px+n*delta[0];yy=y+py+n*delta[1]
            required=(c=='L') ^ bool(sum(v<=n for v in thresholds)%2)
            stats.update(field.read_constant(q,yy,required));stats['tail_epoch_obligations']+=1
        if side:
            # Extra-column perturbations occupy rows 0..4 only. Check EVERY
            # future ray encounter with those rows, even absent from current field.
            for yy in range(5):
                v=yy-y-py
                if v%delta[1]==0 and v//delta[1]>=0:
                    n=v//delta[1];guard_point(x+px+n*delta[0],yy,width,kmin,side)
    return {'mode':mode,'d':d,'kmin':kmin,'time':time.pair(),
            'head_x':x.pair(),'head_y':y,'heading':h,'drift':list(delta),
            'preserved_extra_side':side,'proof_counts':dict(stats),
            'full_field':field.compact()},field,footprint


SMALL=(
 (17106,2789,1479,2661,5711,2665,2557),
 (1516,1423,1591,6410,6430,6322),
 (1547,1925,1945,1837),
 (1635,2021,2041,1933),
 (1715,2883,3787,3915,3413,3433,3325),
 (1787,3071,3447,4199,4495,4859,6975,7638,7658,7550),
 (1859,4607,4451,4471,4363),
 (1931,3543,3931,4491,4771,4470,4490,4382),
 (2003,3635,4163,6057,6077,5969))


def prediction(l,r):
    """Exact first-exit, post-exit first-P104 delay, and absolute first P104 time.

    Constants are theorem data, checked against nine all-parameter schemata and
    the complete finite complement. This is NOT a generic HC classifier.
    """
    if type(l)is not int or type(r)is not int or min(l,r)<0:
        raise ValueError('nonnegative integer counters required')
    if r<=l:
        exit_time=8*r*r+60*r+16;d=l-r
        if d==0:delay=(11560,940)[r]if r<2 else 40*r+1031
        elif d==1:delay=32*r+883
        else:delay=32*r+799
    else:
        exit_time=8*l*l+68*l+48;d=r-l
        if l<9:delay=SMALL[l][min(d,len(SMALL[l]))-1]
        else:
            a,b=((72,1427),(128,2611),(144,3011),(176,3658),(176,3678),(176,3570))[min(d,6)-1]
            delay=a*l+b
    return exit_time,delay,exit_time+delay


def max_entry_at_minimum(m):
    """Exact maximum over the INFINITE set {(l,r):min(l,r)=m}."""
    if type(m)is not int or m<0:raise ValueError('nonnegative integer minimum required')
    if m>=9:return 8*m*m+244*m+3726
    return max([prediction(m,m)[2],prediction(m+1,m)[2],prediction(m+2,m)[2]]+
               [prediction(m,m+d)[2]for d in range(1,len(SMALL[m])+1)])
