"""Geometry-free bounded-reread-delay analysis for the literal LR ant.

White turns right, black turns left, then flip and move; states are pre-update.
A delay violation is NOT a negative HIGHWAY or universality result.
The periodic verifier uses exact integer ray intersections and all-future parity.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

Point = tuple[int, int]
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))

@dataclass(frozen=True)
class State:
    black: frozenset[Point]
    pos: Point = (0, 0)
    heading: int = 0

    def __post_init__(self):
        if type(self.heading) is not int or self.heading not in range(4):
            raise ValueError('heading must be an integer in 0..3')
        if any(len(q) != 2 or any(type(a) is not int for a in q)
               for q in [self.pos, *self.black]):
            raise ValueError('all positions must be pairs of integers')


def simulate(start: State, steps: int):
    if type(steps) is not int or steps < 0:
        raise ValueError('steps must be a nonnegative integer')
    black, pos, h = set(start.black), start.pos, start.heading
    positions, turns = [pos], []
    for _ in range(steps):
        occupied = pos in black
        turns.append('L' if occupied else 'R')
        black.symmetric_difference_update((pos,))
        h = (h + (-1 if occupied else 1)) % 4
        dx, dy = DIRS[h]
        pos = (pos[0] + dx, pos[1] + dy)
        positions.append(pos)
    return State(frozenset(black), pos, h), ''.join(turns), positions


def suffix_predict(word: str) -> str:
    """The order-D predictor: invert the latest return's read; fresh means R.

    This predicts literal dynamics only when the present cell's previous read
    is inside this suffix, or when it is a virgin initially white cell.
    Translation/rotation do not affect the coordinate-equality test.
    """
    if not word or set(word) - {'R', 'L'}:
        raise ValueError('a nonempty R/L suffix is required')
    p, h, visits = (0, 0), 0, []
    for letter in word:
        visits.append(p)
        h = (h + (1 if letter == 'R' else -1)) % 4
        dx, dy = DIRS[h]
        p = (p[0] + dx, p[1] + dy)
    for j in range(len(visits) - 1, -1, -1):
        if visits[j] == p:
            return 'L' if word[j] == 'R' else 'R'
    return 'R'


def multiple(v: Point, drift: Point) -> int | None:
    """Return the integer k with v=k*drift; drift must be nonzero."""
    if drift == (0, 0):
        raise ValueError('zero drift')
    axis = 0 if drift[0] else 1
    if v[axis] % drift[axis]:
        return None
    k = v[axis] // drift[axis]
    return k if (k * drift[0], k * drift[1]) == v else None


def geometry(start: State, word: str):
    if not word or set(word) - {'R', 'L'}:
        raise ValueError('a nonempty R/L period is required')
    p, h, points = start.pos, start.heading, []
    for letter in word:
        points.append(p)
        h = (h + (1 if letter == 'R' else -1)) % 4
        dx, dy = DIRS[h]
        p = (p[0] + dx, p[1] + dy)
    return points, h, (p[0] - start.pos[0], p[1] - start.pos[1])


def _links(points: list[Point], drift: Point, i: int):
    """(threshold epoch r, temporal gap) for preceding periodic reads."""
    P = len(points)
    result = []
    for j, q in enumerate(points):
        r = multiple((q[0] - points[i][0], q[1] - points[i][1]), drift)
        if r is not None and r >= 0 and (r > 0 or j < i):
            result.append((r, r * P + i - j))
    return result


def verify_period(start: State, word: str) -> dict:
    """Decide whether the COMPLETE input state follows word^omega exactly.

    Each proposed read lies on points[i]+k*drift. Earlier periodic reads turn
    on at finitely many epoch thresholds; finite initial black cells cause
    finitely many one-epoch exceptions. Check all breakpoints, including the
    final unbounded interval. No finite simulation is extrapolated.
    """
    points, end_h, drift = geometry(start, word)
    if end_h != start.heading:
        return {'valid': False, 'reason': 'nonzero heading rotation'}
    if drift == (0, 0):
        return {'valid': False, 'reason': 'zero drift would confine the orbit'}
    checks, first_bad = 0, None
    P = len(word)
    for i, p in enumerate(points):
        links = _links(points, drift, i)
        hits = set()
        for q in start.black:
            k = multiple((q[0] - p[0], q[1] - p[1]), drift)
            if k is not None and k >= 0:
                hits.add(k)
        breaks = {0} | {r for r, _ in links} | hits | {k + 1 for k in hits}
        for k in sorted(breaks):
            colour = (int(k in hits) + sum(k >= r for r, _ in links)) % 2
            checks += 1
            if colour != int(word[i] == 'L'):
                candidate = k * P + i
                if first_bad is None or candidate < first_bad:
                    first_bad = candidate
    result = {'valid': first_bad is None, 'period': P, 'drift': list(drift),
              'breakpoint_checks': checks}
    if first_bad is not None:
        result.update(reason='all-future read parity mismatch',
                      first_bad_offset=first_bad)
    return result


def periodic_delay(start: State, word: str, last_read: Mapping[Point, int] | None = None,
                   start_time: int = 0, limit: int | None = None) -> dict:
    """Compute the maximum future consecutive-read delay and first violation.

    Requires an already verified period. last_read uses absolute times strictly
    below start_time. Initial cells with no historical read do not have a delay.
    The colour verifier and this lifetime verifier serve different obligations.
    """
    points, end_h, drift = geometry(start, word)
    if end_h != start.heading or drift == (0, 0):
        raise ValueError('requires a nonzero translating period')
    old = {} if last_read is None else dict(last_read)
    if any(type(t) is not int or t >= start_time for t in old.values()):
        raise ValueError('historical read times must be integers below start_time')
    if limit is not None and (type(limit) is not int or limit < 0):
        raise ValueError('limit must be a nonnegative integer')
    largest, first = 0, None
    P = len(word)

    def observe(offset: int, gap: int, point: Point):
        nonlocal largest, first
        largest = max(largest, gap)
        if limit is not None and gap > limit:
            record = {'time': start_time + offset, 'previous_time': start_time + offset - gap,
                      'gap': gap, 'point': list(point)}
            if first is None or record['time'] < first['time']:
                first = record

    for i, p in enumerate(points):
        links = _links(points, drift, i)
        threshold = min((r for r, _ in links), default=None)
        if threshold is not None:
            # As k grows, more previous visits become eligible. Their minimum
            # positive gap cannot increase, so the first eligible epoch attains
            # the largest internal-period consecutive-read gap for this phase.
            gap = min(g for r, g in links if r == threshold)
            point = (p[0] + threshold * drift[0], p[1] + threshold * drift[1])
            observe(threshold * P + i, gap, point)
        for q, previous in old.items():
            k = multiple((q[0] - p[0], q[1] - p[1]), drift)
            if k is not None and k >= 0 and (threshold is None or k < threshold):
                observe(k * P + i, start_time + k * P + i - previous, q)
    return {'max_future_delay': largest, 'first_violation': first}


def classify_delay(start: State, D: int, max_steps: int | None = None) -> dict:
    """Total exact classifier with supplied D, unless a caller imposes a cap.

    Returns either a real (possibly symbolically certified future) delay>D, or
    a fully verified translating tail with every future delay<=D. No geometric
    confinement, mass bound, input-size cutoff, or MSO compiler is assumed.
    Failed guesses are never NO answers. Totality follows from the bounded-delay
    theorem in PROOF.md, not from an assumed global claim about arbitrary seeds.
    """
    if type(D) is not int or D < 1:
        raise ValueError('D must be a positive integer')
    if max_steps is not None and (type(max_steps) is not int or max_steps < 0):
        raise ValueError('max_steps must be a nonnegative integer')
    black, pos, h = set(start.black), start.pos, start.heading
    last, turns, seen = {}, [], {}
    t, trials, exceptions = 0, 0, 0
    while True:
        if pos in last and t - last[pos] > D:
            return {'kind': 'delay_violation', 'D': D, 'time': t,
                    'previous_time': last[pos], 'point': list(pos), 'gap': t-last[pos],
                    'witness_mode': 'literal_prefix', 'updates_executed': t,
                    'period_trials': trials, 'virgin_black_reads': exceptions}
        virgin_black = pos not in last and pos in black
        if t >= D and not virgin_black:
            key = ''.join(turns[-D:])
            if key in seen:
                word = ''.join(turns[seen[key]:t])
                here = State(frozenset(black), pos, h)
                certificate = verify_period(here, word)
                trials += 1
                if certificate['valid']:
                    delay = periodic_delay(here, word, last, t, D)
                    base = {'D': D, 'entry': t, 'turns': word, 'certificate': certificate,
                            'delay_check': delay, 'updates_executed': t,
                            'period_trials': trials, 'virgin_black_reads': exceptions}
                    if delay['first_violation'] is not None:
                        return dict(base, kind='delay_violation',
                                    witness_mode='verified_periodic_future',
                                    **delay['first_violation'])
                    return dict(base, kind='translating_tail')
            seen[key] = t
        if max_steps is not None and t >= max_steps:
            return {'kind': 'inconclusive', 'D': D, 'updates_executed': t,
                    'period_trials': trials, 'reason': 'caller resource limit'}
        if virgin_black:
            exceptions += 1
            seen.clear()
        occupied = pos in black
        turns.append('L' if occupied else 'R')
        last[pos] = t
        black.symmetric_difference_update((pos,))
        h = (h + (-1 if occupied else 1)) % 4
        dx, dy = DIRS[h]
        pos = (pos[0] + dx, pos[1] + dy)
        t += 1
