"""Independent finite controls and exact huge-prefix algebra controls."""
from __future__ import annotations
import json,random,sys,time,hashlib
from pathlib import Path
from collections import Counter
from symbolic_stale import (Segment, SymbolicState, ray_segment_epochs,
    verify_period,apply_periodic_prefix,next_stale_macro,step,predecessor,
    preceding_turns, state_data, state_from_data, event_prefix)
from memory_delay import State,simulate,geometry,verify_period as verify_explicit

def reference(s: State,n: int):
    b={complex(*p) for p in s.black};p=complex(*s.pos)
    dirs=(1j,1,-1j,-1);h=dirs[s.heading]
    for _ in range(n):
        if p in b:b.remove(p);h*=1j
        else:b.add(p);h*=-1j
        p+=h
    return State(frozenset((int(q.real),int(q.imag)) for q in b),
                 (int(p.real),int(p.imag)),dirs.index(h))

def first_event(s: State,D: int,cap: int):
    # Independent inverse history; do not call the tested suffix predictor.
    b={complex(*p) for p in s.black};p=complex(*s.pos);dirs=(1j,1,-1j,-1);h=dirs[s.heading]
    backb=set(b);backp=p;backh=h;hist=[]
    for _ in range(D):
        q=backp-backh;was_right=q in backb
        if was_right:backb.remove(q)
        else:backb.add(q)
        backh*=1j if was_right else -1j;backp=q;hist.append(q)
    hist=list(reversed(hist))
    for t in range(cap):
        if p in b and p not in hist[-D:]:return t
        hist.append(p)
        if p in b:b.remove(p);h*=1j
        else:b.add(p);h*=-1j
        p+=h
    return None

def main():
    if sys.flags.optimize: raise SystemExit('assertions required')
    rng=random.Random(20261012);c=Counter()
    for _ in range(4000):
        q=(rng.randrange(-8,9),rng.randrange(-8,9));d=(rng.randrange(-4,5),rng.randrange(-4,5))
        if d==(0,0):d=(1,0)
        a=(rng.randrange(-8,9),rng.randrange(-8,9));v=(rng.randrange(-4,5),rng.randrange(-4,5))
        if v==(0,0):v=(0,1)
        s=Segment(a,v,rng.randrange(1,15));ap=ray_segment_epochs(q,d,s)
        actual={ (a[0]+j*v[0],a[1]+j*v[1]) for j in range(s.length)}
        for k in range(60):
            want=(q[0]+k*d[0],q[1]+k*d[1]) in actual
            got=ap is not None and ap[0]<=k<=ap[1] and k%ap[3]==ap[2]
            assert want==got,(q,d,s,k,ap);c['ray_epoch_comparisons']+=1
    # Parallel, congruence, reversed-stride, singleton and coincident cancellation controls.
    for A in [-6,-4,-2,-1,1,2,4,6]:
      for B in [-9,-6,-3,-1,1,3,6,9]:
       for C in range(-8,9):
        s=Segment((C,2*C),(B,2*B),11);ap=ray_segment_epochs((0,0),(A,2*A),s)
        for k in range(100):
            want=s.contains((k*A,2*k*A));got=ap is not None and ap[0]<=k<=ap[1] and k%ap[3]==ap[2]
            assert want==got;c['parallel_epoch_comparisons']+=1
    words=[]
    for n in (4,8,12,16):
      for _ in range(150):
        w=''.join(rng.choice('RL') for _ in range(n));_,h,d=geometry(State(frozenset()),w)
        if h==0 and d!=(0,0):words.append(w)
    for _ in range(256):
        terms=[]
        for _ in range(8):
            a=(rng.randrange(-7,8),rng.randrange(-7,8));v=rng.choice([(1,0),(0,1),(2,2),(-3,-3),(1,-1)])
            terms.append(Segment(a,v,rng.randrange(1,8)))
        terms.extend(terms[:2]) # deliberate XOR cancellation
        x=SymbolicState(tuple(terms));e=x.materialize();y,ch=step(x)
        assert y.materialize()==reference(e,1)
        prev,ch2=predecessor(y);assert prev.materialize()==e and ch==ch2;c['inverse_controls']+=1
        for w in rng.sample(words,min(4,len(words))):
            a=verify_period(x,w);b=verify_explicit(e,w)
            assert a['valid']==b['valid']
            assert a['first_bad_offset']==b.get('first_bad_offset')
            n=a['first_bad_offset'] if not a['valid'] else 300
            z=apply_periodic_prefix(x,w,n)
            assert z.materialize()==reference(e,n);c['period_xor_controls']+=1
    cells=[(a,b) for a in (-1,0,1) for b in (-1,0,1)]
    for mask in range(128):
      for h in range(4):
       e=State(frozenset(p for i,p in enumerate(cells) if mask>>i&1),(0,0),h)
       for D in (1,2,4,8):
        x=SymbolicState.explicit(e);ans=next_stale_macro(x,D)
        assert ans['kind']=='stale_read';t=ans['event_time'];assert t==first_event(e,D,t+1)
        assert ans['before'].materialize()==reference(e,t)
        assert ans['after'].materialize()==reference(e,t+1)
        c['full_macro_small_controls']+=1
    # Iterate on changing fields without materialization in the tested code.
    for _ in range(32):
        e=State(frozenset(p for p in cells if rng.randrange(2)),(0,0),rng.randrange(4));x=SymbolicState.explicit(e)
        for _ in range(20):
            ans=next_stale_macro(x,8)
            if ans['kind']!='stale_read':break
            e=reference(e,ans['duration']);x=ans['after'];assert x.materialize()==e;c['composed_macros']+=1
    mature,w,ps=simulate(State(frozenset()),12000);_,word,_=simulate(mature,104)
    x=SymbolicState.explicit(mature)
    assert verify_period(x,word)['valid'];out=next_stale_macro(x,128)
    assert out['kind']=='permanent_no_stale';c['permanent_tail_controls']+=1
    # Huge exact endpoint: 10^12 periods are represented by finitely many terms.
    K=10**12
    points,_,d=geometry(mature,word);remote=(points[0][0]+K*d[0],points[0][1]+K*d[1])
    pert=SymbolicState.explicit(State(mature.black|{remote},mature.pos,mature.heading))
    ans=next_stale_macro(pert,128);assert ans['kind']=='stale_read';assert ans['event_time']==104*K
    direct=apply_periodic_prefix(pert,word,104*K)
    assert direct.pos==ans['before'].pos and direct.heading==ans['before'].heading
    def ray_colour_from_explicit(p,n):
        # Separate exact count of prescribed prefix reads at a chosen point.
        parity=int(p in mature.black or p==remote)
        for i,q in enumerate(points):
            dx=p[0]-q[0];dy=p[1]-q[1]
            if dx%d[0]==0 and dy%d[1]==0 and dx//d[0]==dy//d[1]:
                k=dx//d[0]
                if k>=0 and 104*k+i<n:parity^=1
        return bool(parity)
    probes=set(mature.black)|{remote}
    for k in (0,1,2,K//2,K-3,K-2,K-1,K,K+1):
        for q in points:
            probes.add((q[0]+k*d[0],q[1]+k*d[1]))
    for _ in range(200):probes.add((rng.randrange(-10**13,10**13),rng.randrange(-10**13,10**13)))
    for p in probes:
        expected=ray_colour_from_explicit(p,104*K)
        assert ans['before'].black(p)==direct.black(p)==expected
        assert ans['after'].black(p)==(expected^(p==remote));c['huge_endpoint_point_controls']+=1
    # Crucially the returned state is usable as the input to another exact macro.
    following=next_stale_macro(ans['after'],128)
    assert following['kind'] in ('stale_read','permanent_no_stale')
    if following['kind']=='stale_read' and following['duration']<2000:
        y=ans['after']
        for _ in range(following['duration']):y,_=step(y)
        for p in probes|{y.pos,following['after'].pos}:
            assert y.black(p)==following['after'].black(p)
        assert (y.pos,y.heading)==(following['after'].pos,following['after'].heading)
    c['huge_successor_reused']=1
    encoded=state_data(ans['after'])
    assert state_from_data(json.loads(json.dumps(encoded)))==ans['after']
    c['serialization_roundtrips']=1
    e=State(frozenset());batch=event_prefix(SymbolicState.explicit(e),8,20)
    assert batch['kind']=='event_budget_reached' and len(batch['events'])==20
    assert batch['state'].materialize()==reference(e,batch['elapsed'])
    c['event_prefix_driver_checks']=1
    assert event_prefix(x,128,1)['kind']=='permanent_no_stale'
    assert event_prefix(x,128,1,max_suffix_states=0)['kind']=='inconclusive'
    endpoint_sha=hashlib.sha256(json.dumps(encoded,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    recipe={'schema':'langtons-ant-symbolic-huge-recipe-v1','blank_updates':12000,
            'blank_initial_heading':0,'D':128,'remote_period_offset':K,
            'remote_cell':list(remote),'event_time':ans['event_time'],
            'endpoint_encoding_sha256':endpoint_sha,
            'endpoint_encoding':'state_data(after), JSON sort_keys=True separators=(comma,colon)',
            'next_event_duration':following.get('duration'),
            'scope':'Finite exact symbolic prefix and its successor, not an infinite-run result.'}
    Path(__file__).with_name('huge_recipe.json').write_text(json.dumps(recipe,indent=2)+'\n')
    assert verify_period(x,word,max_residue_checks=0)['kind']=='inconclusive'
    assert next_stale_macro(x,128,max_suffix_states=0)['kind']=='inconclusive'
    try:ans['before'].materialize(1000)
    except ValueError:c['expansion_cap_controls']+=1
    else:raise AssertionError('enormous field should not materialize')
    report=dict(status='passed',counts=dict(c),huge=dict(event_time=ans['event_time'],
                explicit_updates=ans['explicit_updates'],source_terms=ans['source_terms'],
                target_terms=ans['target_terms'],next_kind=following['kind'],
                next_duration=following.get('duration'),
                max_segment_length=max(s.length for s in ans['after'].terms)),
                scope=dict(exact_complete_state_composition=True,finite_support_only=True,
                global_nonuniversality=False,global_HIGHWAY_decider=False,
                infinite_composition_termination_proved=False,third_party_review=False))
    Path(__file__).with_name('check_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
