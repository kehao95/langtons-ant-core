"""Independent literal-geometry regressions for PROOF.md; not proof premises."""
from __future__ import annotations
from collections import defaultdict
from itertools import combinations, product
from pathlib import Path
import hashlib
import random
import subprocess

import screen as fast
import family

MOVES=((0,1),(1,0),(0,-1),(-1,0))
STANDARD='RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR'


def canon(q,d):
    x,y=q; a,b=d
    r=x%a; k=(x-r)//a
    return r,y-k*b


def literal_edges(O,d):
    """Paint individual horizontal/vertical edges, not arithmetic runs."""
    a,b=d; H=defaultdict(list); V=defaultdict(list)
    for x,y in O:
        rem=y%abs(b); k=(y-rem)//b
        H[rem].append(x-k*a);V[x].append(y)
    edges=set()
    for Y,values in H.items():
        values.sort()
        if len(values)%2:return None
        for left,right in zip(values[::2],values[1::2]):
            for X in range(left,right):
                u,v=(X,Y),(X+1,Y)
                if (X+Y)%2==0:e=(canon(u,d),canon(v,d),1)
                else:e=(canon(v,d),canon(u,d),3)
                assert e not in edges
                edges.add(e)
    for X,values in V.items():
        values.sort()
        if len(values)%2:return None
        for bottom,top in zip(values[::2],values[1::2]):
            for Y in range(bottom,top):
                u,v=(X,Y),(X,Y+1)
                if (X+Y)%2:e=(canon(u,d),canon(v,d),0)
                else:e=(canon(v,d),canon(u,d),2)
                assert e not in edges
                edges.add(e)
    return edges


def literal_signature(O,edges,vertex_order=None):
    """Direct edge permutation and unsimplified local port corrections."""
    if vertex_order is None:
        vertices=sorted({q for e in edges for q in e[:2]} | set(O),key=lambda q:(q[1],q[0]))
        vertex_order={q:i for i,q in enumerate(vertices)}
    sources=sorted(edges,key=lambda e:(vertex_order[e[0]],int(e[2] in (0,1))))
    targets=sorted(edges,key=lambda e:(vertex_order[e[1]],int(e[2] in (0,1))))
    place={e:i for i,e in enumerate(targets)}
    pi=[place[e] for e in sources]
    E=sum(pi[i]>pi[j] for i in range(len(pi)) for j in range(i+1,len(pi)))%2
    outgoing=defaultdict(int);incoming=defaultdict(int)
    for s,t,h in edges:
        if h in (0,1):outgoing[s]^=1;incoming[t]^=1
    L=0
    for v in vertex_order:
        D=int(v in O);p=incoming[v]^outgoing[v]
        L^=(p*(D+1) if sum(v)%2==0 else D*(p+1))%2
    return E^L


def from_word(w,heading):
    """Vector-turn geometry, normalized independently of the native implementation."""
    vectors=((0,1),(1,0),(0,-1),(-1,0))
    dx,dy=vectors[heading];x=0;y=heading%2;start=(x,y)
    points=[];moves=[]
    for c in w:
        points.append((x,y))
        dx,dy=(dy,-dx) if c=='R' else (-dy,dx)
        moves.append(vectors.index((dx,dy)));x+=dx;y+=dy
    d=x-start[0],y-start[1]
    assert (dx,dy)==vectors[heading] and d[0] and d[1]
    end=x,y
    if d[0]<0:
        d=-d[0],-d[1];end=-x,-y
        points=[(-x,-y) for x,y in points];moves=[(h+2)%4 for h in moves]
    groups=defaultdict(list);D=defaultdict(int);counts=defaultdict(int)
    for i,p in enumerate(points):
        q=canon(p,d);level=(p[0]-q[0])//d[0]
        groups[q].append((i-len(w)*level,i));D[q]+=1 if w[i]=='R' else -1
        t=canon(points[i+1] if i+1<len(w) else end,d)
        counts[q,t,moves[i]]^=1
    assert set(D.values()) <= {0,1}
    O={q for q,v in D.items() if v};edges={e for e,v in counts.items() if v}
    assert edges==literal_edges(O,d)
    K=0;stable=True
    for entries in groups.values():
        for rank,(_,i) in enumerate(sorted(entries)):
            if w[i]=='L':K^=rank%2
            stable &= (w[i]==('L' if rank%2 else 'R'))
    F=literal_signature(O,edges)
    assert K^F==1
    assert fast.compressed_signature(O,d)==F
    return O,d,K,F,len(edges),stable


def run(binary: Path) -> dict:
    if not __debug__:raise RuntimeError('run without -O')
    rng=random.Random(20261016)
    for _ in range(10000):
        n=rng.randrange(20);m=rng.randrange(1,20);a=rng.randrange(-50,50);b=rng.randrange(-50,50)
        assert fast.floor_sum(n,m,a,b)==sum((a*i+b)//m for i in range(n))
    for _ in range(10000):
        A=fast.Run(rng.randrange(1,15),rng.randrange(1,15),rng.randrange(-40,40),0,0,0,0)
        B=fast.Run(rng.randrange(1,15),rng.randrange(1,15),rng.randrange(-40,40),0,0,0,0)
        bound=rng.randrange(-60,60)
        assert fast.pairs_leq(A,B,bound)==sum(A.sy+A.step*i-B.sy-B.step*j<=bound for i in range(A.n) for j in range(B.n))
    drifts=((1,-1),(2,-2),(3,1),(3,-3),(4,2),(4,-4),(2,4),(1,-3))
    tests=0;order_tests=0;quadratic_tests=0
    bank={}
    for d in drifts:
        samples=[]
        for j in range(500):
            O=set()
            for _ in range(rng.randrange(1,5)):
                x1,x2=rng.sample(range(-6,7),2);y1,y2=rng.sample(range(-6,7),2)
                for p in ((x1,y1),(x2,y1),(x1,y2),(x2,y2)):
                    q=canon(p,d)
                    if q in O:O.remove(q)
                    else:O.add(q)
            edges=literal_edges(O,d);runs=fast.runs_for(O,d)
            expanded=[e for r in runs for e in r.edges()]
            expected={(s,t,int(h in (0,1))) for s,t,h in edges}
            assert len(expanded)==len(set(expanded)) and set(expanded)==expected
            F=literal_signature(O,edges)
            assert F==fast.compressed_signature(O,d)
            assert fast.compressed_signature(O,d,True)['endpoint_port_parity']==0
            assert fast.compressed_signature({canon((x,y+1),d) for x,y in O},d)==F
            assert len(runs)<=len(O)*(d[0]+1)
            if j<64:
                vertices=list({q for e in edges for q in e[:2]}|O);rng.shuffle(vertices)
                assert literal_signature(O,edges,{q:i for i,q in enumerate(vertices)})==F
                order_tests+=1
            samples.append(O);tests+=1
        bank[d]=samples
        for j in range(64):
            A,B,C=samples[3*j:3*j+3]
            sets=(A,B,C,A^B,A^C,B^C,A^B^C)
            assert sum(fast.compressed_signature(O,d) for O in sets)%2==0
            quadratic_tests+=1
    closed=0;slots=list(product(range(2),range(8)))
    for mask in range(1<<16):
        O={p for k,p in enumerate(slots) if mask>>k&1}
        if any(sum(q[i]%2==r for q in O)%2 for i in range(2) for r in range(2)):continue
        q0=sum(sum(q)%2==0 and q[0]==0 for q in O)
        Q=[sum(q) for q in O if sum(q)%2==0]
        C=[sum(q) for q in O if sum(q)%2]
        J=sum(q<c for q in Q for c in C)
        g=len(O)
        assert fast.compressed_signature(O,(2,-2))==(J+g*(g-1)//2+q0)%2
        closed+=1
    native=subprocess.run([str(binary),'--exhaust','20'],capture_output=True,text=True,check=True,timeout=120)
    native_rows=[];balanced=0
    for line in native.stdout.splitlines():
        fields=line.split()
        if fields[0]=='COUNT':
            native_rows.append(dict(zip(('period','all_words','balanced_words','kinematic_words'),map(int,fields[1:]))));continue
        _,n,w,h,K,F,a,b,ne=fields
        O,d,kk,ff,ee,stable=from_word(w,int(h))
        assert (len(w),kk,ff,*d,ee)==tuple(map(int,(n,K,F,a,b,ne)))
        balanced+=1
    controls=[]
    heading=1
    for phase in range(104):
        shifted=STANDARD[phase:]+STANDARD[:phase]
        for power in range(1,5):
            for rotation in range(4):controls.append((shifted*power,(heading+rotation)%4))
        heading=(heading+(1 if STANDARD[phase]=='R' else -1))%4
    control_out=subprocess.run([str(binary)],input=''.join(f'{w} {h}\n' for w,h in controls),capture_output=True,text=True,check=True,timeout=120)
    assert len(control_out.stdout.splitlines())==len(controls)
    for (w,h),line in zip(controls,control_out.stdout.splitlines()):
        _,n,nw,nh,K,F,a,b,ne=line.split()
        assert nw==w and int(nh)==h
        O,d,kk,ff,ee,stable=from_word(w,h)
        assert stable and (len(w),kk,ff,*d,ee)==tuple(map(int,(n,K,F,a,b,ne)))
        result=fast.screen(sorted(O),d)
        assert result['status']=='NOT_EXCLUDED' and result['winding']==1
    fail=set(family.BASE)
    passing={(0,1),(0,5),(1,-4),(1,-2),(1,5),(1,6),(2,-4),(2,4)}
    f=fast.screen(sorted(fail),(3,1));p=fast.screen(sorted(passing),(3,1))
    assert f['status']=='EXCLUDED' and f['reason']=='quadratic port sign'
    assert p['status']=='NOT_EXCLUDED'
    assert f['charges']==p['charges'] and f['winding']==p['winding']==1
    representation_tests=0
    for O in (fail,passing):
        expected=fast.screen(sorted(O),(3,1))['status']
        for rot in range(4):
            d=(3,1);R=list(O)
            for _ in range(rot):R=[(y,-x) for x,y in R];d=d[1],-d[0]
            assert fast.screen(R,d,(-1)**rot)['status']==expected
            representation_tests+=1
        shifted=[]
        for x,y in O:
            k=rng.randrange(-10**80,10**80);shifted.append((x+3*k,y+k))
        assert fast.screen(shifted,(3,1))['status']==expected
        representation_tests+=1
        assert fast.screen(sorted(O),(3,1),-1)['status']==expected
        representation_tests+=1
    bad_inputs=0
    for args in [([], (2,0)), ([(0,0),(3,1)],(3,1)), ([(True,1)],(3,1)), ([(0,0)],(3,1),0)]:
        try:fast.screen(*args)
        except ValueError:bad_inputs+=1
        else:raise AssertionError('invalid input accepted')
    assert fast.screen(family.BASE,(10**100,2))['status']=='EXCLUDED'
    symbolic=family.symbolic()
    n=10**100;M=12*n+1
    huge=fast.screen([(M*x,M*y) for x,y in family.BASE],(3,1))
    assert huge['status']=='EXCLUDED' and huge['runs']==32 and huge['odd_edges']==192*n+16
    return {'status':'complete','floor_sum_cases':10000,'lattice_pair_count_cases':10000,
            'literal_edge_and_signature_cases':tests,'drifts':[list(d) for d in drifts],
            'checker_and_translation_invariance_checks':tests,'vertex_order_checks':order_tests,'quadratic_polarization_checks':quadratic_tests,
            'all_two_lane_closed_masks':closed,'native_period_rows':native_rows,
            'native_all_words':sum(r['all_words'] for r in native_rows),
            'native_kinematic_factorizations':sum(r['kinematic_words'] for r in native_rows),
            'native_balanced_words_cross_checked':balanced,
            'native_exhaust_stdout_sha256':hashlib.sha256(native.stdout.encode()).hexdigest(),
            'standard_phase_rotation_power_controls':len(controls),
            'representative_and_rotation_checks':representation_tests,'invalid_input_controls':bad_inputs,
            'new_drift_negative_example':f,'arithmetic_matched_not_excluded_example':p,
            'symbolic_unbounded_family':symbolic,'huge_parameter_decimal_digits':len(str(n)),
            'huge_case':huge,'mathematical_scope':'necessary only; NOT_EXCLUDED is not realizable',
            'formal_kernel_checked':False,'independent_human_review':False}

if __name__=='__main__':
    import argparse,json
    ap=argparse.ArgumentParser();ap.add_argument('binary',type=Path);ap.add_argument('--output',type=Path)
    args=ap.parse_args();report=run(args.binary)
    text=json.dumps(report,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(text)
