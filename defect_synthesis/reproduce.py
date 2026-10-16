#!/usr/bin/env python3
"""Replay the exact supplied-schema arithmetic and finite-cover reconstruction."""
import argparse, hashlib, json, shutil, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-report',type=Path)
    args=ap.parse_args()
    if not __debug__: ap.error('Run without Python -O')
    imported=json.loads((ROOT/'evidence/import-consolidation-2026-10-16.json').read_text())
    for row in imported['files']:
        assert hashlib.sha256((ROOT/row['destination']).read_bytes()).hexdigest()==row['sha256'],row['destination']
    stages=[]
    tasks=[('presburger_defects',['check.py','--compare','report.json']),
           ('defect_resource_spectrum',['reproduce.py']),
           ('schema_supply',['reproduce.py']),
           ('defect_compiler_optimization',['check.py','--compare','check_results.json'])]
    with tempfile.TemporaryDirectory(prefix='ant-defect-synthesis-') as td:
        work=Path(td)/'verification'
        shutil.copytree(ROOT/'verification',work,ignore=shutil.ignore_patterns('__pycache__'))
        for name,command in tasks:
            start=time.monotonic()
            run=subprocess.run([sys.executable,*command],cwd=work/name,text=True,capture_output=True)
            if run.returncode: raise RuntimeError(name+'\n'+run.stdout+'\n'+run.stderr)
            stages.append({'module':name,'command':command,'status':'passed','seconds':round(time.monotonic()-start,3)})
            print(name+': PASS',flush=True)
    report={'status':'passed','source_commit':imported['source_commit'],
            'completed_utc':datetime.now(timezone.utc).isoformat(),'stages':stages,
            'all_coordinate_nonzero_budget_disjunction_expanded':False,
            'small_witness_proof':'analytic; original executable archive absent',
            'source_sha256':{row['destination']:row['sha256'] for row in imported['files']}}
    if args.output_report:
        args.output_report.parent.mkdir(parents=True,exist_ok=True)
        args.output_report.write_text(json.dumps(report,indent=2)+'\n')
    print('DEFECT SYNTHESIS: ALL BUNDLED CHECKS PASSED')
if __name__=='__main__':main()
