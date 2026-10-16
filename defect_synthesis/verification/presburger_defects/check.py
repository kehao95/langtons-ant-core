#!/usr/bin/env python3
"""Theorem-local exact relation checks; no whole-repository or full cover replay."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from random import Random
from compiler import *
from cover import descriptions, descriptor_count, cover_bounds, all_coordinate_existence, LOOPS
from isl_exact import sample_parameters

HERE=Path(__file__).resolve().parent


def literal_plan(word,pose=(0,0),heading=0,source=None):
    # Separate vector implementation: does not call compiler.geometry or DIRS.
    vectors=((0,1),(1,0),(0,-1),(-1,0))
    vx,vy=vectors[heading]; x,y=pose
    first={};previous={};positions=[];valid=True
    for ch in word:
        p=(x,y);positions.append(p)
        if p in previous and previous[p]==ch: valid=False
        first.setdefault(p,ch);previous[p]=ch
        vx,vy=(vy,-vx) if ch=='R' else (-vy,vx)
        x+=vx;y+=vy
    minimum={p for p,ch in first.items() if ch=='L'}
    initial=set(minimum if source is None else source)
    valid &= all((p in initial)==(ch=='L') for p,ch in first.items())
    black=set(initial)
    if valid:
        for p in positions: black.symmetric_difference_update((p,))
    return dict(valid=bool(valid),minimum=minimum,visited=set(positions),black=black,
                pose=(x,y),heading=vectors.index((vx,vy)),positions=positions)


def point_domain(s,ctx,values):
    return s.param_set(ctx,' and '.join(f'{p}={values[p]}' for p in s.parameters) or '1=1')


def finite_set(s,ctx,points):
    return s.black_set(ctx,' or '.join(f'(x={x} and y={y})' for x,y in sorted(points)) or 'false')


def check_instance(comp,ctx,values,counters,source=None):
    s=comp.schema;word=s.expand(values)
    pose=tuple(e.evaluate(values) for e in s.pose)
    expected=literal_plan(word,pose,s.heading,source)
    dom=point_domain(s,ctx,values)
    actual=not comp.feasible.intersect(dom).is_empty()
    assert actual==expected['valid'],(word,values,str(comp.feasible))
    assert comp.first_black.intersect_params(dom).is_equal(finite_set(s,ctx,expected['minimum']).intersect_params(dom))
    assert comp.visited.intersect_params(dom).is_equal(finite_set(s,ctx,expected['visited']).intersect_params(dom))
    if actual:
        assert comp.endpoint.intersect_params(dom).is_equal(finite_set(s,ctx,expected['black']).intersect_params(dom))
        assert tuple(e.evaluate(values) for e in s.end_pose)==expected['pose']
        assert s.end_heading==expected['heading']
        counters['full_endpoints']+=1
    count=sum(word[i:i+10] not in L10 for i in range(max(0,len(word)-9)))
    last=len(word)>=10 and word[-10:] not in L10
    chosen=[]
    for f in factor_cases(s):
        if not s.param_set(ctx,f.condition).intersect(dom).is_empty(): chosen.append(f)
    assert len(chosen)==1,(values,len(chosen))
    assert chosen[0].count.evaluate(values)==count
    assert chosen[0].last_bad==last
    counters['parameter_instances']+=1
    counters['literal_plan_updates']+=len(word)
    return expected


def run():
    ctx=Context();relations={};counters=dict(parameter_instances=0,full_endpoints=0,literal_plan_updates=0)
    assert len(W)==104 and len(A)==28 and len(B)==102 and len(T)==24 and len(LOOPS)==156
    n,m,k=var('n'),var('m'),var('k')
    # A closed geometric loop is not a physically repeatable cycle.
    s=Schema(['n'],[Power('RRRR',n)])
    r=compile_schema(s,ctx)
    assert r.feasible.is_equal(s.param_set(ctx,'n<=1'))
    relations['closed_square']=str(r.feasible)
    for nn in range(7):check_instance(r,ctx,{'n':nn},counters)

    # Reproduce the inherited all-length three-fold conflict automatically.
    s=Schema(['n','m'],[B,Power(A,n),B,Power(A,m),B])
    r=compile_schema(s,ctx)
    assert r.feasible.is_empty()
    relations['three_folds']=str(r.feasible)
    for nn in range(5):
        for mm in range(5):check_instance(r,ctx,{'n':nn,'m':mm},counters)

    # Two independent fold depths: a quantified, non-box parameter calculation.
    C='RLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLL'
    D='LLRRRRLRRLRRRRLLLLRLRRRRLRL'
    s=Schema(['n','m'],[C,Power(A,n+6),B,Power(A,m+2),D],domain='n>=0 and m>=0')
    r=compile_schema(s,ctx)
    expected=s.param_set(ctx,'m<=n')
    assert r.feasible.is_equal(expected)
    assert r.feasible.is_equal(r.feasible.intersect(defect_domain(s,ctx,0,exact=True)))
    relations['two_depth_fold']=str(r.feasible)
    for nn in range(5):
        for mm in range(5):check_instance(r,ctx,{'n':nn,'m':mm},counters)
    # The known diagonal specialization ends with its FIRST contained defect.
    s2=Schema(['n'],[C,Power(A,n+6),B,Power(A,n+2),D,'R'],domain='n>=0')
    source=compile_schema(Schema(['n'],[C,Power(A,n+6),B,Power(A,n+2),D],domain='n>=0'),ctx).first_black
    r2=compile_schema(s2,ctx,source)
    assert r2.feasible.is_equal(s2.param_set(ctx))
    assert r2.feasible.is_equal(defect_domain(s2,ctx,1,exact=True,ends_bad=True))
    assert s2.length==56*n+398
    assert s2.end_pose==(Affine(-1),Affine(1)) and s2.end_heading==0
    relations['silent_first_event_post']=str(s2.endpoint_map(ctx,r2.feasible))

    # Full old rail, cap and ALL generated residues, not just the head neighbourhood.
    E=[(-2,-1),(-1,0)]
    cap=[(-1,-4),(-1,-3),(0,-5),(0,-3),(0,-2),(1,-6),(1,-5),(1,-4),(1,-3),(2,-3),(2,-2)]
    residue=[(-2,0),(-1,-1),(-1,0),(0,-1),(1,-1),(1,0)]
    rail_formula=' or '.join([f'(x={x} and y={y})' for x,y in E]+
        [f'(x={x} and y={y}-2*n)' for x,y in cap]+
        ['(exists (j: 1<=j<=n and ((x=-2 and y=-2*j) or (x=0 and y=-2*j-1))))'])
    s=Schema(['n','k'],[Power(T,k)],domain='n>=0')
    source=s.black_set(ctx,rail_formula)
    r=compile_schema(s,ctx,source)
    target_formula=' or '.join([f'(x={x} and y={y}-2*k)' for x,y in E]+
        [f'(x={x} and y={y}-2*n)' for x,y in cap]+
        ['(exists (j: k+1<=j<=n and ((x=-2 and y=-2*j) or (x=0 and y=-2*j-1))))']+
        [f'(exists (j: 0<=j<k and x={x} and y={y}-2*j))' for x,y in residue])
    target=s.black_set(ctx,target_formula)
    assert r.feasible.is_equal(s.param_set(ctx,'k<=n'))
    assert r.endpoint_identity_domain(target).is_equal(r.feasible)
    relations['rail_exact_exhaustion']=str(r.feasible)
    relations['rail_full_endpoint_identity']=str(r.endpoint_identity_domain(target))
    for nn in range(6):
        bb=set(E)|{(-2,-2*j) for j in range(1,nn+1)}|{(0,-2*j-1) for j in range(1,nn+1)}|{(x,y-2*nn) for x,y in cap}
        for kk in range(6):check_instance(r,ctx,{'n':nn,'k':kk},counters,bb)

    # A standard source and a marker at completely unrestricted integer coordinates.
    seed=literal_plan(W)['minimum'];assert len(seed)==17
    formula,_=exact_seed_formula(sorted(seed))
    s=Schema(['k','px','py'],[Power(W,k)])
    r=compile_schema(s,ctx,s.black_set(ctx,'('+formula+') or (x=px and y=py)'))
    outside=' and '.join(f'(px!={x} or py!={y})' for x,y in sorted(seed))
    allcoords=ctx.set('[px,py] -> { : '+outside+' }')
    bad=s.param_set(ctx,outside).subtract(r.feasible).project_params(0,1)
    safe=allcoords.subtract(bad).coalesce()
    # Independently derive the 104 ray union by vector geometry.
    trace=literal_plan(W)
    dx,dy=trace['pose']
    rays=ctx.set('[px,py] -> { : '+' or '.join(
        f'(exists (j: j>=0 and px={x}+{dx}*j and py={y}+{dy}*j))'
        for x,y in trace['positions'])+' }')
    assert safe.is_equal(allcoords.subtract(rays))
    relations['one_marker_permanent_standard_domain']=str(safe)
    for nn in range(1,5):
        for p in [(9,9),(-2*nn,-2*nn),(10**60,3),(1,1)]:
            check_instance(r,ctx,{'k':nn,'px':p[0],'py':p[1]},counters,seed|{p})
    # One exact first-J10 relation, solved simultaneously for exponent and marker.
    s=Schema(['k','px','py'],[Power(W,k),'L'],domain='k>=1')
    r=compile_schema(s,ctx,s.black_set(ctx,'('+formula+') or (x=px and y=py)'))
    expected=s.param_set(ctx,'px=-2*k and py=-2*k')
    assert r.feasible.is_equal(expected)
    assert r.feasible.is_equal(r.feasible.intersect(defect_domain(s,ctx,1,exact=True,ends_bad=True)))
    relations['all_coordinate_first_marker_event']=str(s.endpoint_map(ctx,r.feasible))
    huge={'k':10**60,'px':-2*10**60,'py':-2*10**60}
    assert not r.feasible.intersect(point_domain(s,ctx,huge)).is_empty()
    assert s.length.evaluate(huge)==104*10**60+1

    # Existentially eliminate ALL initial coordinates for a supplied rail schema.
    for mass in range(3):
        names=tuple(v for i in range(mass) for v in (f'a{i}',f'b{i}'))
        s=Schema(('k',*names),[Power('LRRL',k)],heading=1)
        black,distinct=exact_seed_formula([(f'a{i}',f'b{i}') for i in range(mass)])
        r=compile_schema(s,ctx,s.black_set(ctx,black))
        answer=r.feasible.intersect(s.param_set(ctx,distinct)).project_params(1,2*mass).coalesce()
        expect=ctx.set(f'[k] -> {{ : 0<=k<={mass//2} }}')
        assert answer.is_equal(expect)
        relations[f'rail_all_coordinates_mass_{mass}']=str(answer)

    # Moduli 2/4, all quarter turns, empty fragments, zero powers, cross-block rereads.
    rng=Random(731909)
    loops=['RRRR','LLLL','LRRL','RLLR',T,A,W]
    for _ in range(32):
        u,v=rng.choice(loops),rng.choice(loops)
        prefix=''.join(rng.choice('LR') for _ in range(rng.randrange(6)))
        middle=''.join(rng.choice('LR') for _ in range(rng.randrange(5)))
        suffix=''.join(rng.choice('LR') for _ in range(rng.randrange(5)))
        s=Schema(['n','m'],[prefix,Power(u,n),middle,Power(v,m),suffix],heading=rng.randrange(4),pose=(13,-21))
        r=compile_schema(s,ctx)
        for nn,mm in [(0,0),(0,2),(2,0),(1,1),(2,3)]:
            check_instance(r,ctx,{'n':nn,'m':mm},counters)
    for w in ['', 'R', 'RRRRR', 'LRRL'*4]:
        s=Schema([], [w]);r=compile_schema(s,ctx);check_instance(r,ctx,{},counters)

    # Exhaust a small finite generator only; not the enormous all-input cover.
    all_desc=list(descriptions(2,3,loops=('RRRR','LRRL')))
    assert len(all_desc)==len(set(all_desc))==descriptor_count(2,3,2)==557
    for pieces,words in all_desc:
        assert len(pieces)==len(words)+1 and sum(map(len,pieces))<=3 and len(words)<=2
    assert cover_bounds(0)==(5,2048) and cover_bounds(1)==(10,4097)
    capped=all_coordinate_existence(2,1,max_schemas=5)
    assert capped['status']=='UNKNOWN' and capped['schemas']==5
    # Negative controls distinguish invalid schemas, physical mismatch and native caps.
    rejected=0
    for fn in [lambda:Power('R',n),lambda:Schema(['x'],['R']),lambda: n*m]:
        try:fn()
        except (TypeError,ValueError):rejected+=1
    assert rejected==3
    tiny=Context(max_operations=1)
    try:
        tiny.set('[n] -> { [x] : exists (j: 0<=j<n and x=2*j) }').coalesce()
    except ArithmeticError:rejected+=1
    assert rejected==4
    assert sample_parameters(ctx.set('[a,b] -> { : a>=3 and b=-2*a }'),2)==(3,-6)
    assert ctx.set('[a] -> { : a>=1 }').subtract(ctx.set('[a] -> { : a>=2 }')).is_equal(ctx.set('[a] -> { : a=1 }'))

    return dict(schema='presburger-defect-compiler-v1',scope='supplied-schema exact arithmetic and analytic global coverage; no HC proof',
                native_version=ctx.version,relations=relations,controls=counters,
                complete_toy_descriptors=557,negative_controls=rejected+1,
                full_nonzero_budget_cover_executed=False,
                imported_coverage=dict(max_cycles_per_silent_run=5,noncyclic_vertices=956,period_sum=212,warmup=149),
                huge_marker=dict(epoch='10^60',event_time='104*10^60',post_time='104*10^60+1',literal_replay=False),
                source_sha256={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                               for name in ['isl_exact.py','compiler.py','cover.py','check.py']})


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path)
    p.add_argument('--compare',type=Path)
    args=p.parse_args(); report=run()
    if args.compare:
        old=json.loads(args.compare.read_text())
        # ISL may print a different but equivalent normal form across versions.
        a={k:v for k,v in report.items() if k not in {'native_version','relations'}}
        b={k:v for k,v in old.items() if k not in {'native_version','relations'}}
        assert a==b,'deterministic non-format report changed'
        ctx=Context()
        for key,text in old['relations'].items():
            parse=ctx.map if '[] ->' in text else ctx.set
            assert parse(text).is_equal(parse(report['relations'][key])),key
    text=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(text)
    print(text)

if __name__=='__main__':main()
