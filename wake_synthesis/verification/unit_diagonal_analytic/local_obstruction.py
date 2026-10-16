"""Period-free, width-free local obstruction for drift (1,-1).

Independent row-at-a-time implementation: it constructs a full port graph anew
for each candidate, never calls the C++ enumerator, and never supplies a period.
An interrupted enumeration does not produce a theorem certificate.
"""
from __future__ import annotations
from itertools import combinations
from collections import Counter
import json,hashlib

# Rows are top first. Bits mean arrival from the already built, upper side.
def departures(t:int,a:tuple[int,...])->tuple[int,...]:
    return tuple((b^(k%2)) ^ (t%2) for k,b in enumerate(a))

def candidates(t:int,I:int,J:int):
    """All finite arrival words with odd indicator 0 or 1 and these port counts."""
    for o in (0,1):
        for ae in range(I+1):
            n=2*(I+J-2*ae)+o if t%2==0 else 2*(J-I+2*ae)-o
            ao=I-ae
            if n<0 or ae>(n+1)//2 or not 0<=ao<=n//2:continue
            if n-J<0 or n-I<0 or n-J==0:continue  # a deeper visited layer is required
            for even in combinations(range(0,n,2),ae):
                for odd in combinations(range(1,n,2),ao):
                    ones=set(even+odd)
                    a=tuple(int(k in ones) for k in range(n))
                    assert sum(a)==I and sum(departures(t,a))==J
                    yield a

def build(rows):
    """Build from literal geometric directed ports, paired in stable rank order."""
    nodes=[(t,k,a) for t,row in enumerate(rows) for k,a in enumerate(row)]
    ids={(t,k):i for i,(t,k,a) in enumerate(nodes)}
    nxt=[None]*len(nodes);prev=[None]*len(nodes);vol=[0]*len(nodes)
    ds=[departures(-t,row) for t,row in enumerate(rows)]
    def join(u,v,delta):
        assert nxt[u] is None and prev[v] is None
        nxt[u]=v;prev[v]=u;vol[u]=delta
    for t in range(1,len(rows)):
        # Upper -> lower. The upper vertex emits S on an even layer, W on odd.
        source=[ids[t-1,k] for k,d in enumerate(ds[t-1]) if d==0]
        target=[ids[t,k] for k,a in enumerate(rows[t]) if a==1]
        assert len(source)==len(target)
        for u,v in zip(source,target):join(u,v,-((t-1)%2))
        # Lower -> upper. The lower vertex emits N on an even layer, E on odd.
        source=[ids[t,k] for k,d in enumerate(ds[t]) if d==1]
        target=[ids[t-1,k] for k,a in enumerate(rows[t-1]) if a==0]
        assert len(source)==len(target)
        for u,v in zip(source,target):join(u,v,t%2)
    return nodes,nxt,prev,vol,ids

def obstruction(rows):
    nodes,nxt,prev,vol,ids=build(rows);N=len(nodes)
    chains=[];where={};position={};voltage={}
    for s in range(N):
        if prev[s] is not None:continue
        chain=[];i=s;v=0
        while i is not None:
            assert i not in where
            where[i]=len(chains);position[i]=len(chain);voltage[i]=v
            chain.append(i);v+=vol[i];i=nxt[i]
        chains.append(chain)
    if len(where)!=N:
        unseen=set(range(N))-where.keys();u=next(iter(unseen));cycle=[u];v=nxt[u]
        while v!=u:cycle.append(v);v=nxt[v]
        return dict(kind='closed_component',cycle=cycle)
    # Same physical-cell consecutive reads, in independently lifted coordinates.
    for chain in chains:
        last={}
        for i in chain:
            t,k,_=nodes[i];x=voltage[i];cell=(x,-t-x)
            if cell in last:
                old=last[cell]
                if k!=nodes[old][1]+1:
                    return dict(kind='rank_gap',previous=old,current=i,cell=cell)
            last[cell]=i
    # On a chain of length ell <= P, the stable key z + p - P*v
    # has exactly the lexicographic order (-v,p), independently of P.
    for chain in chains:
        by_layer={}
        for i in chain:
            by_layer.setdefault(nodes[i][0],[]).append(i)
        for visits in by_layer.values():
            visits.sort(key=lambda i:nodes[i][1])
            for u,v in zip(visits,visits[1:]):
                if (-voltage[u],position[u])>=(-voltage[v],position[v]):
                    return dict(kind='stable_order_reversal',previous=u,current=v,
                                voltage_difference=voltage[v]-voltage[u],
                                time_difference=position[v]-position[u],
                                chain_length=len(chain))
    return None

def verify():
    survivors=[((0,),)];reports=[];certificates=[]
    for depth in range(1,4):
        nxt=[];counts=Counter();max_events=0;max_row=0
        for rows in survivors:
            old=rows[-1];d=departures(-(depth-1),old)
            I=d.count(0);J=old.count(0)
            assert I==J
            for a in candidates(-depth,I,J):
                rs=rows+(a,);max_events=max(max_events,sum(map(len,rs)));max_row=max(max_row,len(a))
                witness=obstruction(rs)
                if witness is None:nxt.append(rs);counts['survives']+=1
                else:
                    counts[witness['kind']]+=1
                    certificates.append(dict(rows=rs,witness=witness))
        reports.append(dict(depth=depth,candidates=sum(counts.values()),outcomes=dict(counts),max_events=max_events,max_row=max_row,survivors=nxt))
        survivors=nxt
    assert not survivors
    digest=hashlib.sha256(json.dumps(certificates,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return dict(status='complete',period_parameter_used=False,width_parameter_used=False,rows_below_extreme=3,reports=reports,certificate_count=len(certificates),certificates_sha256=digest),certificates

if __name__=='__main__':
    import argparse
    import gzip
    from pathlib import Path
    if not __debug__:
        raise RuntimeError('Run without Python -O')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificates', type=Path)
    args=parser.parse_args()
    report,certificates=verify()
    if args.certificates:
        with gzip.open(args.certificates,'wt') as stream:
            json.dump(certificates,stream)
    print(json.dumps(report,indent=2))
