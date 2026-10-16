#!/usr/bin/env python3
"""Exact tests for the mixed-wake parity theorem, with no numerical solver.

--enumerate also repeats the bounded growth-eight screen; that finite screen
is explicitly not a periodic-realizability decision or an all-growth-eight proof.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, random
from collections import Counter,defaultdict
from pathlib import Path
import mixed_wake as mw
ROOT=Path(__file__).resolve().parent
MOVES=((0,1),(1,0),(0,-1),(-1,0))
STANDARD='LRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLR'


def require(test,message):
    if not test:raise AssertionError(message)


class BoolPoly:
    """Exact F2[z_0,...,z_8]/(z_i^2-z_i), as XOR sets of monomial masks."""
    def __init__(self,value=0):
        self.terms=({0} if value&1 else set()) if isinstance(value,int) else set(value)
    @classmethod
    def var(cls,i):return cls({1<<i})
    def __xor__(self,other):
        if isinstance(other,int):other=BoolPoly(other)
        return BoolPoly(self.terms^other.terms)
    __rxor__=__xor__
    def __mul__(self,other):
        if isinstance(other,int):other=BoolPoly(other)
        result=set()
        for a in self.terms:
            for b in other.terms:
                c=a|b
                if c in result:result.remove(c)
                else:result.add(c)
        return BoolPoly(result)
    __rmul__=__mul__


def kernel():
    count=0
    for state in itertools.product((0,1),repeat=5):
        for letters in itertools.product((0,1),repeat=4):
            target,cost=mw.kernel_step(state,letters)
            require(cost==mw.H(state)^mw.H(target),'local F2 identity')
            count+=1
    variables=[BoolPoly.var(i) for i in range(9)]
    target,cost=mw.kernel_step(variables[:5],variables[5:])
    residual=cost^mw.H(variables[:5])^mw.H(target)
    require(not residual.terms,'Boolean polynomial residual is nonzero')
    return {'truth_cases':count,'symbolic_variables':9,'symbolic_residual_monomials':0}


def inv(bits):
    ones=answer=0
    for b in bits:
        if b:ones+=1
        else:answer^=ones%2
    return answer


def permutation_sign(values):
    seen=set();cycles=0
    for start in range(len(values)):
        if start in seen:continue
        cycles+=1;i=start
        while i not in seen:seen.add(i);i=values[i]
    return (len(values)-cycles)%2


def geometric(word,h=0):
    x=y=0;points=[];headings=[]
    for c in word:
        points.append((x,y));headings.append(h)
        h=(h+(1 if c=='R' else -1))%4
        dx,dy=MOVES[h];x+=dx;y+=dy
    return points,headings,(x,y),h


def rank_factorization(word):
    points,hs,d,h=geometric(word)
    require(d==(2,-2) and h==0,'wrong geometric control endpoint')
    groups=defaultdict(list);ports=[];edges=Counter()
    for i,((x,y),h) in enumerate(zip(points,hs)):
        t=x+y;out=(h+(1 if word[i]=='R' else -1))%4
        ports.append((int(h in (0,1)),int(out in (0,1))))
        groups[t,x%2].append((i-len(word)*(x//2),i))
        edges[t,x%2,int(out in(0,1))]+=1
    ranks={};ordered={};K=J=Lraw=0;input_order=[];output_order=[]
    for key in sorted(groups):
        seq=[i for tau,i in sorted(groups[key])];ordered[key]=seq
        ranks.update({i:k for k,i in enumerate(seq)})
        a=[ports[i][0] for i in seq];b=[ports[i][1] for i in seq];m=len(seq)
        J^=inv(a)^inv(b)
        Lraw^=((sum(a)+sum(b))*(m-1))%2
        if key[0]%2:Lraw^=(m*(m-1)//2)%2
        input_order.extend(sorted(seq,key=lambda i:(ports[i][0],ranks[i])))
        output_order.extend(sorted(seq,key=lambda i:(ports[i][1],ranks[i])))
    K=sum(ranks[i] for i,c in enumerate(word) if c=='L')%2
    where={i:j for j,i in enumerate(input_order)}
    E=permutation_sign([where[(i+1)%len(word)] for i in output_order])
    oddedges=sorted(e for e,n in edges.items() if n%2)
    E_blocks=0
    for i,a in enumerate(oddedges):
        for b in oddedges[i+1:]:
            def target(edge):
                t,r,pos=edge;hd=(1 if pos else 3) if t%2==0 else (0 if pos else 2)
                dx,dy=MOVES[hd];return t+dx+dy,(r+dx)%2,pos
            E_blocks^=target(a)>target(b)
    require(E==E_blocks,'edge block order and full event permutation disagree')
    require(J^E==1 and K==J^Lraw and K==1^E^Lraw,'general rank factorization')
    return len(groups)


def words_from_steps(us,vs):
    vprev=1;word=[]
    for u,v in zip(us,vs):
        word.append('R' if u==vprev else 'L')
        word.append('L' if u==v else 'R')
        vprev=v
    return ''.join(word)


def raw_words():
    counts={};group_checks=0
    for M in (4,6,8,10):
        total=0
        for positive_u in itertools.combinations(range(M),(M+2)//2):
            U=set(positive_u);us=tuple(1 if j in U else -1 for j in range(M))
            for positive_v in itertools.combinations(range(M-1),(M-4)//2):
                V=set(positive_v);vs=tuple(1 if j in V else -1 for j in range(M-1))+(1,)
                group_checks+=rank_factorization(words_from_steps(us,vs));total+=1
        counts[2*M]=total
    require(counts=={8:4,12:75,16:1176,20:17640},'geometric enumeration coverage')
    return {'geometric_words_by_length':counts,'total':sum(counts.values()),'class_checks':group_checks,
            'scope':'arbitrary geometric words, not asserted dynamically realizable'}


def layer_controls():
    sites=[(t,r) for t in range(8) for r in (0,1)]
    closed=residue=0
    for mask in range(1<<len(sites)):
        O={sites[i] for i in range(len(sites)) if mask>>i&1}
        q0,q1,c0,c1=mw.counts(O)
        if len({q0%2,q1%2,c0%2,c1%2})!=1:continue
        r=mw.layer_reconstruction(O)
        require(r['closed'],'finite edge parity support')
        I=sum(t<u for t,l in O if t%2==0 for u,k in O if u%2)
        value=(I+len(O)*(len(O)-1)//2+q0)%2
        require(r['combined']==value,'unreduced wake sign formula')
        closed+=1
        if O and len(O)%4==0 and mw.residue_ok(O):
            p=mw.parity_screen(O)
            require(p['actual_parity']==value,'compact parity screen')
            residue+=1
    return {'enumerated_wakes':1<<len(sites),'closed_mod2_wakes':closed,'signed_residue_wakes':residue}


def standard_tests():
    count=0;full=0
    for phase in range(104):
        word=STANDARD[phase:]+STANDARD[:phase]
        # The normalized positive drift is obtained by the appropriate heading.
        for heading in range(4):
            points,hs,d,final=geometric(word,heading)
            if d!=(2,-2):continue
            require(final==heading,'heading reset')
            groups=defaultdict(list)
            for i,(x,y) in enumerate(points):groups[x+y,x%2].append((i-104*(x//2),i))
            O=set();seed=set()
            for key,events in groups.items():
                seq=sorted(events)
                require(all(word[i]==('R' if k%2==0 else 'L') for k,(tau,i) in enumerate(seq)), 'stable P104 class word')
                if len(seq)%2:O.add(key)
            sig=1 if heading%2==0 else -1
            report=mw.parity_screen(O,sig)
            require(report['status']=='NOT_EXCLUDED','standard rejected')
            normalized=mw.validate(O,sig)
            require(mw.layer_reconstruction(normalized)['combined']==1,'standard complete layer sign')
            # Rank factorization is independently checked on vertical-N-normalized phases below.
            count+=1
            if heading==0:
                rank_factorization(word);full+=1
    require(count==104,'all standard phases')
    return {'standard_phases':count,'full_rank_factorizations':full,'class_turns_checked':104*104}


def shape_controls():
    table=[]
    for seq in sorted(set(itertools.permutations('QQCC'))):
        results=[]
        for qlane,clane in itertools.product((0,1),repeat=2):
            t=1;levels=[]
            for kind in seq:
                t+=1
                if t%2!=(kind=='C'):t+=1
                levels.append(t)
            hi=t+1+(t%2==1)
            O=mw.paired_family((1,hi,levels),qlane,clane)
            p=mw.parity_screen(O)
            expected='EXCLUDED' if ''.join(seq) in ('QCQC','CQCQ') else 'NOT_EXCLUDED'
            require(p['status']==expected,'interleaving pattern table')
            results.append(p['status'])
        table.append({'sequence':''.join(seq),'lane_choices':4,'result':results[0]})
    rng=random.Random(20261015);wide=0
    for _ in range(256):
        seq=rng.choice(('QCQC','CQCQ'))
        t=1;levels=[]
        for c in seq:
            t+=2*rng.randrange(1,10**40)+1
            if t%2!=(c=='C'):t+=1
            levels.append(t)
        hi=t+2*rng.randrange(1,10**40)+1
        if hi%2==0:hi+=1
        O=mw.paired_family((1,hi,levels),rng.randrange(2),rng.randrange(2))
        require(mw.parity_screen(O)['status']=='EXCLUDED','unbounded-gap arithmetic test')
        shifted={(t+1,r) for t,r in O}
        require(mw.parity_screen(shifted,-1)['status']=='EXCLUDED','checker-sector translation')
        wide+=1
    # Four Q internal classes and only the four extremal C classes are forbidden.
    saturated=0
    for layers in itertools.combinations(range(2,14,2),4):
        for lane in (0,1):
            O={(1,0),(1,1),(15,0),(15,1)}|{(t,lane) for t in layers}
            require(mw.parity_screen(O)['status']=='EXCLUDED','saturated-extrema Q-only interior')
            saturated+=1
    return {'interior_order_types':table,'huge_gap_cases':wide,'saturated_extrema_cases':saturated}


def enumeration(widths):
    report=[]
    for W in widths:
        raw=old=reject=passn=0;bytype=defaultdict(lambda:[0,0])
        sites=[(t,r) for t in range(2,W+1) for r in (0,1)]
        hasher=hashlib.sha256()
        for lr,hr in itertools.product(((0,),(1,),(0,1)),repeat=2):
            boundary={(1,r) for r in lr}|{(W+1,r) for r in hr}
            for inner in itertools.combinations(sites,8-len(boundary)):
                raw+=1;O=boundary|set(inner)
                if not mw.residue_ok(O):continue
                q0,q1,c0,c1=mw.counts(O)
                if q0+q1==0 or c0+c1==0:continue
                old+=1;p=mw.parity_screen(O)
                excluded=p['status']=='EXCLUDED';reject+=excluded;passn+=not excluded
                bytype[q0,c0,c1,q1][int(not excluded)]+=1
                hasher.update((repr(sorted(O))+':'+str(int(excluded))+'\n').encode())
        report.append({'width':W,'raw_wakes':raw,'pass_prior_residues_and_mixing':old,
                       'excluded_by_new_parity':reject,'not_excluded':passn,
                       'by_residue_matrix':{str(k):{'excluded':v[0],'not_excluded':v[1]} for k,v in sorted(bytype.items())},
                       'stream_sha256':hasher.hexdigest(),
                       'scope':'complete wake arithmetic screen at this width; no accepted realization claim'})
        print('SCREEN',W,old,reject,passn,flush=True)
    return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--enumerate',action='store_true');args=parser.parse_args()
    report={'schema':'langton-mixed-wake-parity-v1','status':'passed','kernel':kernel()}
    print('kernel passed',flush=True)
    report['raw_event_order']=raw_words();print('rank factorization passed',flush=True)
    report['layer_controls']=layer_controls();print('layer identity passed',flush=True)
    report['standard']=standard_tests();report['shapes']=shape_controls()
    bad={(1,0),(1,1),(2,0),(3,0),(4,1),(5,1),(11,0),(11,1)}
    good={(1,0),(1,1),(2,0),(3,0),(5,1),(6,1),(11,0),(11,1)}
    report['example']={'excluded':{'wake':sorted(bad),'test':mw.parity_screen(bad)},
                       'not_excluded':{'wake':sorted(good),'test':mw.parity_screen(good)}}
    require(report['example']['excluded']['test']['status']=='EXCLUDED','negative example')
    require(report['example']['not_excluded']['test']['status']=='NOT_EXCLUDED','scope control')
    if args.enumerate:report['bounded_growth8_screen']=enumeration((10,12,14))
    for value,sig in [([(1,0),(1,0)],1),([(1,2)],1),([(1.5,0)],1),([(1,0)],0)]:
        try:mw.parity_screen(value,sig)
        except ValueError:pass
        else:raise AssertionError('invalid input accepted')
    for drift in ((1,-1),(4,-4),(2,0)):
        try:mw.parity_screen(bad,drift=drift)
        except ValueError:pass
        else:raise AssertionError('unsupported full drift accepted')
    report['unsupported_drift_rejections']=3
    report['source_sha256']={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ('mixed_wake.py','check.py')}
    report['scope']={'all_growth8_excluded':False,'finite_nonstandard_seed_found':False,'HC_proved':False,
                     'Lean_formalized':False,'externally_reviewed':False,'pass_means_realizable':False}
    name='check_results_full.json' if args.enumerate else 'check_results.json'
    (ROOT/name).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
