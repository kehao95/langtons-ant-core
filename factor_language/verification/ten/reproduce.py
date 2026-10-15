"""Run only this package's checks in a disposable, certificate-preserving copy."""
from __future__ import annotations
import hashlib,json,shutil,subprocess,sys,tempfile,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    if not __debug__:raise RuntimeError('Do not use -O for proof checking.')
    compiler=shutil.which('g++') or shutil.which('clang++')
    if compiler is None:raise RuntimeError('A C++17 compiler (g++ or clang++) is required.')
    certs={str(p.relative_to(ROOT)):digest(p) for p in sorted((ROOT/'certificates').iterdir()) if p.is_file()}
    sources={str(p.relative_to(ROOT)):digest(p) for p in sorted(ROOT.rglob('*')) if p.suffix in ('.py','.cpp') and '__pycache__' not in str(p)}
    stages=[]
    with tempfile.TemporaryDirectory(prefix='ten-factor-replay-') as td:
        work=Path(td)/'package'
        shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('__pycache__','reports','*.pdf','*.aux','*.log','*.out'))
        exe=Path(td)/'independent'
        commands=[('python_complete_kernel',[sys.executable,'check.py']),
                  ('compile_independent',[compiler,'-std=c++17','-O2','-Wall','-Wextra','-pedantic','independent.cpp','-o',str(exe)]),
                  ('cpp_complete_kernel',[str(exe),'certificates']),
                  ('negative_controls',[sys.executable,'negative_controls.py',str(exe)]),
                  ('all_input_algorithm',[sys.executable,'check_algorithm.py'])]
        for name,cmd in commands:
            start=time.monotonic();p=subprocess.run(cmd,cwd=work,capture_output=True,text=True,timeout=180)
            row={'stage':name,'returncode':p.returncode,'elapsed_seconds':round(time.monotonic()-start,3)}
            if p.stdout.strip():
                try:row['result']=json.loads(p.stdout)
                except json.JSONDecodeError:row['stdout']=p.stdout
            if p.stderr.strip():row['stderr']=p.stderr
            stages.append(row)
            if p.returncode:raise RuntimeError(json.dumps(row,indent=2))
        assert all(digest(work/f)==d for f,d in certs.items()),'certificate changed in disposable copy'
    assert all(digest(ROOT/f)==d for f,d in certs.items()),'original certificate changed'
    report={'status':'passed','completed_utc':datetime.now(timezone.utc).isoformat(),'execution':'Fresh theorem-local replay in a disposable copy; no old repository suite',
            'certificates_unchanged':True,'certificate_sha256':certs,'source_sha256':sources,'stages':stages,
            'HC_proved':False,'finite_HC_counterexample':False,'external_mathematical_review':False,'Lean_formalized':False}
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports/reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
