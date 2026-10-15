"""Dedicated controls: exact first time AND complete endpoint, never pose-only."""
from __future__ import annotations
from collections import defaultdict
import hashlib,json,random,time
from pathlib import Path
import macro as m
ROOT=Path(__file__).resolve().parent

# Independent literal implementation uses Gaussian integers for geometry.
def literal_step(B,p,h):
    black=p in B;c='L' if black else 'R'
    if black:B.remove(p)
    else:B.add(p)
    h=h*(1j if black else -1j)
    return p+h,h,c

def literal_past(B,p,h,n=9):
    B=set(B);letters=[]
    for _ in range(n):
        q=p-h;black=q in B;c='R' if black else 'L'
        if black:B.remove(q)
        else:B.add(q)
        h=h*(1j if c=='R' else -1j);p=q;letters.append(c)
    return ''.join(reversed(letters))

def to_gauss(B,p,h):
    return {complex(*q)for q in B},complex(*p),(1j,1,-1j,-1)[h]

def from_gauss(B,p,h):
    return {(int(q.real),int(q.imag))for q in B},(int(p.real),int(p.imag)),(1j,1,-1j,-1).index(h)

def brute(B,p,h,limit):
    B,p,h=to_gauss(B,p,h);hist=literal_past(B,p,h)
    for t in range(limit):
        c='L' if p in B else 'R';bad=hist+c not in m.L10
        p,h,c=literal_step(B,p,h);hist=(hist+c)[-9:]
        if bad:return t,from_gauss(B,p,h)
    return None

def move(B,p,h,t):
    B,p,h=to_gauss(B,p,h)
    for _ in range(t):p,h,_=literal_step(B,p,h)
    return from_gauss(B,p,h)

def periodic_black_prefix(word,n):
    return m.r.first_read_seed(word*n)

def T_family(n,wit):
    terms=[m.Segment(tuple(p))for p in wit['sharp_family']['E']]
    if n:
        terms.extend([m.Segment((-2,-2),(0,-2),n),m.Segment((0,-3),(0,-2),n)])
    terms.extend(m.Segment((x,y-2*n))for x,y in wit['sharp_family']['cap'])
    return m.State(tuple(terms))

def U_rail(n,wit):
    points=[(2,-3),(2,-2),(3,-4),(3,-2),(3,-1)]
    return m.State((m.Segment((1,-1)),)+tuple(m.Segment(p,(0,-4),n)for p in points))

def summary_graph(data):
    nodes=sorted(data['lift']); edge_lines=[];rank_lines=[]
    for v in nodes:
        i=data['ids'][v];budget=data['budget'][i]
        rank_lines.append(v[0]+'\t'+str(v[1])+'\t'+'\t'.join(map(str,budget)))
        for u in sorted(data['lift'][v]):edge_lines.append(v[0]+'\t'+str(v[1])+'\t'+u[0]+'\t'+str(u[1]))
    return {'vertices':len(nodes),'edges':len(edge_lines),'cyclic_lengths':sorted(len(data['comps'][i])for i in data['cyclic']),
       'max_periodic_plans':data['maximum'][0],'max_noncyclic_updates':data['maximum'][1],
       'max_period_sum':data['maximum'][2], 'ordinary_update_bound':1111,'term_increment_bound':1530,
       'edges_sha256':m.sha(('\n'.join(edge_lines)+'\n').encode()),
       'rank_sha256':m.sha(('\n'.join(rank_lines)+'\n').encode())}

def run():
    rng=random.Random(2026101503);counts=defaultdict(int);start=time.monotonic()
    data=m.graph_data();g=summary_graph(data);maxordinary=maxplans=0
    def compare(X,limit=60000):
        nonlocal maxordinary,maxplans
        B,p,h=m.expand(X);out=m.next_event(X);maxordinary=max(maxordinary,out.ordinary_updates);maxplans=max(maxplans,out.periodic_plans)
        if out.time is not None:
            if out.time>=limit:raise AssertionError('control limit insufficient')
            result=brute(B,p,h,out.time+1)
            if result is None or result[0]!=out.time or result[1]!=m.expand(out.post_state):
                raise AssertionError(('complete endpoint mismatch',out.time,result))
            counts['literal_updates']+=out.time+1
            points=B|{p};width=max(max(q[a]for q in points)-min(q[a]for q in points)for a in (0,1))
            if out.time+1>212*width+854199:raise AssertionError('linear first-event deadline')
            for q in result[1][0]|{result[1][1]}:
                if any(q[a]<min(v[a]for v in points)-1959 or q[a]>max(v[a]for v in points)+1959 for a in (0,1)):
                    raise AssertionError('complete-field halo control')
            counts['deadline_and_halo_endpoints']+=1
        else:
            result=brute(B,p,h,max(600,out.tail_offset+208))
            if result is not None:raise AssertionError('false permanent absence')
            # Independent pre-existing epoch-breakpoint test on the actual tail endpoint.
            b,q,hh=move(B,p,h,out.tail_offset)
            if not m.r.verify_periodic_field(out.tail_word,{m.r.rotate(m.sub(v,q),-hh) for v in b},[]):
                raise AssertionError('tail failed independent all-future verifier')
        return out
    # Mixed stride rays: modular step two, cancellations, nonparallel and far hits.
    strides=sorted(m.STRIDES-{(0,0)})
    for _ in range(5000):
        s=m.Segment((rng.randrange(-20,21),rng.randrange(-20,21)),rng.choice(sorted(m.STRIDES)),1)
        if s.stride!=(0,0):s=m.Segment(s.start,s.stride,rng.randrange(1,21))
        q=(rng.randrange(-20,21),rng.randrange(-20,21));d=rng.choice(strides)
        hit=m.ray_intersection(q,d,s)
        got=[] if hit is None else list(range(hit[0],hit[1]+1,hit[2]))
        want=[j for j in range(101)if s.contains(m.add(q,m.scale(j,d)))]
        if got!=want:raise AssertionError(('intersection',q,d,s,got,want))
        counts['ray_segment_controls']+=1
    # Extensional equality must ignore representation splitting, but not crossings.
    for _ in range(80):
        terms=[]
        for j in range(6):
            v=rng.choice(strides);terms.append(m.Segment((rng.randrange(-6,7),rng.randrange(-6,7)),v,rng.randrange(2,9)))
        X=m.State(tuple(terms));B,p,h=m.expand(X);Y=m.from_cells(B,p,h)
        if not m.same_complete_state(X,Y):raise AssertionError('split-field equality')
        Z=m.State(Y.terms+(m.Segment((100,100)),),p,h)
        if m.same_complete_state(X,Z):raise AssertionError('changed field accepted')
        counts['exact_field_equalities']+=2
    for _ in range(160):
        B={(rng.randrange(-12,13),rng.randrange(-12,13))for _ in range(rng.randrange(45))}
        p=(rng.randrange(-4,5),rng.randrange(-4,5));h=rng.randrange(4)
        compare(m.from_cells(B,p,h));counts['arbitrary_finite_inputs']+=1
    for i in range(104):
        word=m.r.W[i:]+m.r.W[:i];recipe=m.r.periodic_recipe(word);B=set(map(tuple,recipe['points']))
        B,p,h=move(B,(0,0),0,160)
        for rot in (0,1):
            X=m.from_cells({m.r.rotate(q,rot)for q in B},m.r.rotate(p,rot),(h+rot)%4)
            if compare(X).time is not None:raise AssertionError('mature standard rejected')
            counts['mature_standard_poses']+=1
    wit=m.base.load_witness(m.TEN/'certificates')
    for n in (7,8,13,25,60):
        X=T_family(n,wit);X=m.skip(X,wit['T'],150)
        if compare(X).time is not None:raise AssertionError('T-family should have no future defect')
        counts['finite_24_caps']+=1
        X=U_rail(n,wit);X=m.skip(X,wit['U'],150)
        compare(X);counts['finite_28_rails']+=1
    # The literal word prefixes reach the non-simple component before its folds.
    for n in (2,5,10,30):
        z=wit['B']+wit['A']*n+wit['B']+wit['A']*n
        col=m.r.collision(z);z=z[:col[1]]
        B=m.r.first_read_seed(z)
        for warm in (0,149):
            B1,p,h=move(B,(0,0),0,warm)
            compare(m.from_cells(B1,p,h));counts['folded_prefixes']+=1
    marker=json.loads((m.TEN/'certificates/far_marker.json').read_text()); cases=[]
    seed=set(map(tuple,marker['seed']));d=tuple(marker['drift']);b=tuple(marker['base'])
    for n in (20,30,10**12,10**60):
        X=m.from_cells(seed|{m.add(b,m.scale(n,d))});out=m.next_event(X)
        if out.time!=104*n-92:raise AssertionError('wrong all-parameter marker time')
        if n<100:compare(X)
        # Independently reconstruct the full endpoint by the marker's fixed standard word.
        Y=m.skip(X,marker['word'],out.time);Y,_=m.step(Y)
        if not m.same_complete_state(Y,out.post_state):raise AssertionError('remote complete field differs')
        cases.append({'kind':'remote_marker','n':str(n),'time':str(out.time),'plans':out.periodic_plans,'ordinary':out.ordinary_updates,'post_terms':len(out.post_state.terms)})
    for n in (10**12,10**60):
        X=m.skip(T_family(n,wit),wit['T'],150);out=m.next_event(X)
        if out.time is not None:raise AssertionError('huge cap family rejected')
        # An independently supplied exact target formula T^n Z^omega remains 10-legal.
        remaining=24*n-150
        phase=150%24; Tphase=wit['T'][phase:]+wit['T'][:phase]
        Z=m.skip(X,Tphase,remaining)
        if m.first_mismatch(Z,wit['Z']) is not None:raise AssertionError('huge family target invalid')
        cases.append({'kind':'huge_finite_24_cap','n':str(n),'no_future_event':True,'tail_offset':str(out.tail_offset),'plans':out.periodic_plans,'ordinary':out.ordinary_updates,'input_terms':len(X.terms)})
        X=m.skip(U_rail(n,wit),wit['U'],150);out=m.next_event(X)
        if out.time is None:raise AssertionError('unprotected 28 rail declared permanent')
        cases.append({'kind':'huge_finite_28_rail','n':str(n),'time':str(out.time),'plans':out.periodic_plans,'ordinary':out.ordinary_updates,'post_terms':len(out.post_state.terms)})
    # Actual repeated calls, with the full last endpoint carried forward unchanged.
    for _ in range(12):
        X=m.from_cells({(rng.randrange(-5,6),rng.randrange(-5,6))for _ in range(12)})
        initial=len(X.terms)
        for j in range(20):
            out=compare(X);counts['restarts']+=1
            if out.time is None:break
            X=out.post_state
            if len(X.terms)>initial+1530*(j+1):raise AssertionError('cumulative size bound')
    # A first concrete bridge attempt failed: a 10-legal finite lifetime can exceed 116.
    failed=json.loads((ROOT/'attempt.json').read_text());word=failed['word']
    if m.r.collision(word) is not None or len(word)!=397:raise AssertionError('bad failure witness')
    qs,_,_,_=m.r.geometry(word)
    if [(i,word[i])for i,p in enumerate(qs)if p==(0,0)]!=[(0,'R'),(396,'L')]:raise AssertionError('lifetime is not consecutive')
    if any(word[i:i+10]not in m.L10 for i in range(len(word)-9)):raise AssertionError('word not ten-legal')
    if sorted(map(list,m.r.first_read_seed(word)))!=failed['seed']:raise AssertionError('wrong complete seed')
    counts['failed_116_bridge_checked']=1
    return {'status':'passed','graph':g,'counts':dict(counts),'huge_cases':cases,
            'max_observed_ordinary':maxordinary,'max_observed_plans':maxplans,
            'HC_proved':False,'unbounded_restart_termination_proved':False,
            'seconds':round(time.monotonic()-start,3)}

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Do not disable checks')
    result=run();(ROOT/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
