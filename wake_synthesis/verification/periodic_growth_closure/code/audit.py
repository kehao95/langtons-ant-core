"""Independent exact checks for the proof in PROOF.md.

These do not prove an unbounded theorem by sampling. The residue table is a
complete finite local algebra kernel; unbounded rank/flow reductions are proved
in the document. No third-party audit module is imported here.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from itertools import product
from math import comb
from pathlib import Path
import json, random

MOVES=((0,1),(1,0),(0,-1),(-1,0))
STANDARD='RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR'

def chi(x,y): return 1 if (x+y)%2==0 else -1

def correction(h,c,S,f):
    return (-c*S,c*(S-f),-c*(S+2*f),c*(S+f))[h]

def primitive(f,x):
    if x>=0: return sum(f(j)+f(j+1) for j in range(x))
    return -sum(f(j)+f(j+1) for j in range(x,0))

def residue_local():
    checked=0
    for S,fl,f,fr in product(range(4),repeat=4):
        for c,h,delta in product((-1,1),range(4),(-1,1)):
            nh=(h+delta)%4; dx,dy=MOVES[nh]
            Sn,fn=(S+f+fr,fr) if dx==1 else (S-fl-f,fl) if dx==-1 else (S,f)
            change=delta*c*f+correction(nh,-c,Sn,fn)-correction(h,c,S,f)
            assert change == (4*c*f if delta==1 and h in (1,2) else 0)
            assert change%4==0
            checked+=1
    return checked

def monodromy():
    count=0
    for period in range(1,5):
        for bits in product(range(4),repeat=period):
            f=lambda x:bits[x%period]
            for a in (-period,period):
                for b in range(-3,4):
                    if (a+b)%2: continue
                    for x,y,h in product(range(-2,3),(-1,0,1),range(4)):
                        old=correction(h,chi(x,y),primitive(f,x),f(x))
                        new=correction(h,chi(x+a,y+b),primitive(f,x+a),f(x+a))
                        assert (new-old-2*sum(bits))%4==0
                        count+=1
    return count

def literal_field_checks():
    rng=random.Random(20261015);checks=0
    for _ in range(48):
        B={(rng.randrange(-30,31),rng.randrange(-30,31)) for _ in range(60)}
        x,y,h=rng.randrange(-5,6),rng.randrange(-5,6),rng.randrange(4)
        vals=tuple(rng.randrange(4) for _ in range(5));f=lambda n:vals[n%5]
        field=sum(chi(a,b)*f(a) for a,b in B)
        charge=(field+correction(h,chi(x,y),primitive(f,x),f(x)))%4
        for _ in range(128):
            delta=-1 if (x,y) in B else 1
            B.symmetric_difference_update({(x,y)});h=(h+delta)%4
            dx,dy=MOVES[h];x+=dx;y+=dy
            complete=sum(chi(a,b)*f(a) for a,b in B)
            assert (complete+correction(h,chi(x,y),primitive(f,x),f(x)))%4==charge
            checks+=1
    return checks

def odd_classes(word,h=0):
    x=y=0;points=[]
    for letter in word:
        points.append((x,y));h=(h+(1 if letter=='R' else -1))%4
        dx,dy=MOVES[h];x+=dx;y+=dy
    return points,(x,y),h

def stable(word,points,d):
    a,b=d;groups=defaultdict(list)
    for i,(x,y) in enumerate(points):
        if a:key=(b*x-a*y,x%abs(a));q=x//a
        else:key=(x,y%abs(b));q=y//b
        groups[key].append((i-len(word)*q,i,(x,y)))
    wake=[]
    for vals in groups.values():
        vals.sort()
        assert all(word[i]==('R' if k%2==0 else 'L') for k,(_,i,_) in enumerate(vals))
        if len(vals)%2:wake.append(vals[0][2])
    return wake

def standard_checks():
    total=0
    for mul in (1,2,3,4):
        w=STANDARD*mul
        for phase in range(104):
            v=w[phase:]+w[:phase]
            for h in range(4):
                ps,d,h1=odd_classes(v,h);assert h1==h and d!=(0,0)
                O=stable(v,ps,d);g=len(O)
                assert g==12*mul and g>=8 and g%4==0
                assert g>=2*max(map(abs,d))
                for axis,a in enumerate(d):
                    sums=Counter()
                    if a:
                        for q in O:sums[q[axis]%abs(a)]+=chi(*q)
                        assert all(sums[r]%4==2 for r in range(abs(a)))
                    else:
                        for q in O:sums[q[axis]]+=chi(*q)
                        assert all(n%4==0 for n in sums.values())
                if mul==1: assert len({chi(*q) for q in O})==2
                total+=1
    return total

def inversion(seq):
    return sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))%2

def axis_independent():
    # Generate step-sign lists directly, not the imported four-letter macros.
    counts={}
    for M in (2,4,6,8):
        tested=0
        for us in product((-1,1),repeat=M):
            if sum(us)!=2:continue
            for vs0 in product((-1,1),repeat=M-1):
                vs=vs0+(1,)
                if sum(vs):continue
                vprev=1;x=y=0;poses=[];letters=[];ports=[]
                for u,v in zip(us,vs):
                    poses.append((x,y));letters.append(int(u!=vprev));ports.append((int(vprev>0),int(u>0)))
                    x+=u
                    poses.append((x,y));letters.append(int(u==v));ports.append((int(u>0),int(v>0)))
                    y+=v;vprev=v
                assert (x,y)==(2,0)
                groups=defaultdict(list)
                for i,(x,y) in enumerate(poses):groups[(y,i%2)].append(i)
                rank={};I=0;linear=0;binomials=0;rowbin=0
                for key,seq in groups.items():
                    seq.sort(key=lambda i:(-poses[i][0],i));m=len(seq)
                    al=[ports[i][0] for i in seq];be=[ports[i][1] for i in seq]
                    rank.update({i:k for k,i in enumerate(seq)})
                    A,B=sum(al),sum(be)
                    I^=inversion(al)^inversion(be)
                    linear^=((A+B)*(m-1))%2
                    binomials^=(comb(A,2)+comb(B,2))%2
                    if key[1]:rowbin^=comb(m,2)%2
                K=sum(rank[i] for i,b in enumerate(letters) if b)%2
                assert not linear and not binomials
                assert K==(I^rowbin)==(1+M//2)%2
                inlist=[];outlist=[]
                for key in sorted(groups):
                    seq=groups[key]
                    inlist.extend(sorted(seq,key=lambda i:(ports[i][0],rank[i])))
                    outlist.extend(sorted(seq,key=lambda i:(ports[i][1],rank[i])))
                where={i:k for k,i in enumerate(inlist)}
                E=inversion([where[(i+1)%(2*M)] for i in outlist])
                assert I^E==1
                tested+=1
        counts[2*M]=tested
    return counts

def block_coordinates(block):
    kind,t,r=block;direction={'N':0,'E':1,'S':2,'W':3}[kind]
    p=(r,t-r);d=MOVES[direction];q=(p[0]+d[0],p[1]+d[1])
    sign=int(kind in 'EN')
    return (t,r,sign),(q[0]+q[1],q[0]%2,sign)

def blocksign(blocks):
    source=sorted(blocks,key=lambda b:block_coordinates(b)[0])
    target=sorted(blocks,key=lambda b:block_coordinates(b)[1]);positions={b:i for i,b in enumerate(target)}
    permutation=[positions[b]for b in source];seen=set();cycles=0
    for i in range(len(permutation)):
        if i in seen:continue
        cycles+=1;j=i
        while j not in seen:seen.add(j);j=permutation[j]
    return (len(permutation)-cycles)%2

def gadget(t,r):
    return {('N',t,r),('S',t+2,r),('W',t+1,1-r),('E',t+1,1-r)}

def ladder_checks():
    pairs=[]
    for r,s,diff in product(range(2),range(2),range(-6,7,2)):
        if r==s and diff==0:continue
        a,b=gadget(1,r),gadget(1+diff,s)
        assert not(a&b) and blocksign(a)==blocksign(b)==1
        cross=blocksign(a|b)^blocksign(a)^blocksign(b)
        assert cross==int(r==s and abs(diff)==2)
        pairs.append([r,s,diff,cross])
    checks=0
    for flat in product((0,1),repeat=12):
        blocks=set();runs=[];odds=[]
        for r in range(2):
            bits=flat[6*r:6*r+6];padded=(0,)+bits+(0,)
            runs.append(sum(padded[i]==0 and padded[i+1]==1 for i in range(6)))
            odds.append(sum(padded[i]!=padded[i+1] for i in range(7)))
            for j,bit in enumerate(bits):
                if bit:blocks.update(gadget(1+2*j,r))
        assert odds==[2*n for n in runs]
        assert blocksign(blocks)==sum(runs)%2==sum(comb(n,2)for n in odds)%2
        checks+=1
    return {'pair_table':pairs,'finite_binary_chains':checks}

def arithmetic():
    axis=[]
    for P,g in product(range(4,257,4),range(4,257,4)):
        if g>P:continue
        if (1+P//4)%2!=((P-g)//2)%2:continue
        if (P//2+2+g//2)%4:continue
        assert P%8==4 and g%8==0
        axis.append([P,g])
    pure=0
    for u,v in product(range(2,129,4),repeat=2):
        assert (comb(u,2)+comb(v,2))%2==0
        pure+=1
    matrices={}
    for g in (4,8):
        entries=[]
        for a,b,c in product(range(g+1),repeat=3):
            d=g-a-b-c
            if d<0:continue
            if all(z%4==2 for z in (a-b,d-c,a-c,d-b)):
                entries.append({'matrix':[[a,b],[c,d]],'checker_pure':not(b+c)or not(a+d)})
        matrices[g]=entries
    assert len(matrices[4])==2 and all(x['checker_pure'] for x in matrices[4])
    assert len(matrices[8])==10 and sum(not x['checker_pure'] for x in matrices[8])==6
    drifts=[(a,b) for a,b in product(range(-2,3),repeat=2) if (a or b) and (a+b)%2==0]
    assert len(drifts)==12
    counts=Counter('axis2' if a*b==0 else 'unit' if abs(a)==1 else 'diagonal2' for a,b in drifts)
    assert counts=={'axis2':4,'unit':4,'diagonal2':4}
    # No inference of impossibility from these finite ranges is needed: the
    # displayed modular arguments in the proof cover all positive integers.
    return {'axis_residue_pairs':len(axis),'pure_lane_pairs':pure,'g4_drift_partition':dict(counts),'residue_matrices':matrices}

def main():
    if not __debug__:raise RuntimeError('Assertions must remain enabled')
    report={'status':'passed','local_mod4_identities':residue_local(),
            'monodromy_instances':monodromy(),'literal_full_field_steps':literal_field_checks(),
            'standard_phases_rotations_powers':standard_checks(),
            'independent_axis_words':axis_independent(),'ladder':ladder_checks(),
            'arithmetic':arithmetic(),
            'boundary':'Finite exact checks plus complete written algebra; not an all-seed HC proof or Lean formalization.'}
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
