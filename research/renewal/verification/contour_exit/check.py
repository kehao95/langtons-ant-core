"""Theorem-local reconstruction. Default compares, never repairs, frozen data."""
from __future__ import annotations
from collections import Counter
from functools import lru_cache
import argparse
import hashlib
import json
from pathlib import Path
from random import Random
import subprocess
import tempfile
import kernel as k

HERE=Path(__file__).resolve().parent
BASE='54cbf29d7454da8c0d088c4c14864a55153e4a18'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def literal(B,root,C,cap=100000):
    """Separate vector rotation dynamics; tests actual incoming-state exit."""
    black=set(B);x,y,h=root;dx,dy=((0,1),(1,0),(0,-1),(-1,0))[h]
    contour=set(C);path=[];word=[];digest=14695981039346656037
    while (x,y,h) in contour:
        if len(path)>=cap:raise RuntimeError('INCONCLUSIVE: literal limit')
        path.append((x,y,h));left=(x,y) in black;letter='L' if left else 'R';word.append(letter)
        for byte in f'{x},{y},{h},{letter};'.encode():
            digest=((digest^byte)*1099511628211)&((1<<64)-1)
        if left:black.remove((x,y));dx,dy=-dy,dx
        else:black.add((x,y));dx,dy=dy,-dx
        x+=dx;y+=dy;h=((0,1),(1,0),(0,-1),(-1,0)).index((dx,dy))
    return len(path),(x,y,h),frozenset(black),tuple(path),''.join(word),digest


def exact_case(B,root):
    out=k.first_contour_exit(B,root)
    t,e,field,path,word,digest=literal(B,root,out.contour)
    assert (out.updates,out.exit_dart,out.black)==(t,e,field)
    assert tuple(out.contour[i] for i in out.itinerary)==path
    assert all((j-i)%4==0 for i,j in enumerate(out.matching) if j is not None)
    assert any(j is None for j in out.matching)
    assert t<=k.physical_state_bound(out.matching)
    if k.noninterlaced(out.matching):
        predicted=k.noninterlaced_itinerary(out.matching)
        assert predicted==out.itinerary and t<=len(out.contour)+1
    return out,(t,e,field,path,word,digest)


@lru_cache(None)
def noncrossing_matchings(n):
    if n==0:return ((),)
    result=[(None,)+tuple(None if j is None else j+1 for j in tail)
            for tail in noncrossing_matchings(n-1)]
    for j in range(1,n):
        for inside in noncrossing_matchings(j-1):
            for outside in noncrossing_matchings(n-j-1):
                result.append((j,)+tuple(None if x is None else x+1 for x in inside)+(0,)
                              +tuple(None if x is None else x+j+1 for x in outside))
    return tuple(result)


def cell(a,b):
    x,y=a;xx,yy=b
    if xx==x+1:return x+y,x-y+1
    if yy==y+1:return x+y,x-y
    return cell(b,a)


def tree_field(n,kind):
    if kind=='comb':
        edges=[((0,j),(0,j+1)) for j in range(n-1)]
        edges += [((i,j),(i+1,j))for i in range(n-1)for j in range(n)]
    elif kind=='serpent':
        path=[(i,j)for i in range(n)for j in (range(n)if i%2==0 else range(n-1,-1,-1))]
        edges=list(zip(path,path[1:]))
    else:raise ValueError(kind)
    return frozenset(cell(a,b)for a,b in edges)


def run():
    rng=Random(10202026);counts=Counter();trace=hashlib.sha256();cpp=[];cpp_expected=[]
    def test(B,root,native=False):
        out,data=exact_case(B,root);counts['inputs']+=1;counts['updates']+=out.updates
        counts['noninterlaced']+=int(k.noninterlaced(out.matching))
        counts['interlaced']+=int(not k.noninterlaced(out.matching))
        trace.update(json.dumps([sorted(B),root,out.updates,out.exit_dart,sorted(out.black)],separators=(',',':')).encode())
        if native:cpp.append((B,root));cpp_expected.append(data)
        return out,data
    grid=[(x,y)for x in range(-1,3)for y in range(-1,3)]
    for mask in range(1<<16):
        B=frozenset(p for i,p in enumerate(grid)if mask>>i&1)
        test(B,(0,0,0))
    exhaustive=dict(counts)
    grid3=[(x,y)for x in range(-1,2)for y in range(-1,2)]
    for mask in range(1<<9):
        B=frozenset(p for i,p in enumerate(grid3)if mask>>i&1)
        for h in range(4):test(B,(0,0,h),True)
    for i in range(128):
        B={(rng.randrange(-8,9),rng.randrange(-8,9))for _ in range(rng.randrange(1,85))}
        if i%4==0:B.add((10**60+i,-10**60-i))
        test(frozenset(B),(rng.randrange(-2,3),rng.randrange(-2,3),rng.randrange(4)),True)
    sharp=[]
    for n in list(range(33))+[64,128,1000]:
        B,w=k.sharp_seed(n)
        # Separate explicit-coordinate input formula, not inferred from replay.
        expected={(j+1,j)for j in range(n)}|{(n+1,n),(n+2,n)}
        expected|={(n+2-j,n-1-j)for j in range(n)}|{(2,-1),(1,-1)}
        assert B==expected
        out,data=test(B,(0,0,0),True)
        assert len(out.contour)==4*n+12 and all(j is None for j in out.matching)
        assert out.updates==4*n+13 and data[4]==w+'L'
        assert out.exit_dart==(-1,0,3) and len(out.black)==2*n+7
        sharp.append({'n':n,'initial_black':len(B),'contour_length':len(out.contour),'exit_time':out.updates})
    witness=json.loads((HERE/'witness.json').read_text());B=frozenset(map(tuple,witness['seed']));root=tuple(witness['root'])
    out,data=test(B,root,True)
    assert len(B)==24 and len(out.contour)==witness['length']==100
    assert out.updates==witness['time']==220 and out.updates>2*len(out.contour)
    retained=B|{(10**60,10**60)};extra,_=test(retained,root,True)
    assert extra.contour==out.contour and extra.itinerary==out.itinerary
    assert extra.black==out.black|{(10**60,10**60)}
    shared=[];common_darts=None
    for kind in ['comb','serpent']:
        B0=tree_field(5,kind);o,d=test(B0,(4,0,0),True)
        if common_darts is None:common_darts=set(o.contour)
        else:assert common_darts==set(o.contour)
        assert common_darts==set(out.contour)
        p=sum(j is not None for j in o.matching)//2;q=len(o.matching)-2*p
        shared.append({'kind':kind,'initial_black':len(B0),'length':len(o.contour),'contacts':p,'ports':q,
                       'crossing_pairs':k.crossing_count(o.matching),'exit_time':o.updates})
    abstract_count=0;nc_levels=[]
    for n in range(1,13):
        allowed=0
        for M in noncrossing_matchings(n):
            if any(j is not None and (j-i)%n in (1,n-1)for i,j in enumerate(M)):continue
            assert k.noninterlaced(M)
            expected=k.noninterlaced_itinerary(M);a=k.run_matching(M)
            assert a.status=='EXIT' and a.itinerary==expected and len(expected)<=n+1
            abstract_count+=1;allowed+=1
        nc_levels.append([n,len(noncrossing_matchings(n)),allowed])
    # Stronger auxiliary two-pass claim is NOT a theorem; record its counterexamples.
    abstract_loop=k.run_matching((2,4,0,None,1))
    assert abstract_loop.status=='ABSTRACT_LOOP'
    adjacent=k.run_matching((1,0,None))
    assert adjacent.status=='EXIT' and len(adjacent.itinerary)==6
    rejected=0
    for thunk in [lambda:k.noninterlaced_itinerary((1,0,None)),
                  lambda:k.noninterlaced_itinerary((2,4,0,None,1)),
                  lambda:k.run_matching((1,None)),lambda:k.frozen_contour(set(),(0,0,4)),
                  lambda:k.sharp_seed(-1)]:
        try:thunk()
        except ValueError:rejected+=1
        else:raise AssertionError('invalid input accepted')
    assert rejected==5 and k.run_matching((None,)*4,cap=0).status=='INCONCLUSIVE'
    lines=[str(len(cpp))]
    for B0,r0 in cpp:
        lines.append(f'{len(B0)} {r0[0]} {r0[1]} {r0[2]} 100000')
        lines.extend(f'{x} {y}'for x,y in sorted(B0))
    with tempfile.TemporaryDirectory(prefix='contour-native-') as directory:
        exe=Path(directory)/'independent'
        subprocess.run(['g++','-std=c++17','-O2',str(HERE/'independent.cpp'),'-o',str(exe)],check=True)
        native=subprocess.run([str(exe)],input='\n'.join(lines)+'\n',text=True,capture_output=True,check=True)
    rows=native.stdout.splitlines();assert len(rows)==len(cpp_expected)
    native_steps=0
    for row,expected in zip(rows,cpp_expected):
        values=list(map(int,row.split()));t,x,y,h,m,digest=values[:6]
        field=frozenset(zip(values[6::2],values[7::2]));assert len(field)==m
        assert (t,(x,y,h),field,digest)==(expected[0],expected[1],expected[2],expected[5])
        native_steps+=t
    return {'schema':'initial-contour-exit-v1','status':'PASS','base_commit':BASE,
      'scope':'exact fixed-contour interface and noninterlaced first-exit theorem; no HC/transience conclusion',
      'exhaustive_4x4_one_pose':exhaustive,'all_python_cases':dict(counts),'complete_trace_sha256':trace.hexdigest(),
      'cpp':{'complete_endpoints_and_trace_digests':len(cpp),'literal_updates':native_steps},
      'noncrossing_no_adjacent_abstract':{'cases':abstract_count,'levels':nc_levels},
      'sharp_family':sharp,'interlaced_physical_counterexample':{
          'black':24,'root':list(root),'length':100,'exit_time':220,'crossing_pairs':k.crossing_count(out.matching),
          'final_pose':list(out.exit_dart),'final_black':len(out.black)},
      'same_frozen_dart_set':shared,'negative_controls':{'invalid_inputs_rejected':rejected,
          'cap_is_inconclusive':True,'abstract_nonphysical_trap':list((2,4,0,None,1)),
          'adjacent_nonphysical_counterexample':{'matching':[1,0,None],'length':3,'time':6},
          'unread_remote_cell_preserved':True},
      'sources_sha256':{name:sha((HERE/name).read_bytes())for name in ['kernel.py','check.py','independent.cpp','witness.json']}}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--generate',action='store_true');args=ap.parse_args()
    actual=run();destination=HERE/'report.json'
    if args.generate:destination.write_text(json.dumps(actual,indent=2,sort_keys=True)+'\n')
    else:
        expected=json.loads(destination.read_text())
        if expected!=actual:raise AssertionError('frozen report mismatch; no file was repaired')
    print(json.dumps({'status':'PASS','python':actual['all_python_cases'],'cpp':actual['cpp'],
                      'abstract_cases':actual['noncrossing_no_adjacent_abstract']['cases']},sort_keys=True))
