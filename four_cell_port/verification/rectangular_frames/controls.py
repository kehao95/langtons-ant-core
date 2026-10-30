"""Independent scope controls and adverse-certificate tests; no discovery oracle."""
from __future__ import annotations
import argparse,copy,hashlib,json,random
from pathlib import Path
from literal import rectangle,vector_replay,permanent,chronological_permanent,STANDARD
from verify import Checker,parse,trace
HERE=Path(__file__).resolve().parent

def affine_trace(cert,values):
    names=cert['parameters'];words=[]
    for block in cert['blocks']:
        n=parse(block['repeat'],names).evaluate(values)
        if n<0:raise ValueError('Negative count')
        words.append(block['word']*n)
    return ''.join(words)

def frame_time(n,m):
    if n%2==0 and m%2==0:return 78*n+44*m+555
    if n%2==0:return 30*n+44*m+438
    if m%2==0:return 38*n+62*m+1538
    return 28*n+28*m+287

def replay():
    # Reproduce the blank reference with its full 715-cell history, then certify it.
    w,B,p,_=vector_replay(set(),(0,0,0),9977)
    tail,_,_,_=vector_replay(B,p,104)
    assert tail in STANDARD*2
    assert permanent(B,p,tail) and chronological_permanent(B,p,tail)
    blank={'time':9977,'mass':len(B),'pose':p,'tail':tail}
    # Check each parametric word on one finite complete source, retaining every cell.
    files=sorted(HERE.glob('corner_??.json'))+sorted((HERE/'thin').glob('*.json'))+sorted(HERE.glob('center_?.json'))
    schema_steps=0;schema_rows=[]
    for path in files:
        c=json.loads(path.read_text());values=(0,)*len(c['parameters']);names=c['parameters']
        x0,x1,y0,y1=[parse(x,names).evaluate(values) for x in c['rect']]
        source={(x,y) for x in range(x0,x1+1) for y in range(y0,y1+1)}
        pose=(*(parse(x,names).evaluate(values) for x in c['head'][:2]),c['head'][2])
        proposed=affine_trace(c,values)
        actual,end,p,foot=vector_replay(source,pose,len(proposed))
        assert actual==proposed,(path.name,'word')
        assert permanent(end,p,c['tail']) and chronological_permanent(end,p,c['tail']),path.name
        schema_steps+=len(actual)
        schema_rows.append({'name':c['name'],'steps':len(actual),'endpoint_mass':len(end),
                            'endpoint_sha256':hashlib.sha256(json.dumps(sorted(end),separators=(',',':')).encode()).hexdigest()})
    # Arbitrary interiors: every assignment in three representative small frames,
    # then deterministic random interiors in larger representatives of all parities.
    frame_cases=frame_steps=0;checksum=hashlib.sha256();three=None;last_endpoint=None
    rng=random.Random(20261030)
    dimensions=[(10,10),(10,11),(11,10),(11,11),(16,18),(16,19),(17,18),(17,19)]
    for n,m in dimensions:
        solid=rectangle(n,m);interior=sorted((x,y) for x in range(4,n-4) for y in range(4,m-4))
        tau=frame_time(n,m);baseword,baseB,basepose,reads=vector_replay(solid,(0,0,0),tau)
        tail,_,_,tailreads=vector_replay(baseB,basepose,104)
        assert tail in STANDARD*2 and permanent(baseB,basepose,tail)
        assert not (set(interior)&(reads|tailreads))
        patterns=range(1<<len(interior)) if len(interior)<=9 else [rng.getrandbits(len(interior)) for _ in range(20)]
        for bits in patterns:
            absent={q for i,q in enumerate(interior) if not ((bits>>i)&1)}
            word,out,pose,foot=vector_replay(solid-absent,(0,0,0),tau)
            assert word==baseword and pose==basepose and out==(baseB^absent)
            assert chronological_permanent(out,pose,tail)
            frame_cases+=1;frame_steps+=tau
            checksum.update(json.dumps([n,m,bits,sorted(out)],separators=(',',':')).encode())
        if three is None:
            x=y=h=0;seen=set()
            from literal import DIR
            for t,ch in enumerate(baseword):
                q=x,y
                if min(x,y,n-1-x,m-1-y)>=3 and q not in seen:
                    # Removing this initial black cell changes precisely its first read.
                    v,_,_,_=vector_replay(solid-{q},(0,0,0),t+1)
                    assert v[:t]==baseword[:t] and v[t]!=baseword[t]
                    three={'n':n,'m':m,'removed_cell':q,'first_difference':t,
                           'reference_letter':baseword[t],'modified_letter':v[t]}
                    break
                seen.add(q);h=(h+(1 if ch=='R' else -1))%4;dx,dy=DIR[h];x+=dx;y+=dy
        last_endpoint=baseB,basepose,tail
    assert three is not None
    # Exact huge-coordinate scope controls; these are arithmetic, not huge simulations.
    B,p,u=last_endpoint;ph,d,h=trace(u,p[2]);q0=p[:2];N=10**60
    blocker=(q0[0]+N*d[0],q0[1]+N*d[1])
    assert blocker not in B
    assert not permanent(B|{blocker},p,u)
    assert not chronological_permanent(B|{blocker},p,u)
    inert=(10**70,0)
    while not chronological_permanent(B|{inert},p,u):inert=(inert[0],inert[1]+1)
    assert permanent(B|{inert},p,u)
    shifted=(10**80,-10**80);translated={(x+shifted[0],y+shifted[1]) for x,y in B}
    assert permanent(translated,(p[0]+shifted[0],p[1]+shifted[1],p[2]),u)
    assert chronological_permanent(translated,(p[0]+shifted[0],p[1]+shifted[1],p[2]),u)
    # Certificate mutations: acceptance code must reject, not repair them.
    base=json.loads((HERE/'corner_00.json').read_text());mutations=[]
    c=copy.deepcopy(base);c['blocks'][0]['word']='R'+c['blocks'][0]['word'][1:];mutations.append(('first_colour',c))
    c=copy.deepcopy(base);c['tail']='L' if c['tail'][0]=='R' else 'R';mutations.append(('tail_length',c))
    c=copy.deepcopy(base);c['rect'][0]='1';mutations.append(('source_boundary',c))
    c=copy.deepcopy(base);c['blocks'][0]={'word':'RLLR','repeat':'-1'};mutations.append(('negative_exponent',c))
    c=copy.deepcopy(base);c['blocks'][0]={'word':'RRRR','repeat':'a+1'};mutations.append(('zero_drift',c))
    c=copy.deepcopy(base);c['blocks'][0]['repeat']='a*a';mutations.append(('nonlinear_exponent',c))
    rejected=[]
    for name,c in mutations:
        try:Checker(c,True).run()
        except (ValueError,TypeError,ArithmeticError):rejected.append(name)
        else:raise AssertionError('Accepted corrupted certificate: '+name)
    result={'schema':'rectangular-scope-controls-v1','blank_reference':blank,'finite_schema_controls':len(schema_rows),
            'schema_literal_updates':schema_steps,'schema_rows':schema_rows,'frame_complete_field_comparisons':frame_cases,
            'frame_literal_updates':frame_steps,'frame_outputs_sha256':checksum.hexdigest(),
            'three_layer_trace_counterexample':three,'remote_blocker_epoch':str(N),
            'inert_marker':inert,'translation':shifted,'rejected_mutations':rejected}
    return json.loads(json.dumps(result))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',type=Path);a=p.parse_args();r=replay()
    if a.write:a.write.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    else:
        assert r==json.loads((HERE/'controls_report.json').read_text()),'Frozen report mismatch'
    print(json.dumps({k:v for k,v in r.items() if k!='schema_rows'},sort_keys=True))
