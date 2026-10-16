"""Named prior constructions used as controls, not claimed newly discovered."""
from trace_arithmetic import Aff,Block,Schema
from isl_bridge import Context
B=('RRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLRRRRLRLLLLRRRR'
   'LRRLRRRRLLLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRLL')
assert len(B)==102
A='L'+B[75:]
STANDARD=('LRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLR')
assert len(A)==28 and len(STANDARD)==104

def triple_fold():
    n,m=Aff.var('n'),Aff.var('m')
    s=Schema(['n','m'],[Block(B),Block(A,n),Block(B),Block(A,m),Block(B)],
             domain='n>=0 and m>=0')
    return s,None

def three_sweep():
    n=Aff.var('n')
    s=Schema(['n'],[Block('RLLR',n),Block('LRLLRL'),Block('RLLR',n),Block('LRLLRL'),Block('LRRL',n)],
             heading=1,domain='n>=1')
    seed=s.segment_field([(0,-1,1,0,2*n),(0,4,1,0,2*n)])
    caps=s.point_field([(2*n,0),(2*n+1,1),(2*n+1,2),(2*n,3),(-1,3),(-2,2),(-2,1),(-1,0)])
    return s,seed.union(caps)

def standard_seed(word=STANDARD,heading=0):
    p=(0,0);h=heading;points=[]
    for c in word:
        points.append(p);h=(h+(1 if c=='R' else -1))%4
        v=((0,1),(1,0),(0,-1),(-1,0))[h];p=p[0]+v[0],p[1]+v[1]
    d=p;groups={}
    for i,(x,y) in enumerate(points):
        key=(d[1]*x-d[0]*y,x%abs(d[0]));k=x//d[0]
        groups.setdefault(key,[]).append((k,i,(x,y)))
    seed=set()
    for values in groups.values():
        v=sorted(values,key=lambda x:(-x[0],x[1]));lo=min(x[0] for x in v);hi=max(x[0] for x in v)
        assert all(word[i]==('R' if j%2==0 else 'L') for j,(k,i,q) in enumerate(v))
        a0,_,q0=v[0]
        for k in range(lo,hi):
            if sum(a>k for a,_,_ in v)%2:seed.add((q0[0]+(k-a0)*d[0],q0[1]+(k-a0)*d[1]))
    return seed,d

if __name__=='__main__':
    import sys,time,json
    name=sys.argv[1] if len(sys.argv)>1 else 'sweep'
    s,b=triple_fold() if name=='fold' else three_sweep()
    st=time.monotonic();print('schema',name,'phases',s.phase_count,flush=True)
    a=s.analyze(b,method='lexmin')
    print('good',a['good'],flush=True)
    print('seconds',time.monotonic()-st,flush=True)
    if 'final_black' in a:print('final',a['final_black'])
