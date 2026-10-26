#!/usr/bin/env python3
"""Replay the new periodic arithmetic modules without rerunning old classification."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def check_extensions():
    if not __debug__:raise RuntimeError('Run without -O')
    sources=json.loads((ROOT/'sources.json').read_text())['sha256']
    for name, digest in sources.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    with tempfile.TemporaryDirectory(prefix='wake-extensions-') as td:
        work=Path(td)
        for name in ('periodic_growth_closure','mixed_wake_parity','general_wake_parity','unit_diagonal_analytic','thin_parity_bridge'):
            shutil.copytree(ROOT/'verification'/name,work/name,ignore=shutil.ignore_patterns('__pycache__'))
        subprocess.run([sys.executable,'reproduce.py','--output',str(work/'growth.json')],cwd=work/'periodic_growth_closure',check=True,stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable,'check.py','--enumerate'],cwd=work/'mixed_wake_parity',check=True,stdout=subprocess.DEVNULL)
        mixed=json.loads((work/'mixed_wake_parity/check_results_full.json').read_text())
        assert mixed==json.loads((ROOT/'verification/mixed_wake_parity/check_results_full.json').read_text())
        extra={}
        for name in ('general_wake_parity','unit_diagonal_analytic'):
            output=work/(name+'.json')
            subprocess.run([sys.executable,'reproduce.py','--output',str(output)],cwd=work/name,check=True,stdout=subprocess.DEVNULL)
            extra[name]=json.loads(output.read_text())
        bridge=subprocess.run([sys.executable,'check.py'],cwd=work/'thin_parity_bridge',check=True,capture_output=True,text=True)
        assert json.loads(bridge.stdout)==json.loads((ROOT/'verification/thin_parity_bridge/check_results.json').read_text())
        extra['thin_parity_bridge']=json.loads((work/'thin_parity_bridge/check_results.json').read_text())
        result={'status':'passed','new_arithmetic':extra,
                'periodic_growth':json.loads((work/'growth.json').read_text()),'mixed_wake':mixed}
    print('periodic arithmetic and analytic regressions: PASS',flush=True)
    return result
if __name__=='__main__': print(json.dumps(check_extensions(),indent=2))
