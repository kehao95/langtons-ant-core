"""Scoped exact checks; default compares rather than overwrites report.json.

Universal statements follow from the supplied analytic proof, not these tests.
The C++ oracle shares no simulator, crossing, or phase-ray code with Python.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json
import random
import subprocess
import tempfile

from core import (State, DIR, trace, crossing_records, signature, verify_pair,
                  duplicate_at_endpoint, periodic_future, signature_count,
                  capacity, packing_cost, visit_bound, width_deadline,
                  normal_span, classify_width)

ROOT = Path(__file__).resolve().parent


def rotate(p, k):
    x, y = p
    return ((x, y), (y, -x), (-x, -y), (-y, x))[k % 4]


def finite_combinatorics():
    counts_checked = enumerated = packing_checks = 0
    for height, pairs_max in ((0, 5), (1, 5), (2, 4), (3, 3), (4, 3)):
        lengths = []
        for pairs in range(pairs_max + 1):
            length = 2 * pairs + 1
            count = 0
            for w in product(range(height + 1), repeat=length):
                enumerated += 1
                if min(w) == 0 and all((a - b) % 2 for a, b in zip(w, w[1:])):
                    count += 1
                    lengths.append(length)
            assert count == signature_count(height, pairs)
            assert len(lengths) == capacity(height, pairs)
            counts_checked += 1
        running = 0
        for n, length in enumerate(lengths, 1):
            running += length
            assert packing_cost(height, n) == running
            packing_checks += 1
    assert packing_cost(0, 2) is None
    assert packing_cost(0, 0) == 0
    # Exact factorial entropy inequality after clearing logs and square roots:
    # N! <= 5^N * R^(sum(lengths)/2), so square both sides.
    import math
    entropy_checks = 0
    for h in range(2, 25):
        e, o = h // 2 + 1, (h + 1) // 2
        r = e * o
        assert (h + 1)**2 * r < 25 * (r - 1)**2
        for n in (1, 2, 3, 8, 16, 64, 127, 256):
            cost = packing_cost(h, n)
            assert math.factorial(n)**2 <= 25**n * r**cost
            entropy_checks += 1
    return dict(candidate_words=enumerated, exact_count_equalities=counts_checked,
                exact_minimum_packing_checks=packing_checks,
                integer_entropy_checks=entropy_checks)


def cyclic_rule_controls():
    rules = prefix_checks = 0
    classical = None
    for m in range(2, 9):
        for letters in product('RL', repeat=m):
            rule = ''.join(letters)
            minority = min(rule.count('R'), rule.count('L'))
            if not minority:
                continue
            kappa = Fraction(m, minority)
            balance = Fraction(0)
            for phase in range(m):
                for selected in 'RL':
                    count = 0
                    for r in range(m):
                        balance = max(balance, r - kappa * count)
                        count += rule[(phase + r) % m] == selected
            for phase in range(m):
                for selected in 'RL':
                    count = 0
                    for n in range(4*m + 1):
                        assert n <= kappa * count + balance
                        prefix_checks += 1
                        count += rule[(phase+n) % m] == selected
            if rule == 'RL':
                classical = [str(kappa), str(balance), str(2*kappa+balance)]
                assert classical == ['2', '1', '5']
            rules += 1
    return dict(nonconstant_cyclic_rules=rules, exact_balance_checks=prefix_checks,
                classical_kappa_balance_corner_constant=classical,
                general_rule_classifier_implemented=False)


def literal_controls(temp):
    rng = random.Random(20261030)
    cases = []
    for _ in range(96):
        field = {(rng.randrange(-5, 6), rng.randrange(-5, 6))
                 for _ in range(rng.randrange(0, 30))}
        cases.append((State(field, (rng.randrange(-2, 3), rng.randrange(-2, 3)),
                            rng.randrange(4)), 512))
    for k in range(4):
        cases.append((State(set(), heading=k), 16000))
    lines = [str(len(cases))]
    for s, steps in cases:
        lines.append(f'{len(s.black)} {s.head[0]} {s.head[1]} {s.heading} {steps}')
        lines.extend(f'{x} {y}' for x, y in sorted(s.black))
    exe = temp / 'oracle'
    subprocess.run(['g++', '-std=c++17', '-O2', str(ROOT / 'oracle.cpp'), '-o', str(exe)], check=True)
    proc = subprocess.run([str(exe)], input='\n'.join(lines)+'\n', text=True,
                          capture_output=True, check=True, timeout=60)
    output = proc.stdout.splitlines()
    assert len(output) == 4 * len(cases)
    corner_checks = parity_checks = 0
    prefixes = []
    for i, (s, steps) in enumerate(cases):
        word, ps, end = trace(s, steps)
        header = list(map(int, output[4*i].split()))
        assert header == [i, *end.head, end.heading, len(end.black)]
        assert output[4*i+1] == (word or '-')
        raw = list(map(int, output[4*i+2].split()))
        assert list(zip(raw[::2], raw[1::2])) == sorted(end.black)
        raw = list(map(int, output[4*i+3].split()))
        assert list(zip(raw[::2], raw[1::2])) == ps
        n = Counter(ps[:-1])
        for (x, y), value in n.items():
            for sx, sy in product((-1, 1), repeat=2):
                assert value <= 2*n[x+sx, y] + 2*n[x, y+sy] + 5
                corner_checks += 1
        for record in crossing_records(ps).values():
            assert all((a[2]-b[2]) % 2 == 1 for a, b in zip(record, record[1:]))
            parity_checks += max(0, len(record)-1)
        prefixes.append((s, word, ps, end))
    return prefixes, dict(complete_sources=len(cases),
                          literal_updates_per_implementation=sum(t for _, t in cases),
                          full_endpoint_comparisons=len(cases),
                          full_path_comparisons=len(cases),
                          corner_inequalities=corner_checks,
                          adjacent_crossing_parity_checks=parity_checks)


def certificate_controls():
    source = State(set(), heading=2)
    word, ps, end = trace(source, 16000)
    pair = duplicate_at_endpoint(source, ps)
    cert, at = verify_pair(source, 16000, *pair)
    assert cert['period'] == 104 and cert['drift'] == [2, 2]
    assert periodic_future(at, cert['word'])
    certificates = 1
    for shift in range(4):
        for gap in (2, 4, 6):
            a, b = pair[0] + shift, pair[0] + shift + gap
            c, s = verify_pair(source, 16000, a, b)
            assert c['period'] == 52 * gap and c['drift'] == [gap, gap]
            assert periodic_future(s, c['word'])
            certificates += 1
    # Large, complete initial debris behind both cuts is preserved and harmless.
    debris = State({(-10**60, 10**60)}, heading=2)
    c, s = verify_pair(debris, 16000, *pair)
    assert (-10**60, 10**60) in s.black and periodic_future(s, c['word'])
    certificates += 1
    rejected = 0
    # A site on the proved phase-zero ray eventually blocks that exact future.
    d = cert['drift']
    far = at.head[0] + 10**60*d[0], at.head[1] + 10**60*d[1]
    damaged = source.clone(); damaged.black.add(far)
    try:
        verify_pair(damaged, 16000, *pair)
    except ValueError:
        rejected += 1
    else:
        raise AssertionError('unread forward black defect accepted')
    # The observed finite path itself is unchanged by the far blocker.
    assert trace(damaged, 16000)[1] == ps
    tail = at.clone(); tail.black.symmetric_difference_update({far})
    assert not periodic_future(tail, cert['word'])
    rejected += 1
    for a, b, t in ((pair[1], pair[0], 16000), (-1, pair[1], 16000),
                    (pair[0], pair[1], 20)):
        try:
            verify_pair(source, t, a, b)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('malformed finite guard accepted')
    return cert, dict(exact_full_field_certificates=certificates,
                      rejected_guard_or_future_controls=rejected)


def finite_bound_controls(prefixes):
    checked = duplicates = local_counts = entropy_controls = 0
    normals = ((1, 1), (1, -1), (2, 1), (1, 2),
               (Fraction(3, 2), -1), (1, Fraction(5, 3)))
    for source, word, ps, end in prefixes[:96]:
        for T in (0, 1, 4, 16, 64, 128, 512):
            path = ps[:T+1]
            for alpha, beta in normals:
                w = normal_span(path, alpha, beta)
                h = int(w)
                c = visit_bound(h)
                counts = Counter(path[:-1])
                assert all(n <= c for n in counts.values())
                local_counts += len(counts)
                # The left boundary follows by a genuine half-turn, not reflection.
                for sign in (1, -1):
                    src = source if sign == 1 else State({(-x, -y) for x, y in source.black},
                        (-source.head[0], -source.head[1]), (source.heading+2)%4)
                    pp = path if sign == 1 else [(-x, -y) for x, y in path]
                    frontier = max([src.head[0]] + [x for x, y in src.black])
                    N = max(0, pp[-1][0] - frontier)
                    if N:
                        records = crossing_records(pp)
                        sigs = [signature(records[a]) for a in range(frontier, pp[-1][0])]
                        H = max(max(y for _, y in sig) for sig in sigs)
                        if len(set(sigs)) == N:
                            cost = packing_cost(H, N)
                            assert cost is not None
                            assert cost <= sum(map(len, sigs)) <= (T+1)//2
                            entropy_controls += 1
                        else:
                            duplicates += 1
                # Materialize only small illustrative widths; larger is not a failure.
                if h <= 5:
                    R = max([0] + [abs(x-source.head[0]) for x, y in source.black])
                    assert T <= width_deadline(R, h)['deadline']
                    checked += 1
    return dict(finite_deadline_controls=checked, per_cell_bound_checks=local_counts,
                distinct_record_packing_checks=entropy_controls,
                finite_prefixes_with_repeated_signatures=duplicates)


def classifier_controls():
    positive = []
    for heading in range(4):
        mature = trace(State(set(), heading=heading), 12000)[2]
        # Recover the appropriate diagonal normal from an actual whole period.
        after = trace(mature, 104)[2]
        dx, dy = after.head[0]-mature.head[0], after.head[1]-mature.head[1]
        result = classify_width(mature, 12, dy, -dx, max_steps=800)
        assert result['status'] == 'TRANSLATOR'
        assert result['certificate']['period'] == 104
        positive.append(result['time'])
    negative = []
    for width in range(4):
        result = classify_width(State(set()), width, 1, -1, max_steps=500)
        assert result['status'] == 'WIDTH_EXCEEDED'
        negative.append(result['time'])
    assert classify_width(State(set()), 100, max_steps=0)['status'] == 'UNKNOWN'
    for alpha, beta in ((0, 1), (1, 0)):
        try:
            classify_width(State(set()), 3, alpha, beta, max_steps=1)
        except ValueError:
            pass
        else:
            raise AssertionError('axis normal accepted')
    try:
        width_deadline(0, 10, max_exponent=10)
    except ArithmeticError:
        pass
    else:
        raise AssertionError('arithmetic budget failure accepted')
    return dict(translator_certificate_times=positive, first_width_violation_times=negative,
                cap_returns_unknown=True, axis_normals_rejected=True,
                arithmetic_cap_is_not_a_dynamical_answer=True)


def run():
    combinatorics = finite_combinatorics()
    with tempfile.TemporaryDirectory(prefix='crossing-gap-check-') as folder:
        prefixes, literal = literal_controls(Path(folder))
    certificate, guards = certificate_controls()
    finite_bounds = finite_bound_controls(prefixes)
    classifiers = classifier_controls()
    table = []
    for w in range(6):
        d = width_deadline(0, w)
        table.append({'width': w, 'visit_bound': d['visit_bound'],
                      'max_pairs': d['max_pairs'],
                      'capacity_bits': d['signature_capacity'].bit_length(),
                      'deadline_bits': d['deadline'].bit_length()})
    return {'schema': 'crossing-information-width-gap-v1', 'status': 'passed',
            'base_commit': '3f70d44bf8907a0efade67d052f9b8a51519d5f1',
            'proof_scope': 'Analytic all-prefix bounds with exact scoped controls; not HC or period-104 uniqueness.',
            'combinatorics': combinatorics, 'cyclic_rule_balance': cyclic_rule_controls(),
            'literal_crosscheck': literal,
            'guards': guards, 'finite_bounds': finite_bounds,
            'classifiers': classifiers, 'exact_bound_bitlengths': table,
            'blank_certificate': certificate,
            'source_sha256': {p: sha256((ROOT/p).read_bytes()).hexdigest()
                              for p in ('core.py', 'check.py', 'oracle.cpp')}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', type=Path, help='explicit report generation, not a verification replay')
    args = parser.parse_args()
    report = run()
    if args.write:
        args.write.write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
        print('WROTE', args.write)
    else:
        assert report == json.loads((ROOT/'report.json').read_text()), 'report mismatch; frozen evidence unchanged'
        print('PASS: exact crossing and width-gap controls reproduced')
    print(json.dumps(report, sort_keys=True, indent=2))
