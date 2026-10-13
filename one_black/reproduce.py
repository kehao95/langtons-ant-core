#!/usr/bin/env python3
"""Build the pinned proof in a new directory, without prior .olean/native caches."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import time

ROOT=Path(__file__).resolve().parent
PROOF=ROOT/'lean'
OUT=ROOT/'evidence'

def main():
    OUT.mkdir(exist_ok=True)
    pin=(PROOF/'lean-toolchain').read_text().strip()
    lake=shutil.which('lake')
    if not lake:
        lake=str(Path.home()/'.elan/toolchains'/pin.replace('/','--').replace(':','---')/'bin/lake')
    lean=str(Path(lake).with_name('lean'))
    version=subprocess.check_output([lean,'--version'],cwd=PROOF,text=True).strip()
    if 'version 4.30.0' not in version:
        raise SystemExit('Expected Lean 4.30.0: '+version)
    files=sorted(PROOF.rglob('*.lean'))
    files=[p for p in files if '.lake' not in p.parts]
    for p in files:
        text=p.read_text()
        if re.search(r'^\s*(axiom|opaque\s+.*:\s*Prop\s*$)',text,re.M):
            raise SystemExit('Review explicit axiom-like declaration: '+str(p))
        if re.search(r'\b(sorry|admit)\b',text):
            raise SystemExit('Review proof placeholder: '+str(p))
    started=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='one-black-clean-') as name:
        target=Path(name)/'lean'
        shutil.copytree(PROOF,target,ignore=shutil.ignore_patterns('.lake','lake-manifest.json'))
        assert not (target/'.lake').exists()
        with (OUT/'clean-build.log').open('w') as log:
            result=subprocess.run([lake,'build'],cwd=target,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:
            raise SystemExit('Clean build failed; see one_black/evidence/clean-build.log')
        audit=subprocess.run([lake,'env','lean','StandardTrace.lean'],cwd=target,
                             text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=True)
        (OUT/'axioms.log').write_text(audit.stdout)
        if 'sorryAx' in audit.stdout:
            raise SystemExit('Unexpected sorryAx')
        expected={'propext','Classical.choice','Quot.sound',
            'Highway.checks_pass._native.native_decide.ax_1_1',
            'PrefixLeaf.verified._native.native_decide.ax_1_1',
            'ScatteringLeaf.verified._native.native_decide.ax_1_1'}
        outputs=re.findall(r"depends on axioms: \[([^\]]*)\]",audit.stdout,re.S)
        assert len(outputs)==2, audit.stdout
        for output in outputs:
            assert {x.strip() for x in output.split(',')}==expected, output
    report=dict(schema='one-black-clean-verification-v1',lean=version,
        clean_source_build=True,borrowed_build_cache=False,
        elapsed_seconds=round(time.monotonic()-started,2),
        final_theorems=['OneBlack.universal_one_black','OneBlack.universal_one_black_standard_trace'],
        axioms=sorted(expected),lean_sources=len(files),
        sha256={str(p.relative_to(PROOF)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        external_review=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Clean one-black build and both final axiom audits passed.')

if __name__=='__main__': main()
