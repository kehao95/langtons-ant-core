"""Convex-hull locality and quadratic deadlines for stale-D event prefixes.

All bounds concern prefixes ending at a finite stale event (or a HALT with
an explicitly supplied pre-HALT event budget). They are NOT bounds on the
length of an event-free translating tail or on the total number of events.
Only integer arithmetic is used. General theorems are in PROOF.md.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent / 'baseline'))
from memory_delay import State, geometry, multiple

Point = tuple[int, int]


def _integer(value: int, name: str, lower: int = 0) -> int:
    if type(value) is not int or value < lower:
        raise ValueError(f'{name} must be an integer >= {lower}')
    return value


def cross(o: Point, a: Point, b: Point) -> int:
    return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])


def convex_hull(points: Iterable[Point]) -> tuple[Point, ...]:
    """Counterclockwise vertices, with exact handling of empty/degenerate sets."""
    ps = sorted(set(points))
    if len(ps) < 2:
        return tuple(ps)
    lower, upper = [], []
    for p in ps:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(ps):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return tuple(lower[:-1] + upper[:-1])


def contains(hull: tuple[Point, ...], p: Point) -> bool:
    if not hull:
        return False
    if len(hull) == 1:
        return p == hull[0]
    if len(hull) == 2:
        a, b = hull
        return (cross(a, b, p) == 0 and
                all(min(a[i], b[i]) <= p[i] <= max(a[i], b[i]) for i in (0, 1)))
    return all(cross(a, b, p) >= 0 for a, b in zip(hull, hull[1:]+hull[:1]))


def enlarged_hull(points: Iterable[Point], radius: int) -> tuple[Point, ...]:
    """conv(points) + [-radius,radius]^2, without floating-point tolerances."""
    _integer(radius, 'radius')
    return convex_hull((p[0]+dx, p[1]+dy) for p in convex_hull(points)
                       for dx in (-radius, radius) for dy in (-radius, radius))


def support_diameter(state: State) -> int:
    ps = [state.pos, *state.black]
    return max(max(p[i] for p in ps)-min(p[i] for p in ps) for i in (0, 1))


def macro_halo(D: int) -> int:
    """One finite stale-event macro stays in the full source hull plus this halo."""
    return 5 * (1 << _integer(D, 'D', 1))


def event_deadline(D: int, n: int, diameter: int) -> int:
    """Upper bound on the time JUST AFTER the nth stale event, IF it exists.

    n=0 returns zero. No stopping/nonexistence assertion is inferred when an
    event does occur, or when n is supplied but no future event exists.
    """
    Q = 1 << _integer(D, 'D', 1)
    _integer(n, 'n'); _integer(diameter, 'diameter')
    return Q*n*(diameter+2*Q+10) + 5*Q*Q*n*(n-1)


def halt_deadline(D: int, budget: int, diameter: int,
                  observer_radius: int, observer_states: int) -> int:
    """Strict first-HALT bound, conditional on <=budget earlier stale events."""
    Q = 1 << _integer(D, 'D', 1)
    _integer(budget, 'budget'); _integer(diameter, 'diameter')
    _integer(observer_radius, 'observer_radius')
    _integer(observer_states, 'observer_states', 1)
    return (Q*(budget+1)*(diameter+2*Q+10+5*Q*budget)
            + Q*(observer_radius+observer_states))


def mandatory_event_count(D: int, time: int, diameter: int) -> int:
    """Lower event count before `time`, CONDITIONAL on infinitely many S_D events.

    Exact inverse of the new quadratic deadline; no floating-point logarithms
    or square roots. This does not test whether the infinite-events premise holds.
    """
    _integer(D, 'D', 1); _integer(time, 'time'); _integer(diameter, 'diameter')
    lo, hi = 0, 1
    while event_deadline(D, hi, diameter) <= time:
        lo, hi = hi, hi*2
    while hi-lo > 1:
        mid = (lo+hi)//2
        if event_deadline(D, mid, diameter) <= time:
            lo = mid
        else:
            hi = mid
    return lo


@dataclass(frozen=True)
class PeriodicEnvelope:
    period: int
    drift: Point
    self_epoch: int
    last_old_epoch: int
    cutoff_epoch: int
    old_anchor: Point | None

    @property
    def first_mismatch_strict_deadline(self) -> int:
        return (self.cutoff_epoch+1)*self.period

    @property
    def pre_mismatch_halo(self) -> int:
        return 3*self.period


def periodic_envelope(state: State, word: str) -> PeriodicEnvelope:
    """Geometry of a prescribed heading-restoring nonzero translating word.

    If word^omega has a first physical mismatch, it occurs before the returned
    deadline and its entire preceding read footprint lies in conv(B union {p})
    enlarged by 3*period. The helper itself does NOT assert physical validity.
    The final mismatched physical move requires one additional unit of halo.
    """
    ps, h, d = geometry(state, word)
    if h != state.heading or d == (0, 0):
        raise ValueError('a heading-restoring nonzero translation is required')
    P = len(word)
    self_epoch = 0
    last_old_epoch, old_anchor = -1, None
    for i, p in enumerate(ps):
        for j, q in enumerate(ps):
            k = multiple((q[0]-p[0], q[1]-p[1]), d)
            if k is not None and k >= 0 and (k > 0 or j < i):
                self_epoch = max(self_epoch, k)
        for q in state.black:
            k = multiple((q[0]-p[0], q[1]-p[1]), d)
            if k is not None and k >= 0 and k > last_old_epoch:
                last_old_epoch, old_anchor = k, q
    K = max(0, self_epoch, last_old_epoch+1)
    if self_epoch*max(abs(d[0]), abs(d[1])) > P:
        raise AssertionError('phase-distance bound failed')
    return PeriodicEnvelope(P, d, self_epoch, last_old_epoch, K, old_anchor)


def prefix_extreme_points(state: State, word: str, updates: int,
                          include_terminal: bool = True) -> tuple[Point, ...]:
    """Convex generators of prescribed reads, without expanding huge prefixes.

    For each phase its first and last read generate that finite arithmetic
    segment's hull. These are exact for geometry even before executability is
    separately verified.
    """
    _integer(updates, 'updates')
    ps, h, d = geometry(state, word)
    if h != state.heading or d == (0, 0):
        raise ValueError('a heading-restoring nonzero translation is required')
    P = len(word); out = [state.pos]
    for i, p in enumerate(ps):
        count = 0 if updates <= i else (updates-1-i)//P+1
        if count:
            out.extend((p, (p[0]+(count-1)*d[0], p[1]+(count-1)*d[1])))
    if include_terminal:
        k, i = divmod(updates, P)
        out.append((ps[i][0]+k*d[0], ps[i][1]+k*d[1]))
    return tuple(out)
