"""Reconstruct the complete certificate, verify it independently, compare report.

Default mode NEVER overwrites the frozen report. --generate is explicit.
Only this new theorem-local module is rebuilt, no old project suites.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import random
import subprocess
import tempfile
from pathlib import Path
from core import Catalog, weighted_graph, direct_run, IN, OUT

if not __debug__:
    raise RuntimeError('verification requires Python assertions; do not use -O')

ROOT=Path(__file__).resolve().parent

def digest(data: bytes):return hashlib.sha256(data).hexdigest()
def dump_data(path, c, states, edges, goals):
    with open(path,'w',encoding='ascii') as f:
        f.write('FOUR_ROW_CERT_V1\n')
        for s,p in sorted(c.types):
            f.write(f'{s} {p} {len(c.types[s,p])}\n')
            for row in c.types[s,p]:
                f.write(' '.join('-1 -1' if ans is None else f'{ans[0]} {ans[1]}' for ans in row)+'\n')
        f.write(f'{len(states)} {sum(map(len,edges))} {len(goals)}\n')
        for kind,p,t,seq in states:
            f.write(f'{int(kind=="R")} {p} {t} {len(seq)}'+''.join(f' {i}' for i in seq)+'\n')
        for out in edges:
            f.write(str(len(out))+'\n')
            for e in out:f.write(' '.join(map(str,e))+'\n')
        f.write(' '.join(map(str,goals))+'\n')


def direct_type(c,s,p,columns):
    """Direct full-color behavior tree; no one-column composition used.

    Global x grows left-to-right; columns supplied near-to-far. The residual
    entire bitmap is retained after each same-side return, with memoization.
    """
    from functools import lru_cache
    original=tuple(columns if s==0 else reversed(columns));width=len(original)
    @lru_cache(None)
    def visit(field):
        if not field:return 0
        row=[]
        for channel in range(2):
            t,(x,y,h),out,_=direct_run(field,0 if s==0 else width-1,IN[p][channel],1 if s==0 else 3,cap=10000)
            returned = (x==-1 if s==0 else x==width) and 0<=y<4
            row.append((OUT[p].index(y),visit(tuple(out))) if returned else None)
        key=tuple(row)
        if key not in c.ids[s,p]:raise AssertionError('literal behavior absent from catalog')
        return c.ids[s,p][key]
    return visit(original)


def controls(c,native,witness_path):
    literal_types=0
    # All 1076 catalog representatives have their WHOLE future response tree
    # checked by an independent full-strip color-set simulation.
    for tag,rows in c.types.items():
        s,p=tag
        for i,word in enumerate(c.witness[tag]):
            assert direct_type(c,s,p,word)==i
            literal_types+=1
    # Complete short colored blocks, not just selected representatives.
    short=0
    for width in range(1,4):
        for packed in range(1<<(4*width)):
            word=tuple((packed>>(4*i))&15 for i in range(width))
            for s,p in c.types:
                kind=0
                for j in reversed(range(width)):
                    kind=c.compose(s,(p+j)%2,word[j],kind)
                assert direct_type(c,s,p,word)==kind
                short+=1
    p,l,r,b,y,h=native['column_witness']
    left=c.witness[1,1-p][l];right=c.witness[0,1-p][r]
    columns=tuple(reversed(left))+(b,)+right
    elapsed,pose,field,visits=direct_run(columns,len(left),y,h,cap=34*len(columns)+1)
    assert visits[len(left)]==34
    column_witness={'columns':columns,'pose':[len(left),y,h],'updates':elapsed,'column_updates':34,'final_pose':pose,'final_columns':field}
    p,l,r,side,channel=native['cut_witness']
    left=c.witness[1,p][l];right=c.witness[0,1-p][r]
    columns=tuple(reversed(left))+right;cut=len(left)
    x=cut-1 if side==0 else cut;y=IN[p if side==0 else 1-p][channel];h=3 if side==0 else 1
    # Undo ONE literal update, so the first crossing is part of an actual
    # autonomous run, not a fictitious event preceding the chosen input.
    hx,hy=((0,1),(1,0),(0,-1),(-1,0))[h]
    x,y=x-hx,y-hy
    b=list(columns);after=(b[x]>>y)&1;b[x]^=1<<y
    h=(h-(1 if after else -1))%4
    initial_pose=(x,y,h);initial_columns=tuple(b)
    crossings=0;t=0
    while 0<=x<len(b) and 0<=y<4:
        oldx=x;z=b[x]>>y&1;b[x]^=1<<y;h=(h+(3 if z else 1))%4
        dx,dy=((0,1),(1,0),(0,-1),(-1,0))[h];x+=dx;y+=dy;t+=1
        crossings+= (oldx==cut-1 and x==cut) or (oldx==cut and x==cut-1)
        assert t<=34*len(b)
    assert crossings==21
    cut_witness={'columns':initial_columns,'pose':initial_pose,'cut':cut,'crossings':crossings,'updates':t}
    # Exact maxima extracted from the complete recurrence, independently replayed.
    maxima=[];updates=0
    for line in Path(witness_path).read_text().splitlines():
        a=list(map(int,line.split()));n,x,y,h,want=a[:5];columns=a[5:];assert len(columns)==n
        got,pose,full,visits=direct_run(columns,x,y,h,cap=34*n+1)
        assert got==want and max(visits)<=34
        updates+=got
        maxima.append({'n':n,'time':got,'pose':[x,y,h],'seed_sha256':digest(bytes(columns)),'max_column_updates':max(visits)})
    # Random complete fields at greater widths; these do not establish coverage.
    rng=random.Random(341337);random_updates=0
    for _ in range(160):
        n=rng.randrange(1,321);b=[rng.randrange(16)for _ in range(n)];x=rng.randrange(n);y=rng.randrange(4);h=rng.randrange(4)
        t,pose,out,vis=direct_run(b,x,y,h,cap=34*n+1);assert max(vis)<=34
        random_updates+=t
    exterior_controls=0
    for n in (1,2,4,8,30,100):
        columns=[rng.randrange(16)for _ in range(n)]
        outside={(-1,1),(n,2),(3,4),(-10**60,10**60),(10**60,0)}
        black={(x,y)for x,mask in enumerate(columns)for y in range(4)if mask>>y&1}|outside
        x,y,h=n//2,1,0;expected=direct_run(columns,x,y,h,cap=34*n+1)
        steps=0
        while 0<=x<n and 0<=y<4:
            point=(x,y);turn=-1 if point in black else 1
            black.symmetric_difference_update({point});h=(h+turn)%4
            vx,vy=((0,1),(1,0),(0,-1),(-1,0))[h];x+=vx;y+=vy;steps+=1
        t,pose,final,visits=expected
        assert steps==t and (x,y,h)==pose
        expected_black={(xx,yy)for xx,mask in enumerate(final)for yy in range(4)if mask>>yy&1}|outside
        assert black==expected_black
        exterior_controls+=1
    try:direct_run([0],0,0,0,cap=0)
    except RuntimeError:pass
    else:raise AssertionError('resource cap silently accepted')
    return {'exterior_complete_fields':exterior_controls,'resource_cap_is_unknown':True,'catalog_representatives':literal_types,'complete_short_block_behaviors':short,
            'column_witness':column_witness,'cut_witness':cut_witness,
            'maximizers':maxima,'maximizer_updates':updates,'random_inputs':160,'random_updates':random_updates}


def affine_check(states, edges, goals, path):
    """Second-language integer Bellman proof, no native arithmetic trusted here."""
    values=[0 if k=='F' and t==0 and len(q)<=1 else -10**9 for k,p,t,q in states]
    saved={}
    for width in range(1,24):
        values=[max((w+values[u] for u,w,b,y,h in ee if values[u]>-10**8),default=-10**9) for ee in edges]
        if width>=20:saved[width]=values
    a,b=saved[20],saved[21]
    da=[c-v for c,v in zip(saved[22],a)];db=[d-v for d,v in zip(saved[23],b)]
    rows=list(zip(a,b,da,db))
    actual=[tuple(map(int,line.split()))for line in Path(path).read_text().splitlines()]
    assert rows==actual
    def accepted(rows):
        for i,ee in enumerate(edges):
            ai,bi,di,ei=rows[i];tight0=tight1=False
            for u,w,mask,y,h in ee:
                au,bu,du,eu=rows[u]
                if bi<w+au or ai+di<w+bu or ei<du or di<eu:return False
                tight0 |= bi==w+au and ei==du
                tight1 |= ai+di==w+bu and di==eu
            if not(tight0 and tight1):return False
        return True
    assert accepted(rows)
    damaged=list(rows);ai,bi,di,ei=damaged[0];damaged[0]=(ai-1,bi,di,ei)
    assert not accepted(damaged)
    for g in goals:
        ai,bi,di,ei=rows[g];assert ai<=530 and bi<=564 and di<=68 and ei<=68
    assert any(rows[g][0]==530 and rows[g][2]==68 for g in goals)
    assert any(rows[g][1]==564 and rows[g][3]==68 for g in goals)
    return {'all_24_width_vectors_independently_recomputed':True,
            'inductive_inequalities':4*sum(map(len,edges)),
            'tight_edge_obligations':2*len(states),'damaged_affine_vector_rejected':True}


def run():
    c=Catalog().close();states,edges,goals=weighted_graph(c)
    with tempfile.TemporaryDirectory(prefix='four-row-check-') as directory:
        temp=Path(directory);cert=temp/'certificate.txt';dump_data(cert,c,states,edges,goals)
        exe=temp/'verify'
        subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra',str(ROOT/'verify.cpp'),'-o',str(exe)],check=True,capture_output=True,text=True)
        result=subprocess.run([str(exe),str(cert),str(temp)],capture_output=True,text=True)
        if result.returncode:raise AssertionError(result.stderr or result.stdout)
        native=json.loads((temp/'native.json').read_text())
        report={'schema':'four-row-boundary-v1','status':'passed',
                'scope':'Complete all-width four-row first-exit theorem and exact escape-time function; not HC.',
                'width_type_counts':c.width_counts,'fixed_point_width':c.closed_width,
                'response_max_depth':13,'certificate_sha256':digest(cert.read_bytes()),
                'affine_vectors_sha256':digest((temp/'vectors.txt').read_bytes()),
                'native':native,'controls':controls(c,native,temp/'witnesses.txt'),
                'python_affine_check':affine_check(states,edges,goals,temp/'vectors.txt')}
        # Saved optional files are for the caller's paper/witness check, not input.
        if hasattr(run,'witness_destination'):
            Path(run.witness_destination).write_text((temp/'witnesses.txt').read_text())
        # A damaged response must be rejected, not fixed by the verifier.
        bad=temp/'bad.txt';text=cert.read_text();text=text.replace('-1 -1 -1 -1','0 0 -1 -1',1);bad.write_text(text)
        proc=subprocess.run([str(exe),str(bad),str(temp)],capture_output=True,text=True)
        assert proc.returncode!=0 and 'REJECT' in proc.stderr
        # Missing weighted edges must be rejected. Alter only the stated count.
        bad.write_text(cert.read_text().replace('21248 527764 1078','21248 527763 1078',1))
        proc=subprocess.run([str(exe),str(bad),str(temp)],capture_output=True,text=True)
        assert proc.returncode!=0 and 'REJECT' in proc.stderr
        # Keep the total edge count but falsify one weight. The native checker
        # must reject it from its independently constructed transition relation.
        old=edges[0][0];edges[0][0]=(old[0],old[1]+1,*old[2:])
        dump_data(bad,c,states,edges,goals);edges[0][0]=old
        proc=subprocess.run([str(exe),str(bad),str(temp)],capture_output=True,text=True)
        assert proc.returncode!=0 and 'incorrect recurrence' in proc.stderr
        report['negative_controls']={'corrupted_protocol_rejected':True,
                                    'missing_coverage_edge_count_rejected':True,
                                    'wrong_recurrence_weight_rejected':True}
    report['sources_sha256']={name:digest((ROOT/name).read_bytes())for name in ('core.py','verify.cpp','check.py')}
    return json.loads(json.dumps(report))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--generate',action='store_true');parser.add_argument('--witnesses');a=parser.parse_args()
    if a.witnesses:run.witness_destination=a.witnesses
    result=run();path=ROOT/'report.json'
    if a.generate:path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    else:
        frozen=json.loads(path.read_text())
        if result!=frozen:raise AssertionError('frozen certificate report mismatch; no regeneration')
    print(json.dumps({'status':'passed','exact_formula':'34*n-150 for all n>=13','column_bound':34,'weighted_states':21248,'weighted_edges':527764}))
