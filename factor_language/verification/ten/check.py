from __future__ import annotations
import argparse, hashlib, json, random
from collections import Counter
from pathlib import Path
import kernel as k
r = k.r
ROOT = Path(__file__).resolve().parent

def main(cert: Path):
    wit = k.load_witness(cert)
    assert wit['W'] == r.W and wit['U'] == r.U
    words = (cert/'windows10.txt').read_text().splitlines()
    assert len(words)==len(set(words)) and all(len(w)==150 for w in words)
    computed, generation = k.enumerate_words(10,150)
    assert words == computed, 'incomplete or incorrect immutable edge set'
    graph = k.verify_graph(words, cert, wit)
    supply = k.supply_check(wit['T'])
    # All three proposed eventual periodic modes are physically realizable on
    # the stated finite/infinite fields; only W has no infinite black ray.
    recipes = {}
    for key in ('W','U','A','T'):
        word=wit[key];rec=r.periodic_recipe(word)
        assert r.verify_periodic_field(word,set(map(tuple,rec['points'])),list(map(tuple,rec['ray_starts'])))
        assert r.factors(word,10) <= r.factors(r.W,10)
        recipes[key]={'period':len(word),'drift':rec['drift'],'black_rays':len(rec['ray_starts'])}
    assert recipes['W']['black_rays']==0 and recipes['U']['black_rays']==5 and recipes['T']['black_rays']==2
    A,B,C,T,Z=(wit[x]for x in ('A','B','C','T','Z'))
    assert r.geometry(A)[1::2]==((0,-4),0) and r.geometry(B)[1::2]==((1,11),2)
    assert B[-27:]==A[1:] and A in r.factors(wit['U'],28)
    # Finite coordinate facts used in the ALL-parameter written obstruction.
    aq=r.geometry(A)[0];bq=r.geometry(B)[0]
    assert [(i,y,A[i]) for i,(x,y) in enumerate(aq) if x==0]==[(0,0,'L'),(7,-1,'R'),(8,-2,'R'),(15,-3,'L'),(16,-2,'L'),(27,-5,'L')]
    assert max(y for x,y in bq if x==1)==12
    assert [(i,B[i])for i,p in enumerate(bq)if p==(1,9)]==[(82,'R'),(90,'L')]
    assert min(x for x,y in aq)==-3 and max(x for x,y in aq)==0
    assert [(i,A[i])for i,p in enumerate(aq)if p==(0,-2)]==[(8,'R'),(16,'L')]
    assert [(i,B[i])for i,p in enumerate(bq)if p==(0,2)]==[(32,'R')]
    assert max(y for x,y in bq if x==0)==2
    assert [(i,B[i])for i,p in enumerate(bq)if p==(1,4)]==[(45,'L'),(53,'R')]
    assert [(i,B[i])for i,p in enumerate(bq)if p==(1,8)]==[(73,'L'),(81,'R')]
    cases=[(n,m)for n in range(35)for m in range(35)]
    cases += [(10**12,0),(10**12,10**12-1),(10**12,10**12),(10**12,10**12+1),(1,10**12),(0,10**12)]
    for n,m in cases:
        p,a,b=k.obstruction_witness(n,m)
        visits=k.parametric_visits(A,B,n,m,p)
        ia=visits.index((a,'R'));assert visits[ia+1]==(b,'R')
        if n<8 and m<8:
            w=B+A*n+B+A*m+B
            assert r.collision(w) is not None
    # Family macro: local read support is independent of n, and algebraic
    # cancellation of the two finite rails gives the exact full-field identity.
    tq,td,_,th=r.geometry(T);assert td==(0,-2) and th==0
    assert min(y for x,y in tq)==-3 and max(y for x,y in tq)==0
    first=r.first_read_seed(T)
    assert first=={(-2,-1),(-1,0),(-2,-2),(0,-3)}
    R=set(map(tuple,wit['sharp_family']['residue']))
    assert all(y in (-1,0) for x,y in R)
    E=set(map(tuple,wit['sharp_family']['E']))
    toggles={q for q,v in Counter(tq).items() if v%2}
    assert (E|{(-2,-2),(0,-3)}) ^ toggles == {(x,y-2)for x,y in E}|R
    for key in ('W','U','T'):
        w=wit[key]
        assert min(j for j in range(1,len(w)+1) if len(w)%j==0 and w[:j]*(len(w)//j)==w)==len(w)
    for n in (1,2,3,4,7,11,25,100):
        field=k.family(n,wit);p=(0,0);h=0
        for c in T:
            p,h,a=r.step_cells(field,p,h);assert a==c
        target={(x,y-2)for x,y in k.family(n-1,wit)}
        assert field==target|R and not target&R and p==(0,-2)and h==0
    zrec=r.periodic_recipe(Z)
    assert not zrec['ray_starts'] and set(map(tuple,zrec['points']))==k.family(0,wit)
    assert r.verify_periodic_field(Z,k.family(0,wit),[])
    zq,zd,_,zh=r.geometry(Z);assert max(y for x,y in zq)==0 and zd==(-2,-2)and zh==0
    assert r.collision(T*2+Z*2) is None
    allowed=r.factors(r.W,10);word=T*2+Z*2
    assert all(word[i:i+10] in allowed for i in range(len(word)-9))
    assert T[-3:]==Z[-3:] and T[-4:]!=Z[-4:]
    for n in range(1,9):
        field=k.family(n,wit);assert len(field)==2*n+13;p=(0,0);h=0
        wanted=T*n+Z*3
        for c in wanted:
            p,h,a=r.step_cells(field,p,h);assert a==c
    # Spiral: universal proof uses exactly these support inequalities and the
    # explicit four-phase rectangle formulas, not a finite number of turns.
    U=wit['U'];uq,ud,_,uh=r.geometry(U);cq,cd,_,ch=r.geometry(C)
    assert (ud,uh,cd,ch)==((0,-4),0,(13,-4),3)
    assert (min(x for x,y in uq),max(x for x,y in uq),min(y for x,y in uq),max(y for x,y in uq))==(0,3,-5,0)
    assert (min(x for x,y in cq),max(x for x,y in cq),min(y for x,y in cq),max(y for x,y in cq))==(0,14,-4,0)
    assert r.collision(U+C+U) is None
    local=U*2+C+U*2;allowed9=r.factors(r.W,9)
    assert all(local[i:i+9] in allowed9 for i in range(len(local)-8))
    bad=wit['spiral']['missing10'];hits=[i for i in range(len(local)-9)if local[i:i+10]==bad]
    assert hits==[2*28+11] and bad not in allowed
    # Exact rational-free inequalities used to separate every future shell.
    assert all(15*S>14 and 30*S>14 and 60*S>14 for S in (1,16,16**100))
    assert all(15*S>28 for S in (16,16**100))
    spiral=''.join(U*(5*2**i)+C for i in range(9))
    assert r.collision(spiral) is None
    assert all(spiral[i:i+9] in allowed9 for i in range(len(spiral)-8))
    # Reproduce canonical W directly, not by trusting the certificate title.
    field=set();p=(0,0);h=0;measured=''
    for t in range(12104):
        p,h,c=r.step_cells(field,p,h)
        if t>=12000:measured+=c
    assert measured==r.W
    return {'status':'passed','graph':graph,'supply':supply,'periodic_modes':recipes,
            'parametric_fold_controls':len(cases),'sharp_family_all_parameter_identity':'proved in PROOF.md; local equation and 8 finite controls checked',
            'spiral_literal_control_steps':len(spiral),'all_parameter_claims_are_analytic':True,
            'HC_proved':False,'finite_HC_counterexample':False,'external_review':False,
            'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'kernel.py',ROOT/'check.py',ROOT/'baseline/rigidity.py']}}

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Do not disable verification assertions with -O.')
    p=argparse.ArgumentParser();p.add_argument('--cert-dir',type=Path,default=ROOT/'certificates');a=p.parse_args()
    print(json.dumps(main(a.cert_dir),indent=2))
