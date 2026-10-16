#!/usr/bin/env python3
"""Fresh exact all-parameter checks; independent literal controls are separate."""
import argparse,copy,hashlib,itertools,json,random,subprocess,tempfile
from pathlib import Path
from fractions import Fraction
from isl_core import Context,lib,fn,S
from supply import Schema,compile,joint_relation,unary_count,literal_minimal,geometry,W,A,B,PULSE,Unsupported
import dichotomy
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)

def schemas():
    return {
      'rail':Schema(['nn'],[('LRRL',(0,1))],domain='nn>=0'),
      'pulse':Schema(['nn'],[(PULSE,(0,1))],domain='nn>=0'),
      'standard':Schema(['nn'],[(W,(0,1))],domain='nn>=0'),
      'archive':Schema(['aa','bb','cc'],[(B[9:],None),(A,(0,1,0,0)),(B,None),
          (A,(0,0,1,0)),(PULSE,(0,0,0,1))],domain='aa>=0 and bb>=0 and cc>=0',pose=(-1,0,3)),
      'three_fold':Schema(['aa','bb'],[(B,None),(A,(0,1,0)),(B,None),(A,(0,0,1)),(B,None)],domain='aa>=0 and bb>=0')}

def native(fixtures):
    lines=[W,str(len(fixtures))]
    for name,values,s,w in fixtures:lines.append(' '.join(map(str,s.pose))+' '+(w or '-'))
    with tempfile.TemporaryDirectory(prefix='ant-supply-native-') as td:
        exe=Path(td)/'check';subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror',str(HERE/'independent.cpp'),'-o',str(exe)],check=True,capture_output=True,timeout=40)
        out=subprocess.run([str(exe)],input='\n'.join(lines)+'\n',capture_output=True,text=True,check=True,timeout=45).stdout
    rows=iter(out.splitlines());results=[]
    for item in fixtures:
        h=next(rows).split()
        if h==['NO']:results.append(None);continue
        need(h[0]=='YES' and len(h)==8,'native format');data=list(map(int,h[1:]));ns,df,nb,*pose=data
        seed={tuple(map(int,next(rows).split())) for _ in range(ns)}
        black={tuple(map(int,next(rows).split())) for _ in range(nb)}
        need(len(seed)==ns and len(black)==nb,'duplicate native cells');results.append((seed,black,df,pose))
    need(next(rows,None) is None,'extra native output');return results

def check():
    ctx=Context();ss=schemas();witness=json.loads((HERE/'witness.json').read_text());records={};compiled={};certificates={}
    need(witness['schema']=='flat-schema-supply-v1','wrong witness')
    for name,s in ss.items():
        cert=[]
        if name=='three_fold':
            r=compile(s,ctx);need(r['feasible'].empty(),'three fold became feasible');records[name]={'feasible':str(r['feasible'])};compiled[name]=r;continue
        r=joint_relation(s,ctx,cert);compiled[name]=r;certificates[name]=cert
        records[name]={k:str(r[k]) for k in ('feasible','supply','defects')};records[name]['count_pieces']=len(cert)
        if name in witness:
            projected=r['joint'].project(1,0,len(s.params)).coalesce()
            records[name]['dichotomy']=dichotomy.verify(ctx,projected,witness[name]['components'])
    s=ss['archive'];r=compiled['archive'];spec=witness['archive'];H=s.header
    expected=ctx.set(H+'{: '+spec['feasible']+'}')
    need(r['feasible'].equal(expected),'declared domain mismatch')
    need(r['supply'].equal(ctx.set(H+'{[c]: '+spec['feasible']+' and '+spec['supply']+'}')),'supply claim mismatch')
    need(r['defects'].equal(ctx.set(H+'{[d]: '+spec['feasible']+' and ('+spec['defects']+')}')),'defect claim mismatch')
    budget=r['joint'].intersect(ctx.set('[aa,bb,cc,mm]->{[c,d]:c<=mm}')).project(1,0,3).project(3,0,1).lexmax().coalesce()
    expected_budget=ctx.set('[mm]->{[d]:mm>=51 and exists(q: q>=0 and 10*q<=mm-51<10*q+10 and d=9*q+15)}')
    need(budget.equal(expected_budget),'sharp at-most-m budget');records['archive']['exact_budget']=str(budget)
    badbound=r['joint'].intersect(ctx.set(H+'{[c,d]:10*d>9*c-309}'))
    need(badbound.empty(),'sharp upper bound');need(not r['joint'].intersect(ctx.set(H+'{[c,d]:10*d>9*c-310}')).empty(),'false improvement not rejected')
    # The growing equality ray proves the coefficient cannot be decreased.
    equalray=r['joint'].intersect_params(ctx.set(H+'{:aa=bb+1 and cc=bb+2 and bb>=0}'))
    need(equalray.equal(ctx.set(H+'{[c,d]:aa=bb+1 and cc=bb+2 and bb>=0 and c=51+10*bb and d=15+9*bb}')),'equality ray')
    # The fixed-mass branch is tested only on arithmetic data, not an ant claim.
    vertical=[{'base':[7,2],'generators':[[0,3],[1,0]]}]
    arithmetic=dichotomy.verify(ctx,dichotomy.relation(ctx,vertical),vertical)
    need(arithmetic['kind']=='fixed_mass_unbounded','vertical branch')
    records['arithmetic_vertical_control']={**arithmetic,'is_ant_orbit':False}
    # Unary counting residue/empty controls and an explicit unsupported hole.
    cs=ctx.set('[nn]->{[j]:nn>=0 and 0<=j<nn and j%2=0}')
    counts=unary_count(ctx,'[nn]->',ctx.set('[nn]->{:nn>=0}'),cs,moduli=(2,))
    need(counts.equal(ctx.set('[nn]->{[c]:nn>=0 and nn<=2*c<=nn+1}')),'unary parity count')
    hole=ctx.set('[nn]->{[j]:nn>=0 and 0<=j<2*nn and 0<=j%4<=1}')
    try:unary_count(ctx,'[nn]->',ctx.set('[nn]->{:nn>=0}'),hole)
    except Unsupported:pass
    else:raise ValueError('unsupported holes did not remain unknown')
    fixedhole=unary_count(ctx,'[nn]->',ctx.set('[nn]->{:nn>=0}'),hole,moduli=(4,))
    need(fixedhole.equal(ctx.set('[nn]->{[c]:nn>=0 and ((nn%2=0 and c=nn) or (nn%2=1 and c=nn+1))}')),'residue refinement')
    damaged=[]
    for label,mut in [('missing_linear_component',lambda z:z.pop()),('wrong_minimum_supply',lambda z:z[2]['base'].__setitem__(0,50)),('false_event_slope',lambda z:z[2]['generators'][0].__setitem__(1,10))]:
        comps=copy.deepcopy(spec['components']);mut(comps)
        try:dichotomy.verify(ctx,r['joint'].project(1,0,3),comps)
        except ValueError:damaged.append(label)
        else:raise ValueError('damaged semilinear certificate accepted')
    for kw in [[('R',(0,1))],[('',(0,1))]]:
        try:Schema(['nn'],kw,domain='nn>=0')
        except ValueError:damaged.append('nonresetting_or_empty_power')
        else:raise ValueError('bad power accepted')
    # Test every small independent exponent tuple, including all infeasible boundaries.
    fixtures=[]
    for name in ('rail','pulse','standard'):
        vals=list(range(25))+[31,64,127]
        for n in vals:
            sc=ss[name];fixtures.append((name,(n,),sc,sc.instantiate((n,))))
    vals=set(itertools.product(range(10),repeat=3));rng=random.Random(20261015)
    vals|={(rng.randrange(1,80),rng.randrange(0,80),rng.randrange(0,82)) for _ in range(200)}
    vals|={(a,b,c) for a,b,c in ((1000,999,1001),(1000,0,2),(1,0,3),(1,1,0),(127,126,128))}
    for abc in sorted(vals):fixtures.append(('archive',abc,s,s.instantiate(abc)))
    for aa,bb in itertools.product(range(6),repeat=2):
        sc=ss['three_fold'];fixtures.append(('three_fold',(aa,bb),sc,sc.instantiate((aa,bb))))
    native_rows=native(fixtures);nhash=hashlib.sha256();steps=0;positive=0;endpoint_checks=0
    lastR_cache={};symbolic_counts={}
    for (name,values,sc,word),native_row in zip(fixtures,native_rows):
        rr=compiled[name];point=ctx.set(sc.header+'{: '+' and '.join(f'{p}={v}' for p,v in zip(sc.params,values))+'}')
        prediction=not rr['feasible'].intersect(point).empty();literal=literal_minimal(word,sc.pose)
        need(prediction==(literal is not None)==(native_row is not None),'feasibility mismatch')
        if literal is None:
            nhash.update(json.dumps([name,values,False]).encode());continue
        seed,black,pose,d=literal;nseed,nblack,nd,npose=native_row;dx,dy=((0,1),(1,0),(0,-1),(-1,0))[pose[2]]
        need(seed==nseed and black==nblack and d==nd and [pose[0],pose[1],dx,dy]==npose,'independent field mismatch')
        need(rr['supply'].intersect_params(point).equal(ctx.set(sc.header+f'{{[c]:c={len(seed)}}}').intersect_params(point)),'count mismatch')
        need(rr['defects'].intersect_params(point).equal(ctx.set(sc.header+f'{{[d]:d={d}}}').intersect_params(point)),'defect mismatch')
        if symbolic_counts.get(name,0)<8 and max(values)<=12:
            seedtxt=' or '.join(f'(x={x} and y={y})' for x,y in sorted(seed)) or 'false'
            need(rr['firstL'].intersect_params(point).equal(ctx.set(sc.header+'{[x,y]: '+seedtxt+'}').intersect_params(point)),'symbolic full seed mismatch')
            if name not in lastR_cache:
                lastR_cache[name]=rr['reads'].lexmax().intersect(ctx.map(sc.header+'{[x,y]->[t,b]:b=0}')).domain()
            lastR=lastR_cache[name]
            endtxt=' or '.join(f'(x={x} and y={y})' for x,y in sorted(black)) or 'false'
            need(lastR.intersect_params(point).equal(ctx.set(sc.header+'{[x,y]: '+endtxt+'}').intersect_params(point)),'symbolic complete endpoint mismatch')
            endpoint_checks+=1;symbolic_counts[name]=symbolic_counts.get(name,0)+1
        steps+=len(word);positive+=1
        nhash.update(json.dumps([name,values,len(seed),d,sorted(seed),sorted(black),pose],separators=(',',':')).encode())
    # Huge parameters are checked symbolically, without materializing their fields.
    nn=10**60;point=ctx.set(H+f'{{:aa={nn} and bb={nn-1} and cc={nn+1}}}')
    need(r['joint'].intersect_params(point).equal(ctx.set(H+f'{{[c,d]:c={10*nn+41} and d={9*nn+6}}}').intersect_params(point)),'huge exact control')
    fn('isl_version',[],S);version=lib.isl_version().decode().strip()
    report={'schema':'flat-schema-supply-report-v1','exact':records,'native_library':version,
      'finite_controls':{'cases':len(fixtures),'feasible_cases':positive,'full_updates_per_implementation_on_feasible_cases':steps,
                         'complete_symbolic_seed_endpoint_pairs':endpoint_checks,'symbolic_pairs_by_schema':symbolic_counts,'rows_sha256':nhash.hexdigest()},
      'count_certificate_sha256':hashlib.sha256(json.dumps(certificates,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
      'damaged_certificates_rejected':damaged+['falsely_improved_bound'],
      'huge_parameter':str(nn),'general_counting_backend':'certified interval-residue fast path; unsupported is UNKNOWN',
      'not_established':['HC','a finite HC counterexample','fixed-mass unbounded defects for an ant schema','all-input uniform budget','automatic closure of all program families','Lean or external review'],
      'source_sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ('supply.py','isl_core.py','dichotomy.py','check.py','independent.cpp','witness.json')}}
    return report

def main():
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group();g.add_argument('--write',type=Path);g.add_argument('--compare',type=Path);args=p.parse_args()
    raw=(json.dumps(check(),ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
    if args.write:args.write.write_bytes(raw)
    if args.compare:need(args.compare.read_bytes()==raw,'frozen report mismatch')
    print(raw.decode());print('PASS: exact relations, independent dynamics, and scope controls.')
if __name__=='__main__':main()
