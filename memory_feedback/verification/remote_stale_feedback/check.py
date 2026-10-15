"""Scoped, deterministic checks for the remote-stale-feedback proof package.

Finite checks support the written all-input proofs; they do not prove HC,
existence of a nonperiodic seed, or completeness of general negative certificates.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random

from feedback import (State, DIRS, step, inverse, replay, stale, prior_suffix,
    geometry, multiple, period_check, first_event, first_external_event,
    in_segment_halo, norm, sub, guard_side, escape_bound,
    event_deadline, density_index, external_count_lower, external_event_deadline,
    external_density_index)

ROOT = Path(__file__).resolve().parent


def ensure(condition, message='check failed'):
    if not condition:
        raise AssertionError(message)


def ref_trace(start: State, length: int, back: int = 0):
    """Independent complex-coordinate LR dynamics for small-coordinate checks."""
    black = {complex(*p) for p in start.black}
    p, v = complex(*start.pos), (1j, 1, -1j, -1)[start.heading]
    history = []
    pb, pp, vv = set(black), p, v
    for k in range(1, back+1):
        q = pp-vv
        was_R = q in pb
        pb.symmetric_difference_update((q,))
        vv *= 1j if was_R else -1j
        pp = q
        history.append((int(pp.real), int(pp.imag)))
    positions, letters, events, last = [], [], [], {}
    for k in range(back, 0, -1):
        last[history[k-1]] = -k
    for t in range(length):
        q = (int(p.real), int(p.imag))
        old = p in black
        positions.append(q)
        events.append((old, last.get(q)))
        last[q] = t
        letters.append('L' if old else 'R')
        black.symmetric_difference_update((p,))
        v *= 1j if old else -1j
        p += v
    endpoint = State(frozenset((int(q.real), int(q.imag)) for q in black),
                     (int(p.real), int(p.imag)), (1j, 1, -1j, -1).index(v))
    return endpoint, ''.join(letters), positions+[endpoint.pos], events


def hull(points):
    points = sorted(set(points))
    def cross(a, b, c):
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    lower, upper = [], []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1]+upper[:-1]


def inside_hull(p, vertices):
    return all((b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]) >= 0
               for a, b in zip(vertices, vertices[1:]+vertices[:1]))


def independent_word_seed(word: str, heading: int = 0):
    """Stable-order class criterion, independently of breakpoint parity.

    Returns the forced black boundary seed and rays for a realizable word.
    This is the attributed existing supplied-word criterion, not a new result.
    """
    points, h, d = geometry((0, 0), heading, word)
    ensure(h == heading and d != (0, 0))
    groups = []
    for i, p in enumerate(points):
        for anchor, entries in groups:
            a = multiple(sub(p, anchor), d)
            if a is not None:
                entries.append((i, a))
                break
        else:
            groups.append((p, [(i, 0)]))
    black = set()
    for anchor, entries in groups:
        ordered = sorted(entries, key=lambda z: z[0]-len(word)*z[1])
        ensure(all(word[i] == ('R' if k % 2 == 0 else 'L')
                   for k, (i, a) in enumerate(ordered)), 'word criterion')
        lo = min(a for i, a in entries)
        hi = max(a for i, a in entries)
        for n in range(lo, hi):
            available = [(i, a) for i, a in ordered if a <= n]
            if available and word[available[0][0]] == 'L':
                black.add((anchor[0]+n*d[0], anchor[1]+n*d[1]))
    return State(frozenset(black), (0, 0), heading), points, d


def main():
    rng = random.Random(20261015)
    result = {'schema': 'langtons-ant-remote-stale-feedback-v1',
              'base_commit': '0bcaad6ce318b79479f03e9c9d89cb3fcd4d4489',
              'scope': 'new analytic proofs and isolated deterministic controls; no HC decision'}
    seeds = [State(frozenset())]
    for i in range(15):
        b = frozenset((x, y) for x in range(-4, 5) for y in range(-4, 5)
                      if rng.randrange(5) == 0)
        seeds.append(State(b, (rng.randrange(-2, 3), rng.randrange(-2, 3)), i % 4))
    interval_count = point_count = reverse_count = filtered_count = external_macro_count = 0
    for start in seeds:
        actual, word, points = replay(start, 1200)
        reference, rword, rpoints, events = ref_trace(start, 1200, back=32)
        ensure((actual, word, points) == (reference, rword, rpoints), 'literal implementations')
        x = start
        for _ in range(32):
            y, a = step(x)
            z, b = inverse(y)
            ensure(x == z and a == b, 'inverse round trip')
            x = y
            reverse_count += 1
        for D in (1, 2, 4, 8, 16, 32):
            Q, previous = 1 << D, 0
            times = [t for t, (black, last) in enumerate(events)
                     if black and (last is None or t-last > D)]
            for t in times:
                p, q = points[previous], points[t]
                ensure(t+1-previous <= Q*norm(sub(q, p))+5*Q*Q,
                       'endpoint-sensitive duration')
                for z in points[previous:t+2]:
                    ensure(in_segment_halo(z, p, q, 3*Q+1), 'endpoint tube')
                    point_count += 1
                previous = t+1
                interval_count += 1
            K = frozenset((x, y) for x in range(-2, 3) for y in range(-2, 3))
            expected = next((t for t in times if points[t] not in K), None)
            # Only compare when the independent prefix contains a genuine answer.
            if expected is not None:
                answer = first_external_event(start, D, K, max_events=1000,
                    max_literal_updates=5000, max_suffix_states=5000)
                ensure(answer['kind'] == 'EXTERNAL_EVENT', 'filtered result kind')
                ensure(answer['time'] == expected and tuple(answer['point']) == points[expected],
                       'first exterior event')
                filtered_count += 1
            if D <= 8:
                here, offset = start, 0
                b = escape_bound(guard_side(K, D))
                outer = [t for t in times if points[t] not in K][:6]
                for t in outer:
                    augmented = here.black | K | {here.pos}
                    W = max(max(p[i] for p in augmented)-min(p[i] for p in augmented)
                            for i in range(2))
                    expanded = hull((p[0]+dx, p[1]+dy) for p in augmented
                                    for dx in (-9*Q, 9*Q) for dy in (-9*Q, 9*Q))
                    end, _, path = replay(here, t+1-offset)
                    ensure(all(inside_hull(p, expanded) for p in path), 'external macro path halo')
                    ensure(all(inside_hull(p, expanded) for p in end.black), 'complete-field halo')
                    ensure(t+1-offset <= 2*Q*W+20*Q*Q+b, 'external macro duration')
                    here, offset = end, t+1
                    external_macro_count += 1
    result['finite_controls'] = {'seeds': len(seeds), 'updates_per_seed': 1200,
        'inverse_round_trips': reverse_count, 'endpoint_intervals': interval_count,
        'segment_memberships': point_count, 'filtered_first_events': filtered_count,
        'complete_field_external_macros': external_macro_count}

    # Test the geometric step of the analytic proof at enormous epoch counts.
    plan_count = extreme_count = 0
    for _ in range(2500):
        P = rng.randrange(1, 41)
        word = ''.join(rng.choice('RL') for _ in range(P))
        offsets, h, d = geometry((0, 0), 0, word)
        if h or d == (0, 0):
            continue
        j = rng.randrange(15)
        prefix = ''.join(rng.choice('RL') for _ in range(j))
        if j:
            pp, ph, pd = geometry((0, 0), 0, prefix)
            a = pd
        else:
            a, ph = (0, 0), 0
        placed, hh, drift = geometry(a, ph, word)
        k, phase = 10**50+rng.randrange(100), rng.randrange(P)
        endpoint = (placed[phase][0]+k*drift[0], placed[phase][1]+k*drift[1])
        for i, z in enumerate(placed):
            last_epoch = k if i <= phase else k-1
            for epoch in (0, last_epoch):
                point = z[0]+epoch*drift[0], z[1]+epoch*drift[1]
                ensure(in_segment_halo(point, (0, 0), endpoint, j+2*P), 'plan extreme')
                extreme_count += 1
        plan_count += 1
    result['geometric_plans'] = {'nonzero_translators': plan_count,
        'phase_segment_extremes': extreme_count, 'epoch_scale': '10^50',
        'claim': 'motion-plan geometry only; these random words need not be realizable'}

    # Positive period and complete-field checks use two different infinite tests.
    blank = State(frozenset())
    tail, _, _ = replay(blank, 12000)
    period = replay(tail, 104)[1]
    certificate = period_check(tail, period)
    ensure(certificate['valid'] and len(period) == 104)
    clean, offsets, drift = independent_word_seed(period, tail.heading)
    placed_clean = {(p[0]+tail.pos[0], p[1]+tail.pos[1]) for p in clean.black}
    ensure(placed_clean <= tail.black)
    for q in tail.black-placed_clean:
        ensure(not any((k := multiple(sub(q, (p[0]+tail.pos[0], p[1]+tail.pos[1])), drift))
                       is not None and k >= 0 for p in offsets), 'retained archive guard')
    ensure(first_event(tail, 128, 2000)['kind'] == 'FREE')
    K = frozenset((x, y) for x in range(-64, 65) for y in range(-64, 65))
    no_outside = first_external_event(blank, 128, K, max_events=2000,
                                    max_literal_updates=20000, max_suffix_states=2000)
    ensure(no_outside['kind'] == 'NO_EXTERNAL_EVENT')
    ref_end, ref_word, ref_points, ref_events = ref_trace(blank, 12000, back=128)
    ref_times = [t for t, (b, last) in enumerate(ref_events)
                 if b and (last is None or t-last > 128)]
    ensure(len(ref_times) == no_outside['inside_events'])
    ensure(ref_times[-1]+1 == no_outside['literal_updates'])
    ensure(all(ref_points[t] in K for t in ref_times))
    result['blank_filtered_no'] = {k: no_outside[k] for k in
        ('kind', 'D', 'inside_events', 'literal_updates', 'full_endpoint_black_count')}
    result['standard_control'] = {'period': period, 'black_reads_per_period': period.count('L'),
        'drift': list(drift), 'full_black_count': len(tail.black),
        'clean_black_count': len(clean.black), 'parity_checks': certificate['checks']}

    # One initial blocker 10^60 epochs ahead must not be lost as "distant debris".
    k = 10**60
    marker = tail.pos[0]+k*drift[0], tail.pos[1]+k*drift[1]
    ensure(marker not in tail.black)
    placed, _, _ = geometry(tail.pos, tail.heading, period)
    offsets_time = [i-104*a for i, q in enumerate(placed)
                    if (a := multiple(sub(q, tail.pos), drift)) is not None]
    expected = 104*k+min(offsets_time)
    perturbed = State(tail.black | {marker}, tail.pos, tail.heading)
    far = first_external_event(perturbed, 128, frozenset({tail.pos}), max_events=20,
                              max_literal_updates=1000, max_suffix_states=2000)
    ensure(far['kind'] == 'EXTERNAL_EVENT' and far['time'] == expected)
    ensure(tuple(far['point']) == marker and far['literal_updates'] == 0)
    off_ray = (10**60, -(10**60))
    ensure(not any((a := multiple(sub(off_ray, p), drift)) is not None and a >= 0
                   for p in placed))
    inert = first_external_event(State(tail.black | {off_ray}, tail.pos, tail.heading),
                                128, frozenset({tail.pos}), max_suffix_states=2000)
    ensure(inert['kind'] == 'NO_EXTERNAL_EVENT')
    result['remote_controls'] = {'blocker': list(marker), 'first_event_time': str(expected),
        'literal_inside_replay_updates': far['literal_updates'],
        'off_trace_marker_retained': True}

    # A moving zero-radius observation region does NOT satisfy the fixed-K theorem.
    ensure(period.count('L') > 0)
    ensure(norm((k*drift[0], k*drift[1])) > 3*(1 << 128)+2)
    result['scope_countercontrols'] = {
        'moving_region': 'K_t={p_t}; every S_1 of certified P104 is inside, infinitely often',
        'event_free_tail': 'certified P104 with D=128 escapes the fixed source halo',
        'NO_means': 'no external stale event, never a negative HIGHWAY answer'}

    # Existing all-length two-sweep witness: tests the failed fuel/nesting ideas.
    lifetime_cases, selected_lifetimes = 0, 0
    for L in range(1, 33):
        bottom = {(x, -1) for x in range(2*L)}
        top = {(x, 4) for x in range(2*L)}
        right = {(2*L, 0), (2*L+1, 1), (2*L+1, 2), (2*L, 3)}
        left = {(-1, 3), (-2, 2), (-2, 1), (-1, 0)}
        start = State(frozenset(bottom | top | right | left), (0, 0), 1)
        end, word, pos, ev = ref_trace(start, 12*L+12, back=0)
        ensure(word == 'RLLR'*L+'LRLLRL'+'RLLR'*L+'LRLLRL'+'LRRL'*L)
        cap = {(-1, 1), (-1, 2), (2*L, 1), (2*L, 2)}
        expected_black = {(x, y) for x in range(2*L) for y in (1, 3)} | cap
        ensure(end == State(frozenset(expected_black), (2*L, 0), 1))
        for x in range(2*L):
            b = 4*(x//2)+(3 if x % 2 else 0)
            e = b+8*L+12
            ensure(pos[b] == pos[e] == (x, 0) and word[b] == 'R' and word[e] == 'L')
            ensure(ev[e][1] == b)
            selected_lifetimes += 1
        lifetime_cases += 1
    result['retained_protocol_replay'] = {'L_values': lifetime_cases,
        'verified_created_consumed_lifetimes': selected_lifetimes,
        'conclusion': 'finite protocols only; no renewable interface or infinite seed'}

    count_checks = inversion_checks = validation_checks = 0
    for b in range(6):
        for length in range(13):
            for bits in itertools.product((0, 1), repeat=length):
                runs = ''.join(map(str, bits)).split('1')
                if max(map(len, runs), default=0) <= b:
                    ensure(sum(bits) >= external_count_lower(length, b))
                    count_checks += 1
    for D in range(1, 8):
        for W in (0, 1, 10, 100):
            for n in range(1, 51):
                t = event_deadline(D, n, W)
                ensure(density_index(D, W, t) == n)
                ensure(density_index(D, W, t-1) == n-1)
                inversion_checks += 2
    external_inversion_checks = 0
    for D in (1, 2, 4, 8):
        for W in (0, 10, 100):
            for b in (0, 100, 10**30):
                for n in range(1, 31):
                    t = external_event_deadline(D, n, W, b)
                    ensure(external_density_index(D, W, b, t) == n)
                    ensure(external_density_index(D, W, b, t-1) == n-1)
                    # Exact telescoping of 9Q spatial halos and the per-macro time.
                    Q = 1 << D
                    ensure(t == sum(2*Q*(W+18*Q*i)+20*Q*Q+b for i in range(n)))
                    external_inversion_checks += 2
    for kwargs in ({'max_events': 0}, {'max_literal_updates': 0}, {'max_suffix_states': 0}):
        x = State(frozenset({(0, 0)}))
        answer = first_external_event(x, 1, frozenset({(0, 0)}), **kwargs)
        ensure(answer['kind'] == 'INCONCLUSIVE', 'cap must not return NO')
        validation_checks += 1
    for d in (0, -1, True):
        try:
            first_external_event(blank, d, frozenset())
        except ValueError:
            validation_checks += 1
        else:
            raise AssertionError('invalid D accepted')
    empty = first_external_event(tail, 1, frozenset(), max_suffix_states=2000)
    ensure(empty['kind'] == 'EXTERNAL_EVENT')
    result['arithmetic_controls'] = {'burst_strings': count_checks,
        'deadline_inverse_boundaries': inversion_checks,
        'external_deadline_inverse_boundaries': external_inversion_checks,
        'resource_and_validation_controls': validation_checks,
        'empty_region_control': True}
    result['sources_sha256'] = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                for name in ('feedback.py', 'check.py')}
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'check_results.json')
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2), flush=True)


if __name__ == '__main__':
    main()
