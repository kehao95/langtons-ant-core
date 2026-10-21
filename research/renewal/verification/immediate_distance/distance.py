"""Complete-field Hamming distance to an immediate standard P104 future.

This is NOT distance to the eventual basin HIGHWAY. Unread cells remain in the
input. A small value does not give a bound on the value after a physical macro.
"""
from __future__ import annotations
from functools import lru_cache
from typing import Iterable
from baseline.periodic_verify import STANDARD, reconstruct, multiple

Point = tuple[int, int]
DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))
DRIFTS = ((2, 2), (2, -2), (-2, 2), (-2, -2))
PSTAR = (1, 2)


def point(q: Point) -> Point:
    if not isinstance(q, tuple) or len(q) != 2 or any(type(a) is not int for a in q):
        raise ValueError('a coordinate must be a pair of integers')
    return q


@lru_cache(maxsize=4, typed=True)
def phases(heading: int) -> tuple:
    if type(heading) is not int or heading not in range(4):
        raise ValueError('heading must be an integer in 0..3')
    result = []
    for i in range(104):
        word = STANDARD[i:] + STANDARD[:i]
        seed, geo = reconstruct(word, heading)
        drift = geo['drift']
        sign = 1 if drift[0] > 0 else -1
        rays: dict[tuple[int, int], int] = {}
        for x, y in geo['q']:
            key = (drift[0]*y-drift[1]*x, x % 2)
            if key not in rays or sign*x < rays[key]:
                rays[key] = sign*x
        result.append((frozenset(seed), drift, sign, rays, tuple(geo['q']), word))
    return tuple(result)


def read_member(q: Point, phase: tuple) -> bool:
    _, drift, sign, rays, _, _ = phase
    x, y = q
    key = (drift[0]*y-drift[1]*x, x % 2)
    # An absent key is false, not a comparison with an arbitrary large sentinel.
    return key in rays and sign*x >= rays[key]


def scores(black: Iterable[Point], pos: Point = (0, 0), heading: int = 0) -> list[int]:
    point(pos)
    normalized = {(point(q)[0]-pos[0], q[1]-pos[1]) for q in black}
    return [len(seed)+sum(read_member(q, phase) for q in normalized)
            -2*len(seed & normalized)
            for phase in phases(heading) for seed in [phase[0]]]


def distance(black: Iterable[Point], pos: Point = (0, 0), heading: int = 0) -> int:
    return min(scores(black, pos, heading))


def direct_scores(black: Iterable[Point], pos: Point, heading: int) -> list[int]:
    """Independent direct union-of-rays oracle on the symmetric difference."""
    normalized = {(x-pos[0], y-pos[1]) for x, y in black}
    answer = []
    for seed, drift, _, _, locations, _ in phases(heading):
        count = 0
        for x, y in normalized ^ set(seed):
            for u, v in locations:
                k = multiple((x-u, y-v), drift)
                if k is not None and k >= 0:
                    count += 1
                    break
        answer.append(count)
    return answer


def step(black: set[Point], pos: Point, heading: int) -> tuple[Point, int, str]:
    occupied = pos in black
    black.symmetric_difference_update((pos,))
    heading = (heading + (-1 if occupied else 1)) % 4
    dx, dy = DIRECTIONS[heading]
    return (pos[0]+dx, pos[1]+dy), heading, 'L' if occupied else 'R'


def padding(n: int, start: int = 1000) -> set[Point]:
    if type(n) is not int or n < 0 or type(start) is not int or start < 1000:
        raise ValueError('n >= 0 and start >= 1000 must be integers')
    return {(PSTAR[0]+k*dx, PSTAR[1]+k*dy)
            for dx, dy in DRIFTS for k in range(start, start+n)}


def seed(n: int, start: int = 1000) -> set[Point]:
    clean = phases(1)[0][0]
    return set(clean) | {(0, 0), (1, 1)} | padding(n, start)
