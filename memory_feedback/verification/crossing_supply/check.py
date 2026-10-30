"""Scoped exact checks of request-only crossing capacity; no HC claim.

The old crossing module is pinned, not modified. Default mode compares the
frozen report. --write PATH explicitly creates a new report before review.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
import hashlib
import importlib.util
from itertools import product
import json
from math import factorial
from pathlib import Path
import random
import subprocess
import sys
import tempfile

from core import incoming_key, request_capacity, request_count, request_packing, reconstruct_right

HERE = Path(__file__).resolve().parent
PINS = {
    'core.py': '0d033be9fa0d8e7f59df0013f2ee3bd7b20c926c30d643b47550b9ae1c8ed5e3',
    'oracle.cpp': '7d9da953dc64eae2e79fb594f7c877c5863f259773f86dce488cb588e15f8d13',
}


def baseline():
    root = HERE.parent/'crossing_gap'
    for name, digest in PINS.items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest() != digest:
            raise AssertionError('changed baseline needs a new audit: '+name)
    spec = importlib.util.spec_from_file_location('crossing_gap_prior', root/'core.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod, root


def native_cases(prior, source_dir, cases):
    lines = [str(len(cases))]
    for source, T in cases:
        lines.append(f'{len(source.black)} {source.head[0]} {source.head[1]} {source.heading} {T}')
        lines.extend(f'{x} {y}' for x, y in sorted(source.black))
    with tempfile.TemporaryDirectory(prefix='request-crossing-native-') as temp:
        exe = Path(temp)/'oracle'
        subprocess.run(['g++','-O2','-std=c++17',str(source_dir/'oracle.cpp'),'-o',str(exe)],check=True)
        out = subprocess.check_output([str(exe)],input='\n'.join(lines)+'\n',text=True,timeout=45).splitlines()
    if len(out) != 4*len(cases):
        raise AssertionError('incomplete native output')
    paths = []
    for i,(source,T) in enumerate(cases):
        meta = list(map(int,out[4*i].split()))
        word = '' if out[4*i+1]=='-' else out[4*i+1]
        a = list(map(int,out[4*i+2].split())); B = set(zip(a[::2],a[1::2]))
        a = list(map(int,out[4*i+3].split())); ps = list(zip(a[::2],a[1::2]))
        w, pp, end = prior.trace(source,T)
        if word != w or ps != pp or B != end.black or meta != [i,*end.head,end.heading,len(B)]:
            raise AssertionError('independent complete replay differs')
        paths.append((w,ps,end))
    return paths


def run():
    prior, root = baseline()
    combinations = identities = 0
    for height in range(1,11):
        q = height//2+1
        for pairs in range(5):
            observed = 0
            for code in product(range(q), repeat=pairs+1):
                observed += min(code)==0
                combinations += 1
            if observed != request_count(height,pairs):
                raise AssertionError('request-code count mismatch')
            identities += 1
    capacity_checks = packing_checks = improvements = entropy_checks = 0
    for H in range(17):
        weights = []
        total = 0
        for j in range(12):
            count = request_count(H,j); total += count
            if request_capacity(H,j) != total:
                raise AssertionError('sum identity failed')
            if count > prior.signature_count(H,j):
                raise AssertionError('new upper count exceeds old count')
            improvements += count < prior.signature_count(H,j)
            capacity_checks += 1
            weights += [2*j+1] * min(count,120)
        weights.sort()
        for number in range(min(90,len(weights))+1):
            expected = sum(weights[:number])
            actual = request_packing(H,number)
            if actual != expected:
                raise AssertionError(('packing differs',H,number,actual,expected))
            packing_checks += 1
        if H>=2:
            q=H//2+1
            for number in range(1,90):
                length=request_packing(H,number); J=(length-number)//2
                # Exact exponentiated entropy inequality, no floating point.
                if factorial(number)*number**number > q**J * (2*(J+number))**number:
                    raise AssertionError('integer entropy inequality failed')
                entropy_checks += 1
    if request_packing(0,2) is not None or request_packing(1,10**60)!=(10**60)**2:
        raise AssertionError('zero/one-height control failed')

    rng=random.Random(20261030)
    cases=[]
    for i in range(72):
        B={(rng.randrange(-5,6),rng.randrange(-5,6))for _ in range(rng.randrange(0,18))}
        cases.append((prior.State(B,(0,0),i%4),256+(i%4)*128))
    # The empty source is turned south so its known tail advances rightward.
    for T in (2000,9000,10000,10391,11000,12000):
        cases.append((prior.State(set(),(0,0),2),T))
    trajectories=native_cases(prior,root,cases)
    key_to_record={}; response_fields=local_work=record_pairs=prefix_bounds=certified=0
    larger_packing=0
    certificates=[]
    for (source,T),(word,ps,end) in zip(cases,trajectories):
        frontier=max([source.head[0]]+[p[0]for p in source.black])
        records=prior.crossing_records(ps)
        valid=[];keys={};pair=None
        for cut in range(frontier,end.head[0]):
            rec=records[cut];key=incoming_key(rec);sig=prior.signature(rec)
            low=min(y for _,_,y in rec[::2])
            canonical=tuple((direction,y-low)for _,direction,y in rec)
            if key in key_to_record:
                if key_to_record[key]!=canonical:
                    raise AssertionError('genuine input key has two outputs')
            else:key_to_record[key]=canonical
            B,p,v,steps=reconstruct_right(rec,cut,T,cap=T+1)
            if B != {q for q in end.black if q[0]>cut} or p!=end.head or v!=prior.DIR[end.heading]:
                raise AssertionError('complete residual half-plane reconstruction failed')
            response_fields+=1;local_work+=steps
            for oldcut,oldrec,oldkey,oldsig in valid:
                if (key==oldkey)!=(sig==oldsig):
                    raise AssertionError('request equality/full-record equality differ')
                record_pairs+=1
            if key in keys and pair is None:pair=keys[key],cut
            keys[key]=cut
            valid.append((cut,rec,key,sig))
        if not valid:continue
        if pair is not None:
            cert,s=prior.verify_pair(source,T,*pair)
            if not prior.periodic_future(s,cert['word']):
                raise AssertionError('full-field infinite lasso control failed')
            certified+=1;certificates.append({'T':T,**cert})
        else:
            H=max(max(y for _,_,y in rec)-min(y for _,_,y in rec)for _,rec,_,_ in valid)
            needed=request_packing(H,len(valid))
            if needed is None or needed>(T+1)//2:
                raise AssertionError('new actual-prefix inequality failed')
            old=prior.packing_cost(H,len(valid))
            larger_packing += needed>old
            prefix_bounds+=1

    # Exact retained-history test: two calls from the same boundary location.
    good=[(1,1,0),(3,-1,-1),(5,1,0)]
    B,p,v,work=reconstruct_right(good,0,5)
    if B!={(1,0),(1,-1)} or p!=(1,0) or work!=2:
        raise AssertionError('first complete response incorrect')
    extended=good+[(11,-1,1),(13,1,0)]
    B,p,v,work=reconstruct_right(extended,0,13)
    if len(B)!=4 or work!=8:
        raise AssertionError('second call lost the first-call writes')
    negative=0
    for fn in [lambda:reconstruct_right([(1,1,0),(3,-1,1),(5,1,0)],0,5),
               lambda:reconstruct_right(good,0,5,cap=0),
               lambda:incoming_key([(1,1,0),(3,-1,-1),(5,1,1)]),
               lambda:request_count(True,1),lambda:request_packing(2,-1)]:
        try:fn()
        except (ValueError,RuntimeError):negative+=1
        else:raise AssertionError('negative control accepted')
    if not certificates:raise AssertionError('no positive guarded control')
    cert=certificates[-1]
    try:prior.verify_pair(prior.State({(10**60,0)},(0,0),2),cert['T'],cert['left'],cert['right'])
    except ValueError:negative+=1
    else:raise AssertionError('far initial black source ignored')

    # Explicit numerical compatibility: not a constructed ant trajectory.
    numeric=0
    for n in range(2,250):
        if request_packing(2*n,n)!=3*n-2 or request_packing(2*n,n)>6*n//2:
            raise AssertionError('compatibility example changed')
        numeric+=1
    for v in (Fraction(1,100),Fraction(1,52),Fraction(1,20),Fraction(1,6)):
        new=4*v/(1-2*v)
        if new<=2*v:raise AssertionError('asymptotic algebra failed')
    report={
      'schema':'crossing-request-capacity-v1','status':'passed',
      'base_commit':'de342f553520c0e003bcc83c2a6ae6d4b9e80a75',
      'scope':'analytic request-injectivity and finite-prefix upper capacity; no total fuel budget or HC proof',
      'baseline_sha256':PINS,
      'combinatorics':{'tuples_enumerated':combinations,'count_identities':identities,
                      'capacity_checks':capacity_checks,'packing_checks':packing_checks,
                      'strict_layer_improvements':improvements,'integer_entropy_checks':entropy_checks,
                      'inequality_compatibility_controls_not_ant_trajectories':numeric},
      'physical_controls':{'complete_inputs':len(cases),'updates_per_literal_implementation':sum(T for _,T in cases),
            'complete_endpoints_compared':len(cases),'full_halfplane_residual_comparisons':response_fields,
            'independent_halfplane_updates':local_work,'pairwise_key_equivalence_checks':record_pairs,
            'distinct_observed_request_keys':len(key_to_record),'nonrepeating_prefix_inequalities':prefix_bounds,
            'strict_packing_improvements_on_controls':larger_packing,'guarded_infinite_certificates':certified},
      'negative_controls':negative,
      'example_capacity_H10_length11':{'old_parity_only':prior.signature_count(10,5),
                                        'new_request_upper':request_count(10,5)},
      'source_sha256':{p:hashlib.sha256((HERE/p).read_bytes()).hexdigest()for p in ('core.py','check.py')},
      'blank_certificate':certificates[-1],
      'general_halfplane_return_decider_implemented':False,
      'HC_proved':False}
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path)
    args=parser.parse_args();report=run()
    if args.write:
        args.write.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
        print('WROTE report; run default comparison separately')
    else:
        if report!=json.loads((HERE/'report.json').read_text()):
            raise AssertionError('frozen report differs; not overwritten')
        print('PASS: request-capacity checks, not a global termination proof')
    print(json.dumps(report,indent=2,sort_keys=True))
