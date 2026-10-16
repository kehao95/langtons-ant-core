#!/usr/bin/env python3
"""Run theorem-local checks in a disposable copy, preserving retained evidence."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,tempfile

def main():
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    ap=argparse.ArgumentParser();ap.add_argument('--quick',action='store_true');ap.add_argument('--output');args=ap.parse_args()
    root=Path(__file__).resolve().parent
    manifest=root/'MANIFEST.json'
    if manifest.exists():
        for name,digest in json.loads(manifest.read_text())['sha256'].items():
            if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:raise RuntimeError('Source hash mismatch: '+name)
    with tempfile.TemporaryDirectory(prefix='ant-presburger-') as tmp:
        work=Path(tmp);shutil.copytree(root/'code',work/'code',ignore=shutil.ignore_patterns('__pycache__'))
        (work/'evidence').mkdir()
        cmd=[sys.executable,'-u',str(work/'code/check.py')]
        if args.quick:cmd.append('--quick')
        subprocess.run(cmd,cwd=work,check=True)
        result=json.loads((work/'evidence/replay.json').read_text())
        if not args.quick:
            expected=json.loads((root/'evidence/replay.json').read_text())
            for data in (result,expected):data.pop('wall_seconds_informational',None)
            if result!=expected:raise RuntimeError('Deterministic replay mismatch (backend version also pinned)')
        if args.output:Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
        print('Theorem-local reconstruction passed; no all-coordinate full disjunction was expanded.')
if __name__=='__main__':main()
