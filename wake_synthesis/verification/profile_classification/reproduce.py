#!/usr/bin/env python3
"""Full 256-lift classification replay. Incomplete searches never certify a theorem.

Regenerates the inherited upper witness, all count tables, the 40 exact searches,
local modular/count audits, and cap-104 sanitized differential checks. Existing
release artifacts and retained evidence are never overwritten.
"""
from __future__ import annotations
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import audit_profile as audit
import counts_profile as counts
from generate import generate
import verify_word as verifier

HERE=Path(__file__).resolve().parent
STANDARD=HERE.parent/'standard_wake'
PINS={
 'inputs/glue_top.cpp':'567e5464e0be3fe7a748b50661113d5c0ca4466ae3a73488cd0f643830aba39c',
 'inputs/upper_bound.py':'3a9a227f7e26d99875c37d4ea5fc45f886bb3c772ca350ba31217397e90297b2',
 'code/chain_rank.hpp':'faea9b6b883edd9c888f5bb4bd5a6b1bf086ce4b3169e197c89533ac1c18b056',
}

def write_json(path, value):
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def checked_run(binary, cap, table, mask, seconds, nodes, log):
    p=subprocess.run([str(binary),str(cap),str(table),str(seconds),str(nodes),str(mask)],
                     capture_output=True,text=True,check=True,timeout=seconds+30)
    log.write_text(p.stdout+p.stderr)
    if p.stderr:raise RuntimeError('Unexpected diagnostic: '+str(log))
    result=json.loads(p.stdout.splitlines()[-1])
    if result['status']!='complete':
        raise RuntimeError(f"INCONCLUSIVE: mask {mask}, cap {cap}, status {result['status']}")
    result['words']=[line.split(' ',2)[2] for line in p.stdout.splitlines() if line.startswith('SOLUTION ')]
    if result['solutions']!=len(result['words']) or result['mask']!=mask or result['cap']!=cap:
        raise RuntimeError('Malformed search report')
    return result

def main(args):
    if not __debug__:raise RuntimeError('Run without Python -O')
    if not shutil.which('g++'):raise RuntimeError('g++ with C++17 and UBSan is required')
    if not 1<=args.jobs<=32 or not math.isfinite(args.seconds) or args.seconds<=0 or args.nodes<=0:
        raise ValueError('Invalid resource limits')
    output=Path(args.output).resolve() if args.output else Path(tempfile.mkdtemp(prefix='langtons-profile-'))
    if args.output:output.mkdir(parents=True,exist_ok=False)
    for rel,expected in PINS.items():
        if hashlib.sha256((STANDARD/rel).read_bytes()).hexdigest()!=expected:
            raise RuntimeError('Changed prerequisite; review before repinning: '+rel)
    spec=importlib.util.spec_from_file_location('profile_upper',STANDARD/'inputs/upper_bound.py')
    upper=importlib.util.module_from_spec(spec);spec.loader.exec_module(upper)
    upper_report=upper.verify()
    assert upper_report['period_bound']==168 and upper_report['maximum_edge_lhs']==-1
    write_json(output/'upper_certificate.json',upper_report)
    (output/'logs').mkdir()
    with tempfile.TemporaryDirectory(prefix='profile-work-') as scratch:
        work=Path(scratch);tables=work/'tables';tables.mkdir()
        shutil.copyfile(STANDARD/'code/chain_rank.hpp',work/'chain_rank.hpp')
        lower=[]
        for mask in range(256):
            tab=counts.tables(168,mask)
            bound=tab[0].get((1,1,1,1))
            lower.append({'mask':mask,'lower_bound':None if bound is None else bound+2,
                          'states':sum(map(len,tab.values()))})
            (tables/f'{mask}.txt').write_text(counts.serialize(tab))
        write_json(output/'count_relaxations.json',lower)
        audit_report=audit.audit(lower)
        write_json(output/'audits.json',audit_report)
        masks=[r['mask'] for r in lower if r['lower_bound'] is not None]
        assert len(masks)==40
        source_hash=generate(STANDARD/'inputs/glue_top.cpp',work/'search.cpp',True)
        baseline_hash=generate(STANDARD/'inputs/glue_top.cpp',work/'baseline.cpp',False)
        assert source_hash=='8be9c56502db5ef0e0b54f50ba5104fbdfe21271a3c07c14c8e2f377229e5252'
        assert baseline_hash=='999cb2510eb2c6b35f26f7a69d604b6d50d714a93b861ed92e0d6f1f11296d8a'
        subprocess.run(['g++','-std=c++17','-O3','-Wall','-Wextra',str(work/'search.cpp'),'-o',str(work/'search')],check=True)
        results=[]
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures={pool.submit(checked_run,work/'search',168,tables/f'{m}.txt',m,args.seconds,args.nodes,output/'logs'/f'full_{m:03}.log'):m for m in masks}
            for future in as_completed(futures):
                r=future.result();results.append(r)
                print(f"mask {r['mask']:3}: complete; {r['prefixes']} prefixes; {r['solutions']} accepted",flush=True)
        results.sort(key=lambda r:r['mask'])
        write_json(output/'searches.json',results)
        # The two later chronological pruners are absent in the baseline.
        for source,binary in [('baseline.cpp','baseline_sanitized'),('search.cpp','optimized_sanitized')]:
            subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(work/source),'-o',str(work/binary)],check=True)
        tables104=work/'tables104';tables104.mkdir()
        for m in masks:(tables104/f'{m}.txt').write_text(counts.serialize(counts.tables(104,m)))
        def compare(mask):
            runs=[checked_run(work/b,104,tables104/f'{mask}.txt',mask,args.seconds,args.nodes,
                             output/'logs'/f'{b}_{mask:03}.log') for b in ('baseline_sanitized','optimized_sanitized')]
            assert runs[0]['words']==runs[1]['words']
            return {'mask':mask,'baseline_prefixes':runs[0]['prefixes'],
                    'optimized_prefixes':runs[1]['prefixes'],'words':runs[0]['words']}
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:diff=list(pool.map(compare,masks))
        write_json(output/'differential.json',{'cap':104,'masks_compared':40,'undefined_behavior_sanitizer':True,
                   'sanitizer_diagnostics':0,'all_completed':True,'outputs_equal':True,
                   'baseline_source_sha256':baseline_hash,'results':diff})
    accepted=[]
    for r in results:
        for word in r['words']:
            seed,wake,d=verifier.synthesize(word)
            assert wake==counts.wake(r['mask']) and verifier.forever(seed,word)
            assert not verifier.forever(seed|{(2*10**12,-2*10**12)},word)
            assert all(not verifier.forever(seed-{q},word) for q in seed)
            assert word in verifier.STANDARD+verifier.STANDARD and verifier.primitive_period(word)==104
            accepted.append({'mask':r['mask'],'period':len(word),'primitive_period':104,'word':word,
               'rotation_offset':(verifier.STANDARD+verifier.STANDARD).index(word),'seed':sorted(seed),
               'seed_size':len(seed),'drift':d,'wake':sorted(wake),'forever_verified':True,
               'all_seed_deletions_rejected':len(seed),'remote_blocker_epoch':10**12,'remote_blocker_rejected':True})
    assert [(a['mask'],a['rotation_offset']) for a in accepted]==[(92,18),(163,0)]
    assert next(r for r in results if r['mask']==163)['prefixes']==8580751
    assert sum(r['prefixes'] for r in results)==215709876
    write_json(output/'accepted_words.json',accepted)
    summary={'status':'complete','classification':'standard_P104_only','period_upper_bound':168,
       'wake_assignments':256,'boundary_parity_exclusions':128,'phase_mod4_exclusions':88,
       'fully_enumerated_masks':40,'full_search_prefixes':sum(r['prefixes'] for r in results),
       'accepted_masks':[92,163],'geometric_classes_up_to_translation':1,
       'generated_search_sha256':source_hash,'prerequisite_sha256':PINS,
       'trust_boundary':'analytic coverage plus exact enumeration; not a Lean theorem or independent peer review'}
    write_json(output/'summary.json',summary)
    print(json.dumps(summary,indent=2));print('Evidence directory:',output)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=4)
    parser.add_argument('--seconds',type=float,default=240)
    parser.add_argument('--nodes',type=int,default=1000000000)
    parser.add_argument('--output',help='New directory, which must not already exist')
    main(parser.parse_args())
