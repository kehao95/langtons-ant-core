#!/usr/bin/env python3
"""Reproduce the theorem and the new pruning without trusting optimizer output.

--full (also the default): regenerate upper certificate and exhaust cap 168.
--baseline: additionally exhaust the unchanged cap-168 enumerator.
--quick: cap 104 only; this is not a full uniqueness replay.
Writes a new replay_latest.json; retained evidence is never overwritten.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, random, shutil, subprocess, sys, tempfile
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
# Standalone layout or the corresponding research-repository module layout.
INPUT=(HERE/'inputs' if (HERE/'inputs').is_dir() else HERE.parent/'standard_wake_minimum')
CODE=HERE/'code' if (HERE/'code').is_dir() else HERE
UPPER=(INPUT/'upper_bound.py' if (INPUT/'upper_bound.py').exists()
       else HERE.parent/'standard_wake_uniqueness'/'upper_bound.py')
PINNED={
 'counts.py':'5e735ab9fe491d04d8133d365059324a61f76e851b4e267e4cd00b39de7ef5bc',
 'glue_top.cpp':'567e5464e0be3fe7a748b50661113d5c0ca4466ae3a73488cd0f643830aba39c',
 'verify.py':'4bc7173d87311fc9b42dc3fda131648e2ff4d71bef7b7c34f31ab01dbd5c3973'}
WORD='RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR'
EXPECTED={104:(1443,217,92,343),120:(18644,3147,1006,5021),
          136:(313711,55056,18101,102671),152:(2164812,415360,127727,761427),
          168:(12193595,2454844,663790,4426304)}

def load(name,path):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m

def reference(nodes):
    """Independent coordinate-dictionary oracle, not the stamped-array method."""
    for root,row in enumerate(nodes):
        if row[4]>=0:continue
        i=root;v=0;history=defaultdict(list);steps=0
        while i>=0:
            t,r,k,nxt,prev,vol=nodes[i]
            history[r+2*v,t-r-2*v].append(k)
            v+=vol;i=nxt;steps+=1
            if steps>len(nodes):raise ValueError('cyclic test input')
        if any(any(b!=a+1 for a,b in zip(ks,ks[1:])) for ks in history.values()):
            return False
    return True

def harness_tests(binary,verifier):
    points,heads,drift=verifier.plan(WORD,1)
    groups=defaultdict(list)
    for i,(x,y) in enumerate(points):groups[x+y,x%2].append((i-104*(x//2),i))
    ranks={i:k for entries in groups.values() for k,(_,i) in enumerate(sorted(entries))}
    cases=[];standard=0
    for start in range(104):
        for length in range(1,105):
            nodes=[]
            for j in range(length):
                idx=(start+j)%104;epoch=(start+j)//104
                x,y=points[idx];x+=epoch*2;y-=epoch*2
                if j+1<length:
                    ni=(start+j+1)%104;ne=(start+j+1)//104
                    nx=points[ni][0]+2*ne;vol=nx//2-x//2
                else:vol=0
                nodes.append((x+y,x%2,ranks[idx],j+1 if j+1<length else -1,
                              j-1 if j else -1,vol))
            assert reference(nodes)
            cases.append(nodes);standard+=1
    rng=random.Random(20261015)
    for _ in range(2000):
        n=rng.randrange(1,41)
        nodes=[[rng.randrange(-10,1),rng.randrange(2),rng.randrange(12),-1,-1,0]
               for _ in range(n)]
        permutation=rng.sample(range(n),n)
        for a,b in zip(permutation,permutation[1:]):
            if rng.randrange(4):
                nodes[a][3]=b;nodes[a][5]=rng.randrange(-1,2);nodes[b][4]=a
        cases.append(nodes)
    # Same physical cell and alternating bits, but rank 0 -> 3 is not contiguous.
    cases.append([(0,0,0,1,-1,0),(0,0,3,-1,0,0)])
    cases.append([(0,0,0,1,-1,0),(0,0,1,-1,0,0)])
    expected=[reference(c) for c in cases]
    data=''.join(f'{len(c)} 168\n'+''.join(' '.join(map(str,r))+'\n' for r in c) for c in cases)
    p=subprocess.run([str(binary)],input=data,capture_output=True,text=True,check=True)
    actual=[v=='1' for v in p.stdout.splitlines()]
    if actual!=expected:raise RuntimeError('C++ rank predicate disagrees with geometric oracle')
    return {'standard_cyclic_chain_cases':standard,'random_path_graphs':2000,
            'rank_gap_controls':2,'accepted':sum(actual),'rejected':len(actual)-sum(actual),
            'total_cases':len(actual)}

def run(binary,cap,table,limit=1000000000):
    p=subprocess.run([str(binary),str(cap),str(table),'600',str(limit)],
                     capture_output=True,text=True,check=True,timeout=615)
    lines=p.stdout.splitlines();r=json.loads(lines[-1])
    r['words']=[x.split(' ',2)[2] for x in lines if x.startswith('SOLUTION ')]
    return r

def main(quick=False,baseline=False):
    if not __debug__:raise RuntimeError('Run without Python -O')
    for name,h in PINNED.items():
        if hashlib.sha256((INPUT/name).read_bytes()).hexdigest()!=h:
            raise ValueError('Changed prerequisite: '+name)
    counts=load('pruning_counts',INPUT/'counts.py')
    verifier=load('pruning_verify',INPUT/'verify.py')
    patch=load('patch_search',CODE/'patch_search.py')
    upper=load('upper_bound_replay',UPPER)
    upper_report=upper.verify()
    assert upper_report['period_bound']==168
    data=verifier.periodic_data(WORD,1)
    assert data is not None
    seed,wake,d=data
    assert len(seed)==19 and d==(2,-2)
    assert {(x+y,x%2) for x,y in wake}==counts.WAKE
    assert WORD in verifier.STANDARD+verifier.STANDARD
    assert verifier.verify_forever(seed,WORD,1)
    for r in range(4):
        assert verifier.verify_forever({verifier.rot(q,r) for q in seed},WORD,(1+r)%4)
    for q in seed:assert not verifier.verify_forever(set(seed)-{q},WORD,1)
    assert not verifier.verify_forever(set(seed)|{(2*10**12,-2*10**12)},WORD,1)
    if not shutil.which('g++'):raise RuntimeError('g++ is required')
    jobs=[104] if quick else [104,120,136,152,168]
    runs=[];base_run=None
    with tempfile.TemporaryDirectory(prefix='ant-rank-pruning-') as tmp:
        tmp=Path(tmp);shutil.copy2(CODE/'chain_rank.hpp',tmp/'chain_rank.hpp')
        generated=patch.generate(INPUT/'glue_top.cpp',tmp/'optimized.cpp')
        def compile(source,target):
            subprocess.run(['g++','-std=c++17','-O3','-Wall','-Wextra','-pedantic',
                            '-I',str(tmp),str(source),'-o',str(target)],check=True)
        compile(tmp/'optimized.cpp',tmp/'optimized')
        compile(CODE/'test_rank.cpp',tmp/'test_rank')
        tests=harness_tests(tmp/'test_rank',verifier)
        for cap in jobs:
            text=counts.serialize(counts.tables(cap,'bottom'));table=tmp/f'cost_{cap}.txt'
            table.write_text(text)
            r=run(tmp/'optimized',cap,table)
            assert r['status']=='complete' and r['solutions']==1 and r['words']==[WORD]
            assert tuple(r[k] for k in ('prefixes','order_rejections','cycle_rejections','rank_rejections'))==EXPECTED[cap]
            r['cost_table_sha256']=hashlib.sha256(text.encode()).hexdigest()
            runs.append(r)
            print('optimized',cap,r['status'],r['prefixes'],flush=True)
        assert run(tmp/'optimized',jobs[-1],table,1)['status']=='node_limit'
        if baseline:
            compile(INPUT/'glue_top.cpp',tmp/'baseline')
            base_run=run(tmp/'baseline',jobs[-1],table)
            assert base_run['status']=='complete' and base_run['words']==[WORD]
            assert base_run['prefixes']==(1692 if quick else 40227976)
    result={'status':'passed','full_period_range_replayed':not quick,
            'upper':upper_report,'rank_predicate_tests':tests,'optimized_runs':runs,
            'baseline_run':base_run,'generated_source_sha256':generated,
            'prerequisite_sha256':PINNED,'accepted_word':WORD,
            'complete_seed':sorted(map(list,seed)),'wake':sorted(map(list,counts.WAKE)),
            'controls':{'rotations':4,'active_seed_deletions':19,'far_blocker':True,'node_limit':True},
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                for p in CODE.iterdir() if p.suffix in ('.py','.hpp','.cpp') and p.name!='optimized.cpp'},
            'scope':'Full-wake periodic uniqueness only. No HC entrance or other-wake theorem.'}
    (HERE/'replay_latest.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','full':not quick,'rank_tests':tests},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group()
    g.add_argument('--full',action='store_true');g.add_argument('--quick',action='store_true')
    p.add_argument('--baseline',action='store_true');a=p.parse_args()
    main(a.quick,a.baseline)
