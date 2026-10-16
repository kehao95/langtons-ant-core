"""Exact top-three-layer obstruction, with individually verifiable rejections.
No period, width, wake, mass, or numerical time cutoff is a search parameter.
Only hypothetical heading-reset drift (1,-1) is imposed.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from collections import Counter, defaultdict
from pathlib import Path
import json, hashlib

MOVES=((0,1),(1,0),(0,-1),(-1,0))

@dataclass
class Node:
    t:int
    k:int
    a:int
    down:int
    h:int
    nxt:int=-1
    prev:int=-1
    voltage:int=0

def copy_graph(g):
    return [Node(z.t,z.k,z.a,z.down,z.h,z.nxt,z.prev,z.voltage) for z in g]

def attach(g, i, j, v):
    if g[i].nxt!=-1 or g[j].prev!=-1: raise ValueError('Occupied endpoint')
    g[i].nxt=j;g[i].voltage=v;g[j].prev=i

def children(g, old, t):
    """DFS over local arrival bits; the proved local length bound is exact enough."""
    outputs=[i for i in old if g[i].down]
    inputs=[i for i in old if g[i].a]
    I,J=len(outputs),len(inputs)
    for m in range(2*(I+J)+2):
        def rec(k, incoming, outgoing, bits, graph, row):
            if incoming>I or outgoing>J:return
            if incoming+m-k<I or outgoing+m-k<J:return
            if k==m:
                if incoming==I and outgoing==J:
                    yield ''.join(map(str,bits)),graph,row
                return
            for b in (0,1):
                d=b^(k%2) if t%2==0 else 1-(b^(k%2))
                if incoming+b>I or outgoing+d>J:continue
                new=copy_graph(graph)
                a,down=1-b,1-d
                h=(1 if a else 3) if t%2==0 else (0 if a else 2)
                i=len(new);new.append(Node(t,k,a,down,h))
                if b:attach(new,outputs[incoming],i,-1 if t%2==0 else 0)
                if d:attach(new,i,inputs[outgoing],1 if t%2 else 0)
                yield from rec(k+1,incoming+b,outgoing+d,bits+(b,),new,row+[i])
        yield from rec(0,0,0,(),g,[])

def split_chains(g):
    n=len(g);c=[-1]*n;p=[0]*n;v=[0]*n;chains=[]
    for root,z in enumerate(g):
        if z.prev>=0:continue
        i=root;vv=0;nodes=[]
        while i>=0:
            if c[i]>=0:raise ValueError('Path merge')
            c[i]=len(chains);p[i]=len(nodes);v[i]=vv;nodes.append(i)
            vv+=g[i].voltage;i=g[i].nxt
        chains.append(nodes)
    for i in range(n):
        if c[i]<0:
            cycle=[];j=i
            while j not in cycle:
                cycle.append(j);j=g[j].nxt
                if j<0:raise AssertionError('Unexpected open component')
            return None,{'kind':'closed','nodes':cycle[cycle.index(j):]}
    return (c,p,v,chains),None

def ordered_edges(g,parts):
    c,p,v,chains=parts;edges=[]
    for j,z in enumerate(g):
        if not z.k:continue
        i=j-1
        assert g[i].t==z.t and g[i].k==z.k-1
        edges.append((c[i],c[j],v[j]-v[i],4+p[i]-p[j],i,j))
    return edges

def affine_cycle(g,parts):
    """Find, then independently check, a cycle positive for every P>=|g|."""
    edges=ordered_edges(g,parts);q=len(parts[3]);dist=[(0,0)]*q;pred=[-1]*q
    last=-1
    for _ in range(q):
        last=-1
        for e,(a,b,K,C,i,j) in enumerate(edges):
            cand=(dist[a][0]+K,dist[a][1]+C)
            if cand>dist[b]:dist[b]=cand;pred[b]=e;last=b
        if last<0:return None
    x=last
    for _ in range(q):
        if pred[x]<0:raise AssertionError('Missing cycle predecessor')
        x=edges[pred[x]][0]
    finish=x;ids=[]
    while True:
        e=pred[x];ids.append(e);x=edges[e][0]
        if x==finish:break
        if len(ids)>q:raise AssertionError('Non-simple extracted cycle')
    ids.reverse();cycle=[edges[e] for e in ids]
    assert all(cycle[i][1]==cycle[(i+1)%len(cycle)][0] for i in range(len(cycle)))
    K=sum(e[2]for e in cycle);C=sum(e[3]for e in cycle);n=len(g)
    # This check, not a formal-infinity numerical verdict, is the rejection premise.
    if K<0 or K*n+C<=0:raise AssertionError(('Cycle is not universal',K,C,n,cycle))
    return {'kind':'order','pairs':[[e[4],e[5]]for e in cycle],
            'coefficient':K,'constant':C,'built_events':n}

def physical_conflict(g,parts):
    for chain in parts[3]:
        x=y=0;seen={};trace=[]
        for j in chain:
            z=g[j];c=z.k%2;trace.append((j,x,y,c,z.h))
            if (x,y) in seen:
                oldindex=seen[x,y]
                if trace[oldindex][3]==c:
                    seg=trace[oldindex:]
                    return {'kind':'read','nodes':[i[0]for i in seg],
                            'word':''.join('L' if i[3] else 'R'for i in seg)}
            seen[x,y]=len(trace)-1
            h=(z.h+(1 if c==0 else -1))%4;dx,dy=MOVES[h]
            if z.nxt>=0:
                target=g[z.nxt]
                assert target.h==h and target.t==z.t+dx+dy and z.voltage==dx
            x+=dx;y+=dy
    return None

def certificate():
    rows=[];levels=defaultdict(Counter);terminal=[];nmax=0
    front=[((),[Node(0,0,1,1,1)],[0])]
    for t in (-1,-2,-3):
        nxt=[]
        for path,g,old in front:
            for bits,gg,newrow in children(g,old,t):
                key=path+(bits,);nmax=max(nmax,len(gg))
                parts,rejection=split_chains(gg)
                if not rejection:rejection=affine_cycle(gg,parts)
                if not rejection and t==-3:rejection=physical_conflict(gg,parts)
                if not rejection:
                    if t==-3:raise AssertionError(('Surviving three-layer prefix',key))
                    rejection={'kind':'expand'};nxt.append((key,gg,newrow))
                else:
                    if rejection['kind']=='read':terminal.append({'rows':key,**rejection})
                levels[t][rejection['kind']]+=1
                rows.append({'rows':key,**rejection})
        front=nxt
    assert not front
    return {'schema':'unit-diagonal-three-layer-v1',
            'scope':'No finite-support periodic word of full drift (1,-1); no period/width/growth cutoff.',
            'counts':{str(t):dict(v)for t,v in levels.items()},'max_built_events':nmax,
            'records':rows,'terminal_read_conflicts':terminal}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    obj=certificate();data=json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n'
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(data)
    print(json.dumps({'records':len(obj['records']),'counts':obj['counts'],
                      'max_built_events':obj['max_built_events'],
                      'read_conflicts':len(obj['terminal_read_conflicts']),
                      'sha256':hashlib.sha256(data.encode()).hexdigest()},indent=2))
