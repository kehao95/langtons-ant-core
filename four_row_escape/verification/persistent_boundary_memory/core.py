"""Persistent boundary memory: exact fields and finite response catalogs.

The all-parameter claims are proved in proof/results/persistent-boundary-memory.md.
This module changes neither the LR rule nor any historical project runtime.
"""
from __future__ import annotations
from functools import lru_cache

DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))
A, B, C, V = (6, 5), (10, 9), (6, 10, 12, 17), (18, 29)
P = 'RLLR'
K = 'RLRLRRRRLLLLRLLRLRLLRLLRLRRLLR'


def natural(*values: int) -> None:
    if any(type(x) is not int or x < 0 for x in values):
        raise ValueError('parameters must be nonnegative integers')


def right(j: int, k: int) -> tuple[int, ...]:
    natural(j, k)
    return A*j + C + V*k


def mirrored(columns) -> tuple[int, ...]:
    """Reflection in x=-1/2 AND color complement inside the five-row block."""
    return tuple(31-b for b in reversed(columns))


def source(left: int, right_count: int):
    natural(left, right_count)
    l = (5,) + right(0, left)
    return mirrored(l) + right(0, right_count), (len(l), 3, 1)


def prediction(left: int, right_count: int):
    """Exact first-exit time, pose, complete endpoint, and seam-crossing count."""
    natural(left, right_count)
    l, r = left, right_count
    if r <= l:
        t = 8*r*r + 60*r + 16
        columns = mirrored((5,) + right(r, l-r)) + B*(r+1) + (10, 18)
        return t, (2*(l+r)+9, 1, 1), columns, 2*r
    t = 8*l*l + 68*l + 48
    columns = mirrored((9,) + B*(l+1) + (10, 18)) + right(l+1, r-l-1)
    return t, (-1, 1, 3), columns, 2*l+1


def black_field(columns, height=5):
    return {(x, y) for x, b in enumerate(columns)
            for y in range(height) if b & (1 << y)}


def literal(field, width, height, pose, *, limit=None):
    """Independent set-based ordinary dynamics; exterior cells are retained.

    An explicit execution limit raises an exception; it never certifies escape.
    """
    black = set(field)
    x, y, h = pose
    dx, dy = DIRECTIONS[h]
    turns = []
    positions = []
    while 0 <= x < width and 0 <= y < height:
        if limit is not None and len(turns) >= limit:
            raise RuntimeError('INCONCLUSIVE: execution limit')
        positions.append((x, y))
        if (x, y) in black:
            turns.append('L')
            black.remove((x, y))
            dx, dy = -dy, dx
        else:
            turns.append('R')
            black.add((x, y))
            dx, dy = dy, -dx
        x, y = x+dx, y+dy
    h = DIRECTIONS.index((dx, dy))
    return black, (x, y, h), ''.join(turns), positions


class Catalog:
    """Candidate generator for height <=4, followed by independent local checks.

    A response is None (terminal) or (output-channel, persistent-residual-type).
    Side is left; rotation supplies the right-side case. Parity p fixes input
    rows 1-p modulo 2 and output rows p modulo 2.
    """
    def __init__(self, height):
        if height not in range(1, 5):
            raise ValueError('the finite catalog theorem covers heights 1..4')
        self.height = height
        self.ins = tuple(tuple(y for y in range(height) if (1-p-y) % 2 == 0)
                         for p in (0, 1))
        self.outs = tuple(tuple(y for y in range(height) if (p+y) % 2 == 0)
                          for p in (0, 1))
        self.types = {p: [(None,)*len(self.ins[p])] for p in (0, 1)}
        self.ids = {p: {self.types[p][0]: 0} for p in (0, 1)}
        self.rank = {p: [0] for p in (0, 1)}
        self.witness = {p: [()] for p in (0, 1)}
        self.active = set()
        self.compose = lru_cache(None)(self._compose)

    def column(self, mask, y, heading):
        x = steps = 0
        while x == 0 and 0 <= y < self.height:
            bit = (mask >> y) & 1
            mask ^= 1 << y
            heading = (heading + 1 - 2*bit) % 4
            dx, dy = DIRECTIONS[heading]
            x, y, steps = x+dx, y+dy, steps+1
        if steps > 2:
            raise AssertionError('one-column axis alternation')
        return mask, x, y, heading

    def _compose(self, p, mask, child):
        key = p, mask, child
        if key in self.active:
            raise RuntimeError('INCONCLUSIVE: cyclic candidate product')
        self.active.add(key)
        row = []
        for y0 in self.ins[p]:
            b, r, y, h = mask, child, y0, 1
            while True:
                b, x, y, h = self.column(b, y, h)
                if not 0 <= y < self.height:
                    row.append(None)
                    break
                out = self.outs[p].index(y)
                if x < 0:
                    row.append((out, self.compose(p, b, r)))
                    break
                answer = self.types[1-p][r][out]
                if answer is None:
                    row.append(None)
                    break
                out, residual = answer
                if self.rank[1-p][residual] >= self.rank[1-p][r]:
                    raise AssertionError('child rank')
                r, y, h = residual, self.outs[1-p][out], 3
        row = tuple(row)
        if row not in self.ids[p]:
            if len(self.types[p]) >= 1000:
                raise RuntimeError('INCONCLUSIVE: catalog size cap')
            self.ids[p][row] = len(self.types[p])
            self.types[p].append(row)
            self.rank[p].append(max([0]+[1+self.rank[p][a[1]] for a in row if a]))
            self.witness[p].append((mask,) + self.witness[1-p][child])
        self.active.remove(key)
        return self.ids[p][row]

    def close(self):
        previous = {0: {0}, 1: {0}}
        self.levels = [[1, 1]]
        for width in range(1, 13):
            current = {p: {self.compose(p, b, r)
                           for r in sorted(previous[1-p])
                           for b in range(1 << self.height)} for p in (0, 1)}
            self.levels.append([len(current[p]) for p in (0, 1)])
            if current == previous:
                self.closed_width = width
                break
            previous = current
        else:
            raise RuntimeError('INCONCLUSIVE: no finite closure by search cap')
        if any(current[p] != set(range(len(self.types[p]))) for p in (0, 1)):
            raise AssertionError('unrealized catalog node')
        self.products = {p: [[self.compose(p, b, r)
                             for r in range(len(self.types[1-p]))]
                            for b in range(1 << self.height)] for p in (0, 1)}
        self.verify_local()
        return self

    def verify_local(self):
        """Check all declared equations without calling the generator."""
        checks = 0
        for p in (0, 1):
            if len(set(self.types[p])) != len(self.types[p]):
                raise AssertionError('duplicate finite response tree')
            for i, row in enumerate(self.types[p]):
                for ans in row:
                    if ans is not None and self.rank[p][ans[1]] >= self.rank[p][i]:
                        raise AssertionError('parent rank')
            for b0 in range(1 << self.height):
                for r0 in range(len(self.types[1-p])):
                    t = self.products[p][b0][r0]
                    for channel, y0 in enumerate(self.ins[p]):
                        b, r, y, h = b0, r0, y0, 1
                        while True:
                            b, x, y, h = self.column(b, y, h)
                            if not 0 <= y < self.height:
                                got = None
                                break
                            out = self.outs[p].index(y)
                            if x < 0:
                                got = (out, self.products[p][b][r])
                                break
                            ans = self.types[1-p][r][out]
                            if ans is None:
                                got = None
                                break
                            out, residual = ans
                            if self.rank[1-p][residual] >= self.rank[1-p][r]:
                                raise AssertionError('local child rank')
                            r, y, h = residual, self.outs[1-p][out], 3
                        if got != self.types[p][t][channel]:
                            raise AssertionError('wrong product equation')
                        checks += 1
        return checks
