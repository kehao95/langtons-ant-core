"""Independent witness geometry, local truth tables and genuine-highway controls.

The candidate enumerator is called only for its output. Its graph-building and
obstruction routines are not used to validate the rejection certificates.
"""
from __future__ import annotations
from collections import defaultdict, Counter
from itertools import product
import hashlib
import json
import local_obstruction as local

MOVES=((0,1),(1,0),(0,-1),(-1,0))
STANDARD='RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR'

def vector_graph(rows):
    events=[];outgoing=defaultdict(list);incoming=defaultdict(list)
    for depth,row in enumerate(rows):
        for rank,a in enumerate(row):
            h=(2 if a else 0) if depth%2 else (3 if a else 1)
            oh=(h+(1 if rank%2==0 else -1))%4
            i=len(events);events.append((depth,rank,MOVES[oh]))
            dx,dy=MOVES[h];incoming[depth+dx+dy,depth].append(i)
            dx,dy=MOVES[oh];outgoing[depth,depth-dx-dy].append(i)
    nxt={};prev={}
    for (source,target),us in outgoing.items():
        if 0<=target<len(rows):
            vs=incoming[source,target]
            assert len(us)==len(vs)
            for u,v in zip(us,vs):
                assert u not in nxt and v not in prev
                nxt[u]=v;prev[v]=u
    return events,nxt,prev

def paths_and_coordinates(events,nxt,prev):
    paths=[];chain={};position={};coordinates={}
    for root in range(len(events)):
        if root in prev:continue
        path=[];u=root;x=0;y=-events[root][0]
        while u is not None:
            assert u not in chain
            chain[u]=len(paths);position[u]=len(path);coordinates[u]=(x,y)
            assert x+y==-events[u][0]
            path.append(u);dx,dy=events[u][2];x+=dx;y+=dy;u=nxt.get(u)
        paths.append(path)
    return paths,chain,position,coordinates

def validate_certificate(rows,w):
    try:
        events,nxt,prev=vector_graph(rows)
        if w['kind']=='closed_component':
            c=w['cycle']
            return bool(c) and len(set(c))==len(c) and all(nxt.get(a)==b for a,b in zip(c,c[1:]+c[:1]))
        paths,chain,pos,xy=paths_and_coordinates(events,nxt,prev)
        if len(chain)!=len(events):return False
        if w['kind']=='rank_gap':
            a,b=w['previous'],w['current']
            if chain[a]!=chain[b] or pos[a]>=pos[b] or xy[a]!=xy[b]:return False
            if list(xy[b])!=list(w['cell']):return False
            middle=paths[chain[a]][pos[a]+1:pos[b]]
            return not any(xy[i]==xy[a] for i in middle) and events[b][1]!=events[a][1]+1
        if w['kind']=='stable_order_reversal':
            u,v=w['previous'],w['current']
            if chain[u]!=chain[v] or events[u][0]!=events[v][0] or events[u][1]>=events[v][1]:return False
            delta=xy[v][0]-xy[u][0];dt=pos[v]-pos[u]
            if delta!=w['voltage_difference'] or dt!=w['time_difference']:return False
            if len(paths[chain[u]])!=w['chain_length']:return False
            # For every possible P >= path length, dt - delta*P < 0.
            return delta>0 and dt-delta*len(paths[chain[u]])<0 or delta==0 and dt<=0
        return False
    except (KeyError,IndexError,AssertionError,TypeError):return False

def truth_table():
    count=0
    for depth,a,k in product(range(2),range(2),range(2)):
        h=(2 if a else 0) if depth%2 else (3 if a else 1)
        out=(h+(1 if k==0 else -1))%4
        dx,dy=MOVES[out]
        assert int(dx+dy==1)==a^k^(depth%2)
        count+=1
    # Brute force all short arrival strings, independent of rank-count formula.
    examined=0;groups=defaultdict(set)
    for depth in (1,2):
        for n in range(14):
            for a in product((0,1),repeat=n):
                I=sum(a);J=0
                for k,bit in enumerate(a):
                    h=(2 if bit else 0) if depth%2 else (3 if bit else 1)
                    dx,dy=MOVES[(h+(1 if k%2==0 else -1))%4]
                    J+=dx+dy==1
                if n>=I and n>J:groups[depth,I,J].add(a)
                examined+=1
    for depth,I,J in product((1,2),range(4),range(4)):
        words=groups[depth,I,J]
        actual={a for a in local.candidates(-depth,I,J) if len(a)<=13}
        assert actual==words
    return dict(geometric_port_cases=count,binary_strings_examined=examined,port_count_groups_compared=32)

def plan(word,heading):
    x=y=0;points=[];headings=[]
    for c in word:
        points.append((x,y));headings.append(heading)
        heading=(heading+(1 if c=='R' else -1))%4
        dx,dy=MOVES[heading];x+=dx;y+=dy
    return points,headings,(x,y),heading

def highway_control(word,heading,depth):
    """Same necessary tests on a real two-residue P104 prefix, not one-lane data.

Compare stable-edge matching with the actual successor, then lift every fixed
path by literal move vectors. Every fixed path is then tested for stable-order reversals; neither the
enumeration graph nor its rank-group sorting routine is imported.
"""
    points,heads,drift,endh=plan(word,heading);P=len(word)
    assert drift==(2,-2) and endh==heading
    groups=defaultdict(list)
    for i,(x,y) in enumerate(points):groups[x+y,x%2].append((i-P*(x//2),i))
    ranks={i:k for visits in groups.values() for k,(_,i) in enumerate(sorted(visits))}
    assert all(word[i]==('R' if ranks[i]%2==0 else 'L') for i in range(P))
    top=max(x+y for x,y in points);chosen={i for i,(x,y) in enumerate(points) if x+y>=top-depth}
    def cls(i):x,y=points[i];return x+y,x%2
    outs=defaultdict(list);ins=defaultdict(list)
    for i in chosen:
        j=(i+1)%P
        if j in chosen:outs[cls(i),cls(j)].append(i);ins[cls(i),cls(j)].append(j)
    nxt={};prev={}
    for edge,src in outs.items():
        src.sort(key=ranks.get);dst=sorted(ins[edge],key=ranks.get)
        for u,v in zip(src,dst):
            assert v==(u+1)%P # strong first-to-first matching positive control
            nxt[u]=v;prev[v]=u
    chains=[];where={};voltage={}
    for root in sorted(chosen-prev.keys()):
        t,r=cls(root);x=r;y=t-r;i=root;path=[];last={}
        while i is not None:
            assert i not in where
            t,r=cls(i);assert x+y==t and x%2==r
            where[i]=len(chains);voltage[i]=(x-r)//2;path.append(i)
            cell=x,y
            if cell in last:assert ranks[i]==last[cell]+1
            last[cell]=ranks[i]
            dx,dy=MOVES[(heads[i]+(1 if word[i]=='R' else -1))%4]
            x+=dx;y+=dy;i=nxt.get(i)
        chains.append(path)
    assert len(where)==len(chosen)
    for path in chains:
        position={i:p for p,i in enumerate(path)}
        for visits in groups.values():
            ids=[i for _,i in sorted(visits) if i in position]
            for u,v in zip(ids,ids[1:]):
                delta=voltage[v]-voltage[u]
                assert delta<0 or delta==0 and position[u]<position[v]

def audit():
    if not __debug__:raise RuntimeError('Python -O disables proof checks')
    report,certificates=local.verify()
    assert all(validate_certificate(c['rows'],c['witness']) for c in certificates)
    first=next(c for c in certificates if c['witness']['kind']=='rank_gap')
    corrupt=json.loads(json.dumps(first));corrupt['witness']['cell'][0]+=1
    assert not validate_certificate(corrupt['rows'],corrupt['witness'])
    corrupt=json.loads(json.dumps(certificates[0]));corrupt['witness']['voltage_difference']+=10
    assert not validate_certificate(corrupt['rows'],corrupt['witness'])
    points,heads,d,eh=plan(STANDARD,1)
    controls=0
    for phase in range(104):
        shifted=STANDARD[phase:]+STANDARD[:phase]
        for depth in range(1,10):
            highway_control(shifted,heads[phase],depth);controls+=1
    return dict(status='complete',witnesses_checked=len(certificates),corruption_controls=2,
                literal_geometry=truth_table(),standard_highway_prefix_controls=controls,
                standard_controls_use_full_drift=[2,-2],
                certificate_sha256=report['certificates_sha256'])

if __name__=='__main__':print(json.dumps(audit(),indent=2))
