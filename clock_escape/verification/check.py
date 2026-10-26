#!/usr/bin/env python3
"""Independent exact clock audit; stdlib only, no repository simulator imports."""
from array import array
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

if sys.flags.optimize:
    raise SystemExit('Assertions are required; do not use -O')
HERE = Path(__file__).resolve().parent
D = ((0, 1), (1, 0), (0, -1), (-1, 0))


def step(black, p, h):
    """Integer-vector rotation, deliberately independent of cyclic heading arithmetic."""
    dx, dy = D[h]
    dx, dy = (-dy, dx) if p in black else (dy, -dx)
    return black ^ {p}, (p[0]+dx, p[1]+dy), D.index((dx, dy))


def phi(black, p, h, r, c):
    parity = lambda q: 1-2*((q[0]+q[1]) % 2)
    sigma = parity(p)*(1 if h % 2 == 0 else -1)
    u, v = r**(sum(p)-c), r**(c-sum(p))
    pose = 2*((u-r*v) if h < 2 else (v-r*u))/(r+1)
    return -sigma*sum((parity(q)*(r**(sum(q)-c)+r**(c-sum(q))) for q in black), Q(0))+pose


def bound(n, r):
    field = sum((r**(x+y-n+1)+r**(n-1-x-y) for x in range(n) for y in range(n)), Q(0))
    pose = 2*(r**(n-1)-r**(1-n))
    budget = (field+pose)/(2*(r-3)/(r+1))
    return budget.numerator//budget.denominator+1


def closed_bound(n, r):
    value = (r+1)/(r-3)*(r**(1-n)*(r**n-1)**2/(r-1)**2+r**(n-1)-r**(1-n))
    return value.numerator//value.denominator+1


def square_graph(n):
    """All colourings, positions and headings, no symmetry pruning.

    Each graph vertex is evaluated once. -1 marks the current DFS stack:
    a confined cycle fails the audit rather than hanging the search.
    """
    poses = 4*n*n
    total = poses*(1 << (n*n))
    distance = array('i', [0])*total
    successors = []
    for cell in range(n*n):
        x, y = divmod(cell, n)
        successors.append([((x+dx)*n+y+dy)*4+h
                           if 0 <= x+dx < n and 0 <= y+dy < n else -1
                           for h, (dx, dy) in enumerate(D)])
    longest = 0
    witness = None
    for seed in range(total):
        if distance[seed]:
            continue
        node = seed
        path = []
        while node >= 0 and distance[node] == 0:
            distance[node] = -1
            path.append(node)
            mask, pose = divmod(node, poses)
            cell, h = divmod(pose, 4)
            black = (mask >> cell) & 1
            new_h = (h+(3 if black else 1)) % 4
            new_pose = successors[cell][new_h]
            node = (mask ^ (1 << cell))*poses+new_pose if new_pose >= 0 else -1
        assert node < 0 or distance[node] > 0, 'Confined cycle found'
        tail = 0 if node < 0 else distance[node]
        for old in reversed(path):
            tail += 1
            distance[old] = tail
            if tail > longest:
                longest, witness = tail, old
    mask, pose = divmod(witness, poses)
    cell, h = divmod(pose, 4)
    initial = {(x, y) for x, y in product(range(n), repeat=2) if mask >> (x*n+y) & 1}
    black, p, heading = initial, divmod(cell, n), h
    replay = 0
    while 0 <= p[0] < n and 0 <= p[1] < n:
        black, p, heading = step(black, p, heading)
        replay += 1
        assert replay <= longest
    assert replay == longest
    assert longest <= closed_bound(n, Q(3)+Q(3,n))
    return dict(n=n, states=total, evaluated_transitions=total, maximum_exit=longest,
                witness=dict(black=sorted(initial), position=divmod(cell,n), heading=h),
                distance_sum=sum(distance))


def row_invariant(black, p, h):
    rows=set()
    for x,y in black:
        rows.symmetric_difference_update({y})
    if h % 2:
        rows.symmetric_difference_update({p[1]})
    return rows


def main():
    local = 0
    for r, p, h, black_here, c in product(
            (Q(3001,1000), Q(10,3), Q(4), Q(6), Q(17,2)),
            tuple(product(range(-4,5),repeat=2)), range(4), (False,True), (-5,0,7)):
        black = {(31,-29),(-37,32)} | ({p} if black_here else set())
        nxt, q, k = step(black,p,h)
        assert row_invariant(black,p,h)==row_invariant(nxt,q,k)
        u,v = r**(sum(p)-c),r**(c-sum(p))
        small,big = (r-3)/(r+1),(5*r+1)/(r+1)
        e,en = h < 2,k < 2
        expected = small*(u+v) if e==en else (small*u+big*v if e else big*u+small*v)
        assert phi(nxt,q,k,r,c)-phi(black,p,h,r,c)==expected
        assert expected >= 2*small > 0
        local += 1
    # Direct finite sums, not a comparison of two copies of the closed formula.
    for n,r in product(range(1,21),(Q(10,3),Q(4),Q(6))):
        assert bound(n,r)==closed_bound(n,r)
    for n in range(1,1001):
        assert closed_bound(n,Q(3)+Q(3,n)) <= 8*n*3**n+1
    # The lower bound must be strict only for r>3. At r=3 equal signs give zero.
    assert phi({(0,0)},(1,0),1,Q(3),0)-phi(set(),(0,0),0,Q(3),0)==0
    # Integer-vector stepping remains exact far beyond floating-point coordinates.
    a=10**30
    assert step(set(),(a,-a),0)==({(a,-a)},(a+1,-a),1)
    squares=[square_graph(n) for n in range(1,5)]
    report=dict(schema='clock-escape-independent-audit-v1', local_increment_cases=local,
                direct_field_sum_cases=60, exponential_bound_parameters=1000,
                exact_square_graphs=squares, endpoint_control='1x1 exits at update 1',
                nonstrict_base_control='r=3 rejected as a strict clock',
                full_ant_theorem_formalized=False,
                checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
