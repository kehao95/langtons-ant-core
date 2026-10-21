"""Exact first departure from a fixed frozen incoming-state contour.

A departure is NOT permanent spatial escape. Full input fields are retained.
This module has no P104, J10, periodicity or future-liveness premise.
"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

Point = tuple[int, int]
Dart = tuple[int, int, int]
DIR = ((0, 1), (1, 0), (0, -1), (-1, 0))


def validate_dart(e: Dart) -> None:
    if len(e) != 3 or any(type(v) is not int for v in e) or e[2] not in range(4):
        raise ValueError('integer point and heading 0..3 required')


def frozen_successor(black: set[Point] | frozenset[Point], e: Dart) -> Dart:
    x, y, h = e
    h = (h + (-1 if (x, y) in black else 1)) % 4
    dx, dy = DIR[h]
    return x + dx, y + dy, h


def frozen_contour(black: Iterable[Point], root: Dart) -> tuple[Dart, ...]:
    validate_dart(root)
    black = frozenset(black)
    if any(len(p) != 2 or any(type(z) is not int for z in p) for p in black):
        raise ValueError('finite set of integer pairs required')
    current = root
    seen: set[Dart] = set()
    contour: list[Dart] = []
    bound = max(4, 8 * len(black))
    while current not in seen:
        seen.add(current)
        contour.append(current)
        if len(contour) > bound:
            raise AssertionError('inherited finite-modification contour bound failed')
        current = frozen_successor(black, current)
    if current != root:
        raise AssertionError('frozen routing must be a permutation')
    return tuple(contour)


def contact_matching(contour: tuple[Dart, ...]) -> tuple[int | None, ...]:
    if not contour or len(set(contour)) != len(contour):
        raise ValueError('nonempty, distinct incoming states required')
    index = {e: i for i, e in enumerate(contour)}
    return tuple(index.get((x, y, (h + 2) % 4)) for x, y, h in contour)


def validate_matching(mate: tuple[int | None, ...]) -> None:
    if not mate:
        raise ValueError('empty contour')
    for i, j in enumerate(mate):
        if j is not None and (type(j) is not int or not 0 <= j < len(mate)
                              or j == i or mate[j] != i):
            raise ValueError('matching must be a symmetric partial involution')


def noninterlaced(mate: tuple[int | None, ...]) -> bool:
    """Linear-time stack test for noninterleaving cyclic chords, cut at root."""
    validate_matching(mate)
    stack: list[int] = []
    for i, j in enumerate(mate):
        if j is None:
            continue
        if i < j:
            stack.append(j)
        elif not stack or stack.pop() != i:
            return False
    return not stack


def crossing_count(mate: tuple[int | None, ...]) -> int:
    pairs = [(i, j) for i, j in enumerate(mate) if j is not None and i < j]
    return sum(a < c < b < d or c < a < d < b
               for k, (a, b) in enumerate(pairs) for c, d in pairs[:k])


def noninterlaced_itinerary(mate: tuple[int | None, ...]) -> tuple[int, ...]:
    """Exact pre-update itinerary under noninterlacing and no adjacent contact.

    The abstract matching need not be grid-realizable. Both hypotheses are
    checked; unproved extrapolation to interlaced contours is refused.
    """
    if not noninterlaced(mate):
        raise ValueError('interlaced contacts are outside the theorem')
    n = len(mate)
    if any(j is not None and (j - i) % n in (1, n - 1) for i, j in enumerate(mate)):
        raise ValueError('adjacent paired occurrences are excluded')
    repeated = [(i, j) for i, j in enumerate(mate) if j is not None and j < i]
    if not repeated:
        return tuple(range(n)) + (0,)
    b, a = min(repeated)
    if not (a + 1 < b and mate[a + 1] is None):
        raise AssertionError('first-contact port lemma failed')
    return tuple(range(b + 1)) + (a + 1,)


@dataclass(frozen=True)
class MatchingRun:
    status: str
    itinerary: tuple[int, ...]
    exit_port: int | None


def run_matching(mate: tuple[int | None, ...], *, cap: int = 100000,
                 detect_loops: bool = True) -> MatchingRun:
    """General exact finite matching machine; a resource cap is INCONCLUSIVE."""
    validate_matching(mate)
    if type(cap) is not int or cap < 0:
        raise ValueError('nonnegative update cap required')
    n = len(mate)
    successors = list(range(1, n)) + [0]
    root = 0
    seen: set[tuple[int, tuple[int, ...]]] = set()
    path: list[int] = []
    for _ in range(cap):
        if detect_loops:
            state = root, tuple(successors)
            if state in seen:
                return MatchingRun('ABSTRACT_LOOP', tuple(path), None)
            seen.add(state)
        path.append(root)
        nxt = successors[root]
        other = mate[root]
        if other is None:
            successors[root] = -1 if nxt >= 0 else (root + 1) % n
        else:
            successors[root], successors[other] = successors[other], successors[root]
        if nxt < 0:
            return MatchingRun('EXIT', tuple(path), root)
        root = nxt
    return MatchingRun('INCONCLUSIVE', tuple(path), None)


@dataclass(frozen=True)
class PhysicalExit:
    updates: int
    contour: tuple[Dart, ...]
    matching: tuple[int | None, ...]
    itinerary: tuple[int, ...]
    exit_dart: Dart
    black: frozenset[Point]


def endpoint(black: Iterable[Point], contour: tuple[Dart, ...],
             itinerary: tuple[int, ...]) -> PhysicalExit:
    """Reconstruct COMPLETE output using actual physical-site visit parity."""
    source = frozenset(black)
    mate = contact_matching(contour)
    if not itinerary or mate[itinerary[-1]] is not None:
        raise ValueError('last read must be at an exposed port')
    counts = Counter(contour[i][:2] for i in itinerary)
    changed = {p for p, count in counts.items() if count % 2}
    x, y, h = contour[itinerary[-1]]
    outside = frozen_successor(source, (x, y, (h + 2) % 4))
    if outside in set(contour):
        raise AssertionError('opposite-port successor is not outside')
    return PhysicalExit(len(itinerary), contour, mate, itinerary, outside,
                        frozenset(source.symmetric_difference(changed)))


def first_contour_exit(black: Iterable[Point], root: Dart, *, cap: int = 100000) -> PhysicalExit:
    source = frozenset(black)
    contour = frozen_contour(source, root)
    mate = contact_matching(contour)
    if noninterlaced(mate):
        itinerary = noninterlaced_itinerary(mate)
        if len(itinerary) > cap:
            raise RuntimeError('INCONCLUSIVE: requested execution cap')
    else:
        result = run_matching(mate, cap=cap)
        if result.status != 'EXIT':
            raise RuntimeError(result.status + ': not an HC-negative certificate')
        itinerary = result.itinerary
    return endpoint(source, contour, itinerary)


def physical_state_bound(mate: tuple[int | None, ...]) -> int:
    """Universal finite-state bound for PHYSICALLY REALIZABLE contours only.

    Totality imports no-finite-orbit, not an assumption for arbitrary diagrams.
    """
    validate_matching(mate)
    ports = sum(j is None for j in mate)
    pairs = (len(mate) - ports) // 2
    if not ports:
        raise ValueError('a finite physical plane contour must expose a port')
    return (ports + 1) * (2 * pairs * (1 << pairs) + 1)


def sharp_seed(n: int) -> tuple[frozenset[Point], str]:
    if type(n) is not int or n < 0:
        raise ValueError('n must be nonnegative')
    word = 'RL' * n + 'RLRRLR' + 'RL' * n + 'RLRRLR'
    current = (0, 0, 0)
    seen: set[Point] = set()
    black: set[Point] = set()
    for letter in word:
        x, y, h = current
        if (x, y) in seen:
            raise AssertionError('claimed sharp family is not site-simple')
        seen.add((x, y))
        if letter == 'L':
            black.add((x, y))
        h = (h + (1 if letter == 'R' else -1)) % 4
        dx, dy = DIR[h]
        current = x + dx, y + dy, h
    if current != (0, 0, 0) or len(black) != 2 * n + 4:
        raise AssertionError('sharp family endpoint or supply identity')
    return frozenset(black), word
