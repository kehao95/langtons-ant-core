"""Exact diagonal clock and finite-square escape bounds for Langton's ant.

Literal convention: white turns right, black turns left, flips, then moves.
All calculations use integers or fractions. This is NOT a HIGHWAY decider.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from typing import FrozenSet, Tuple

Point = Tuple[int, int]
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))  # N,E,S,W

@dataclass(frozen=True)
class State:
    black: FrozenSet[Point]
    pos: Point = (0, 0)
    heading: int = 0

    def __post_init__(self):
        if self.heading not in range(4):
            raise ValueError('heading must be 0,1,2,3 (N,E,S,W)')

def chi(p: Point) -> int:
    return 1 if (p[0] + p[1]) % 2 == 0 else -1

def sigma(st: State) -> int:
    return chi(st.pos) * (1 if st.heading % 2 == 0 else -1)

def eps(heading: int) -> int:
    return 1 if heading in (0, 1) else -1

def step(st: State) -> State:
    black = set(st.black)
    occupied = st.pos in black
    if occupied:
        black.remove(st.pos)
    else:
        black.add(st.pos)
    h = (st.heading + (-1 if occupied else 1)) % 4
    dx, dy = DIRS[h]
    return State(frozenset(black), (st.pos[0] + dx, st.pos[1] + dy), h)

def _base(r: Q) -> Q:
    r = Q(r)
    if r <= 3:
        raise ValueError('the strict-clock base must exceed 3')
    return r

def f(s: int, r: Q) -> Q:
    return r**s + r**(-s)

def g(s: int, e: int, r: Q) -> Q:
    a = Q(2, 1) / (r + 1)
    if e == 1:
        return a * (r**s - r**(1-s))
    if e == -1:
        return a * (r**(-s) - r**(s+1))
    raise ValueError('e must be +1 or -1')

def clock(st: State, r: Q = Q(4), center: int = 0) -> Q:
    r = _base(r)
    field = sum((chi(p)*f(p[0]+p[1]-center, r) for p in st.black), Q(0))
    s = sum(st.pos) - center
    return -sigma(st)*field + g(s, eps(st.heading), r)

def expected_delta(st: State, r: Q = Q(4), center: int = 0) -> Q:
    r = _base(r)
    nxt = step(st)
    e, en = eps(st.heading), eps(nxt.heading)
    s = sum(st.pos) - center
    d = (r - 3) / (r + 1)
    big = (5*r + 1) / (r + 1)
    if e == en:
        return d*f(s,r)
    if e == 1:
        return d*r**s + big*r**(-s)
    return big*r**s + d*r**(-s)

def square_escape_bound(n: int, r: Q | None = None) -> int:
    """Upper bound on T=min{t>=0: p_t outside an n-by-n square}.

    The initial pose must be inside the square; all initial colorings are allowed.
    Bound includes the final move out. The physical orbit is not terminated there.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('n must be a positive integer')
    r = _base(Q(3) + Q(3,n) if r is None else r)
    R = n-1
    bracket = r**(-R)*(r**n-1)**2/(r-1)**2 + r**R-r**(-R)
    value = (r+1)/(r-3) * bracket
    return value.numerator // value.denominator + 1

def coarse_square_escape_bound(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('n must be a positive integer')
    return 8*n*3**n + 1


def inverse_step(st: State) -> State:
    """Exact inverse of flip-then-move, with the pre-update state convention."""
    dx, dy = DIRS[st.heading]
    old_pos = (st.pos[0]-dx, st.pos[1]-dy)
    black = set(st.black)
    post_black = old_pos in black
    if post_black:
        black.remove(old_pos)   # The previous update was white -> black.
    else:
        black.add(old_pos)      # The previous update was black -> white.
    old_heading = (st.heading + (-1 if post_black else 1)) % 4
    return State(frozenset(black), old_pos, old_heading)


def forward_time(start: State, target: State) -> int | None:
    """Decide exact complete-state reachability; return t with F^t(start)=target.

    No timeout or search-budget NO answers are used. The exact clock supplies
    a finite upper bound on every possible witness. This does not test whether
    the future TRACE eventually belongs to the standard P104 family.
    """
    if sigma(start) != sigma(target):
        return None
    difference = clock(target)-clock(start)
    if difference < 0:
        return None
    limit_q = Q(5,2)*difference  # Reciprocal of the r=4 minimum increment 2/5.
    limit = limit_q.numerator // limit_q.denominator
    st = start
    for t in range(limit+1):
        if st == target:
            return t
        if t < limit:
            st = step(st)
    return None


def orbit_time(start: State, target: State) -> int | None:
    """Decide bi-infinite exact orbit equivalence and return the signed offset."""
    if sigma(start) != sigma(target):
        return None
    if clock(target) >= clock(start):
        return forward_time(start, target)
    reverse = forward_time(target, start)
    return None if reverse is None else -reverse


@dataclass(frozen=True)
class OrbitNormalForm:
    representative: State
    offset: int  # Original input = F^offset(representative).


def orbit_normal_form(st: State) -> OrbitNormalForm:
    """Unique zero-crossing representative of a complete bi-infinite orbit.

    The representative C satisfies clock(C)>=0>clock(F^-1(C)).
    Termination is guaranteed by the uniform two-sided clock increment.
    """
    current = st
    value = clock(current)
    offset = 0
    if value < 0:
        while value < 0:
            delta = expected_delta(current)
            current = step(current)
            value += delta
            offset -= 1
        return OrbitNormalForm(current, offset)
    while True:
        previous = inverse_step(current)
        previous_value = value-expected_delta(previous)
        if previous_value < 0:
            return OrbitNormalForm(current, offset)
        current, value = previous, previous_value
        offset += 1
