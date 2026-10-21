from __future__ import annotations
import _paths  # Pin and load the unchanged sibling schema syntax.
import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path
from compiler import Schema,Power,var,Affine,W,T,A,geometry,scan_factors,compile_schema,L10
from isl_exact import Context
from stream_qf import Encoder,Segment,point_source,Circuit,STRIDES,atom
from factor_dag import count_circuit
from solver import Session,version
import numeric
from api import solve_schema

STANDARD=[(-1,2),(0,-1),(0,1),(0,2),(1,-1),(1,2),(2,-1),(2,0),(2,1),(2,3),
          (3,-2),(3,-1),(3,0),(3,1),(3,3),(4,1),(4,2)]

def require_unsat(s,expr,label):
    got=s.check(expr)
    if got!='unsat':raise AssertionError((label,got))


def all_intersections():
    count=0;nodes=0
    for ds in sorted(STRIDES):
        for dr in [(0,0),*sorted(STRIDES)]:
            for e in (0,1):
                schema=Schema(('nn','mm','ax','ay','zz'),[])
                enc=Encoder(schema,[]);c=enc.c
                s=Segment((0,0),ds,var('nn'))
                r=Segment((var('ax'),var('ay')),dr,1 if dr==(0,0) else var('mm'))
                v=enc.intersection(s,r,e)
                zz='zz';lhs=c.and_(v.active,c.le(v.lo,zz),c.le(zz,v.hi))
                point=(ds[0]*(2*var('zz')+e),ds[1]*(2*var('zz')+e))
                rhs=enc.member(r,point)
                difference=atom(c.xor([lhs,rhs]))
                with Session(10000) as solver:
                    solver.run(c.text())
                    require_unsat(solver,difference,('intersection',ds,dr,e))
                nodes+=c.nodes;count+=1
    return dict(all_integer_equivalences=count,circuit_nodes=nodes)


def initial(source,values):
    b=set()
    for s in source:
        n=s.length.evaluate(values)
        if n<0:raise ValueError('negative source count')
        a=tuple(v.evaluate(values) for v in s.anchor)
        for j in range(n):b.symmetric_difference_update([(a[0]+s.stride[0]*j,a[1]+s.stride[1]*j)])
    return b


def literal_plan(schema,source,values):
    word=schema.expand(values,limit=10000);b=initial(source,values)
    p=tuple(v.evaluate(values) for v in schema.pose);h=schema.heading;first=None
    for t,ch in enumerate(word):
        if (p in b)!=(ch=='L') and first is None:first=t
        b.symmetric_difference_update([p]);h=(h+(1 if ch=='R' else -1))%4
        dx,dy=((0,1),(1,0),(0,-1),(-1,0))[h];p=(p[0]+dx,p[1]+dy)
    return dict(valid=first is None,first_bad=first,black=b,pose=p,heading=h,steps=len(word))


def minimal_prefix(word,h):
    req={};black=set();ph,_,_=geometry(word,h)
    for p,_,ch in ph:
        if p not in req:
            if ch=='L':black.add(p)
        elif req[p]==ch:return None
        req[p]=ch
    return sorted(black)


def source_isl(s,ctx,source):
    out=s.black_set(ctx,'false')
    for seg in source:
        a,b=seg.anchor;dx,dy=seg.stride
        if seg.stride==(0,0):text=f'x={a} and y={b}'
        else:text=f'exists (idx: 0<=idx<{seg.length} and x={a}+{dx}*idx and y={b}+{dy}*idx)'
        other=s.black_set(ctx,text)
        out=out.subtract(other).union(other.subtract(out))
    return out.coalesce()


def literal_controls(start=0,stop=34):
    rng=random.Random(20261015);cases=[]
    for u in (W,T,A,'LRRL'):
        for h in range(4):
            s=Schema(('nn','mm'),[Power(u,var('nn'))],heading=h)
            b=minimal_prefix(u*3,h)
            if b is None:raise AssertionError('test loop not feasible for finite prefix')
            cases.append((s,point_source(b),'mode'))
    for i in range(8):
        u=(T,A,'LRRL')[i%3];v=(A,'LRRL',T)[i%3];h=i%4
        bridge=['L','RR','LRL',''][i%4]
        s=Schema(('nn','mm'),[Power(u,var('nn')),bridge,Power(v,var('mm'))],heading=h)
        b=minimal_prefix(s.expand({'nn':1,'mm':1}),h)
        if b is None:b=sorted({(rng.randrange(-6,7),rng.randrange(-6,7)) for _ in range(20)})
        cases.append((s,point_source(b),'paired'))
    # Both signs, parity mod 2, intersections and cancellations in the source.
    for i in range(8):
        s=Schema(('nn','mm'),[Power('LRRL',var('nn')),'RLL',Power(T,var('mm'))],heading=i%4)
        ds=sorted(STRIDES)[i]
        src=[Segment((var('mm')-2,-var('nn')),ds,var('nn')),
             Segment((0,0),(2,0),var('mm')),Segment((1,0))]
        if i%2:src += [Segment((3,4)),Segment((3,4))]
        cases.append((s,tuple(src),'xor'))
    cases.append((Schema(('nn','mm'),[]),point_source([(100,100)]),'empty'))
    cases.append((Schema(('nn','mm'),['RRRRR']),(),'impossible'))
    totals=dict(schemas=0,parameter_instances=0,literal_plan_updates=0,valid_complete_endpoints=0,
                invalid_prefixes=0,endpoint_bit_checks=0,legacy_feasibility_comparisons=0)
    if not 0<=start<=stop<=len(cases):raise ValueError('invalid literal test range')
    for s,source,name in cases[start:stop]:
        enc=Encoder(s,source);ctx=Context(30000000)
        old=compile_schema(s,ctx,source_isl(s,ctx,source))
        with Session(10000) as solver:
            solver.run(enc.c.text())
            for n,m in itertools.product(range(4),repeat=2):
                values={'nn':n,'mm':m};lit=literal_plan(s,source,values);fast=numeric.verify(s,source,values)
                if lit['valid']!=fast['valid'] or lit['first_bad']!=fast['first_bad']:
                    raise AssertionError(('independent numeric',name,values,lit,fast))
                dom=s.param_set(ctx,f'nn={n} and mm={m}')
                legacy=not old.feasible.intersect(dom).is_empty()
                if legacy!=lit['valid']:raise AssertionError(('legacy mismatch',name,values))
                condition=f'(and (= nn {n}) (= mm {m}) {"(not "+atom(enc.valid)+")" if lit["valid"] else atom(enc.valid)})'
                require_unsat(solver,condition,('compiled vs literal',name,values))
                if fast['post_position']!=lit['pose'] or fast['post_heading']!=lit['heading']:
                    raise AssertionError('pose mismatch')
                totals['parameter_instances']+=1;totals['literal_plan_updates']+=lit['steps']
                totals['legacy_feasibility_comparisons']+=1
                if lit['valid']:
                    totals['valid_complete_endpoints']+=1
                    # Check the ENTIRE support box, plus an off-trace marker.
                    rs,_,_,_=numeric.streams(s,values)
                    points=set(lit['black'])|initial(source,values)|{(0,0)}
                    for seg,_,_,_ in rs:
                        p,d,k=seg
                        if k:points|={p,(p[0]+d[0]*(k-1),p[1]+d[1]*(k-1))}
                    for axis in (0,1):
                        if max(p[axis] for p in points)-min(p[axis] for p in points)>1000:raise AssertionError('oversized literal box')
                    xmin,xmax=min(p[0] for p in points),max(p[0] for p in points)
                    ymin,ymax=min(p[1] for p in points),max(p[1] for p in points)
                    reconstructed=set()
                    for p in itertools.product(range(xmin,xmax+1),range(ymin,ymax+1)):
                        if numeric.endpoint_bit(s,source,values,p):reconstructed.add(p)
                        totals['endpoint_bit_checks']+=1
                    if reconstructed!=lit['black']:raise AssertionError('full endpoint mismatch')
                else:totals['invalid_prefixes']+=1
        totals['schemas']+=1
        print('literal schema',totals['schemas'],flush=True)
    return totals


def factor_controls():
    rng=random.Random(59105);total=0;nodes=0
    for i in range(20):
        params=('nn','mm','kk');parts=[]
        for j,p in enumerate(params):
            u=[W,T,A,'LRRL','RRRR','RLRLLRLR'][(i+j)%6]
            parts.extend([''.join(rng.choice('RL') for _ in range(i%4)),Power(u,var(p))])
        parts.append('' if i%2 else 'LLR')
        s=Schema(params,parts);c=Circuit(params);count,state=count_circuit(s,c)
        with Session(10000) as solver:
            solver.run(c.text())
            for values_tuple in itertools.product(range(4),repeat=3):
                values=dict(zip(params,values_tuple));word=s.expand(values)
                expected=sum(word[j-9:j+1] not in L10 for j in range(9,len(word)))
                last=len(word)>=10 and word[-10:] not in L10
                cond='(and '+' '.join(f'(= {p} {v})' for p,v in values.items())+' '
                wrong=f'(or (not (= {atom(count)} {expected})) (xor {atom(state.last_bad)} {atom(last)}))'
                require_unsat(solver,cond+wrong+')',('factor',i,values))
                if numeric.factor_count(s,values)!=(expected,last):raise AssertionError('independent compressed factor count')
                total+=1
        nodes+=c.nodes
    # A nonenumerated 64-power family: every positive number of W copies is legal.
    params=tuple(f'kk{i}' for i in range(64));s=Schema(params,[Power(W,var(p)) for p in params])
    c=Circuit(params);count,_=count_circuit(s,c)
    with Session(10000) as solver:
        solver.run(c.text())
        condition='(and '+' '.join(f'(>= {p} 0)' for p in params)+f' (not (= {atom(count)} 0)))'
        require_unsat(solver,condition,'64 unbounded powers')
    return dict(literal_parameter_instances=total,circuit_nodes=nodes,
                unbounded_64_power_count_zero=True,wide_circuit_nodes=c.nodes,
                wide_old_case_count=str(2**64),wide_smt_bytes=len(c.text().encode()))


def symbolics():
    # Exact all-coordinate parameter relation, no coordinate bound.
    s=Schema(('kk','px','py'),[Power(W,var('kk')),'L'])
    src=point_source(STANDARD)+point_source([(var('px'),var('py'))])
    enc=Encoder(s,src);count,last=count_circuit(s,enc.c)
    with Session(30000) as solver:
        solver.run(enc.c.text())
        require_unsat(solver,f'(and (> kk 0) (xor {atom(enc.valid)} (and (= px (* (- 2) kk)) (= py (* (- 2) kk)))))','marker domain')
        require_unsat(solver,f'(and (> kk 0) {atom(enc.valid)} (or (not (= {atom(count)} 1)) (not {atom(last.last_bad)})))','marker defect')
    huge=10**60;v={'kk':huge,'px':-2*huge,'py':-2*huge}
    answer=numeric.verify(s,src,v)
    if not answer['valid'] or answer['post_time']!=104*huge+1:raise AssertionError('huge witness')
    damaged={**v,'px':v['px']+1}
    if numeric.verify(s,src,damaged)['valid']:raise AssertionError('damaged marker')
    # Finite-input rail. The source itself is a compact finite XOR family.
    s2=Schema(('nn','kk'),[Power('LRRL',var('kk'))],heading=1)
    source=(Segment((0,0),(2,0),var('nn')),Segment((1,0),(2,0),var('nn')))
    e2=Encoder(s2,source)
    with Session(10000) as solver:
        solver.run(e2.c.text())
        require_unsat(solver,f'(xor {atom(e2.valid)} (and (>= nn 0) (>= kk 0) (<= kk nn)))','rail exact domain')
    return dict(marker_all_coordinate_relation='kk>0 => (valid iff px=py=-2*kk)',
                marker_exact_defect_count=1,marker_encoder=enc.stats(),
                huge_parameter=str(huge),huge_post_time=str(answer['post_time']),
                huge_numeric_parity_checks=answer['checks'],damaged_marker_rejected=True,
                rail_all_parameter_equivalence=True)



def endpoint_and_api():
    s=Schema(('nn','kk','qx','qy'),[Power('LRRL',var('kk'))],heading=1)
    huge=10**60
    source=(Segment((0,0),(2,0),var('nn')),Segment((1,0),(2,0),var('nn')),
            Segment((huge,100)),Segment((3,99)),Segment((3,99)))
    enc=Encoder(s,source);black=enc.black_at((var('qx'),var('qy')))
    # Entire infinite coordinate plane, every n,k with 0<=k<=n. Two equal
    # markers cancel by XOR; the remote untouched marker remains in the field.
    expected=f'(or (and (= qy 0) (<= (* 2 kk) qx) (< qx (* 2 nn))) (and (= qy 1) (<= 0 qx) (< qx (* 2 kk))) (and (= qx {huge}) (= qy 100)))'
    with Session(10000) as solver:
        solver.run(enc.c.text())
        require_unsat(solver,f'(and (>= nn 0) (>= kk 0) (<= kk nn) (xor {atom(black)} {expected}))','full endpoint all coordinates')
    # Two genuinely different Boolean encodings of the boundary condition.
    s2=Schema(('nn','mm'),[Power(T,var('nn')),'LR',Power(A,var('mm'))])
    src=point_source([(-1,0),(0,-1),(2,2)])
    jumps=Encoder(s2,src,method='jumps');values=Encoder(s2,src,method='values')
    import re
    renamed=re.sub(r'\baux(\d+)\b',r'auxV\1',values.c.text())
    renamed='\n'.join(line for line in renamed.splitlines() if not line.startswith('(declare-const nn ') and not line.startswith('(declare-const mm '))
    value_valid=re.sub(r'\baux(\d+)\b',r'auxV\1',atom(values.valid))
    with Session(30000) as solver:
        solver.run(jumps.c.text()+renamed)
        require_unsat(solver,f'(xor {atom(jumps.valid)} {value_valid})','jump/value encodings')
    rail=Schema(('nn','kk'),[Power('LRRL',var('kk'))],heading=1)
    rail_source=(Segment((0,0),(2,0),var('nn')),Segment((1,0),(2,0),var('nn')))
    sat=solve_schema(rail,rail_source,defects=31,where=lambda c:c.eq('nn',10))
    if sat['status']!='SAT' or sat['witness']['defects']<31:raise AssertionError('API SAT')
    no=solve_schema(rail,rail_source,where=lambda c:c.and_(c.eq('nn',3),c.eq('kk',4)))
    if no['status']!='UNSAT':raise AssertionError('API UNSAT')
    empty=solve_schema(Schema((),[]),point_source([(huge,100)]),defects=0,exact=True)
    if empty['status']!='SAT' or empty['witness']['post_time']!=0:raise AssertionError('empty API')
    # Sparse-coordinate lists must exclude duplicates, unlike XOR-segment inputs.
    from stream_qf import distinct_formula
    points=[(var('aa'),0),(var('bb'),0)]
    with Session() as solver:
        solver.run('(declare-const aa Int)(declare-const bb Int)')
        require_unsat(solver,f'(xor {distinct_formula(points)} (distinct aa bb))','sparse list distinctness')
    # Deterministic native resource exhaustion must stay UNKNOWN, not UNSAT.
    with Session() as solver:
        solver.run('(set-option :rlimit 1)(declare-const trial Int)(assert (> trial 0))')
        exhausted=solver.check()
        if exhausted!='unknown':raise AssertionError(('resource control not triggered',exhausted))
    return dict(full_endpoint_all_coordinate_equivalence=True,jump_value_all_parameter_equivalence=True,
                sparse_distinctness_equivalence=True,api_sat_independently_verified=True,
                api_unsat_scope='supplied schema only',api_empty_word=True,resource_result=exhausted)


def negative_controls():
    count=0
    for f in [lambda:Encoder(Schema(('nn',),[Power('RRRR',var('nn'))]),()),
              lambda:Encoder(Schema(('nn',),[Power(W,var('nn'))],domain='nn>=0'),()),
              lambda:Segment((0,0),(3,1),var('nn')),
              lambda:Segment((0,0),(0,0),var('nn')),
              lambda:Encoder(Schema(('aux0',),[]),()),
              lambda:Encoder(Schema((),[]),(),method='guess'),
              lambda:Encoder(Schema((),[]),point_source([(var('undeclared'),0)]))]:
        try:f()
        except (ValueError,TypeError):count+=1
        else:raise AssertionError('invalid input accepted')
    with Session() as s:
        try:s.run('(assert (= undeclared_thing 0))')
        except ArithmeticError:count+=1
        else:raise AssertionError('solver error not raised')
    return dict(rejected=count)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--part',choices=['all','intersections','literal','factors','symbolic','endpoints','negative'],default='all')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--literal-start',type=int,default=0)
    parser.add_argument('--literal-stop',type=int,default=34)
    args=parser.parse_args()
    tests={'intersections':all_intersections,'literal':lambda:literal_controls(args.literal_start,args.literal_stop),'factors':factor_controls,'symbolic':symbolics,'endpoints':endpoint_and_api,'negative':negative_controls}
    out={'solver_version':version()}
    for name,test in tests.items():
        if args.part not in ('all',name):continue
        out[name]=test();print(name,json.dumps(out[name],sort_keys=True),flush=True)
    if args.output:args.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
