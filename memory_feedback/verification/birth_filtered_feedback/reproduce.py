#!/usr/bin/env python3
"""Reconstruct all newborn-feedback evidence in a disposable directory."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys, tempfile

def digest_report(report):
    report=dict(report);report.pop('elapsed_seconds',None)
    return hashlib.sha256(json.dumps(report,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def main():
    if not __debug__:raise RuntimeError('Run without Python -O')
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args()
    root=Path(__file__).resolve().parent
    expected=json.loads((root/'evidence'/'checked_summary.json').read_text())
    for name,sha in expected['source_sha256'].items():
        if hashlib.sha256((root/'code'/name).read_bytes()).hexdigest()!=sha:
            raise RuntimeError(f'Source changed: {name}')
    with tempfile.TemporaryDirectory(prefix='ant-birth-feedback-') as td:
        work=Path(td);shutil.copytree(root/'code',work/'code',ignore=shutil.ignore_patterns('__pycache__'))
        (work/'evidence').mkdir()
        run=subprocess.run([sys.executable,str(work/'code'/'check.py')],cwd=work/'code',capture_output=True,text=True)
        if run.returncode:
            raise RuntimeError(run.stdout+'\n'+run.stderr)
        result=json.loads((work/'evidence'/'replay.json').read_text())
        if digest_report(result)!=expected['deterministic_report_sha256']:
            raise RuntimeError('Reconstructed report differs')
        if hashlib.sha256((work/'evidence'/'rounds.json').read_bytes()).hexdigest()!=expected['rounds_sha256']:
            raise RuntimeError('Reconstructed reset rounds differ')
        if args.output:
            args.output.mkdir(parents=True,exist_ok=True)
            for name in ('replay.json','rounds.json'):
                shutil.copy2(work/'evidence'/name,args.output/name)
        print(json.dumps({'status':'passed','deterministic_report_sha256':digest_report(result),
                          'blank_positive_rounds':result['blank_positive_renewal_rounds'],
                          'terminal_checkpoint':result['blank_terminal_checkpoint'],
                          'scope':'Birth-filtered total query and necessary non-ETC consequences; no global exclusion.'},indent=2))
if __name__=='__main__':main()
