"""Adversarial and positive controls for the certificate machinery.
These finite tests are not the proof of the universal extraction lemma.
"""
from __future__ import annotations
from pathlib import Path
from collections import defaultdict,Counter
import json, random, copy, hashlib
import obstruction as O
import verify_certificate as V

STANDARD='RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR'
SEED={(-7,0),(-7,1),(-6,-3),(-6,-2),(-6,-1),(-6,2),(-5,-2),(-5,0),(-5,1),(-5,2),(-4,-2),(-4,1),(-3,-3),(-3,1),(-2,-3),(-2,-1),(-2,1),(-1,-2),(-1,0)}

def built_graph(P,phase_to_lift,phase_to_label,cuts):
    """Assign ranks by actual lifted integer times, independently of O's solver."""
    group=defaultdict(list)
    for i,z in phase_to_lift.items():group[phase_to_label[i]].append((i-P*z,i,z))
    phases={};g=[];time=[]
    for label,entries in sorted(group.items()):
        entries.sort()
        assert all(b[0]-a[0]>=4 for a,b in zip(entries,entries[1:]))
        for k,(tau,i,z)in enumerate(entries):
            phases[i]=len(g);g.append(O.Node(label,k,0,0,0));time.append(tau)
    for i,u in phases.items():
        j=(i+1)%P
        if j in phases and i not in cuts:
            v=phases[j];delta=phase_to_lift[j]-phase_to_lift[i]+int(j==0)
            O.attach(g,u,v,delta)
            assert time[v]-time[u]==1-P*delta
    parts,closed=O.split_chains(g)
    assert closed is None
    assert O.affine_cycle(g,parts) is None
    return g

def positive_controls():
    rng=random.Random(151043)
    # Abstract periodic embeddings, some phases not built, both possible even P residues.
    abstract=0;odd_half=0
    for _ in range(5000):
        P=2*rng.randrange(3,50)
        selected=sorted(rng.sample(range(P),rng.randrange(2,P)))
        lift={};labels={}
        for i in selected:
            if P%4==0:
                labels[i]=4*rng.randrange(4)+i%4;lift[i]=rng.randrange(-8,9)
            else:
                labels[i]=2*rng.randrange(4)+i%2
                lift[i]=2*rng.randrange(-4,5)+((i-i%2)//2)%2
        cuts={i for i in selected if rng.randrange(5)==0}
        built_graph(P,lift,labels,cuts);abstract+=1;odd_half+=P%4==2
    # Actual standard word, full translation classes for drift (2,-2).
    # Only the general time-constraint routine is tested; the one-lane premise is NOT imposed.
    actual=0
    for phase in range(104):
        w=STANDARD[phase:]+STANDARD[:phase];x=y=0;h=1;points=[]
        for letter in w:
            points.append((x,y));h=(h+(1 if letter=='R'else-1))%4;dx,dy=V.VECTORS[h];x+=dx;y+=dy
        assert h==1 and abs(x)==abs(y)==2
        dx,dy=x,y
        # Complete class key and a coordinate along full drift, not primitive drift.
        group={};labels={};lift={}
        for i,(x,y) in enumerate(points):
            key=(dy*x-dx*y,x%abs(dx))
            if key not in group:group[key]=len(group)
            labels[i]=group[key];lift[i]=x//dx
        for _ in range(20):
            chosen=set(rng.sample(range(104),rng.randrange(5,104)))
            built_graph(104,{i:lift[i]for i in chosen},{i:labels[i]for i in chosen},
                        {i for i in chosen if rng.randrange(6)==0})
            actual+=1
    return abstract,odd_half,actual

def permanent(seed,word,heading):
    positions=[];x=y=0;h=heading
    for letter in word:
        positions.append((x,y));h=(h+(1 if letter=='R' else -1))%4
        dx,dy=V.VECTORS[h];x+=dx;y+=dy
    drift=(x,y)
    if h!=heading or drift==(0,0):return False
    def multiple(v):
        a,b=drift
        if a:
            if v[0]%a:return None
            k=v[0]//a
            return k if v[1]==k*b else None
        if v[0] or v[1]%b:return None
        return v[1]//b
    for i,p in enumerate(positions):
        thresholds=[];hits=set()
        for j,q in enumerate(positions):
            k=multiple((q[0]-p[0],q[1]-p[1]))
            if k is not None and (k>0 or k==0 and j<i):thresholds.append(k)
        for q in seed:
            k=multiple((q[0]-p[0],q[1]-p[1]))
            if k is not None and k>=0:hits.add(k)
        for k in {0,*thresholds,*hits,*(v+1 for v in hits)}:
            if ((k in hits)+sum(v<=k for v in thresholds))%2!=(word[i]=='L'):return False
    return True

def literal_controls():
    b=set(SEED);x=y=0;h=1
    forever=0
    for phase,letter in enumerate(STANDARD):
        w=STANDARD[phase:]+STANDARD[:phase]
        assert permanent({(u-x,v-y)for u,v in b},w,h);forever+=1
        b.symmetric_difference_update({(x,y)});h=(h+(1 if letter=='R'else-1))%4
        dx,dy=V.VECTORS[h];x+=dx;y+=dy
    assert not permanent(SEED|{(2*10**20,-2*10**20)},STANDARD,1)
    for r in range(4):
        def rot(q):
            x,y=q
            for _ in range(r):x,y=y,-x
            return x,y
        assert permanent({rot(q)for q in SEED},STANDARD,(1+r)%4)
    b=set(SEED);x=y=0;h=1
    for letter in STANDARD*100:
        assert ((x,y)in b)==(letter=='L');b.symmetric_difference_update({(x,y)})
        h=(h+(1 if letter=='R'else-1))%4;dx,dy=V.VECTORS[h];x+=dx;y+=dy
    assert (x,y,h)==(200,-200,1)
    w='RLRRRRLLR';positions=[];h=0;x=y=0
    for letter in w:
        positions.append((x,y));h=(h+(1 if letter=='R'else-1))%4;dx,dy=V.VECTORS[h];x+=dx;y+=dy
    assert positions[0]==positions[8] and positions[0]not in positions[1:8]
    # Every assignment of initially read colors fails the prescribed nine-letter factor.
    cells=sorted(set(positions));count=0
    for mask in range(1<<len(cells)):
        field={q for k,q in enumerate(cells)if mask>>k&1};x=y=0;h=0
        for c in w:
            black=(x,y)in field
            if black!=(c=='L'):break
            field.symmetric_difference_update({(x,y)});h=(h+(-1 if black else 1))%4
            dx,dy=V.VECTORS[h];x+=dx;y+=dy
        else:raise AssertionError('Forbidden factor realized')
        count+=1
    return {'standard_literal_steps':10400,'standard_infinite_phases':forever,'standard_rotations':4,'far_blocker_epoch':10**20,'forbidden_factor_assignments':count,
            'forbidden_factor_positions':positions}

def corrupt_controls(cert):
    count=0
    def reject(obj):
        nonlocal count
        try:V.verify(obj)
        except (ValueError,IndexError,KeyError):count+=1
        else:raise AssertionError('Corrupt certificate accepted')
    c=copy.deepcopy(cert);c['records'].pop(0);reject(c)
    c=copy.deepcopy(cert);c['records'].append(c['records'][0]);reject(c)
    c=copy.deepcopy(cert);next(r for r in c['records']if r['kind']=='order')['coefficient']+=1;reject(c)
    c=copy.deepcopy(cert);next(r for r in c['records']if r['kind']=='order')['pairs'][0][1]=0;reject(c)
    c=copy.deepcopy(cert);next(r for r in c['records']if r['kind']=='closed')['nodes']=[0];reject(c)
    c=copy.deepcopy(cert);next(r for r in c['records']if r['kind']=='read')['word']='R';reject(c)
    c=copy.deepcopy(cert);next(r for r in c['records']if r['kind']=='read')['kind']='expand';reject(c)
    return count

def main(path):
    cert=json.loads(path.read_text());a,b,c=positive_controls();literal=literal_controls()
    report={'status':'passed','abstract_valid_partial_cycles':a,'period_2_mod_4_controls':b,
            'actual_standard_partial_cycles':c,'corrupt_certificates_rejected':corrupt_controls(cert),**literal}
    print(json.dumps(report,indent=2));return report

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('certificate',type=Path);p.add_argument('--report',type=Path);a=p.parse_args()
    result=main(a.certificate)
    if a.report:a.report.write_text(json.dumps(result,indent=2)+'\n')
