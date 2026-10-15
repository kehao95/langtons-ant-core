"""Theorem-local exact checks. No -O, no historical suite, no global HC claim."""
from __future__ import annotations
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json, random, sys
import wake

if sys.flags.optimize:
    raise SystemExit('Run without Python -O')
HERE=Path(__file__).resolve().parent
rng=random.Random(20261015)
counts=Counter()
CANON={(0,-6),(-1,-5),(0,-5),(-2,-4),(0,-4),(-2,-3),(1,-3),(-1,-2),(1,-2),(-1,-1),(-2,0),(-1,0),(0,0)}


def step(B,p,h):
    # Independent vector rotation, not heading modular addition.
    dx,dy=wake.MOVES[h]
    if p in B:
        B.remove(p); dx,dy=-dy,dx; c='L'
    else:
        B.add(p); dx,dy=dy,-dx; c='R'
    return (p[0]+dx,p[1]+dy),wake.MOVES.index((dx,dy)),c


def gam(a,b,h):
    return (2/(b+1),2/(a+1),-2*b/(b+1),-2*a/(a+1))[h]


def potential(B,p,h,a,b,inv=False):
    sig=wake.chi(p)*(1 if h%2==0 else -1)
    if inv:
        field=sum(wake.chi(q)*a**(-q[0])*b**(-q[1]) for q in B)
        return -sig*field+gam(a,b,(h+2)%4)*a**(-p[0])*b**(-p[1])
    field=sum(wake.chi(q)*a**q[0]*b**q[1] for q in B)
    return -sig*field+gam(a,b,h)*a**p[0]*b**p[1]


def increment(p,h,c,a,b,inv=False):
    k=1-2/(a+1)-2/(b+1)
    if inv:
        p=(-p[0],-p[1]);h=(h+2)%4
    extra=(h==2 and c=='L') or (h==3 and c=='R')
    return (k+4*extra)*a**p[0]*b**p[1]

# Reproduce the standard word from the pinned thirteen-cell canonical template.
B=CANON.copy();p=(0,0);h=3;letters=[]
for _ in range(104):p,h,c=step(B,p,h);letters.append(c)
assert ''.join(letters)==wake.STANDARD

for _ in range(400):
    a,b=rng.choice((F(4),F(7,2),F(5),F(9,2))),rng.choice((F(4),F(5),F(8)))
    p=(rng.randrange(-6,7),rng.randrange(-6,7))
    for h in range(4):
        for black in (False,True):
            B={(rng.randrange(-9,10),rng.randrange(-9,10)) for _ in range(12)}
            B.discard(p)
            if black:B.add(p)
            C=B.copy();q,k,c=step(C,p,h)
            center=rng.randrange(-6,7)
            s0=sum(p)-center; eps0=1 if h in (0,1) else -1; eps1=1 if k in (0,1) else -1
            expected=1+(4*(3**abs(s0)-1) if eps0!=eps1 and eps0*s0<0 else 0)
            assert wake.integer_clock(C,q,k,center)-wake.integer_clock(B,p,h,center)==expected>=1
            counts['integer_clock_full_state_identities']+=1
            for inv in (False,True):
                assert potential(C,q,k,a,b,inv)-potential(B,p,h,a,b,inv)==increment(p,h,c,a,b,inv)>0
                counts['full_state_local_clock_identities']+=1


def flux(word,heading=0):
    pts,hs,d=wake.plan(word,heading)
    assert d[0]==-d[1] and d[0]!=0
    sig=1 if heading%2==0 else -1
    A=Counter();m=Counter();up=Counter();dn=Counter();through_up=Counter();through_dn=Counter()
    for p,h,c in zip(pts,hs,word):
        t=sum(p);m[t]+=1;A[t]+=-sig*wake.chi(p)*(1 if c=='R' else -1)
        incoming=sum(wake.MOVES[h]);hout=(h+(1 if c=='R' else -1))%4;out=sum(wake.MOVES[hout])
        if out==1:up[t]+=1
        else:dn[t-1]+=1
        if incoming==out==1:through_up[t]+=1
        if incoming==out==-1:through_dn[t]+=1
    assert up==dn
    for t in m:
        assert through_up[t]==through_dn[t]
        assert m[t]==up[t-1]+up[t]
        assert m[t]==A[t]+4*through_up[t]
        assert up[t]<=3*up[t-1]+A[t]
        assert up[t-1]<=3*up[t]+A[t]
        counts['level_flow_identities']+=1
    assert len(word)==2*sum(up.values())
    assert d[0]==sum(sig*(1 if t%2==0 else -1)*f for t,f in up.items())
    return A,m,up

# Exhaustive, geometry-only identity controls include unrealizable words.
for n in range(2,15,2):
    for bits in product('RL',repeat=n):
        word=''.join(bits)
        try:pts,hs,d=wake.plan(word)
        except ValueError:continue
        if d[0]!=-d[1]:continue
        flux(word);counts['abstract_diagonal_word_controls']+=1

canonical=None
for ph in range(104):
    word=wake.STANDARD[ph:]+wake.STANDARD[:ph]
    for h0 in range(4):
        for power in (1,2,3):
            w=word*power;data=wake.periodic_data(w,h0);assert data
            seed,O,d=data;spec=wake.WakeSpec(d,O,h0);bn=wake.period_bound(spec)
            assert bn['cap']==856*power and bn['integer_clock']['cap']==856*power
            d0,O0,h=spec.normal();rturn=next(k for k in range(4) if wake.rot(d,k)==d0)
            pts,hs,_=wake.plan(w,h0);pts=[wake.rot(p,rturn) for p in pts];hs=[(v+rturn)%4 for v in hs]
            eta,A=wake.coefficients(spec)
            expected_A=Counter()
            sig=1 if h%2==0 else -1
            for q in O0:expected_A[sum(q)]-=sig*wake.chi(q)
            actual_A,m,f=flux(w,h)
            assert actual_A==expected_A
            caps=dict(bn['diagonal']['cuts']);assert all(v<=caps.get(t,0) for t,v in f.items())
            for rr in (F(4),F(7,2)):
                mb=wake.moment_bound(spec,rr)
                for inv,key in ((False,'plus'),(True,'minus')):
                    val=sum(increment(q,g,c,rr,rr,inv) for q,g,c in zip(pts,hs,w))
                    assert val==F(mb[key])>0
                    counts['period_moment_equalities']+=1
            counts['standard_phase_rotation_power_controls']+=1
            if ph%13==0 and h0==0 and power==1:
                assert wake.verify_forever(seed,w,h0)
                # Complete field check: untouched remote debris cancels in period increments.
                B={wake.rot(q,rturn) for q in seed}|{(100,-130),(-120,150)}
                p=(0,0);g=h;before=[potential(B,p,g,F(4),F(4),inv) for inv in (False,True)]
                for c in w:
                    p,g,got=step(B,p,g);assert got==c
                mb=wake.moment_bound(spec,F(4))
                for inv,key,old in zip((False,True),('plus','minus'),before):
                    assert potential(B,p,g,F(4),F(4),inv)-old==F(mb[key])
                counts['full_period_debris_controls']+=1
            if ph==h0==0 and power==1:
                canonical={'word':w,'seed':sorted(seed),'wake_representatives':O,'drift':d,'heading':h0,'bound':bn}

assert canonical
spec=wake.WakeSpec(tuple(canonical['drift']),tuple(map(tuple,canonical['wake_representatives'])))
positive=wake.synthesize(spec,witness=wake.STANDARD);assert positive['status']=='YES'
assert wake.synthesize(spec,max_nodes=0)['status']=='INCONCLUSIVE'
small=wake.WakeSpec((1,-1),((0,-3),(0,-1),(0,0),(0,1)),0)
negative=wake.synthesize(small);assert negative['status']=='NO' and negative['bound']['cap']==14
# Independent complete raw-word check through the DERIVED cap for the same inverse input.
for n in range(1,negative['bound']['cap']+1):
    for bits in product('RL',repeat=n):
        assert wake.spec_matches(small,''.join(bits)) is None
        counts['raw_negative_word_controls']+=1
# Representative shifts preserve all bounds; duplicate classes are rejected.
O=spec.representatives;d=spec.drift
for _ in range(64):
    shifted=tuple((q[0]+(n:=rng.randrange(-100,101))*d[0],q[1]+n*d[1]) for q in O)
    other=wake.WakeSpec(d,shifted,spec.heading)
    assert wake.period_bound(other)==wake.period_bound(spec)
    counts['coset_representative_controls']+=1
for d in ((1,0),(0,2),(0,0)):
    try:wake.WakeSpec(d,())
    except ValueError:counts['rejected_unsupported_inputs']+=1
    else:raise AssertionError('axis drift mislabeled as supported')
try:wake.WakeSpec(spec.drift,(O[0],(O[0][0]+spec.drift[0],O[0][1]+spec.drift[1])))
except ValueError:counts['rejected_unsupported_inputs']+=1
else:raise AssertionError('duplicate accepted')
# Non-axis parameters: same local clock identity already checked for anisotropic bases.
for d in ((1,-3),(2,-4),(3,1),(-5,-1)):
    fake=tuple((x,0) for x in range(4));s=wake.WakeSpec(d,fake)
    mb=wake.moment_bound(s)
    assert mb['cap']>=0
    counts['anisotropic_input_controls']+=1

report={'schema':'langtons-ant-wake-inverse-checks-v1','status':'passed','counts':dict(counts),
        'standard_period':104,'standard_exact_wake_period_cap':856,
        'standard_uniqueness_exhausted':False,'small_inverse_no':negative,
        'scope':{'HC_proved':False,'HC_counterexample':False,'axis_inverse_problem_solved':False,
                 'independent_review':False,'lean_formalization':False},
        'sha256':{p.name:sha256(p.read_bytes()).hexdigest() for p in (HERE/'wake.py',HERE/'check.py')}}
(HERE/'check_results.json').write_text(json.dumps(report,indent=2)+'\n')
(HERE/'standard_wake.json').write_text(json.dumps(canonical,indent=2)+'\n')
print(json.dumps(report,indent=2))
