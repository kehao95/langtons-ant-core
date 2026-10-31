"""Replay exact arbitrary-time complete-state queries and a separate C++ walk.

Finite controls test implementations. All-input/all-time coverage for this
specified family follows from the written acceleration proof and inherited
basin certificate, not from a maximum test parameter. Default never rewrites.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import random
import subprocess
import tempfile
import core as fast
HERE=Path(__file__).resolve().parent


def check(condition,message):
    if not condition:raise AssertionError(message)


def explicit_source(l,r):
    left=[5,6,10,12,17]+[18,29]*l
    columns=[31-b for b in left[::-1]]+[6,10,12,17]+[18,29]*r
    return {(x,y)for x,c in enumerate(columns)for y in range(5)if c&(1<<y)},(2*l+5,3,1)


def controls():
    w=fast.certificate();cases={(0,0),(1,1)}
    for l,row in enumerate(w['left_exhausted_small_delays']):
        cases.update((l,l+d)for d in range(1,len(row)+1))
    for m in (0,1,2,8,9,31):
        cases.update((m+d,m)for d in (0,1,2,17))
        cases.update((m,m+d)for d in (1,2,3,4,5,6,17))
    rng=random.Random(20261030)
    cases.update((rng.randrange(40),rng.randrange(40))for _ in range(12))
    output=[]
    for l,r in sorted(cases):
        E,delay,tau=fast.prediction(l,r);m=min(l,r)
        ts={0,1,E-1,E,E+1,tau-1,tau,tau+1,tau+103,tau+104,tau+337}
        for j in {0,m//2,m}:
            if not 0<=j<=m:continue
            b=8*j*j+56*j
            for z in (b,b+4*j,b+8*j+30,b+16*j+64):ts.update((z-1,z,z+1))
        lc,rc=fast.clip(l,r);name=('east'if rc<=lc else 'west')+'-'+str(abs(lc-rc))
        if m in (2,9) and name in w['all_parameter_schemata'] and not(lc==rc and lc<2)and not(lc<rc and lc<9):
            start=E
            for stage in w['all_parameter_schemata'][name]['stages']:
                size=len(stage['word']);n=stage['a']*m+stage['b']
                for z in (start,start+size,start+max(0,n-1)*size,start+n*size):ts.update((z-1,z,z+1))
                start+=size*n
        ts=sorted(t for t in ts if 0<=t<=tau+337)
        output.append((l,r,ts))
    return output


def literal_controls():
    cases=controls();lines=[str(len(cases))]
    for l,r,ts in cases:lines.append(f'{l} {r} {len(ts)}\n'+' '.join(map(str,ts)))
    with tempfile.TemporaryDirectory(prefix='basin-access-')as td:
        td=Path(td);inp=td/'inputs';exe=td/'oracle';out=td/'states'
        inp.write_text('\n'.join(lines)+'\n')
        subprocess.run(['g++','-std=c++17','-O2',str(HERE/'oracle.cpp'),'-o',str(exe)],check=True)
        with out.open('w')as f:subprocess.run([str(exe),str(inp)],stdout=f,check=True,timeout=180)
        result=Counter();maximum=0;fingerprint=hashlib.sha256()
        with out.open()as f:
            for i,(l,r,ts)in enumerate(cases):
                black,pose=explicit_source(l,r);x,y,h=pose;dx,dy=fast.DIR[h];t=0
                for target in ts:
                    while t<target:
                        p=x,y;b=p in black
                        if b:black.remove(p);dx,dy=-dy,dx
                        else:black.add(p);dx,dy=dy,-dx
                        x+=dx;y+=dy;t+=1
                    data=list(map(int,next(f).split()));pose=x,y,fast.DIR.index((dx,dy))
                    check(data[:6]==[i,t,*pose,len(black)],'native pose or mass differs')
                    native=list(zip(data[6::2],data[7::2]));check(native==sorted(black),'complete literal fields differ')
                    answer=fast.state_at(l,r,t);expanded=answer.field.materialize()
                    check(answer.pose==pose and expanded==black,'fast whole state differs')
                    check(answer.field.cardinality()==len(black),'exact segment cardinality')
                    check(answer.next_turn()==('L'if(x,y)in black else'R'),'random-access read bit')
                    maximum=max(maximum,len(answer.field.terms));result['full_snapshots']+=1
                    fingerprint.update((str((l,r,t,pose,sorted(black)))+'\n').encode())
                result['literal_updates_per_implementation']+=t
            check(not f.read().strip(),'unexpected extra native records')
    result.update(complete_inputs=len(cases),maximum_segments=maximum)
    return dict(result,full_states_sha256=fingerprint.hexdigest())


def segment_controls():
    rng=random.Random(10430);count=0
    for trial in range(1000):
        field=fast.Field()
        for _ in range(rng.randrange(1,20)):
            x,y=rng.randrange(-20,21),rng.randrange(-20,21)
            dy=rng.choice((-2,0,2));n=rng.randrange(10)
            field.add(x,y,2,dy,n)
        explicit=field.materialize()
        check(field.cardinality()==len(explicit),'arrangement cardinality failed')
        fresh=fast.Field()
        for p in explicit:fresh.toggle(p)
        check(field.equal(fresh),'exact compressed equality failed')
        for _ in range(4):
            p=rng.randrange(-30,31),rng.randrange(-30,31)
            check(field.contains(p)==(p in explicit),'point membership failed')
        count+=1
    big=10**100;field=fast.Field()
    field.add(-2*big,0,2,0,2*big+1)
    field.add(-2*big,-2*big,2,2,2*big+1)
    field.add(-2*big,2*big,2,-2,2*big+1)
    check(field.cardinality()==6*big+1,'three-way crossing correction')
    field.toggle((0,0));check(field.cardinality()==6*big,'four-way cancellation')
    return {'finite_arrangements':count,'huge_three_and_four_way_crossings':2}


def huge_controls():
    huge=10**60;params=[(huge,huge),(huge+1,huge),(huge+2,huge),(huge*huge,huge),
                       *[(huge,huge+d)for d in range(1,7)],(huge,huge*huge),
                       (0,huge),(huge,0),(5,huge),(huge,1)]
    comparisons=0;example=None;maximum=0
    for l,r in params:
        E,delay,tau=fast.prediction(l,r);m=min(l,r);j=m//2
        times={0,1,8*j*j+56*j,E-1,E,E+1,tau-1,tau,tau+104*huge+37}
        for t in sorted(times):
            a=fast.state_at(l,r,t);b=fast.state_at(l,r,t+1)
            color=a.field.contains(a.pose[:2]);h=(a.pose[2]+(-1 if color else 1))%4
            dx,dy=fast.DIR[h];expected=(a.pose[0]+dx,a.pose[1]+dy,h)
            one=a.field.copy();one.toggle(a.pose[:2])
            check(b.pose==expected and one.equal(b.field),'huge one-step complete equality')
            check(b.field.cardinality()-a.field.cardinality()==(-1 if color else 1),'huge one-step mass')
            maximum=max(maximum,len(a.field.terms),len(b.field.terms));comparisons+=1
        at=fast.state_at(l,r,tau);later=fast.state_at(l,r,tau+104*huge)
        # The standard certificate fixes growth 12; no huge literal run is claimed.
        check(later.field.cardinality()-at.field.cardinality()==12*huge,'standard-cycle mass')
        if l==r==huge:
            sample=fast.state_at(l,r,tau+104*huge+37)
            example={'left':str(l),'right':str(r),'time':str(tau+104*huge+37),
                     'pose':[str(sample.pose[0]),str(sample.pose[1]),sample.pose[2]],
                     'black_mass':str(sample.field.cardinality()),'segments':len(sample.field.terms),
                     'next_turn':sample.next_turn(),'stats':{k:str(v)if abs(v)>10**12 else v for k,v in sample.stats.items()}}
    payload_checks=0
    for l,r,pts in ((huge,1,[(-huge,1),(0,2)]),(1,huge,[(3*huge,1),(10**100,4)])):
        for t in (0,1,fast.prediction(l,r)[2],10**120):
            raw=fast.state_at(l,r,t);with_payload=fast.state_at(l,r,t,protected_toggles=pts)
            expected=raw.field.copy()
            for p in pts:expected.toggle(p)
            check(with_payload.pose==raw.pose and with_payload.field.equal(expected),'protected full payload')
            payload_checks+=1
    invalid=0
    for fun in (lambda:fast.state_at(-1,0,0),lambda:fast.state_at(0,0,-1),
                lambda:fast.state_at(True,0,0),lambda:fast.state_at(0,1,0.5),
                lambda:fast.state_at(0,0,0,protected_toggles=[(0,0)]),
                lambda:fast.state_at(100,1,0,protected_toggles=[(0,5)]),
                lambda:fast.state_at(100,1,0,protected_toggles=[(0,2),(0,2)]),
                lambda:fast.state_at(huge,huge,10**120).field.materialize(1000)):
        try:fun()
        except ValueError:invalid+=1
        else:raise AssertionError('invalid or oversized request accepted')
    return {'complete_one_step_equalities':comparisons,'parameter_cases':len(params),
            'whole_period_mass_equalities':len(params),'protected_payload_controls':payload_checks,
            'negative_controls':invalid,'maximum_segments':maximum,'example':example,
            'huge_ordinary_updates_simulated':0}


def run():
    segments=segment_controls();print('exact segment algebra passed',flush=True)
    literal=literal_controls();print('all finite literal snapshots passed',flush=True)
    huge=huge_controls();print('huge complete-field arithmetic controls passed',flush=True)
    return {'schema':'counter-basin-random-access-v1','status':'passed',
            'scope':'all times on the inherited explicit two-counter family, not arbitrary seeds or HC',
            'universal_claim_basis':'written acceleration induction and inherited all-parameter basin certificate',
            'segment_algebra':segments,'literal':literal,'huge':huge,
            'source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest()for n in ('core.py','check.py','oracle.cpp')},
            'baseline_sha256':fast.PINS}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write',type=Path);a=parser.parse_args()
    result=run()
    if a.write:a.write.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print('WROTE candidate report')
    else:
        check(result==json.loads((HERE/'report.json').read_text()),'frozen report mismatch; not overwritten')
        print('PASS: exact random-access complete-state controls')
