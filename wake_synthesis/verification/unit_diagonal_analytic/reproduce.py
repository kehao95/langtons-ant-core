#!/usr/bin/env python3
"""Replay the complete, period-free unit-diagonal exclusion and its audit."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import local_obstruction
import audit
import analytic_audit

HERE=Path(__file__).resolve().parent
EXPECTED_HASH='e23fc0680978657507b6192e1fa9984f9b927d686f57584e8e7816414482593d'
FLAGS=['-std=c++17','-O2','-Wall','-Wextra','-Werror','-pedantic',
       '-fsanitize=undefined','-fno-sanitize-recover=all']

def replay():
    if not __debug__:raise RuntimeError('Run without Python -O')
    sources=json.loads((HERE/'evidence/source_manifest.json').read_text())
    for name,wanted in sources.items():
        got=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
        if got!=wanted:raise RuntimeError('Changed source requires review: '+name)
    compiler=shutil.which('g++')
    if not compiler:raise RuntimeError('A C++17 compiler (g++) is required')
    primary,certificates=local_obstruction.verify()
    assert primary['status']=='complete'
    assert [r['candidates'] for r in primary['reports']]==[4,124,12756]
    assert [r['outcomes'].get('survives',0) for r in primary['reports']]==[2,2,0]
    assert len(certificates)==12880 and primary['certificates_sha256']==EXPECTED_HASH
    with tempfile.TemporaryDirectory(prefix='unit-diagonal-') as temp:
        binary=Path(temp)/'independent'
        subprocess.run([compiler,*FLAGS,str(HERE/'independent.cpp'),'-o',str(binary)],check=True)
        run=subprocess.run([str(binary)],capture_output=True,text=True,check=True)
        if run.stderr:raise RuntimeError('Native audit emitted diagnostics: '+run.stderr)
        secondary=json.loads(run.stdout)
    assert secondary['status']=='complete'
    for p,c in zip(primary['reports'],secondary['rows']):
        assert p['depth']==c['depth'] and p['candidates']==c['candidates']
        for key in ('closed_component','rank_gap','stable_order_reversal','survives'):
            assert p['outcomes'].get(key,0)==c[key]
        words=sorted([[''.join(map(str,row)) for row in rs] for rs in p['survivors']])
        assert words==c['survivor_words'] and p['max_events']==c['max_events']
    checks=audit.audit()
    assert checks['status']=='complete' and checks['witnesses_checked']==12880
    assert checks['standard_highway_prefix_controls']==936
    version=subprocess.run([compiler,'--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0]
    analytic=analytic_audit.verify()
    return dict(proof_type='analytic',finite_checks_are_premises=False,analytic_audit=analytic,status='complete',theorem='No finite-support periodic highway has full drift (1,-1)',
                scope=dict(period_bound_assumed=False,width_bound_assumed=False,
                           growth_assumed=False,tail_thinness_assumed=False),
                python_enumeration=primary,independent_cpp=secondary,audit=checks,
                compiler=version,compiler_flags=FLAGS,python_version=sys.version.split()[0],
                source_sha256=sources,
                growth_corollary_dependencies='Jillhewar: positive growth, density, axis g4, even-diagonal g4; not revalidated here',
                formal_kernel_checked=False,independent_human_review=False)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,help='Write a fresh report to this path (not an existing file)')
    args=parser.parse_args()
    if args.output and args.output.exists():raise FileExistsError('Refusing to overwrite an existing report')
    result=replay();text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')

if __name__=='__main__':main()
