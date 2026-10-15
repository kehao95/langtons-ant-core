#!/usr/bin/env python3
"""Run the theorem-specific checks in a disposable source copy."""
from pathlib import Path
import argparse,json,shutil,subprocess,sys,tempfile

def main():
    if not __debug__:raise RuntimeError('Do not run with -O')
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group()
    g.add_argument('--full',action='store_true');g.add_argument('--quick',action='store_true')
    p.add_argument('--jobs',type=int,default=4);p.add_argument('--output',type=Path);a=p.parse_args()
    if not 1<=a.jobs<=16:p.error('--jobs must be between 1 and 16')
    root=Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix='thin-wake-replay-')as tmp:
        target=Path(tmp)/'package'
        shutil.copytree(root,target,ignore=shutil.ignore_patterns('build','__pycache__','render','repo','.git'))
        subprocess.run([sys.executable,str(target/'code/check.py'),'--quick'if a.quick else'--full','--jobs',str(a.jobs)],check=True,cwd=target)
        report=(target/'evidence/replay_latest.json').read_text()
        if a.output:a.output.write_text(report)
        print('Disposable replay passed; immutable evidence files were not overwritten.')
if __name__=='__main__':main()
