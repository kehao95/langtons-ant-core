"""Mixed-checker wake parity, full drift (2,-2), classical LR ant.

This is a NECESSARY test only. A passing input is NOT_EXCLUDED, never a
realizable highway. No period or width bound is used in the production test.
The layer/edge reconstruction is an independent, finite-span audit routine.
"""
from __future__ import annotations
from collections import Counter
from itertools import product


def validate(wake, sigma=1):
    if type(sigma) is not int or sigma not in (-1, 1):
        raise ValueError('sigma must be +1 or -1')
    items=tuple(wake)
    if any(not isinstance(p,(tuple,list)) or len(p)!=2 or type(p[0]) is not int
           or type(p[1]) is not int or p[1] not in (0,1) for p in items):
        raise ValueError('use integer full classes (t=x+y,r=x mod 2)')
    items=tuple((p[0],p[1]) for p in items)
    if len(set(items))!=len(items):raise ValueError('duplicate full drift class')
    # Translation by (0,1) flips sigma and t parity without altering x residue.
    return frozenset((t+(sigma==-1),r) for t,r in items)


def counts(wake):
    return tuple(sum((t%2,r)==(p,s) for t,r in wake)
                 for p,s in ((0,0),(0,1),(1,0),(1,1)))


def residue_ok(wake):
    q0,q1,c0,c1=counts(wake)
    return all(x%4==2 for x in (q0-c0,q1-c1,q0-c1,q1-c0))


def parity_screen(wake, sigma=1, drift=(2,-2)):
    """O(g log g) integer algorithm, independent of transverse coordinate size."""
    if tuple(drift)!=(2,-2):
        raise ValueError("unsupported full drift; rotate first, do not divide by gcd")
    O=validate(wake,sigma);g=len(O)
    if not O or g%4 or not residue_ok(O):
        return {'status':'EXCLUDED','reason':'growth_or_signed_residues','growth':g}
    layers=Counter(t for t,r in O)
    prefix_vertical=0;inversions=0
    for t,m in sorted(layers.items()):
        if t%2==0:prefix_vertical+=m
        else:inversions+=prefix_vertical*m
    assert prefix_vertical%2==0
    index=(inversions+prefix_vertical//2)%2
    return {'status':'NOT_EXCLUDED' if index==1 else 'EXCLUDED',
            'reason':'mixed_wake_rank_parity','growth':g,
            'vertical_odd_classes':prefix_vertical,'horizontal_odd_classes':g-prefix_vertical,
            'ordered_vertical_horizontal_pairs':inversions,
            'required_parity':1,'actual_parity':index,
            'normalized_residue_counts_Q0_Q1_C0_C1':list(counts(O))}


def edge_target(edge):
    t,r,positive=edge
    return (t+(1 if positive else -1),1-r if t%2==0 else r,positive)


def layer_reconstruction(wake):
    """Independent full layer algebra. May be slow for enormous coordinate gaps.
    The public screen above does NOT expand those gaps.
    """
    O=validate(wake)
    if not O:return {'closed':True,'E':0,'L':0,'combined':0}
    lo=min(t for t,r in O)-4;lo-=lo%2
    hi=max(t for t,r in O)+4;hi+=hi%2
    if hi-lo>100000:raise ValueError('audit span too large; no negative verdict')
    n={};e={};edges=set();L=0
    for t in range(lo,hi+1,2):
        for r in (0,1):
            Q=int((t,r) in O);C=int((t+1,r) in O)
            n[t+1,r]=n.get((t-1,r),0)^Q^C
            e[t,r]=e.get((t-2,r),0)^int((t-1,1-r) in O)^Q
            if e[t,r]:edges.add((t,r,1))
            if e[t,r]^Q:edges.add((t,r,0))
            if n[t+1,r]:edges.add((t+1,r,1))
            if n[t+1,r]^C:edges.add((t+1,r,0))
    closed=not any(n[hi+1,r] or e[hi,r] for r in (0,1))
    if not closed:return {'closed':False}
    for t in range(lo,hi+1,2):
        for r in (0,1):
            Q=int((t,r) in O);C=int((t+1,r) in O)
            pQ=n.get((t-1,r),0)^e[t,r]
            pC=e[t,1-r]^n[t+1,r]
            L^=pQ*(1^Q)^C*(1^pC)
    ordered=sorted(edges);E=0
    for i,a in enumerate(ordered):
        for b in ordered[i+1:]:E^=edge_target(a)>edge_target(b)
    return {'closed':True,'E':E,'L':L,'combined':E^L,'odd_directed_blocks':len(edges)}


def same_layer(parity,b):
    w0,e0,w1,e1=b
    return (w0*w1 ^ e0*w1 ^ e0*e1) if parity==0 else e0*w1


def adjacent(a,b):return (a[1]^a[3])*(b[0]^b[2])


def distance_two(parity,a,b):
    return (a[1]*(b[0]^b[2]) ^ a[3]*b[2]) if parity==0 else (a[1]*b[0] ^ a[3]*(b[0]^b[2]))


def H(state):
    e0,e1,c0,c1,q=state
    return e0^e1^q^(e0*c1)^(e1*c0)^(e1*c1)^(e1*q)^(c0*c1)^(c0*q)


def kernel_step(state,letters):
    """One Q/C layer pair; every variable is a bit. Full 512-case identity."""
    e0,e1,c0,c1,q=state;Q0,Q1,C0,C1=letters
    n0=e1^q^c0;n1=e0^q^c1
    E0=e0^Q0^c1;E1=e1^Q1^c0
    N0=n0^Q0^C0;N1=n1^Q1^C1
    # Only the positive old-Q counts enter distance-two inversions.
    oldQ=(0,e0,0,e1);oldC=(n0^c0,n0,n1^c1,n1)
    newQ=(E0^Q0,E0,E1^Q1,E1);newC=(N0^C0,N0,N1^C1,N1)
    E=(same_layer(0,newQ)^same_layer(1,newC)^adjacent(oldC,newQ)
       ^distance_two(0,oldQ,newQ)^adjacent(newQ,newC)^distance_two(1,oldC,newC))
    L=(n0^E0)*(1^Q0) ^ (n1^E1)*(1^Q1) ^ C0*(1^E1^N0) ^ C1*(1^E0^N1)
    I=(q^Q0^Q1)*(C0^C1)
    allbits=(Q0,Q1,C0,C1)
    B=(n0^n1)*(Q0^Q1^C0^C1)
    for i in range(4):
        for j in range(i+1,4):B^=allbits[i]*allbits[j]
    correction=E^L^I^B^Q0
    target=(E0,E1,C0,C1,q^Q0^Q1)
    return target,correction


def paired_family(levels,q_lane=0,c_lane=0):
    """Two full extreme C layers and four separate internal singleton layers."""
    if type(q_lane) is not int or type(c_lane) is not int or q_lane not in (0,1) or c_lane not in (0,1):
        raise ValueError('invalid lane')
    lo,hi,internals=levels
    if not (lo<hi and lo%2==hi%2==1 and len(internals)==4
            and lo<min(internals) and max(internals)<hi and len(set(internals))==4):
        raise ValueError('invalid extreme/interior levels')
    qs=sorted(t for t in internals if t%2==0);cs=sorted(t for t in internals if t%2)
    if len(qs)!=2 or len(cs)!=2:raise ValueError('need two Q and two C levels')
    return {(lo,0),(lo,1),(hi,0),(hi,1),(qs[0],q_lane),(qs[1],1-q_lane),
            (cs[0],c_lane),(cs[1],1-c_lane)}
