"""Finite certificates for a global mass/ten-factor-defect inequality.

Generator output is checked by local integer edge inequalities. The default
mode never writes or repairs witness.json. No HC conclusion is returned.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, time
from collections import defaultdict, deque
from pathlib import Path

W='RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR'
D=((0,1),(1,0),(0,-1),(-1,0))
L10={ (W*2)[i:i+10] for i in range(104) }
DEPTH=300

def weight(c): return 29 if c=='L' else -23

def digest(b): return hashlib.sha256(b).hexdigest()

def literal(word):
    p=(0,0);h=0;last={};seed=set();positions=[]
    for i,c in enumerate(word):
        if last.get(p)==c: raise ValueError(('same-cell conflict',i,p,c))
        if p not in last and c=='L':seed.add(p)
        last[p]=c;positions.append(p);h=(h+(1 if c=='R' else -1))%4
        p=(p[0]+D[h][0],p[1]+D[h][1])
    return seed,positions,p,h

def enumerate_kernel():
    # Every state stores a cloned last-read map; the C++ checker uses mutable
    # initial cell colours and depth-first backtracking instead.
    states=[('',(0,0),0,{},0)]
    best=(0,''); levels=[]; extensions=0;rejections=0
    for depth in range(1,DEPTH+1):
        following=[]
        for word,p,h,last,score in states:
            for c in 'LR':
                if depth>=10 and (word+c)[-10:] not in L10:continue
                extensions+=1
                if last.get(p)==c:
                    rejections+=1;continue
                g=(h+(1 if c=='R' else -1))%4
                q=(p[0]+D[g][0],p[1]+D[g][1]);new=last.copy();new[p]=c
                z=score+weight(c);v=word+c
                following.append((v,q,g,new,z))
                if depth<DEPTH and (z>best[0] or z==best[0] and (len(v),v)<(len(best[1]),best[1])):
                    best=z,v
        states=following;levels.append([depth,len(states)])
    words=sorted(x[0]for x in states)
    return words,best,{'levels':levels,'extensions':extensions,'rejections':rejections}

def build_graph(words):
    nodes=sorted({x for w in words for x in (w[:-1],w[1:])})
    ids={w:i for i,w in enumerate(nodes)}
    edges=[(ids[w[:-1]],ids[w[1:]],weight(w[-1])) for w in words]
    return nodes,edges

def generate_potential(size,edges):
    # Only a proposal generator. The inequalities are checked separately.
    back=[[]for _ in range(size)]
    for a,b,c in edges:back[b].append((a,c))
    values=[0]*size;queue=deque(range(size));queued=set(queue);relax=0
    while queue:
        b=queue.popleft();queued.remove(b);relax+=1
        if relax>10_000_000:raise RuntimeError('resource cap, no theorem output')
        for a,c in back[b]:
            if values[a]<c+values[b]:
                values[a]=c+values[b]
                if a not in queued:queue.append(a);queued.add(a)
    return values,relax

def verify_potential(nodes,edges,h):
    if len(h)!=len(nodes) or any(not isinstance(x,int) or x<0 for x in h):
        raise ValueError('invalid nonnegative potential')
    for a,b,c in edges:
        if h[a]<c+h[b]:raise ValueError(('bad edge inequality',a,b,c))
    maximum=max(sum(map(weight,v))+h[i]for i,v in enumerate(nodes))
    if maximum>284:raise ValueError('long-word bound exceeds 284')
    return maximum

def main(generate=False):
    start=time.monotonic();words,best,stats=enumerate_kernel();nodes,edges=build_graph(words)
    h,relax=generate_potential(len(nodes),edges);long=verify_potential(nodes,edges,h)
    seed,_,_,_=literal(best[1])
    expected={'depth':DEPTH,'vertices':len(nodes),'edges':len(edges),'short_maximum':best[0],
      'short_witness':best[1],'short_seed':sorted(map(list,seed)),
      'long_maximum':long,'potential_maximum':max(h),
      'edge_words_sha256':digest(('\n'.join(words)+'\n').encode()),
      'potential_sha256':digest(('\n'.join(map(str,h))+'\n').encode()),
      'standard_word':W,'global_constant':322,'defect_penalty':351}
    root=Path(__file__).resolve().parent
    if generate:
        (root/'witness.json').write_text(json.dumps(expected,indent=2)+'\n')
    elif json.loads((root/'witness.json').read_text())!=expected:
        raise ValueError('immutable witness mismatch')
    if (len(nodes),len(edges),best[0],long,max(h))!=(29334,29559,322,284,251):
        raise ValueError('unexpected finite kernel')
    # An altered potential must be rejected, not repaired by the checker.
    bad=h.copy();a,b,c=next(e for e in edges if e[2]+h[e[1]]>0);bad[a]=c+h[b]-1
    try:verify_potential(nodes,edges,bad)
    except ValueError:pass
    else:raise AssertionError('damaged potential accepted')
    assert sum(map(weight,W))==0 and len(W)==104 and W.count('R')-W.count('L')==12
    literal(W*4)
    report={'status':'passed','kernel':expected,'all_integer_inequalities_checked':len(edges),
      'short_lengths_checked':[0,299],'damaged_potential_rejected':True,
      'queue_removals':relax,'enumeration':stats,'seconds':round(time.monotonic()-start,3),
      'HC_proved':False,'global_finiteness_proved':False,'external_review':False}
    (root/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    # These are reproducible temporary values for the independent comparison.
    (root/'edge_words.generated').write_text('\n'.join(words)+'\n')
    (root/'potential.generated').write_text('\n'.join(map(str,h))+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='enumeration'},indent=2))
if __name__=='__main__':
    if not __debug__:raise RuntimeError('Do not disable checking assertions')
    parser=argparse.ArgumentParser();parser.add_argument('--generate',action='store_true')
    main(parser.parse_args().generate)
