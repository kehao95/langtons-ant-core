"""Exact parametric controls plus independent literal finite tests.
No bounded example is used to establish the full parametric theorem.
"""
from pathlib import Path
import argparse,itertools,json,random,time,hashlib
from trace_arithmetic import Aff,Block,Schema
from isl_bridge import Context,ArithmeticFailure,count_fixed
from examples import A,B,STANDARD,three_sweep,triple_fold
from flat_cover import L10,inspect

HERE=Path(__file__).resolve().parent

def literal(word,heading=0,initial=None,start=(0,0)):
    # Independent vector rotation, not the schema's direction table.
    vector=((0,1),(1,0),(0,-1),(-1,0))[heading]
    point=start;last={};required=set();firstL=[];pairs=[];visits=[];valid=True
    field=None if initial is None else set(initial)
    for i,ch in enumerate(word):
        visits.append(point)
        if point in last:
            j,c=last[point];pairs.append((j,i))
            if c==ch:valid=False
        elif ch=='L':required.add(point);firstL.append(i)
        if field is not None:
            if (point in field)!=(ch=='L'):valid=False
            field.symmetric_difference_update((point,))
        last[point]=(i,ch)
        dx,dy=vector;vector=(dy,-dx) if ch=='R' else (-dy,dx)
        point=point[0]+vector[0],point[1]+vector[1]
    return dict(valid=valid,required=required,field=field,endpoint=point,visits=visits,pairs=pairs,firstL=firstL)

def check_short_words(maxlength=7):
    total=0;valid=0;steps=0
    for n in range(maxlength+1):
        for letters in itertools.product('RL',repeat=n):
            word=''.join(letters);s=Schema([], [Block(word)] if word else [])
            ref=literal(word);a=s.analyze(None,method='composition')
            assert (not a['good'].empty())==ref['valid']
            expected=s.ctx.map('[] -> { '+('; '.join(f'[t={i}] -> [u={j}]' for i,j in ref['pairs']) or '[t] -> [u] : false')+' }')
            assert a['successive'].equal(expected)
            if ref['valid']:
                assert a['required_initial_black'].equal(s.point_field(ref['required']));valid+=1
            total+=1;steps+=n
    return dict(words=total,valid=valid,requested_updates=steps)

def check_powered(number=48):
    rng=random.Random(20261015);n,m=Aff.var('n'),Aff.var('m');tested=valid=updates=0
    loops=['RLLR','LRRL','RRRR','LLLL','RL','LR']
    for k in range(number):
        v=''.join(rng.choice('RL') for _ in range(rng.randrange(1,6)))
        w=''.join(rng.choice('RL') for _ in range(rng.randrange(1,5)))
        blocks=[Block(v),Block(rng.choice(loops),n),Block(w),Block(rng.choice(loops),m)]
        heading=rng.randrange(4);s=Schema(['n','m'],blocks,heading=heading,domain='n>=0 and m>=0')
        a=s.analyze(None,method='composition');b=s.analyze(None,method='lexmin')
        assert a['successive'].equal(b['successive']) and a['good'].equal(b['good'])
        base=literal(s.instantiate({'n':1,'m':1}),heading)['required']
        concrete=s.analyze(s.point_field(base),method='lexmin')
        for nn,mm in itertools.product(range(4),repeat=2):
            values={'n':nn,'m':mm};word=s.instantiate(values);ref=literal(word,heading)
            assert (not s.at(a['good'],values).empty())==ref['valid']
            if ref['valid']:
                assert s.at(a['required_initial_black'],values).equal(s.at(s.point_field(ref['required']),values));valid+=1
            r=literal(word,heading,base)
            assert (not s.at(concrete['good'],values).empty())==r['valid']
            if r['valid']:
                assert s.at(concrete['final_black'],values).equal(s.at(s.point_field(r['field']),values))
            tested+=1;updates+=len(word)
    return dict(schemas=number,assignments=tested,feasible_assignments=valid,literal_updates=updates)

def check_parametric():
    records={};n,m=Aff.var('n'),Aff.var('m')
    s,field=three_sweep();r=s.analyze(field,method='composition');r2=s.analyze(field,method='lexmin')
    assert r['good'].equal(s.domain) and r['successive'].equal(r2['successive'])
    expected=s.segment_field([(0,1,1,0,2*n),(0,3,1,0,2*n)]).union(s.point_field([(-1,1),(-1,2),(2*n,1),(2*n,2)]))
    assert r['final_black'].equal(expected)
    records['three_sweep']={'domain':str(r['good']),'endpoint_field':str(r['final_black']),'all_lengths':True}
    # Simultaneously unbounded run length and marker coordinates, including overlap.
    aa,bb=Aff.var('aa'),Aff.var('bb')
    s=Schema(['n','aa','bb'],[Block('RLLR',n)],heading=1,domain='n>=0')
    rail=s.segment_field([(0,-1,1,0,2*n)]);field=rail.union(s.point_field([(aa,bb)]))
    r=s.analyze(field,method='lexmin')
    expected=s.ctx.set('[n,aa,bb] -> { : n>=0 and (bb!=0 or aa<0 or aa>=2n) }')
    assert r['good'].equal(expected)
    huge={'n':10**60,'aa':10**61,'bb':0}
    end=s.segment_field([(0,0,1,0,2*n)]).union(s.point_field([(aa,bb)]))
    assert s.at(r['final_black'],huge).equal(s.at(end,huge))
    records['unrestricted_marker']={'domain':str(r['good']),'huge_count':str(10**60),'complete_endpoint_checked':True}
    # Exact nonempty two-fold domain, with a compact first-black table.
    s=Schema(['n','m'],[Block(B),Block(A,n),Block(B),Block(A,m)],domain='n>=0 and m>=0')
    r=s.analyze(None,method='lexmin');expected=s.ctx.set('[n,m] -> { : n>=1 and 0<=m<n }')
    assert r['good'].equal(expected)
    fixed0=[2,3,4,9,20,21,23,24,26,28,29,37,44,45,46,55,61,72,73,74,83,89,100,101]
    fixed2=[2,3,4,20,21,23,24,26,28,29,37,44,45,46,55,61,72,73,74,83,89,100,101]
    variable=[0,9,15,26,27]
    entries=[f'[t={i}]' for i in fixed0]+[f'[t={102+ i}+28n]' for i in fixed2]
    entries += [f'[t] : exists (j : 0<=j<n and t=102+28j+{i})' for i in variable]
    entries += [f'[t] : exists (j : 0<=j<m and t=204+28n+28j+{i})' for i in variable]
    first=s.ctx.set('[n,m] -> { '+'; '.join(entries)+' }').restrict(expected)
    actual=r['first_times'].intersect(s.left.domain()).restrict(r['good'])
    assert first.equal(actual)
    # Every displayed time family is disjoint: block separation and distinct phases.
    records['two_fold']={'domain':str(r['good']),'root_cost':'5*n+5*m+47','fixed_first_L':[fixed0,fixed2],'power_first_L_phases':variable,'all_parameter_identity_checked':True}
    # Universal three-fold exclusion in two exact formulations.
    s,_=triple_fold();r=s.analyze(None,method='composition');r2=s.analyze(None,method='lexmin')
    assert r['good'].empty() and r2['good'].empty() and r['successive'].equal(r2['successive'])
    records['three_fold']={'domain':str(r['good']),'two_successor_formulations_agree':True}
    # Finite-fuel scanner root and defect threshold, including zero powers.
    s=Schema(['n'],[Block('LRRL',n)],heading=1,domain='n>=0')
    r=s.analyze();firstL=r['first_times'].intersect(s.left.domain());defects=s.defect_times(L10)
    assert defects.equal(s.ctx.set('[n] -> { [t] : n>=0 and 9<=t<4n }'))
    for budget in range(13):
        assert s.cardinality_at_most(firstL,budget).equal(s.ctx.set(f'[n] -> {{ : 0<=n<={budget//2} }}'))
        assert s.cardinality_at_most(defects,budget).equal(s.ctx.set(f'[n] -> {{ : 0<=n<={(budget+9)//4} }}'))
    records['thresholds']={'root_cost':'2*n','defect_count':'max(0,4*n-9)','exact_threshold_checks':26}
    # Infinite schema with unbounded support requirements; never a finite seed.
    s=Schema([], [Block('RLLR',None)],heading=1)
    r=s.analyze(s.field('false'),method='composition');assert r['good'].empty()
    r=s.analyze(s.field('y=-1 and x>=0'),method='composition');assert r['good'].equal(s.domain)
    assert r['required_initial_black'].equal(s.field('y=-1 and x>=0'))
    records['infinite_scope_control']={'empty_finite_seed_rejected':True,'infinite_black_ray_accepted_only_when_explicitly_supplied':True}
    return records

def controls():
    rejected=0
    for fn in (lambda:Schema(['n'],[Block('R',Aff.var('n'))]),lambda:Schema(['n'],[Block('RLLR',None),Block('R')]),lambda:Aff.var('a')*Aff.var('b')):
        try:fn()
        except ValueError:rejected+=1
        else:raise AssertionError('bad input accepted')
    try:Schema([], [Block(STANDARD,None)],ctx=Context(max_operations=1))
    except ArithmeticFailure:rejected+=1
    else:raise AssertionError('operation limit not detected')
    from budget_schema import compile_all_coordinates
    capped=compile_all_coordinates(0,1,max_schemas=4)
    assert capped['status']=='INCONCLUSIVE' and capped['schemas']==4
    return {'input_and_resource_rejections':rejected,'resource_error_is_not_NO':True,'global_generator_cap':'INCONCLUSIVE'}

def main(full=True):
    if not __debug__:raise RuntimeError('Do not disable assertions')
    start=time.monotonic();report={'status':'passed','scope':'Exact supplied-schema arithmetic, with inherited complete bounded-defect coverage; no unrestricted HC decider.'}
    report['backend']=Context().version
    report['short']=check_short_words(7 if full else 4);print('short passed',flush=True)
    report['powered']=check_powered(48 if full else 6);print('powered passed',flush=True)
    report['parametric']=check_parametric();print('parametric passed',flush=True)
    report['flat_cover']=inspect();report['negative_controls']=controls()
    report['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('*.py'))}
    report['wall_seconds_informational']=time.monotonic()-start
    out=HERE.parent/'evidence'/'replay.json';out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');a=parser.parse_args();main(not a.quick)
