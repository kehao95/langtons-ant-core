"""Explicit indexed readout in one passive standard-highway class.

All fields are complete finite sets. The intervention toggles the current cell
once before the ordinary update at a specified time. No head reset is allowed.
A source contains an arbitrary finite binary matrix; it does not generate
unbounded data from a fixed-size initial input.
"""
from __future__ import annotations

DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))
STANDARD = ('LRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLR'
            'RRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLR')
W = STANDARD[-1:] + STANDARD[:-1]
P = frozenset(((0,-3),(0,-2),(0,-1),(1,-2),(2,-2),(2,0),(3,-3),
              (3,0),(4,-3),(4,-1),(5,-2),(5,-1),(6,-1)))
Q = frozenset(((0,2),(0,3),(1,0),(1,4),(1,5),(1,6),(2,0),
              (2,1),(2,2),(2,5),(3,0),(3,3),(3,4)))
CODE = ('RLLR', 'LRRL')
PERIOD_GAP = 3
PHASE = 72


def natural(value, name):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(name+' must be a nonnegative integer')
    return value


def shift(field, offset):
    a,b=offset
    return {(x+a,y+b) for x,y in field}


def matrix(rows):
    rows=tuple(tuple(r) for r in rows)
    if not rows or not rows[0] or any(len(r)!=len(rows[0]) for r in rows):
        raise ValueError('nonempty rectangular matrix required')
    if any(type(b) is not int or b not in (0,1) for row in rows for b in row):
        raise ValueError('entries must be binary integers')
    return rows


def origin(j):
    natural(j,'lane')
    return 8+6*j, -1-6*j


def trigger(j):
    natural(j,'lane')
    return 312*j+72


def tile(bit, consumed=False):
    if type(bit) is not int or bit not in (0,1):
        raise ValueError('binary bit required')
    xs = ((0,2) if bit==0 else (-1,3)) if consumed else ((1,2) if bit==0 else (0,3))
    return {(x,y) for x in xs for y in (0,1)}


def lane(bits, j, consumed=0):
    bits=tuple(bits);natural(consumed,'consumed')
    if consumed>len(bits):raise ValueError('too many consumed tiles')
    x,y=origin(j)
    field=shift(Q,(x,y+2*len(bits)))
    for r,b in enumerate(bits):
        piece=shift(tile(b,r<consumed),(x,y+2*r))
        if field & piece:raise AssertionError('lane source overlap')
        field |= piece
    return field


def source(rows):
    rows=matrix(rows);field=set(P)
    for j,row in enumerate(rows):
        piece=lane(row,j)
        if field & piece:raise AssertionError('distinct lanes overlap')
        field |= piece
    return field


def geometry(word, heading):
    x=y=0;h=heading;reads=[]
    for c in word:
        if c not in 'RL':raise ValueError('invalid turn')
        reads.append((x,y))
        h=(h+(1 if c=='R' else -1))%4
        dx,dy=DIRECTIONS[h];x+=dx;y+=dy
    return reads,(x,y),h


def literal(initial, pose, steps, flip_at=None, cap=None):
    natural(steps,'steps')
    if flip_at is not None:natural(flip_at,'flip_at')
    if cap is not None:
        natural(cap,'cap')
        if steps>cap:raise TimeoutError('UNKNOWN: finite execution budget')
    field=set(initial);x,y,h=pose;dx,dy=DIRECTIONS[h];word=[];reads=[]
    for t in range(steps):
        p=(x,y);reads.append(p)
        if t==flip_at:field.symmetric_difference_update((p,))
        if p in field:
            field.remove(p);dx,dy=-dy,dx;word.append('L')
        else:
            field.add(p);dx,dy=dy,-dx;word.append('R')
        x+=dx;y+=dy
    return field,(x,y,DIRECTIONS.index((dx,dy))),''.join(word),reads


def passive_prefix(length):
    natural(length,'length')
    return (W*((length+103)//104))[:length]


def prescribed(rows,j,tail=0):
    rows=matrix(rows);natural(j,'lane');natural(tail,'tail')
    if j>=len(rows):raise ValueError('lane out of range')
    return passive_prefix(trigger(j))+'L'+''.join(CODE[b] for b in rows[j])+passive_prefix(tail)


def checkpoint(rows,j,r):
    """Complete field just after activation and r selected data tiles."""
    rows=matrix(rows);natural(j,'lane');natural(r,'tile count')
    if j>=len(rows) or r>len(rows[0]):raise ValueError('invalid checkpoint')
    background,_,_,_=literal(P,(0,0,1),trigger(j))
    for a,row in enumerate(rows):
        piece=lane(row,a,r if a==j else 0)
        if background & piece:raise AssertionError('background/source overlap')
        background |= piece
    x,y=origin(j)
    return background,(x,y+2*r,0)


def readout_profile(n,m,horizon):
    natural(n,'n');natural(m,'m');natural(horizon,'horizon')
    if min(n,m)<1:raise ValueError('positive dimensions required')
    return [min(m,max(0,(horizon-trigger(j)+2)//4)) for j in range(n)]


def lower_profile(horizon):
    """Explicit bit lower bound for all one-flip response equivalence classes."""
    natural(horizon,'horizon')
    a=(horizon-70)//4
    if a<1:return {'bits':0,'rows':0,'columns':0}
    n=1+(a-1)//78
    return {'bits':n*a-39*n*(n-1),'rows':n,'columns':a}


def reachable_count(horizon):
    natural(horizon,'horizon')
    return 0 if horizon==0 else horizon*horizon-horizon+1


def reachable_sites(horizon):
    """Exact alternating-axis read light cone, for east initial heading."""
    natural(horizon,'horizon');out=set()
    for t in range(max(0,horizon-4),horizon):
        a,b=t//2,(t+1)//2
        out.update((x,y)for x in range(-a,a+1,2)for y in range(-b,b+1,2))
    return out


def passive_ray_bases():
    """Disjoint rays whose union is the whole infinite passive read footprint."""
    reads,_,_=geometry(W,1);groups={}
    for x,y in reads:
        k=x//2;rep=x-2*k,y+2*k
        groups[rep]=min(k,groups.get(rep,k))
    return sorted((x+2*k,y-2*k)for(x,y),k in groups.items())


def ray_count(horizon,base):
    natural(horizon,'horizon');x,y=base
    residue={(0,0):0,(0,1):1,(1,1):2,(1,0):3}[x%2,y%2]
    t=horizon-1-((horizon-1-residue)%4)
    if t<0:return 0
    a,b=t//2,(t+1)//2
    lo=max(0,(-a-x+1)//2,(y-b+1)//2)
    hi=min((a-x)//2,(b+y)//2)
    return max(0,hi-lo+1)


def passive_count(horizon):
    return sum(ray_count(horizon,b)for b in passive_ray_bases())


def full_control_bits(horizon):
    """Exact log2 quotient size in the fixed passive class, arbitrary toggles."""
    return reachable_count(horizon)-passive_count(horizon)


def controlled(initial,actions):
    field=set(initial);x=y=0;h=1;word=[]
    for u in actions:
        if u not in(0,1):raise ValueError('binary actions required')
        p=x,y
        if u:field.symmetric_difference_update((p,))
        black=p in field;field.symmetric_difference_update((p,))
        h=(h+(-1 if black else 1))%4;dx,dy=DIRECTIONS[h];x+=dx;y+=dy
        word.append('L'if black else'R')
    return ''.join(word)
