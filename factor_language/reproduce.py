#!/usr/bin/env python3
"""Replay the paper's exact checks in a disposable copy; preserve retained evidence."""
import argparse, hashlib, json, shutil, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-report',type=Path)
    parser.add_argument('--extensions-only',action='store_true',help='skip the original base and replay later additions')
    parser.add_argument('--new-results-only',action='store_true',help='replay only silent supply and the nine-factor bound')
    args=parser.parse_args()
    if not __debug__: parser.error('Run without Python -O')
    sources=json.loads((ROOT/'sources.json').read_text())['sha256']
    for name, digest in sources.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    scope='new-results-only' if args.new_results_only else ('extensions-only' if args.extensions_only else 'full')
    report={'status':'passed','scope':scope,
            'completed_utc':None,'stages':[]}
    with tempfile.TemporaryDirectory(prefix=ROOT.name+'-replay-') as td:
        work=Path(td)/'experiments/hc_global'
        shutil.copytree(ROOT/'verification',work,ignore=shutil.ignore_patterns('__pycache__'))
        native=Path(td)/'research/nine_factor'
        native.mkdir(parents=True)
        shutil.copy2(work/'nine_factor/enumerate.cpp',native/'enumerate.cpp')
        def run(module,command,outputs=(),compare=True):
            start=time.monotonic()
            result=subprocess.run([sys.executable,*command],cwd=work/module,text=True,capture_output=True)
            if result.returncode: raise RuntimeError(result.stdout+'\n'+result.stderr)
            row={'module':module,'command':command,'seconds':round(time.monotonic()-start,3),'status':'passed'}
            for name in outputs:
                actual=(work/module/name).read_bytes()
                if compare:
                    assert json.loads(actual)==json.loads((ROOT/'verification'/module/name).read_text()),(module,name)
                row[name]=json.loads(actual)
            report['stages'].append(row)
            print(module+': '+command[0]+' PASS',flush=True)
        if not args.extensions_only and not args.new_results_only:
            run('ten',['restore_certificates.py'])
            run('ten',['reproduce.py'],('reports/reproduction.json',),False)
            run('ten_event_macro',['reproduce.py'],('reproduction.json',),False)
            run('mass',['reproduce.py'],('reproduction.json',),False)
        if not args.new_results_only:
            run('silent_fold_reset',['check.py','--compare','report.json'],('derived_masks.json','report.json'))
            run('silent_archive_amplification',['check.py','--compare','checked_report.json'],('checked_report.json',))
            run('silent_archive_recovery',['reproduce.py'])
            run('silent_axis_geometry',['check.py','--report','report.json'],('report.json',))
        run('silent_supply',['check.py'])
        run('nine_mass',['check.py','--compare','check_results.json'])
    report['completed_utc']=datetime.now(timezone.utc).isoformat()
    report['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted((ROOT/'verification').rglob('*'))
                             if p.is_file() and '__pycache__' not in p.parts}
    if args.output_report:
        args.output_report.parent.mkdir(parents=True,exist_ok=True)
        args.output_report.write_text(json.dumps(report,indent=2)+'\n')
    print(ROOT.name+': SELECTED CHECKS PASSED ('+report['scope']+')')

if __name__=='__main__': main()
