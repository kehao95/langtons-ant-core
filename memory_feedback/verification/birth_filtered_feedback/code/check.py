"""Independent finite controls for the complete-field newborn-feedback algorithm."""
from __future__ import annotations
import hashlib, json, random, sys, time
from pathlib import Path
import renewal as r

HERE=Path(__file__).resolve().parent
STANDARD='RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR'
SEED={(-7,0),(-7,1),(-6,-3),(-6,-2),(-6,-1),(-6,2),(-5,-2),(-5,0),(-5,1),(-5,2),(-4,-2),(-4,1),(-3,-3),(-3,1),(-2,-3),(-2,-1),(-2,1),(-1,-2),(-1,0)}

# This implementation uses an integer direction vector, not r.DIR or geometry.
def turn(v, black):
    x,y=v
    return (-y,x) if black else (y,-x)

def independent_prefix(black,pos,h,D,K,steps):
    B=set(black); p=pos; v=((0,1),(1,0),(0,-1),(-1,0))[h]
    born={}; last={}; reads=[]
    for t in range(steps):
        c=p in B
        if c and p in born and t-born[p]>D and p not in K:
            at=p; birth=born[p]
            B.remove(p); v=turn(v,True); p=(p[0]+v[0],p[1]+v[1])
            return dict(point=at,birth=birth,death=t,age=t-birth,black=B,pos=p,v=v),reads
        reads.append((t,p,c))
        if c: B.remove(p); born.pop(p,None)
        else: B.add(p); born[p]=t
        last[p]=t; v=turn(v,c); p=(p[0]+v[0],p[1]+v[1])
    return None,reads

def turn_replay(black,word,h=1):
    B=set(black); p=(0,0); v=((0,1),(1,0),(0,-1),(-1,0))[h]
    for t,c in enumerate(word):
        black_now=p in B
        if black_now != (c=='L'): return t
        if black_now:B.remove(p)
        else:B.add(p)
        v=turn(v,black_now); p=(p[0]+v[0],p[1]+v[1])
    return None

# A different infinite-tail formula, restricted to explicit seeds; independent
# of r.ray_intersection, segment intersection, residue splitting, or predictor.
def explicit_forever(seed,word,head=1):
    p=(0,0); v=((0,1),(1,0),(0,-1),(-1,0))[head]; pts=[]
    for c in word:
        pts.append(p); v=turn(v,c=='L'); p=(p[0]+v[0],p[1]+v[1])
    d=p; P=len(word)
    if d==(0,0) or v!=((0,1),(1,0),(0,-1),(-1,0))[head]:return False
    def match(a,b):
        dif=(a[0]-b[0],a[1]-b[1]); j=0 if d[0] else 1
        if dif[j]%d[j]:return None
        n=dif[j]//d[j]
        return n if dif==(n*d[0],n*d[1]) else None
    for i,q in enumerate(pts):
        old={k for z in seed if (k:=match(z,q)) is not None and k>=0}
        shifts=[k for j,z in enumerate(pts) if (k:=match(z,q)) is not None and (k>0 or (k==0 and j<i))]
        for k in {0,*old,*(j+1 for j in old),*shifts}:
            if ((k in old)+sum(s<=k for s in shifts))%2 != (word[i]=='L'):return False
    return True

def main():
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    started=time.monotonic(); rng=random.Random(20261015); report={}
    # Exact AP intersections: negative directions, nonprimitive directions,
    # singletons, cancellations and both determinant cases.
    intersections=0
    for _ in range(5000):
        a=(rng.randrange(-12,13),rng.randrange(-12,13))
        v=(rng.randrange(-4,5),rng.randrange(-4,5))
        n=1 if v==(0,0) else rng.randrange(1,20)
        q=(rng.randrange(-8,9),rng.randrange(-8,9))
        d=(0,0)
        while d==(0,0):d=(rng.randrange(-4,5),rng.randrange(-4,5))
        seg=r.Segment(a,v,n); ap=r.ray_intersection(seg,q,d)
        actual=set() if ap is None else {ap[0]+ap[1]*j for j in range(ap[2])}
        positions={(a[0]+j*v[0],a[1]+j*v[1]) for j in range(n)}
        expected={k for k in range(200) if (q[0]+k*d[0],q[1]+k*d[1]) in positions}
        assert actual==expected,(seg,q,d,ap,expected);intersections+=1
    report['ray_segment_intersections']=intersections
    # Direct epoch-word comparison, also checks the infinite last interval:
    # all finite APs end before a computed horizon, and thresholds are stable.
    sweeps=0
    for _ in range(800):
        terms=[]
        for j in range(rng.randrange(1,9)):
            v=(rng.randrange(-3,4),rng.randrange(-3,4));n=1 if v==(0,0) else rng.randrange(1,15)
            terms.append(r.Segment((rng.randrange(-9,10),rng.randrange(-9,10)),v,n))
        if rng.randrange(2):terms.extend(terms[:1]*2)
        f=r.Field(terms); exact=f.materialize();q=(rng.randrange(-5,6),rng.randrange(-5,6))
        d=(rng.choice((-3,-2,-1,1,2,3)),rng.randrange(-3,4))
        th=[rng.randrange(20) for _ in range(rng.randrange(8))];expected=rng.randrange(2)
        first=r.first_bad_epoch(f,q,d,th,expected,r.Limits())
        brute=next((k for k in range(200) if (((q[0]+k*d[0],q[1]+k*d[1]) in exact)+sum(s<=k for s in th))%2!=expected),None)
        assert first==brute;sweeps+=1
    report['epoch_parity_sweeps']=sweeps
    # Literal inverse uses no guessed negative-time all-white past.
    inv=0
    for _ in range(400):
        B={(x,y) for x in range(-2,3) for y in range(-2,3) if rng.randrange(3)==0}
        p=(rng.randrange(-2,3),rng.randrange(-2,3));h=rng.randrange(4)
        s=r.State.explicit(B,p,h); w=[];r.literal(s,0,w);c=r.inverse(s)
        assert s.field.materialize()==B and s.pos==p and s.heading==h and c==w[0].letter;inv+=1
    report['forward_inverse_pairs']=inv
    controls=[];readcount=0
    for i in range(120):
        B={(x,y) for x in range(-2,3) for y in range(-2,3) if rng.randrange(5)==0}
        h=rng.randrange(4); D=rng.choice((1,4,8,16,32,64,128))
        K={(x,y) for x in range(-1,2) for y in range(-1,2)} if i%3==0 else ({(0,0)} if i%3==1 else set())
        plain,reads=independent_prefix(B,(0,0),h,D,K,2500);readcount+=len(reads)
        got=r.fresh_feedback(r.State.explicit(B,heading=h),D,K,r.Limits(10000,300,100000))
        if plain is None:
            assert got['kind']!='FRESH_EXTERNAL' or got['death']>=2500
            continue
        assert got['kind']=='FRESH_EXTERNAL',(i,got)
        for k in ('point','birth','death','age'):assert got[k]==plain[k],(i,k,got[k],plain[k])
        assert got['post'].field.materialize()==plain['black']
        assert got['post'].pos==plain['pos'] and r.DIR[got['post'].heading]==plain['v']
        assert len(got['ignored_initial'])<=len(B)
        if D<=4:assert got['death']+1<=r.renewal_deadline(B,(0,0),D,K)
        # Every individual timestamp and bit in the compressed read schedule.
        flat=[]
        for ww in got['reads']:
            for j in range(ww.segment.length):
                flat.append((ww.time0+j*ww.time_stride,r.add(ww.segment.start,r.mul(ww.segment.stride,j)),ww.letter=='L'))
        flat.sort()
        expected_reads=reads+[(got['death'],got['point'],True)]
        assert flat==expected_reads
        controls.append(r.summary(got))
    report['birth_filtered_finite_controls']=len(controls)
    report['independent_literal_updates_before_targets']=readcount
    # Initial coordinates may be re-created; a static exclusion of B0 is wrong.
    witness=None
    for i in range(200):
        B={(x,y) for x in range(-2,3) for y in range(-2,3) if rng.randrange(3)==0}
        h=rng.randrange(4)
        got=r.fresh_feedback(r.State.explicit(B,heading=h),4,set(),r.Limits(2000,100,10000))
        if got['kind']=='FRESH_EXTERNAL' and got['point'] in B:
            plain,_=independent_prefix(B,(0,0),h,4,set(),got['death']+1)
            assert plain is not None and plain['birth']==got['birth']
            witness={'black':sorted(B),'heading':h,'result':r.summary(got)};break
    assert witness is not None
    report['reborn_initial_coordinate']=witness
    assert explicit_forever(SEED,STANDARD)
    assert turn_replay(SEED,STANDARD*25) is None
    report['standard_independent_infinite_check']=True
    report['standard_literal_steps']=2600
    negative=[]
    def rotate(p,n):
        for _ in range(n):p=(p[1],-p[0])
        return p
    for q in range(4):
        seed={rotate(p,q) for p in SEED}
        result=r.fresh_feedback(r.State.explicit(seed,heading=(1+q)%4),128,set(),r.Limits(10000,100,10000))
        assert result['kind']=='NO_FRESH_EXTERNAL'
        cert=result['certificate'];assert r.period_mismatch(cert['state'],cert['word']) is None
        negative.append(r.summary(result))
    report['negative_periodic_controls']=negative
    huge=[]
    for n in (10,100,10**60):
        seed=SEED|{(2*n,-2*n)}
        result=r.fresh_feedback(r.State.explicit(seed,heading=1),128,set(),r.Limits(10000,100,100000))
        assert result['kind']=='FRESH_EXTERNAL'
        assert ((2*n,-2*n),104*n) in result['ignored_initial']
        assert result['birth']==104*n-102 and result['death']==104*n+46
        assert result['point']==(2*n-3,-2*n+1) and result['age']==148
        assert sum(w.segment.length for w in result['reads'])==result['death']+1
        if n<=100:
            plain,_=independent_prefix(seed,(0,0),1,128,set(),104*n+47)
            assert plain and plain['birth']==result['birth']
            assert result['post'].field.materialize()==plain['black']
        # A later source time must NOT keep using the old origin's birth rule.
        huge.append({'epoch':str(n),'result':r.summary(result)})
    report['remote_initial_black_is_not_renewal']=huge
    caps=[]
    for lim in (r.Limits(suffix_states=0),r.Limits(event_calls=0)):
        got=r.fresh_feedback(r.State.explicit([]),128,set(),lim)
        assert got['kind']=='INCONCLUSIVE';caps.append(got['reason'])
    f=r.Field([r.Segment((0,0),(7,0),10)])
    try:r.first_bad_epoch(f,(0,0),(1,0),[],0,r.Limits(residue_modulus=1));assert False
    except r.Exhausted:caps.append('epoch residue modulus')
    report['resource_controls']=caps
    # Uniform growing parameters: compute exact integer horizon cutoffs, not
    # a numerical asymptotic extrapolation or a diagnosed nonperiodic input.
    scales=[]
    for exponent in (64,80,128,256,512):
        H=3**exponent
        result=r.growing_scale_floor(20,100,H)
        n=result['n'];a=result['quadratic_coefficient'];c=result['linear_coefficient']
        assert a*n*n+c*n<=H<a*(n+1)*(n+1)+c*(n+1)
        assert result['L']==exponent and result['D']>=1
        assert result['ell']<=5*exponent//16+5 and result['count']>0
        scales.append({k:v for k,v in result.items() if k not in ('burst','linear_coefficient')})
    report['growing_scale_arithmetic']=scales
    parts=r.deadline_parts(set(),(0,0),128,{(0,0)})
    assert parts['exponent']>10**30
    try:r.renewal_deadline(set(),(0,0),128,{(0,0)});assert False
    except r.Exhausted:pass
    report['symbolic_huge_deadline_control']=True
    # Complete resetting test: canonicalization is exact XOR cancellation,
    # not deletion of genuinely unvisited or inactive physical black cells.
    state=r.State.explicit([]); at=0; rounds=[]
    for k in range(100):
        B=state.field.materialize(); start_pos=state.pos; start_h=state.heading
        result=r.fresh_feedback(state,128,set(),r.Limits(30000,500,100000))
        rec=r.summary(result);rec['start_time']=at;rec['source_mass']=len(B);rounds.append(rec)
        if result['kind']=='NO_FRESH_EXTERNAL':
            cert=result['certificate'];assert r.period_mismatch(cert['state'],cert['word']) is None
            break
        assert result['kind']=='FRESH_EXTERNAL'
        direct,_=independent_prefix(B,start_pos,start_h,128,set(),result['death']+1)
        assert direct and direct['birth']==result['birth'] and direct['point']==result['point']
        assert direct['black']==result['post'].field.materialize()
        at+=result['death']+1;state=result['post'];state.field=r.Field.explicit(state.field.materialize())
    assert len(rounds)==32 and at==9990 and rounds[-1]['kind']=='NO_FRESH_EXTERNAL'
    report['blank_positive_renewal_rounds']=31
    report['blank_terminal_checkpoint']=9990
    (HERE.parent/'evidence'/'rounds.json').write_text(json.dumps(rounds,indent=2)+'\n')
    report['status']='passed'
    report['evidence_boundary']='Analytic totality proof is separate. Finite tests do not prove HC or existence of a nonperiodic orbit. NO_FRESH_EXTERNAL certifies ETC, not NO_HIGHWAY.'
    report['elapsed_seconds']=time.monotonic()-started
    report['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HERE.glob('*.py')}
    out=HERE.parent/'evidence'/'replay.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('negative_periodic_controls','remote_initial_black_is_not_renewal','reborn_initial_coordinate')},indent=2),flush=True)

if __name__=='__main__':main()
