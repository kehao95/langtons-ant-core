"""Scoped exact controls for the written all-state cocycle classification.

Default execution reconstructs and compares report.json without changing it.
--write is explicit generation, not a claimed comparison pass. No HC result,
external review, or exhaustive classification of arbitrary joint invariants.
"""
from __future__ import annotations
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import subprocess
import tempfile

from core import (DIRECTIONS, canonical, classical_clock, clock, coefficients,
                  compact_charge, edge_increments, field_term, maximal_period,
                  pose_potential_counts, pose_term, prefix_counts, sector_of)
from linear_audit import compact_rank, compact_smith, phase_order

HERE=Path(__file__).resolve().parent


def all_rules(maximum):
    return [''.join(w)for n in range(1,maximum+1)for w in product('RL',repeat=n)]


def local_audit():
    transitions=periods=cycle_checks=face_checks=0
    for rule in all_rules(8):
        n,r=len(rule),rule.count('R');m=maximal_period(rule)
        for x,y in product(range(4),repeat=2):
            a,b,_=coefficients(n,r,(x,y));d=a-b
            assert (2*d)%m==0 and (r*a+(n-r)*b)%m==0
            cycle_checks+=1
            cell_sum=sum(coefficients(n,r,(xx,yy))[int((x+y)%2==0)]
                         for xx,yy in ((x,y),(x+1,y),(x,y+1),(x+1,y+1)))
            assert (cell_sum-4)%m==0
            face_checks+=1
            for h in range(4):
                if (h-x-y)%2:continue
                f=pose_potential_counts(n,r,(x,y,h))
                assert f==pose_potential_counts(n,r,(x+4,y,h))==pose_potential_counts(n,r,(x,y+4,h))
                periods+=1
                for c,ch in enumerate(rule):
                    cc=(c+1)%n;hh=(h+(1 if ch=='R'else-1))%4;dx,dy=DIRECTIONS[hh]
                    change=(field_term(rule,(x,y),cc,0)-field_term(rule,(x,y),c,0)
                            +pose_potential_counts(n,r,(x+dx,y+dy,hh))-f)
                    assert change%m==1
                    transitions+=1
    huge_checks=0
    for n in (2,3,4,5,6,7,8,13,64,101,10**60+2):
        for r in sorted({1,n//2,n-1}):
            for x,y in ((0,0),(1,0),(-3,7),(10**60+1,-10**60+3)):
                a,b,m=coefficients(n,r,(x,y));assert (2*(a-b))%m==0 and (r*a+(n-r)*b)%m==0
                for h in range(4):
                    if (h-x-y)%2:continue
                    for ch,z in (('R',a),('L',b)):
                        hh=(h+(1 if ch=='R'else-1))%4;dx,dy=DIRECTIONS[hh]
                        delta=z+pose_potential_counts(n,r,(x+dx,y+dy,hh))-pose_potential_counts(n,r,(x,y,h))
                        assert delta%m==1;huge_checks+=1
    # A lifted version of the explicit classical formula fails at modulus 32.
    # This one control is not a proof against other formulae; maximality is analytic.
    black_weight=-4
    old_phi=10  # (1,1),S
    new_phi=-1 # (0,1),W
    assert (black_weight+new_phi-old_phi)%16==1
    assert (black_weight+new_phi-old_phi)%32==17
    # Nonlinear pair interaction: the same read at the origin has two distinct
    # field increments according to an unread distant color.
    distant=(10**60,0)
    fun=lambda B:int((0,0)in B and distant in B)
    changes=[fun(B^{(0,0)})-fun(B)for B in (set(),{distant})]
    assert changes==[0,1]
    invalid=0
    for thunk in (lambda:maximal_period(''),lambda:maximal_period('RX'),
                  lambda:coefficients(0,0,(0,0)),lambda:clock('RL',{(0,0):2},(0,0,0)),
                  lambda:compact_charge('RL','R',(0,0),{},(0,0,0)),
                  lambda:compact_charge('RRL','R',(1,0),{},(0,0,0)),
                  lambda:compact_charge('RRL','R',(0,0),{},(0,0,1))):
        try:thunk()
        except ValueError:invalid+=1
        else:raise AssertionError('invalid construction accepted')
    return {'rules':len(all_rules(8)),'color_transition_equalities':transitions,
            'four_period_pose_equalities':periods,'color_cycle_relations':cycle_checks,
            'face_relations':face_checks,'huge_integer_local_equalities':huge_checks,
            'mod32_naive_lift_detected':True,'nonlinear_pair_increment_conflict':changes,
            'invalid_inputs_rejected':invalid}


def linear_checks():
    records=[];compact_boxes=compact_eqs=0
    for rule in all_rules(8):
        if len(set(rule))!=2:continue
        for side in (3,4):
            result=compact_rank(rule,side);compact_boxes+=1;compact_eqs+=result['raw_equations']
    # Separate raw all-color periodic presentations, not the derived R/L reduction.
    selected={'R'*r+'L'*(n-r)for n in range(1,9)for r in range(n+1)}
    selected.update(all_rules(4));selected.update(('RLRLRL','RRLLRRLL','RLRLRLRL'))
    for rule in sorted(selected,key=lambda w:(len(w),w)):
        small=phase_order(rule,2);large=phase_order(rule,4)
        assert small==4*len(rule) and large==maximal_period(rule)
        records.append({'rule':rule,'period_two_ansatz_order':small,'period_four_ansatz_order':large})
    compact_integer=[compact_smith(rule,3)for rule in ('RL','LR','RRL','RLL','RRLL','RLRL','RRRL','RRRLLL','RRRRLL','RRRRLLLL')]
    return {'raw_periodic_presentations':2*len(records),'phase_orders':records,
            'compact_binary_boxes':compact_boxes,'compact_binary_raw_equations':compact_eqs,
            'compact_integer_smith':compact_integer,
            'solver':'exact Smith form over Z (SymPy); XOR rank for GF(2)',
            'infinite_plane_maximality_is_from_written_proof':True}


def make_cases():
    rng=random.Random(20261030)
    cases=[]
    for rule in all_rules(7):
        for sector in (0,1):
            for trial in range(3):
                x,y=rng.randrange(-7,8),rng.randrange(-7,8)
                h=(x+y+sector)%2+2*rng.randrange(2)
                field={}
                if len(rule)>1:
                    for _ in range(18):field[rng.randrange(-9,10),rng.randrange(-9,10)]=rng.randrange(1,len(rule))
                    field[(100000+trial,-100000-sector)]=len(rule)-1
                cases.append((rule,field,(x,y,h),256))
    for h in range(4):cases.append(('RL',{},(0,0,h),12000))
    return cases


def run_python(rule,initial,pose,steps):
    field=dict(initial);x,y,h=pose;dx,dy=DIRECTIONS[h];sector=sector_of(pose)
    m=maximal_period(rule);g=4*len(rule)
    start=clock(rule,field,pose);start_common=clock(rule,field,pose,common_field=True)
    acc=sum(field_term(rule,p,c,sector)for p,c in field.items())%m
    acc_common=sum(field_term(rule,p,c,sector,common_field=True)for p,c in field.items())%g
    colors=[];checkpoints=0
    # Check both compact basis orientations where they exist, at unrelated faces.
    generators=[]
    if sector==0 and len(set(rule))==2:
        for turning,face in (('R',(0,0)),('L',(0,1))):
            if rule.count(turning)%2==0:
                generators.append((turning,face,compact_charge(rule,turning,face,field,pose)))
    for t in range(steps):
        p=x,y;c=field.get(p,0);cc=(c+1)%len(rule);colors.append(chr(65+c))
        acc=(acc+field_term(rule,p,cc,sector)-field_term(rule,p,c,sector))%m
        acc_common=(acc_common+field_term(rule,p,cc,sector,common_field=True)-field_term(rule,p,c,sector,common_field=True))%g
        if cc:field[p]=cc
        else:field.pop(p,None)
        dx,dy=(dy,-dx)if rule[c]=='R'else(-dy,dx);x+=dx;y+=dy;h=DIRECTIONS.index((dx,dy));now=x,y,h
        assert (acc+pose_term(rule,now)-start)%m==(t+1)%m
        assert (acc_common+pose_term(rule,now,common_field=True)-start_common)%g==(t+1)%g
        for turning,face,value in generators:
            assert compact_charge(rule,turning,face,field,now)==value
        if t%64==0 or t+1==steps:
            assert clock(rule,field,now)==(start+t+1)%m
            assert clock(rule,field,now,common_field=True)==(start_common+t+1)%g
            if rule=='RL':assert classical_clock(set(field),now)==clock(rule,field,now)
            checkpoints+=1
    return (x,y,h),field,''.join(colors),start,(start+steps)%m,start_common,(start_common+steps)%g,checkpoints


def literal_checks():
    cases=make_cases();lines=[str(len(cases))]
    for rule,field,pose,steps in cases:
        lines.append(f'{rule} {pose[0]} {pose[1]} {pose[2]} {steps} {len(field)}')
        lines.extend(f'{x} {y} {c}'for (x,y),c in sorted(field.items()))
    with tempfile.TemporaryDirectory(prefix='phase-clock-')as td:
        folder=Path(td);inp=folder/'input.txt';exe=folder/'oracle';inp.write_text('\n'.join(lines)+'\n')
        subprocess.run(['g++','-std=c++17','-O2',str(HERE/'oracle.cpp'),'-o',str(exe)],check=True)
        native=subprocess.run([str(exe),str(inp)],check=True,capture_output=True,text=True,timeout=90)
    output=native.stdout.splitlines();assert len(output)==3*len(cases)
    updates=checkpoints=0;trace=hashlib.sha256()
    for i,(rule,field,pose,steps)in enumerate(cases):
        head,full,colors,c0,c1,u0,u1,ck=run_python(rule,field,pose,steps)
        header=list(map(int,output[3*i].split()))
        assert header==[i,*head,c0,c1,u0,u1,len(full)]
        assert output[3*i+1]==colors
        cells=list(map(int,output[3*i+2].split()));assert len(cells)==3*len(full)
        assert list(zip(cells[::3],cells[1::3],cells[2::3]))==[(x,y,c)for(x,y),c in sorted(full.items())]
        trace.update(native.stdout.splitlines()[3*i+1].encode());updates+=steps;checkpoints+=ck
    # Complete-field tests far beyond native-coordinate range.
    big=10**60;large_checks=0
    for rule in ('RL','RRRL','RRLL','RRL'):
        for h in range(4):
            B={(big,-big+3):1,(-big-1,big+7):len(rule)-1}
            pose=(big,-big+3,h);run_python(rule,B,pose,72);large_checks+=1
    return {'complete_inputs':len(cases),'literal_updates_per_implementation':updates,
            'exact_read_color_stream_comparisons':len(cases),'complete_endpoint_field_comparisons':len(cases),
            'python_complete_field_clock_recomputations':checkpoints,
            'huge_coordinate_python_inputs':large_checks,'color_stream_sha256':trace.hexdigest(),
            'native_pose_potential':'independently integrated on the raw 4x4 pose graph'}


def run():
    local=local_audit();print('Local equations complete.',flush=True)
    linear=linear_checks();print('Raw matrix and compact-basis audits complete.',flush=True)
    literal=literal_checks();print('Independent literal controls complete.',flush=True)
    return {'schema':'separated-phase-cocycles-v1','status':'passed',
            'base_commit':'80a96531f26dcc361ebfa1bef47b0e6953c29b77',
            'claims':'analytic all-state classification plus exact scoped controls; not HC or unrestricted joint-state invariants',
            'local':local,'linear':linear,'literal':literal,
            'source_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                             for name in ('core.py','linear_audit.py','oracle.cpp','check.py')}}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',type=Path)
    args=parser.parse_args();result=run()
    if args.write:
        args.write.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print('Explicit report written.')
    else:
        expected=json.loads((HERE/'report.json').read_text())
        assert result==expected,'frozen report changed; no file overwritten'
        print('PASS: scoped report reproduced.')
