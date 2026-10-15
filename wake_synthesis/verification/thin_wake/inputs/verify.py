"""Inherited supplied-word criterion and separate full-field verifier.
Copied from wake_synthesis/wake.py (original Git blob 7c45915e435a0cd4807b6257229aaf8ef5f206d0).
Not a new realization criterion.

Exact all-period synthesis from a prescribed non-axis wake.

White=R, black=L, flip then move.  Headings N,E,S,W=0,1,2,3.
The generic finite-word realizability criterion is prior work, not a new claim.
New clock bounds make the period-unknown search finite.  Resource caps return
INCONCLUSIVE.  An axis-parallel drift is unsupported, NOT a negative answer.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import gcd, isqrt
from typing import Iterable

Point = tuple[int, int]
MOVES: tuple[Point, ...] = ((0, 1), (1, 0), (0, -1), (-1, 0))
STANDARD = 'LRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLR'


def chi(q: Point) -> int:
    return 1 if (q[0] + q[1]) % 2 == 0 else -1


def rot(q: Point, n: int) -> Point:
    x, y = q
    for _ in range(n % 4):
        x, y = y, -x
    return x, y


def class_key(q: Point, d: Point) -> tuple[int, int]:
    """Full Z*d quotient, not the quotient by the primitive drift."""
    x, y = q; a, b = d
    if a:
        return b * x - a * y, x % abs(a)
    if b:
        return x, y % abs(b)
    raise ValueError('zero drift')


def plan(word: str, heading: int = 0) -> tuple[list[Point], list[int], Point]:
    if not word or set(word) - {'R', 'L'} or heading not in range(4):
        raise ValueError('invalid word or heading')
    p = (0, 0); h = heading; pts = []; hs = []
    for c in word:
        pts.append(p); hs.append(h)
        h = (h + (1 if c == 'R' else -1)) % 4
        e = MOVES[h]; p = p[0] + e[0], p[1] + e[1]
    if h != heading or p == (0, 0):
        raise ValueError('word does not give a nonzero heading-reset translator')
    return pts, hs, p


def periodic_data(word: str, heading: int = 0) -> tuple[frozenset[Point], tuple[Point, ...], Point] | None:
    """Known stabilized visit-order test and explicit finite seed."""
    try:
        pts, _, d = plan(word, heading)
    except ValueError:
        return None
    P = len(word); groups = defaultdict(list)
    for i, q in enumerate(pts):
        level = q[0] // d[0] if d[0] else q[1] // d[1]
        groups[class_key(q, d)].append((i - P * level, i, level, q))
    seed: set[Point] = set(); wake = []
    for values in groups.values():
        vs = sorted(values)
        if any(word[v[1]] != ('R' if j % 2 == 0 else 'L') for j, v in enumerate(vs)):
            return None
        if len(vs) % 2:
            wake.append(vs[0][3])
        _, _, a0, q0 = vs[0]
        for n in range(min(v[2] for v in vs), max(v[2] for v in vs)):
            if sum(v[2] > n for v in vs) % 2:
                seed.add((q0[0] + (n - a0) * d[0], q0[1] + (n - a0) * d[1]))
    return frozenset(seed), tuple(sorted(wake)), d


def integer_multiple(q: Point, d: Point) -> int | None:
    n = None
    for a, b in zip(q, d):
        if b:
            if a % b:
                return None
            k = a // b
            if n is not None and n != k:
                return None
            n = k
        elif a:
            return None
    return n


def verify_forever(seed: Iterable[Point], word: str, heading: int = 0) -> bool:
    """Independent epoch-breakpoint parity expression, keeps the full seed."""
    try:
        pts, _, d = plan(word, heading)
    except ValueError:
        return False
    B = set(seed)
    for i, q in enumerate(pts):
        hits = set(); changes = []
        for z in B:
            k = integer_multiple((z[0] - q[0], z[1] - q[1]), d)
            if k is not None and k >= 0:
                hits.add(k)
        for j, z in enumerate(pts):
            k = integer_multiple((z[0] - q[0], z[1] - q[1]), d)
            if k is not None and (k > 0 or (k == 0 and j < i)):
                changes.append(k)
        for k in {0, *hits, *(k + 1 for k in hits), *changes}:
            actual = ((k in hits) + sum(s <= k for s in changes)) % 2
            if actual != (word[i] == 'L'):
                return False
    return True


