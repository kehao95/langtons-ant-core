"""Fixed-region filtered stale-read decisions; literal complete-field LR dynamics.

The new result is in proof/results/remote-stale-feedback.md. The suffix predictor
and supplied-period parity criterion are existing results, reimplemented here to
keep this research check isolated from shared trusted modules. No timeout is NO;
NO means no stale-D event outside the supplied FIXED finite set, not NO-HIGHWAY.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from typing import Iterable

Point = tuple[int, int]
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def point_ok(p: Point) -> bool:
    return isinstance(p, tuple) and len(p) == 2 and all(type(x) is int for x in p)


@dataclass(frozen=True)
class State:
    black: frozenset[Point]
    pos: Point = (0, 0)
    heading: int = 0

    def __post_init__(self):
        if not isinstance(self.black, frozenset):
            raise ValueError('black must be a complete frozenset')
        if not point_ok(self.pos) or any(not point_ok(p) for p in self.black):
            raise ValueError('integer coordinate pairs required')
        if type(self.heading) is not int or self.heading not in range(4):
            raise ValueError('heading must be 0,1,2,3')


def _state(black: frozenset[Point], pos: Point, heading: int) -> State:
    """Internal construction from already validated exact arithmetic only."""
    result = object.__new__(State)
    object.__setattr__(result, 'black', black)
    object.__setattr__(result, 'pos', pos)
    object.__setattr__(result, 'heading', heading)
    return result


def check_D(D: int) -> None:
    if type(D) is not int or D < 1:
        raise ValueError('D must be a positive integer')


def cap_ok(cap: int | None) -> None:
    if cap is not None and (type(cap) is not int or cap < 0):
        raise ValueError('resource cap must be nonnegative or None')


def norm(p: Point) -> int:
    return max(abs(p[0]), abs(p[1]))


def sub(p: Point, q: Point) -> Point:
    return p[0]-q[0], p[1]-q[1]


def step(x: State) -> tuple[State, str]:
    letter = 'L' if x.pos in x.black else 'R'
    h = (x.heading + (-1 if letter == 'L' else 1)) % 4
    v = DIRS[h]
    return _state(x.black.symmetric_difference((x.pos,)),
                 (x.pos[0]+v[0], x.pos[1]+v[1]), h), letter


def inverse(x: State) -> tuple[State, str]:
    v = DIRS[x.heading]
    q = x.pos[0]-v[0], x.pos[1]-v[1]
    letter = 'R' if q in x.black else 'L'
    h = (x.heading + (-1 if letter == 'R' else 1)) % 4
    return _state(x.black.symmetric_difference((q,)), q, h), letter


def replay(x: State, n: int) -> tuple[State, str, list[Point]]:
    if type(n) is not int or n < 0:
        raise ValueError('nonnegative replay length required')
    b, p, h = set(x.black), x.pos, x.heading
    positions, letters = [p], []
    for _ in range(n):
        black = p in b
        letters.append('L' if black else 'R')
        b.symmetric_difference_update((p,))
        h = (h + (-1 if black else 1)) % 4
        v = DIRS[h]
        p = p[0]+v[0], p[1]+v[1]
        positions.append(p)
    return _state(frozenset(b), p, h), ''.join(letters), positions


def prior_suffix(x: State, D: int) -> str:
    check_D(D)
    chars = []
    for _ in range(D):
        x, letter = inverse(x)
        chars.append(letter)
    return ''.join(reversed(chars))


def geometry(p: Point, h: int, word: str) -> tuple[list[Point], int, Point]:
    if not word or set(word)-{'R', 'L'}:
        raise ValueError('nonempty R/L word required')
    start, points = p, []
    for letter in word:
        points.append(p)
        h = (h + (1 if letter == 'R' else -1)) % 4
        v = DIRS[h]
        p = p[0]+v[0], p[1]+v[1]
    return points, h, sub(p, start)


@lru_cache(maxsize=100000)
def predict(word: str) -> str:
    points, _, drift = geometry((0, 0), 0, word)
    for i in range(len(word)-1, -1, -1):
        if points[i] == drift:
            return 'L' if word[i] == 'R' else 'R'
    return 'R'


def stale(x: State, D: int) -> bool:
    check_D(D)
    return x.pos in x.black and predict(prior_suffix(x, D)) == 'R'


def multiple(v: Point, d: Point) -> int | None:
    if d == (0, 0):
        raise ValueError('nonzero drift required')
    a = 0 if d[0] else 1
    if v[a] % d[a]:
        return None
    k = v[a] // d[a]
    return k if (k*d[0], k*d[1]) == v else None


def period_check(x: State, word: str) -> dict:
    """Complete-field all-future breakpoint parity; not finite extrapolation."""
    points, h, d = geometry(x.pos, x.heading, word)
    if h != x.heading or d == (0, 0):
        return {'valid': False, 'geometric_failure': True}
    P, first, checks = len(word), None, 0
    for i, p in enumerate(points):
        thresholds = []
        for j, q in enumerate(points):
            k = multiple(sub(q, p), d)
            if k is not None and (k > 0 or (k == 0 and j < i)):
                thresholds.append(k)
        hits = set()
        for q in x.black:
            k = multiple(sub(q, p), d)
            if k is not None and k >= 0:
                hits.add(k)
        breaks = {0, *thresholds, *hits, *(k+1 for k in hits)}
        for k in sorted(breaks):
            bit = (int(k in hits) + sum(a <= k for a in thresholds)) % 2
            checks += 1
            if bit != int(word[i] == 'L'):
                t = k*P+i
                first = t if first is None else min(first, t)
    return {'valid': first is None, 'first_bad': first,
            'period': P, 'drift': list(d), 'checks': checks}


def first_event(start: State, D: int, max_suffix_states: int | None = None) -> dict:
    """Existing next-S_D theorem, with a new isolated implementation.

    EVENT can be arbitrarily far in ordinary time. Its finite lasso/arithmetic
    witness uses the entire initial field. FREE certifies no future S_D.
    """
    check_D(D)
    cap_ok(max_suffix_states)
    initial = prior_suffix(start, D)
    word, seen, letters, here = initial, {}, [], start
    while word not in seen:
        if max_suffix_states is not None and len(seen) >= max_suffix_states:
            return {'kind': 'INCONCLUSIVE', 'reason': 'suffix cap'}
        actual = 'L' if here.pos in here.black else 'R'
        if actual != predict(word):
            if actual != 'L' or predict(word) != 'R':
                raise AssertionError('invalid physical suffix mismatch')
            return {'kind': 'EVENT', 'time': len(letters), 'point': list(here.pos),
                    'prefix': ''.join(letters), 'literal': True}
        seen[word] = len(letters)
        here, ch = step(here)
        letters.append(ch)
        word = word[1:]+ch
    j = len(letters)
    cycle = ''.join(letters[seen[word]:])
    prefix = ''.join(letters)
    points, h, d = geometry(here.pos, here.heading, cycle)
    rotation = (h-here.heading) % 4
    if rotation or d == (0, 0):
        multiplier = 1 if rotation == 0 else (2 if rotation == 2 else 4)
        block = cycle*multiplier
        for k in range(2*len(block)):
            actual = 'L' if here.pos in here.black else 'R'
            if actual != block[k % len(block)]:
                if actual != 'L' or block[k % len(block)] != 'R':
                    raise AssertionError('invalid closed-plan mismatch')
                return {'kind': 'EVENT', 'time': j+k, 'point': list(here.pos),
                        'prefix': prefix, 'cycle': cycle, 'closed': True}
            here, _ = step(here)
        raise AssertionError('impossible complete-state recurrence')
    witness = period_check(here, cycle)
    if witness['valid']:
        return {'kind': 'FREE', 'entry': j, 'prefix': prefix,
                'cycle': cycle, 'certificate': witness}
    k, i = divmod(witness['first_bad'], len(cycle))
    p = points[i]
    return {'kind': 'EVENT', 'time': j+witness['first_bad'],
            'point': [p[0]+k*d[0], p[1]+k*d[1]],
            'prefix': prefix, 'cycle': cycle, 'certificate': witness}


def in_segment_halo(z: Point, a: Point, b: Point, halo: int) -> bool:
    """Exact rational feasibility of z in [a,b]+[-halo,halo]^2."""
    if type(halo) is not int or halo < 0:
        raise ValueError('nonnegative integer halo required')
    lo, hi = Fraction(0), Fraction(1)
    for i in range(2):
        d, u = b[i]-a[i], z[i]-a[i]
        if d == 0:
            if abs(u) > halo:
                return False
        else:
            c, e = sorted((Fraction(u-halo, d), Fraction(u+halo, d)))
            lo, hi = max(lo, c), min(hi, e)
    return lo <= hi


def escape_bound(n: int) -> int:
    """Retained conservative all-colouring square first-exit bound."""
    if type(n) is not int or n < 1:
        raise ValueError('positive square side required')
    return 8*n*3**n+1


def guard_side(K: Iterable[Point], D: int) -> int:
    check_D(D)
    points = list(K)
    if not points or any(not point_ok(p) for p in points):
        raise ValueError('nonempty finite set of integer pairs required')
    diameter = max(max(p[i] for p in points)-min(p[i] for p in points)
                   for i in range(2))
    return diameter+2*(3*(1 << D)+2)+1


def external_count_lower(total: int, burst_bound: int) -> int:
    if type(total) is not int or total < 0 or type(burst_bound) is not int or burst_bound < 0:
        raise ValueError('nonnegative integer counts required')
    return total//(burst_bound+1)


def event_deadline(D: int, n: int, W: int) -> int:
    check_D(D)
    if any(type(a) is not int or a < 0 for a in (n, W)):
        raise ValueError('nonnegative n,W required')
    Q = 1 << D
    return Q*n*(W+2*Q+10)+5*Q*Q*n*(n-1)


def density_index(D: int, W: int, time: int) -> int:
    """Invert the retained conditional quadratic deadline, exactly."""
    check_D(D)
    if any(type(a) is not int or a < 0 for a in (W, time)):
        raise ValueError('nonnegative W,time required')
    lo, hi = 0, 1
    while event_deadline(D, hi, W) <= time:
        lo, hi = hi, 2*hi
    while hi-lo > 1:
        mid = (lo+hi)//2
        if event_deadline(D, mid, W) <= time:
            lo = mid
        else:
            hi = mid
    return lo


def external_event_deadline(D: int, n: int, augmented_width: int, burst: int) -> int:
    """Conditional post-nth-EXTERNAL-event bound; burst is E(ell(K,D)).

    Supply the mathematically valid burst bound; an arbitrary number does not
    certify a concrete K. Keeping it a parameter avoids constructing enormous
    powers just to state the formula.
    """
    check_D(D)
    if any(type(a) is not int or a < 0 for a in (n, augmented_width, burst)):
        raise ValueError('nonnegative integer parameters required')
    Q = 1 << D
    return n*(2*Q*augmented_width+20*Q*Q+burst)+18*Q*Q*n*(n-1)


def external_density_index(D: int, width: int, burst: int, time: int) -> int:
    check_D(D)
    if any(type(a) is not int or a < 0 for a in (width, burst, time)):
        raise ValueError('nonnegative integer parameters required')
    lo, hi = 0, 1
    while external_event_deadline(D, hi, width, burst) <= time:
        lo, hi = hi, 2*hi
    while hi-lo > 1:
        mid = (lo+hi)//2
        if external_event_deadline(D, mid, width, burst) <= time:
            lo = mid
        else:
            hi = mid
    return lo


def first_external_event(start: State, D: int, K: frozenset[Point], *,
                         max_events: int | None = None,
                         max_literal_updates: int | None = None,
                         max_suffix_states: int | None = None) -> dict:
    """Total uncapped decision of whether S_D ever occurs outside FIXED K.

    All inside events are executed with the FULL finite field retained. The new
    endpoint-tube/escape theorem proves this loop cannot continue forever.
    Bounds are kept symbolic: evaluating 3**(6*2**D) is not needed to execute.
    This implementation replays inside-event gaps literally; no efficiency or
    complete-state symbolic acceleration claim is made for those gaps.
    """
    check_D(D)
    for cap in (max_events, max_literal_updates, max_suffix_states):
        cap_ok(cap)
    if not isinstance(K, frozenset) or any(not point_ok(p) for p in K):
        raise ValueError('K must be a fixed finite frozenset of integer points')
    side = guard_side(K | {start.pos}, D)
    here, elapsed, count = start, 0, 0
    while True:
        if max_events is not None and count >= max_events:
            return {'kind': 'INCONCLUSIVE', 'reason': 'event cap',
                    'inside_events': count, 'literal_updates': elapsed}
        result = first_event(here, D, max_suffix_states)
        if result['kind'] == 'INCONCLUSIVE':
            return dict(result, inside_events=count, literal_updates=elapsed)
        if result['kind'] == 'FREE':
            return {'kind': 'NO_EXTERNAL_EVENT', 'D': D, 'inside_events': count,
                    'literal_updates': elapsed, 'guard_square_side': side,
                    'tail': result, 'full_endpoint_black_count': len(here.black)}
        point, time = tuple(result['point']), result['time']
        if point not in K:
            return {'kind': 'EXTERNAL_EVENT', 'D': D, 'time': elapsed+time,
                    'point': list(point), 'inside_events': count,
                    'literal_updates': elapsed, 'guard_square_side': side,
                    'next_event_witness': result}
        duration = time+1
        if max_literal_updates is not None and elapsed+duration > max_literal_updates:
            return {'kind': 'INCONCLUSIVE', 'reason': 'literal replay cap',
                    'inside_events': count, 'literal_updates': elapsed}
        before, _, _ = replay(here, time)
        if before.pos != point or not stale(before, D):
            raise AssertionError('next-event witness failed literal endpoint check')
        here, _ = step(before)
        elapsed += duration
        count += 1
