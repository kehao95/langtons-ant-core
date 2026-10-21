"""Exact persistent one-sided responses for the classical ant in four rows.

No P104 assumption, time cutoff, unbounded strip quotient, or erased history.
The finite type catalog is a generated certificate checked separately. A type
forgets terminal exit direction/time, but retains every future same-side reply.
"""
from __future__ import annotations
from collections import defaultdict
from functools import lru_cache
from typing import Optional

HEIGHT = 4
DIR = ((0, 1), (1, 0), (0, -1), (-1, 0))  # N,E,S,W
IN = tuple(tuple(y for y in range(4) if (1-p-y) % 2 == 0) for p in range(2))
OUT = tuple(tuple(y for y in range(4) if (p+y) % 2 == 0) for p in range(2))
Reply = Optional[tuple[int, int]]


def literal_column(mask: int, y: int, heading: int):
    """Exact first exit of one column, including its exit-producing update."""
    if not (0 <= mask < 16 and 0 <= y < 4 and 0 <= heading < 4):
        raise ValueError('invalid column state')
    x = updates = 0
    while x == 0 and 0 <= y < 4:
        black = (mask >> y) & 1
        mask ^= 1 << y
        heading = (heading + (3 if black else 1)) % 4
        dx, dy = DIR[heading]
        x += dx
        y += dy
        updates += 1
        if updates > 2:
            raise AssertionError('axis alternation failed')
    return mask, x, y, heading, updates


class Catalog:
    """Four catalogs: near side s=0/1 (left/right), local parity p=0/1.

    A node has two responses, each terminal or (output channel, residual node).
    Nodes are interned only after their children, and have no silent transitions.
    """
    def __init__(self):
        self.types = {(s,p): [(None,None)] for s in (0,1) for p in (0,1)}
        self.ids = {k: {(None,None): 0} for k in self.types}
        self.depth = {k: [0] for k in self.types}
        self.witness = {k: [()] for k in self.types}  # masks, near to far
        self.active = set()
        self.compose = lru_cache(None)(self._compose)
        self.from_pose = lru_cache(None)(self._from_pose)
        self.script = lru_cache(None)(self._script)

    def _compose(self, side, parity, mask, child):
        key = side, parity, mask, child
        if key in self.active:
            raise AssertionError('cyclic return product: no certificate')
        self.active.add(key)
        replies = []
        for channel in range(2):
            b, r, entry_side, entry = mask, child, side, channel
            while True:
                b, x, y, h, _ = literal_column(b, IN[parity][entry], 1 if entry_side == 0 else 3)
                if x == 0:
                    replies.append(None)
                    break
                leaving = int(x > 0)
                out = OUT[parity].index(y)
                if leaving == side:
                    residual = self.compose(side, parity, b, r)
                    replies.append((out, residual))
                    break
                ans = self.types[side, 1-parity][r][out]
                if ans is None:
                    replies.append(None)
                    break
                entry, new_r = ans
                if self.depth[side,1-parity][new_r] >= self.depth[side,1-parity][r]:
                    raise AssertionError('child response did not decrease rank')
                r, entry_side = new_r, 1-side
        row = tuple(replies)
        self.active.remove(key)
        tag = side, parity
        if row not in self.ids[tag]:
            i = len(self.types[tag])
            self.ids[tag][row] = i
            self.types[tag].append(row)
            self.depth[tag].append(max([0] + [1+self.depth[tag][a[1]] for a in row if a is not None]))
            self.witness[tag].append((mask,) + self.witness[side,1-parity][child])
        return self.ids[tag][row]

    def close(self):
        prev = {k: {0} for k in self.types}
        self.width_counts = []
        for width in range(1, 10):
            nxt = {k: {self.compose(*k, b, r)
                       for r in sorted(prev[k[0],1-k[1]]) for b in range(16)}
                   for k in self.types}
            self.width_counts.append([len(nxt[k]) for k in sorted(nxt)])
            if nxt == prev:
                self.closed_width = width
                break
            prev = nxt
        else:
            raise AssertionError('declared finite catalog did not close')
        # Checking these local clauses, NOT the discovery cap, proves all widths.
        for s,p in self.types:
            if set(range(len(self.types[s,p]))) != nxt[s,p]:
                raise AssertionError('catalog coverage/reachability disagreement')
            for r in range(len(self.types[s,1-p])):
                for b in range(16):
                    assert self.compose(s,p,b,r) in nxt[s,p]
        assert self.width_counts == [[n]*4 for n in (12,36,83,158,240,264,269,269)]
        assert all(max(d) == 13 for d in self.depth.values())
        return self

    def _from_pose(self, p, b, r, y, h):
        """Near side LEFT: run a new column with a persistent right child.

        Output is (near channel or None, final mask, child type, local updates,
        child request script). Terminal child calls are included in the script.
        """
        cost, calls = 0, []
        while True:
            b, x, y, h, count = literal_column(b, y, h)
            cost += count
            if x == 0:
                return None, b, r, cost, tuple(calls)
            if x < 0:
                return OUT[p].index(y), b, r, cost, tuple(calls)
            j = IN[1-p].index(y)
            calls.append(j)
            ans = self.types[0,1-p][r][j]
            if ans is None:
                return None, b, r, cost, tuple(calls)
            j, r = ans
            y, h = OUT[1-p][j], 3

    def _script(self, p, b, r, sequence):
        """Process a finite sequence of requests; preserve both residual states."""
        cost, requests = 0, []
        for index, channel in enumerate(sequence):
            out, b, r, c, sub = self.from_pose(p,b,r,IN[p][channel],1)
            cost += c
            requests.extend(sub)
            if out is None and index != len(sequence)-1:
                raise AssertionError('request after terminal')
        return cost, tuple(requests)

    def root_tag(self, p, out, b, r):
        return 0 if out is None else 1 + 2*self.compose(0,p,b,r) + out

    def rooted_representatives(self):
        """Every way to prepend one column, root new or still in the child.

        Root tag 0 means terminal. Tag 1+2*t+j means first root-run returns on
        channel j and leaves ordinary residual type t. Every root location is
        accounted for by exactly these two placements (not by a boundary lemma).
        """
        ordinary, rooted = defaultdict(list), defaultdict(list)
        for p in (0,1):
            for b in range(16):
                for r in range(len(self.types[0,1-p])):
                    ordinary[p,self.compose(0,p,b,r)].append((b,r))
                    for y in range(4):
                        for h in range(4):
                            if (h-p-y) % 2:
                                continue
                            out,bb,rr,c,sub = self.from_pose(p,b,r,y,h)
                            o = self.root_tag(p,out,bb,rr)
                            rooted[p,o].append(('F',b,r,y,h,bb,rr,c,sub))
                for child_root in range(1+2*len(self.types[0,1-p])):
                    if child_root == 0:
                        out,bb,rr,c,sub = None,b,0,0,()
                    else:
                        r,j = divmod(child_root-1,2)
                        out,bb,rr,c,sub = self.from_pose(p,b,r,IN[p][j],3)
                    o = self.root_tag(p,out,bb,rr)
                    rooted[p,o].append(('R',b,child_root,-1,-1,bb,rr,c,sub))
        return ordinary, rooted


def weighted_graph(catalog):
    """Exact weighted recurrence for ALL four-row colors, poses, and widths.

    F state: ordinary type and a supplied request script.
    R state: root response tag, followed by a supplied request script.
    An edge adds a left column, with its number of real column updates as weight.
    """
    ordinary, rooted = catalog.rooted_representatives()
    states, index, edges = [], {}, []
    def intern(state):
        if state not in index:
            index[state] = len(states)
            states.append(state)
            edges.append([])
        return index[state]
    goals = [intern(('R',p,o,())) for p,o in sorted(rooted)]
    i = 0
    while i < len(states):
        kind,p,t,seq = states[i]
        if kind == 'F':
            for b,r in ordinary[p,t]:
                cost, sub = catalog.script(p,b,r,seq)
                target = intern(('F',1-p,r,sub))
                edges[i].append((target,cost,b,-1,-1))
        else:
            for tag,b,r,y,h,bb,rr,c,sub in rooted.get((p,t),()):
                if t == 0 and seq:
                    raise AssertionError('terminal root cannot receive another request')
                cc, tail = catalog.script(p,bb,rr,seq)
                target = intern((tag,1-p,r,sub+tail))
                edges[i].append((target,c+cc,b,y,h))
        i += 1
        if len(states) > 25000:
            raise AssertionError('certificate size cap exceeded; no conclusion')
    assert (len(states),sum(map(len,edges)),len(goals)) == (21248,527764,1078)
    return states, edges, goals


def direct_run(columns, x, y, h, *, cap=None):
    """Independent literal geometry on a COMPLETE finite rectangle coloring.

    This simulator makes no macro calls. It returns the full retained columns.
    cap, when supplied, only raises an error; it never certifies escape.
    """
    b = list(columns)
    n, t = len(b), 0
    visits = [0]*n
    while 0 <= x < n and 0 <= y < 4:
        if cap is not None and t >= cap:
            raise RuntimeError('literal run cap reached: UNKNOWN')
        colour = b[x] >> y & 1
        b[x] ^= 1 << y
        h = (h + (3 if colour else 1)) % 4
        visits[x] += 1
        dx,dy = DIR[h]
        x,y,t = x+dx,y+dy,t+1
    return t,(x,y,h),b,visits
