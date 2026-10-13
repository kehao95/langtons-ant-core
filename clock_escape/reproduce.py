#!/usr/bin/env python3
"""Replay precisely the clock paper evidence, without unrelated HC checks."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
EVIDENCE=HERE/'evidence'
EVIDENCE.mkdir(exist_ok=True)


def run(args, logfile=None, cwd=HERE):
    p=subprocess.run(args,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if logfile is not None:
        (EVIDENCE/logfile).write_text(p.stdout)
    if p.returncode:
        print(p.stdout)
        raise SystemExit(p.returncode)


def main():
    if sys.flags.optimize:
        raise SystemExit('Do not use -O')
    run([sys.executable,str(HERE/'verification/check.py')])
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
        shutil.copy2(root/'clock_check_results.json',EVIDENCE/'legacy.json')
        for script, output in [('check_orbit_decider.py','orbit_decider_checks.json'),
                               ('check_affine_certificates.py','affine_certificate_checks.json')]:
            run([sys.executable,str(root/'baseline'/script)],cwd=root/'baseline')
            shutil.copy2(root/'baseline'/output,EVIDENCE/output)
    pin=(HERE/'lean/lean-toolchain').read_text().strip()
    lean=shutil.which('lean')
    if not lean:
        lean=str(Path.home()/'.elan/toolchains'/pin.replace('/','--').replace(':','---')/'bin/lean')
    version=subprocess.check_output([lean,'--version'],cwd=HERE/'lean',text=True).strip()
    if 'version 4.30.0' not in version:
        raise SystemExit('Expected Lean 4.30.0, got '+version)
    run([lean,'ClockLemmas.lean'],'lean.log',HERE/'lean')
    if any(x in (EVIDENCE/'lean.log').read_text() for x in ('sorryAx','ofReduceBool','error:')):
        raise SystemExit('Unexpected trust dependency in local clock lemmas')
    sources=[HERE/'paper/main.tex',HERE/'lean/ClockLemmas.lean',HERE/'verification/check.py',checker]+[baseline.parent/p for p in baseline_files]
    report={'schema':'clock-reproduction-v1','python':sys.version,'lean':version,
            'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
            'full_ant_formalization':False,'third_party_review':False}
    (EVIDENCE/'reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Clock evidence passed: independent graph, legacy replay, kernel-checked local lemmas.')

if __name__=='__main__':
    main()
