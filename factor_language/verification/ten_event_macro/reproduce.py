"""Disposable, theorem-local replay; never edits source witnesses or old modules."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile,time
ROOT=Path(__file__).resolve().parent
TEN=ROOT.parent/'ten'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    if not __debug__:raise RuntimeError('Do not disable checks')
    started=time.monotonic();before={p.name:digest(p)for p in (ROOT/'witness.json',ROOT/'attempt.json')}
    compiler=shutil.which('g++') or shutil.which('clang++')
    if compiler is None:raise RuntimeError('A C++17 compiler is required; no passed report produced')
    with tempfile.TemporaryDirectory(prefix='ant-ten-event-') as tmp:
        home=Path(tmp);module=home/'ten_event_macro';ten=home/'ten'
        shutil.copytree(ROOT,module,ignore=shutil.ignore_patterns('__pycache__','report.json','cpp_edges.txt','cpp_ranks.txt','reproduction.json'))
        shutil.copytree(TEN,ten,ignore=shutil.ignore_patterns('__pycache__','paper','reports'))
        def run(cmd,cwd=module,success=True):
            p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
            if (p.returncode==0)!=success:raise RuntimeError(p.stdout+'\n'+p.stderr)
            return p.stdout
        # This recovers exactly the prior theorem's immutable large input witnesses.
        # It does not run unrelated ten-factor results or old global suites.
        if not (ten/'certificates/windows10.txt').exists() or not (ten/'certificates/quotient.tsv').exists():
            run([sys.executable,'restore_certificates.py'],ten)
        out=json.loads(run([sys.executable,'check.py']))
        expected=json.loads((ROOT/'witness.json').read_text())
        if out['graph']!=expected:raise RuntimeError('new immutable graph certificate mismatch')
        exe=home/'independent'
        run([compiler,'-O2','-std=c++17','-Wall','-Wextra','-pedantic','independent.cpp','-o',str(exe)])
        args=[str(exe),str(ten/'certificates/windows10.txt'),str(ten/'certificates/quotient.tsv'),str(module)]
        cpp=json.loads(run(args))
        if digest(module/'cpp_edges.txt')!=expected['edges_sha256'] or digest(module/'cpp_ranks.txt')!=expected['rank_sha256']:
            raise RuntimeError('independent finite lift mismatch')
        corrupt=home/'corrupt-ranks.txt';lines=(module/'cpp_ranks.txt').read_text().splitlines()
        row=lines[0].split('\t');row[-3:]=['0','0','0'];lines[0]='\t'.join(row);corrupt.write_text('\n'.join(lines)+'\n')
        damaged_before=digest(corrupt);run(args+[str(corrupt)],success=False)
        if digest(corrupt)!=damaged_before:raise RuntimeError('damaged rank repaired')
        badwords=home/'missing-word.txt';lines=(ten/'certificates/windows10.txt').read_text().splitlines();badwords.write_text('\n'.join(lines[:-1])+'\n')
        bargs=[str(exe),str(badwords),str(ten/'certificates/quotient.tsv'),str(module)];run(bargs,success=False)
        report={'status':'passed','research_date':'2026-10-15','scope':'New lifted graph, exact first-J10 macros, complete endpoint controls; not old suites or HC',
                'python':out,'cpp':cpp,'negative_controls':{'corrupt_rank_rejected_unchanged':True,'missing_base_word_rejected':True},
                'witnesses_unchanged':before=={p.name:digest(p)for p in (ROOT/'witness.json',ROOT/'attempt.json')},
                'source_sha256':{p.name:digest(p)for p in ROOT.iterdir()if p.suffix in ('.py','.cpp')},
                'seconds':round(time.monotonic()-started,3),'external_mathematical_review':False,'Lean_formalized':False}
        if not report['witnesses_unchanged']:raise RuntimeError('source witness changed')
    (ROOT/'reproduction.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
