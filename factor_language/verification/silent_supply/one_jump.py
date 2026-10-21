"""Exact first intrinsic J10 with at most one standard-highway jump.

Totality depends on the analytic silent-supply theorem and inherited complete
finite-path coverage. The runtime contains no overlap graph, A/T accelerators,
Presburger solver, or deleted historical cells. Explicit point inputs only.
"""
from __future__ import annotations
from dataclasses import dataclass
from model import (W, L10, DIR, Field, Segment, Point, add, mul, geometry,
                   inverse_history, first_period_mismatch, allowance)

STANDARD_HISTORIES = {
    (W*4)[i:i+149]: (W*4)[i+149:i+253] for i in range(104)
}
assert len(STANDARD_HISTORIES) == 104


@dataclass(frozen=True)
class Result:
    status: str  # EVENT, NO_FUTURE_DEFECT, UNKNOWN
    event_time: int | None
    head: Point
    heading: int
    field: Field
    ordinary_updates: int
    standard_plans: int
    elapsed: int
    tail: str | None = None


def next_defect(cells, head=(0, 0), heading=0, *, max_ordinary: int | None = None) -> Result:
    base = frozenset(cells)
    if type(heading) is not int or heading not in range(4):
        raise ValueError('heading must be 0..3')
    for p in (*base, head):
        if len(p) != 2 or any(type(a) is not int for a in p):
            raise ValueError('integer coordinates required')
    if max_ordinary is not None and (type(max_ordinary) is not int or max_ordinary < 0):
        raise ValueError('nonnegative resource cap required')
    hist = inverse_history(base, head, heading, 9)
    changes: set[Point] = set()
    segments: list[Segment] = []
    elapsed = ordinary = plans = 0
    bound = allowance(len(base)) + 1

    def snapshot():
        return Field(base, frozenset(changes), tuple(segments))
    def black(p):
        b = (p in base) ^ (p in changes)
        for s in segments:
            b ^= s.contains(p)
        return b
    def flip(p):
        if p in changes:
            changes.remove(p)
        else:
            changes.add(p)

    while True:
        if max_ordinary is not None and ordinary >= max_ordinary:
            return Result('UNKNOWN', None, head, heading, snapshot(), ordinary, plans, elapsed)
        ch = 'L' if black(head) else 'R'
        if hist[-9:]+ch not in L10:
            time = elapsed
            flip(head)
            heading = (heading+(1 if ch == 'R' else -1)) % 4
            head = add(head, DIR[heading])
            elapsed += 1
            ordinary += 1
            if ordinary > bound:
                raise AssertionError('proved ordinary-work bound exceeded')
            return Result('EVENT', time, head, heading, snapshot(), ordinary, plans, elapsed)

        # Use only histories containing at least 149 actual forward updates.
        word = STANDARD_HISTORIES.get(hist) if plans == 0 and elapsed >= 149 else None
        if word is not None:
            assert not segments
            source = base ^ changes
            mismatch = first_period_mismatch(source, head, heading, word)
            plans = 1
            if mismatch is None:
                return Result('NO_FUTURE_DEFECT', None, head, heading, snapshot(), ordinary,
                              plans, elapsed, word)
            qs, drift, hs, _ = geometry(word, heading)
            qs = [add(head, p) for p in qs]
            whole, partial = divmod(mismatch, 104)
            if whole:
                segments.extend(Segment(q, drift, whole) for q in qs)
            for i in range(partial):
                flip(add(qs[i], mul(whole, drift)))
            head = add(qs[partial], mul(whole, drift))
            heading = hs[partial]
            hist = ''.join(word[(mismatch-9+j) % 104] for j in range(9))
            elapsed += mismatch
            # At a nondefect mismatch the first literal update exits the W SCC.
            # No second W plan is attempted; silent-supply bounds the remainder.
            continue

        flip(head)
        heading = (heading+(1 if ch == 'R' else -1)) % 4
        head = add(head, DIR[heading])
        hist = (hist+ch)[-149:]
        elapsed += 1
        ordinary += 1
        if ordinary > bound:
            raise AssertionError('proved ordinary-work bound exceeded')
