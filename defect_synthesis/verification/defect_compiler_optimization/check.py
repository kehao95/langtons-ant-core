"""Theorem-local equivalence checks. No global nonzero-budget enumeration."""
from __future__ import annotations
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import sys

from fast import (Aff, Block, FastSchema, Schema, Context, ArithmeticFailure,
                  CountQuery, _decision_dag, dag_defect_times, PINS)
from fixtures import L10, schema_case
from isl_bridge import count_fixed


def evaluate_dag(nodes, root, word):
    while root > 1:
        offset, r, l = nodes[root]
        root = r if word[offset] == 'R' else l
    return root == 1


def set_of(schema, values):
    return schema.ctx.set(schema.prefix + '{[t]:' +
        (' or '.join('t=' + str(v) for v in sorted(set(values))) or 'false') + '}')


def independent_turns(word, heading=0):
    """Independent complex-coordinate rotation, first-read colors and literal replay."""
    p, direction = 0j, (1j, 1, -1j, -1)[heading]
    last, seed, points = {}, set(), []
    for letter in word:
        if p in last and last[p] == letter:
            return None
        if p not in last and letter == 'L':
            seed.add(p)
        last[p] = letter
        points.append(p)
        direction *= -1j if letter == 'R' else 1j
        p += direction
    field = set(seed)
    for point, letter in zip(points, word):
        assert (point in field) == (letter == 'L')
        field.symmetric_difference_update({point})
    return len(seed), points, field


def run():
    report = {'schema': 'defect-compiler-optimization-check-v1',
              'base_commit': '6afea97c2a8a26d03b2bf89de9d23a87d64a31e0',
              'scope': 'exact supplied-schema query optimization, not HC or a global budget search',
              'backend': Context().version.strip(), 'baseline_sha256': PINS}
    width, nodes, root = _decision_dag(tuple(sorted(L10)))
    accepted = 0
    for bits in product('RL', repeat=width):
        word = ''.join(bits)
        truth = evaluate_dag(nodes, root, word)
        assert truth == (word in L10)
        accepted += truth
    report['dag_truth_table'] = {'words': 2**width, 'accepted': accepted,
                                'nonterminal_nodes': len(nodes)-2}

    # Every subset, including overlaps in later symbolic tests; explicit duplicates count once.
    s = FastSchema([], [])
    finite = 0
    for mask in range(32):
        values = [i-3 for i in range(5) if mask >> i & 1]
        times = set_of(s, values)
        query = CountQuery(s, times)
        for bound in range(7):
            answer = query.at_most(bound)
            expected = s.domain if len(values) <= bound else s.ctx.set('{ : false }')
            assert answer.equal(expected)
            if bound <= 2:
                assert answer.equal(Schema.cardinality_at_most(s, times, bound))
            finite += 1
    report['finite_count_checks'] = finite
    report['finite_baseline_count_equalities'] = 32*3

    n, a = Aff.var('n'), Aff.var('a')
    s = FastSchema(['n', 'a'], [], domain='n>=0')
    expressions = [
        'false', 'a<=t<a+n',
        'a<=t<a+4*n and (t-a)%4=0',
        'a<=t<a+4*n and ((t-a)%4=0 or (t-a)%4=3)',
        '(a<=t<a+n) or (a+n<=t<a+2*n)',
        '(a<=t<a+2*n) or (a+n<=t<a+3*n)',
        '(a<=t<a+n) or (a+2*n<=t<a+3*n and (t-a)%3=0)',
        '(a<=t<a+n and (t-a)%2=0) or (a+2*n<=t<a+3*n and (t-a)%3=0)',
        't=a', 't>=a', 't<=a', 'true',
    ]
    symbolic = fixed_controls = 0
    for expr in expressions:
        times = s.ctx.set(s.prefix + '{[t]:' + expr + '}').restrict(s.domain)
        for bound in (0, 1, 2, 3, 4):
            answer = s.cardinality_at_most(times, bound)
            old = Schema.cardinality_at_most(s, times, bound)
            assert answer.equal(old), (expr, bound)
            symbolic += 1
            if expr not in ('t>=a', 't<=a', 'true'):
                for length, origin in product((0, 1, 3, 8), (-11, 10**60)):
                    values = {'n': length, 'a': origin}
                    actual = count_fixed(s.at(times, values))
                    assert (not s.at(answer, values).empty()) == (actual <= bound)
                    fixed_controls += 1
    report['symbolic_count_equalities'] = symbolic
    report['independent_fixed_fibre_counts'] = fixed_controls

    # Very large numeric thresholds: symbolic answers, NOT huge literal expansions.
    huge = 10**60
    query = CountQuery(s, s.ctx.set(s.prefix+'{[t]:a<=t<a+4*n and ((t-a)%4=0 or (t-a)%4=3)}'))
    out = query.at_most(huge)
    assert out.equal(s.ctx.set(s.prefix + f'{{ : 0<=n and 2*n<={huge} }}'))
    assert query.last_stats['new_compositions'] == huge.bit_length()-1 + huge.bit_count()-1
    first_stats = dict(query.last_stats)
    out2 = query.at_most(huge+1)
    assert out2.equal(s.ctx.set(s.prefix + f'{{ : 0<=n and 2*n<={huge+1} }}'))
    report['huge_threshold'] = {'bound': str(huge), 'first': first_stats,
                               'cached_followup': dict(query.last_stats),
                               'result': str(out)}

    factor_cases = []
    for name in ('standard', 'rail', 'fold', 'marker', 'sweeps'):
        sc = schema_case(name)
        new = sc.defect_times(L10)
        if name in ('rail', 'sweeps'):
            old = Schema.defect_times(sc, L10)
            assert new.equal(old), name
            validation = 'exact baseline set equality'
        else:
            expected_text = '[t] : n>0 and t=104*n' if name == 'marker' else '[t] : false'
            expected_set = sc.ctx.set(sc.prefix + '{ ' + expected_text + ' }').restrict(sc.domain)
            assert new.equal(expected_set), name
            validation = 'exact algebraic expected set; no baseline completion claim'
        factor_cases.append({'name': name, 'validation': validation, **sc.last_factor_stats})
        for length in (0, 1, 2, 5):
            if name in ('fold', 'sweeps') and length == 0:
                continue
            values = {'n': length}
            if name == 'fold': values['m'] = length-1
            word = sc.instantiate(values)
            expected = [i for i in range(9, len(word)) if word[i-9:i+1] not in L10]
            assert sc.at(new, values).equal(set_of(sc, expected).restrict(
                sc.ctx.set(sc.prefix+'{ : '+ ' and '.join(f'{k}={v}' for k,v in values.items())+' }')))
    report['schema_factor_equivalences'] = factor_cases
    # Check DAG reduction, including functions independent of some letters,
    # on additional complete and partial whitelists of widths one through five.
    generic_checks = 0
    sample_schema = FastSchema(['n'], [Block('LRRL', Aff.var('n')), Block('LR')],
                              domain='n>=0')
    for size in range(1, 6):
        universe = [''.join(w) for w in product('RL', repeat=size)]
        for whitelist in (set(universe), {universe[0]}, {w for w in universe if w[0]=='L'},
                          {w for i,w in enumerate(universe) if i%3==0}):
            actual = dag_defect_times(sample_schema, whitelist)
            expected = Schema.defect_times(sample_schema, whitelist)
            assert actual.equal(expected)
            generic_checks += 1
    report['additional_whitelist_equivalences'] = generic_checks

    # Random short schemas include empty/zero powers and all headings.
    rng = random.Random(20261015)
    words_checked = assignments_checked = viable = 0
    for trial in range(24):
        prefix = ''.join(rng.choice('RL') for _ in range(rng.randrange(0, 6)))
        suffix = ''.join(rng.choice('RL') for _ in range(rng.randrange(0, 6)))
        loop = rng.choice(('LRRL', 'RLLR', 'RRRR', 'LLLL', 'RL', 'LR'))
        heading = trial % 4
        sc = FastSchema(['n'], [Block(prefix or 'RRRR', 0 if not prefix else 1),
                               Block(loop, n), Block(suffix or 'RRRR', 0 if not suffix else 1)],
                        heading=heading, domain='n>=0')
        new = sc.defect_times(L10)
        assert new.equal(Schema.defect_times(sc, L10))
        data = sc.analyze()
        first_l = data['first_times'].intersect(sc.left.domain()).restrict(data['good'])
        for bound in (0, 1, 3):
            assert sc.cardinality_at_most(first_l, bound).equal(
                Schema.cardinality_at_most(sc, first_l, bound))
        for length in range(4):
            values = {'n': length}
            word = sc.instantiate(values)
            expected = [i for i in range(9, len(word)) if word[i-9:i+1] not in L10]
            assert count_fixed(sc.at(new, values)) == len(expected)
            literal = independent_turns(word, heading)
            assert (not sc.at(data['good'], values).empty()) == (literal is not None)
            if literal is not None:
                viable += 1
                for bound in (0, 1, 3):
                    assert (not sc.at(sc.cardinality_at_most(first_l, bound), values).empty()) == (literal[0] <= bound)
            words_checked += len(word)
            assignments_checked += 1
    report['independent_schema_controls'] = {'schemas': 24, 'assignments': assignments_checked,
                                           'requested_letters': words_checked, 'feasible': viable}

    # Complete historical marker retained; optimizations do not change endpoint semantics.
    sc = schema_case('sweeps')
    n = Aff.var('n')
    initial = sc.segment_field([(0,-1,1,0,2*n),(0,4,1,0,2*n)]).union(sc.point_field(
        [(2*n,0),(2*n+1,1),(2*n+1,2),(2*n,3),(-1,3),(-2,2),(-2,1),(-1,0), (10**60, -10**60)]))
    data = sc.analyze(initial)
    target = sc.segment_field([(0,1,1,0,2*n),(0,3,1,0,2*n)]).union(sc.point_field(
        [(-1,1),(-1,2),(2*n,1),(2*n,2),(10**60,-10**60)]))
    assert data['good'].equal(sc.domain)
    assert data['final_black'].equal(target)
    report['complete_remote_history_preserved'] = True

    rejected = 0
    sc = FastSchema([], [])
    for bad_bound in (-1, True, 1.5, '3'):
        try: sc.cardinality_at_most(set_of(sc, (1,)), bad_bound)
        except ValueError: rejected += 1
        else: raise AssertionError('invalid threshold accepted')
    try: CountQuery(sc, sc.ctx.set('{ [t,u] : t=0 and u=0 }'))
    except ValueError: rejected += 1
    else: raise AssertionError('multidimensional fibre accepted')
    other = FastSchema([], [])
    try: CountQuery(sc, set_of(other, (1,)))
    except ValueError: rejected += 1
    else: raise AssertionError('mixed context accepted')
    for invalid in (set(), {'R', 'LL'}, {'RX'}):
        try: sc.defect_times(invalid)
        except ValueError: rejected += 1
        else: raise AssertionError('invalid whitelist accepted')
    # Exhaust the native budget. Exceptions are not interpreted as an empty answer.
    try:
        tiny = Context(max_operations=1)
        tiny.set('[n]->{[t]:0<=t<n}')
    except ArithmeticFailure: rejected += 1
    else: raise AssertionError('quota control unexpectedly succeeded')
    report['negative_controls'] = {'rejected': rejected, 'resource_failure_is_not_NO': True}
    report['full_global_template_enumeration'] = False
    here = Path(__file__).resolve().parent
    report['sources_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (here/'fast.py', here/'fixtures.py', here/'check.py')}
    report['status'] = 'passed'
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', type=Path)
    parser.add_argument('--compare', type=Path)
    args = parser.parse_args()
    result = run()
    if args.compare:
        assert result == json.loads(args.compare.read_text()), 'deterministic report differs'
    if args.write:
        args.write.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True, indent=2))
