"""Rebuild all-parameter and finite-complement certificates.

The default compares report.json without writing it. --write PATH explicitly
creates a report. No finite parameter test is used as the all-parameter proof.
"""
from __future__ import annotations
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import random
import subprocess
import tempfile
import time
import affine
import core
import literal
import order_oracle
from affine import Aff,Field,ZERO,ONE

HERE=Path(__file__).resolve().parent

def digest(x):return hashlib.sha256(x).hexdigest()
def pack(B):return [list(p)for p in sorted(B)]

def six_kernels():
    K='RLRLRRRRLLLLRLLRLRLLRLLRLRRLLR';E='RLRLRRRRLLLLRLLR'
    rows=[(core.A,(0,3,1),'RLLR',core.B,(2,3,1)),
          (core.B,(1,2,3),'RLLR',core.A,(-1,2,3)),
          (core.C+core.V,(0,3,1),K,core.A+core.C,(-1,2,3)),
          (core.C,(0,3,1),E,core.B+(10,18),(4,1,1)),
          ((5,),(0,2,1),'LR',(9,),(1,3,1)),
          ((9,),(0,2,3),'RL',(5,),(-1,3,3))]
    for columns,pose,word,target,end in rows:
        s=literal.State(core.black_field(columns),pose)
        for c in word:
            if not(0<=s.x<len(columns)and 0<=s.y<5):raise AssertionError('kernel left prematurely')
            if s.step()!=c:raise AssertionError('kernel turn')
        if s.pose!=end or s.black!=core.black_field(target):raise AssertionError('complete kernel endpoint')
    return {'kernels':len(rows),'literal_updates':sum(len(r[2])for r in rows),
            'attribution':'persistent-boundary-memory.md, inherited six kernels and first-exit composition'}


def all_parameter(w):
    expected={'east-0':[40,1031],'east-1':[32,883],'east-2':[32,799],
              'west-1':[72,1427],'west-2':[128,2611],'west-3':[144,3011],
              'west-4':[176,3658],'west-5':[176,3678],'west-6':[176,3570]}
    if set(w['all_parameter_schemata'])!=set(expected):raise AssertionError('coverage schema missing')
    results={};counts=Counter();oracle_counts=Counter();field_digests={}
    primary=affine.zero_on_epochs
    for name,record in w['all_parameter_schemata'].items():
        result,F,footprint=core.verify_schema(record)
        if result['time']!=expected[name]:raise AssertionError('wrong formula')
        fields=result['full_field'];field_digests[name]=digest(json.dumps(fields,separators=(',',':')).encode())
        counts.update(result['proof_counts']);results[name]={k:v for k,v in result.items()if k!='full_field'}
        try:
            affine.zero_on_epochs=core.zero_on_epochs=order_oracle.zero_on_epochs
            alt,FF,footprint2=core.verify_schema(record)
        finally:affine.zero_on_epochs=core.zero_on_epochs=primary
        if {k:v for k,v in result.items()if k!='proof_counts'}!={k:v for k,v in alt.items()if k!='proof_counts'}:
            raise AssertionError('independent order-cover proof differs')
        oracle_counts.update(alt['proof_counts'])
    # Domain exhaustiveness is symbolic and explicitly encoded: three right-exit
    # cones and six left-exit cones for l>=9; only l=0..8 remains on the left.
    for name,sc in w['all_parameter_schemata'].items():
        mode,d=name.split('-');d=int(d)
        wanted=2 if name=='east-0'else 0 if mode=='east'else 9
        if (sc['mode'],sc['d'],sc['kmin'])!=(mode,d,wanted):raise AssertionError('domain mislabel')
    return {'schemata':results,'primary_totals':dict(counts),'independent_order_totals':dict(oracle_counts),
            'complete_affine_endpoint_sha256':field_digests},results


def finite_complement(w):
    table=w['left_exhausted_small_delays']
    if tuple(tuple(r)for r in table)!=core.SMALL or w['balanced_exceptions']!=[11560,940]:
        raise AssertionError('finite complement mismatch')
    cases=[(0,0,11560,False),(1,1,940,False)]
    for l,row in enumerate(table):
        for d,delay in enumerate(row,1):cases.append((l,l+d,delay,d==len(row)))
    totals=Counter();records=[]
    for l,r,delay,screen in cases:
        cols,pose,exit_time=core.after(l,r);s=literal.State(core.black_field(cols),pose);path=[];prev=None
        for _ in range(delay):path.append((s.x,s.y));prev=s.step()
        entered=s.pose;field=set(s.black);word=''.join(s.step()for _ in range(104))
        if word not in core.PHASES or prev==word[-1]or not literal.permanent(field,entered,word):
            raise AssertionError(('finite permanent onset',l,r))
        if screen and not literal.finite_halfstrip_guard(path,entered,word,len(cols),'right'):
            raise AssertionError(('finite extension guard',l,r))
        totals['finite_cases']+=1;totals['updates']+=delay+104;totals['screened_infinite_rows']+=screen
        records.append([l,r,exit_time+delay,list(entered),len(field),digest(json.dumps(pack(field)).encode())])
    return {'totals':dict(totals),'complete_endpoint_records':records}


def independent_literal(w,temppath):
    rng=random.Random(20261030)
    cases={(l,r)for l in range(15)for r in range(15)}
    cases|={(rng.randrange(70),rng.randrange(70))for _ in range(70)}
    cases|={(k+d,k)for k in (0,1,2,9,20,64)for d in (0,1,2,7,50)}
    cases|={(k,k+d)for k in (0,1,2,8,9,20,64)for d in (1,2,3,4,5,6,30)}
    cases|={(0,1000),(1000,0),(257,262),(1000,1000)}
    cases=sorted(cases)
    inp=temppath/'inputs.txt';out=temppath/'native.jsonl';exe=temppath/'independent'
    inp.write_text(str(len(cases))+'\n'+'\n'.join(f'{l} {r} {core.prediction(l,r)[2]}'for l,r in cases)+'\n')
    subprocess.run(['g++','-std=c++17','-O2',str(HERE/'independent.cpp'),'-o',str(exe)],check=True)
    with out.open('w')as f:subprocess.run([str(exe),str(inp)],stdout=f,check=True,timeout=180)
    updates=0;endpoints=0;certificate_count=0
    with out.open()as f:
        for l,r in cases:
            row=json.loads(next(f));T,delay,tau=core.prediction(l,r)
            if(row['l'],row['r'])!=(l,r)or row['first_exit']!=T:raise AssertionError('native input/first exit')
            cols,pose=core.source(l,r);s=literal.State(core.black_field(cols),pose)
            exit_cols,exit_pose,_=core.after(l,r);turns=row['turns']
            if len(turns)!=tau+104:raise AssertionError('truncated literal trace')
            entry=None;entry_pose=None
            for t,c in enumerate(turns):
                if s.step()!=c:raise AssertionError(('independent trace',l,r,t))
                if t+1==T:
                    if s.pose!=exit_pose or pack(s.black)!=row['exit_field']or s.black!=core.black_field(exit_cols):
                        raise AssertionError('complete first-exit field')
                    endpoints+=1
                if t+1==tau:
                    entry=set(s.black);entry_pose=s.pose
                    if pack(entry)!=row['entry_field']or list(entry_pose)!=row['entry_pose']:
                        raise AssertionError('complete entrance field')
                    endpoints+=1
            tail=turns[-104:]
            if turns[tau-1]==tail[-1]or tail not in core.PHASES or not row['tail_accepted']:
                raise AssertionError('native sharp standard certificate')
            if not literal.permanent(entry,entry_pose,tail):raise AssertionError('Python infinite tail')
            updates+=len(turns);certificate_count+=1
        if f.read().strip():raise AssertionError('extra native cases')
    return {'complete_inputs':len(cases),'updates_per_implementation':updates,
            'full_turn_stream_comparisons':len(cases),'complete_field_comparisons':endpoints,
            'independent_infinite_certificates_per_implementation':certificate_count,
            'largest_balanced_counter':1000,'case_list_sha256':digest(inp.read_bytes())}


def negative_and_arithmetic(w):
    rng=random.Random(104104);comparisons=0;failures=0
    for _ in range(1200):
        domain=rng.randrange(4);count=Aff(rng.randrange(4),rng.randrange(1,6))
        edges={Aff(rng.randrange(-3,4),rng.randrange(-8,9))for _ in range(rng.randrange(8))}
        outcomes=[]
        for check in (affine.zero_on_epochs,order_oracle.zero_on_epochs):
            try:check(edges,count,domain);outcomes.append(True)
            except AssertionError:outcomes.append(False)
        if outcomes[0]!=outcomes[1]:raise AssertionError('independent affine decision disagreement')
        if outcomes[0]:
            for k in range(domain,domain+12):
                for j in range(count(k)):
                    if sum(j>=e(k)for e in edges)%2:raise AssertionError('accepted arithmetic counterexample')
        comparisons+=1
    def rejected(fun):
        nonlocal failures
        try:fun()
        except (AssertionError,ValueError):failures+=1
        else:raise AssertionError('damaged proof accepted')
    sc=w['all_parameter_schemata']['east-0']
    damaged=copy.deepcopy(sc);word=damaged['stages'][0]['word'];damaged['stages'][0]['word']=('L'if word[0]=='R'else'R')+word[1:]
    rejected(lambda:core.verify_schema(damaged))
    damaged=copy.deepcopy(sc);damaged['kmin']=0;rejected(lambda:core.verify_schema(damaged))
    damaged=copy.deepcopy(sc);damaged['tail']='R'+damaged['tail'][1:]if damaged['tail'][0]=='L'else'L'+damaged['tail'][1:]
    rejected(lambda:core.verify_schema(damaged))
    damaged=copy.deepcopy(sc);damaged['tail']=damaged['tail'][1:]+damaged['tail'][0];rejected(lambda:core.verify_schema(damaged))
    damaged=copy.deepcopy(sc);damaged['stages'][1]['b']+=1;rejected(lambda:core.verify_schema(damaged))
    result,F,_=core.verify_schema(sc);k=2;pose=(result['head_x'][0]*k+result['head_x'][1],result['head_y'],result['heading'])
    full=F.evaluate(k);q=(pose[0]-2*10**60,pose[1]+2*10**60);full.symmetric_difference_update({q})
    if literal.permanent(full,pose,sc['tail']):raise AssertionError('far future blocker ignored')
    failures+=1
    # Prove the all-m upper bound symbolically, rather than sample m.
    table=[core.max_entry_at_minimum(m)for m in range(9)]
    if any(t>8*m*m+244*m+17154 for m,t in enumerate(table))or table[0]!=17154:
        raise AssertionError('sharp uniform intercept')
    large_max_checks=0
    for name,sc in w['all_parameter_schemata'].items():
        a=sum(len(item['word'])*item['a'] for item in sc['stages'])
        b=sum(len(item['word'])*item['b'] for item in sc['stages'])
        entry_rest=Aff(a+(60 if sc['mode']=='east'else 68),b+(16 if sc['mode']=='east'else 48))
        affine.nonnegative(Aff(244,3726)-entry_rest,9)
        if name=='west-5' and entry_rest!=Aff(244,3726):raise AssertionError('sharp extremizer')
        large_max_checks+=1
    if 3726>17154:raise AssertionError('large-m intercept')
    huge=10**60
    if core.prediction(huge,huge+5)[2]!=8*huge*huge+244*huge+3726:raise AssertionError('huge integer formula')
    for bad in ((-1,0),(True,1),(0,1.5)):
        rejected(lambda bad=bad:core.prediction(*bad))
    return {'independent_affine_kernel_comparisons':comparisons,'rejected_controls':failures,
            'far_blocker_periods':'10^60','huge_parameter_is_evaluation_not_simulation':True,
            'exact_max_entry_for_minimum_0_to_8':table,'unbounded_maximum_comparisons':large_max_checks}


def protected_payload_controls():
    """Whole-history comparison with arbitrary finite unseen payloads.

    This supplements, not replaces, the exact half-strip guards. Payloads are
    supplied to the original input, not inserted at a later checkpoint.
    """
    cases=((5,3,'left'),(9,15,'right'),(8,14,'right'))
    updates=0
    for l,r,side in cases:
        cols,pose=core.source(l,r);width=len(cols)
        payload={(x,y)for x in ((-1,-3,-10**60)if side=='left'else(width,width+7,10**60))
                 for y in (0,2,4)}
        initial=core.black_field(cols)
        if payload&initial:raise AssertionError('payload overlaps the complete common source')
        a=literal.State(initial,pose);b=literal.State(initial^payload,pose)
        tau=core.prediction(l,r)[2];tail=[];entry=None
        for t in range(tau+104):
            if (a.x,a.y)in payload:raise AssertionError('guarded payload was read')
            ca,cb=a.step(),b.step()
            if ca!=cb or a.pose!=b.pose:raise AssertionError('full trace clipping failed')
            if t+1==tau:entry=(set(b.black),b.pose)
            if t>=tau:tail.append(cb)
        if a.black^b.black!=payload:raise AssertionError('complete residual payload not preserved')
        if not literal.permanent(entry[0],entry[1],''.join(tail)):
            raise AssertionError('protected payload alters infinite future')
        updates+=tau+104
    return {'complete_sources':len(cases),'updates_per_python_trace':updates,
            'payload_coordinate_scale':'10^60','complete_residual_differences_preserved':True}


def standard_control():
    if len(core.W)!=104 or any(core.W==core.W[:d]*(104//d)for d in range(1,104)if 104%d==0):
        raise AssertionError('standard word not primitive of length104')
    s=literal.State(set(),(0,0,0))
    for _ in range(12000):s.step()
    B=set(s.black);pose=s.pose;word=''.join(s.step()for _ in range(104))
    if word not in core.PHASES or not literal.permanent(B,pose,word):raise AssertionError('standard identification')
    return {'blank_prefix':12000,'permanent_period':104}


def run():
    w=json.loads((HERE/'witness.json').read_text())
    if w['base_commit']!='80a96531f26dcc361ebfa1bef47b0e6953c29b77':raise AssertionError('baseline attribution')
    small=six_kernels();std=standard_control();proof,_=all_parameter(w)
    print('all nine infinite domains: BOTH exact arithmetic kernels passed',flush=True)
    finite=finite_complement(w);negative=negative_and_arithmetic(w);payload=protected_payload_controls()
    print('finite complement and unlimited-column guards passed',flush=True)
    with tempfile.TemporaryDirectory(prefix='counter-basin-')as folder:controls=independent_literal(w,Path(folder))
    files=('affine.py','core.py','literal.py','order_oracle.py','independent.cpp','check.py','witness.json','query.py')
    return {'schema':'counter-highway-basin-report-v1','status':'passed',
            'base_commit':w['base_commit'],'inherited_kernels':small,'standard_identity_control':std,
            'all_parameter_proof':proof,'finite_complement':finite,'native_literal_controls':controls,
            'negative_and_arithmetic':negative,'protected_payload_controls':payload,'full_HC_proved':False,
            'general_scope':'all nonnegative counter pairs in the explicitly specified complete source family',
            'trust':'unformalized analytic composition plus two exact integer arithmetic kernels and independent literal controls',
            'source_sha256':{p:digest((HERE/p).read_bytes())for p in files}}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',type=Path);args=parser.parse_args()
    report=run()
    if args.write:args.write.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print('WROTE candidate report',args.write)
    else:
        expected=json.loads((HERE/'report.json').read_text())
        if expected!=report:raise AssertionError('frozen report mismatch (not overwritten)')
        print('PASS: complete two-parameter basin certificate')
