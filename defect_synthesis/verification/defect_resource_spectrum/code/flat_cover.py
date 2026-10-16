"""Independent reconstruction of the inherited flat ten-factor coverage.

The numerical graph and fold lemma are prior project results. This file rechecks
that dependency for the semilinearity lift; it does not claim a new factor bound.
"""
from collections import deque,Counter
from hashlib import sha256
from examples import A,B,STANDARD

T='RRRRLLRLLRRRRLLRRRRLLRLL'
L10={ (STANDARD*2)[i:i+10] for i in range(104)}
DIR=((0,1),(1,0),(0,-1),(-1,0))

def edge_words(length=150):
    """All literal-feasible finite words, not selected simulations."""
    prefix=[];last={};result=[]
    def visit(p,h):
        if len(prefix)==length:result.append(''.join(prefix));return
        previous=last.get(p)
        choices='RL' if previous is None else ('L' if previous=='R' else 'R')
        tail=''.join(prefix[-9:])
        for c in choices:
            if len(prefix)>=9 and tail+c not in L10:continue
            last[p]=c;prefix.append(c)
            hh=(h+(1 if c=='R' else -1))%4;dx,dy=DIR[hh]
            visit((p[0]+dx,p[1]+dy),hh)
            prefix.pop()
        if previous is None:last.pop(p,None)
        else:last[p]=previous
    visit((0,0),0)
    return sorted(result)

def sccs(adj):
    rev=[[] for _ in adj]
    for v,ds in enumerate(adj):
        for w in ds:rev[w].append(v)
    seen=set();order=[]
    for root in range(len(adj)):
        if root in seen:continue
        seen.add(root);stack=[(root,iter(adj[root]))]
        while stack:
            v,it=stack[-1]
            try:w=next(it)
            except StopIteration:order.append(v);stack.pop();continue
            if w not in seen:seen.add(w);stack.append((w,iter(adj[w])))
    component=[-1]*len(adj);groups=[]
    for root in reversed(order):
        if component[root]>=0:continue
        k=len(groups);component[root]=k;nodes=[];todo=[root]
        while todo:
            v=todo.pop();nodes.append(v)
            for w in rev[v]:
                if component[w]<0:component[w]=k;todo.append(w)
        groups.append(nodes)
    return component,groups

def inspect():
    words=edge_words();names=sorted(set(w[:-1] for w in words)|set(w[1:] for w in words))
    ids={w:i for i,w in enumerate(names)}
    edges=[(ids[w[:-1]],ids[w[1:]],w[-1]) for w in words]
    adj=[[] for _ in names]
    for v,w,c in edges:adj[v].append(w)
    comp,groups=sccs(adj)
    cyclic=[g for g in groups if len(g)>1 or g[0] in adj[g[0]]]
    assert sorted(map(len,cyclic))==[24,104,366]
    H=set(next(g for g in cyclic if len(g)==366))
    # Resolve the quotient phase from each complete 149-letter history.
    def advance(q,c):
        if c==B[q]:return (q+1)%102
        if q==0 and c=='L':return 75
        return None
    phases={}
    for v in sorted(H):
        possible=[]
        for initial in range(102):
            q=initial
            for c in names[v]:
                q=advance(q,c)
                if q is None:break
            if q is not None:possible.append(q)
        if len(set(possible))!=1:raise AssertionError(('ambiguous quotient',len(set(possible))))
        phases[v]=possible[0]
    for v,w,c in edges:
        if v in H and w in H:assert advance(phases[v],c)==phases[w]
    lifted=[]
    for v in range(len(names)):
        if v not in H:lifted.append((v,0))
        else:
            lifted.extend((v,k) for k in range(4) if k<3 or phases[v]!=0)
    lid={v:i for i,v in enumerate(lifted)};le=[]
    for v,w,c in edges:
        for k in (range(4) if v in H else (0,)):
            if (v,k) not in lid:continue
            kk=(k+int(phases[v]==0 and c=='R')) if v in H and w in H else 0
            if (w,kk) in lid:le.append((lid[v,k],lid[w,kk],c))
    la=[[] for _ in lifted]
    for v,w,c in le:la[v].append(w)
    lc,lg=sccs(la);cycle=[g for g in lg if len(g)>1 or g[0] in la[g[0]]]
    assert sorted(map(len,cycle))==[24,28,28,28,104]
    for g in cycle:
        gs=set(g);assert all(sum(w in gs for w in la[v])==1 for v in g)
    # Cyclic SCC words are phases of the THREE fixed words.
    edge_label={(v,w):c for v,w,c in le}
    for g in cycle:
        gs=set(g);v=g[0];chars=[]
        for _ in range(len(g)):
            w=next(x for x in la[v] if x in gs);chars.append(edge_label[v,w]);v=w
        w=''.join(chars);target={24:T,28:A,104:STANDARD}[len(g)]
        assert w in target+target
    dag=[set() for _ in lg];indeg=[0]*len(lg)
    for v,w,c in le:
        a,b=lc[v],lc[w]
        if a!=b:dag[a].add(b)
    for ds in dag:
        for b in ds:indeg[b]+=1
    todo=deque(i for i,d in enumerate(indeg) if not d);order=[]
    while todo:
        a=todo.popleft();order.append(a)
        for b in dag[a]:
            indeg[b]-=1
            if indeg[b]==0:todo.append(b)
    rank=[(0,0,0)]*len(lg)
    for a in reversed(order):
        n=len(lg[a]);cyc=n>1 or lg[a][0] in la[lg[a][0]]
        weight=(1,0,n) if cyc else (0,1,0)
        rank[a]=tuple(weight[j]+max([rank[b][j] for b in dag[a]]+[0]) for j in range(3))
    maxrank=tuple(max(r[j] for r in rank) for j in range(3))
    assert maxrank==(5,956,212)
    assert len(words)==6605 and len(names)==6501 and len(lifted)==7595 and len(le)==7763
    return dict(base_vertices=len(names),base_edges=len(edges),lifted_vertices=len(lifted),
                lifted_edges=len(le),simple_cycles=sorted(map(len,cycle)),maxima=maxrank,
                quotient_states=len(phases),window_sha256=sha256(('\n'.join(words)+'\n').encode()).hexdigest(),
                finite_literal_bound=149+956+212,power_bound=5,
                origin='Inherited ten-factor/macro structure, reconstructed independently; triple-fold arithmetic checked separately.')

if __name__=='__main__':
    import json,time
    t0=time.monotonic();r=inspect();r['seconds']=time.monotonic()-t0;print(json.dumps(r,indent=2))
