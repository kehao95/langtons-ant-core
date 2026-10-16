"""Matched fresh-process benchmarks; timeouts are INCONCLUSIVE, never NO.

Times cover the named query, not common schema construction. Linux peak RSS
covers the whole child process. Exact output-set equality is checked whenever
both methods complete. No extrapolated speedups are reported for timeouts.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import resource
import statistics
import subprocess
import sys
import time

from fast import Aff, Block, Context, FastSchema, Schema, ArithmeticFailure
from fixtures import L10, schema_case

CASES = (
    ('count', 'interval', 32), ('count', 'interval', 64),
    ('count', 'interval', 128), ('count', 'root_rail', 4),
    ('count', 'defect_rail', 128),
    ('factor', 'rail', 0), ('factor', 'sweeps', 0), ('factor', 'standard', 0),
)


def worker(group, name, bound, method):
    # A safety budget, not a mathematical restriction on an input domain.
    resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
    if group == 'count':
        if name == 'interval':
            sc = FastSchema(['n'], [], domain='n>=0')
            times = sc.ctx.set(sc.prefix + '{[t]:0<=t<n}')
        else:
            sc = schema_case('rail')
            if name == 'root_rail':
                data = sc.analyze()
                times = data['first_times'].intersect(sc.left.domain())
            elif name == 'defect_rail':
                times = sc.defect_times(L10)
            else:
                raise ValueError('unknown count fixture')
        begin = time.perf_counter_ns()
        output = (Schema.cardinality_at_most(sc, times, bound) if method == 'baseline'
                  else sc.cardinality_at_most(times, bound))
        elapsed = time.perf_counter_ns() - begin
        stats = ({'explicit_time_dimensions': bound+1, 'cartesian_products': bound}
                 if method == 'baseline' else sc.last_count_stats)
    else:
        sc = schema_case(name)
        begin = time.perf_counter_ns()
        output = Schema.defect_times(sc, L10) if method == 'baseline' else sc.defect_times(L10)
        elapsed = time.perf_counter_ns() - begin
        stats = ({'mask_intersections': 10*len(L10), 'mask_unions': len(L10)}
                 if method == 'baseline' else sc.last_factor_stats)
    return {'status': 'completed', 'query_seconds': elapsed / 1e9,
            'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'output': str(output), 'operations': stats}


def child(group, name, bound, method, timeout):
    command = [sys.executable, __file__, '--worker', group, name, str(bound), method]
    try:
        run = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'status': 'INCONCLUSIVE', 'reason': 'wall-time cap', 'cap_seconds': timeout}
    if run.returncode:
        return {'status': 'INCONCLUSIVE', 'reason': 'child failure',
                'returncode': run.returncode, 'stderr': run.stderr[-1500:]}
    return json.loads(run.stdout)


def execute(repeats, timeout, selected=None):
    rows = []
    for group, name, bound in (CASES if selected is None else (CASES[selected],)):
        print(group, name, bound, file=sys.stderr, flush=True)
        runs = {'baseline': [], 'optimized': []}
        # Alternate order to avoid systematically favoring one method.
        failed = set()
        for trial in range(repeats):
            methods = ('baseline', 'optimized') if trial % 2 == 0 else ('optimized', 'baseline')
            for method in methods:
                if method in failed:
                    continue
                sample = child(group, name, bound, method, timeout)
                runs[method].append(sample)
                print('sample', trial, method, sample.get('status'), sample.get('query_seconds'), file=sys.stderr, flush=True)
                if sample['status'] != 'completed':
                    failed.add(method)
        row = {'group': group, 'name': name, 'bound': bound, 'runs': runs}
        good = {k: [x for x in v if x['status'] == 'completed'] for k, v in runs.items()}
        ctx = Context()
        answers = [(method, r['output']) for method in good for r in good[method]]
        reference = None
        for method, text in answers:
            current = ctx.set(text)
            if reference is None:
                reference = current
            elif not reference.equal(current):
                raise AssertionError('inequivalent completed benchmark outputs')
        row['exact_outputs_equal_where_completed'] = True
        row['both_methods_completed'] = bool(good['baseline'] and good['optimized'])
        for method, values in good.items():
            if values:
                row[method] = {
                    'completed_samples': len(values),
                    'median_seconds': statistics.median(x['query_seconds'] for x in values),
                    'median_peak_rss_kib': statistics.median(x['peak_rss_kib'] for x in values),
                }
        if row['both_methods_completed']:
            row['median_speedup'] = row['baseline']['median_seconds'] / row['optimized']['median_seconds']
        rows.append(row)
    here = Path(__file__).resolve().parent
    return {'schema': 'defect-compiler-optimization-benchmark-v1',
            'base_commit': '6afea97c2a8a26d03b2bf89de9d23a87d64a31e0',
            'backend': Context().version.strip(), 'python': platform.python_version(),
            'platform': platform.platform(), 'requested_repeats': repeats,
            'wall_time_cap_seconds': timeout, 'address_space_cap_bytes': 1024**3,
            'timing_scope': 'named query only; common schema/time-set construction excluded',
            'memory_scope': 'Linux whole-child-process peak RSS, KiB; not incremental query allocation',
            'global_cover_benchmarked': False, 'cases': rows,
            'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in (here/'fast.py', here/'fixtures.py', Path(__file__))}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', nargs=4)
    parser.add_argument('--repeats', type=int, default=5)
    parser.add_argument('--timeout', type=float, default=10.0)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--case-index', type=int, choices=range(len(CASES)))
    args = parser.parse_args()
    if args.worker:
        group, name, bound, method = args.worker
        try:
            print(json.dumps(worker(group, name, int(bound), method), sort_keys=True))
        except (ArithmeticFailure, MemoryError) as exc:
            print(json.dumps({'status': 'INCONCLUSIVE', 'reason': type(exc).__name__, 'detail': str(exc)}))
    else:
        if args.repeats < 1 or args.timeout <= 0:
            parser.error('positive repeats and timeout required')
        result = execute(args.repeats, args.timeout, args.case_index)
        text = json.dumps(result, indent=2, sort_keys=True)+'\n'
        if args.output: args.output.write_text(text)
        print(text)
