"""Separate graph-pair implementation; imports no axis_wake code."""
from collections import Counter, defaultdict
from itertools import combinations, permutations
import json


def all_patterns(a,h):
    for bits in range(1<<((a-1)*(h-1))):
        grid=[[0]*a for _ in range(h)]
        for y in range(h-1):
            for x in range(a-1): grid[y][x]=(bits>>(y*(a-1)+x))&1
            grid[y][-1]=sum(grid[y])%2
        for x in range(a): grid[-1][x]=sum(grid[y][x] for y in range(h-1))%2
        yield {(x,y) for y in range(h) for x in range(a) if grid[y][x]}


def graph(a,O):
    edges=set(); rows=defaultdict(list); cols=defaultdict(list)
    for x,y in O: rows[y].append(x); cols[x].append(y)
    for y,xx in rows.items():
        xx.sort(); assert len(xx)%2==0
        for lo,hi in zip(xx[::2],xx[1::2]):
            edges.update(('H',x,y) for x in range(lo,hi))
    for x,yy in cols.items():
        yy.sort(); assert len(yy)%2==0
        for lo,hi in zip(yy[::2],yy[1::2]):
            edges.update(('V',x,y) for y in range(lo,hi))
    return edges


def character(a,G,O,convention):
    sk=[]; tk=[]; positive=0
    for axis,x,y in sorted(G):
        p=(x,y); q=((x+1)%a,y) if axis=='H' else (x,y+1)
        c=(x+y+convention)%2
        pos=c==(0 if axis=='H' else 1)
        s,t=(p,q) if pos else (q,p)
        # Checker-first order differs from the other implementation's row-major order.
        def key(v): return ((sum(v)+convention)%2,v[1],v[0],int(pos))
        sk.append(key(s)); tk.append(key(t)); positive+=pos
    inv=sum((sk[i]<sk[j])!=(tk[i]<tk[j])
            for i in range(len(sk)) for j in range(i+1,len(sk)))
    return (inv+positive+sum((x+y+convention)%2 for x,y in O))%2


def inversion(O):
    return sum(x<xx and y>yy for x,y in O for xx,yy in O)


def check():
    cases=Counter(); checks=Counter()
    for a,h in ((2,6),(4,4),(6,3)):
        for O in all_patterns(a,h):
            G=graph(a,O); q=(inversion(O)+len(O)//2)%2
            for c in (0,1):
                assert character(a,G,O,c)==q
                checks['sector_graphs']+=1
                for y in range(-1,h+1):
                    R={('H',x,y) for x in range(a)}
                    assert character(a,G^R,O,c)==q^1
                    checks['row_cycle_toggles']+=1
            for dx in range(a):
                M={((x+dx)%a,y) for x,y in O}
                assert inversion(M)%2==inversion(O)%2
                checks['seam_shifts']+=1
            cases[f'{a}x{h}']+=1
    for a in (2,4,6,8,16,64):
        yy=[2*10**(3*j) for j in range(a)]
        O={(j,yy[j]) for j in range(a-1)}|{(j+1,yy[j]) for j in range(a-1)}
        O|={(0,yy[-1]),(a-1,yy[-1])}
        assert inversion(O)==2*a-3
        assert all(sum((-1)**((x+y)%2) for xx,y in O if xx==x)%4==2 for x in range(a))
        assert all(sum((-1)**((x+y)%2) for x,yy0 in O if yy0==y)%4==0 for y in yy)
        checks['large_gap_staircases']+=1
    return {'schema':'axis-wake-independent-v1','windows':dict(cases),'checks':dict(checks)}


if __name__=='__main__': print(json.dumps(check(),indent=2,sort_keys=True))
