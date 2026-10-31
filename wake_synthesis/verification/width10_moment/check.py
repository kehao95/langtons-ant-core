"""Reproducible, scope-limited checker of the width-ten sharp moment claim.

Default: immutable-file SHA checks, mask arithmetic, small independent positive
word, and a selected deterministic native search sample.
--full: also regenerate all exact 13,216 -> 1,914 masks and replay EVERY one
of the 1,616 chronology cases, with explicit COMPLETE/no-UNKNOWN checks.

The proof imports the existing 54,718-node upper-graph integer certificate; this
script does NOT recheck that older result. It is not an HC proof.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from collections import Counter

ROOT=Path(__file__).resolve().parent
EXPECTED_PROOF='width10-moment-proof-v1'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(cond,msg):
    if not cond: raise AssertionError(msg)


def compile_native(root, target, source):
    subprocess.run(['g++','-std=c++17','-O2',str(root/source),'-o',str(target)],
                   check=True,timeout=120)


def source_integrity(report):
    for name,expected in report['source_sha256'].items():
        actual=sha(ROOT/name)
        require(actual==expected, f'source SHA mismatch: {name} expected={expected} actual={actual}')
    for name,key in (('masks.json','mask_sha256'),('chronology_certificate.json','certificate_sha256')):
        require(sha(ROOT/name)==report[key],f'frozen file mismatch: {name}')
    return len(report['source_sha256'])+2


def run_one(exe,row,t_limit=180.0,node_cap=10000000000):
    index,a,b,g,K,expected_prefixes,expected_solutions=row
    cmd=[str(exe),str(K),str(g),str(t_limit),'1','0',str(a),str(b),str(node_cap)]
    result=subprocess.run(cmd,text=True,capture_output=True,check=True,timeout=t_limit+20)
    lines=result.stdout.strip().splitlines()
    require(lines,f'no native report: {index}')
    report=json.loads(lines[-1])
    require(report['status']=='COMPLETE',f'UNKNOWN in candidate {index}: {report["status"]}')
    require(report['cap']==K and report['growth']==g, f'wrong metadata: {index}')
    require(report['prefixes']==expected_prefixes,f'wrong exhaustive prefix count: {index}')
    require(report['solutions']==expected_solutions,f'wrong solution count: {index}')
    solutions=[]
    for line in lines[:-1]:
        if line.startswith('SOLUTION '):
            fields=line.split()
            require(len(fields)==4 and int(fields[1])<=K and int(fields[2])==g,
                    f'invalid solution: {index}')
            solutions.append(fields[3])
    require(len(solutions)==expected_solutions,f'missing native witness: {index}')
    return solutions


def proof_inventory():
    report=json.loads((ROOT/'report.json').read_text())
    require(report['schema']==EXPECTED_PROOF,'bad report schema')
    return report


def run(*,full=False,time_per_class=180,node_cap=10000000000):
    report=proof_inventory()
    verified=source_integrity(report)
    import masks
    import word_certifier
    raw=masks.raw_masks()
    m=json.loads((ROOT/'masks.json').read_text())
    c=json.loads((ROOT/'chronology_certificate.json').read_text())
    require(len(raw)==13216 and len(m['rows'])==1914 and len(c['complete_rows'])==1616,'wrong cardinalities')
    require(m['raw_sha256']==masks.sha(raw),'wrong full mask source arithmetic')
    require(m['representative_sha256']==masks.sha(m['rows']),'wrong representative digest')
    require(c['base_mask_sha256']==masks.sha(m['rows']),'wrong certificate parent')
    rawindex={(a,b):i for i,(a,b,g,K) in enumerate(raw)}
    filtered=[(rawindex[(a,b)],a,b,g,K) for a,b,g,K,P in m['rows'] if K<=168]
    require([(i,a,b,g,K)for i,a,b,g,K,_,_ in c['complete_rows']]==filtered,
            'not one COMPLETE result for every eligible mask')
    require(Counter(x[3] for x in c['complete_rows'])==Counter({8:371,12:1020,16:225}),
            'wrong growth distribution')
    require(all(x[-1]==0 for x in c['complete_rows'] if x[0]!=c['accepted_index']),
            'unexpected second accepted word')
    accepted=[x for x in c['complete_rows'] if x[-1]>0]
    require(len(accepted)==1 and accepted[0][0]==4328 and accepted[0][1:5]==[1337,1607,12,168],
            'wrong positive identity')
    witness=word_certifier.finite_support_realization(c['accepted_word'])
    require(witness['period']==104 and len(witness['minimum_initial_black'])==19 and
            witness['infinite_breakpoint_checks']==194,'positive independent ray certificate failed')
    origin_odd=sorted(tuple(p) for p in witness['odd_wake'])
    extent=min(j for j,r in origin_odd)
    moment=2*sum(((-1)**(j-extent))*(j-extent-5)**2 for j,r in origin_odd)
    require(moment==168 and len(origin_odd)==12,'standard does not attain sharp moment')
    with tempfile.TemporaryDirectory(prefix='hc-width10-moment-') as directory:
        tmp=Path(directory)
        exe=tmp/'engine'
        compile_native(ROOT,exe,'engine.cpp')
        if full:
            compile_native(ROOT,tmp/'count_screen','count_screen.cpp')
            proc=subprocess.run([sys.executable,str(ROOT/'build_masks.py')],check=True,
                                text=True,capture_output=True,timeout=240)
            require('PASS all normalized masks' in proc.stdout,'mask DP replay failed')
            rows=c['complete_rows']
        else:
            # Deterministic controls from three growth classes, including the
            # unique positive word and nontrivial chronological search.
            subset=[next(x for x in c['complete_rows'] if x[3]==g and x[-2]>1000)for g in (8,12,16)]
            rows=[*subset,accepted[0]]
        found=[]
        for j,row in enumerate(rows,1):
            found+=run_one(exe,row,t_limit=time_per_class,node_cap=node_cap)
            if full and j%100==0:print(f'full chronology replay: {j}/{len(rows)} COMPLETE',flush=True)
        if full:
            require(found==[c['accepted_word']],'full replay unexpected positive word')
        else:
            require(found==[c['accepted_word']],'quick replay did not reconstruct standard')
    print(json.dumps({'result':'PASS','mode':'FULL_ALL_1616'if full else'QUICK_4',
        'frozen_files_checked':verified,'raw_masks':len(raw),
        'count_feasible':m['count_feasible'],'canonical_representatives':len(m['rows']),
        'exhaustive_cases':len(rows),'true_complete_in_frozen_certificate':1616,
        'positive_words':len(found),'independent_infinite_breakpoints':194,
        'note':'Inherited upper graph certificate not replayed; no HC claim'},sort_keys=True))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--full',action='store_true',help='repeat complete 1616-case enumeration')
    parser.add_argument('--time-per-class',type=float,default=180)
    parser.add_argument('--node-cap',type=int,default=10000000000)
    args=parser.parse_args()
    run(full=args.full,time_per_class=args.time_per_class,node_cap=args.node_cap)
