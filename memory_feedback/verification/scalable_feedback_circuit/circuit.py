"""Twenty-cell scalable feedback circuit, with all-parameter affine guards.

Literal classical ant: white/right, black/left, toggle then move. Parameter
n=2*k, k>=10. This is a family of finite autonomous positive inputs, not a
self-renewing device or an HC counterexample. No shared simulator is changed.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache

Point = tuple[int, int]
Linear = tuple[int, int]  # a*k+b
DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))
G = frozenset({(0, -1), (1, 1), (1, 3), (2, 2)})
KMIN = 10
PERIOD = 104
PRELUDE = 182
REGION = (-16, -14, 12)  # x>=-16 and -14<=x+y<=12

@dataclass(frozen=True)
class State:
    black: frozenset[Point]
    pos: Point = (0, 0)
    heading: int = 1

def rotate(p: Point, clockwise: int) -> Point:
    x, y = p
    for _ in range(clockwise % 4):
        x, y = y, -x
    return x, y

def add(p: Point, q: Point) -> Point:
    return p[0]+q[0], p[1]+q[1]

def lin_value(a: Linear, k: int) -> int:
    return a[0]*k+a[1]

def lin_sub(a: Linear, b: Linear) -> Linear:
    return a[0]-b[0], a[1]-b[1]

def in_region(p: Point) -> bool:
    return p[0] >= REGION[0] and REGION[1] <= sum(p) <= REGION[2]

def replay(x: State, steps: int) -> tuple[State, str, list[Point], list[int]]:
    if type(steps) is not int or steps < 0:
        raise ValueError('nonnegative integer number of updates required')
    black, p, h = set(x.black), x.pos, x.heading
    positions, headings, word = [p], [h], []
    for _ in range(steps):
        bit = p in black
        word.append('L' if bit else 'R')
        black.symmetric_difference_update((p,))
        h = (h + (-1 if bit else 1)) % 4
        p = add(p, DIRS[h])
        positions.append(p)
        headings.append(h)
    return State(frozenset(black), p, h), ''.join(word), positions, headings

def inverse(x: State) -> State:
    v = DIRS[x.heading]
    q = x.pos[0]-v[0], x.pos[1]-v[1]
    bit = q in x.black
    return State(x.black.symmetric_difference((q,)), q,
                 (x.heading + (-1 if bit else 1)) % 4)

def multiple(v: Point, d: Point) -> int | None:
    if d == (0, 0):
        raise ValueError('nonzero drift required')
    a = 0 if d[0] else 1
    if v[a] % d[a]:
        return None
    k = v[a]//d[a]
    return k if (k*d[0], k*d[1]) == v else None

def geometry(p: Point, h: int, word: str):
    if not word or set(word)-{'R', 'L'}:
        raise ValueError('nonempty R/L word required')
    points, heads = [p], [h]
    for ch in word:
        h = (h + (1 if ch == 'R' else -1)) % 4
        p = add(p, DIRS[h])
        points.append(p); heads.append(h)
    return points, heads

def verify_period(x: State, word: str) -> dict:
    """Complete-field parity at ALL epoch breakpoints, including infinity.

    This reimplements the already attributed supplied-word criterion. It does
    not infer an infinite tail from finite repetition.
    """
    ps, hs = geometry(x.pos, x.heading, word)
    d = ps[-1][0]-x.pos[0], ps[-1][1]-x.pos[1]
    if hs[-1] != x.heading or d == (0, 0):
        return {'valid': False, 'reason': 'not a heading-restoring translator'}
    ps = ps[:-1]; P = len(word); bad = None; count = 0
    for i, p in enumerate(ps):
        thresholds = []
        for j, q in enumerate(ps):
            r = multiple((q[0]-p[0], q[1]-p[1]), d)
            if r is not None and (r > 0 or (r == 0 and j < i)):
                thresholds.append(r)
        hits = set()
        for q in x.black:
            r = multiple((q[0]-p[0], q[1]-p[1]), d)
            if r is not None and r >= 0:
                hits.add(r)
        for r in {0, *thresholds, *hits, *(a+1 for a in hits)}:
            count += 1
            bit = (int(r in hits)+sum(a <= r for a in thresholds)) % 2
            if bit != int(word[i] == 'L'):
                at = r*P+i
                bad = at if bad is None else min(bad, at)
    return {'valid': bad is None, 'first_bad': bad, 'period': P,
            'drift': list(d), 'breakpoints': count}

@lru_cache(maxsize=1)
def reference() -> dict:
    start = State(G)
    tail, A, prefix, prefix_h = replay(start, PRELUDE)
    _, U, cycle, cycle_h = replay(tail, PERIOD)
    return {'source': start, 'tail': tail, 'A': A, 'U': U,
            'prefix': prefix[:-1], 'prefix_h': prefix_h[:-1],
            'cycle': cycle[:-1], 'cycle_h': cycle_h,
            'cycle_endpoint': cycle[-1]}

# origins have two affine coordinates in k; clockwise rotation relative to E.
SPECS = (
    (((0, 0), (0, 0)), 0, (1, -4), 61),
    (((2, -1), (2, 0)), -1, (2, -5), 71),
    (((-2, 0), (6, -4)), 2, (4, -6), 61),
    (((-10, 5), (-2, 0)), 1, (2, -7), 71),
    (((-6, 0), (-6, 8)), 0, (3, -4), 14),
)
# Every row asserts max(normal.A)<boundary<=min(normal.B), for ALL k>=10.
SEPARATORS = (
    (0, 1, (0, 1), (2, 0)),
    (2, 0, (1, 0), (0, 0)),
    (3, 0, (0, 1), (0, -2)),
    (4, 0, (1, 0), (0, 0)),
    (2, 1, (1, 0), (-2, 1)),
    (3, 1, (0, 1), (2, 0)),
    (4, 1, (0, 1), (2, 0)),
    (3, 2, (0, 1), (-2, 1)),
    (2, 4, (1, -1), (0, -11)),
    (3, 4, (1, 0), (-6, 0)),
)

def parameter(n: int) -> int:
    if type(n) is not int or n < 20 or n % 2:
        raise ValueError('n must be an even integer at least 20')
    return n//2

def seed(n: int) -> State:
    k = parameter(n); black = set()
    for origin, rotation, _, _ in SPECS:
        p = tuple(lin_value(a, k) for a in origin)
        black.update(add(p, rotate(q, rotation)) for q in G)
    if len(black) != 20:
        raise AssertionError('twenty distinct input cells required')
    return State(frozenset(black))

def stage_length(i: int, k: int) -> int:
    _, _, repeats, remainder = SPECS[i]
    return PRELUDE+PERIOD*lin_value(repeats, k)+remainder

def milestones(n: int) -> list[int]:
    k = parameter(n); times = [0]
    for i in range(5):
        times.append(times[-1]+stage_length(i, k))
    return times

def stage_word(i: int, k: int) -> str:
    _, _, repeats, remainder = SPECS[i]; r = reference()
    return r['A']+r['U']*lin_value(repeats, k)+r['U'][:remainder]

def projection_bounds(stage: int, normal: Point) -> list[tuple[Linear, Linear]]:
    """Exact affine extrema for every finite point or repeated-phase stream."""
    origin, rot, repeats, remainder = SPECS[stage]
    r = reference(); d = rotate((2, 2), rot)
    base = (sum(normal[a]*origin[a][0] for a in range(2)),
            sum(normal[a]*origin[a][1] for a in range(2)))
    ds = sum(normal[a]*d[a] for a in range(2))
    out = []
    def point(q):
        q = rotate(q, rot)
        return base[0], base[1]+sum(normal[a]*q[a] for a in range(2))
    for q in r['prefix']:
        v = point(q); out.append((v, v))
    for q in r['cycle']:
        v = point(q)
        end = v[0]+ds*repeats[0], v[1]+ds*(repeats[1]-1)
        out.append((v, end) if ds >= 0 else (end, v))
    for q in r['cycle'][:remainder]:
        v = point(q)
        end = v[0]+ds*repeats[0], v[1]+ds*repeats[1]
        out.append((end, end))
    return out

def affine_nonnegative(a: Linear) -> bool:
    """Exact universal test on the integer half-line k>=KMIN."""
    return a[0] >= 0 and lin_value(a, KMIN) >= 0

def separation_certificate() -> dict:
    count = 0; minimum_slack = None; rows = []
    for A, B, normal, boundary in SEPARATORS:
        inequalities = []
        for _, upper in projection_bounds(A, normal):
            inequalities.append(lin_sub((boundary[0], boundary[1]-1), upper))
        for lower, _ in projection_bounds(B, normal):
            inequalities.append(lin_sub(lower, boundary))
        if not all(affine_nonnegative(a) for a in inequalities):
            raise AssertionError(('invalid separator', A, B, normal))
        slack = min(lin_value(a, KMIN) for a in inequalities)
        minimum_slack = slack if minimum_slack is None else min(slack, minimum_slack)
        count += len(inequalities)
        rows.append({'lower_stage': A, 'upper_stage': B, 'normal': list(normal),
                     'boundary': list(boundary), 'inequalities': len(inequalities),
                     'minimum_slack_at_k10': slack})
    if len({frozenset((a,b)) for a,b,_,_ in SEPARATORS}) != 10:
        raise AssertionError('must cover all ten stage pairs')
    for _, _, repeats, _ in SPECS:
        if not affine_nonnegative((repeats[0], repeats[1]-1)):
            raise AssertionError('at least one complete cycle in every stage')
    return {'universal_linear_inequalities': count, 'minimum_slack': minimum_slack,
            'separators': rows}

def protected_core() -> frozenset[Point]:
    """The n-independent restriction of the collision field to REGION.

    Section 4 of the proof derives this finite XOR formula. Stages 1,2,3 lie
    outside REGION; the two NE streams are truncated only outside it.
    """
    r = reference(); black = set()
    def toggle(q):
        if in_region(q): black.symmetric_difference_update((q,))
    for q in G: toggle(q)
    for q in r['prefix']: toggle(q)
    # Stage zero: at k=10 there are six full cycles; all later cycles miss REGION.
    for j in range(6):
        for q in r['cycle']: toggle(add(q, (2*j, 2*j)))
    # Final stage: v=j-(3k-4), with fixed terminal-epoch origin (-8,0).
    for v in range(-26, 0):
        for q in r['cycle']: toggle(add(q, (2*v-8, 2*v)))
    for q in r['cycle'][:14]: toggle(add(q, (-8, 0)))
    return frozenset(black)

def protected_region_certificate() -> dict:
    """Check the affine inequalities used to discard NO physical data.

    These prove equality of restrictions. Every exterior cell stays in the
    true full field; coupling, not erasure of the actual input, is used.
    """
    inequalities = []
    # Stage 1: x+y>12. Stage 3: x+y<-14.
    for low, _ in projection_bounds(1, (1, 1)):
        inequalities.append(lin_sub(low, (0, 13)))
    for _, high in projection_bounds(3, (1, 1)):
        inequalities.append(lin_sub((0, -15), high))
    # REGION entails x-y>=-44. Stage 2 has x-y<=-45.
    for _, high in projection_bounds(2, (1, -1)):
        inequalities.append(lin_sub((0, -45), high))
    r = reference()
    # Stage 4 source and finite prelude are below the strip.
    for q in [*G, *r['prefix']]:
        # sum(origin4+q)=-12k+8+sum(q), required <=-15.
        inequalities.append((12, -23-sum(q)))
    # All stage-0 tail epochs j>=6 are above the strip.
    for q in r['cycle']:
        if sum(q)+24 < 13: raise AssertionError('stage-0 truncation')
    # All incoming epochs v<=-27 are below the strip.
    for q in r['cycle']:
        if sum(q)-8-108 > -15: raise AssertionError('incoming truncation')
    if not all(affine_nonnegative(a) for a in inequalities):
        raise AssertionError('parameter-independent protected-region equality failed')
    return {'affine_inequalities': len(inequalities),
            'constant_tail_inequalities': 2*len(r['cycle']),
            'core_cells': len(protected_core())}

def first_return_time(n: int) -> int:
    parameter(n)
    return 624*n-1516

def standard_entry_time(n: int) -> int:
    parameter(n)
    return first_return_time(n)+774


def full_collision_state(n: int) -> State:
    """Exact finite XOR of the full declared prefix, not an isolated core.

    Universal executability is supplied by the stage separation certificate;
    this generator retains all prior writes and initial cells.
    """
    k = parameter(n); black = set(seed(n).black); r = reference()
    for origin, rot, repeats, remainder in SPECS:
        p = tuple(lin_value(a, k) for a in origin)
        for q in r['prefix']:
            black.symmetric_difference_update((add(p, rotate(q, rot)),))
        d = rotate((2, 2), rot)
        for j in range(lin_value(repeats, k)):
            shift = p[0]+j*d[0], p[1]+j*d[1]
            for q in r['cycle']:
                black.symmetric_difference_update((add(shift, rotate(q, rot)),))
        j = lin_value(repeats, k); shift = p[0]+j*d[0], p[1]+j*d[1]
        for q in r['cycle'][:remainder]:
            black.symmetric_difference_update((add(shift, rotate(q, rot)),))
    return State(frozenset(black), (0, 2), 1)
