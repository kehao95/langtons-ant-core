#!/usr/bin/env python3
"""Scoped deterministic replay of the scalable feedback circuit and its guards."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import random
import circuit as c

BASE = '7a8101ee9827d2f060853e70a2804c0fd5c9117e'
HERE = Path(__file__).resolve().parent

def digest(points):
    return hashlib.sha256(json.dumps(sorted(points), separators=(',', ':')).encode()).hexdigest()

def independent(start: c.State, steps: int):
    """Second implementation: complex directions and black-set mutation.

    Used only at small integral coordinates in these finite controls, exactly
    representable by complex binary floats. No huge-coordinate claim uses it.
    """
    black = {complex(x,y) for x,y in start.black}
    p = complex(*start.pos); direction = [1j,1,-1j,-1][start.heading]
    positions = []; word = []; heads = []; last = {}; events = []
    for t in range(steps):
        positions.append((int(p.real),int(p.imag)))
        heads.append([1j,1,-1j,-1].index(direction))
        bit = p in black
        if bit and (p not in last or t-last[p] > 128):
            events.append(t)
        last[p] = t
        word.append('L' if bit else 'R')
        if bit: black.remove(p);direction *= 1j
        else: black.add(p);direction *= -1j
        p += direction
    positions.append((int(p.real),int(p.imag)))
    heads.append([1j,1,-1j,-1].index(direction))
    result = c.State(frozenset((int(q.real),int(q.imag)) for q in black),
                     positions[-1],heads[-1])
    return result,''.join(word),positions,heads,events,last

def ordered_class_check(x: c.State, word: str) -> dict:
    """Independent infinite check: stable class alternation + exact clean seed."""
    pp, hh = c.geometry(x.pos,x.heading,word); points=pp[:-1]
    d=pp[-1][0]-x.pos[0],pp[-1][1]-x.pos[1]
    if hh[-1]!=x.heading or d==(0,0):return {'valid':False}
    remaining=set(range(len(word)));required=set();classes=0
    while remaining:
        anchor=points[min(remaining)];group=[]
        for j in sorted(remaining):
            a=c.multiple((points[j][0]-anchor[0],points[j][1]-anchor[1]),d)
            if a is not None:group.append((a,j))
        for _,j in group:remaining.remove(j)
        group.sort(key=lambda a:(-a[0],a[1]));classes+=1
        if any(word[j]!=('R' if rank%2==0 else 'L') for rank,(_,j) in enumerate(group)):
            return {'valid':False,'reason':'stable alternation'}
        low=min(a for a,j in group);high=max(a for a,j in group)
        for k in range(low,high):
            available=[(a,j) for a,j in group if a<=k]
            if available and word[available[0][1]]=='L':
                required.add((anchor[0]+k*d[0],anchor[1]+k*d[1]))
    for q in x.black.symmetric_difference(required):
        for p in points:
            a=c.multiple((q[0]-p[0],q[1]-p[1]),d)
            if a is not None and a>=0:
                return {'valid':False,'reason':'complete-field ray discrepancy'}
    return {'valid':True,'classes':classes,'required_black':len(required)}

def reference_controls():
    r=c.reference();a=c.verify_period(r['tail'],r['U']);b=ordered_class_check(r['tail'],r['U'])
    assert a['valid'] and b['valid']
    assert (len(r['tail'].black),r['tail'].pos,r['tail'].heading)==(36,(5,1),1)
    stop=390
    x,w,ps,hs=c.replay(c.State(c.G),stop)
    y,v,qq,jj,events,_=independent(c.State(c.G),stop)
    assert (x,w,ps,hs)==(y,v,qq,jj)
    assert events==[1,22,32,58,157,280,281]
    assert ps[60]==(0,2) and w[60]=='R'
    assert max(i for i,p in enumerate(ps[:-1]) if p==(0,2))==60
    assert min(p[0] for p in r['cycle'])>=4
    assert r['cycle'][14]==(8,2) and r['U'][14]=='R'
    assert r['cycle'][61]==(7,8) and r['cycle'][71]==(6,9)
    # Infinite S_128-freedom from epoch one, not extrapolation of events[].
    phase_bounds=[]; stationary_gaps=[]
    for i,ch in enumerate(r['U']):
        if ch!='L':continue
        links=[]
        for j,q in enumerate(r['cycle']):
            p=r['cycle'][i];k=c.multiple((q[0]-p[0],q[1]-p[1]),(2,2))
            if k is not None and (k>0 or (k==0 and j<i)):
                gap=104*k+i-j
                if gap<=128:links.append((k,gap))
        assert links
        phase_bounds.append(min(k for k,gap in links)); stationary_gaps.append(min(gap for k,gap in links))
    assert max(phase_bounds)==1 and max(stationary_gaps)==116
    assert all(q in set(r['prefix']) for q in c.G)
    return {'complete_endpoint_cells':36,'period_parity':a,'ordered_classes':b,
            'first_visit_and_old_read_offsets':events,
            'all_black_phases_have_128_recent_predecessor_by_epoch':1,'stationary_max_black_gap':116}

def affine_endpoint_controls():
    r=c.reference(); checks=0; cumulative=(0,0)
    expected_times=[(0,0),(104,-173),(312,-440),(728,-821),(936,-1296),(1248,-1516)]
    expected_origins=[spec[0] for spec in c.SPECS]+[((0,0),(0,2))]
    for i,(origin,rot,repeats,rem) in enumerate(c.SPECS):
        q=c.rotate(r['cycle'][rem],rot);d=c.rotate((2,2),rot)
        end=tuple((origin[a][0]+d[a]*repeats[0],
                   origin[a][1]+q[a]+d[a]*repeats[1]) for a in range(2))
        assert end==tuple(expected_origins[i+1]);checks+=2
        target_h=1 if i==4 else (1+c.SPECS[i+1][1])%4
        assert (r['cycle_h'][rem]+rot)%4==target_h;checks+=1
        cumulative=(cumulative[0]+104*repeats[0],cumulative[1]+182+104*repeats[1]+rem)
        assert cumulative==expected_times[i+1];checks+=1
    return {'universal_affine_endpoint_equalities':checks}

def recovery_controls():
    source=c.State(c.protected_core(),(0,2),1)
    target,prefix,ps,hs=c.replay(source,774)
    _,word,qs,_=c.replay(target,104)
    a=c.verify_period(target,word);b=ordered_class_check(target,word)
    assert a['valid'] and b['valid'] and a['drift']==[2,-2]
    assert all(c.in_region(p) for p in ps+qs)
    assert prefix[-1]=='R' and word[-1]=='L'
    U=c.reference()['U'];assert word==U[103:]+U[:103]
    reverse=source
    for _ in range(128):
        reverse=c.inverse(reverse)
        assert c.in_region(reverse.pos)
    # Scope checks: deletion of the feedback cell changes its actual read.
    altered=c.State(source.black-{(0,2)},source.pos,source.heading)
    assert c.replay(source,1)[1]=='L' and c.replay(altered,1)[1]=='R'
    # A far future blocker invalidates an otherwise certified period.
    p=(target.pos[0]+2*10**30,target.pos[1]-2*10**30)
    bad=c.State(target.black|{p},target.pos,target.heading)
    assert not c.verify_period(bad,word)['valid']
    assert not ordered_class_check(bad,word)['valid']
    # Off-trace material is retained, not declared absent.
    off=(10**30,10**30)
    good=c.State(target.black|{off},target.pos,target.heading)
    assert c.verify_period(good,word)['valid'] and ordered_class_check(good,word)['valid']
    return {'protected_region':list(c.REGION),'core_cells':len(source.black),
            'core_sha256':digest(source.black),'recovery_updates':774,
            'target_cells':len(target.black),'target_pose':[list(target.pos),target.heading],
            'period_parity':a,'ordered_classes':b,'standard_phase_in_reference':103,
            'last_incompatible_turn_offset':773,'previous_128_reads_protected':True,
            'far_blocker_rejected':True,'off_trace_marker_retained':True},word

def factor_controls():
    """Definition-only J10 count, independent of the concurrent rigidity proof.

    Deleting complete interior U cycles removes only allowed ten-factors and
    preserves both length-nine boundary contexts. Every stage has >=1 cycle.
    """
    r=c.reference(); U=r['U']; allowed={(U*2)[i:i+10] for i in range(104)}
    prefix=''.join(r['A']+U+U[:spec[3]] for spec in c.SPECS)
    _,recovery,_,_=c.replay(c.State(c.protected_core(),(0,2),1),774)
    tail=U[103:]+U[:103]; word=prefix+recovery+tail[:9]
    bad=[i for i in range(9,len(word)) if word[i-9:i+1] not in allowed]
    assert len(allowed)==84 and sum(60<i<len(prefix) for i in bad)==264
    assert len(bad)==532 and bad[-1]-len(prefix)==782
    return {'factor_length':10,'allowed_factors':84,
            'J10_strictly_between_birth_and_return':264,
            'J10_from_update_9_onwards':532,
            'last_J10_relative_to_return':782,
            'basis':'remove only full standard cycles; no use of factor-rigidity theorem'}


def finite_family_controls(word):
    rows=[];total_updates=0
    offsets=reference_controls()['first_visit_and_old_read_offsets']
    for n in (20,22,24,30,40,60,100,200):
        start=c.seed(n);e=c.first_return_time(n);times=c.milestones(n)
        full,turns,ps,hs,events,last=independent(start,e)
        total_updates+=e
        assert full.pos==(0,2) and full.heading==1 and (0,2) in full.black
        assert last[complex(0,2)]==60
        assert len(start.black)==20 and (0,2) not in start.black
        assert sum(60<t<e for t in events)==31
        declared=''.join(c.stage_word(i,n//2) for i in range(5))
        assert turns==declared
        U=c.reference()['U']; allowed={(U*2)[i:i+10] for i in range(104)}
        assert sum(turns[i-9:i+1] not in allowed for i in range(61,e))==264
        expected_events=sorted(t+a for t in times[:-1] for a in offsets)
        assert events==expected_events
        assert full==c.full_collision_state(n)
        assert {q for q in full.black if c.in_region(q)}==c.protected_core()
        final,w,_,_=c.replay(full,774);total_updates+=774
        assert c.verify_period(final,word)['valid'] and ordered_class_check(final,word)['valid']
        assert w[-1]=='R'
        for i,t in enumerate(times[:-1]):
            origin,rot,_,_=c.SPECS[i]
            assert ps[t]==tuple(c.lin_value(a,n//2) for a in origin) and hs[t]==(1+rot)%4
        rows.append({'n':n,'input_cells':20,'birth':60,'consumption':e,
                     'age':e-60,'S128_strictly_between':31,
                     'exact_standard_entry':e+774,'full_collision_cells':len(full.black),
                     'full_collision_sha256':digest(full.black),
                     'complete_standard_state_cells':len(final.black)})
    return {'parameters':rows,'literal_updates':total_updates}

def no_intervening_event_controls():
    rng=random.Random(104128);cases=0;updates=0
    for seed_no in range(12):
        B=frozenset((x,y) for x in range(-3,4) for y in range(-3,4) if rng.randrange(6)==0)
        source=c.State(B,(0,0),seed_no%4)
        _,word,positions,_=c.replay(source,1800);updates+=1800
        previous={};gaps=[]
        for t,p in enumerate(positions[:-1]):
            gaps.append(None if p not in previous else t-previous[p]);previous[p]=t
        for D in (1,2,3,4,8,16):
            sums=[0]
            for t,ch in enumerate(word):
                sums.append(sums[-1]+int(ch=='L' and (gaps[t] is None or gaps[t]>D)))
            for e,gap in enumerate(gaps):
                if gap is None:continue
                birth=e-gap
                if birth<D or word[birth]!='R':continue
                if sums[e]-sums[birth+1]==0:
                    assert gap<=5*(1<<D)**2;cases+=1
    return {'finite_no_intervening_event_returns':cases,'literal_updates':updates,
            'claim_boundary':'finite controls supplement the analytic lasso argument'}

def main():
    if not __debug__: raise RuntimeError('do not disable assertions')
    sep=c.separation_certificate();region=c.protected_region_certificate()
    rec,word=recovery_controls()
    report={'schema':'langtons-ant-scalable-feedback-circuit-v1','base_commit':BASE,
            'claim':'all-parameter positive family and a failed event-count-only age closure; not HC',
            'reference':reference_controls(),'endpoints':affine_endpoint_controls(),
            'separation':sep,'protected_region':region,'recovery':rec,
            'finite_family':finite_family_controls(word),
            'no_intervening_event':no_intervening_event_controls(),'factor_counts':factor_controls()}
    failures=0
    for n in (True,19,21,-2,0,20.0):
        try:c.seed(n)
        except ValueError:failures+=1
        else:raise AssertionError('invalid parameter accepted')
    assert failures==6
    big=2*10**60
    report['huge_parameter']={'n':str(big),'source_cells':len(c.seed(big).black),
                             'consumption':str(c.first_return_time(big)),
                             'exact_standard_entry':str(c.standard_entry_time(big)),
                             'mode':'all-parameter certificate; no huge literal replay'}
    report['validation_rejections']=failures
    report['sources_sha256']={p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in ('circuit.py','check.py')}
    output=HERE/'report.json';output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','affine_inequalities':sep['universal_linear_inequalities']+region['affine_inequalities'],
                      'finite_family_updates':report['finite_family']['literal_updates'],
                      'return_controls':report['no_intervening_event']['finite_no_intervening_event_returns'],
                      'source_parameters':len(report['finite_family']['parameters'])},sort_keys=True))

if __name__=='__main__':main()
