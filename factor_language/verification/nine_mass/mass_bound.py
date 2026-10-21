"""Exact finite graph certificate for the nine-factor mass-deficit bound.

Complete finite enumeration is a stated input to graph_certificate; the runner
rebuilds and checks it with two different enumerators. No positive-cycle solver
or numerical optimization is trusted. The bounded integer potential is rebuilt.
"""
from __future__ import annotations
from collections import deque
import hashlib

WEIGHT = (-23, 29)  # R, L: 3*length - 26*(R-L)
STANDARD = 'RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR'


def digest(value) -> str:
    import json
    return hashlib.sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()


def conflict(word: str) -> dict:
    """Fresh complex-coordinate checker, independent of quotient geometry."""
    p=0j;v=1j;last={}
    for i,c in enumerate(word):
        if c not in 'RL':raise ValueError('expected R/L')
        if p in last and word[last[p]]==c:
            return {'earlier':last[p],'later':i,'point':[int(p.real),int(p.imag)],'letter':c}
        last[p]=i;v*=(-1j if c=='R' else 1j);p+=v
    raise ValueError('purported forbidden factor is physically feasible')


def independent_enumeration() -> dict:
    """All feasible standard-nine-legal prefixes through length 150.

    This uses complex directions, dictionaries and tuple suffixes, unlike the
    native array/coordinate/integer-bitmask enumerator. No node cutoff is used.
    """
    factors={tuple(int(c=='L') for c in (STANDARD*2)[i:i+9]) for i in range(104)}
    choices={}
    for w in factors:choices.setdefault(w[:-1],[]).append(w[-1])
    for row in choices.values():row.sort()
    word=[];last={};nodes=leaves=0;maximum=(0,'');sha=hashlib.sha256()
    def visit(t,p,v,score):
        nonlocal nodes,leaves,maximum
        nodes+=1
        if t<150 and score>maximum[0]:maximum=(score,''.join('RL'[b] for b in word))
        if t==150:
            leaves+=1;sha.update((''.join('RL'[b] for b in word)+'\n').encode());return
        old=last.get(p)
        for b in choices.get(tuple(word[-8:]),[]) if t>=8 else (0,1):
            if old==b:continue
            last[p]=b;word.append(b);nv=v*(1j if b else -1j)
            visit(t+1,p+nv,nv,score+WEIGHT[b]);word.pop()
            if old is None:last.pop(p)
            else:last[p]=old
    visit(0,0j,1j,0)
    return {'nodes':nodes,'words':leaves,'words_sha256':sha.hexdigest(),
            'max_short_deficit':maximum[0],'short_witness':maximum[1]}


def components(edges):
    """Iterative Tarjan SCCs, not the earlier two-pass implementation."""
    n=len(edges);idx=[-1]*n;low=[0]*n;on=bytearray(n);active=[];number=0
    comp=[-1]*n;groups=[]
    for root in range(n):
        if idx[root]>=0:continue
        idx[root]=low[root]=number;number+=1;active.append(root);on[root]=1;stack=[(root,0)]
        while stack:
            v,k=stack[-1]
            if k<len(edges[v]):
                u,_=edges[v][k];stack[-1]=(v,k+1)
                if idx[u]<0:
                    idx[u]=low[u]=number;number+=1;active.append(u);on[u]=1;stack.append((u,0))
                elif on[u]:low[v]=min(low[v],idx[u])
            else:
                stack.pop()
                if stack:low[stack[-1][0]]=min(low[stack[-1][0]],low[v])
                if low[v]==idx[v]:
                    group=[];c=len(groups)
                    while True:
                        u=active.pop();on[u]=0;comp[u]=c;group.append(u)
                        if u==v:break
                    groups.append(group)
    return comp,groups


def follower_quotient(vertices, internal):
    ids={v:i for i,v in enumerate(sorted(vertices))};nexts=[[-1,-1] for _ in ids]
    for u,v,b in internal:
        assert nexts[ids[u]][b] in (-1,ids[v]);nexts[ids[u]][b]=ids[v]
    part=[0]*len(ids)
    for iteration in range(len(ids)+1):
        groups={};new=[]
        for row in nexts:
            key=tuple(part[v] if v>=0 else -1 for v in row)
            if key not in groups:groups[key]=len(groups)
            new.append(groups[key])
        if new==part:break
        part=new
    else:raise RuntimeError('finite follower refinement did not stabilize')
    quotient=[None]*len(groups)
    for u,row in enumerate(nexts):
        signature=tuple(part[v] if v>=0 else -1 for v in row)
        if quotient[part[u]] is not None:assert quotient[part[u]]==signature
        quotient[part[u]]=signature
    assert all(quotient[part[ids[u]]][b]==part[ids[v]] for u,v,b in internal)
    return quotient,iteration+1


def factor_automaton(patterns):
    go=[[-1,-1]];fail=[0];bad=[False]
    for word in patterns:
        v=0
        for c in word:
            b=int(c=='L')
            if go[v][b]<0:
                go[v][b]=len(go);go.append([-1,-1]);fail.append(0);bad.append(False)
            v=go[v][b]
        bad[v]=True
    todo=deque()
    for b in (0,1):
        if go[0][b]<0:go[0][b]=0
        else:todo.append(go[0][b])
    while todo:
        v=todo.popleft();bad[v]|=bad[fail[v]]
        for b in (0,1):
            u=go[v][b]
            if u>=0:fail[u]=go[fail[v]][b];todo.append(u)
            else:go[v][b]=go[fail[v]][b]
    return go,bad


def product_graph(quotient, patterns):
    go,bad=factor_automaton(patterns)
    states=[(v,0) for v in range(len(quotient))];ids={k:i for i,k in enumerate(states)};edges=[]
    for v,s in states:
        row=[]
        for b,u in enumerate(quotient[v]):
            if u<0:continue
            t=go[s][b]
            if bad[t]:continue
            key=u,t
            if key not in ids:ids[key]=len(states);states.append(key)
            row.append((ids[key],b))
        edges.append(row)
    assert len(states)<=len(quotient)*len(go)
    return edges,len(go)


def potential(edges, ceiling=306):
    reverse=[[] for _ in edges]
    for u,row in enumerate(edges):
        for v,b in row:reverse[v].append((u,WEIGHT[b]))
    y=[0]*len(edges);todo=deque(range(len(edges)));queued=bytearray([1])*len(edges);updates=0
    while todo:
        v=todo.popleft();queued[v]=0
        for u,cost in reverse[v]:
            needed=y[v]+cost
            if needed>y[u]:
                if needed>ceiling:raise ValueError('integer potential ceiling exceeded')
                y[u]=needed;updates+=1
                if not queued[u]:todo.append(u);queued[u]=1
    # The inequalities, not the generating relaxation or a hash, are the certificate.
    assert all(0<=v<=ceiling for v in y)
    assert all(y[u]-y[v]>=WEIGHT[b] for u,row in enumerate(edges) for v,b in row)
    return y,updates


def graph_certificate(words, patterns):
    assert len(words)==164283 and all(len(w)==150 and set(w)<={'R','L'} for w in words)
    assert len(set(words))==len(words)
    conflicts=[{'word':w,**conflict(w)} for w in patterns]
    vertices={};values=[];edges=[];mask=(1<<149)-1
    def vertex(v):
        if v not in vertices:vertices[v]=len(edges);edges.append([]);values.append(v)
        return vertices[v]
    for w in words:
        k=int(w.translate(str.maketrans('RL','01')),2)
        a=vertex(k>>1);b=vertex(k&mask);edges[a].append((b,k&1))
    comp,groups=components(edges);budgets=[0]*len(groups);cyclic=[];simple=[];complex_report=None
    for c,group in enumerate(groups):
        internal=[(u,v,b) for u in group for v,b in edges[u] if comp[v]==c]
        if not internal:continue
        cyclic.append([len(group),len(internal)])
        if len(internal)==len(group):
            u=start=group[0];word=''
            while True:
                row=[(v,b) for v,b in edges[u] if comp[v]==c];assert len(row)==1
                u,b=row[0];word+='RL'[b]
                if u==start:break
            costs=[WEIGHT[x=='L'] for x in word];assert sum(costs)<=0
            bound=max(sum((costs*2)[i:i+k]) for i in range(len(costs)) for k in range(len(costs)+1))
            budgets[c]=bound;simple.append({'word':word,'length':len(word),'period_cost':sum(costs),'path_budget':bound})
        else:
            assert complex_report is None
            quotient,rounds=follower_quotient(group,internal)
            product,ac=product_graph(quotient,patterns)
            y,updates=potential(product)
            budgets[c]=max(y)
            complex_report={'vertices':len(group),'edges':len(internal),'quotient_states':len(quotient),
                'refinement_rounds':rounds,'factor_automaton_states':ac,'product_vertices':len(product),
                'product_edges':sum(map(len,product)),'max_potential':max(y),'integer_updates':updates,
                'edges_sha256':digest(product),'potential_sha256':digest(y),'potential':y,
                'edge_inequalities_checked':sum(map(len,product))}
    count=len(groups);out=[[] for _ in groups];indegree=[0]*count
    for u,row in enumerate(edges):
        for v,b in row:
            a,c=comp[u],comp[v]
            if a!=c:out[a].append((c,WEIGHT[b]));indegree[c]+=1
    initial=[-10**9]*count
    for u,k in enumerate(values):initial[comp[u]]=max(initial[comp[u]],52*k.bit_count()-23*149)
    bound=[initial[c]+budgets[c] for c in range(count)]
    queue=deque(c for c in range(count) if indegree[c]==0);visited=0
    while queue:
        c=queue.popleft();visited+=1
        for d,cost in out[c]:
            bound[d]=max(bound[d],bound[c]+cost+budgets[d]);indegree[d]-=1
            if indegree[d]==0:queue.append(d)
    assert visited==count
    assert all(bound[c]>=initial[c]+budgets[c] for c in range(count))
    assert all(bound[d]>=bound[c]+cost+budgets[d] for c in range(count) for d,cost in out[c])
    return {'vertices':len(edges),'edges':len(words),'cyclic_components':cyclic,'simple_components':simple,
        'complex_component':complex_report,'forbidden_factor_conflicts':conflicts,
        'condensation_nodes':count,'condensation_edges':sum(map(len,out)),
        'condensation_rank_sha256':digest(bound),'max_initial_149_cost':max(initial),
        'max_all_path_cost':max(bound),'uniform_nine_bound':max(bound)}
