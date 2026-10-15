"""Exact scoped controls; finite tests are not all-input or nonuniversality proofs."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import random
import sys
from observed_stale import Observer, next_observed_macro, observed_event_budget, scan_prescribed_observations, _feed_repeated, first_trigger_deadline
from symbolic_stale import Segment, SymbolicState, State, next_stale_macro, state_data, geometry


def stats():
    return dict(explicit_updates=0, symbols_built=0, transition_evaluations=0,
                epoch_intervals=0, blocks_skipped=0)


def pair(z): return int(z.real), int(z.imag)
def heading(v): return (1j, 1, -1j, -1).index(v)


def complex_state(x):
    y=x.materialize()
    return set(complex(*v) for v in y.black), complex(*y.pos), 1j*(-1j)**y.heading


def literal(b,p,v):
    old=p in b; b.symmetric_difference_update({p})
    v*=1j if old else -1j
    return p+v,v


def reverse(b,p,v):
    p-=v; old=p in b; b.symmetric_difference_update({p})
    v*=1j if old else -1j
    return p,v


def symbol(o,b,p,v):
    mask=sum(int(p+complex(*off) in b)<<j for j,off in enumerate(o.offsets))
    return heading(v)*(1<<len(o.offsets))+mask


def ref_trigger(x,D,o,state=0,max_steps=10000):
    b,p,v=complex_state(x); rb,rp,rv=b.copy(),p,v; last={}
    for k in range(1,D+1):
        rp,rv=reverse(rb,rp,rv);last.setdefault(rp,-k)
    for t in range(max_steps):
        nxt=o.table[state][symbol(o,b,p,v)]
        if nxt==-1:
            return 'halt',t,State(frozenset(pair(q) for q in b),pair(p),heading(v)),state
        state=nxt
        stale=p in b and t-last.get(p,-D-1)>D
        last[p]=t;p,v=literal(b,p,v)
        if stale:
            return 'stale_read',t,State(frozenset(pair(q) for q in b),pair(p),heading(v)),state
    return None


def table(q,offsets,rng,halting=True):
    a=4*(1<<len(offsets))
    return Observer(offsets,tuple(tuple(-1 if halting and rng.randrange(17)==0
                        else rng.randrange(q) for _ in range(a)) for _ in range(q)))


def main():
    if sys.flags.optimize: raise SystemExit('Do not use -O')
    rng=random.Random(1202026)
    counts=dict(literal_trigger_controls=0,prescribed_observation_controls=0,
                repeated_word_controls=0,event_budget_controls=0,invalid_or_cap_controls=0)
    cells=[(x,y) for x in range(-1,2) for y in range(-1,2)]
    observers=[table(3,((0,0),(1,0),(0,1)),rng),table(5,((-2,1),(1,-2)),rng,False)]
    for mask in range(512):
        for h in range(4):
            D=(1,2,4,8)[(mask+h)%4]
            x=SymbolicState.explicit(State(frozenset(v for j,v in enumerate(cells) if mask>>j&1),(0,0),h))
            o=observers[(mask+h)%2];s=(mask+h)%len(o.table);ref=ref_trigger(x,D,o,s)
            assert ref is not None
            out=next_observed_macro(x,D,o,s)
            assert out['kind']==ref[0],(mask,h,out,ref)
            assert out['time' if ref[0]=='halt' else 'event_time']==ref[1]
            assert out['state' if ref[0]=='halt' else 'after'].materialize()==ref[2]
            assert out['observer_state']==ref[3] and ref[1]<first_trigger_deadline(x,D,o)
            counts['literal_trigger_controls']+=1
    for trial in range(320):
        while True:
            word=''.join(rng.choice('RL') for _ in range(rng.choice((4,8,12,16))))
            terms=tuple(Segment((rng.randrange(-6,7),rng.randrange(-6,7)),
                        rng.choice(((1,0),(0,-1),(1,1),(-2,1))),rng.randrange(1,10)) for _ in range(5))
            x=SymbolicState(terms,(rng.randrange(-2,3),rng.randrange(-2,3)),rng.randrange(4))
            _,_,h,d=geometry(x,word)
            if h==x.heading and d!=(0,0):break
        o=table(4,((0,0),(2,-1),(-1,2)),rng,trial%2==0)
        n=rng.randrange(0,350);s=rng.randrange(4);b,p,v=complex_state(x);rstate=s;expected=None
        for t in range(n):
            nxt=o.table[rstate][symbol(o,b,p,v)]
            if nxt==-1:expected=t;break
            rstate=nxt;b.symmetric_difference_update({p})
            v*=-1j if word[t%len(word)]=='R' else 1j;p+=v
        hit,outstate=scan_prescribed_observations(x,word,o,s,n,stats())
        assert (hit,outstate)==(expected,rstate),(trial,word,n,hit,outstate,expected,rstate)
        counts['prescribed_observation_controls']+=1
    for trial in range(320):
        o=table(rng.randrange(1,8),((0,0),),rng,trial%2==0)
        block=[rng.randrange(8) for _ in range(rng.randrange(1,14))]
        n=rng.randrange(300);s=rng.randrange(len(o.table));rstate=s;expected=None
        for t in range(n*len(block)):
            nxt=o.table[rstate][block[t%len(block)]]
            if nxt==-1:expected=t;break
            rstate=nxt
        hit,outstate=_feed_repeated(o,s,block,n,stats())
        assert (hit,outstate)==(expected,rstate)
        counts['repeated_word_controls']+=1
    o=Observer(((0,0),),tuple(tuple((-1 if s==2 else s+1) if code&1 else s for code in range(8)) for s in range(3)))
    for mask in range(64):
        x=SymbolicState.explicit(State(frozenset(v for j,v in enumerate(cells[:6]) if mask>>j&1)))
        short=observed_event_budget(x,1,o,1);enough=observed_event_budget(x,1,o,2)
        assert short['kind']=='budget_exhausted' and not short['global_no_halt']
        assert enough['kind']=='halt' and enough['consumed']==2
        b,p,v=complex_state(x); black_count=0
        for t in range(1000):
            if p in b:black_count+=1
            if black_count==3:break
            p,v=literal(b,p,v)
        assert enough['time']==t
        counts['event_budget_controls']+=2
    b,p,v=set(),0j,1j
    for _ in range(12000):p,v=literal(b,p,v)
    highway=SymbolicState.explicit(State(frozenset(pair(z) for z in b),pair(p),heading(v)))
    bb,pp,vv=b.copy(),p,v;turns=[];points=[]
    for _ in range(104):
        points.append(pair(pp));turns.append('L' if pp in bb else 'R');pp,vv=literal(bb,pp,vv)
    word=''.join(turns);drift=pair(pp-p);N=10**12;offset=(200,-200)
    marker=(points[0][0]+offset[0]+N*drift[0],points[0][1]+offset[1]+N*drift[1])
    ant_cross={q[0]-q[1] for q in points};obs_cross={z+400 for z in ant_cross}
    assert ant_cross.isdisjoint(obs_cross)
    assert {int(z.real-z.imag) for z in b}.isdisjoint(obs_cross)
    marked=SymbolicState(highway.terms+(Segment(marker,(0,0),1),),highway.pos,highway.heading)
    physical=next_stale_macro(marked,128)
    assert physical['kind']=='permanent_no_stale'
    observer=Observer((offset,),(tuple(-1 if code&1 else 0 for code in range(8)),))
    out=next_observed_macro(marked,128,observer);expected=[]
    for i,q in enumerate(points):
        dx,dy=marker[0]-q[0]-offset[0],marker[1]-q[1]-offset[1]
        if dx%drift[0]==0 and dy%drift[1]==0 and dx//drift[0]==dy//drift[1]>=0:
            expected.append(104*(dx//drift[0])+i)
    first=min(expected)
    assert out['kind']=='halt' and out['time']==first
    assert out['state'].black((out['state'].pos[0]+offset[0],out['state'].pos[1]+offset[1]))
    assert next_observed_macro(highway,128,observer)['kind']=='permanent_no_halt'
    active_marker=(points[0][0]+N*drift[0],points[0][1]+N*drift[1])
    active=SymbolicState(highway.terms+(Segment(active_marker,(0,0),1),),highway.pos,highway.heading)
    phase_reader=Observer(((0,0),),tuple(tuple(-1 if s==0 and code&1 else (s+1)%104
                                             for code in range(8)) for s in range(104)))
    tied=next_observed_macro(active,128,phase_reader)
    physical_tied=next_stale_macro(active,128)
    assert tied['kind']=='halt' and physical_tied['kind']=='stale_read'
    assert tied['time']==physical_tied['event_time']==104*N
    assert tied['observer_state']==0 and tied['state'].black(active_marker)
    segments=(Segment((marker[0]-N*drift[0]+1000*drift[0],marker[1]-N*drift[1]+1000*drift[1]),
                       (3*drift[0],3*drift[1]),10**15),
              Segment((marker[0]-N*drift[0]+2000*drift[0],marker[1]-N*drift[1]+2000*drift[1]),
                       (5*drift[0],5*drift[1]),10**15))
    track=SymbolicState(highway.terms+segments,highway.pos,highway.heading)
    counter=Observer((offset,),tuple(tuple((s+1)%7 for _ in range(8)) for s in range(7)))
    count=104*10**18+37;st=stats()
    hit,end=scan_prescribed_observations(track,word,counter,0,count,st)
    assert hit is None and end==count%7 and st['blocks_skipped']>10**15
    for kwargs in [dict(max_suffix_states=0),dict(max_residue_checks=0),dict(max_symbols=0)]:
        r=next_observed_macro(highway,128,observer,**kwargs)
        assert r['kind']=='inconclusive';counts['invalid_or_cap_controls']+=1
    for args in [((),()),(((0,0),),((0,),)),(((0,0),(0,0)),(tuple(0 for _ in range(16)),))]:
        try:Observer(*args)
        except ValueError:counts['invalid_or_cap_controls']+=1
        else:raise AssertionError('invalid observer accepted')
    report={'schema':'langtons-ant-observer-macro-checks-v1','date':'2026-10-12','status':'passed',
            'counts':counts,'passive_marker':{'phase_word':word,'period':104,'drift':list(drift),
            'offset':list(offset),'marker':list(marker),'epoch_parameter':N,'first_halt':first,
            'physical_stale_result':physical['kind'],'observer_result':out['kind'],
            'explicit_updates':out['stats']['explicit_updates'],'stats':out['stats'],
            'halt_state_sha256':hashlib.sha256(json.dumps(state_data(out['state']),sort_keys=True).encode()).hexdigest()},
            'simultaneous_halt_and_stale':{'time':tied['time'],'result':tied['kind'],'pre_update_black_preserved':True},
            'long_residue_observation':{'count':count,'final_observer_state':end,'stats':st},
            'scope':{'global_nonuniversality':False,'arbitrary_global_halt_decider':False,
                     'old_one_black_rerun':False,'lean':False,'independent_mathematical_review':False},
            'source_sha256':{n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in
                             ['observed_stale.py','check_observer.py','symbolic_stale.py','memory_delay.py']}}
    Path('observer_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
