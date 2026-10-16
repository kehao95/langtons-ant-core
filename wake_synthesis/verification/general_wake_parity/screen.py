"""Necessary wake-only obstructions for non-axis Langton-ant highways.

PROOF.md, Theorems 1--3: exact edge reconstruction and quadratic port sign.
A passing screen is NOT a finite-seed realization certificate.
All coordinates and counts use Python integers; no period or spatial cap is used.
"""
from dataclasses import dataclass
from collections import defaultdict
from itertools import combinations
from typing import Iterable

@dataclass(frozen=True)
class Run:
    n:int
    step:int
    sy:int
    sx:int
    ty:int
    tx:int
    positive:int
    def edges(self):
        for i in range(self.n):
            yield ((self.sx,self.sy+self.step*i),(self.tx,self.ty+self.step*i),self.positive)

def ceildiv(x:int,y:int)->int:
    return -(-x//y)

def floor_sum(n:int,m:int,a:int,b:int)->int:
    """Sum floor((a*i+b)/m), i=0..n-1, by Euclidean lattice transposition."""
    if n<0 or m<=0:raise ValueError('floor-sum domain')
    ans=0
    while True:
        qa,a=divmod(a,m);qb,b=divmod(b,m)
        ans+=qa*n*(n-1)//2+qb*n
        y=a*n+b
        if y<m:return ans
        n,b=divmod(y,m)
        m,a=a,m

def pairs_leq(A:Run,B:Run,bound:int)->int:
    # Count sy_A + i*sA - sy_B - j*sB <= bound.
    T=bound-A.sy+B.sy;u=A.step;v=B.step;n=A.n;m=B.n
    lo=min(m,max(0,ceildiv(-T,v)))
    hi=min(m,max(0,ceildiv(u*n-T,v)))
    assert hi>=lo
    return (m-hi)*n+(hi-lo)+floor_sum(hi-lo,u,v,T+v*lo)

def run_inversions(A:Run,B:Run)->int:
    s=0 if (A.sx,A.positive)<(B.sx,B.positive) else -1
    delta=(A.ty-A.sy)-(B.ty-B.sy)
    t=-delta+(0 if (A.tx,A.positive)<(B.tx,B.positive) else -1)
    lo,hi=sorted((s,t))
    return pairs_leq(A,B,hi)-pairs_leq(A,B,lo)

def canonical(q,d):
    a,b=d;x,y=q;return x%a,y-(x//a)*b

def runs_for(O,d):
    a,b=d
    if a<=0 or b==0 or (a+b)%2:raise ValueError('canonical non-axis checker-even drift required')
    O=set(canonical(q,d) for q in O)
    hg=defaultdict(list);vg=defaultdict(list)
    for x,y in O:
        k=(y-y%abs(b))//b
        hg[y%abs(b)].append(x-k*a);vg[x].append(y)
    runs=[]
    for Y,xs in sorted(hg.items()):
        xs.sort()
        if len(xs)%2:return None
        for L,R in zip(xs[::2],xs[1::2]):
            for r in range(a):
                low=ceildiv(L-r,a);high=(R-1-r)//a
                stride=1 if a%2==0 else 2
                for parity in range(stride):
                    first=low+(parity-low)%stride;last=high-(high-parity)%stride
                    if first>last:continue
                    n=(last-first)//stride+1;k=last if b>0 else first
                    ly=Y-k*b;rx=(r+1)%a;ry=Y-(k+int(r==a-1))*b
                    positive=int((r+Y+a*k)%2==0)
                    if positive:sx,sy,tx,ty=r,ly,rx,ry
                    else:sx,sy,tx,ty=rx,ry,r,ly
                    runs.append(Run(n,abs(b)*stride,sy,sx,ty,tx,positive))
    for x,ys in sorted(vg.items()):
        ys.sort()
        if len(ys)%2:return None
        for L,R in zip(ys[::2],ys[1::2]):
            for parity in range(2):
                y=L+(parity-L)%2
                if y>=R:continue
                n=(R-1-y)//2+1;positive=int((x+y)%2==1)
                sy=y if positive else y+1;ty=y+1 if positive else y
                runs.append(Run(n,2,sy,x,ty,x,positive))
    return sorted(runs,key=lambda r:(r.sy,r.sx,r.positive,r.ty,r.tx,r.step,r.n))

def touches(run,q,source):
    x,y=q;rx=run.sx if source else run.tx;ry=run.sy if source else run.ty
    z=y-ry
    return x==rx and z>=0 and z%run.step==0 and z//run.step<run.n

def compressed_signature(O,d,detail=False):
    O=set(canonical(q,d) for q in O);runs=runs_for(O,d)
    if runs is None:return None
    E=sum(run_inversions(A,B) for A,B in combinations(runs,2))%2
    Np=sum(r.n for r in runs if r.positive)%2
    endpoint=sum(int(touches(r,q,True))+int(touches(r,q,False)) for q in O for r in runs if r.positive)%2
    C=sum(sum(q)%2 for q in O)%2
    if endpoint:
        raise RuntimeError("endpoint-port cancellation failed")
    L=(Np+C)%2
    F=E^L
    if detail:return dict(signature=F,E=E,L=L,positive_edges_parity=Np,endpoint_port_parity=endpoint,C_parity=C,runs=len(runs),odd_edges=sum(r.n for r in runs))
    return F


def screen(wake: Iterable[tuple[int, int]], drift: tuple[int, int],
           sector: int = 1) -> dict:
    """Return EXCLUDED or NOT_EXCLUDED, never a positive realization claim.

    ``wake`` contains distinct full-drift classes, given by lattice representatives.
    ``sector`` optionally chooses either of the equivalent checker conventions.
    The obstruction is independent of this choice (PROOF.md, Lemma 4); no
    physical heading hypothesis is imposed. Negative x drift is half-turned.
    Axis drift is explicitly unsupported, not an exclusion.
    """
    def point(q):
        if not isinstance(q, (list, tuple)) or len(q) != 2 or any(type(v) is not int for v in q):
            raise ValueError("coordinates must be pairs of integers")
        return tuple(q)
    d = point(drift)
    points = [point(q) for q in wake]
    if sector not in (-1, 1) or type(sector) is not int:
        raise ValueError("sector must be +1 or -1")
    if not all(d):
        raise ValueError("non-axis nonzero drift is required; axis case is unsupported")
    if (d[0] + d[1]) % 2:
        return {"status": "EXCLUDED", "reason": "checker displacement parity"}
    if sector == -1:
        points = [(x, y + 1) for x, y in points]
    if d[0] < 0:
        d = (-d[0], -d[1]); points = [(-x, -y) for x, y in points]
    a, b = d
    O = {canonical(q, d) for q in points}
    if len(O) != len(points):
        raise ValueError("duplicate full-drift wake class")
    g = len(O)
    base = {"drift": list(d), "growth": g, "orientation_convention": 1}
    if g == 0 or g % 4:
        return dict(base, status="EXCLUDED", reason="positive growth divisible by four")
    if g < 2 * max(a, abs(b)):
        return dict(base, status="EXCLUDED", reason="signed-residue density bound")
    charges = []
    for axis, v in enumerate(d):
        row = [0] * abs(v)
        for q in O:
            row[q[axis] % abs(v)] += 1 if sum(q) % 2 == 0 else -1
        charges.append(row)
    if any(c % 4 != 2 for row in charges for c in row):
        return dict(base, status="EXCLUDED", reason="signed mod-four residue", charges=charges)
    winding = sum(y // abs(b) for x, y in O) % 2
    if winding != 1:
        return dict(base, status="EXCLUDED", reason="odd-edge winding parity", winding=winding)
    data = compressed_signature(O, d, detail=True)
    if data is None:
        raise RuntimeError("signed residues did not give even fibre populations")
    required = (1 + a) % 2
    return dict(base, status="NOT_EXCLUDED" if data["signature"] == required else "EXCLUDED",
                reason="quadratic port sign", required_signature=required,
                winding=winding, charges=charges, **data)


def main():
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path,
                        help='JSON object with drift, wake, and optional sector')
    args = parser.parse_args()
    value = json.loads(args.input.read_text())
    print(json.dumps(screen(value["wake"], value["drift"], value.get("sector", 1)), indent=2))


if __name__ == "__main__":
    main()
