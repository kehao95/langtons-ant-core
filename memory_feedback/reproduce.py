#!/usr/bin/env python3
"""Replay the paper's exact checks in a disposable copy; preserve retained evidence."""
import argparse, hashlib, json, shutil, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def replay_crossing_results():
    """Replay both crossing modules with their complete retained inputs."""
    sources = json.loads((ROOT / 'sources.json').read_text())['sha256']
    for name, expected in sources.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise RuntimeError('Source mismatch: ' + name)
    stages = []
    with tempfile.TemporaryDirectory(prefix='memory-crossing-') as directory:
        work = Path(directory)
        for module in ('crossing_gap', 'crossing_supply'):
            shutil.copytree(ROOT / 'verification' / module, work / module,
                            ignore=shutil.ignore_patterns('__pycache__'))
        for module in ('crossing_gap', 'crossing_supply'):
            subprocess.run([sys.executable, 'check.py'], cwd=work / module, check=True)
            stages.append({'module': module, 'status': 'passed', 'command': ['check.py']})
    return stages


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-report',type=Path)
    parser.add_argument('--extensions-only',action='store_true',help='replay birth-filtered feedback and both crossing modules')
    parser.add_argument('--crossing-only', action='store_true', help='replay both crossing modules; inherit unchanged feedback evidence')
    args=parser.parse_args()
    if not __debug__: raise SystemExit('Run without Python -O')
    crossing_results = replay_crossing_results()
    if args.crossing_only:
        report = {'status': 'passed', 'scope': 'crossing-only', 'stages': crossing_results, 'inherited_checks_replayed': False}
        if args.output_report:
            args.output_report.parent.mkdir(parents=True, exist_ok=True)
            args.output_report.write_text(json.dumps(report, indent=2) + '\n')
        return

    if not __debug__: parser.error('Run without Python -O')
    sources=json.loads((ROOT/'sources.json').read_text())['sha256']
    for name, digest in sources.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    report={'status':'passed','scope':'extensions-only' if args.extensions_only else 'full',
            'completed_utc':None,'stages':crossing_results}
    with tempfile.TemporaryDirectory(prefix=ROOT.name+'-replay-') as td:
        work=Path(td)/'verification'
        shutil.copytree(ROOT/'verification',work,ignore=shutil.ignore_patterns('__pycache__'))
        def run(module,command,outputs=(),compare=True):
            start=time.monotonic()
            result=subprocess.run([sys.executable,*command],cwd=work/module,text=True,capture_output=True)
            if result.returncode: raise RuntimeError(result.stdout+'\n'+result.stderr)
            row={'module':module,'command':command,'seconds':round(time.monotonic()-start,3),'status':'passed'}
            for name in outputs:
                actual=(work/module/name).read_bytes()
                if compare:
                    expected=json.loads((ROOT/'verification'/module/name).read_text())
                    if module=='stale_memory' and name=='check_results.json':
                        # Historical report includes a separately attached witness, not emitted by check.py.
                        expected.pop('blank_created_memory_witness',None)
                        row['historical_annotation_not_regenerated']='blank_created_memory_witness'
                    assert json.loads(actual)==expected,(module,name)
                row[name]=json.loads(actual)
            report['stages'].append(row)
            print(module+': '+command[0]+' PASS',flush=True)
        if not args.extensions_only:
            run('stale_memory',['check.py'],('check_results.json',))
            run('symbolic',['check_symbolic.py'],('check_results.json','huge_recipe.json'))
            run('event_geometry',['check.py'],('check_results.json',))
            run('remote_stale_feedback',['check.py'],('check_results.json',))
            run('scalable_feedback_circuit',['check.py'],('report.json',))
        run('birth_filtered_feedback',['reproduce.py','--output','fresh'],('fresh/replay.json','fresh/rounds.json'),False)
    report['completed_utc']=datetime.now(timezone.utc).isoformat()
    report['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted((ROOT/'verification').rglob('*'))
                             if p.is_file() and '__pycache__' not in p.parts}
    if args.output_report:
        args.output_report.parent.mkdir(parents=True,exist_ok=True)
        args.output_report.write_text(json.dumps(report,indent=2)+'\n')
    print(ROOT.name+': ALL PAPER CHECKS PASSED')

if __name__=='__main__': main()
