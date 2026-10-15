"""Finite, complete proof kernels for standard-highway factor rigidity.

Only Python's standard library is used. Finite-word admissibility is exact:
consecutive reads of the same physical cell must alternate R and L.
No eventual-periodicity hypothesis is made by the graph coverage argument.
"""
from __future__ import annotations
from collections import defaultdict
from typing import Iterable

W = 'RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR'
U = 'RRLRLLLLRRRRLRRLRRRRLLLLRLRR'  # 28-period infinite-background control
V = 'RRLRRRRLLLLRLRR'                # purely symbolic 15-period control
DIR = ((0, 1), (1, 0), (0, -1), (-1, 0))
Point = tuple[int, int]


def factors(word: str, length: int) -> set[str]:
    if not word or length < 1:
        raise ValueError('nonempty word and positive factor length required')
    repeated = word * (2 + length // len(word))
    return {repeated[i:i + length] for i in range(len(word))}


def geometry(word: str):
    p, h, reads, headings = (0, 0), 0, [], []
    for c in word:
        if c not in 'RL':
            raise ValueError('turn letters must be R or L')
        reads.append(p)
        headings.append(h)
        h = (h + (1 if c == 'R' else -1)) % 4
        p = (p[0] + DIR[h][0], p[1] + DIR[h][1])
    return reads, p, headings, h


def collision(word: str):
    """Return the first conflicting consecutive pair, or None."""
    p, h, last = (0, 0), 0, {}
    for i, c in enumerate(word):
        if p in last and last[p][1] == c:
            return (last[p][0], i, p, c)
        last[p] = (i, c)
        h = (h + (1 if c == 'R' else -1)) % 4
        p = (p[0] + DIR[h][0], p[1] + DIR[h][1])
    return None


def first_read_seed(word: str) -> set[Point]:
    """Construct a finite seed for a physically admissible finite word."""
    if collision(word) is not None:
        raise ValueError('word is not physically admissible')
    q = geometry(word)[0]
    seen, black = set(), set()
    for p, c in zip(q, word):
        if p not in seen and c == 'L':
            black.add(p)
        seen.add(p)
    return black


def enumerate_windows(k: int, length: int = 93):
    """Complete enumeration; no numerical simulation time or spatial cutoff."""
    if not 2 <= k <= length:
        raise ValueError('2 <= k <= length required')
    allowed = factors(W, k)
    extensions = defaultdict(list)
    for word in sorted(allowed):
        extensions[word[:-1]].append(word[-1])
    words = {w for w in allowed if collision(w) is None}
    levels = [[k, len(words)]]
    tested = rejected = 0
    for size in range(k + 1, length + 1):
        following = set()
        for word in sorted(words):
            for c in extensions[word[-(k - 1):]]:
                tested += 1
                candidate = word + c
                if collision(candidate) is None:
                    following.add(candidate)
                else:
                    rejected += 1
        words = following
        levels.append([size, len(words)])
    return sorted(words), {'levels': levels, 'extensions_tested': tested,
                           'collision_rejections': rejected}


def graph_of(words: Iterable[str]):
    adj = defaultdict(set)
    for word in words:
        adj[word[:-1]].add(word[1:])
        adj[word[1:]]
    return dict(adj)


def reachable(adj: dict[str, set[str]], start: str) -> set[str]:
    seen, pending = {start}, [start]
    while pending:
        for nxt in adj[pending.pop()]:
            if nxt not in seen:
                seen.add(nxt)
                pending.append(nxt)
    return seen


def components(adj: dict[str, set[str]]) -> list[set[str]]:
    """SCCs via mutual reachability, deliberately not the C++ algorithm."""
    reach = {v: reachable(adj, v) for v in adj}
    unused, result = set(adj), []
    while unused:
        v = min(unused)
        comp = {u for u in reach[v] if v in reach[u]}
        result.append(comp)
        unused -= comp
    return result


def verify_graph(words: list[str], k: int):
    """Finite kernel used in the all-infinite-path argument in PROOF.md."""
    adj = graph_of(words)
    comps = components(adj)
    cycles = [c for c in comps if len(c) > 1 or any(v in adj[v] for v in c)]
    standard = factors(W, 92)
    wanted = [standard] if k == 14 else [standard, factors(U, 92)]
    if {frozenset(c) for c in cycles} != {frozenset(c) for c in wanted}:
        raise AssertionError('unexpected recurrent component')
    for comp in cycles:
        for v in comp:
            if len(adj[v] & comp) != 1:
                raise AssertionError('recurrent component is not a simple cycle')
    ancestors = {v for v in adj if reachable(adj, v) & standard}
    if ancestors != standard:
        raise AssertionError('a nonstandard vertex can reach the standard cycle')
    for word in factors(W, 93):
        if word not in words:
            raise AssertionError('missing standard edge')
    if k == 13 and not factors(U, 93) <= set(words):
        raise AssertionError('wrong 28-cycle labels')
    return {'k': k, 'window_length': 93, 'vertices': len(adj),
            'edges': sum(map(len, adj.values())),
            'cyclic_component_lengths': sorted(map(len, cycles)),
            'all_cyclic_components_are_simple': True,
            'vertices_able_to_reach_standard': len(ancestors),
            'standard_cycle_has_no_external_ancestors': True}


def multiple(a: Point, d: Point):
    if d == (0, 0):
        raise ValueError('zero drift')
    j = 0 if d[0] else 1
    if a[j] % d[j]:
        return None
    n = a[j] // d[j]
    return n if a == (n * d[0], n * d[1]) else None


def periodic_recipe(word: str):
    """Exact periodic realization on points plus rays, possibly infinite.

    Full-drift translation classes are sorted by chronological order. This
    criterion and the finite-support specialization are prior methods, not
    claimed as new by this research package.
    """
    q, d, _, h = geometry(word)
    if h or d == (0, 0):
        raise ValueError('word must restore heading with nonzero drift')
    groups = []
    for i, p in enumerate(q):
        for b, entries in groups:
            a = multiple((p[0] - b[0], p[1] - b[1]), d)
            if a is not None:
                entries.append((a, i, word[i]))
                break
        else:
            groups.append((p, [(0, i, word[i])]))
    points, rays, records = set(), [], []
    for b, entries in groups:
        entries.sort(key=lambda a: (-a[0], a[1]))
        if any(entries[j][2] == entries[j - 1][2] for j in range(1, len(entries))):
            raise ValueError('nonalternating stabilized class')
        lo, hi = min(a[0] for a in entries), max(a[0] for a in entries)
        for n in range(lo, hi):
            first = next(c for a, _, c in entries if a <= n)
            if first == 'L':
                points.add((b[0] + n * d[0], b[1] + n * d[1]))
        if entries[0][2] == 'L':
            rays.append((b[0] + hi * d[0], b[1] + hi * d[1]))
        records.append({'anchor': list(b), 'entries': [list(a) for a in entries]})
    return {'word': word, 'drift': list(d), 'points': [list(p) for p in sorted(points)],
            'ray_starts': [list(p) for p in sorted(rays)], 'classes': records}


def verify_periodic_field(word: str, points: set[Point], rays: list[Point]):
    """Independent all-future epoch-breakpoint parity formula.

    Rays have the word's full drift. Field input is an XOR; recipes' pieces
    are disjoint, so it equals their set union. Tests the final infinite interval.
    """
    q, d, _, h = geometry(word)
    if h or d == (0, 0):
        return False
    for i, p in enumerate(q):
        cuts, earlier, hits, starts = {0}, [], [], []
        for j, a in enumerate(q):
            z = multiple((a[0] - p[0], a[1] - p[1]), d)
            if z is not None and (z > 0 or z == 0 and j < i):
                earlier.append(z)
                cuts.add(z)
        for a in points:
            z = multiple((a[0] - p[0], a[1] - p[1]), d)
            if z is not None and z >= 0:
                hits.append(z)
                cuts.update((z, z + 1))
        for a in rays:
            z = multiple((a[0] - p[0], a[1] - p[1]), d)
            if z is not None:
                starts.append(max(0, z))
                cuts.add(max(0, z))
        for n in cuts:
            bit = (sum(a == n for a in hits) + sum(a <= n for a in starts)
                   + sum(a <= n for a in earlier)) % 2
            if bit != (word[i] == 'L'):
                return False
    return True


def step_cells(black: set[Point], p: Point, h: int):
    c = 'L' if p in black else 'R'
    black.symmetric_difference_update({p})
    h = (h + (1 if c == 'R' else -1)) % 4
    return (p[0] + DIR[h][0], p[1] + DIR[h][1]), h, c


def rotate(p: Point, h: int) -> Point:
    x, y = p
    return ((x, y), (y, -x), (-x, -y), (-y, x))[h % 4]


def finite_lower_control():
    word = W[57:] + W[:57]
    recipe = periodic_recipe(word)
    if recipe['ray_starts']:
        raise AssertionError('standard seed unexpectedly infinite')
    K = set(map(tuple, recipe['points']))
    B, p, h = K | {(0, -1)}, (0, -1), 1
    target = set(B)
    new_p, new_h, c = step_cells(target, p, h)
    if (new_p, new_h, c, target) != ((0, 0), 0, 'L', K):
        raise AssertionError('finite one-step witness failed')
    prefix = 'L' + word * 2
    if prefix[:12] not in factors(W, 12) or prefix[:104] in factors(W, 104):
        raise AssertionError('finite sharpness failed')
    if prefix[:13] in factors(W, 13):
        raise AssertionError('13 does not detect the control')
    if not verify_periodic_field(word, K, []):
        raise AssertionError('one-step target is not permanently standard')
    return {'black': [list(p) for p in sorted(B)], 'head': [0, -1], 'heading': 1,
            'one_step_target_phase': 57, 'first_standard_time': 1,
            'first_12_factor': prefix[:12], 'first_13_factor': prefix[:13]}
