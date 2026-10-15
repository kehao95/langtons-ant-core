"""Exact local finite-state observations through recency-predicted LR macros.

Observers are explicit finite tables, not arbitrary Python decoders. All samples
are PRE-update. HALT has priority over a stale read at the same time. Event
outputs include the full post-update colouring AND the updated observer state.
No total algorithm over infinitely many stale events is asserted.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import lcm
from symbolic_stale import (
    Point, SymbolicState, add, sub, multiple, geometry, ray_segment_epochs,
    preceding_turns, suffix_predict, step, verify_period, apply_periodic_prefix,
)


@dataclass(frozen=True)
class Observer:
    offsets: tuple[Point, ...]
    # Column heading*2**len(offsets)+bitmap; -1 means emit HALT.
    table: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        if not self.table:
            raise ValueError('observer needs at least one state')
        if any(len(v) != 2 or any(type(c) is not int for c in v) for v in self.offsets):
            raise ValueError('integer two-coordinate offsets required')
        if len(set(self.offsets)) != len(self.offsets):
            raise ValueError('duplicate offsets')
        alphabet = 4 * (1 << len(self.offsets))
        if any(len(row) != alphabet for row in self.table):
            raise ValueError('one transition for every heading and bitmap required')
        if any(type(v) is not int or not -1 <= v < len(self.table)
               for row in self.table for v in row):
            raise ValueError('transition must be -1 or a valid state')

    def symbol(self, x: SymbolicState) -> int:
        bitmap = sum(int(x.black(add(x.pos, v))) << j
                     for j, v in enumerate(self.offsets))
        return (x.heading << len(self.offsets)) | bitmap

    @property
    def radius(self) -> int:
        return max((max(abs(a), abs(b)) for a, b in self.offsets), default=0)


class SearchLimit(Exception):
    pass


def _feed_repeated(o: Observer, state: int, block: list[int], repeats: int | None,
                   stats: dict) -> tuple[int | None, int]:
    """First HALT offset and state; None repeats means infinitely many copies.

    Inspect at most one transient/cycle of observer states at block boundaries.
    A skipped boundary cycle has already been checked for intermediate HALT.
    """
    if not block:
        raise ValueError('nonempty block required')
    seen = {}
    k = 0
    while repeats is None or k < repeats:
        if state in seen:
            if repeats is None:
                return None, state
            cycle = k - seen[state]
            skip = (repeats - k) // cycle
            if skip:
                stats['blocks_skipped'] += skip * cycle
                k += skip * cycle
                if k == repeats:
                    break
            seen.clear()
        seen[state] = k
        for j, symbol in enumerate(block):
            stats['transition_evaluations'] += 1
            nxt = o.table[state][symbol]
            if nxt == -1:
                return k * len(block) + j, state
            state = nxt
        k += 1
    return None, state


def scan_prescribed_observations(x: SymbolicState, word: str, o: Observer,
                                 state: int, count: int | None, stats: dict,
                                 max_symbols: int | None = None) -> tuple[int | None, int]:
    """Compute observations of a prescribed translating write path.

    Like apply_periodic_prefix, this helper does NOT certify that the path follows
    the LR read rule. The public solver certifies it through the final sampled
    pre-state before calling. count is the number of pre-update observations.
    """
    if count is not None and (type(count) is not int or count < 0):
        raise ValueError('nonnegative sample count required')
    if count == 0:
        return None, state
    ps, hs, heading, drift = geometry(x, word)
    if heading != x.heading or drift == (0, 0):
        raise ValueError('nonzero translating period required')
    P = len(word)
    specs = []
    breaks = {0}
    for i, p in enumerate(ps):
        phase = []
        for v in o.offsets:
            z = add(p, v)
            thresholds = []
            for j, q in enumerate(ps):
                r = multiple(sub(q, z), drift)
                if r is not None and r >= 0 and (r > 0 or j < i):
                    thresholds.append(r)
            aps = [a for seg in x.terms
                   if (a := ray_segment_epochs(z, drift, seg)) is not None]
            breaks.update(thresholds)
            for lo, hi, _, _ in aps:
                breaks.update((lo, hi + 1))
            phase.append((thresholds, aps))
        specs.append(phase)
    cuts = sorted(breaks)
    for index, lo in enumerate(cuts):
        base = lo * P
        if count is not None and base >= count:
            break
        end = cuts[index + 1] * P if index + 1 < len(cuts) else None
        if count is not None:
            end = count if end is None else min(end, count)
        length = None if end is None else end - base
        active_specs = []
        modulus = 1
        for phase in specs:
            active_phase = []
            for thresholds, aps in phase:
                active = [a for a in aps if a[0] <= lo <= a[1]]
                parity = sum(r <= lo for r in thresholds) % 2
                for a in active:
                    modulus = lcm(modulus, a[3])
                active_phase.append((parity, active))
            active_specs.append(active_phase)
        epochs = modulus if length is None else min(modulus, (length + P - 1) // P)
        block_length = epochs * P
        if max_symbols is not None and stats['symbols_built'] + block_length > max_symbols:
            raise SearchLimit('caller observation-symbol cap')
        block = []
        for k in range(lo, lo + epochs):
            for i, phase in enumerate(active_specs):
                bitmap = 0
                for j, (parity, aps) in enumerate(phase):
                    bit = (parity + sum(k % a[3] == a[2] for a in aps)) % 2
                    bitmap |= bit << j
                block.append((hs[i] << len(o.offsets)) | bitmap)
        stats['symbols_built'] += len(block)
        stats['epoch_intervals'] += 1
        if length is None:
            hit, state = _feed_repeated(o, state, block, None, stats)
            return (None if hit is None else base + hit), state
        repeats, remainder = divmod(length, len(block))
        hit, state = _feed_repeated(o, state, block, repeats, stats)
        if hit is not None:
            return base + hit, state
        if remainder:
            hit, state = _feed_repeated(o, state, block[:remainder], 1, stats)
            if hit is not None:
                return base + repeats * len(block) + hit, state
    return None, state


def next_observed_macro(x: SymbolicState, D: int, o: Observer, observer_state: int = 0,
                        max_suffix_states: int | None = None,
                        max_residue_checks: int | None = None,
                        max_symbols: int | None = None) -> dict:
    """Total per call: first HALT, next complete stale event, or permanent no-HALT.

    Optional caller caps return INCONCLUSIVE, never a negative verdict. The
    observer cannot change the physical rule and cannot inspect an unbounded field.
    """
    if type(D) is not int or D < 1:
        raise ValueError('positive integer D required')
    if type(observer_state) is not int or observer_state not in range(len(o.table)):
        raise ValueError('invalid observer state')
    for cap in (max_suffix_states, max_residue_checks, max_symbols):
        if cap is not None and (type(cap) is not int or cap < 0):
            raise ValueError('caps must be nonnegative integers')
    stats = dict(explicit_updates=0, symbols_built=0, transition_evaluations=0,
                 epoch_intervals=0, blocks_skipped=0)
    state = observer_state
    elapsed = 0
    w = preceding_turns(x, D)
    seen = {}
    turns = []

    def sample(y, t):
        nonlocal state
        stats['transition_evaluations'] += 1
        nxt = o.table[state][o.symbol(y)]
        if nxt == -1:
            return dict(kind='halt', time=t, state=y, observer_state=state, stats=stats)
        state = nxt
        return None

    def event(y, t, **evidence):
        after, ch = step(y)
        stats['explicit_updates'] += 1
        if ch != 'L':
            raise AssertionError('stale event must read black')
        return dict(kind='stale_read', event_time=t, duration=t + 1,
                    before=y, after=after, observer_state=state, stats=stats, **evidence)

    while w not in seen:
        if max_suffix_states is not None and len(seen) >= max_suffix_states:
            return dict(kind='inconclusive', reason='caller suffix cap', stats=stats)
        if (halt := sample(x, elapsed)) is not None:
            return halt
        actual = 'L' if x.black(x.pos) else 'R'
        if actual != suffix_predict(w):
            return event(x, elapsed)
        seen[w] = elapsed
        turns.append(actual)
        x, _ = step(x)
        stats['explicit_updates'] += 1
        elapsed += 1
        w = w[1:] + actual
    cycle = ''.join(turns[seen[w]:])
    _, _, heading, drift = geometry(x, cycle)
    rotation = (heading - x.heading) % 4
    if rotation or drift == (0, 0):
        block = cycle * (2 if rotation == 2 else (4 if rotation else 1))
        for j in range(2 * len(block)):
            if (halt := sample(x, elapsed + j)) is not None:
                return halt
            if ('L' if x.black(x.pos) else 'R') != block[j % len(block)]:
                return event(x, elapsed + j)
            x, _ = step(x)
            stats['explicit_updates'] += 1
        raise AssertionError('a bounded infinite LR orbit would result')
    certificate = verify_period(x, cycle, max_residue_checks)
    if certificate['kind'] == 'inconclusive':
        return dict(kind='inconclusive', reason=certificate['reason'], stats=stats)
    bad = certificate['first_bad_offset']
    # At bad the earlier prescribed updates are valid, so its PRE-update sample
    # is still valid. Only the turn at bad is wrong; HALT gets priority over it.
    count = None if bad is None else bad + 1
    try:
        hit, state = scan_prescribed_observations(x, cycle, o, state, count, stats, max_symbols)
    except SearchLimit as exc:
        return dict(kind='inconclusive', reason=str(exc), stats=stats)
    if hit is not None:
        y = apply_periodic_prefix(x, cycle, hit)
        return dict(kind='halt', time=elapsed + hit, state=y, observer_state=state,
                    cycle=cycle, period_entry=elapsed, certificate=certificate, stats=stats)
    if bad is None:
        return dict(kind='permanent_no_halt', entry=elapsed, state=x,
                    observer_cycle_state=state, cycle=cycle, certificate=certificate, stats=stats)
    y = apply_periodic_prefix(x, cycle, bad)
    if cycle[bad % len(cycle)] != 'R':
        raise AssertionError('recency mismatch must predict right')
    return event(y, elapsed + bad, cycle=cycle, certificate=certificate)


def observed_event_budget(x: SymbolicState, D: int, o: Observer, n: int,
                          observer_state: int = 0, **limits) -> dict:
    """Decide HALT with at most n stale reads STRICTLY BEFORE its pre-state.

    A budget result is NO only to this bounded-event question, not global NO-HALT.
    HALT at the next stale-read pre-state is checked before that event is counted.
    """
    if type(n) is not int or n < 0:
        raise ValueError('nonnegative event budget required')
    time = 0
    state = observer_state
    for consumed in range(n + 1):
        result = next_observed_macro(x, D, o, state, **limits)
        if result['kind'] == 'halt':
            return dict(kind='halt', time=time + result['time'], consumed=consumed,
                        terminal=result)
        if result['kind'] != 'stale_read':
            return dict(kind=result['kind'], elapsed=time, consumed=consumed, terminal=result)
        time += result['duration']
        x = result['after']
        state = result['observer_state']
    return dict(kind='budget_exhausted', elapsed=time, consumed=n + 1,
                state=x, observer_state=state, global_no_halt=False)


def first_trigger_deadline(x: SymbolicState, D: int, o: Observer) -> int:
    """Safe waiting bound; use the exact sparse radius or this expression upper bound."""
    if type(D) is not int or D < 1:
        raise ValueError('positive integer D required')
    Q = 1 << D
    return Q * (x.radius_upper() + 2 * Q + o.radius + len(o.table) + 10)
