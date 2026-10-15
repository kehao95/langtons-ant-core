#!/usr/bin/env python3
"""Replay the chain-separation lemma controls and exact cap-168 enumeration.

Default/--full completes every tested cap through 168. --quick ends at 104 and
is not a full uniqueness check. --baseline also runs both preceding engines.
All generated files live in a disposable directory. A requested --output file
receives fresh evidence; the retained audit.json is never overwritten by default.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
INPUT = (HERE.parent/'inputs' if (HERE.parent/'inputs').is_dir()
         else HERE.parent/'standard_wake_minimum')
RANK = (HERE.parent/'code' if (HERE.parent/'code').is_dir()
        else HERE.parent/'standard_wake_pruning'/'code')
BASE_REPLAY = RANK.parent/'reproduce.py'
UPPER = (INPUT/'upper_bound.py' if (INPUT/'upper_bound.py').exists()
         else HERE.parent/'standard_wake_uniqueness'/'upper_bound.py')
EXPECTED = {104:1376, 120:17566, 136:270080, 152:1739460, 168:8580751}
RANK_EXPECTED = {104:1443, 120:18644, 136:313711, 152:2164812, 168:12193595}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def normalized_nodes(classes, levels, cuts, ranks=None):
    """A declared periodic event embedding cut into contiguous chains.

    Independently assign stable ranks from literal integer event times. This
    oracle never uses a difference constraint or the proposed edge-weight rule.
    """
    period = len(classes)
    if ranks is None:
        groups = defaultdict(list)
        for i, cell in enumerate(classes):
            groups[cell].append((i-period*levels[i], i))
        ranks = {}
        for entries in groups.values():
            for rank, (_, i) in enumerate(sorted(entries)):
                ranks[i] = rank
    order = sorted(range(period), key=lambda i: (*classes[i], ranks[i]))
    inverse = {j:i for i,j in enumerate(order)}
    nodes = []
    for i in order:
        following = (i+1) % period
        preceding = (i-1) % period
        voltage = levels[following] + int(following == 0) - levels[i]
        nodes.append((*classes[i], ranks[i],
                      -1 if i in cuts else inverse[following],
                      -1 if preceding in cuts else inverse[preceding],
                      0 if i in cuts else voltage))
    return nodes


def crossing_control(crossed):
    # Two abstract five-event chains. X=(0,0), Y=(-2,0).
    # Crossed: A visits X before B, but B visits Y before A. Their interiors
    # would have to overlap. Other labels are distinct; no rank gap is involved.
    classes = [(0,0),(-1,0),(-2,1),(-1,1),(-2,0),
               (-2,0),(-3,0),(-4,1),(-3,1),(0,0)]
    ranks = dict.fromkeys(range(10), 0)
    ranks[9] = 1
    ranks[4 if crossed else 5] = 1
    return normalized_nodes(classes, [0]*10, {4,9}, ranks)


def literal_two_chain_oracle(nodes, period=16):
    """Enumerate actual circle placements, not linear-relaxation feasibility."""
    chains = []
    for start, node in enumerate(nodes):
        if node[4] >= 0:
            continue
        chain = []
        i = start
        while i >= 0:
            chain.append(i)
            i = nodes[i][3]
        chains.append(chain)
    assert len(chains) == 2
    for second_start in range(-period, period+1):
        times = {}
        occupied = set()
        collision = False
        for chain, start in zip(chains, (0, second_start)):
            for position, i in enumerate(chain):
                time = start+position
                if time % period in occupied:
                    collision = True
                occupied.add(time % period)
                times[i] = time
        if collision:
            continue
        if all(node[2] == 0 or times[i]-times[i-1] >= 4
               for i,node in enumerate(nodes)):
            return True
    return False


def predicate_tests(strong_binary, rank_binary, verifier, word):
    points, _, _ = verifier.plan(word, 1)
    classes = [(x+y,x%2) for x,y in points]
    levels = [x//2 for x,y in points]
    cases = []
    # Every one-cut and two-cut decomposition of the genuine P104 cycle.
    for cut_count in (1,2):
        for cuts in combinations(range(104), cut_count):
            nodes = normalized_nodes(classes, levels, set(cuts))
            cases.append((104, nodes))
            cases.append((168, nodes))
    standard = len(cases)
    rng = random.Random(2026101502)
    # General cycle embeddings vary stable ranks, voltages, phases and cuts.
    # They test the chain lemma independently of this particular ant word;
    # they are not asserted to be ant trajectories.
    for _ in range(2000):
        period = 4*rng.randrange(1,7)
        classes = [(2*rng.randrange(-5,1)-(i%2), (i%4)//2)
                   for i in range(period)]
        # Keep the synthetic quotient coordinates within the search band.
        classes = [(max(-10,t),r) if t%2==0 else (max(-9,t),r)
                   for t,r in classes]
        levels = [rng.randrange(-1,2) for _ in range(period)]
        cuts = set(rng.sample(range(period), rng.randrange(1,period+1)))
        cases.append((period+4*rng.randrange(0,5), normalized_nodes(classes,levels,cuts)))
    positive = len(cases)
    crossed = crossing_control(True)
    ordered = crossing_control(False)
    assert not literal_two_chain_oracle(crossed)
    assert literal_two_chain_oracle(ordered)
    cases.extend([(16,crossed),(16,ordered)])
    encoded = ''.join(f'{len(nodes)} {cap}\n' + ''.join(
        ' '.join(map(str,node))+'\n' for node in nodes) for cap,nodes in cases)
    def run(binary):
        process = subprocess.run([str(binary)],input=encoded,text=True,
                                 capture_output=True)
        if process.returncode:
            raise RuntimeError(f'{binary.name}: {process.stderr}')
        return [line == '1' for line in process.stdout.splitlines()]
    old = run(rank_binary)
    new = run(strong_binary)
    assert old == [True]*len(cases), 'Rank baseline rejected a positive embedding/control'
    assert new == [True]*positive+[False,True], 'Chain-separation control mismatch'
    return {'standard_one_or_two_cut_embeddings_at_two_caps':standard,
            'independent_abstract_cycle_embeddings':2000,
            'literal_circle_packing_controls':2,'total_cases':len(cases),
            'rank_baseline_accepts_crossing_control':True,
            'chain_separation_rejects_crossing_control':True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--full',action='store_true')
    mode.add_argument('--quick',action='store_true')
    parser.add_argument('--baseline',action='store_true')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--upper-check',type=Path,
                        help='Optional equivalent upper-certificate replay module')
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError('Run without Python -O')
    base = load('rank_replay',BASE_REPLAY)
    for name, sha in base.PINNED.items():
        assert hashlib.sha256((INPUT/name).read_bytes()).hexdigest() == sha
    counts = load('chain_counts',INPUT/'counts.py')
    verifier = load('chain_verify',INPUT/'verify.py')
    rank_patch = load('chain_rank_patch',RANK/'patch_search.py')
    patch = load('chain_separation_patch',HERE/'patch_search.py')
    upper = load('chain_upper',args.upper_check or UPPER)
    upper_report = upper.verify(UPPER) if args.upper_check else upper.verify()
    assert upper_report['period_bound'] == 168
    word = base.WORD
    seed, wake, drift = verifier.periodic_data(word,1)
    assert len(seed) == 19 and drift == (2,-2)
    assert {(x+y,x%2) for x,y in wake} == counts.WAKE
    assert verifier.verify_forever(seed,word,1)
    for rotation in range(4):
        assert verifier.verify_forever({verifier.rot(q,rotation) for q in seed},word,(1+rotation)%4)
    for q in seed:
        assert not verifier.verify_forever(set(seed)-{q},word,1)
    assert not verifier.verify_forever(set(seed)|{(2*10**12,-2*10**12)},word,1)
    reports = []
    baselines = {}
    with tempfile.TemporaryDirectory(prefix='ant-chain-separation-replay-') as directory:
        tmp = Path(directory)
        shutil.copy2(RANK/'chain_rank.hpp',tmp/'chain_rank.hpp')
        generated_sha = patch.generate(INPUT/'glue_top.cpp',tmp/'generated.cpp',RANK/'patch_search.py')
        rank_patch.generate(INPUT/'glue_top.cpp',tmp/'rank.cpp')
        def compile(source,target):
            subprocess.run(['g++','-std=c++17','-O3','-Wall','-Wextra','-pedantic',
                            '-I',str(tmp),str(source),'-o',str(target)],check=True)
        compile(tmp/'generated.cpp',tmp/'search')
        compile(HERE/'test_feasible.cpp',tmp/'test_strong')
        harness = (HERE/'test_feasible.cpp').read_text().replace('"generated.cpp"','"rank.cpp"')
        (tmp/'test_rank_feasible.cpp').write_text(harness)
        compile(tmp/'test_rank_feasible.cpp',tmp/'test_rank_feasible')
        controls = predicate_tests(tmp/'test_strong',tmp/'test_rank_feasible',verifier,word)
        compile(RANK/'test_rank.cpp',tmp/'test_rank')
        rank_controls = base.harness_tests(tmp/'test_rank',verifier)
        print('independent controls passed',controls['total_cases'],flush=True)
        for cap in ([104] if args.quick else [104,120,136,152,168]):
            table = tmp/f'cost-{cap}.txt'
            table.write_text(counts.serialize(counts.tables(cap,'bottom')))
            result = base.run(tmp/'search',cap,table)
            assert result['status'] == 'complete' and result['words'] == [word]
            assert result['solutions'] == 1 and result['prefixes'] == EXPECTED[cap]
            result['cost_table_sha256'] = hashlib.sha256(table.read_bytes()).hexdigest()
            reports.append(result)
            print('chain separation',cap,result['status'],result['prefixes'],flush=True)
        assert base.run(tmp/'search',cap,table,1)['status'] == 'node_limit'
        if args.baseline:
            for name, source, expected in (
                ('rank',tmp/'rank.cpp',RANK_EXPECTED[cap]),
                ('original',INPUT/'glue_top.cpp',1692 if args.quick else 40227976)):
                compile(source,tmp/name)
                result = base.run(tmp/name,cap,table)
                assert result['status'] == 'complete' and result['words'] == [word]
                assert result['prefixes'] == expected
                baselines[name] = result
                print(name,cap,result['status'],result['prefixes'],flush=True)
    report = {'status':'passed','full_period_range_replayed':not args.quick,
              'upper':upper_report,'chain_separation_controls':controls,
              'rank_predicate_controls':rank_controls,'optimized_runs':reports,
              'baselines':baselines,'generated_source_sha256':generated_sha,
              'prerequisite_sha256':base.PINNED,
              'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted(HERE.iterdir()) if p.suffix in ('.py','.cpp')},
              'accepted_word':word,
              'controls':{'rotations':4,'active_seed_deletions':19,
                          'far_blocker':True,'node_limit':True},
              'scope':'Only the specified full standard wake and drift; no entrance theorem.'}
    if args.output:
        args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
