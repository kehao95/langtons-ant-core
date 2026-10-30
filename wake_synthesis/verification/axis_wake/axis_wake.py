"""Exact necessary wake screen for horizontal full drift (a, 0).

No SAT solver, floating point, time cutoff, or simulation is used by screen().
Passing is NOT_EXCLUDED, never a certificate of a realizable highway.
"""
from __future__ import annotations
import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable

Point = tuple[int, int]
Edge = tuple[Point, int, Point]
DIR = ((0, 1), (1, 0), (0, -1), (-1, 0))


def normalize(a: int, points: Iterable[Point]) -> set[Point]:
    if type(a) is not int or a <= 0:
        raise ValueError("The horizontal full displacement must be a positive integer")
    out = set()
    for point in points:
        if len(point) != 2 or any(type(v) is not int for v in point):
            raise ValueError("Every point must have two integer coordinates")
        x, y = point
        out.add((x % a, y))
    return out


def fibers(O: set[Point]):
    rows, cols = defaultdict(list), defaultdict(list)
    for x, y in O:
        rows[y].append(x)
        cols[x].append(y)
    return ({y: sorted(xs) for y, xs in rows.items()},
            {x: sorted(ys) for x, ys in cols.items()})


def even_fibers(O: set[Point]) -> None:
    rows, cols = fibers(O)
    if any(len(v) % 2 for v in (*rows.values(), *cols.values())):
        raise ValueError("The endpoint identity requires even row and column populations")


def inversions(values: list[int]) -> int:
    """Count strict inversions by merge sort (equal entries are not inversions)."""
    def rec(xs):
        if len(xs) < 2:
            return xs, 0
        L, c = rec(xs[:len(xs)//2])
        R, d = rec(xs[len(xs)//2:])
        i = j = 0
        out = []
        c += d
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                out.append(L[i]); i += 1
            else:
                out.append(R[j]); j += 1
                c += len(L)-i
        return out + L[i:] + R[j:], c
    return rec(values)[1]


def endpoint(a: int, points: Iterable[Point]) -> dict:
    O = normalize(a, points)
    even_fibers(O)
    I = inversions([x for x, y in sorted(O, key=lambda p: (p[1], p[0]))])
    return {"growth": len(O), "strict_inversions": I,
            "inversion_parity": I % 2, "seam_zero_character": (I+len(O)//2) % 2}


def prefilters(a: int, O: set[Point]) -> list[str]:
    """Established necessary conditions, checked without allocating a-sized arrays."""
    rows, cols = fibers(O)
    g = len(O)
    reasons = []
    if a % 2: reasons.append("odd_axis_displacement")
    if not g or g % 4: reasons.append("growth_not_positive_multiple_of_four")
    if g < 2*a: reasons.append("density_below_twice_displacement")
    if any(len(xs) % 2 for xs in rows.values()): reasons.append("odd_row_population")
    if any(len(ys) % 2 for ys in cols.values()): reasons.append("odd_column_population")
    if len(cols) != a or any(sum((-1)**((x+y) % 2) for y in ys) % 4 != 2
                             for x, ys in cols.items()):
        reasons.append("signed_column_residue")
    if any(sum((-1)**((x+y) % 2) for x in xs) % 4 for y, xs in rows.items()):
        reasons.append("signed_exact_row")
    return reasons


def screen(a: int, points: Iterable[Point]) -> dict:
    O = normalize(a, points)
    failures = prefilters(a, O)
    if failures:
        return {"status": "EXCLUDED_BY_ESTABLISHED_PREFILTER", "reasons": failures,
                "growth": len(O), "drift": [a, 0]}
    result = endpoint(a, O)
    result.update(drift=[a, 0], status=("EXCLUDED_BY_AXIS_WAKE_PARITY"
                  if result["inversion_parity"] else "NOT_EXCLUDED"))
    return result


def edge(a: int, p: Point, h: int) -> Edge:
    x, y = p; dx, dy = DIR[h]
    return ((x % a, y), h, ((x+dx) % a, y+dy))


def horizontal(a: int, x: int, y: int) -> Edge:
    return edge(a, (x, y), 1) if (x+y) % 2 == 0 else edge(a, (x+1, y), 3)


def vertical(a: int, x: int, y: int) -> Edge:
    return edge(a, (x, y), 0) if (x+y) % 2 == 1 else edge(a, (x, y+1), 2)


def row_cycle(a: int, y: int) -> set[Edge]:
    return {horizontal(a, x, y) for x in range(a)}


def literal_graph(a: int, O: set[Point], cap: int = 200000) -> set[Edge]:
    """Finite regression oracle. Its size guard raises, and is not an exclusion."""
    even_fibers(O)
    rows, cols = fibers(O)
    size = sum(xs[i+1]-xs[i] for xs in rows.values() for i in range(0,len(xs),2))
    size += sum(ys[i+1]-ys[i] for ys in cols.values() for i in range(0,len(ys),2))
    if size > cap:
        raise ValueError("Literal graph size guard; use endpoint() or run_character()")
    G = set()
    for y, xs in rows.items():
        for i in range(0, len(xs), 2):
            for x in range(xs[i], xs[i+1]): G.add(horizontal(a,x,y))
    for x, ys in cols.items():
        for i in range(0, len(ys), 2):
            for y in range(ys[i], ys[i+1]): G.add(vertical(a,x,y))
    return G


def edge_character(G: set[Edge], O: set[Point], order=None, sector: int = 0) -> dict:
    """Permutation-sign implementation; a=2 parallel ports remain distinct."""
    key = (lambda p: (p[1],p[0])) if order is None else (lambda p: order[p])
    def sk(e): return (key(e[0]), int(e[1] in (0,1)))
    def tk(e): return (key(e[2]), int(e[1] in (0,1)))
    S, T = sorted(G,key=sk), sorted(G,key=tk)
    if len({sk(e) for e in G}) != len(G) or len({tk(e) for e in G}) != len(G):
        raise ValueError("Duplicate directed source or target ports")
    target = {e:i for i,e in enumerate(T)}
    perm = [target[e] for e in S]
    seen, cycles = set(), 0
    for i in range(len(perm)):
        if i in seen: continue
        cycles += 1
        while i not in seen:
            seen.add(i); i = perm[i]
    E = (len(G)-cycles) % 2
    N = sum(h in (0,1) for p,h,q in G)
    C = sum((x+y+sector) % 2 for x,y in O)
    return {"character": (E+N+C)%2, "edge_sign": E,
            "edges": len(G), "positive_edges": N, "checker_term": C}


@dataclass(frozen=True)
class Run:
    sx: int
    sy: int
    tx: int
    ty: int
    port: int
    length: int
    axis: str


def edge_runs(a: int, O: set[Point]) -> list[Run]:
    even_fibers(O)
    rows, cols = fibers(O)
    runs = []
    for y, xs in rows.items():
        for i in range(0,len(xs),2):
            for x in range(xs[i],xs[i+1]):
                p,h,q = horizontal(a,x,y)
                runs.append(Run(*p,*q,int(h in (0,1)),1,"H"))
    for x, ys in cols.items():
        for i in range(0,len(ys),2):
            lo,hi=ys[i:i+2]
            for y in (lo,lo+1):
                n=(hi-1-y)//2+1
                if n <= 0: continue
                p,h,q=vertical(a,x,y)
                runs.append(Run(*p,*q,int(h in (0,1)),n,"V"))
    return runs


def pair_inversions(A: Run, B: Run) -> int:
    # Source and target inequalities reduce to thresholds on i-j.
    s=(B.sy-A.sy-1+int((A.sx,A.port)<(B.sx,B.port)))//2
    t=(B.ty-A.ty-1+int((A.tx,A.port)<(B.tx,B.port)))//2
    if abs(s-t)>2: raise AssertionError("Unexpected unit-edge threshold span")
    return sum(max(0,min(A.length-1,B.length-1+k)-max(0,k)+1)
               for k in range(min(s,t)+1,max(s,t)+1))


def run_character(a: int, O: set[Point]) -> dict:
    runs=edge_runs(a,O)
    pairs={"HH":0,"HV":0,"VV":0}
    for A,B in combinations(runs,2):
        pairs[''.join(sorted((A.axis,B.axis)))]+=pair_inversions(A,B)
    E=sum(pairs.values())
    N=sum(r.length for r in runs if r.port)
    C=sum((x+y)%2 for x,y in O)
    return {"character":(E+N+C)%2,"inversions":E,"positive_edges":N,
            "edges":sum(r.length for r in runs),"runs":len(runs),"pair_counts":pairs}


def closed_masks(a: int, height: int):
    """All even-row/even-column indicators in a finite window, without omissions."""
    for mask in range(1<<((a-1)*(height-1))):
        O=set()
        for y in range(height-1):
            for x in range(a-1):
                if mask>>(y*(a-1)+x)&1: O.add((x,y))
            if sum((x,y) in O for x in range(a-1))%2: O.add((a-1,y))
        for x in range(a):
            if sum((x,y) in O for y in range(height-1))%2: O.add((x,height-1))
        yield O


def staircase(a: int, heights: list[int]) -> set[Point]:
    if a < 2 or a%2 or len(heights)!=a or any(x>=y for x,y in zip(heights,heights[1:])):
        raise ValueError("Require positive even a and a strictly increasing height list of length a")
    if len({y%2 for y in heights})!=1: raise ValueError("Heights must have one parity")
    O={(j,y) for j,y in enumerate(heights[:-1])}
    O|={(j+1,y) for j,y in enumerate(heights[:-1])}
    return O|{(0,heights[-1]),(a-1,heights[-1])}


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path,help='JSON object {"a":4,"wake":[[x,y],...]}')
    args=parser.parse_args()
    data=json.loads(args.input.read_text())
    print(json.dumps(screen(data["a"],data["wake"]),indent=2))
