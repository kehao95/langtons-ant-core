"""Exact all-period synthesis from a prescribed non-axis wake.

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


@dataclass(frozen=True)
class WakeSpec:
    drift: Point
    representatives: tuple[Point, ...]
    heading: int = 0

    def __post_init__(self) -> None:
        if len(self.drift) != 2 or any(type(x) is not int for x in self.drift):
            raise ValueError('integer drift required')
        if not self.drift[0] or not self.drift[1]:
            raise ValueError('axis-parallel drift is outside this theorem')
        if type(self.heading) is not int or self.heading not in range(4):
            raise ValueError('invalid heading')
        for q in self.representatives:
            if len(q) != 2 or any(type(x) is not int for x in q):
                raise ValueError('integer representatives required')
        keys = [class_key(q, self.drift) for q in self.representatives]
        if len(set(keys)) != len(keys):
            raise ValueError('duplicate translation class')

    def normal(self) -> tuple[Point, tuple[Point, ...], int]:
        for k in range(4):
            d = rot(self.drift, k)
            if d[0] > 0 and d[1] < 0:
                return d, tuple(rot(q, k) for q in self.representatives), (self.heading + k) % 4
        raise AssertionError('non-axis normalization failed')


def coefficients(spec: WakeSpec) -> tuple[tuple[int, int], dict[int, int]]:
    d, reps, h = spec.normal(); k = gcd(*d)
    eta = -d[1] // k, d[0] // k
    sig = 1 if h % 2 == 0 else -1
    A: dict[int, int] = defaultdict(int)
    for q in reps:
        A[eta[0] * q[0] + eta[1] * q[1]] -= sig * chi(q)
    return eta, dict(A)


def integer_clock(black: Iterable[Point], position: Point, heading: int, center: int = 0) -> int:
    """A global integer clock with gain >=1 on every classical update."""
    if heading not in range(4) or type(center) is not int:
        raise ValueError('invalid heading/center')
    sig = chi(position) * (1 if heading % 2 == 0 else -1)
    s = sum(position) - center
    f = 3 ** abs(s) - 1
    eps = 1 if heading in (0, 1) else -1
    correction = f // 2 if eps * s >= 0 else -3 * (f // 2)
    return -sig * sum(chi(q) * (3 ** abs(sum(q) - center) - 1) for q in black) + correction


def integer_clock_bound(spec: WakeSpec) -> dict | None:
    eta, A = coefficients(spec)
    if eta != (1, 1):
        return None
    if not A:
        return {'cap': 0, 'centers': []}
    values = [(c, sum(v * (3 ** abs(t - c) - 1) for t, v in A.items()))
              for c in range(min(A), max(A) + 1)]
    return {'cap': max(0, min(v for c, v in values)), 'centers': values}


def moment_bound(spec: WakeSpec, r: Fraction = Fraction(4)) -> dict:
    """P^2 <= A_plus*A_minus/kappa^2, evaluated with exact rationals."""
    r = Fraction(r)
    if r <= 1:
        raise ValueError('r must exceed one')
    eta, A = coefficients(spec)
    a, b = r ** eta[0], r ** eta[1]
    kappa = 1 - Fraction(2, a + 1) - Fraction(2, b + 1)
    if kappa <= 0:
        raise ValueError('strict-clock parameter required')
    plus = sum((c * r ** t for t, c in A.items()), Fraction())
    minus = sum((c * r ** (-t) for t, c in A.items()), Fraction())
    cap = 0
    if plus > 0 and minus > 0:
        square = plus * minus / kappa ** 2
        cap = isqrt(square.numerator // square.denominator)
    return {'r': str(r), 'kappa': str(kappa), 'plus': str(plus), 'minus': str(minus), 'cap': cap}


def diagonal_bound(spec: WakeSpec) -> dict | None:
    """Wake-driven crossing recurrence, with no assumed strip for the trace."""
    eta, A = coefficients(spec)
    if eta != (1, 1):
        return None
    if not A:
        return {'cap': 0, 'cuts': []}
    lo, hi = min(A), max(A)
    left = {lo - 1: 0}; right = {hi: 0}
    for t in range(lo, hi):
        left[t] = 3 * left[t - 1] + A.get(t, 0)
    for t in range(hi - 1, lo - 1, -1):
        right[t] = 3 * right[t + 1] + A.get(t + 1, 0)
    cuts = [(t, min(left[t], right[t])) for t in range(lo, hi)]
    if any(c < 0 for _, c in cuts):
        return {'cap': 0, 'cuts': cuts, 'reason': 'negative required crossing bound'}
    d, _, h = spec.normal()
    sig = 1 if h % 2 == 0 else -1
    plus = sum(c for t, c in cuts if sig * (1 if t % 2 == 0 else -1) == 1)
    minus = sum(c for t, c in cuts if sig * (1 if t % 2 == 0 else -1) == -1)
    cap = max(0, min(2 * sum(c for _, c in cuts), 4 * plus - 2 * d[0], 4 * minus + 2 * d[0]))
    return {'cap': cap, 'cuts': cuts, 'positive_cut_sum': plus, 'negative_cut_sum': minus}


def period_bound(spec: WakeSpec) -> dict:
    if sum(spec.drift) % 2 or len(spec.representatives) % 4:
        return {'cap': 0, 'reason': 'heading/position/wake parity', 'moments': []}
    moments = [moment_bound(spec, r) for r in (Fraction(4), Fraction(7, 2), Fraction(5), Fraction(6))]
    diagonal = diagonal_bound(spec)
    integer = integer_clock_bound(spec)
    cap = min(x['cap'] for x in moments)
    if diagonal is not None:
        cap = min(cap, diagonal['cap'])
    if integer is not None:
        cap = min(cap, integer['cap'])
    return {'cap': cap, 'moments': moments, 'diagonal': diagonal, 'integer_clock': integer}


def spec_matches(spec: WakeSpec, word: str) -> tuple[frozenset[Point], tuple[Point, ...], Point] | None:
    data = periodic_data(word, spec.heading)
    if data is None or data[2] != spec.drift:
        return None
    if {class_key(q, spec.drift) for q in data[1]} != {class_key(q, spec.drift) for q in spec.representatives}:
        return None
    if not verify_forever(data[0], word, spec.heading):
        raise AssertionError('independent infinite verifier disagrees')
    return data


def synthesize(spec: WakeSpec, *, witness: str | None = None, max_nodes: int | None = None) -> dict:
    """Total without max_nodes, with no user-supplied period cutoff.

    A supplied witness is only a search shortcut and is fully checked.
    NO is returned only after a necessary bound excludes all periods or the
    entire finite depth-bounded tree is exhausted.  No recursion-depth limit.
    """
    bound = period_bound(spec); cap = bound['cap']
    if witness is not None:
        data = spec_matches(spec, witness)
        if data:
            if len(witness) > cap:
                raise AssertionError('valid word exceeds proven period cap')
            return {'status': 'YES', 'word': witness, 'seed': sorted(data[0]), 'bound': bound, 'nodes': 0}
    if cap == 0:
        return {'status': 'NO', 'bound': bound, 'nodes': 0}
    if max_nodes is not None and (type(max_nodes) is not int or max_nodes < 0):
        raise ValueError('invalid resource cap')
    target = {class_key(q, spec.drift) for q in spec.representatives}
    # State includes a chronological last-turn map, not a guessed finite board.
    stack = [('', (0, 0), spec.heading, {})]; nodes = 0
    while stack:
        if max_nodes is not None and nodes >= max_nodes:
            return {'status': 'INCONCLUSIVE', 'bound': bound, 'nodes': nodes}
        word, p, h, last = stack.pop(); nodes += 1
        if word and p == spec.drift and h == spec.heading and word.count('R') - word.count('L') == len(target):
            data = spec_matches(spec, word)
            if data:
                return {'status': 'YES', 'word': word, 'seed': sorted(data[0]), 'bound': bound, 'nodes': nodes}
        if len(word) == cap:
            continue
        remaining = cap - len(word)
        if abs(p[0] - spec.drift[0]) + abs(p[1] - spec.drift[1]) > remaining:
            continue
        choices = ('L' if last[p] == 'R' else 'R',) if p in last else ('R', 'L')
        for c in reversed(choices):
            hh = (h + (1 if c == 'R' else -1)) % 4
            e = MOVES[hh]; pp = p[0] + e[0], p[1] + e[1]
            history = last.copy(); history[p] = c
            stack.append((word + c, pp, hh, history))
    return {'status': 'NO', 'bound': bound, 'nodes': nodes}
