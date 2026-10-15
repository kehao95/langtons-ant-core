"""Exact reproducibility checks for the thin-wake theorem.

The default/full mode reruns every recorded finite search, including all eight
shards of the final case. --quick validates reductions, records, positive and
negative controls, but explicitly does NOT replay the large exclusions.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import derive

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'inputs'))
import upper_bound
import verify
import counts as prior_counts


def sha(raw):return hashlib.sha256(raw).hexdigest()


def run(binary,cap,table,mask,hole,shard=0,shards=1,limit=2_000_000_000,seconds=1800):
    cmd=[str(binary),str(cap),str(table),str(seconds),str(limit),str(mask),str(hole)]
    if 'shard'in binary.name:cmd.extend((str(shard),str(shards)))
    proc=subprocess.run(cmd,check=True,text=True,capture_output=True,timeout=seconds+15)
    lines=proc.stdout.strip().splitlines()
    answer=json.loads(lines[-1])
    answer['words']=[s.split()[2]for s in lines if s.startswith('SOLUTION ')]
    return answer,proc.stdout


def local_checks():
    groups=defaultdict(set);n=0
    for parity in(0,1):
        for m in range(11):
            for word in itertools.product((0,1),repeat=m):
                I=sum(word)
                J=sum((b^(k%2))if not parity else 1-(b^(k%2))for k,b in enumerate(word))
                groups[parity,I,J,m%2].add(m);n+=1
    for key,values in groups.items():
        assert {m for m in derive.local_counts(*key)if m<=10}==values
    return {'binary_strings':n,'count_cases':len(groups)}


def reduction_checks():
    rows=[];survivors={h:[]for h in derive.HOLES};tested=0
    for hole in range(-9,0):
        signed=sum((1 if t%2==0 else-1)*n for t,n in zip(range(-10,1),derive.density(hole)))
        assert signed==(4 if hole%2 else 2)
        for mask in range(256):
            O=derive.wake(hole,mask);assert len(O)==12
            assert derive.wake(hole,mask^255)==frozenset((t,1-r)for t,r in O)
            a=derive.modular_trace(O);b=derive.modular_trace(O,'top')
            opposite=derive.modular_trace(derive.wake(hole,mask^255))
            assert a['possible']==b['possible']==opposite['possible']
            if a['possible']:
                assert hole%2 and a['period_mod16']==b['period_mod16']==opposite['period_mod16']
                if mask>=128:survivors[hole].append(mask)
            tested+=1
            rows.append({'hole':hole,'mask':mask,'bottom':a['frontier'],'top':b['frontier'],
                         'phase':a['phase_residues'],'possible':a['possible'],'mod16':a['period_mod16']})
    assert [len(survivors[h])for h in derive.HOLES]==[12,20,12,20,12]
    assert [derive.bound(h)for h in derive.HOLES]==[192,168,160,168,192]
    return {'masks_checked':tested,'survivors':survivors,'recurrence_sha256':sha(json.dumps(rows,sort_keys=True,separators=(',',':')).encode())}


def witness_checks(word):
    assert len(word)==104 and word in verify.STANDARD+verify.STANDARD
    seed,odd,d=verify.periodic_data(word,1)
    assert d==(2,-2) and len(seed)==19 and verify.verify_forever(seed,word,1)
    points,headings,drift=verify.plan(word,1)
    cs=Counter((x+y,x%2)for x,y in points)
    O=frozenset(c for c,n in cs.items()if n%2)
    assert O==derive.wake(-3,163)
    assert max(x+y for x,y in points)==0 and min(x+y for x,y in points)==-10
    assert word.count('R')-word.count('L')==12
    top1=[i for i,(x,y)in enumerate(points)if x+y==0 and x%2==1]
    assert len(top1)==1
    phase=top1[0];changed=word[phase:]+word[:phase]
    data=verify.periodic_data(changed,1)
    assert data is not None and data[2]==(2,-2)
    pp,_,_=verify.plan(changed,1);cc=Counter((x+y,x%2)for x,y in pp)
    assert frozenset(c for c,n in cc.items()if n%2)==derive.wake(-3,92)
    for rotation in range(4):
        assert verify.verify_forever({verify.rot(q,rotation)for q in seed},word,(1+rotation)%4)
    for q in seed:assert not verify.verify_forever(seed-{q},word,1)
    assert not verify.verify_forever(seed|{(2*10**12,-2*10**12)},word,1)
    return {'seed':sorted(map(list,seed)),'word':word,'drift':[2,-2],
            'standard_masks':[163,92],'other_top_phase':phase,'single_deletion_controls':len(seed),'rotations':4}


def main(quick=False,workers=4):
    if not __debug__:raise RuntimeError('Do not run with -O')
    started=time.monotonic()
    saved=json.loads((ROOT/'evidence/cases.json').read_text())
    for directory in('native','inputs'):
        manifest=json.loads((ROOT/directory/'MANIFEST.json').read_text())
        for name,h in manifest.items():assert sha((ROOT/directory/name).read_bytes())==h,(directory,name)
    upper=upper_bound.verify();assert upper['period_bound']==168
    local=local_checks();red=reduction_checks();witness=witness_checks(saved['word'])
    required={(h,m)for h,ms in red['survivors'].items()for m in ms}
    assert {(r['hole'],r['mask'])for r in saved['cases']}==required
    assert len(saved['cases'])==len(required)==76
    by_id={j['id']:j for j in saved['jobs']};assert len(by_id)==len(saved['jobs'])==83
    for c in saved['cases']:
        js=[by_id[j]for j in c['jobs']]
        assert js and all((j['hole'],j['mask'])==(c['hole'],c['mask'])for j in js)
        modulus=derive.modular_trace(derive.wake(c['hole'],c['mask']))['period_mod16']
        assert modulus==c['mod16']
        highest=derive.bound(c['hole'])-(derive.bound(c['hole'])-modulus)%16
        assert all(j['cap']>=highest for j in js)
        if len(js)>1:
            assert {j['shard']for j in js}==set(range(len(js)))
            assert all(j['shards']==len(js)for j in js)
            assert len({j['expected']['cuts']for j in js})==len({j['expected']['cut_hash']for j in js})==1
            assert sum(j['expected']['selected_cuts']for j in js)==js[0]['expected']['cuts']
    assert [w for j in saved['jobs']for w in j['expected']['words']]==[saved['word']]
    actual=[];table_checks=0
    with tempfile.TemporaryDirectory(prefix='thin-wake-')as tmp:
        work=Path(tmp);bins={}
        shutil.copyfile(ROOT/'native/chain_rank.hpp',work/'chain_rank.hpp')
        for name in {j['engine']for j in saved['jobs']}:
            src=ROOT/'native'/f'{name}.cpp';dest=work/f'{name}.cpp';shutil.copyfile(src,dest)
            binary=work/name
            subprocess.run(['g++','-O3','-std=c++17','-Wall','-Wextra','-pedantic',str(dest),'-o',str(binary)],check=True)
            bins[name]=binary
        for job in saved['jobs']:
            assert job['expected']['status']=='complete'
            src=ROOT/'native'/f"{job['engine']}.cpp"
            assert sha(src.read_bytes())==job['source_sha256']
            log=ROOT/'evidence/logs'/f"{job['id']}.log"
            assert sha(log.read_bytes())==job['stdout_sha256']
            O=derive.wake(job['hole'],job['mask']);op='bottom'if job['side']=='top'else'top'
            tab=derive.tables(job['cap'],O,op);text=derive.serialize(tab)
            assert sha(text.encode())==job['table_sha256']
            # An independently retained implementation of the count recurrence.
            prior_counts.WAKE=O
            assert prior_counts.serialize(prior_counts.tables(job['cap'],op))==text
            (work/f"{job['id']}.table").write_text(text);table_checks+=1
        # Positive, negative and partition controls; not large exclusion replays.
        O=derive.wake(-3,163);table=work/'control.table'
        table.write_text(derive.serialize(derive.tables(104,O,'bottom')))
        base,_=run(bins['profile_search'],104,table,163,-3)
        assert base['status']=='complete'and base['words']==[saved['word']]
        controls=[]
        for shard in range(8):
            ans,_=run(bins['sharded_top'],104,table,163,-3,shard,8)
            assert ans['status']=='complete';controls.append(ans)
        assert [w for a in controls for w in a['words']]==[saved['word']]
        assert len({a['cuts']for a in controls})==len({a['cut_hash']for a in controls})==1
        assert sum(a['selected_cuts']for a in controls)==controls[0]['cuts']
        stopped,_=run(bins['profile_search'],104,table,163,-3,limit=1)
        assert stopped['status']=='node_limit'
        if not quick:
            def worker(job):
                answer,text=run(bins[job['engine']],job['cap'],work/f"{job['id']}.table",
                                job['mask'],job['hole'],job['shard'],job['shards'])
                assert answer['status']=='complete',(job['id'],answer)
                stable={k:v for k,v in answer.items()if k!='seconds'}
                assert stable==job['expected'],(job['id'],'deterministic mismatch')
                print(job['id'],answer['prefixes'],answer['solutions'],flush=True)
                return {'id':job['id'],'seconds':answer['seconds'],'verified':True}
            with ThreadPoolExecutor(max_workers=workers)as pool:
                actual=list(pool.map(worker,saved['jobs']))
    report={'status':'passed','mode':'quick-controls-only'if quick else'full-exhaustion-replay',
            'upper':upper,'local':local,'reduction':red,'witness':witness,
            'canonical_cases':76,'recorded_jobs':83,'native_jobs_replayed':len(actual),
            'table_crosschecks':table_checks,'small_shard_controls':8,'node_limit_control':True,
            'recorded_accumulated_prefixes':saved['accumulated_prefixes'],
            'runs':actual,'seconds':time.monotonic()-started,
            'boundary':'Conventional coverage argument and exact computations, not Lean or external peer review. Quick mode does not replay the large exclusions.'}
    (ROOT/'evidence/replay_latest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('upper','runs','reduction','witness')},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();g=ap.add_mutually_exclusive_group()
    g.add_argument('--full',action='store_true');g.add_argument('--quick',action='store_true')
    ap.add_argument('--jobs',type=int,default=4);args=ap.parse_args()
    if not 1<=args.jobs<=16:ap.error('--jobs must be between 1 and 16')
    main(args.quick,args.jobs)
