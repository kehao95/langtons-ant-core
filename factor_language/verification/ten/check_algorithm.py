"""Scoped exact controls of the new reachability decision algorithm."""
from __future__ import annotations
import hashlib, json, random
from pathlib import Path
import algorithm as a
import kernel as k
r=k.r
ROOT=Path(__file__).resolve().parent

def brute_event(B,p,h,limit):
    B=set(B);hist=a.intrinsic_history(B,p,h)
    for t in range(limit):
        c='L' if p in B else 'R'
        if hist+c not in a.ALLOWED:return t
        p,h,c=r.step_cells(B,p,h);hist=(hist+c)[-9:]
    return None

def main():
    wit=k.load_witness(ROOT/'certificates');rng=random.Random(20261015)
    counts={'inverse_pairs':0,'mature_phases_rotations':0,'finite_sharp_family':0,'random_inputs':0,'far_marker_literal_steps':0}
    for _ in range(600):
        B={(rng.randrange(-8,9),rng.randrange(-8,9)) for j in range(rng.randrange(30))}
        p=(rng.randrange(-5,6),rng.randrange(-5,6));h=rng.randrange(4);b=set(B)
        q,g,c=r.step_cells(b,p,h);q,g,d=a.inverse(b,q,g)
        assert (b,q,g,d)==(B,p,h,c);counts['inverse_pairs']+=1
    # Recover the complete mature actual state, not a hypothetical periodic past.
    for ph in range(104):
        w=r.W[ph:]+r.W[:ph];rec=r.periodic_recipe(w);B=set(map(tuple,rec['points']));p=(0,0);h=0
        for _ in range(20):p,h,c=r.step_cells(B,p,h)
        for g in range(4):
            b={r.rotate(q,g) for q in B};q=r.rotate(p,g);hh=(h+g)%4
            out=a.decide_future_defect(b,q,hh)
            assert not out['event_exists'] and out['main_updates']<=12*len(b)+221
            counts['mature_phases_rotations']+=1
    for n in range(31):
        B=k.family(n,wit);out=a.decide_future_defect(B,intrinsic=False)
        assert not out['event_exists']
        tau=max(0,24*n-3);p=(0,0);h=0;b=set(B)
        for _ in range(tau):p,h,c=r.step_cells(b,p,h)
        assert a.permanent_phase(b,p,h) is not None
        if tau:
            p,h,c=a.inverse(b,p,h)
            assert a.permanent_phase(b,p,h) is None
        counts['finite_sharp_family']+=1
    for _ in range(400):
        B={(rng.randrange(-9,10),rng.randrange(-9,10)) for j in range(rng.randrange(50))}
        p=(rng.randrange(-5,6),rng.randrange(-5,6));h=rng.randrange(4)
        out=a.decide_future_defect(B,p,h)
        t=brute_event(B,p,h,12*len(B)+222)
        if out['kind']=='observed':assert t==out['first_event_update']
        elif not out['event_exists']:assert t is None
        assert out['main_updates']<=12*len(B)+221
        counts['random_inputs']+=1
    marker=json.loads((ROOT/'certificates/far_marker.json').read_text())
    seed=set(map(tuple,marker['seed']));word=marker['word'];d=tuple(marker['drift']);base=tuple(marker['base'])
    assert len(seed)==27 and a.permanent_phase(seed,(0,0),0) is not None
    assert len(a.intrinsic_history(seed,(0,0),0))==9
    positions,drift,_,dh=r.geometry(word);assert drift==d and dh==0
    candidates=[]
    for i,q in enumerate(positions):
        s=r.multiple((q[0]-base[0],q[1]-base[1]),d)
        if s is not None:candidates.append((i-104*s,s,i))
    off,level,ph=min(candidates)
    assert off==marker['first_contact_offset']==-92 and ph==marker['contact_phase']==12
    assert all(20-s>=0 for _,s,_ in candidates)
    assert word[ph]=='R'
    fact=''.join(word[(ph-j)%104] for j in range(9,0,-1))+'L'
    assert fact==marker['bad_factor'] and fact not in a.ALLOWED
    assert all(max(abs(x),abs(y))<20 for x,y in seed)
    cases=[]
    for n in (20,30,10**12):
        point=base[0]+n*d[0],base[1]+n*d[1];B=seed|{point};out=a.decide_future_defect(B)
        assert len(B)==28 and out['kind']=='forced_future' and out['main_updates']==548
        exact=104*n-92
        if n<100:
            assert brute_event(B,(0,0),0,exact+1)==exact
            counts['far_marker_literal_steps']+=exact+1
        cases.append({'n':n,'exact_first_event':exact,'main_updates':out['main_updates'],'decision':out['kind']})
    return {'status':'passed','counts':counts,'far_markers':cases,'scope':'Reachability YES/NO, not a general first-event-time or HIGHWAY decider','all_parameter_proofs':'PROOF.md','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'algorithm.py',ROOT/'check_algorithm.py')}}

if __name__=='__main__':print(json.dumps(main(),indent=2))
