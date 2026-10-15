"""Exact critical anisotropic potentials for the literal Langton ant.

Coordinates are integers unless using the square-only half-integral centre.
The potential never discards old black cells. Bounds concern FIRST EXIT only.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache

Point = tuple[int, int]
MOVES = ((0,1),(1,0),(0,-1),(-1,0))
REWARD_SIGNS = (
    ((1,-1),(-1,-1)), # N: white, black
    ((-1,-1),(-1,1)), # E
    ((-1,1),(1,1)),   # S
    ((1,1),(1,-1)),   # W
)

@dataclass(frozen=True)
class State:
    black: frozenset[Point]
    pos: Point = (0,0)
    heading: int = 0
    def __post_init__(self):
        if type(self.heading) is not int or not 0 <= self.heading < 4:
            raise ValueError('heading must be 0=N,1=E,2=S,3=W')
        for p in [self.pos, *self.black]:
            if len(p)!=2 or any(type(v) is not int for v in p):
                raise ValueError('finite integer lattice points required')


def chi(p: Point) -> int:
    return 1 if (p[0]+p[1]) % 2 == 0 else -1


def advance(s: State) -> State:
    h=(s.heading + (-1 if s.pos in s.black else 1))%4
    dx,dy=MOVES[h]
    return State(s.black.symmetric_difference((s.pos,)),
                 (s.pos[0]+dx,s.pos[1]+dy),h)


def sector(s: State) -> int:
    return chi(s.pos) * (1 if s.heading%2==0 else -1)


def head_term(U: Q, V: Q, h: int, a: Q, b: Q) -> Q:
    if h==0: return 2/(b+1)*(U+1/U)*(V-b/V)
    if h==1: return 2/(a+1)*(U-a/U)*(V+1/V)
    if h==2: return 2/(b+1)*(U+1/U)*(1/V-b*V)
    return 2/(a+1)*(1/U-a*U)*(V+1/V)


class Potential:
    def __init__(self,a:Q,b:Q,centre:Point=(0,0)):
        self.a,self.b=Q(a),Q(b)
        if self.a<=1 or self.b<=1 or (self.a-1)*(self.b-1)!=4:
            raise ValueError('require a,b>1 and (a-1)(b-1)=4')
        if any(type(v) is not int for v in centre):
            raise ValueError('integer centre required; use square_value for half centres')
        self.centre=centre

    @lru_cache(None)
    def uv(self,p:Point):
        return self.a**(p[0]-self.centre[0]),self.b**(p[1]-self.centre[1])

    @lru_cache(None)
    def field_coefficient(self,p:Point):
        U,V=self.uv(p)
        return -chi(p)*(U-1/U)*(V-1/V)

    @lru_cache(None)
    def head(self,p:Point,h:int):
        U,V=self.uv(p)
        return head_term(U,V,h,self.a,self.b)

    def __call__(self,s:State):
        return sector(s)*sum((self.field_coefficient(p) for p in s.black),Q(0))+self.head(s.pos,s.heading)

    def increment(self,s:State):
        sx,sy=REWARD_SIGNS[s.heading][s.pos in s.black]
        U,V=self.uv(s.pos)
        return 4*U**sx*V**sy


def square_value(s:State,n:int) -> Q:
    """a=b=3, centred at ((n-1)/2,(n-1)/2), without square roots."""
    if type(n) is not int or n<1: raise ValueError('positive side required')
    c=n-1
    def f(k): return Q(3)**k+Q(3)**(-k)
    def g(k,e):
        return (Q(3)**k-Q(3)**(1-k))/2 if e==1 else (Q(3)**(-k)-Q(3)**(k+1))/2
    def eps(h): return 1 if h%4 in(0,1) else -1
    field=sector(s)*sum((chi(p)*(f(p[0]-p[1])-f(p[0]+p[1]-c)) for p in s.black),Q(0))
    x,y=s.pos
    return field+g(x+y-c,eps(s.heading))+g(x-y,eps(s.heading-1))


def square_range_upper(n:int) -> Q:
    if type(n) is not int or n<1: raise ValueError('positive side required')
    return Q(3)**(1-n)*(3**n-1)**2+4*(Q(3)**(n-1)-Q(3)**(1-n))


def square_exit_bound(n:int) -> int:
    return 4*int(3*square_range_upper(n)//16)+4


def rectangular_exit_bound(n:int,h:int) -> int:
    if type(n) is not int or type(h) is not int or min(n,h)<1:
        raise ValueError('positive integer dimensions required')
    return int(Q(9,2)*(n*h+16)*(4*n+1)**(h//2))+3


def exact_rectangle_bound(n:int,h:int):
    """A sharper input-independent bound, computable with rational arithmetic."""
    if min(n,h)<1: raise ValueError('positive dimensions required')
    p=Potential(Q(n+1,n),Q(4*n+1),(0,(h-1)//2))
    cells=[(x,y) for x in range(n) for y in range(h)]
    field=sum(abs(p.field_coefficient(v)) for v in cells)
    heads=[p.head(v,d) for v in cells for d in range(4)]
    width=field+max(heads)-min(heads)
    delta=4*(1+1/p.b)*p.a**(-(n-1))
    return int(2*width//delta)+3,width,delta
