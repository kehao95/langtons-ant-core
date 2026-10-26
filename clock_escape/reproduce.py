#!/usr/bin/env python3
"""Replay precisely the clock paper evidence, without unrelated HC checks."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
EVIDENCE=HERE/'evidence'



def run(args, logfile=None, cwd=HERE):
    p=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if logfile is not None:
        (OUTPUT/logfile).write_text(p.stdout)
    if p.returncode:
        print(p.stdout)
        raise SystemExit(p.returncode)


def run_critical():
    source = HERE / 'verification/critical'
    evidence = EVIDENCE / 'critical'
    with tempfile.TemporaryDirectory(prefix='critical-clock-') as name:
        work = Path(name)
        shutil.copytree(source, work / 'module', ignore=shutil.ignore_patterns('__pycache__'))
        for script, output in [('check.py', 'check_results.json'), ('audit.py', 'audit.json')]:
            result = subprocess.run([sys.executable, script], cwd=work / 'module',
                                    capture_output=True, check=True)
            if result.stdout != (evidence / output).read_bytes():
                raise SystemExit(f'Critical evidence mismatch: {output}')
            print(f'Critical {script}: PASS')
    sources = [*sorted(source.glob('*.py')), HERE / 'PROOF.md', HERE / 'paper/main.tex',
               HERE / 'reproduce.py', evidence / 'check_results.json', evidence / 'audit.json']
    report = {'status': 'passed', 'scope': 'critical strengthening only',
              'source_commit': 'c8e280096572b39fd4db4ba91a2fc49bf86d80ff', 'python': sys.version,
              'sha256': {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in sources},
              'original_report_reproduced_byte_for_byte': True,
              'independent_laurent_audit_reproduced_byte_for_byte': True,
              'new_lean_formalization': False}
    (OUTPUT / 'critical-reproduction.json').write_text(json.dumps(report, indent=2) + '\n')


def run_integer():
    with tempfile.TemporaryDirectory(prefix='integer-clock-') as name:
        work = Path(name)
        for source in (HERE / 'verification/integer').glob('*.py'):
            shutil.copy2(source, work / source.name)
        for script in ('check.py', 'audit.py'):
            result = subprocess.run([sys.executable, script], cwd=work,
                                    capture_output=True, check=True)
            expected = EVIDENCE / 'integer' / (Path(script).stem + '.json')
            if result.stdout != expected.read_bytes():
                raise SystemExit(f'Integer evidence mismatch: {script}')
            print(f'Integer {script}: PASS')


def verify():
    global OUTPUT
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--integer-only', action='store_true',
                       help='verify the integer clock and stronger square bound')
    scope.add_argument('--critical-only', action='store_true',
                        help='verify only the new critical-potential strengthening')
    parser.add_argument('--output-dir', type=Path, help='retain generated checks outside the source tree')
    args = parser.parse_args()
    OUTPUT = args.output_dir.resolve() if args.output_dir else Path(output_tmp)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if sys.flags.optimize:
        raise SystemExit('Do not use -O')
    if not args.critical_only:
        run_integer()
    if args.integer_only:
        return
    run_critical()
    if args.critical_only:
        return
    result=subprocess.run([sys.executable,str(HERE/'verification/check.py')],capture_output=True,check=True)
    assert json.loads(result.stdout)==json.loads((EVIDENCE/'independent.json').read_text())
    baseline=HERE/'verification/baseline/diagonal_clock.py'
    checker=HERE/'verification/check_clock_paper.py'
    baseline_files=['diagonal_clock.py','check_orbit_decider.py',
                    'check_affine_certificates.py','affine_clock_certificates.json']
    with tempfile.TemporaryDirectory(prefix='clock-legacy-') as name:
        root=Path(name)
        (root/'baseline').mkdir()
        for filename in baseline_files:
            shutil.copy2(baseline.parent/filename,root/'baseline'/filename)
        shutil.copy2(checker,root/'check_legacy.py')
        run([sys.executable,str(root/'check_legacy.py')],cwd=root)
        shutil.copy2(root/'clock_check_results.json',OUTPUT/'legacy.json')
        for script, output in [('check_orbit_decider.py','orbit_decider_checks.json'),
                               ('check_affine_certificates.py','affine_certificate_checks.json')]:
            run([sys.executable,str(root/'baseline'/script)],cwd=root/'baseline')
            shutil.copy2(root/'baseline'/output,OUTPUT/output)
    pin=(HERE/'lean/lean-toolchain').read_text().strip()
    lean=shutil.which('lean')
    if not lean:
        lean=str(Path.home()/'.elan/toolchains'/pin.replace('/','--').replace(':','---')/'bin/lean')
    version=subprocess.check_output([lean,'--version'],cwd=HERE/'lean',text=True).strip()
    if 'version 4.30.0' not in version:
        raise SystemExit('Expected Lean 4.30.0, got '+version)
    run([lean,'ClockLemmas.lean'],'lean.log',HERE/'lean')
    if any(x in (OUTPUT/'lean.log').read_text() for x in ('sorryAx','ofReduceBool','error:')):
        raise SystemExit('Unexpected trust dependency in local clock lemmas')
    sources=[HERE/'paper/main.tex',HERE/'lean/ClockLemmas.lean',HERE/'verification/check.py',checker]+[baseline.parent/p for p in baseline_files]
    report={'schema':'clock-reproduction-v1','python':sys.version,'lean':version,
            'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
            'full_ant_formalization':False}
    (OUTPUT/'reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Clock evidence passed: independent graph, legacy replay, kernel-checked local lemmas.')

if __name__=='__main__':
    with tempfile.TemporaryDirectory(prefix='clock-output-') as output_tmp:
        verify()
