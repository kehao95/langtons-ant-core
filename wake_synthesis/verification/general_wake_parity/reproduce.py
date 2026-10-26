#!/usr/bin/env python3
"""Replay the exact audits in an isolated directory; preserve retained evidence."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
SOURCES = ('screen.py', 'family.py', 'audit.py', 'independent.cpp',
           'reproduce.py', 'PROOF.md', 'README.md')
FLAGS = ('-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic',
         '-fsanitize=undefined', '-fno-sanitize-recover=all')


def main() -> None:
    if not __debug__:
        raise RuntimeError('run without Python -O')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='new report path; retained evidence is protected')
    args = parser.parse_args()
    if args.output and (args.output.resolve() == (HERE/'evidence/full_replay.json').resolve()):
        raise ValueError('choose an output outside retained evidence')
    compiler = shutil.which('g++')
    if compiler is None:
        raise RuntimeError('g++ with C++17 and undefined-behavior sanitizer is required')
    hashes = {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in SOURCES}
    manifest = HERE/'evidence/source_manifest.json'
    if manifest.exists():
        expected = json.loads(manifest.read_text())['source_sha256']
        if expected != hashes:
            raise RuntimeError('source manifest mismatch; review the changed source')
    with tempfile.TemporaryDirectory(prefix='langton-general-wake-') as temp:
        work = Path(temp)
        for name in ('screen.py','family.py','audit.py','independent.cpp'):
            shutil.copyfile(HERE/name, work/name)
        binary = work/'native'
        subprocess.run([compiler,*FLAGS,str(work/'independent.cpp'),'-o',str(binary)],
                       check=True,capture_output=True,text=True,timeout=90)
        result_path = work/'audit.json'
        subprocess.run([sys.executable,str(work/'audit.py'),str(binary),'--output',str(result_path)],
                       cwd=work,check=True,capture_output=True,text=True,timeout=180)
        audit = json.loads(result_path.read_text())
    baseline = HERE/'evidence/full_replay.json'
    matched = None
    if baseline.exists():
        matched = json.loads(baseline.read_text())['audit'] == audit
        if not matched:
            raise RuntimeError('fresh deterministic audit differs from retained evidence')
    report = {'status':'complete','audit':audit,'source_sha256':hashes,
              'compiler':subprocess.run([compiler,'--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0],
              'compiler_flags':list(FLAGS),'python_version':platform.python_version(),
              'isolated_replay':True,'retained_audit_matched':matched,
              'proof_boundary':'analytic general theorem; exact affine all-n application; finite tests are regressions',
              'formal_kernel_checked':False,'independent_human_review':False}
    text = json.dumps(report,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(text)


if __name__ == '__main__':
    main()
