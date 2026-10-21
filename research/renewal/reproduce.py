#!/usr/bin/env python3
"""Replay scoped contour and rank-obstruction evidence; no global HC claim."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-report', type=Path)
    args = parser.parse_args()
    if not __debug__:
        parser.error('Run without Python -O')
    imported = json.loads((ROOT/'evidence/import-2026-10-20.json').read_text())
    for row in imported['files']:
        assert hashlib.sha256((ROOT/row['destination']).read_bytes()).hexdigest() == row['sha256'], row['destination']
    stages = []
    with tempfile.TemporaryDirectory(prefix='ant-renewal-') as td:
        work = Path(td)/'verification'
        shutil.copytree(ROOT/'verification', work, ignore=shutil.ignore_patterns('__pycache__'))
        for module in ('contour_surgery_pivot', 'contour_exit', 'immediate_distance'):
            command = [sys.executable, 'check.py']
            if module == 'immediate_distance':
                command += ['--compare', 'check_results.json', '--output', str(Path(td)/'distance.json')]
            start = time.monotonic()
            result = subprocess.run(command, cwd=work/module, text=True, capture_output=True)
            if result.returncode:
                raise RuntimeError(module+'\n'+result.stdout+'\n'+result.stderr)
            stages.append({'module': module, 'status': 'passed',
                           'seconds': round(time.monotonic()-start, 3), 'stdout': result.stdout})
            print(module+': PASS', flush=True)
    report = {'status': 'passed', 'scope': 'local theorems and obstruction controls only',
              'source_commit': imported['source_commit'], 'stages': stages,
              'completed_utc': datetime.now(timezone.utc).isoformat(),
              'global_hc_conclusion': False,
              'source_sha256': {r['destination']: r['sha256'] for r in imported['files']}}
    if args.output_report:
        args.output_report.parent.mkdir(parents=True, exist_ok=True)
        args.output_report.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
