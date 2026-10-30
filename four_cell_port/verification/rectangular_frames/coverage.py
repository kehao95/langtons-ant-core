"""Check the exact, disjoint parameter cover and sharp entrance bound.

This checks the correspondence between hypotheses, immutable certificates and
replayed acceptance reports. It does not replace the all-parameter verifier.
"""
from __future__ import annotations
import hashlib,json
from pathlib import Path
from exact_sets import Context
from verify import parse,trace
HERE=Path(__file__).resolve().parent

def jobs():
    return ([(HERE/f'corner_{p}{q}.json',HERE/f'corner_{p}{q}.report.json',True) for p in range(2) for q in range(2)]
      +[(HERE/'thin'/f'thin_{axis}{fixed}_{p}_rebuilt.json',HERE/'reports'/f'thin_{axis}{fixed}_{p}_rebuilt.json',False)
        for axis in ('n','m') for fixed in range(1,10) for p in range(2)]
      +[(HERE/f'center_{p}.json',HERE/f'center_{p}.report.json',False) for p in range(2)])

def audit():
    ctx=Context();seen=set();corner=[];thin=[];centre=[];read_checks=geometry_checks=blocks=0
    for path,rpath,guard in jobs():
        c=json.loads(path.read_text());r=json.loads(rpath.read_text());names=c['parameters']
        assert c['name'] not in seen;seen.add(c['name'])
        assert r['accepted'] and r['name']==c['name'] and r['deep_interior_never_read']==guard
        sha=hashlib.sha256(json.dumps(c,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        assert sha==r['certificate_sha256']
        assert names==(['a','b'] if guard else ['a'])
        hdr='['+','.join(names)+'] -> '
        domain=ctx.set(hdr+'{ : '+c['domain']+' }')
        target=ctx.set(hdr+'{ : '+' and '.join(n+'>=0' for n in names)+' }')
        assert domain.equal(target),'Domain does not cover the full claimed orthant'
        rect=[parse(x,names) for x in c['rect']];head=[parse(x,names) for x in c['head'][:2]]
        assert c['head'][2]==0 and all(x==parse(0,names) for x in head)
        length=parse(0,names);h=0;px=py=parse(0,names)
        for b in c['blocks']:
            count=parse(b['repeat'],names);ph,d,end=trace(b['word'],h)
            if count!=parse(1,names):assert end==h and d!=(0,0)
            px+=count*d[0];py+=count*d[1];h=end;length+=count*len(b['word'])
        assert length==parse(r['tail_boundary'],names)
        assert [px,py]==[parse(x,names) for x in r['tail_pose'][:2]] and h==r['tail_pose'][2]
        assert trace(c['tail'],h)[1]==tuple(r['drift'])
        last=c['blocks'][-1];assert parse(last['repeat'],names)==parse(1,names)
        suffix=0
        for ch in last['word'][::-1]:
            if ch!=c['tail'][(-suffix-1)%104]:break
            suffix+=1
        assert suffix<len(last['word']) and suffix==r['matching_suffix']
        t=length-suffix;assert t==parse(r['first_entrance'],names)
        read_checks+=r['read_checks'];geometry_checks+=r['geometry_checks'];blocks+=r['blocks']
        name=path.stem
        if name.startswith('corner'):
            p,q=map(int,name[-2:]);n=parse(f'{10+p}+2*a',names);m=parse(f'{10+q}+2*b',names)
            expected=[parse(0,names),n-1,parse(0,names),m-1];assert rect==expected
            formula=([78,44,555] if p==q==0 else [30,44,438] if p==0 else [38,62,1538] if q==0 else [28,28,287])
            assert t==n*formula[0]+m*formula[1]+formula[2]
            assert tuple(r['drift'])==(2*(-1)**p,2*(-1)**q)
            residual=t-(n+m)*242
            assert all(x<=0 for x in residual.c[1:]) and residual.c[0]<=29325
            corner.append({'n_parity':p,'m_parity':q,'time_coefficients':formula,'read_checks':r['read_checks']})
        elif name.startswith('thin'):
            axis=name[5];fixed=int(name[6]);p=int(name[8]);ell=parse(f'{200+p}+2*a',names)
            n=parse(fixed,names) if axis=='n' else ell;m=ell if axis=='n' else parse(fixed,names)
            assert rect==[parse(0,names),n-1,parse(0,names),m-1]
            assert t.c[1]%2==0
            alpha=t.c[1]//2;beta=t.c[0]-alpha*(200+p)
            residual=t-(n+m)*242
            assert residual.c[1]<=0 and residual.c[0]<=29325
            thin.append({'fixed_axis':axis,'fixed':fixed,'variable_parity':p,'slope':alpha,'intercept':beta,
                         'residual_max':residual.c[0],'read_checks':r['read_checks'],'blocks':r['blocks']})
        else:
            p=int(name[-1]);rad=parse(f'{32 if p==0 else 43}+2*a',names)
            assert rect==[-rad,rad,-rad,rad]
            formula=[248,9475] if p==0 else [820,24110]
            assert t==rad*formula[0]+formula[1]
            centre.append({'radius_parity':p,'radius_min':32 if p==0 else 43,'time_coefficients':formula,
                           'read_checks':r['read_checks'],'blocks':r['blocks']})
    data=json.loads((HERE/'finite_report.json').read_text());rows=data['rows']
    finite={(z['n'],z['m']):z for z in rows if z['kind']=='corner'}
    expected={(n,m) for n in range(1,200) for m in range(1,200) if min(n,m)<=9}
    assert set(finite)==expected and len(finite)==3501
    central={(z['n']-1)//2:z for z in rows if z['kind']=='center'}
    expected_c={r for r in range(43) if not(r%2==0 and r>=32)}
    assert set(central)==expected_c and len(central)==37
    assert all(z['n']==z['m']==2*r+1 and z['head']==[r,r,0] for r,z in central.items())
    assert len(rows)==len(finite)+len(central)==data['cases']
    maximal=max(z['first']-242*(n+m) for (n,m),z in finite.items())
    assert maximal==29325 and finite[30,4]['first']==37553
    sharp=[z for z in thin if (z['fixed_axis'],z['fixed'],z['variable_parity'])==('m',5,1)][0]
    assert (sharp['slope'],sharp['intercept'])==(242,8703)
    return {'schema':'rectangular-cover-v1','accepted':True,'universal_schemas':42,'corner_schemas':4,
            'thin_schemas':36,'center_schemas':2,'read_checks':read_checks,'frame_geometry_checks':geometry_checks,
            'blocks':blocks,'finite_rectangles':3501,'finite_center_squares':37,
            'finite_updates_per_implementation':data['literal_updates_per_implementation'],
            'sharp_slope':242,'sharp_intercept':29325,'intercept_witness':{'n':30,'m':4,'first':37553},
            'corner':corner,'thin':thin,'center':centre}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--write',type=Path);a=p.parse_args();r=audit()
    if a.write:a.write.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    else:assert r==json.loads((HERE/'coverage_report.json').read_text())
    print(json.dumps({k:v for k,v in r.items() if k not in ('corner','thin','center')},sort_keys=True))
