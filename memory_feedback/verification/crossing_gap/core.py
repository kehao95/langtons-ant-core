"""Exact finite crossing certificates and integer information bounds.

A certificate implies an eventual translating TRACE, not necessarily P104.
All initial cells are retained. Arithmetic bounds are not trajectory guesses.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

Point = tuple[int, int]
DIR = ((0, 1), (1, 0), (0, -1), (-1, 0))


@dataclass
class State:
    black: set[Point]
    head: Point = (0, 0)
    heading: int = 0

    def clone(self) -> 'State':
        return State(set(self.black), self.head, self.heading)

    def step(self) -> str:
        if self.heading not in range(4):
            raise ValueError('invalid heading')
        p = self.head
        black = p in self.black
        self.heading = (self.heading + (-1 if black else 1)) % 4
        self.black.symmetric_difference_update({p})
        dx, dy = DIR[self.heading]
        self.head = p[0] + dx, p[1] + dy
        return 'L' if black else 'R'


def trace(source: State, steps: int):
    if type(steps) is not int or steps < 0:
        raise ValueError('nonnegative number of steps required')
    state = source.clone()
    positions = [state.head]
    letters = []
    for _ in range(steps):
        letters.append(state.step())
        positions.append(state.head)
    return ''.join(letters), positions, state


def crossing_records(positions: list[Point]):
    records = {}
    for time, (p, q) in enumerate(zip(positions, positions[1:]), 1):
        dx, dy = q[0] - p[0], q[1] - p[1]
        if abs(dx) + abs(dy) != 1:
            raise ValueError('not a nearest-neighbour path')
        if dx:
            cut = min(p[0], q[0])
            records.setdefault(cut, []).append((time, dx, q[1]))
    return records


def signature(record):
    if not record:
        return ()
    low = min(v[2] for v in record)
    return tuple((direction, y - low) for _, direction, y in record)


def duplicate_at_endpoint(source: State, positions: list[Point]):
    """Find two initially-white right-side cuts in ONE actual finite prefix.

    The caller obtains positions from a literal run. verify_pair independently
    recreates that run and checks the full fields and finite no-exit guard.
    """
    frontier = max([source.head[0]] + [p[0] for p in source.black])
    end = positions[-1][0]
    records = crossing_records(positions)
    seen = {}
    for cut in range(frontier, end):
        record = records.get(cut, [])
        sig = signature(record)
        if not sig:
            raise ValueError('missing necessary crossing')
        if sig in seen:
            return seen[sig], cut
        seen[sig] = cut
    return None


def verify_pair(source: State, steps: int, left: int, right: int):
    """Check a self-protecting nested-half-plane pumping certificate."""
    if type(left) is not int or type(right) is not int or not left < right:
        raise ValueError('ordered integer cuts required')
    initial_frontier = max([source.head[0]] + [q[0] for q in source.black])
    if left < initial_frontier:
        raise ValueError('the full initial right half-plane is not white')
    word, ps, _ = trace(source, steps)
    if ps[-1][0] <= right:
        raise ValueError('endpoint not beyond both cuts')
    records = crossing_records(ps)
    a, b = records.get(left, []), records.get(right, [])
    if not a or signature(a) != signature(b):
        raise ValueError('complete crossing histories do not match')
    if [v[1] for v in a] != [1 if j % 2 == 0 else -1 for j in range(len(a))]:
        raise ValueError('invalid crossing orientation')
    if len(a) % 2 != 1:
        raise ValueError('last crossing must enter')
    s, t = a[-1][0], b[-1][0]
    if not s < t:
        raise ValueError('last entries not correctly ordered')
    delta = min(v[2] for v in b) - min(v[2] for v in a)
    drift = right - left, delta
    if not all(p[0] > left for p in ps[s:t + 1]):
        raise ValueError('finite no-exit guard fails')
    xs = source.clone()
    for _ in range(s):
        xs.step()
    xt = xs.clone()
    for _ in range(t - s):
        xt.step()
    if xt.head != (xs.head[0] + drift[0], xs.head[1] + drift[1]) or xt.heading != xs.heading:
        raise ValueError('poses do not translate')
    expected = {(x + drift[0], y + drift[1]) for x, y in xs.black if x > left}
    actual = {q for q in xt.black if q[0] > right}
    if expected != actual:
        raise ValueError('complete inside fields do not translate')
    return {'left': left, 'right': right, 'start': s, 'end': t,
            'period': t - s, 'drift': list(drift), 'word': word[s:t],
            'crossings_per_cut': len(a)}, xs


def periodic_future(source: State, word: str) -> bool:
    """Independent all-epoch phase-ray parity check; no finite-repeat heuristic."""
    if not word or set(word) - {'R', 'L'}:
        raise ValueError('nonempty R/L word required')
    p, h = source.head, source.heading
    ps = []
    for c in word:
        ps.append(p)
        h = (h + (1 if c == 'R' else -1)) % 4
        dx, dy = DIR[h]
        p = p[0] + dx, p[1] + dy
    d = p[0] - source.head[0], p[1] - source.head[1]
    if h != source.heading or d == (0, 0):
        return False
    axis = 0 if d[0] else 1

    def multiple(v):
        if v[axis] % d[axis]:
            return None
        k = v[axis] // d[axis]
        return k if v == (k * d[0], k * d[1]) else None

    for i, q in enumerate(ps):
        thresholds = []
        for j, z in enumerate(ps):
            k = multiple((z[0] - q[0], z[1] - q[1]))
            if k is not None and (k > 0 or k == 0 and j < i):
                thresholds.append(k)
        hits = set()
        for z in source.black:
            k = multiple((z[0] - q[0], z[1] - q[1]))
            if k is not None and k >= 0:
                hits.add(k)
        epochs = {0, *thresholds, *hits, *(k + 1 for k in hits)}
        epochs.add(max(epochs) + 1)
        for k in epochs:
            black = (k in hits) ^ bool(sum(s <= k for s in thresholds) % 2)
            if black != (word[i] == 'L'):
                return False
    return True


def _natural(*values):
    if any(type(v) is not int or v < 0 for v in values):
        raise ValueError('nonnegative integers required')


def geometric_sum(base: int, terms: int) -> int:
    _natural(base, terms)
    if terms == 0:
        return 0
    if base == 1:
        return terms
    if base == 0:
        return 1
    return (base ** terms - 1) // (base - 1)


def signature_count(height: int, pairs: int) -> int:
    """Exact normalized alternating-parity words of odd length 2*pairs+1.

    This is combinatorial capacity, not an assertion of physical realization.
    """
    _natural(height, pairs)
    evens, odds = height // 2 + 1, (height + 1) // 2
    return (height + 1) * (evens * odds) ** pairs - height * ((evens - 1) * odds) ** pairs


def capacity(height: int, max_pairs: int) -> int:
    _natural(height, max_pairs)
    e, o = height // 2 + 1, (height + 1) // 2
    return ((height + 1) * geometric_sum(e * o, max_pairs + 1)
            - height * geometric_sum((e - 1) * o, max_pairs + 1))


def packing_cost(height: int, number: int) -> int | None:
    """Minimum total length of number DISTINCT combinatorial signatures.

    None means no such collection exists. Use exact integers throughout.
    """
    _natural(height, number)
    if not number:
        return 0
    if height == 0:
        return 1 if number == 1 else None
    if height == 1:
        full, extra = divmod(number - 1, 2)
        return 1 + 2 * full * (full + 2) + extra * (2 * full + 3)
    left, cost, j = number, 0, 0
    while left:
        n = min(left, signature_count(height, j))
        cost += (2 * j + 1) * n
        left -= n
        j += 1
    return cost


def visit_bound(width: int) -> int:
    _natural(width)
    return 5 * (4 ** (width // 2 + 1) - 1) // 3


def profile_deadline(radius: int, height: int, multiplicity: int, max_exponent: int = 200000):
    """Exact certificate-or-time bound for a supplied finite read profile."""
    _natural(radius, height, multiplicity, max_exponent)
    if multiplicity == 0:
        raise ValueError('positive multiplicity bound required')
    levels = height + 1
    r = levels * multiplicity - 1
    if r + 1 > max_exponent:
        raise ArithmeticError('symbolic deadline exceeds materialization budget')
    m = capacity(height, r)
    return {'visit_bound': multiplicity, 'column_levels': levels, 'max_pairs': r,
            'signature_capacity': m,
            'deadline': (2 * (radius + m) + 1) * levels * multiplicity}


def width_deadline(radius: int, width: int, max_exponent: int = 200000):
    """Normalize min(|alpha|,|beta|)=1 and use floor of the normal span.

    An arithmetic cap is not a dynamical answer. The preliminary guard also
    avoids constructing an enormous local-visit power before testing the cap.
    """
    _natural(radius, width, max_exponent)
    if width // 2 + 1 > max_exponent.bit_length() + 1:
        raise ArithmeticError('symbolic local-visit bound exceeds arithmetic budget')
    return profile_deadline(radius, width, visit_bound(width), max_exponent)


def normal_span(positions: Iterable[Point], alpha, beta):
    alpha, beta = Fraction(alpha), Fraction(beta)
    if alpha == 0 or beta == 0:
        raise ValueError('both normal components must be nonzero')
    scale = min(abs(alpha), abs(beta))
    values = [(alpha * x + beta * y) / scale for x, y in positions]
    if not values:
        raise ValueError('nonempty trajectory required')
    return max(values) - min(values)


def classify_width(source: State, width: int, alpha=1, beta=-1, max_steps: int | None = None):
    """Total without caps: find a width violation or a permanent translator.

    TRANSLATOR does not assert that the width bound remains true forever, and
    it does not by itself assert that the primitive word is standard P104.
    """
    _natural(width)
    if max_steps is not None:
        _natural(max_steps)
    alpha, beta = Fraction(alpha), Fraction(beta)
    if not alpha or not beta:
        raise ValueError('axis-parallel normals are not supported by this theorem')
    scale = min(abs(alpha), abs(beta))
    alpha, beta = alpha / scale, beta / scale
    low = high = alpha * source.head[0] + beta * source.head[1]
    state = source.clone()
    positions = [state.head]
    extremes = [state.head[0], state.head[0]]
    t = 0
    while True:
        value = alpha * state.head[0] + beta * state.head[1]
        low, high = min(low, value), max(high, value)
        if high - low > width:
            return {'status': 'WIDTH_EXCEEDED', 'time': t, 'span': str(high - low)}
        x = state.head[0]
        side = 1 if x > extremes[1] else -1 if x < extremes[0] else 0
        extremes = [min(extremes[0], x), max(extremes[1], x)]
        if side:
            if side == 1:
                initial, path = source, positions
            else:
                initial = State({(-a, -b) for a, b in source.black},
                                (-source.head[0], -source.head[1]), (source.heading + 2) % 4)
                path = [(-a, -b) for a, b in positions]
            pair = duplicate_at_endpoint(initial, path)
            if pair is not None:
                cert, at = verify_pair(initial, t, *pair)
                if not periodic_future(at, cert['word']):
                    raise AssertionError('independent all-future verification failed')
                return {'status': 'TRANSLATOR', 'time': t, 'halfturn': side == -1,
                        'certificate': cert}
        if max_steps is not None and t >= max_steps:
            return {'status': 'UNKNOWN', 'time': t, 'reason': 'caller step cap'}
        state.step()
        positions.append(state.head)
        t += 1
