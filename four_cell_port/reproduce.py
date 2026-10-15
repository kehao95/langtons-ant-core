#!/usr/bin/env python3
"""Reproduce the four-cell certificates without changing retained evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
CERTIFICATES = ('escapes.json', 'witness.json', 'report.json')


def main():
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
    print('FOUR-CELL OUTGOING PORT: PASS')


if __name__ == '__main__':
    main()
