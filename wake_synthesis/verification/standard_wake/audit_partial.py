"""Check partial periodic embeddings against the actual chain predicate.

The oracle starts with literal integer event times, removes events while
retaining initial stable-rank segments, and cuts every edge crossing a removed
event. Its surviving open chains therefore have a declared periodic completion.
This checks n < P <= cap, including translated copies of different chains.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import shutil
import subprocess
import tempfile


SEED = 19062026
TRIALS = 4000


def make_cases():
    rng = random.Random(SEED)
    cases = []
    for _ in range(TRIALS):
        period = 4 * rng.randint(2, 42)
        radius = max(1, period // 8)
        # Each class has one time residue modulo four. Consecutive stable
        # ranks therefore satisfy the existing four-update separation rule.
        classes = [(-2 * rng.randint(0, 4) - i % 2, (i % 4) // 2)
                   for i in range(period)]
        levels = [rng.randint(-radius, radius) for _ in range(period)]
        groups = defaultdict(list)
        for i, cell in enumerate(classes):
            groups[cell].append((i - period * levels[i], i))

        retained = set()
        ranks = {}
        for entries in groups.values():
            entries.sort()
            count = rng.randrange(len(entries) + 1)
            for rank, (_, i) in enumerate(entries[:count]):
                retained.add(i)
                ranks[i] = rank
        if not retained:
            raise ValueError('The fixed control recipe produced an empty case')
        if len(retained) == period:
            # The declared period must have at least one omitted phase.
            # Removing a maximal rank preserves the initial-rank condition.
            removable = min(i for i in retained
                            if ranks[i] == len(groups[classes[i]]) - 1)
            retained.remove(removable)
        order = sorted(retained, key=lambda i: (classes[i], ranks[i]))
        index = {old: new for new, old in enumerate(order)}
        nodes = []
        for i in order:
            following = (i + 1) % period
            preceding = (i - 1) % period
            voltage = levels[following] + int(following == 0) - levels[i]
            nodes.append((*classes[i], ranks[i], index.get(following, -1),
                          index.get(preceding, -1),
                          voltage if following in retained else 0))
        cap = period + 4 * rng.randrange(5)
        if not 0 < len(nodes) < period <= cap:
            raise ValueError('Malformed partial embedding')
        cases.append((period, cap, nodes))
    return cases


def source_layout(search_dir):
    parent = search_dir.parent
    if (parent / 'inputs').is_dir() and (parent / 'code').is_dir():
        return parent / 'inputs', parent / 'code'
    return (parent / 'standard_wake_minimum',
            parent / 'standard_wake_pruning' / 'code')


def verify(search_dir=None):
    search = (Path(search_dir).resolve() if search_dir is not None else
              Path(__file__).resolve().parents[1] / 'standard_wake_pruning_v2')
    inputs, rank = source_layout(search)
    spec = importlib.util.spec_from_file_location(
        'partial_embedding_search_overlay', search / 'patch_search.py')
    if spec is None or spec.loader is None:
        raise ValueError('Cannot load the chain-separation overlay')
    patch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(patch)
    cases = make_cases()
    encoded = ''.join(
        f'{len(nodes)} {cap}\n'
        + ''.join(' '.join(map(str, node)) + '\n' for node in nodes)
        for _, cap, nodes in cases)

    with tempfile.TemporaryDirectory(prefix='ant-partial-embedding-review-') as directory:
        tmp = Path(directory)
        shutil.copy2(rank / 'chain_rank.hpp', tmp / 'chain_rank.hpp')
        generated_sha = patch.generate(inputs / 'glue_top.cpp',
                                       tmp / 'generated.cpp',
                                       rank / 'patch_search.py')
        command = ['g++', '-std=c++17', '-O2', '-fsanitize=undefined',
                   '-fno-sanitize-recover=undefined', '-I', str(tmp),
                   str(search / 'test_feasible.cpp'), '-o', str(tmp / 'check')]
        compiled = subprocess.run(command, text=True, capture_output=True)
        if compiled.returncode:
            raise RuntimeError('Control compilation failed:\n' + compiled.stderr)
        process = subprocess.run([str(tmp / 'check')], input=encoded,
                                 text=True, capture_output=True)
        if process.returncode:
            raise RuntimeError('Native control failed:\n' + process.stderr)
        answers = process.stdout.splitlines()
        if answers != ['1'] * len(cases):
            failures = [i for i, answer in enumerate(answers) if answer != '1']
            raise ValueError(f'Positive embedding rejected: {failures[:10]}; '
                             f'received {len(answers)} answers for {len(cases)} cases')
        if process.stderr:
            raise ValueError('Unexpected native diagnostic:\n' + process.stderr)

    sources = {
        'review/check.py': Path(__file__),
        'search/patch_search.py': search / 'patch_search.py',
        'search/test_feasible.cpp': search / 'test_feasible.cpp',
        'rank/patch_search.py': rank / 'patch_search.py',
        'rank/chain_rank.hpp': rank / 'chain_rank.hpp',
        'inputs/glue_top.cpp': inputs / 'glue_top.cpp',
    }
    periods = [period for period, _, _ in cases]
    caps = [cap for _, cap, _ in cases]
    return {
        'status': 'passed', 'partial_periodic_embeddings': len(cases),
        'random_seed': SEED, 'period_range': [min(periods), max(periods)],
        'cap_range': [min(caps), max(caps)],
        'strictly_omitted_event_phases_in_every_case': True,
        'cases_with_period_strictly_below_cap': sum(
            period < cap for period, cap, _ in cases),
        'all_declared_completions_accepted': True,
        'undefined_behavior_sanitizer_passed': True,
        'generated_source_sha256': generated_sha,
        'control_input_sha256': hashlib.sha256(encoded.encode()).hexdigest(),
        'source_sha256': {name: hashlib.sha256(path.read_bytes()).hexdigest()
                          for name, path in sorted(sources.items())},
        'scope': 'Independent positive controls for the chain lemma; abstract '
                 'periodic embeddings, not new ant realizations or exclusions.',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--search-dir', type=Path,
                        help='Directory containing the v2 overlay and native harness')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = json.dumps(verify(args.search_dir), indent=2) + '\n'
    if args.output:
        args.output.write_text(report)
    print(report, end='')
