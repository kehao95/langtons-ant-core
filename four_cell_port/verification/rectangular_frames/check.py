"""Reproduce immutable theorem evidence. Default is the complete replay.

--quick replays only four frame certificates and scope controls; it explicitly
is NOT a fresh replay of the other 38 universal or 3538 finite certificates.
"""
from __future__ import annotations
import argparse,concurrent.futures,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
from coverage import jobs,audit
from controls import replay as controls
from verify import Checker
HERE=Path(__file__).resolve().parent

def validate_manifest():
    manifest=json.loads((HERE/'sources.json').read_text())
    for rel,digest in manifest['files'].items():
        path=HERE/rel
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise ValueError('Source/certificate mismatch: '+rel)
    return len(manifest['files'])

def one(job):
    source,report,guard=job
    actual=json.loads(json.dumps(Checker(json.loads(source.read_text()),guard).run()))
    expected=json.loads(report.read_text())
    if actual!=expected:raise AssertionError('Acceptance report differs: '+source.name)
    return actual['name'],actual['read_checks']

def main():
    p=argparse.ArgumentParser(description=__doc__)
    mode=p.add_mutually_exclusive_group();mode.add_argument('--full',action='store_true');mode.add_argument('--quick',action='store_true')
    p.add_argument('--jobs',type=int,default=1);p.add_argument('--output',type=Path)
    a=p.parse_args()
    if sys.flags.optimize:raise RuntimeError('Run without Python -O; checks use assertions')
    if a.jobs<1:raise ValueError('jobs must be positive')
    count=validate_manifest();selected=jobs()[:4] if a.quick else jobs();done=[]
    with concurrent.futures.ProcessPoolExecutor(max_workers=a.jobs) as pool:
        for name,checks in pool.map(one,selected):
            done.append(name);print(json.dumps({'accepted':name,'read_checks':checks}),flush=True)
    c=controls()
    if c!=json.loads((HERE/'controls_report.json').read_text()):raise AssertionError('Scope controls changed')
    finite=False
    if not a.quick:
        subprocess.run([sys.executable,str(HERE/'finite_check.py')],check=True,cwd=HERE)
        finite=True
    cover=audit()
    if cover!=json.loads((HERE/'coverage_report.json').read_text()):raise AssertionError('Coverage report changed')
    validate_manifest()
    result={'accepted':True,'mode':'quick_partial' if a.quick else 'full','hashed_files':count,
            'fresh_universal_schemas':len(done),'fresh_finite_cover':finite,'fresh_scope_controls':True,
            'coverage_audit':True,'universal_read_checks':sum(json.loads(r.read_text())['read_checks'] for _,r,_ in selected)}
    if a.output:a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
