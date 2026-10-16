#!/usr/bin/env python3
"""Replay the new periodic arithmetic modules without rerunning old classification."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def check_extensions():
    if not __debug__:raise RuntimeError('Run without -O')
    imported=json.loads((ROOT/'evidence/import-2026-10-16.json').read_text())
    for row in imported['files']:
        assert hashlib.sha256((ROOT/row['destination']).read_bytes()).hexdigest()==row['sha256'],row['destination']
    with tempfile.TemporaryDirectory(prefix='wake-extensions-') as td:
        work=Path(td)
        for name in ('periodic_growth_closure','mixed_wake_parity'):
            shutil.copytree(ROOT/'verification'/name,work/name,ignore=shutil.ignore_patterns('__pycache__'))
        subprocess.run([sys.executable,'reproduce.py','--output',str(work/'growth.json')],cwd=work/'periodic_growth_closure',check=True,stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable,'check.py','--enumerate'],cwd=work/'mixed_wake_parity',check=True,stdout=subprocess.DEVNULL)
        mixed=json.loads((work/'mixed_wake_parity/check_results_full.json').read_text())
        assert mixed==json.loads((ROOT/'verification/mixed_wake_parity/check_results_full.json').read_text())
        result={'status':'passed','source_commit':imported['source_commit'],
                'periodic_growth':json.loads((work/'growth.json').read_text()),'mixed_wake':mixed}
    print('periodic growth dependencies and mixed-wake parity: PASS',flush=True)
    return result
if __name__=='__main__': print(json.dumps(check_extensions(),indent=2))
