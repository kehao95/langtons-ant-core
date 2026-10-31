"""Scoped exact checks for sparse-source trace complexity and topology.

Default execution compares a frozen report and never modifies it. --write is
an explicit generation mode. Analytic arguments, not these finite samples,
establish the all-m asymptotic exponent and Cantor--Bendixson derivative.
"""
from __future__ import annotations
from collections import Counter
from copy import deepcopy
import argparse
import hashlib
from itertools import product, combinations
import json
from math import comb
from pathlib import Path
import random
import subprocess
import tempfile
from core import (DIR, Run, decode, first_black_code, kernel, move, positive_lower,
                  predicted_endpoint, predicted_word, prefix_upper, simulate,
                  source, translate, verify_kernel)
HERE=Path(__file__).resolve().parent

def digest(raw):return hashlib.sha256(raw).hexdigest()

def finite_tree():
    # Complete branching only at fresh cells. Neither coordinates nor replay
    # time is used as an extra pruning rule beyond the stated finite controls.
    hist=[Counter()for _ in range(25)];codes={};checked=0
    def visit(word,B,seen,p,h,cost,times):
        nonlocal checked
        depth=len(word);hist[depth][cost]+=1
        if depth==24:
            code=tuple(times)
            if code in codes:raise AssertionError('first-black encoding not injective')
            codes[code]=word
            restored=decode(depth,code)
            if restored.word!=word or restored.field!=B or(restored.head,restored.heading)!=(p,h):
                raise AssertionError('exact decoding failed')
            ts,M=first_black_code(word)
            literal=simulate(M,depth)
            if ts!=code or literal!=restored:raise AssertionError('minimal seed mismatch')
            checked+=1;return
        options=[int(p in B)]if p in seen else([0,1]if cost<3 else[0])
        for b in options:
            fresh=p not in seen;bb=set(B)
            if fresh and b:bb.add(p)
            bb.symmetric_difference_update({p});hh=(h+(3 if b else 1))%4
            visit(word+('L'if b else'R'),bb,seen|{p},move(p,hh),hh,
                  cost+int(fresh and b),times+[depth]if fresh and b else times)
    visit('',set(),set(),(0,0),0,0,[])
    table=[]
    for n,c in enumerate(hist):
        row=[sum(v for r,v in c.items()if r<=m)for m in range(4)]
        if any(row[m]>prefix_upper(n,m)for m in range(4)):raise AssertionError('upper bound')
        table.append(row)
    return {'full_depth':24,'source_budget':3,'complete_leaf_decodings':checked,
            'prefix_counts_by_depth_m0_to_m3':table,
            'code_table_sha256':digest(json.dumps(sorted(codes.items()),separators=(',',':')).encode())}

def cases():
    w=kernel();trial=[]
    for size in range(9):
        for bits in product((0,1),repeat=size):
            steps=w['t0']+208*size+20*sum(bits)
            trial.append((source(bits,w),(0,0),0,steps,tuple(bits)))
    cells=[(x,y)for x in range(-1,2)for y in range(-1,2)]
    for mask in range(512):
        B={p for i,p in enumerate(cells)if mask>>i&1}
        trial.append((B,(0,0),mask%4,192,None))
    rng=random.Random(20261030)
    for i in range(40):
        B={(rng.randrange(-8,9),rng.randrange(-8,9))for _ in range(rng.randrange(20))}
        B.add((10**9+i,-10**9))
        trial.append((B,(rng.randrange(-3,4),rng.randrange(-3,4)),rng.randrange(4),500,None))
    return trial

def literal_controls():
    w=kernel();blank,kreport=verify_kernel(w);trial=cases();lines=[str(len(trial))]
    for B,p,h,n,bits in trial:
        lines.append(f'{p[0]} {p[1]} {h} {n} {len(B)}')
        lines.extend(f'{x} {y}'for x,y in sorted(B))
    with tempfile.TemporaryDirectory(prefix='sparse-trace-')as td:
        td=Path(td);exe=td/'oracle';inp=td/'input.txt';inp.write_text('\n'.join(lines)+'\n')
        subprocess.run(['g++','-O2','-std=c++17',str(HERE/'oracle.cpp'),'-o',str(exe)],check=True)
        native=subprocess.run([str(exe),str(inp)],check=True,capture_output=True,text=True,timeout=120)
    output=native.stdout.splitlines()
    if len(output)!=4*len(trial):raise AssertionError('incomplete native output')
    actual_updates=codecases=macrochecks=0;stream=hashlib.sha256();topology_controls=0
    sample_prefixes={}
    for i,(B,p,h,n,bits)in enumerate(trial):
        rr=simulate(B,n,p,h);header=list(map(int,output[4*i].split()))
        if header!=[i,*rr.head,rr.heading,len(rr.field)]or output[4*i+1]!=rr.word:
            raise AssertionError('literal pose/read stream mismatch')
        coords=list(map(int,output[4*i+2].split()))
        if list(zip(coords[::2],coords[1::2]))!=sorted(rr.field):
            raise AssertionError('COMPLETE endpoint mismatch')
        seen=set();mark=[]
        for t,q in enumerate(rr.reads):
            if q not in seen and q in B:mark.append(t)
            seen.add(q)
        if list(map(int,output[4*i+3].split()))!=mark:raise AssertionError('independent first-black times')
        actual_updates+=n;stream.update(rr.word.encode())
        if bits is not None:
            pred=predicted_endpoint(bits,blank,w)
            if rr.word!=blank.word+pred.word or rr.field!=pred.field or(rr.head,rr.heading)!=(pred.head,pred.heading):
                raise AssertionError('complete all-block induction control')
            ts,M=first_black_code(rr.word)
            expected=tuple(w['t0']+208*j+20*sum(bits[:j])+13 for j,b in enumerate(bits)if b)
            if ts!=expected or M!=B:raise AssertionError('source symbols are not all first black')
            if len(rr.field)!=835+24*len(bits)+sum(bits):raise AssertionError('complete mass')
            codecases+=1;macrochecks+=len(bits)
            if len(bits)==8:sample_prefixes[bits]=rr.word
    # All pairs of length-eight binary sources: their first actual turn
    # disagreement equals the exact decoding formula, not just a hash.
    pairchecks=0
    for a,b in combinations(sample_prefixes,2):
        j=next(i for i in range(8)if a[i]!=b[i])
        first=w['t0']+208*j+20*sum(a[:j])+13
        wa,wb=sample_prefixes[a],sample_prefixes[b]
        if wa[:first]!=wb[:first]or wa[first]==wb[first]:raise AssertionError('first disagreement')
        pairchecks+=1
    # Fresh first-read perturbations approaching unrelated finite-source traces.
    for i in range(32):
        B={(i%5-2,i%7-3)}if i else set()
        rr=simulate(B,3000)
        seen=set(rr.reads[:100+i]);t=100+i
        while t<len(rr.reads)and(rr.reads[t]in seen or rr.reads[t]in B):
            seen.add(rr.reads[t]);t+=1
        if t==len(rr.reads):raise AssertionError('finite fresh-site control failed')
        q=rr.reads[t];alt=simulate(B|{q},t+1)
        if alt.word[:t]!=rr.word[:t]or alt.word[t]==rr.word[t]:raise AssertionError('late divergence')
        topology_controls+=1
    return {'kernel':kreport,'complete_inputs':len(trial),'literal_updates_per_implementation':actual_updates,
            'complete_endpoint_comparisons':len(trial),'positive_code_inputs':codecases,
            'coded_blocks':macrochecks,'first_disagreement_pairs':pairchecks,
            'fresh_site_accumulation_controls':topology_controls,'turn_stream_sha256':stream.hexdigest()}

def other_controls():
    w=kernel();rejected=0
    for bad in ('RRRRR','LRX'):
        try:first_black_code(bad)
        except ValueError:rejected+=1
        else:raise AssertionError('bad word accepted')
    for n,ts in ((8,(4,)),(2,(1,1)),(2,(-1,)),(2,(2,))):
        try:decode(n,ts)
        except ValueError:rejected+=1
        else:raise AssertionError('bad code accepted')
    for kind in ('word','residue','front','marker'):
        b=deepcopy(w)
        if kind=='word':b['S']=b['S'][:-1]+('R'if b['S'][-1]=='L'else'L')
        if kind=='residue':b['Sres'].remove(min(b['Sres']))
        if kind=='front':b['C'].add((10,0))
        if kind=='marker':b['q']=(99,99)
        try:verify_kernel(b)
        except (AssertionError,ValueError):rejected+=1
        else:raise AssertionError('damaged kernel accepted')
    large=0
    for m in range(21):
        for n in (0,20,11017,10**6,10**60):
            lo=positive_lower(n,m);hi=prefix_upper(n,m)
            if lo>hi:raise AssertionError('combinatorial bounds cross')
            large+=1
    # This checks symbolic timing/geometry identities only, not huge replay.
    big=10**60
    bits={big,2*big+7,10*big}
    for j,i in enumerate(sorted(bits)):
        q=source([1],w).pop();p=q[0]-4*i,q[1]-4*i
        if sum(p)!=sum(q)-8*i:raise AssertionError('large-coordinate guard')
        if w['t0']+208*i+20*j+13<=208*i:raise AssertionError('large time')
    return {'malformed_controls_rejected':rejected,'large_exact_combinatorial_checks':large,
            'huge_slot_symbolic_checks':len(bits),'huge_slot_literal_simulation_claimed':False}

def run():
    if not __debug__:raise RuntimeError('run verifier without Python -O')
    tree=finite_tree();print('finite first-read tree checked',flush=True)
    literals=literal_controls();print('independent complete-field controls checked',flush=True)
    other=other_controls()
    return {'schema':'sparse-trace-space-v1','status':'scoped_checks_passed',
            'analytic_targets':['all-m polynomial prefix exponent m','derived set T_m prime equals T_(m-1)',
                                'full-complexity compact subfamily of eventual-standard inputs'],
            'all_input_HC_proved':False,'publication_or_external_review_claimed':False,
            'finite_tree':tree,'literal_controls':literals,'negative_and_large_controls':other,
            'source_sha256':{name:digest((HERE/name).read_bytes())for name in ('core.py','check.py','oracle.cpp','witness.json')}}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',type=Path)
    args=parser.parse_args();result=run()
    if args.write:
        args.write.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print('WROTE report; not a comparison pass')
    else:
        if result!=json.loads((HERE/'report.json').read_text()):raise AssertionError('frozen report mismatch')
        print('PASS: sparse-source trace checks; infinite claims rely on the analytic proof')
