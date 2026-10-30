#!/usr/bin/env python3
"""Replay the exact supplied-schema arithmetic and finite-cover reconstruction."""
import argparse, hashlib, json, shutil, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent

MODULE = 'six_cell_feedback'

def replay_added_result(command):
    """Check bound inputs and replay the added theorem in a disposable copy."""
    sources = json.loads((ROOT / 'sources.json').read_text())['sha256']
    for name, expected in sources.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError('Source mismatch: ' + name)
    with tempfile.TemporaryDirectory(prefix=ROOT.name + '-added-') as directory:
        work = Path(directory) / 'module'
        shutil.copytree(ROOT / 'verification' / MODULE, work,
                        ignore=shutil.ignore_patterns('__pycache__'))
        subprocess.run([sys.executable, *command], cwd=work, check=True)
    return {'module': MODULE, 'status': 'passed', 'command': command}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-report',type=Path)
    ap.add_argument('--new-results-only',action='store_true',help='replay only the quantifier-free backend')
    ap.add_argument('--six-cell-only', action='store_true', help='replay only the added theorem; inherit unchanged evidence')
    args=ap.parse_args()
    if not __debug__: raise SystemExit('Run without Python -O')
    added_result = replay_added_result(['verify.py'])
    if args.six_cell_only:
        report = {'status': 'passed', 'scope': 'six-cell-only', 'stages': [added_result], 'inherited_checks_replayed': False}
        if args.output_report:
            args.output_report.parent.mkdir(parents=True, exist_ok=True)
            args.output_report.write_text(json.dumps(report, indent=2) + '\n')
        return

    if not __debug__: ap.error('Run without Python -O')
    sources=json.loads((ROOT/'sources.json').read_text())['sha256']
    for name, digest in sources.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    stages=[added_result]
    tasks=[('presburger_defects',['check.py','--compare','report.json']),
           ('defect_resource_spectrum',['reproduce.py']),
           ('schema_supply',['reproduce.py']),
           ('defect_compiler_optimization',['check.py','--compare','check_results.json'])]
    with tempfile.TemporaryDirectory(prefix='ant-defect-synthesis-') as td:
        work=Path(td)/'verification'
        shutil.copytree(ROOT/'verification',work,ignore=shutil.ignore_patterns('__pycache__'))
        for name,command in ([] if args.new_results_only else tasks):
            start=time.monotonic()
            run=subprocess.run([sys.executable,*command],cwd=work/name,text=True,capture_output=True)
            if run.returncode: raise RuntimeError(name+'\n'+run.stdout+'\n'+run.stderr)
            stages.append({'module':name,'command':command,'status':'passed','seconds':round(time.monotonic()-start,3)})
            print(name+': PASS',flush=True)
        frozen=json.loads((work/'presburger_fast/report.json').read_text())
        for part in ('intersections','literal','factors','symbolic','endpoints','negative'):
            output=Path(td)/(part+'.json')
            command=['check_fast.py','--part',part,'--output',str(output)]
            start=time.monotonic()
            result=subprocess.run([sys.executable,*command],cwd=work/'presburger_fast',text=True,capture_output=True)
            if result.returncode: raise RuntimeError(result.stdout+'\n'+result.stderr)
            actual=json.loads(output.read_text())
            assert actual[part]==frozen[part],part
            stages.append({'module':'presburger_fast','part':part,'status':'passed',
                           'seconds':round(time.monotonic()-start,3),'result':actual[part],
                           'solver_version':actual['solver_version']})
            print('presburger_fast/'+part+': PASS',flush=True)
    report={'status':'passed',
            'scope':'new-results-only' if args.new_results_only else 'full',
            'completed_utc':datetime.now(timezone.utc).isoformat(),'stages':stages,
            'all_coordinate_nonzero_budget_disjunction_expanded':False,
            'small_witness_proof':'analytic; original executable archive absent',
            'source_sha256':sources}
    if args.output_report:
        args.output_report.parent.mkdir(parents=True,exist_ok=True)
        args.output_report.write_text(json.dumps(report,indent=2)+'\n')
    print('DEFECT SYNTHESIS: SELECTED CHECKS PASSED ('+report['scope']+')')
if __name__=='__main__':main()
