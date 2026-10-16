"""Exact one-parameter vertical-band certificate verifier.

A read occurrence occupies one affine integer interval in a class (x, y mod 4).
The finite arrangement of all interval endpoints covers every n >= 1 and every
lattice cell. It is not a bounded-n simulation. See proof/results/silent-archive-amplification.md for the coverage
argument. No solver, floating point, network access, or shared ant runtime.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from collections import defaultdict
import hashlib
import json

Aff = tuple[int, int]             # a*n+b
Tri = tuple[int, int, int]        # a*n+b*r+c
DIR = ((0, 1), (1, 0), (0, -1), (-1, 0))


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def value(f: Aff, n: int) -> int:
    return f[0] * n + f[1]


def add(f: Aff, g: Aff) -> Aff:
    return f[0] + g[0], f[1] + g[1]


def nonnegative(f: Aff, lo: int, hi: int | None) -> bool:
    if value(f, lo) < 0:
        return False
    return f[0] >= 0 if hi is None else value(f, hi) >= 0


@dataclass(frozen=True)
class Token:
    x: int
    residue: int
    lo: Aff
    stop: Aff
    kind: str
    block: int = -1
    order: int = 0
    turn: str = ''
    time: Tri = (0, 0, 0)

    def active(self, n: int, r: int) -> bool:
        return value(self.lo, n) <= r < value(self.stop, n)


def profile_tokens(profile: dict, kind: str) -> list[Token]:
    out = []
    for part in ('low', 'bulk', 'high'):
        pts = profile[part]
        require(len({tuple(p) for p in pts}) == len(pts), 'duplicate profile point')
        for x, y in pts:
            require(type(x) is int and type(y) is int, 'noninteger point')
            if part == 'low':
                require(y < 8, 'low profile outside its band')
            elif part == 'bulk':
                require(8 <= y < 12, 'bulk profile outside one period')
            else:
                require(y >= 8, 'high profile below its band')
            residue = y % 4
            r = (y - residue) // 4
            if part == 'low':
                lo, stop = (0, r), (0, r + 1)
            elif part == 'bulk':
                lo, stop = (0, r), (1, r)
            else:
                lo, stop = (1, r), (1, r + 1)
            out.append(Token(x, residue, lo, stop, kind))
    return out


def word_trace(word: str, h: int = 0):
    require(word and set(word) <= {'L', 'R'}, 'invalid word')
    x = y = 0
    visits = []
    for i, turn in enumerate(word):
        visits.append((x, y, turn, i))
        h = (h + (1 if turn == 'R' else -1)) % 4
        dx, dy = DIR[h]
        x, y = x + dx, y + dy
    return visits, (x, y), h


def read_tokens(cert: dict):
    x, y0, heading = cert['pose']
    y, elapsed = (0, y0), (0, 0)
    out, boundaries = [], []
    for block, spec in enumerate(cert['blocks']):
        word, count = spec['word'], tuple(spec['count'])
        require(len(count) == 2 and nonnegative(count, 1, None), 'invalid repeat count')
        visits, (dx, dy), end_h = word_trace(word, heading)
        single = count == (0, 1)
        require(single or (end_h == heading and dx == 0 and abs(dy) == 4),
                'unsupported repeating block (must restore heading and drift vertically by four)')
        require(y[0] % 4 == 0, 'nonintegral affine residue')
        for qx, qy, turn, i in visits:
            yy, a = y[1] + qy, y[0] // 4
            residue = yy % 4
            b = (yy - residue) // 4
            if single:
                lo, stop = (a, b), (a, b + 1)
                tm, order = (elapsed[0], 0, elapsed[1] + i), i
            else:
                s = dy // 4
                if s == 1:
                    lo, stop = (a, b), (a + count[0], b + count[1])
                else:
                    lo, stop = (a - count[0], b - count[1] + 1), (a, b + 1)
                order = i - len(word) * s * b
                tm = (elapsed[0] - len(word) * s * a,
                      len(word) * s, elapsed[1] + order)
            out.append(Token(x + qx, residue, lo, stop, 'read', block, order, turn, tm))
        require(single or dx == 0, 'parameter-dependent horizontal position')
        x += dx * count[1]
        y = add(y, (dy * count[0], dy * count[1]))
        elapsed = add(elapsed, (len(word) * count[0], len(word) * count[1]))
        heading = end_h
        boundaries.append({'x': x, 'y': y, 'h': heading, 'time': elapsed})
    return out, boundaries


def n_slabs(groups: dict) -> list[tuple[int, int | None]]:
    """Split every possible crossing of affine endpoint functions, exactly."""
    starts = {1}
    for toks in groups.values():
        endpoints = {f for t in toks for f in (t.lo, t.stop)}
        lines = list(endpoints)
        for i, f in enumerate(lines):
            for g in lines[:i]:
                if f[0] == g[0]:
                    continue
                cross = Fraction(g[1] - f[1], f[0] - g[0])
                if cross >= 1:
                    k = cross.numerator // cross.denominator
                    starts.update((k, k + 1))
    s = sorted(starts)
    return [(lo, s[i + 1] - 1 if i + 1 < len(s) else None) for i, lo in enumerate(s)]


def identically_zero(f: Tri, left: Aff, right: Aff,
                     nlo: int, nhi: int | None) -> bool:
    """Prove f(n,r)=0 on left(n)<=r<right(n), n in the whole slab."""
    for bound in (left, (right[0], right[1] - 1)):
        g = (f[0] + f[1] * bound[0], f[2] + f[1] * bound[1])
        if not (nonnegative(g, nlo, nhi) and nonnegative((-g[0], -g[1]), nlo, nhi)):
            return False
    return True


def verify(cert: dict) -> dict:
    require(cert['schema'] == 'langtons-ant-silent-archive-v1', 'wrong schema')
    require(cert['parameter_min'] == 1, 'wrong parameter domain')
    require(cert['pose'] == [-1, 0, 3], 'wrong initial pose')
    words = cert['words']
    require([len(words[k]) for k in ('W', 'A', 'B', 'P')] == [104, 28, 102, 20],
            'wrong word lengths')
    expected = [(words['B'][9:], [0, 1]), (words['A'], [1, 0]),
                (words['B'], [0, 1]), (words['A'], [1, -1]),
                (words['P'], [1, 1]), ('RLL', [0, 1])]
    require([(b['word'], b['count']) for b in cert['blocks']] == expected, 'wrong program')
    require(cert['true_past9'] == words['B'][:9], 'wrong past convention')
    source = profile_tokens(cert['source'], 'source')
    ret = profile_tokens(cert['return'], 'return')
    pulse = profile_tokens(cert['pulse_end'], 'pulse_end')
    final = profile_tokens(cert['final'], 'final')
    reads, boundaries = read_tokens(cert)
    require(boundaries[3] == {'x': 0, 'y': (0, 4), 'h': 0, 'time': (56, 167)}, 'return pose/time')
    require(boundaries[4] == {'x': 0, 'y': (4, 8), 'h': 0, 'time': (76, 187)}, 'pulse pose/time')
    require(boundaries[5] == {'x': 0, 'y': (4, 9), 'h': 3, 'time': (76, 190)}, 'final pose/time')
    # Select both genuine, pre-defect-created rail lifetimes, 0 <= j <= n.
    selectors = [Token(1, 0, (0, 1), (1, 2), 'left_lifetime'),
                 Token(0, 3, (0, 1), (1, 2), 'right_lifetime')]
    groups = defaultdict(list)
    for t in source + ret + pulse + final + reads + selectors:
        groups[t.x, t.residue].append(t)
    slabs = n_slabs(groups)
    bands = checks = lifetime_bands = 0
    digest = hashlib.sha256()
    for nlo, nhi in slabs:
        for cls, toks in sorted(groups.items()):
            functions = {f for t in toks for f in (t.lo, t.stop)}
            ordered = sorted(functions, key=lambda f: (value(f, nlo), f))
            # Validate the claimed ordering on the entire (possibly infinite) slab.
            for f, g in zip(ordered, ordered[1:]):
                require(nonnegative((g[0] - f[0], g[1] - f[1]), nlo, nhi),
                        'endpoint order not valid on full slab')
                if value(f, nlo) == value(g, nlo) and f != g:
                    require(nhi == nlo, 'unisolated endpoint equality')
            unique = []
            for f in ordered:
                if not unique or value(unique[-1], nlo) != value(f, nlo):
                    unique.append(f)
            for left, right in zip(unique, unique[1:]):
                require(nonnegative((right[0] - left[0], right[1] - left[1] - 1), nlo, nhi),
                        'empty or changing spatial band')
                r = value(left, nlo)
                active = [t for t in toks if t.active(nlo, r)]
                if not active:
                    continue
                sources = [t for t in active if t.kind == 'source']
                require(len(sources) <= 1, 'source profile pieces overlap')
                bit = len(sources) % 2
                seq = sorted((t for t in active if t.kind == 'read'), key=lambda t: (t.block, t.order))
                prefix = [t for t in seq if t.block < 4]
                require(not bit or prefix, 'an initial black lifetime survives unread to return')
                original_bit = bit
                for cutoff, target in ((4, 'return'), (5, 'pulse_end'), (6, 'final')):
                    state = original_bit
                    for t in seq:
                        if t.block >= cutoff:
                            break
                        require(state == (t.turn == 'L'),
                                f'read conflict at n={nlo}, class={cls}, r={r}, block={t.block}')
                        state ^= 1
                        checks += 1
                    target_tokens = [t for t in active if t.kind == target]
                    require(len(target_tokens) <= 1, 'target profile pieces overlap')
                    require(state == len(target_tokens), f'complete {target} field mismatch')
                selected = [t.kind for t in active if t.kind.endswith('_lifetime')]
                for which in selected:
                    require(prefix and prefix[-1].turn == 'R', 'fuel not a new legal-prefix birth')
                    consumed = [t for t in seq if t.block == 4]
                    require(consumed and consumed[0].turn == 'L', 'fuel not first read black in pulse')
                    side = 'left' if which == 'left_lifetime' else 'right'
                    def in_r(label):
                        a, b, c = cert['claims'][side + '_' + label + '_n_j_const']
                        return a, b, c - b  # j=r-1
                    birth, death = in_r('birth'), in_r('death')
                    for actual, wanted in ((prefix[-1].time, birth), (consumed[0].time, death)):
                        diff = tuple(a - b for a, b in zip(actual, wanted))
                        require(identically_zero(diff, left, right, nlo, nhi), 'wrong lifetime identity')
                    lifetime_bands += 1
                bands += 1
                row = [nlo, nhi, cls, left, right, original_bit,
                       [(t.block, t.order, t.turn, t.time) for t in seq]]
                digest.update((json.dumps(row, separators=(',', ':')) + '\n').encode())
    # Source and endpoint masses; their disjointness was checked above for all n.
    for name, claim in (('source', [10, 41]), ('return', [18, 58]),
                        ('pulse_end', [22, 62]), ('final', [22, 61])):
        profile = cert[name]
        mass = [len(profile['bulk']), len(profile['low']) + len(profile['high'])]
        require(mass == claim == cert['claims'][name + '_mass'], 'wrong mass')
    # Exact maximum y in the event-free excursion. Every read is covered.
    prefix_reads = [t for t in reads if t.block < 4]
    for t in prefix_reads:
        top = (4 * t.stop[0], 4 * (t.stop[1] - 1) + t.residue)
        require(nonnegative((4 - top[0], 13 - top[1]), 1, None), 'height upper bound failed')
    require(any(t.lo == (1, 3) and t.stop == (1, 4) and t.residue == 1
                and t.block == 2 for t in prefix_reads), 'height bound not attained')
    return {'n_slabs': [list(s) for s in slabs], 'affine_spatial_bands': bands,
            'read_colour_checks': checks, 'lifetime_identity_bands': lifetime_bands,
            'read_phase_tokens': len(reads), 'cell_classes': len(groups),
            'arrangement_sha256': digest.hexdigest(), 'complete_fields_checked': 3}
