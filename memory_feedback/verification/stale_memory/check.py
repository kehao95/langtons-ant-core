"""Exact scoped checks. Run without Python -O. No global nonuniversality claim."""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
import sys

from stale_memory import (State, simulate, predecessor, preceding_turns, suffix_details,
                         is_stale, first_stale_read, radius, event_count_deadline,
                         geometry, verify_period)

ROOT=Path(__file__).resolve().parent


def complex_start(s: State):
    return {complex(x,y) for x,y in s.black},complex(*s.pos),(1j,1,-1j,-1)[s.heading]


def ref_step(B,p,d):
    ch='L' if p in B else 'R'
    if p in B: B.remove(p); d*=1j
    else: B.add(p); d*=-1j
    return p+d,d,ch


def ref_past(s: State,D: int):
    B,p,d=complex_start(s)
    chars=[];positions=[]
    for _ in range(D):
        q=p-d
        if q in B:
            B.remove(q); d*=1j;ch='R'
        else:
            B.add(q); d*=-1j;ch='L'
        p=q;chars.append(ch);positions.append(p)
    return ''.join(reversed(chars)),list(reversed(positions))


def ref_first(s: State,D: int,limit: int=1000):
    _,old=ref_past(s,D)
    last={p:-D+j for j,p in enumerate(old)}
    B,p,d=complex_start(s)
    for t in range(limit):
        if p in B and (p not in last or t-last[p]>D):
            return t,[int(p.real),int(p.imag)]
        last[p]=t
        p,d,_=ref_step(B,p,d)
    return None


def rotated(s: State,r: int):
    f=(1j)**r
    def point(q):
        z=complex(*q)*f
        return int(z.real),int(z.imag)
    return State(frozenset(point(q) for q in s.black),point(s.pos),(s.heading-r)%4)


def first_ray_hit(s: State,word: str,q):
    points,_,d=geometry(s,word)
    options=[]
    for i,p in enumerate(points):
        v=q[0]-p[0],q[1]-p[1]
        k=None
        if d[0] and v[0]%d[0]==0:
            k=v[0]//d[0]
        elif not d[0] and d[1] and v[1]%d[1]==0:
            k=v[1]//d[1]
        if k is not None and k>=0 and (k*d[0],k*d[1])==v:
            options.append(k*len(word)+i)
    return min(options) if options else None


def basic():
    counts={'inverse_roundtrip':0,'local_predicate_checks':0,
            'small_seed_classifications':0,'white_old_return_controls':0}
    cells=list(itertools.product(range(-1,2),repeat=2))
    first_blank=[]
    for mask in range(512):
        B=frozenset(cells[i] for i in range(9) if mask>>i&1)
        for h in range(4):
            s=State(B,(0,0),h)
            prev,ch=predecessor(s)
            forward,word,_=simulate(prev,1)
            assert forward==s and word==ch
            counts['inverse_roundtrip']+=1
            for D in (1,2,4,8):
                past,positions=ref_past(s,D)
                assert preceding_turns(s,D)==past
                latest=next((j for j in range(D-1,-1,-1) if positions[j]==complex(*s.pos)),None)
                assert suffix_details(past)[1]==latest
                assert is_stale(s,D)==(s.pos in s.black and latest is None)
                counts['local_predicate_checks']+=1
                output=first_stale_read(s,D)
                expected=ref_first(s,D)
                assert expected is not None and output['kind']=='stale_read'
                assert (output['event_time'],output['point'])==expected
                assert output['event_time']<output['strict_waiting_bound']
                counts['small_seed_classifications']+=1
    # The initially all-white orbit itself creates long-lived black memory.
    blank=State(frozenset())
    for D in (4,16,64,128,256):
        out=first_stale_read(blank,D)
        expected=ref_first(blank,D,2000)
        assert expected==(out['event_time'],out['point'])
        first_blank.append({k:out[k] for k in ('D','event_time','point','updates_executed')})
    B,p,d=complex_start(blank);last={};turns=[]
    for t in range(2500):
        if t>=16 and p in last and t-last[p]>16 and p not in B:
            w=''.join(turns[-16:])
            assert suffix_details(w)==('R',None)
            counts['white_old_return_controls']+=1
        last[p]=t;p,d,ch=ref_step(B,p,d);turns.append(ch)
    assert counts['white_old_return_controls']>0
    out=first_stale_read(blank,128,max_suffix_states=0)
    assert out['kind']=='inconclusive'
    invalid=0
    for D in (0,-1,True,1.5):
        try:first_stale_read(blank,D)
        except ValueError:invalid+=1
    assert invalid==4
    result={'counts':counts,'blank_first_events':first_blank,
            'caller_cap_checks':1,'invalid_inputs_rejected':invalid}
    (ROOT/'basic_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


def periodic():
    mature,_,_=simulate(State(frozenset()),12000)
    h=mature
    controls=0
    for phase in range(104):
        for r in (range(4) if phase == 0 else range(1)):
            inp=rotated(h,r)
            out=first_stale_read(inp,128)
            assert out['kind']=='permanent_no_stale'
            assert len(out['cycle'])==104 and out['certificate']['valid']
            controls+=1
        h,_,_=simulate(h,1)
    base=first_stale_read(mature,128)
    assert base['entry']<=104
    word=base['prefix'][:104]
    assert len(word)==104 and verify_period(mature,word)['valid']
    points,_,drift=geometry(mature,word)
    far=[]
    for epoch in (10,1_000_000):
        q=(points[0][0]+epoch*drift[0],points[0][1]+epoch*drift[1])
        expected=first_ray_hit(mature,word,q)
        assert q not in mature.black and expected is not None
        modified=State(mature.black|{q},mature.pos,mature.heading)
        out=first_stale_read(modified,128)
        assert out['kind']=='stale_read' and out['event_time']==expected
        assert out['updates_executed']<1000
        far.append({'epoch':epoch,'point':list(q),'expected_first_hit':expected,
                    'returned_event_time':out['event_time'],
                    'updates_executed':out['updates_executed'],
                    'witness_mode':out['witness_mode']})
    q=(100_000_000,-100_000_000)
    assert first_ray_hit(mature,word,q) is None
    irrelevant=State(mature.black|{q},mature.pos,mature.heading)
    assert first_stale_read(irrelevant,128)['kind']=='permanent_no_stale'
    rejected=0
    for j in range(0,104,13):
        bad=word[:j]+('L' if word[j]=='R' else 'R')+word[j+1:]
        if not verify_period(mature,bad)['valid']:rejected+=1
    assert rejected==8
    result={'phase_rotation_controls':controls,'far_blockers':far,
            'irrelevant_archive_controls':1,'mutated_words_rejected':rejected,
            'positive_example':base,
            'scope':{'arbitrary_HALTING_decided':False,'global_nonuniversality':False,
                     'HC_proved':False,'independent_mathematical_review':False}}
    (ROOT/'periodic_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='positive_example'}))


def main():
    if sys.flags.optimize:raise SystemExit('Do not run exact checkers with -O.')
    mode=sys.argv[1] if len(sys.argv)>1 else 'all'
    if mode not in ('basic','periodic','all'):raise SystemExit('mode: basic, periodic, or all')
    if mode in ('basic','all'):basic()
    if mode in ('periodic','all'):periodic()
    if mode=='all':
        report={'status':'passed','basic':json.loads((ROOT/'basic_results.json').read_text()),
                'periodic':json.loads((ROOT/'periodic_results.json').read_text()),
                'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in (ROOT/'stale_memory.py',ROOT/'check.py',ROOT/'baseline/memory_delay.py')}}
        (ROOT/'check_results.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
