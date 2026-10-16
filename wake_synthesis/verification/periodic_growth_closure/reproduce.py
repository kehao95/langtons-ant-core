#!/usr/bin/env python3
"""Offline exact replay. Neither copied audit output nor a hash is a theorem."""
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys, tempfile

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git_blob(p):
    b=p.read_bytes();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def main():
    if not __debug__:raise RuntimeError('Do not use Python -O')
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    root=Path(__file__).resolve().parent
    manifest=json.loads((root/'MANIFEST.json').read_text())
    for name,sha in manifest['files'].items():
        if digest(root/name)!=sha:raise RuntimeError('Changed pinned file: '+name)
    for name,sha in manifest['upstream_git_blobs'].items():
        if git_blob(root/'third_party'/name)!=sha:raise RuntimeError('Not the recorded upstream bytes: '+name)
    saved=json.loads((root/'evidence/unit_replay.json').read_text())
    with tempfile.TemporaryDirectory(prefix='ant-growth-closure-') as td:
        work=Path(td);shutil.copytree(root/'unit',work/'unit')
        def run(script,*argv):
            p=subprocess.run([sys.executable,str(script),*map(str,argv)],capture_output=True,text=True,check=True)
            return p.stdout
        run(work/'unit/obstruction.py','--output',work/'certificate.json')
        run(work/'unit/verify_certificate.py',work/'certificate.json','--report',work/'verification.json')
        run(work/'unit/controls.py',work/'certificate.json','--report',work/'controls.json')
        if digest(work/'certificate.json')!=saved['certificate_sha256']:raise RuntimeError('Unit certificate changed')
        for key in ('verification','controls'):
            if json.loads((work/f'{key}.json').read_text())!=saved[key]:raise RuntimeError('Unit evidence changed: '+key)
        axis=run(root/'third_party/axis_rank_parity_audit.py')
        if axis!=(root/'evidence/upstream_axis.txt').read_text():raise RuntimeError('Upstream axis replay changed')
        diagonal=json.loads(run(root/'third_party/even_diagonal_rank_parity_audit.py','--chain-length','6'))
        if diagonal!=json.loads((root/'evidence/upstream_diagonal.json').read_text()):raise RuntimeError('Upstream diagonal replay changed')
        independent=json.loads(run(root/'code/audit.py'))
        if independent!=json.loads((root/'evidence/independent.json').read_text()):raise RuntimeError('Independent audit changed')
        report={'status':'passed','unit_certificate_sha256':digest(work/'certificate.json'),
                'unit_verification':saved['verification'],'unit_controls':saved['controls'],
                'upstream_axis':axis,'upstream_diagonal':diagonal,
                'independent':independent,'attribution':manifest['attribution'],
                'scope':'All-period necessary restrictions and g>=8. Not HC, not g>=12, not an existence claim at g=8, not Lean or peer review.'}
    text=json.dumps(report,indent=2)+'\n';print(text)
    if args.output:args.output.write_text(text)
if __name__=='__main__':main()
