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


MODULE = 'axis_wake'

def replay_added_result(command):
    """Check bound inputs and replay the added theorem in a disposable copy."""
    sources = json.loads((ROOT / 'sources.json').read_text())['sha256']
    for name, expected in sources.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError('Source mismatch: ' + name)
    with tempfile.TemporaryDirectory(prefix=ROOT.name + '-added-') as directory:
        work = Path(directory) / 'module'
        shutil.copytree(ROOT / 'verification' / MODULE, work,
                        ignore=shutil.ignore_patterns('__pycache__'))
        subprocess.run([sys.executable, *command], cwd=work, check=True)
    return {'module': MODULE, 'status': 'passed', 'command': command}



def replay_moment(full):
    """Join the inherited all-period graph bound to the extremal search."""
    sources=json.loads((ROOT/'sources.json').read_text())['sha256']
    for name,digest in sources.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Source mismatch: '+name)
    with tempfile.TemporaryDirectory(prefix='wake-moment-') as td:
        work=Path(td)/'verification'
        shutil.copytree(ROOT/'verification',work,ignore=shutil.ignore_patterns('__pycache__'))
        result=subprocess.run([sys.executable,str(work/'standard_wake/upper_pruning.py'),'--upper-source',str(work/'standard_wake/inputs/upper_bound.py')],capture_output=True,text=True,check=True)
        actual=json.loads(result.stdout)
        expected=json.loads((ROOT/'evidence/standard_wake/upper-pruning.json').read_text())
        if actual!=expected:raise RuntimeError('Upper graph certificate mismatch')
        command=[sys.executable,str(work/'width10_moment/check.py')]
        if full:command+=['--full','--time-per-class','300']
        subprocess.run(command,cwd=work/'width10_moment',check=True)
    return {'status':'passed','scope':'full' if full else 'quick','upper_graph_replayed':True,'all_1616_cases_replayed':full}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extensions-only',action='store_true',help='replay only new periodic arithmetic; inherit unchanged classification evidence')
    parser.add_argument('--quick', action='store_true', help='skip the 76-case thin-wake exhaustion; still check its upper graph, count tables and controls')
    parser.add_argument('--jobs', type=int, default=4, help='parallel thin-wake native jobs, 1..16')
    parser.add_argument('--search', action='store_true', help='also replay the bounded detour experiment')
    parser.add_argument('--baseline', action='store_true', help='also replay both preceding exact enumerators')
    parser.add_argument('--output-report', type=Path, help='write a fresh verification record')
    parser.add_argument('--axis-only', action='store_true', help='replay only the added theorem; inherit unchanged evidence')
    parser.add_argument('--moment-only',action='store_true',help='check the sharp moment and shared period bound')
    parser.add_argument('--full',action='store_true',help='with --moment-only, replay all 1616 chronology cases')
    args = parser.parse_args()
    if not __debug__: raise SystemExit('Run without Python -O')
    if args.moment_only:
        report=replay_moment(args.full)
        if args.output_report:
            args.output_report.parent.mkdir(parents=True,exist_ok=True)
            args.output_report.write_text(json.dumps(report,indent=2)+'\n')
        return
    if not args.axis_only and not args.extensions_only:
        replay_moment(not args.quick)
    added_result = replay_added_result(['reproduce.py'])
    if args.axis_only:
        report = {'status': 'passed', 'scope': 'axis-only', 'stages': [added_result], 'inherited_checks_replayed': False}
        if args.output_report:
            args.output_report.parent.mkdir(parents=True, exist_ok=True)
            args.output_report.write_text(json.dumps(report, indent=2) + '\n')
        return

    if not 1 <= args.jobs <= 16:
        parser.error('--jobs must be 1..16')
    if sys.flags.optimize:
        parser.error('Run without Python -O')
    from verification.check_extensions import check_extensions
    extensions=check_extensions()
    extensions['axis_wake'] = added_result
    if args.extensions_only:
        report={'status':'passed','scope':'extensions-only','extensions':extensions,
                'full_current_classification_replayed':False}
        if args.output_report: args.output_report.write_text(json.dumps(report,indent=2)+'\n')
        return
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
        report = {'status': 'passed', 'scope':'quick' if args.quick else 'full', 'extensions':extensions, 'general_checks': [name for name, _ in tasks],
                  'count_audit': counts, 'partial_cycle_audit': partial, 'standard_wake': actual,
                  'retained_evidence_matches': True,
                  'source_sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                                    for path in sorted((ROOT / 'verification').rglob('*'))
                                    if path.is_file() and '__pycache__' not in path.parts}}
        thin_output = work / 'thin-wake-replay.json'
        thin_command = [sys.executable, str(ROOT/'verification/thin_wake/reproduce.py'),
                        '--quick' if args.quick else '--full', '--jobs', str(args.jobs),
                        '--output', str(thin_output)]
        subprocess.run(thin_command, check=True)
        report['thin_wake'] = json.loads(thin_output.read_text())
        report['full_current_classification_replayed'] = not args.quick
        if args.output_report:
            args.output_report.write_text(json.dumps(report, indent=2) + '\n')
    print('WAKE SYNTHESIS AND THIN-WAKE RIGIDITY: PASS')


if __name__ == '__main__':
    main()
