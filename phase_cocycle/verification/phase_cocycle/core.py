"""Exact separated phase clocks and compact spatial charges.

All-state theorems, including maximality, are proved in phase-cocycle-rigidity.md.
This module evaluates explicit witnesses. It does not decide HIGHWAY or supply a
termination rank. In particular, a modular clock is not an ordered integer clock.
"""
from __future__ import annotations
from functools import lru_cache
from collections.abc import Mapping, Sequence

DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))
Point = tuple[int, int]
Pose = tuple[int, int, int]


def validate_rule(rule: str) -> None:
    if not isinstance(rule, str) or not rule or set(rule) - {'R', 'L'}:
        raise ValueError('a nonempty R/L cyclic rule is required')


def validate_pose(pose: Pose) -> None:
    if len(pose) != 3 or any(type(a) is not int for a in pose) or pose[2] not in range(4):
        raise ValueError('integer (x,y,heading), heading N/E/S/W=0/1/2/3, required')


def canonical(p: Point, sector: int) -> Point:
    x, y = p
    return (x, y) if sector == 0 else (-y, x)


def sector_of(pose: Pose) -> int:
    validate_pose(pose)
    x, y, h = pose
    return (h-x-y) % 2


def maximal_period(rule: str, *, common_field: bool = False) -> int:
    validate_rule(rule)
    n, r = len(rule), rule.count('R')
    return 8*n if not common_field and r % 2 and (n-r) % 2 else 4*n


def coefficients(n: int, right_count: int, p: Point, *, common_field=False):
    """Return a,b,M: per-R/L field increments for the unit-rate clock.

    This count-level function does not expand a huge symbolic rule. The evaluator
    below accepts an explicit finite rule so the actual color prefixes are known.
    """
    if type(n) is not int or type(right_count) is not int or n < 1 or not 0 <= right_count <= n:
        raise ValueError('positive color count and valid R count required')
    x, y = p
    odd = not common_field and right_count % 2 and (n-right_count) % 2
    m = (8 if odd else 4)*n
    indicator = (x % 2)*(y % 2)
    if odd:
        sign = 1 if (x+y) % 2 == 0 else -1
        u = (1-n//2)*indicator-(n//2)*sign*x*y
        a = 4*u
        b = (1-n)*a
    else:
        a = b = 4*indicator
    return a % m, b % m, m


def edge_increments(n: int, r: int, x: int, y: int, *, common_field=False):
    """Positive-x/y gradients of the primary-pose correction, sector zero."""
    a, b, m = coefficients(n, r, (x, y), common_field=common_field)
    d = a-b
    if (x+y) % 2 == 0:  # primary heading N
        east = 1-a
        an, _, _ = coefficients(n, r, (x, y+1), common_field=common_field)
        north = an-1+d
    else:  # primary heading E
        an, bn, _ = coefficients(n, r, (x+1, y), common_field=common_field)
        east = an-1-(an-bn)+d
        north = 1-b
    return east % m, north % m


def periodic_sum(values: Sequence[int], endpoint: int) -> int:
    """Signed sum from 0 to endpoint; works for negative and huge coordinates."""
    if not values or type(endpoint) is not int:
        raise ValueError('nonempty period and integer endpoint required')
    q, r = divmod(endpoint, len(values))
    return q*sum(values)+sum(values[:r])


def primary_potential(n: int, r: int, x: int, y: int, *, common_field=False):
    east = tuple(edge_increments(n, r, i, 0, common_field=common_field)[0] for i in range(4))
    north = tuple(edge_increments(n, r, x, j, common_field=common_field)[1] for j in range(4))
    m = coefficients(n, r, (x, y), common_field=common_field)[2]
    return (periodic_sum(east, x)+periodic_sum(north, y)) % m


def pose_potential_counts(n: int, r: int, pose: Pose, *, common_field=False) -> int:
    x, y, h = pose
    if (h-x-y) % 2:
        raise ValueError('count-level pose must be in sector zero')
    a, b, m = coefficients(n, r, (x, y), common_field=common_field)
    return (primary_potential(n, r, x, y, common_field=common_field)
            + (a-b if h >= 2 else 0)) % m


@lru_cache(maxsize=256)
def prefix_counts(rule: str):
    validate_rule(rule)
    out = [(0, 0)]
    r = l = 0
    for c in rule:
        r += c == 'R'
        l += c == 'L'
        out.append((r, l))
    return tuple(out)


def field_term(rule: str, p: Point, color: int, sector: int, *, common_field=False) -> int:
    if type(color) is not int or not 0 <= color < len(rule):
        raise ValueError('invalid cell color')
    a, b, m = coefficients(len(rule), rule.count('R'), canonical(p, sector), common_field=common_field)
    rc, lc = prefix_counts(rule)[color]
    return (rc*a+lc*b) % m


def pose_term(rule: str, pose: Pose, *, common_field=False) -> int:
    sector = sector_of(pose)
    x, y = canonical(pose[:2], sector)
    h = (pose[2]-sector) % 4
    return pose_potential_counts(len(rule), rule.count('R'), (x, y, h), common_field=common_field)


def clock(rule: str, field: Mapping[Point, int], pose: Pose, *, common_field=False) -> int:
    """Complete finite field; all nonzero cells, including unread debris, enter."""
    validate_rule(rule)
    sector = sector_of(pose)
    value = pose_term(rule, pose, common_field=common_field)
    for p, c in field.items():
        if len(p) != 2 or any(type(z) is not int for z in p):
            raise ValueError('integer cell coordinates required')
        value += field_term(rule, p, c, sector, common_field=common_field)
    return value % maximal_period(rule, common_field=common_field)


def classical_clock(black: set[Point], pose: Pose) -> int:
    """Explicit four-by-four formula for RL, independent of path integration."""
    sector = sector_of(pose)
    x, y = canonical(pose[:2], sector)
    h = (pose[2]-sector) % 4
    if y % 2 == 0:
        u = x % 2
    elif x % 2:
        u = 4*y-2
    else:
        u = 4*x-1
    correction = u + (8*x*y if h >= 2 else 0)
    for point in black:
        a, b = canonical(point, sector)
        correction -= 4*(1 if (a+b) % 2 == 0 else -1)*a*b
    return correction % 16


def directed_face(lower_left: Point, turning: str) -> frozenset[Pose]:
    """The four incoming poses of one R- or L-turn plaquette, sector zero."""
    x, y = lower_left
    if turning not in ('R', 'L') or ((x+y) % 2 != (turning == 'R')):
        raise ValueError('face parity and cycle handedness disagree')
    h = 3 if turning == 'R' else 2
    poses = []
    for _ in range(4):
        poses.append((x, y, h))
        h = (h + (1 if turning == 'R' else -1)) % 4
        dx, dy = DIRECTIONS[h]
        x, y = x+dx, y+dy
    return frozenset(poses)


def compact_charge(rule: str, counted_turn: str, lower_left: Point,
                   field: Mapping[Point, int], pose: Pose) -> int:
    """One GF(2) compact basis element; mixed cyclic rules, sector zero.

    Counting R requires an even number of R colors and an L-face; counting L
    requires an even number of L colors and an R-face. Four pixels and the four
    indicated incoming poses are the entire support of the invariant.
    """
    validate_rule(rule)
    if len(set(rule)) != 2 or counted_turn not in ('R', 'L') or rule.count(counted_turn) % 2:
        raise ValueError('this compact generator is unavailable for the rule')
    if sector_of(pose):
        raise ValueError('compact generator evaluator uses sector zero')
    opposite = 'L' if counted_turn == 'R' else 'R'
    poses = directed_face(lower_left, opposite)
    x, y = lower_left
    channel = int(counted_turn == 'L')
    value = int(pose in poses)
    for point in ((x, y), (x+1, y), (x, y+1), (x+1, y+1)):
        c = field.get(point, 0)
        if type(c) is not int or not 0 <= c < len(rule):
            raise ValueError('invalid cell color')
        value += prefix_counts(rule)[c][channel]
    return value % 2
