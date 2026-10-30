#!/usr/bin/env python3
"""Reproduce the four-cell certificates without changing retained evidence."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
CERTIFICATES = ('escapes.json', 'witness.json', 'report.json')


MODULE = 'rectangular_frames'

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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-report', type=Path)
    parser.add_argument('--frames-only', action='store_true', help='replay only the added theorem; inherit unchanged evidence')
    parser.add_argument('--jobs', type=int, default=3, help='workers for rectangle certificates')
    args = parser.parse_args()
    if not __debug__: raise SystemExit('Run without Python -O')
    added_result = replay_added_result(['check.py', '--full'] + ['--jobs', str(args.jobs)])
    if args.frames_only:
        report = {'status': 'passed', 'scope': 'frames-only', 'stages': [added_result], 'inherited_checks_replayed': False}
        if args.output_report:
            args.output_report.parent.mkdir(parents=True, exist_ok=True)
            args.output_report.write_text(json.dumps(report, indent=2) + '\n')
        return

    stages = [added_result]
    if sys.flags.optimize:
        raise SystemExit('Run without Python optimization (-O).')
    with tempfile.TemporaryDirectory(prefix='four-cell-port-') as directory:
        work = Path(directory)
        for source in (ROOT / 'verification').glob('*.py'):
            shutil.copy2(source, work / source.name)
        for name in CERTIFICATES:
            shutil.copy2(ROOT / 'evidence' / name, work / name)
        for name in ('check.py', 'independent.py'):
            result = subprocess.run([sys.executable, name], cwd=work,
                                    check=True, capture_output=True, text=True)
            print(f'{name}: {result.stdout.strip()}')
        for name in CERTIFICATES:
            original = (ROOT / 'evidence' / name).read_bytes()
            if (work / name).read_bytes() != original:
                raise SystemExit(f'Regenerated certificate differs: {name}')
            print(f'{name}: SHA256 {hashlib.sha256(original).hexdigest()} PASS')
        result = subprocess.run([sys.executable, 'audit.py', str(ROOT / 'evidence')],
                                cwd=work, check=True, capture_output=True, text=True)
        observed = json.loads(result.stdout)
        retained = json.loads((ROOT / 'evidence' / 'audit.json').read_text())
        if observed != retained or observed['status'] != 'PASS':
            raise SystemExit('Independent audit differs from retained results.')
        print('audit.py: 284 finite seeds, infinite cell certificates, mutation controls, '
              '96 exterior completions PASS')
    with tempfile.TemporaryDirectory(prefix='scattering-') as directory:
        work = Path(directory)
        sources=json.loads((ROOT/'sources.json').read_text())['sha256']
        for name, digest in sources.items():
            assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
        for module, retained in [('guarded_scattering', 'check_results.json'), ('return_scattering', 'report.json')]:
            shutil.copytree(ROOT/'verification'/module, work/module, ignore=shutil.ignore_patterns('__pycache__'))
            result = subprocess.run([sys.executable, 'check.py', '--compare', retained],
                                    cwd=work/module, capture_output=True, text=True)
            if result.returncode: raise RuntimeError(result.stdout+'\n'+result.stderr)
            stages.append({'module':module, 'status':'passed',
                           'retained_report':json.loads((work/module/retained).read_text())})
            print(module+': full exact replay PASS', flush=True)
    if args.output_report:
        args.output_report.write_text(json.dumps({'status':'passed','base_port_replayed':True,
            'stages':stages,'completed_utc':datetime.now(timezone.utc).isoformat()},indent=2)+'\n')
    print('FOUR-CELL PORTS AND COMPOSABLE SCATTERING: PASS')


if __name__ == '__main__':
    main()
