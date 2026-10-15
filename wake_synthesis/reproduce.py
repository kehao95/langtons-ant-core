#!/usr/bin/env python3
"""Reproduce the self-contained wake artifact in a disposable directory."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--search', action='store_true', help='also replay the bounded detour experiment')
    args = parser.parse_args()
    if sys.flags.optimize:
        parser.error('Run without Python -O')
    tasks = [('check.py', ('check_results.json', 'standard_wake.json')),
             ('audit.py', ()), ('audit_integer.py', ()), ('audit_trace.py', ())]
    if args.search:
        tasks.append(('search_replay.py', ('detour_results.json',)))
    with tempfile.TemporaryDirectory(prefix='wake-synthesis-') as directory:
        work = Path(directory)
        for source in (ROOT / 'verification').iterdir():
            if source.is_file():
                shutil.copy2(source, work / source.name)
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
    print('WAKE SYNTHESIS: PASS')


if __name__ == '__main__':
    main()
