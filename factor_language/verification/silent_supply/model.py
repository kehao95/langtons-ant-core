"""Literal classical ant and complete finite-XOR fields, for silent-supply checks.

White/right, black/left, toggle and then move. Time is pre-update. No history
is deleted. These routines do not decide unrestricted HIGHWAY.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

Point = tuple[int, int]
DIR: tuple[Point, ...] = ((0, 1), (1, 0), (0, -1), (-1, 0))
W = ('RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRL'
     'LRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR')
T = 'RRRRLLRLLRRRRLLRRRRLLRLL'
A = 'LLRRRRLRRLRRRRLLLLRLRRRRLRLL'
B = ('RRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLRRRRLRLLLLRRRR'
     'LRRLRRRRLLLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRLL')
L10 = frozenset((W * 2)[i:i + 10] for i in range(104))
WORD_HASH = '6b76e51621e15d2304f1c0baa28790cc267cabafca3fc03250dea8721b2b4794'
F = 1322
CORE_INTERCEPT = 154693
RETURN_INTERCEPT = 223437


def allowance(m: int) -> int:
    if type(m) is not int or m < 0:
        raise ValueError('nonnegative integer mass required')
    return 114 * m + CORE_INTERCEPT


def add(p: Point, q: Point) -> Point:
    return p[0] + q[0], p[1] + q[1]


def mul(n: int, p: Point) -> Point:
    return n * p[0], n * p[1]


def geometry(word: str, heading: int = 0):
    if set(word) - {'R', 'L'} or type(heading) is not int or heading not in range(4):
        raise ValueError('invalid LR word or heading')
    p = (0, 0)
    h = heading
    points, headings = [], []
    for ch in word:
        points.append(p)
        headings.append(h)
        h = (h + (1 if ch == 'R' else -1)) % 4
        p = add(p, DIR[h])
    return points, p, headings, h


def multiple(p: Point, d: Point):
    if d == (0, 0):
        raise ValueError('nonzero direction required')
    a = 0 if d[0] else 1
    if p[a] % d[a]:
        return None
    k = p[a] // d[a]
    return k if p == mul(k, d) else None


def minimal_seed(word: str, heading: int = 0) -> frozenset[Point] | None:
    """Full finite-word test, not an infinite-tail certificate."""
    points, _, _, _ = geometry(word, heading)
    last: dict[Point, str] = {}
    black = set()
    for p, ch in zip(points, word):
        if p not in last:
            if ch == 'L':
                black.add(p)
        elif last[p] == ch:
            return None
        last[p] = ch
    return frozenset(black)


def defect_count(word: str) -> int:
    return sum(word[t-9:t+1] not in L10 for t in range(9, len(word)))


def literal(cells: Iterable[Point], steps: int, head: Point = (0, 0), heading: int = 0):
    black = set(cells)
    letters, positions = [], [head]
    for _ in range(steps):
        ch = 'L' if head in black else 'R'
        letters.append(ch)
        if ch == 'L':
            black.remove(head)
        else:
            black.add(head)
        heading = (heading + (1 if ch == 'R' else -1)) % 4
        head = add(head, DIR[heading])
        positions.append(head)
    return frozenset(black), head, heading, ''.join(letters), positions


def inverse_history(cells: Iterable[Point], head: Point, heading: int, length: int = 9) -> str:
    black = set(cells)
    letters = []
    for _ in range(length):
        q = add(head, mul(-1, DIR[heading]))
        ch = 'R' if q in black else 'L'
        if q in black:
            black.remove(q)
        else:
            black.add(q)
        heading = (heading - (1 if ch == 'R' else -1)) % 4
        head = q
        letters.append(ch)
    return ''.join(reversed(letters))


@dataclass(frozen=True)
class Segment:
    start: Point
    stride: Point
    length: int

    def __post_init__(self):
        if type(self.length) is not int or self.length <= 0 or self.stride == (0, 0):
            raise ValueError('positive finite translating segment required')

    def contains(self, q: Point) -> bool:
        k = multiple((q[0]-self.start[0], q[1]-self.start[1]), self.stride)
        return k is not None and 0 <= k < self.length


@dataclass(frozen=True)
class Field:
    """Complete field: base XOR point changes XOR every finite segment."""
    base: frozenset[Point]
    changes: frozenset[Point] = frozenset()
    segments: tuple[Segment, ...] = ()

    def black(self, p: Point) -> bool:
        bit = (p in self.base) ^ (p in self.changes)
        for segment in self.segments:
            bit ^= segment.contains(p)
        return bit

    def expand(self, cap: int = 1000000) -> frozenset[Point]:
        if len(self.base) + len(self.changes) + sum(s.length for s in self.segments) > cap:
            raise ValueError('expansion cap, not a mathematical negative answer')
        result = set(self.base ^ self.changes)
        for s in self.segments:
            for j in range(s.length):
                p = add(s.start, mul(j, s.stride))
                if p in result:
                    result.remove(p)
                else:
                    result.add(p)
        return frozenset(result)


def first_period_mismatch(cells: Iterable[Point], head: Point, heading: int, word: str):
    """Exact first disagreement with word^omega, using all finite-source points.

    A final infinite parity interval is checked. None is a proof of permanence,
    not a finite repetition heuristic. This is the inherited ray-parity method.
    """
    # Materialize once: iterable inputs may be generators or contain duplicates.
    cells = frozenset(cells)
    rel, drift, _, end_h = geometry(word, heading)
    if end_h != heading or drift == (0, 0):
        raise ValueError('heading-resetting translating word required')
    qs = [add(head, p) for p in rel]
    P = len(word)
    answer = None
    for i, q in enumerate(qs):
        changes = {0: int(word[i] == 'L')}
        def toggle(k):
            changes[k] = changes.get(k, 0) ^ 1
        for j, z in enumerate(qs):
            s = multiple((z[0]-q[0], z[1]-q[1]), drift)
            if s is not None and (s > 0 or (s == 0 and j < i)):
                toggle(s)
        for z in cells:
            s = multiple((z[0]-q[0], z[1]-q[1]), drift)
            if s is not None and s >= 0:
                toggle(s)
                toggle(s + 1)
        bit = 0
        for k in sorted(changes):
            bit ^= changes[k]
            if bit:
                time = P*k+i
                answer = time if answer is None else min(answer, time)
                break
    return answer
