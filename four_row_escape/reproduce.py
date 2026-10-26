#!/usr/bin/env python3
"""Reconstruct the complete four-row certificate in a disposable directory."""
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
    sources=json.loads((ROOT/'sources.json').read_text())['sha256']
    for name, digest in sources.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='four-row-core-') as td:
        work = Path(td)/'module'
        shutil.copytree(ROOT/'verification/four_row_boundary', work,
                        ignore=shutil.ignore_patterns('__pycache__'))
        result = subprocess.run([sys.executable, 'check.py'], cwd=work,
                                text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stdout+'\n'+result.stderr)
        print(result.stdout, end='')
    report = {'status': 'passed', 'scope': 'complete four-row certificate',
              'completed_utc': datetime.now(timezone.utc).isoformat(),
              'seconds': round(time.monotonic()-start, 3),
              'result': json.loads(result.stdout), 'lean_formalized': False,
              'source_sha256': sources}
    if args.output_report:
        args.output_report.parent.mkdir(parents=True, exist_ok=True)
        args.output_report.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
