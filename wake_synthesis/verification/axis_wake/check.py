"""Scoped deterministic regression tests for the analytic axis-wake theorem."""
from __future__ import annotations
import json
import random
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
from axis_wake import (DIR, closed_masks, edge, edge_character, endpoint,
    horizontal, literal_graph, normalize, prefilters, row_cycle, run_character,
    screen, staircase, vertical)


def short_words():
    totals={}; stable=0
    for P in (4,8,12,16):
        count=0
        for mask in range(1<<P):
            p=(0,0); h=0; events=[]
            for i in range(P):
                left=(mask>>i)&1
                nh=(h+1-2*left)%4
                events.append((p,h,nh,left))
                dx,dy=DIR[nh]; p=(p[0]+dx,p[1]+dy); h=nh
            if h or p[1] or p[0]<=0: continue
            a=p[0]
            assert a%2==0
            groups=defaultdict(list); counts=Counter()
            for i,(p,h,nh,left) in enumerate(events):
                v=(p[0]%a,p[1]); k=(p[0]-v[0])//a
                groups[v].append((i-P*k,h,nh,left))
                counts[edge(a,p,nh)]+=1
            I=K=L=0; alternating=True
            for v, visits in groups.items():
                visits.sort()
                alpha=[int(h in (0,1)) for tau,h,nh,left in visits]
                beta=[int(nh in (0,1)) for tau,h,nh,left in visits]
                I+=sum(A[i]>A[j] for A in (alpha,beta)
                       for i in range(len(A)) for j in range(i+1,len(A)))
                K+=sum(k for k,(_,h,nh,left) in enumerate(visits) if left)
                m=len(visits); pv=(sum(alpha)+sum(beta))%2
                L+=pv*(m-1)+(sum(v)%2)*(m*(m-1)//2)
                alternating &= all(left==k%2 for k,(_,h,nh,left) in enumerate(visits))
            G={e for e,n in counts.items() if n%2}
            E=edge_character(G,set())["edge_sign"]
            assert (I+E)%2==1
            assert (K-I-L)%2==0
            if alternating:
                O={v for v,xs in groups.items() if len(xs)%2}
                assert screen(a,O)["status"]=="NOT_EXCLUDED"
                stable+=1
            count+=1
        totals[str(P)]=count
    return {"by_period":totals,"total":sum(totals.values()),"stable_realizable":stable}


def four_level(heights):
    y0,y1,y2,y3=heights
    return {(0,y2),(0,y3),(1,y1),(1,y2),(2,y0),(2,y1),(3,y0),(3,y3)}


def check():
    rng=random.Random(20261029)
    out={"schema":"axis-wake-reconstruction-check-v1"}
    windows={}
    for a,H in ((4,4),(2,6),(6,4)):
        n=0
        for O in closed_masks(a,H):
            q=endpoint(a,O)["seam_zero_character"]
            assert edge_character(literal_graph(a,O),O)["character"]==q
            n+=1
        windows[f"{a}x{H}"]=n
    out["all_even_fiber_windows"]=windows
    out["short_word_factorization"]=short_words()
    counts=Counter()
    for a in (2,4,6,8):
        for _ in range(100):
            O=set()
            for j in range(6):
                xs=rng.sample(range(a),2); ys=rng.sample(range(-4,7),2)
                O.symmetric_difference_update(product(xs,ys))
            G=literal_graph(a,O); q=endpoint(a,O)["seam_zero_character"]
            assert edge_character(G,O)["character"]==q
            assert run_character(a,O)["character"]==q
            counts["three_way_comparisons"]+=1
            rev={(t,(h+2)%4,s) for s,h,t in G}
            assert edge_character(rev,O,sector=1)["character"]==q
            counts["checker_reversals"]+=1
            vertices=list({p for s,h,t in G for p in (s,t)})
            rng.shuffle(vertices); order={p:i for i,p in enumerate(vertices)}
            assert edge_character(G,O,order=order)["character"]==q
            counts["vertex_orders"]+=1
            for y in (-5,0,7):
                assert edge_character(G^row_cycle(a,y),O)["character"]==1-q
                counts["row_cycle_toggles"]+=1
            dx,dy=rng.randint(-12,12),rng.randint(-7,7)
            moved=normalize(a,[(x+dx,y+dy) for x,y in O])
            assert endpoint(a,moved)["seam_zero_character"]==q
            counts["translations"]+=1
        R=row_cycle(a,0); er=edge_character(R,set())["edge_sign"]
        assert edge_character(R,set())["character"]==1
        for x in range(a):
            for y in range(-2,3):
                for e in (horizontal(a,x,y),vertical(a,x,y)):
                    assert (edge_character(R^{e},set())["edge_sign"]+er)%2==0
                    counts["radical_basis_checks"]+=1
    out["random_and_basis_controls"]=dict(counts)
    count=0
    for ds in product((2,4,6,8,10,12),repeat=3):
        heights=[-6]
        for d in ds: heights.append(heights[-1]+d)
        O=four_level(heights); delta=heights[-1]-heights[0]
        ep=endpoint(4,O); rr=run_character(4,O)
        assert not prefilters(4,O)
        assert ep["strict_inversions"]==15 and rr["character"]==1
        assert rr["edges"]==2*delta+6 and rr["positive_edges"]==delta+4
        assert rr["pair_counts"]=={"HH":1,"HV":10,"VV":2*delta-2}
        count+=1
    out["four_level_gap_controls"]=count
    count=0
    for a in range(2,25,2):
        for _ in range(5):
            heights=[-20]
            for i in range(1,a): heights.append(heights[-1]+2*rng.randint(1,10))
            O=staircase(a,heights)
            assert not prefilters(a,O)
            assert endpoint(a,O)["strict_inversions"]==2*a-3
            assert edge_character(literal_graph(a,O),O)["character"]==1
            assert run_character(a,O)["character"]==1
            count+=1
    out["staircase_controls"]=count
    contrast={(x,y) for x in range(4) for y in (0,20)}
    assert screen(4,contrast)["status"]=="NOT_EXCLUDED"
    out["passing_contrast"]=screen(4,contrast)
    huge=1<<1000
    O=four_level((-huge,0,huge+2,3*huge+8))
    assert not prefilters(4,O)
    rr=run_character(4,O)
    assert rr["character"]==endpoint(4,O)["seam_zero_character"]==1
    out["large_coordinate_control"]={"max_coordinate_bits":max(abs(y).bit_length() for x,y in O),
                                   "runs":rr["runs"],"strict_inversions":15}
    count=0
    for m in (2,4,6,8):
        for ys in combinations(range(10),m):
            O=set(product(range(2),ys)); ep=endpoint(2,O)
            assert ep["strict_inversions"]==m*(m-1)//2
            assert ep["seam_zero_character"]==m//2%2
            count+=1
    out["two_column_controls"]=count
    # Sharp scope / bad-input controls. These deliberately do not claim sufficiency.
    assert screen(1<<1000,[(0,0),(1,0),(0,1),(1,1)])["status"].startswith("EXCLUDED_BY_ESTABLISHED")
    assert screen(3,[(0,0),(1,0)])["status"].startswith("EXCLUDED_BY_ESTABLISHED")
    try: endpoint(4,[(0,0)])
    except ValueError: pass
    else: raise AssertionError("Uneven fiber was not rejected")
    witness=staircase(4,[0,10,20,30])
    assert screen(4,witness)["status"]=="EXCLUDED_BY_AXIS_WAKE_PARITY"
    assert endpoint(4,witness)["strict_inversions"]==5
    # Corrupt-character control must disagree with independently constructed graph.
    assert (endpoint(4,witness)["seam_zero_character"]^1)!=edge_character(literal_graph(4,witness),witness)["character"]
    out["scope_controls"]=5
    out["example"]={"wake":sorted(witness),**screen(4,witness)}
    return out


if __name__=="__main__":
    print(json.dumps(check(),indent=2,sort_keys=True))
