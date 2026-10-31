"""Independent exact linear presentations; these do not prove infinite coverage.

Raw equations contain one unknown for EACH nonzero color at EACH site, not
pre-assumed R/L increments or the derived spatial weight formula. The Smith
calculation uses SymPy over Z. Compact GF(2) ranks use integer XOR elimination.
"""
from __future__ import annotations
from itertools import product

D=((0,1),(1,0),(0,-1),(-1,0))


def rank_binary(rows):
    pivots={}
    for word in rows:
        while word:
            p=word.bit_length()-1
            if p not in pivots:
                pivots[p]=word
                break
            word^=pivots[p]
    return len(pivots)


def compact_system(rule, side):
    cells=list(product(range(side),repeat=2));inside=set(cells)
    ids={('f',x,y,c):i for i,(x,y,c) in enumerate((x,y,c)for x,y in cells for c in range(1,len(rule)))}
    for x,y in cells:
        for h in range(4):
            if (h-x-y)%2==0:ids['p',x,y,h]=len(ids)
    rows=[]
    for x,y in product(range(-1,side+1),repeat=2):
        for h in range(4):
            if (h-x-y)%2:continue
            for c,ch in enumerate(rule):
                terms={}
                def add(key,value):
                    if key in ids:terms[ids[key]]=terms.get(ids[key],0)+value
                cc=(c+1)%len(rule)
                if c:add(('f',x,y,c),-1)
                if cc:add(('f',x,y,cc),1)
                hh=(h+(1 if ch=='R'else-1))%4;dx,dy=D[hh]
                add(('p',x+dx,y+dy,hh),1);add(('p',x,y,h),-1)
                rows.append(terms)
    return ids,rows


def compact_basis(rule,side,ids):
    vectors=[]
    for x,y in product(range(side-1),repeat=2):
        counted='R' if (x+y)%2==0 else 'L'
        if rule.count(counted)%2:continue
        face={(x,y),(x+1,y),(x,y+1),(x+1,y+1)}
        turning='L' if counted=='R'else'R'
        h=2 if turning=='L'else 3;xx,yy=x,y;cycle=set()
        for _ in range(4):
            cycle.add((xx,yy,h));h=(h+(1 if turning=='R'else-1))%4
            dx,dy=D[h];xx+=dx;yy+=dy
        v=0
        for key,i in ids.items():
            kind,xx,yy,z=key
            bit=(rule[:z].count(counted)%2 if kind=='f' and (xx,yy)in face else
                 int((xx,yy,z)in cycle)if kind=='p'else 0)
            if bit:v|=1<<i
        vectors.append(v)
    return vectors


def compact_rank(rule,side):
    ids,rows=compact_system(rule,side)
    words=[sum(1<<i for i,a in row.items()if a%2)for row in rows]
    basis=compact_basis(rule,side,ids)
    for v in basis:
        if any((r&v).bit_count()%2 for r in words):raise AssertionError('basis violates raw local equation')
    rank=rank_binary(words);brank=rank_binary(basis)
    if len(ids)-rank!=brank or brank!=len(basis):raise AssertionError('compact basis incomplete on the finite test box')
    return {'variables':len(ids),'rank':rank,'basis_dimension':brank,'raw_equations':len(rows)}


def periodic_matrix(rule,side):
    import sympy as sp
    cells=list(product(range(side),repeat=2))
    ids={('f',x,y,c):i for i,(x,y,c) in enumerate((x,y,c)for x,y in cells for c in range(1,len(rule)))}
    for x,y in cells:
        for h in range(4):
            if (h-x-y)%2==0:ids['p',x,y,h]=len(ids)
    k=len(ids);rows=[]
    for x,y in cells:
        for h in range(4):
            if (h-x-y)%2:continue
            for c,ch in enumerate(rule):
                row=[0]*(k+1);cc=(c+1)%len(rule)
                if c:row[ids['f',x,y,c]]-=1
                if cc:row[ids['f',x,y,cc]]+=1
                hh=(h+(1 if ch=='R'else-1))%4;dx,dy=D[hh]
                row[ids['p',(x+dx)%side,(y+dy)%side,hh]]+=1
                row[ids['p',x,y,h]]-=1;row[k]-=1;rows.append(row)
    return sp.Matrix(rows),k


def smith_signature(matrix):
    from sympy.matrices.normalforms import smith_normal_form
    from sympy.polys.domains import ZZ
    diag=smith_normal_form(matrix,domain=ZZ)
    values=[abs(int(diag[i,i]))for i in range(min(diag.shape))if diag[i,i]]
    product=1
    for a in values:product*=a
    return len(values),product,[a for a in values if a>1]


def phase_order(rule,side):
    import sympy as sp
    matrix,k=periodic_matrix(rule,side)
    rank,torsion,_=smith_signature(matrix)
    row=[0]*matrix.cols;row[k]=1
    rank2,torsion2,_=smith_signature(matrix.col_join(sp.Matrix([row])))
    if rank!=rank2 or torsion%torsion2:raise AssertionError('phase generator was not torsion')
    return torsion//torsion2


def compact_smith(rule,side):
    import sympy as sp
    ids,rows=compact_system(rule,side)
    matrix=sp.zeros(len(rows),len(ids))
    for j,row in enumerate(rows):
        for i,a in row.items():matrix[j,i]=a
    rank,_,factors=smith_signature(matrix)
    expected=len(compact_basis(rule,side,ids))
    if rank!=len(ids)or factors!=[2]*expected:raise AssertionError('compact integral module mismatch')
    return {'rule':rule,'side':side,'variables':len(ids),'torsion_factors':factors}
