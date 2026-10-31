"""Scoped exact verification of all finite leaves of the capacity proof.

Default compares a rebuilt report with frozen report.json and never overwrites
it. All-n,m claims are proved by the written lane-separation induction, not the
finite controls. Native checker separately audits both infinite period seeds.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import random
import subprocess
import tempfile
from core import (CODE, DIRECTIONS, P, Q, W, STANDARD, checkpoint, geometry, lane,
                  literal, lower_profile, matrix, origin, passive_prefix,
                  readout_profile, reachable_count, shift, source, tile, trigger,
                  reachable_sites, passive_ray_bases, passive_count, full_control_bits, controlled)

HERE=Path(__file__).resolve().parent

def digest_bytes(b):return hashlib.sha256(b).hexdigest()
def canon(o):return json.dumps(o,sort_keys=True,separators=(',',':')).encode()

def periodic(word,h,seed):
    """Representatives chosen from first encountered phase (not native gauge)."""
    reads,d,eh=geometry(word,h)
    assert d[0]==2 and abs(d[1])==2 and eh==h
    groups=[]
    for i,p in enumerate(reads):
        for c,events in groups:
            diff=p[0]-c[0]
            if diff%2==0:
                k=diff//2
                if p==(c[0]+k*d[0],c[1]+k*d[1]):
                    events.append((i,k,word[i]));break
        else:groups.append((p,[(i,0,word[i])]))
    initial=set();records=[];checks=0
    for c,events in groups:
        cuts=sorted({k for i,k,a in events});slabs=[]
        for j,a in enumerate(cuts):
            eligible=sorted((i-104*k,b)for i,k,b in events if k<=a)
            letters=''.join(b for t,b in eligible)
            assert all(x!=y for x,y in zip(letters,letters[1:]));checks+=len(letters)-1
            upper=cuts[j+1] if j+1<len(cuts)else None
            if upper is None:assert letters[0]=='R'
            elif letters[0]=='L':
                initial.update((c[0]+k*d[0],c[1]+k*d[1])for k in range(a,upper))
            slabs.append([a,upper,letters])
        records.append([list(c),slabs])
    assert initial==set(seed)
    return {'classes':len(groups),'alternation_checks':checks,'drift':list(d),
            'chronology_sha256':digest_bytes(canon(records))}

def signed_lines(field):
    a,b=defaultdict(int),defaultdict(int)
    for x,y in field:
        a[x]+=(-1)**((x+y)%2);b[y]+=(-1)**((x+y)%2)
    return sorted((x,v)for x,v in a.items()if v),sorted((y,v)for y,v in b.items()if v)

def finite_leaves():
    down=periodic(W,1,P);up=periodic(W,0,Q)
    assert W==STANDARD[-1:]+STANDARD[:-1] and len(W)==104 and W[72]=='R'
    assert W[-2:]=='LL' and all(W[i:]+W[:i]!=W for i in range(1,104))
    assert literal(set(),(0,0,0),10081)[2][9977:]==STANDARD
    rd,d,h=geometry(W,1);ru,du,hu=geometry(W,0)
    assert min(x+y for x,y in rd)==-4 and max(x+y for x,y in rd)==6
    assert max(x for x,y in rd)==8 and max(x for x,y in P)==6
    bg,p,w,r72=literal(P,(0,0,1),72)
    assert p==(8,-2,1) and p[:2] not in bg
    assert (7,-1)not in P and (7,-1)not in r72
    assert min(x for x,y in ru)==min(y for x,y in ru)==0
    assert min(y-x for x,y in ru)==-4 and max(y-x for x,y in Q)==5
    assert max(x for x,y in Q)==3 and min(x+y for x,y in ru)==0
    records=[]
    for bit in (0,1):
        a=tile(bit);b,p,w,r=literal(a,(0,0,0),4)
        assert b==tile(bit,True) and p==(0,2,0) and w==CODE[bit]
        assert signed_lines(a)==([],[])
        assert all(-1<=x<=1 and 0<=y<2 for x,y in r)
        records.append({'bit':bit,'source':sorted(a),'target':sorted(b),'reads':r,'turns':w})
    # Strict all-parameter separation reduces to these constant inequalities.
    # Earlier-lane support is left of any outgoing read; later support is below
    # the NE strip; all passive writes have x+y<=6.
    assert 3-6 < -1                 # neighboring source vs selected data reads
    assert 3-6 < 0                  # earlier cap vs outgoing x>=0
    assert 5-12 < -4                # later cap vs outgoing y-x>=-4
    assert -1-12 < -4               # later data vs outgoing y-x>=-4
    assert 7 > 6                    # every source data/cap off passive trace
    assert 7+2 > 6                  # outgoing reads even farther above old field
    return {'passive_period':down,'outgoing_period':up,'kernels':records,
            'phase':72,'phase_pose':[8,-2,1],'guard_inequalities':6,
            'background_strip':[-4,6],'outgoing_normal_min':-4}

def small_cases():
    out=[]
    for n,mmax in ((1,7),(2,4),(3,3),(4,2)):
        for m in range(1,mmax+1):
            for u in itertools.product((0,1),repeat=n*m):
                out.append(tuple(tuple(u[j*m:(j+1)*m])for j in range(n)))
    rng=random.Random(20261030)
    for n,m in ((5,7),(8,16),(16,32),(32,16),(1,1000),(128,1)):
        out += [tuple(tuple(b for _ in range(m))for _ in range(n))for b in (0,1)]
        out += [tuple(tuple((j+r)%2 for r in range(m))for j in range(n)),
                tuple(tuple(rng.randrange(2)for _ in range(m))for _ in range(n))]
    return out

def run_cases():
    cases=small_cases();inputs=[];expected=[];updates=points=profiles=0
    by_dimensions=defaultdict(list);checksums=hashlib.sha256();guarded=0;first=0
    for ix,rows in enumerate(cases):
        n,m=len(rows),len(rows[0]);initial=source(rows)
        assert len(initial)==13+n*(13+4*m)
        assert signed_lines(initial)==signed_lines(source([[0]*m for _ in range(n)]))
        assert (min(x for x,y in initial),max(x for x,y in initial))==(0,6*n+5)
        assert min(y for x,y in initial)==min(-3,5-6*n)
        assert max(y for x,y in initial)==2*m+5
        js=list(range(n))if n<=4 else sorted({0,n//2,n-1})
        # For finite profile equality use every experiment for complete small families.
        traces=[]
        for j in js:
            t=trigger(j);boundary=t+1+4*m
            total=boundary+104
            field,pose,word,reads=literal(initial,(0,0,1),total,t)
            predicted=passive_prefix(t)+'L'+''.join(CODE[b]for b in rows[j])+W
            assert word==predicted
            before,head=checkpoint(rows,j,m)
            end,h,tail,_=literal(before,head,104)
            assert (field,pose)==(end,h)
            assert pose==(head[0]+2,head[1]+2,0)
            # Inspect all actual intermediate complete fields on a selected scope.
            # The full endpoint is compared for every experiment.
            if ix%41==0 or (n==1 and m<=4):
                partial,ph,_,_=literal(initial,(0,0,1),t+1,t)
                assert (partial,ph)==checkpoint(rows,j,0);points+=1
                for r in range(1,m+1):
                    partial,ph,_,_=literal(partial,ph,4)
                    assert (partial,ph)==checkpoint(rows,j,r);points+=1
            prefix=predicted[:boundary]
            mismatch=[i for i,c in enumerate(prefix)if c!=W[(i-boundary)%104]]
            assert max(mismatch,default=-1)+1==boundary-rows[j][-1];first+=1
            inputs.append((initial,(0,0,1),total,t));expected.append((field,pose,word))
            updates+=total;checksums.update(canon([n,m,j,word,sorted(field),pose]))
            traces.append(word)
            if ix%211==0 and j==js[0]:
                remote={(-10**60,10**60)}
                ee,hh,ww,_=literal(initial|remote,(0,0,1),total,t)
                assert (ee,hh,ww)==(field|remote,pose,word);guarded+=1
        if n*m<=9:by_dimensions[n,m].append(traces)
        # Sample passive controls; infinite passive agreement is the strip proof.
        if ix%41==0:
            total=trigger(n-1)+104
            a,p,w,_=literal(initial,(0,0,1),total)
            assert w==passive_prefix(total)
            inputs.append((initial,(0,0,1),total,None));expected.append((a,p,w));updates+=total
    for (n,m),family in by_dimensions.items():
        assert len(family)==2**(n*m)
        horizons=sorted({0,1,71,72,73,74,trigger(n-1)+4*m+10}|
                        {trigger(j)+4*r+z for j in range(n)for r in range(m+1)for z in (1,2,3)})
        for T in horizons:
            # Continue the already certified suffix when an earlier lane ends first.
            seen={tuple((row+passive_prefix(max(0,T-len(row))))[:T]for row in responses)for responses in family}
            q=sum(readout_profile(n,m,T))
            assert len(seen)==2**q,(n,m,T,len(seen),q);profiles+=1
    with tempfile.TemporaryDirectory(prefix='capacity-native-')as td:
        td=Path(td);path=td/'input';exe=td/'oracle'
        lines=[W]
        for h,seed in ((1,P),(0,Q)):
            lines.append(f'{h} {len(seed)}');lines.extend(f'{x} {y}'for x,y in sorted(seed))
        lines.append(str(len(inputs)))
        for B,p,steps,flip in inputs:
            lines.append(f'{steps} {flip if flip is not None else -1} {p[0]} {p[1]} {p[2]} {len(B)}')
            lines.extend(f'{x} {y}'for x,y in sorted(B))
        path.write_text('\n'.join(lines)+'\n')
        subprocess.run(['g++','-O2','-std=c++17','-Wall','-Wextra',str(HERE/'independent.cpp'),'-o',str(exe)],check=True)
        result=subprocess.run([str(exe),str(path)],capture_output=True,text=True,check=True,timeout=120)
    out=result.stdout.splitlines();assert out[:2]==['PERIOD 130','PERIOD 130']
    out=out[2:];assert len(out)==3*len(expected)
    for i,(B,p,w)in enumerate(expected):
        assert list(map(int,out[3*i].split()))==[i,*p,len(B)]
        assert out[3*i+1]==(w or '-')
        c=list(map(int,out[3*i+2].split()))
        assert list(zip(c[::2],c[1::2]))==sorted(B)
    return {'matrices':len(cases),'complete_native_runs':len(inputs),
            'updates_per_implementation':updates,'complete_intermediate_checks':points,
            'exact_profile_checks':profiles,'first_entry_checks':first,
            'huge_unread_cell_controls':guarded,'trajectory_sha256':checksums.hexdigest()}

def combinatorial_controls():
    sites=set();front={((0,0),1)};counts=[]
    for T in range(1,33):
        sites.update(p for p,h in front)
        assert len(sites)==reachable_count(T)
        counts.append(len(sites))
        nf=set()
        for (x,y),h in front:
            for delta in(-1,1):
                hh=(h+delta)%4;dx,dy=DIRECTIONS[hh];nf.add(((x+dx,y+dy),hh))
        front=nf
    lowers=[]
    for T in (0,1,70,73,74,100,1000,10000,10**60):
        d=lower_profile(T);n,m=d['rows'],d['columns']
        if n and n<100000:assert d['bits']==sum(readout_profile(n,m,T))
        assert 0<=d['bits']<=T*(T-1)//2
        lowers.append({'T':T,**d})
    bases=passive_ray_bases()
    assert len(bases)==22 and all(x>=0 and y<=0 for x,y in bases)
    # On each of the four residue classes, every ray upper index is >=-1
    # already at T=13..16; increasing T by 4 raises it by one forever.
    for T in range(13,17):
        for x,y in bases:
            r={(0,0):0,(0,1):1,(1,1):2,(1,0):3}[x%2,y%2]
            t=T-1-((T-1-r)%4);a,b=t//2,(t+1)//2
            assert min((a-x)//2,(b+y)//2)>=-1
    offsets=(33,27,22,16)
    for T in list(range(13,201)) + [10**60+r for r in range(4)]:
        assert full_control_bits(T)==T*T-T+1-22*(T//4)+offsets[T%4]
    quotient=[]
    for T in range(1,5):
        K=reachable_sites(T)
        footprint={(x+2*k,y-2*k)for x,y in bases for k in range(T+9)}
        free=sorted(K-footprint)
        assert len(free)==full_control_bits(T)
        actions=list(itertools.product((0,1),repeat=T));responses=set()
        for colors in itertools.product((0,1),repeat=len(free)):
            initial=set(P)|{p for p,b in zip(free,colors)if b}
            responses.add(tuple(controlled(initial,u)for u in actions))
        assert len(responses)==2**len(free)
        quotient.append({'T':T,'free_cells':len(free),'classes':len(responses),'actions':len(actions)})
    rejects=0
    for func in(lambda:matrix([]),lambda:matrix([[0],[1,0]]),lambda:matrix([[2]]),
                 lambda:trigger(-1),lambda:literal(P,(0,0,1),2,cap=1)):
        try:func()
        except (ValueError,TimeoutError):rejects+=1
        else:raise AssertionError('invalid input accepted')
    bad=set(P);bad.symmetric_difference_update(((0,0),))
    try:periodic(W,1,bad)
    except AssertionError:rejects+=1
    else:raise AssertionError('damaged period seed accepted')
    # A delayed off-trace disturbance in an outgoing read ray cannot be deleted.
    big=10**60;p=(2*big,2*big)
    assert p[0]%2==0 and p[1]==p[0] # the phase-zero read of Q at epoch big.
    assert p not in Q
    try:periodic(W,0,set(Q)|{p})
    except AssertionError:rejects+=1
    else:raise AssertionError('remote future blocker accepted')
    return {'reachable_area_counts':counts,'lower_bounds':lowers,'negative_controls':rejects,
            'future_ray_blocker_rejected':True,'passive_ray_bases':bases,
            'exact_full_control_quotients':quotient, 'full_control_quasipolynomial_from':13}

def run():
    leaves=finite_leaves();controls=combinatorial_controls();cases=run_cases()
    return {'schema':'quadratic-interventional-capacity-v1','status':'passed',
            'scope':'one passive P104 class; one current-site toggle at a chosen time; no HC theorem',
            'all_parameter_bridge':'written constant-spacing lane-separation and exact read/write induction',
            'finite_leaves':leaves,'controls':controls,'literal':cases,
            'sources_sha256':{p:digest_bytes((HERE/p).read_bytes())for p in ('core.py','check.py','independent.cpp')}}

if __name__=='__main__':
    if not __debug__:raise RuntimeError('verification requires Python assertions; do not use -O')
    ap=argparse.ArgumentParser();ap.add_argument('--write',type=Path);args=ap.parse_args()
    report=run();raw=json.dumps(report,sort_keys=True,indent=2)+'\n'
    if args.write:args.write.write_text(raw);print('WROTE',args.write)
    else:
        assert (HERE/'report.json').read_text()==raw,'frozen report mismatch'
        print('PASS: exact finite leaves, full-field controls and native audit agree')
    print(json.dumps(report['literal'],sort_keys=True))
