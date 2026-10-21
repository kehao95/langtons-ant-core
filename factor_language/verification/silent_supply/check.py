"""Theorem-local deterministic replay; no unrestricted HC conclusion."""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
import argparse
import hashlib
import json
from pathlib import Path
import random
import subprocess
import tempfile
import time

import graph
from model import (A, B, T, W, DIR, F, L10, WORD_HASH, Field, Segment, add, mul,
                   geometry, multiple, minimal_seed, literal, defect_count,
                   first_period_mismatch, allowance, RETURN_INTERCEPT)
from one_jump import next_defect

ROOT = Path(__file__).resolve().parent


def stable_first_left(word):
    points, d, _, h = geometry(word)
    assert h == 0 and d != (0, 0)
    stable = []
    for i, (p, ch) in enumerate(zip(points, word)):
        if ch != 'L':
            continue
        earlier = []
        for j, q in enumerate(points):
            s = multiple((q[0]-p[0], q[1]-p[1]), d)
            if s is not None and (s > 0 or (s == 0 and j < i)):
                earlier.append(s)
        if not earlier:
            stable.append(i)
    return stable


def phase_checks():
    phase_table = []
    prefix_checks = 0
    width_checks = 0
    for name, basis, supply in [('T', T, 2), ('A', A, 5), ('W', W, 0)]:
        for phase in range(len(basis)):
            word = basis[phase:]+basis[:phase]
            stable = stable_first_left(word)
            assert len(stable) == supply
            for heading in range(4):
                points, d, _, h = geometry(word, heading)
                assert h == heading
                if name == 'W':
                    assert abs(d[0]) == abs(d[1]) == 2
                    n = (1, -1) if d[0]*d[1] > 0 else (1, 1)
                    width = 11
                else:
                    assert (d[0] == 0) != (d[1] == 0)
                    n = (1, 0) if d[0] == 0 else (0, 1)
                    width = 4
                z = [p[0]*n[0]+p[1]*n[1] for p in points]
                assert max(z)-min(z)+1 == width
                width_checks += 1
            if name != 'W':
                assert word.count('R')-word.count('L') == 4
                for k in (0, 1, 2, 5, 12, 31):
                    seed = minimal_seed(word*k)
                    assert seed is not None and len(seed) >= supply*k
                    prefix_checks += 1
                phase_table.append(dict(mode=name, phase=phase, permanent_first_L_phases=stable))
    # Exact per-cell identity for the auxiliary XOR cofactor. No physical
    # evolution is assumed for that cofactor on its own.
    shadow_checks = 0
    for r in (0, 1):
        for d in (0, 1):
            for z in (0, 1):
                correction = ((r ^ z)-r)-(((r ^ d) ^ z)-(r ^ d))
                assert abs(correction) <= 2*(d & z)
                if not (d & z):
                    assert correction == 0
                shadow_checks += 1
    return dict(phase_supply_table=phase_table, phase_orientation_width_checks=width_checks,
                finite_supply_controls=prefix_checks, shadow_bit_identities=shadow_checks,
                transverse_overlap_bound=44, uncorrected_cofactor_balance_rejected=True)


def inherited_fold_facts():
    # Finite premises of the imported all-parameter three-fold argument.
    aps, ad, _, ah = geometry(A)
    bps, bd, _, bh = geometry(B)
    column = [(i, p[1], A[i]) for i, p in enumerate(aps) if p[0] == 0]
    assert column == [(0, 0, 'L'), (7, -1, 'R'), (8, -2, 'R'),
                      (15, -3, 'L'), (16, -2, 'L'), (27, -5, 'L')]
    assert min(p[0] for p in aps) == -3 and max(p[0] for p in aps) == 0
    assert ad == (0, -4) and ah == 0 and bd == (1, 11) and bh == 2
    expected = {(0, 2): [(32, 'R')], (1, 9): [(82, 'R'), (90, 'L')],
                (1, 4): [(45, 'L'), (53, 'R')], (1, 8): [(73, 'L'), (81, 'R')],
                (1, 0): [(1, 'R'), (5, 'L'), (17, 'R')]}
    for p, visits in expected.items():
        assert [(i, B[i]) for i, q in enumerate(bps) if p == q] == visits
    assert max(p[1] for p in bps if p[0] == 0) == 2
    assert max(p[1] for p in bps if p[0] == 1) == 12
    return dict(A_axis_column=column, B_named_cells_checked=len(expected),
                all_parameter_proof='inherited; reproduced analytically in the proof appendix')


def arithmetic_checks():
    # q=m+F. k_T<=q/2; 5*k_i<=3*q+4*S_(i-1)+88*(i-1)+44.
    slope = Fraction(0)
    intercept = Fraction(0)
    stages = []
    for i in range(1, 4):
        slope = Fraction(9, 5)*slope+Fraction(3, 5)
        intercept = Fraction(9, 5)*intercept+Fraction(88*(i-1)+44, 5)
        stages.append([str(slope), str(intercept)])
    assert slope == Fraction(453, 125) and intercept == Fraction(15004, 125)
    coefficient = 12+28*slope
    constant = F*(coefficient+1)+28*intercept
    assert coefficient == Fraction(14184, 125)
    assert constant == Fraction(3867322, 25)
    assert coefficient <= 114 and constant <= 154693
    assert 52*F+154693 == RETURN_INTERCEPT
    # Independent finite evaluations are controls for the written symbolic algebra.
    trials = 0
    for m in (0, 1, 3, 20, 100, 10**12):
        q = m+F
        kt = q//2
        total = 0
        for i in range(1, 4):
            ki = (3*q+4*total+88*(i-1)+44)//5
            total += ki
        outside = F+24*kt+28*total
        assert outside <= allowance(m)
        trials += 1
    return dict(A_prefix_sum_bounds=stages, outside_core_mass_coefficient=str(coefficient),
                outside_core_constant=str(constant), outside_core_rounded='114*m+154693',
                return_bound='52*displacement_inf+114*m+223437',
                exact_arithmetic_controls=trials)


def check_word(word, data):
    assert defect_count(word) == 0
    seed = minimal_seed(word)
    assert seed is not None
    decomposition = graph.parse(word, data)
    L = len(word)
    outside = L-decomposition['core_length']
    assert outside <= allowance(len(seed))
    _, d, _, _ = geometry(word)
    assert L <= 52*max(map(abs, d))+114*len(seed)+RETURN_INTERCEPT
    k = decomposition['core_length']
    if k:
        a = decomposition['core_start']
        unit = word[a:a+104]
        assert unit in {W[i:]+W[:i] for i in range(104)}
        assert word[a:a+k] == unit*(k//104)
    return decomposition


def word_controls(data):
    tested = updates = 0
    max_length = 0
    for basis in (T, A, W):
        for phase in range(len(basis)):
            w = basis[phase:]+basis[:phase]
            for k in (1, 3, 11):
                check_word(w*k, data)
                tested += 1
                updates += len(w)*k
    C = 'RLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLL'
    D = 'LLRRRRLRRLRRRRLLLLRLRRRRLRL'
    folds = []
    for n in (0, 1, 2, 5, 20, 100, 1000, 4000):
        w = C+A*(n+6)+B+A*(n+2)+D
        seed = minimal_seed(w)
        assert seed is not None and len(seed) == 10*n+76
        decomp = check_word(w, data)
        assert decomp['core_length'] == 0
        got = literal(seed, len(w))
        assert got[3] == w and got[1] == (-1, 0)
        folds.append(dict(n=n, length=len(w), initial_black=len(seed), outside_core=len(w)))
        tested += 1
        updates += len(w)
        max_length = max(max_length, len(w))
    for n, m in ((1, 0), (2, 0), (2, 1), (5, 4), (12, 6), (80, 79)):
        w = B+A*n+B+A*m
        decomp = check_word(w, data)
        assert decomp['core_length'] == 0
        assert len(minimal_seed(w)) == 5*n+5*m+47
        tested += 1
        updates += len(w)
    Z = ('RRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR'
         'RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLL')
    assert len(Z) == 104
    for n in (0, 1, 4, 20):
        for k in (0, 1, 5, 100):
            w = T*n+Z*k
            check_word(w, data)
            tested += 1
            updates += len(w)
    rng = random.Random(20261020)
    random_segments = 0
    for _ in range(32):
        seed = {(rng.randrange(-5, 6), rng.randrange(-5, 6)) for _ in range(rng.randrange(25))}
        _, _, _, word, _ = literal(seed, 2000, heading=rng.randrange(4))
        start = 0
        for j in range(9, len(word)):
            if word[j-9:j+1] not in L10:
                check_word(word[start:j], data)
                random_segments += 1
                start = j+1
        check_word(word[start:], data)
        random_segments += 1
    return dict(structured_words=tested, structured_letter_controls=updates,
                longest_fold_length=max_length, folded_family=folds,
                random_complete_inputs=32, random_literal_updates=64000,
                random_silent_segments=random_segments)


def scope_controls():
    # Inherited twenty-black circuit, used only as a finite silence-negative control.
    n = 400
    port = {(0, -1), (1, 1), (1, 3), (2, 2)}
    starts = [((0, 0), 1), ((n-1, n), 0), ((-n, 3*n-4), 3),
              ((-5*n+5, -n), 2), ((-3*n, -3*n+8), 1)]
    seed = set()
    for p, h in starts:
        for xx, yy in port:
            for _ in range((h-1) % 4):
                xx, yy = yy, -xx
            seed.add((p[0]+xx, p[1]+yy))
    assert len(seed) == 20
    length = 624*n-1516
    _, end, _, word, _ = literal(seed, length, heading=1)
    assert end == (0, 2)
    proposed = 52*max(map(abs, end))+114*len(seed)+RETURN_INTERCEPT
    assert length > proposed and defect_count(word) > 0
    # A real ten-legal return also disproves a mass-free use of our constants.
    C = 'RLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLL'
    D = 'LLRRRRLRRLRRRRLLLLRLRRRRLRL'
    w = C+A*4006+B+A*4002+D
    assert geometry(w[:-1])[1] == (0, 0) and defect_count(w[:-1]) == 0
    assert len(w)-1 > RETURN_INTERCEPT
    return dict(defect_containing_circuit=dict(initial_black=20, length=length,
                                              endpoint=end, contained_defects=defect_count(word),
                                              violates_unconditional_return_bound=True),
                mass_free_bound_rejected_by_silent_return=len(w)-1)


def independent_next(cells, head=(0, 0), heading=0, cap=150000):
    """Separately written complex-vector dynamics, including inverse history."""
    if any(max(map(abs, q))+cap >= 2**50 for q in (*cells, head)):
        raise ValueError('complex-vector control is restricted to exactly representable finite coordinates')
    black = {complex(*p) for p in cells}
    p = complex(*head)
    direction = (1j, 1, -1j, -1)[heading]
    past_black = set(black)
    q, d = p, direction
    backwards = []
    for _ in range(9):
        q -= d
        ch = 'R' if q in past_black else 'L'
        if q in past_black:
            past_black.remove(q)
        else:
            past_black.add(q)
        d *= 1j if ch == 'R' else -1j
        backwards.append(ch)
    hist = ''.join(reversed(backwards))
    word = []
    for t in range(cap):
        ch = 'L' if p in black else 'R'
        event = hist[-9:]+ch not in L10
        if p in black:
            black.remove(p)
        else:
            black.add(p)
        direction *= -1j if ch == 'R' else 1j
        p += direction
        word.append(ch)
        if event:
            return (t, frozenset((int(z.real), int(z.imag)) for z in black),
                    (int(p.real), int(p.imag)), (1j, 1, -1j, -1).index(direction), ''.join(word))
        hist = (hist+ch)[-9:]
    return None


def xor_normal_form(field, drift):
    """Exact whole-field equality for finite segments parallel to this drift.

    Independent of the phase-ray event checker. Endpoints are swept in full
    translation classes, so enormous segment lengths are not expanded.
    """
    a = 0 if drift[0] else 1
    changes = defaultdict(set)
    def add_interval(p, v, length):
        scale = 0 if v == (0, 0) else multiple(v, drift)
        assert scale in (0, 1, -1)
        k = p[a]//drift[a]
        key = (p[0]-k*drift[0], p[1]-k*drift[1])
        lo, hi = sorted((k, k+scale*(length-1)))
        for endpoint in (lo, hi+1):
            if endpoint in changes[key]:
                changes[key].remove(endpoint)
            else:
                changes[key].add(endpoint)
    for p in field.base ^ field.changes:
        add_interval(p, (0, 0), 1)
    for s in field.segments:
        add_interval(s.start, s.stride, s.length)
    return {k: tuple(sorted(v)) for k, v in changes.items() if v}


def event_controls(data):
    clean = minimal_seed(W*10)
    assert clean is not None and first_period_mismatch(clean, (0, 0), 0, W) is None
    mature, p, h, _, _ = literal(clean, 3*104)
    base_qs, drift, hs, _ = geometry(W, h)
    qs = [add(p, q) for q in base_qs]
    cases = []
    # Unread, distant perturbations leave the original nine-turn history intact.
    for i in range(104):
        q = add(qs[i], mul(12, drift))
        cases.append((mature ^ {q}, p, h, 'marker'))
    C = 'RLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLL'
    D = 'LLRRRRLRRLRRRRLLLLRLRRRRLRL'
    for n in (0, 1, 2, 5, 20, 100):
        w = C+A*(n+6)+B+A*(n+2)+D
        seed = minimal_seed(w)
        out, q, hh, _, _ = literal(seed, 9)
        cases.append((out, q, hh, 'silent_fold'))
    rng = random.Random(43044)
    for _ in range(64):
        seed = frozenset((rng.randrange(-8, 9), rng.randrange(-8, 9)) for _ in range(rng.randrange(30)))
        cases.append((seed, (0, 0), rng.randrange(4), 'random'))
    ordinary_max = total_literal = complete = nontrivial_suffix = 0
    for seed, start, heading, kind in cases:
        result = next_defect(seed, start, heading)
        direct = independent_next(seed, start, heading)
        assert direct is not None and result.status == 'EVENT'
        t, endpoint, pos, hh, word = direct
        assert result.event_time == t and result.elapsed == t+1
        assert result.head == pos and result.heading == hh
        assert result.field.expand() == endpoint
        event_position = add(pos, mul(-1, DIR[hh]))
        radius = max(abs(event_position[a]-start[a]) for a in (0, 1))
        assert t <= 52*radius+114*len(seed)+RETURN_INTERCEPT
        assert result.standard_plans <= 1 and result.ordinary_updates <= allowance(len(seed))+1
        if result.standard_plans and result.ordinary_updates > 150:
            nontrivial_suffix += 1
        check_word(word[:-1], data)
        total_literal += len(word)
        complete += 1
        ordinary_max = max(ordinary_max, result.ordinary_updates)
    # Exact permanent absence on a complete mature source and with unread debris.
    no_events = 0
    for seed in (mature, mature | {(10**60, -3*10**60)}):
        result = next_defect(seed, p, h)
        assert result.status == 'NO_FUTURE_DEFECT' and result.standard_plans == 1
        final, pos, hh, _, _ = literal(seed, result.elapsed, p, h)
        assert result.field.expand() == final and result.head == pos and result.heading == hh
        assert first_period_mismatch(final, pos, hh, result.tail) is None
        no_events += 1
    # Find an actual first-read phase whose flip makes an immediate ten-defect.
    chosen = None
    for i in range(104):
        candidate = add(qs[i], mul(20, drift))
        hits = []
        for j, q in enumerate(qs):
            k = multiple((candidate[0]-q[0], candidate[1]-q[1]), drift)
            if k is not None and k >= 0:
                hits.append((104*k+j, j))
        t, j = min(hits)
        context = ''.join(W[(j-9+r) % 104] for r in range(9))
        changed = 'L' if W[j] == 'R' else 'R'
        if W[j] == 'R' and context+changed not in L10:
            chosen = i
            break
    assert chosen is not None
    # The public finite-source routine accepts iterables, not just reusable sets.
    assert first_period_mismatch((q for q in clean), (0, 0), 0, W) is None
    assert first_period_mismatch(list(clean)*2, (0, 0), 0, W) is None
    n = 10**60
    marker = add(qs[chosen], mul(n, drift))
    seed = mature ^ {marker}
    result = next_defect(seed, p, h)
    hits = []
    for j, q in enumerate(qs):
        k = multiple((marker[0]-q[0], marker[1]-q[1]), drift)
        if k is not None and k >= 0:
            hits.append((104*k+j, j))
    event, j = min(hits)
    assert result.status == 'EVENT' and result.event_time == event
    assert result.standard_plans == 1 and result.ordinary_updates == 150
    expected_h = (hs[j]-1) % 4
    assert result.head == add(marker, DIR[expected_h]) and result.heading == expected_h
    whole, part = divmod(event, 104)
    changes = {marker}
    for r in range(part):
        q = add(qs[r], mul(whole, drift))
        if q in changes:
            changes.remove(q)
        else:
            changes.add(q)
    expected = Field(frozenset(seed), frozenset(changes),
                     tuple(Segment(q, drift, whole) for q in qs) if whole else ())
    assert xor_normal_form(result.field, drift) == xor_normal_form(expected, drift)
    damaged = Field(expected.base, expected.changes ^ {(123, 456)}, expected.segments)
    assert xor_normal_form(result.field, drift) != xor_normal_form(damaged, drift)
    assert next_defect(mature, p, h, max_ordinary=0).status == 'UNKNOWN'
    huge = dict(epoch=str(n), event_time=str(event), ordinary_updates=result.ordinary_updates,
                standard_plans=result.standard_plans, complete_field_symbolic_equality=True,
                literal_replay=False)
    return dict(complete_event_endpoints=complete, independent_literal_updates=total_literal,
                max_ordinary_updates=ordinary_max, nontrivial_post_highway_silent_suffixes=nontrivial_suffix,
                certified_no_future_event_controls=no_events, huge_marker=huge,
                resource_cap_is_UNKNOWN=True, damaged_complete_field_rejected=True,
                clean_standard_seed_black=len(clean), iterable_source_controls=2)


def run():
    words, counts = graph.enumerate_words()
    raw = '\n'.join(words)+'\n'
    with tempfile.TemporaryDirectory(prefix='silent-supply-native-') as directory:
        tmp = Path(directory)
        subprocess.run(['g++', '-O2', '-std=c++17', str(ROOT/'independent.cpp'), '-o', str(tmp/'enumerate')],
                       check=True, capture_output=True)
        subprocess.run([str(tmp/'enumerate'), str(tmp/'words.txt'), str(tmp/'counts.txt')],
                       check=True, capture_output=True)
        assert (tmp/'words.txt').read_text() == raw
        assert list(map(int, (tmp/'counts.txt').read_text().split())) == counts
    data = graph.build(words)
    report = dict(schema='silent-supply-v1', status='passed',
                  mathematical_base='8c414b8963260f5d4d394dc5b4c53065028b4c6e',
                  finite_word_count=len(words), word_sha256=WORD_HASH,
                  python_cpp_all_levels_equal=True, graph=data['report'],
                  phases=phase_checks(), inherited_fold=inherited_fold_facts(), algebra=arithmetic_checks(),
                  words=word_controls(data), scope_controls=scope_controls(), events=event_controls(data),
                  all_length_evidence='analytic supply/cofactor proof plus inherited complete bounded-fold coverage',
                  scope='finite ten-legal words and one first-J10 query; no global event budget or HC solution')
    report['source_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted(ROOT.iterdir()) if p.suffix in ('.py', '.cpp')}
    return json.loads(json.dumps(report))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', action='store_true')
    parser.add_argument('--compare', type=Path, default=ROOT/'report.json')
    args = parser.parse_args()
    start = time.monotonic()
    report = run()
    if args.generate:
        args.compare.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    else:
        expected = json.loads(args.compare.read_text())
        if report != expected:
            raise AssertionError('frozen report mismatch; generator is not run to repair it')
    print(json.dumps({'status': 'passed', 'word_count': report['finite_word_count'],
                      'endpoints': report['events']['complete_event_endpoints'],
                      'seconds_informational': time.monotonic()-start}))
