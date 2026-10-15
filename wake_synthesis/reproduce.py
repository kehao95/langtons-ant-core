#!/usr/bin/env python3
"""Reproduce the self-contained wake artifact in a disposable directory."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--search', action='store_true', help='also replay the bounded detour experiment')
    parser.add_argument('--baseline', action='store_true', help='also replay both preceding exact enumerators')
    parser.add_argument('--output-report', type=Path, help='write a fresh verification record')
    args = parser.parse_args()
    if sys.flags.optimize:
        parser.error('Run without Python -O')
    tasks = [('check.py', ('check_results.json', 'standard_wake.json')),
             ('audit.py', ()), ('audit_integer.py', ()), ('audit_trace.py', ())]
    if args.search:
        tasks.append(('search_replay.py', ('detour_results.json',)))
    with tempfile.TemporaryDirectory(prefix='wake-synthesis-') as directory:
        work = Path(directory)
        shutil.copytree(ROOT / 'verification', work, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__'))
        for script, reports in tasks:
            result = subprocess.run([sys.executable, script], cwd=work,
                                    capture_output=True, text=True, check=True)
            for name in reports:
                if (work / name).read_bytes() != (ROOT / 'evidence' / name).read_bytes():
                    raise SystemExit(f'Retained evidence differs: {name}')
            if not reports:
                retained = (ROOT / 'evidence' / (Path(script).stem + '.json')).read_text()
                if result.stdout != retained:
                    raise SystemExit(f'Algebraic audit differs: {script}')
            print(f'{script}: PASS')
        standard = work / 'standard_wake'
        evidence = ROOT / 'evidence/standard_wake'
        imported = json.loads((evidence / 'provenance.json').read_text())
        for entry in imported['imported_sources']:
            assert hashlib.sha256((ROOT / entry['destination']).read_bytes()).hexdigest() == entry['sha256']
        count_check = subprocess.run([sys.executable, str(standard / 'audit_counts.py')],
                                     capture_output=True, text=True, check=True)
        counts = json.loads(count_check.stdout)
        assert counts == json.loads((evidence / 'counts.json').read_text())
        print('standard wake counts and congruence: PASS', flush=True)
        partial_check = subprocess.run([sys.executable, str(standard / 'audit_partial.py'),
                                        '--search-dir', str(standard / 'v2')],
                                       capture_output=True, text=True, check=True)
        partial = json.loads(partial_check.stdout)
        assert partial == json.loads((evidence / 'partial-embeddings.json').read_text())
        print('4,000 partial-cycle controls with UBSan: PASS', flush=True)
        output = work / 'standard-wake-replay.json'
        command = [sys.executable, str(standard / 'v2/reproduce.py'), '--full',
                   '--upper-check', str(standard / 'upper_pruning.py'), '--output', str(output)]
        if args.baseline:
            command.append('--baseline')
        replay = subprocess.run(command, capture_output=True, text=True)
        if replay.returncode:
            sys.stderr.write(replay.stdout + replay.stderr)
            raise SystemExit(replay.returncode)
        actual = json.loads(output.read_text())
        retained = json.loads((evidence / 'chain-separation.json').read_text())
        def stable(value):
            if isinstance(value, dict):
                return {key: stable(item) for key, item in value.items() if key != 'seconds'}
            if isinstance(value, list):
                return [stable(item) for item in value]
            return value
        for key, value in actual.items():
            if key == 'baselines':
                for name, run in value.items():
                    assert stable(run) == stable(retained[key][name]), name
            else:
                assert stable(value) == stable(retained[key]), key
        assert actual['status'] == 'passed' and actual['full_period_range_replayed']
        assert actual['upper'] == json.loads((evidence / 'upper-pruning.json').read_text())
        cap = actual['optimized_runs'][-1]
        print(f"standard wake uniqueness: PASS; cap={cap['cap']}, prefixes={cap['prefixes']:,}, one P104 word")
        if args.baseline:
            print('original and rank-pruned complete enumeration: PASS')
        report = {'status': 'passed', 'general_checks': [name for name, _ in tasks],
                  'count_audit': counts, 'partial_cycle_audit': partial, 'standard_wake': actual,
                  'retained_evidence_matches': True,
                  'source_sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                    for path in sorted((ROOT / 'verification').rglob('*'))
                                    if path.is_file() and '__pycache__' not in path.parts}}
        if args.output_report:
            args.output_report.write_text(json.dumps(report, indent=2) + '\n')
    print('WAKE SYNTHESIS AND STANDARD-WAKE UNIQUENESS: PASS')


if __name__ == '__main__':
    main()
