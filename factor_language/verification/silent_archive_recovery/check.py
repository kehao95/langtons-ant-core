#!/usr/bin/env python3
"""Theorem-local affine proof checks and independent complete-state controls.

Default checks do not regenerate or overwrite the declarative grammar.
--write creates a report; --compare verifies a frozen report byte for byte.
"""
from __future__ import annotations
import argparse
import base64
import copy
import hashlib
import json
import random
from pathlib import Path
import subprocess
import tempfile
import zlib
from engine import need,verify_regime,blocks_for,at,trace,D,first_read
HERE=Path(__file__).resolve().parent
STANDARD=('RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRL'
          'LRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR')


def digest(b):return hashlib.sha256(b).hexdigest()


def load():
    packed=(HERE/'grammar.json.zlib').read_bytes()
    manifest=json.loads((HERE/'grammar-manifest.json').read_text())
    need(digest(packed)==manifest['compressed_sha256'],'compressed grammar identity')
    raw=zlib.decompress(packed)
    need(len(raw)==manifest['bytes'] and digest(raw)==manifest['sha256'],'decoded grammar identity')
    c=json.loads(raw);need(c['schema']=='silent-archive-recovery-v1','wrong schema')
    need(c['standard']==STANDARD and c['pose']==[-1,0,3],'changed classical convention/word')
    inherited={k:c[k] for k in ('source','pose','standard','past9','producer_blocks')}
    need(digest(json.dumps(inherited,sort_keys=True,separators=(',',':')).encode())==manifest['inherited_subset_sha256'],'changed inherited exact input')
    return c


def unpack_exception(e):
    raw=zlib.decompress(base64.b64decode(e['word_zlib_b64'],validate=True))
    need(len(raw)==e['post_consumer_updates'] and digest(raw)==e['word_sha256'],'finite word identity')
    w=raw.decode('ascii');need(set(w)<={'R','L'},'invalid finite letters');return w


def source(c,n):
    f=c['source']
    return ({tuple(q) for q in f['low']}|{(x,y+4*j) for x,y in f['bulk'] for j in range(n)}
            |{(x,y+4*n) for x,y in f['high']})


def literal_program(c,n):
    name='even' if n%2==0 else 'odd'
    r=next(r for r in c['regimes'] if r['name']==name)
    if n>=r['n_offset']:
        k=(n-r['n_offset'])//2
        return [(b['word'],at(b['count'],k)) for b in blocks_for(c,r)],r['tail']
    e=next(e for e in c['exceptions'] if e['n']==n)
    bs=[(b['word'],at(b['count'],n)) for b in c['producer_blocks']]
    return bs+[(unpack_exception(e),1)],e['tail']


def py_past(b,p,d):
    b=set(b);s=''
    for _ in range(9):
        p=(p[0]-d[0],p[1]-d[1]);b.symmetric_difference_update((p,));old=p in b
        s+='L' if old else 'R';d=(d[1],-d[0]) if old else (-d[1],d[0])
    return s[::-1]


def finite_tail(b,p,d,w):
    need(len(w)==104 and w in STANDARD*2,'tail is not a standard phase')
    # Vector geometry; explicit black/ray hits plus earlier-visit thresholds.
    q=[];v=p;vdir=d
    for ch in w:
        q.append(v);vdir=(vdir[1],-vdir[0]) if ch=='R' else (-vdir[1],vdir[0]);v=(v[0]+vdir[0],v[1]+vdir[1])
    drift=(v[0]-p[0],v[1]-p[1]);need(vdir==d and abs(drift[0])==abs(drift[1])==2,'bad finite tail geometry')
    def mult(v):
        if v[0]%drift[0]:return None
        k=v[0]//drift[0]
        return k if v[1]==k*drift[1] else None
    checks=0
    for i,pt in enumerate(q):
        prev=[];es={0}
        for j,pt2 in enumerate(q):
            z=mult((pt2[0]-pt[0],pt2[1]-pt[1]))
            if z is not None and (z>0 or z==0 and j<i):prev.append(z);es.add(z)
        for cell in b:
            k=mult((cell[0]-pt[0],cell[1]-pt[1]))
            if k is not None and k>=0:es.update((k,k+1))
        es.add(max(es)+1)
        for k in es:
            bit=((pt[0]+k*drift[0],pt[1]+k*drift[1]) in b)^(sum(z<=k for z in prev)%2)
            need(bit==(w[i]=='L'),'finite all-future tail rejected');checks+=1
    return checks


def literal(c,n):
    bs,tail=literal_program(c,n);b=source(c,n);p=(-1,0);d=(-1,0);past=py_past(b,p,d)
    need(past==c['past9'],'initial inverse past');legal={(STANDARD*2)[i:i+10] for i in range(104)}
    t=events=0;last=first=-1;previous=''
    for word,count in bs:
        for _ in range(count):
            for expected in word:
                old=p in b;ch='L' if old else 'R';need(ch==expected,'literal requested word mismatch')
                v=past+ch
                if v not in legal:
                    events+=1;last=t
                    if first<0:first=t
                past=v[1:];b.symmetric_difference_update((p,))
                d=(-d[1],d[0]) if old else (d[1],-d[0]);p=(p[0]+d[0],p[1]+d[1]);t+=1;previous=ch
    need(previous!=tail[-1],'entry not first');checks=finite_tail(b,p,d,tail)
    endpoint=set(b);ep=p;eh=D.index(d);et=t
    for ch in tail[:9]:
        need((p in b)==(ch=='L'),'tail boundary simulation');v=past+ch
        if v not in legal:events+=1;last=t
        past=v[1:];b.symmetric_difference_update((p,));d=(d[1],-d[0]) if ch=='R' else (-d[1],d[0]);p=(p[0]+d[0],p[1]+d[1]);t+=1
    need(first==56*n+168,'first event inherited control')
    row=[n,et,events,last,len(endpoint),ep[0],ep[1],eh,first]
    return row,sorted(endpoint),checks


def native(c,cases):
    lines=[str(len(cases))]
    for n in cases:
        b=sorted(source(c,n));bs,tail=literal_program(c,n)
        lines.append(f'{n} {len(b)}');lines.extend(f'{x} {y}' for x,y in b)
        lines.append(f'-1 0 3 {len(bs)}');lines.extend(f'{w} {cnt}' for w,cnt in bs);lines.append(tail)
    with tempfile.TemporaryDirectory(prefix='ant-recovery-native-') as tmp:
        exe=Path(tmp)/'independent'
        subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror',str(HERE/'independent.cpp'),'-o',str(exe)],capture_output=True,text=True,check=True,timeout=30)
        run=subprocess.run([str(exe)],input='\n'.join(lines)+'\n',capture_output=True,text=True,check=True,timeout=45)
    it=iter(run.stdout.splitlines());out=[]
    for _ in cases:
        row=list(map(int,next(it).split()));need(len(row)==9,'native header')
        pts=[tuple(map(int,next(it).split())) for _ in range(row[4])]
        out.append((row,pts))
    need(next(it,None) is None,'extra native results')
    return out


def negative_controls(c):
    trials={
        'wrong_constant_recovery_turn':lambda r:r['blocks'][0].__setitem__('word',('L' if r['blocks'][0]['word'][0]=='R' else 'R')+r['blocks'][0]['word'][1:]),
        'shortened_parameter_scan':lambda r:r['blocks'][1]['count'].__setitem__(1,r['blocks'][1]['count'][1]-1),
        'wrong_tail_phase':lambda r:r.__setitem__('tail',r['tail'][1:]+r['tail'][0]),
    }
    rejected=[]
    for name,change in trials.items():
        r=copy.deepcopy(c['regimes'][0]);change(r)
        try:verify_regime(c,r)
        except (ValueError,IndexError):rejected.append(name)
        else:raise ValueError('damaged recovery accepted: '+name)
    d=copy.deepcopy(c);d['source']['bulk'].pop()
    try:verify_regime(d,d['regimes'][0])
    except (ValueError,IndexError):rejected.append('missing_source_bulk_cell')
    else:raise ValueError('damaged source accepted')
    # Far future input differences are tested against the COMPLETE field criterion.
    n=10;row,pts,_=literal(c,n);b=set(pts);_,tail=literal_program(c,n);p=(row[5],row[6]);d=D[row[7]]
    _,dx,dy,_=trace(tail,row[7]);q=(p[0]+10**60*dx,p[1]+10**60*dy)
    need(q not in b,'remote control overlaps');bad=b|{q}
    try:finite_tail(bad,p,d,tail)
    except ValueError:rejected.append('blocker_at_10_to_60_tail_epochs')
    else:raise ValueError('far blocker accepted')
    off=(10**60,0);need(off not in b,'off-trace overlap');finite_tail(b|{off},p,d,tail)
    return rejected



def query_controls(c):
    rng=random.Random(1042026);checks=0
    for n in (10,12,17,19,64,65):
        name='even' if n%2==0 else 'odd';reg=next(r for r in c['regimes'] if r['name']==name)
        k=(n-reg['n_offset'])//2;bs,tail=literal_program(c,n);first={};p=(-1,0);h=3;t=0
        for w,count in bs+[(tail,3)]:
            for _ in range(count):
                for ch in w:
                    first.setdefault(p,t);h=(h+(1 if ch=='R' else -1))%4;dx,dy=D[h];p=(p[0]+dx,p[1]+dy);t+=1
        for q in rng.sample(sorted(first),100):
            need(first_read(c,reg,k,q)==first[q],'first-contact query differs from complete finite trace');checks+=1
    reg=c['regimes'][0];n=10**60;k=(n-reg['n_offset'])//2
    endpoint=(-10,-3);epoch=10**60;point=(endpoint[0]-2*epoch,endpoint[1]-2*epoch)
    answer=first_read(c,reg,k,point)
    need(answer is not None and answer>=550*n+6714,'remote first-contact did not reach tail')
    need(first_read(c,reg,k,(10**60,0)) is None,'off-trace query accepted')
    return {'finite_exact_queries':checks,'large_parameter':n,'remote_query':list(point),'remote_first_read':answer,
            'off_trace_query_absent':True,'large_control_is':'finite integer/affine evaluation, not numerical-time simulation'}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--compare',type=Path);ap.add_argument('--write',type=Path);args=ap.parse_args()
    c=load();analyses={r['name']:verify_regime(c,r) for r in c['regimes']}
    need({e['n'] for e in c['exceptions']}=={1,2,3,4,5,6,7,8,9,11,13,15},'incomplete parameter coverage')
    cases=list(range(1,81))+[127,128,255,256,511,512,1000,1001]
    py=[literal(c,n) for n in cases];cpp=native(c,cases)
    need([(r,pts) for r,pts,_ in py]==cpp,'independent COMPLETE endpoint mismatch')
    for row,_,_ in py:
        n=row[0];name='even' if n%2==0 else 'odd';n0=10 if name=='even' else 17
        if n>=n0:
            a=analyses[name];k=(n-n0)//2
            need(row[1]==at(a['entry']['time'],k),'entry affine control')
            need(row[2]==at(a['all_future_J10_k'],k),'event affine control')
            need(row[3]==row[1]+a['last_J10_minus_entry'],'last event control')
            need(row[4]==at(a['entry_mass_k'],k),'mass affine control')
    rejected=negative_controls(c);queries=query_controls(c)
    report={'schema':'silent-archive-recovery-report-v1','regimes':analyses,
            'finite_exceptions':[row for row,_,_ in py if row[0] in {e['n'] for e in c['exceptions']}],
            'controls':{'parameters':cases,'cases':len(cases),'updates_per_simulator':sum(r[1]+9 for r,_,_ in py),
                        'complete_terminal_fields_compared':len(cases),'python_tail_parity_checks':sum(v for _,_,v in py),
                        'rows':[r for r,_,_ in py],'complete_endpoints_sha256':digest(json.dumps(cpp,separators=(',',':')).encode())},
            'first_contact_controls':queries,'damaged_controls_rejected':rejected,'off_trace_control':'retained and certified harmless',
            'source_sha256':{s:digest((HERE/s).read_bytes()) for s in ['engine.py','check.py','independent.cpp','grammar.json.zlib','grammar-manifest.json']},
            'not_established':['HC','finite HC counterexample','arbitrary perturbed ribbon convergence','global J10 budget','Lean formalization','external peer review','priority']}
    text=json.dumps(report,indent=2)+'\n'
    if args.compare:need(text==args.compare.read_text(),'frozen report mismatch')
    if args.write:args.write.write_text(text)
    print(text,end='')

if __name__=='__main__':main()
