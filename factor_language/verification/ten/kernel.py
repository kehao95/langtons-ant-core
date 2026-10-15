"""Exact, finite proof kernels for the ten-factor attraction theorem.

The analytic coverage, all-parameter fold obstruction, and geometric spiral
separation are in PROOF.md. These routines do not purport to decide HC.
"""
from __future__ import annotations
from collections import defaultdict, deque
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent / 'baseline'))
import rigidity as r


def load_witness(cert: Path) -> dict:
    return json.loads((cert / 'witness.json').read_text())



def enumerate_words(k=10, length=150):
    """Complete breadth-first enumeration with cloned last-read maps.

    A different implementation from the C++ live-colour backtracking DFS.
    Every queued node carries the exact geometric pose and last letter at each
    visited cell. No generator output is accepted without re-enumeration.
    """
    if not 2 <= k <= length: raise ValueError('2 <= k <= length required')
    allowed=r.factors(r.W,k);extensions=defaultdict(list)
    for word in sorted(allowed):extensions[word[:-1]].append(word[-1])
    states=[]
    for word in sorted(allowed):
        if r.collision(word) is None:
            q,p,_,h=r.geometry(word)
            states.append((word,p,h,dict(zip(q,word))))
    levels=[[k,len(states)]];tested=rejected=0
    for size in range(k+1,length+1):
        following=[]
        for word,p,h,last in states:
            for c in extensions[word[-(k-1):]]:
                tested+=1
                if last.get(p)==c:
                    rejected+=1;continue
                newlast=last.copy();newlast[p]=c
                g=(h+(1 if c=='R' else -1))%4
                q=(p[0]+r.DIR[g][0],p[1]+r.DIR[g][1])
                following.append((word+c,q,g,newlast))
        states=following;levels.append([size,len(states)])
    return sorted(word for word,p,h,last in states), {'levels':levels,'extensions_tested':tested,'collision_rejections':rejected}

def graph(words):
    adj = defaultdict(set)
    rev = defaultdict(set)
    for w in words:
        a, b = w[:-1], w[1:]
        adj[a].add(b); adj[b]
        rev[b].add(a); rev[a]
    return dict(adj), dict(rev)


def reach(adj, starts):
    seen = set(starts); pending = list(seen)
    while pending:
        for u in adj[pending.pop()]:
            if u not in seen:
                seen.add(u); pending.append(u)
    return seen


def sccs(adj, rev):
    # Iterative Kosaraju, without language-runtime recursion limits.
    done, order = set(), []
    for root in sorted(adj):
        if root in done: continue
        done.add(root); stack = [(root, iter(sorted(adj[root])))]
        while stack:
            v, it = stack[-1]
            u = next(it, None)
            if u is None:
                order.append(v); stack.pop()
            elif u not in done:
                done.add(u); stack.append((u, iter(sorted(adj[u]))))
    done, result = set(), []
    for v in reversed(order):
        if v in done: continue
        comp, pending = {v}, [v]; done.add(v)
        while pending:
            for u in rev[pending.pop()]:
                if u not in done:
                    done.add(u); comp.add(u); pending.append(u)
        result.append(comp)
    return result


def topological(adj, subset):
    subset = set(subset)
    indeg = {v: 0 for v in subset}
    for v in subset:
        for u in adj[v] & subset: indeg[u] += 1
    queue = deque(sorted(v for v in subset if not indeg[v])); out = []
    while queue:
        v = queue.popleft(); out.append(v)
        for u in sorted(adj[v] & subset):
            indeg[u] -= 1
            if indeg[u] == 0: queue.append(u)
    if len(out) != len(subset): raise AssertionError('claimed acyclic subgraph has a cycle')
    return out


def verify_graph(words, cert: Path, wit):
    adj, rev = graph(words)
    comps = sccs(adj, rev)
    cyc = [c for c in comps if len(c) > 1 or any(v in adj[v] for v in c)]
    W, T = r.factors(wit['W'], 149), r.factors(wit['T'], 149)
    assert W in cyc and T in cyc and len(cyc) == 3
    H = next(c for c in cyc if c not in (W, T))
    assert (len(adj), sum(map(len, adj.values())), len(H)) == (6501, 6605, 366)
    for c, w in [(W, wit['W']), (T, wit['T'])]:
        assert all(len(adj[v] & c) == 1 for v in c)
        assert {v + u[-1] for v in c for u in adj[v] & c} == r.factors(w, 150)
    # Explicit homomorphism of every internal non-flat SCC edge.
    lines = (cert / 'quotient.tsv').read_text().splitlines()
    mapping = {}
    for line in lines:
        word, state = line.split('\t')
        assert word not in mapping
        mapping[word] = int(state)
    assert set(mapping) == H and set(mapping.values()) == set(range(102))
    A, B = wit['A'], wit['B']
    assert len(A) == 28 and len(B) == 102 and A[1:] == B[-27:]
    assert A[0] == 'L' and B[0] == 'R'
    model = {(i, B[i]): (i + 1) % 102 for i in range(102)}
    model[0, 'L'] = 75
    count = 0
    for v in H:
        for u in adj[v] & H:
            assert model.get((mapping[v], u[-1])) == mapping[u]
            count += 1
    assert count == 370
    # Appended-edge labels are shifted 149 positions from the original word.
    # This shift does not affect eventual mode classification.
    ancestors = reach(rev, W)
    assert len(ancestors) == 925 and not ancestors & H and T <= ancestors
    assert reach(adj, H) & W == set()
    # Future-window vertices carry the CURRENT turn as v[0], not the appended
    # label u[-1]. The distinction matters in the mass-weighted bound below.
    pre = reach(rev, T) - T
    assert pre <= ancestors and len(pre) == 54
    pre_order = topological(adj, pre)
    costs = {v: 0 for v in pre}; lengths = dict(costs); best = longest_pre = 0
    for v in pre_order:
        a = costs[v] + 1 + (12 if v[0] == 'R' else -12)
        for u in adj[v]:
            if u in T:
                best = max(best, a); longest_pre = max(longest_pre, lengths[v] + 1)
            elif u in pre:
                costs[u] = max(costs[u], a); lengths[u] = max(lengths[u], lengths[v] + 1)
    post = (reach(adj, T) & ancestors) - W - T
    post_order = topological(adj, post); lengths = {}
    for v in reversed(post_order):
        lengths[v] = 1 + max([lengths[u] for u in adj[v] & post] + [0])
    post_max = max([lengths.get(u, 0) for v in T for u in adj[v] if u not in T and u in ancestors] + [0])
    # No-T paths to W are separately acyclic.
    noncyclic = ancestors - W - T
    order = topological(adj, noncyclic); rank = {}
    for v in reversed(order):
        rank[v] = 1 + max([rank[u] for u in adj[v] & noncyclic] + [0])
    no_T_max = max(rank.values(), default=0)
    assert (best, longest_pre, post_max) == (70, 46, 137)
    assert no_T_max == 167
    return {'vertices': len(adj), 'edges': len(words), 'cyclic_components': [24, 104, 366],
            'nonflat_internal_edges_verified': count, 'quotient_vertices': 102,
            'standard_ancestors': len(ancestors), 'pre_weight_max': best,
            'pre_length_max': longest_pre, 'post_length_max': post_max,
            'no_T_length_max': no_T_max, 'bound_intercept': best + post_max + 5}


def first_L_times(word):
    """First-L read times in word^omega: finite exceptions plus time rays.

    Each ray is start + N*len(word). This follows directly from chronological
    full-drift classes, not extrapolation of a finite simulated prefix.
    """
    rec = r.periodic_recipe(word); P = len(word)
    finite, rays = [], []
    for cl in rec['classes']:
        entries = cl['entries']; lo = min(a for a, _, _ in entries); hi = max(a for a, _, _ in entries)
        for n in range(lo, hi):
            a, i, c = next(e for e in entries if e[0] <= n)
            if c == 'L': finite.append((n - a) * P + i)
        a, i, c = entries[0]
        if c == 'L': rays.append((hi - a) * P + i)
    return sorted(finite), sorted(rays)


def supply_check(T):
    rows, maximum = [], -10**9
    for phase in range(24):
        word = T[phase:] + T[:phase]
        finite, rays = first_L_times(word)
        assert len(rays) == 2
        # After D, all exceptional times have passed and both rays have begun.
        # Thus b(L+24)=b(L)+2 for EVERY L>=D.
        D = max([0] + [x + 1 for x in finite] + rays)
        def b(L):
            return sum(x < L for x in finite) + sum(0 if L <= x else (L - 1 - x)//24 + 1 for x in rays)
        values = [L - 12*b(L) for L in range(D + 24)]
        mx = max(values); maximum = max(maximum, mx)
        # Literal controls of the independently derived time representation.
        for L in range(D + 49):
            assert b(L) == len(r.first_read_seed((word * (4 + L//24))[:L]))
        rows.append({'phase': phase, 'finite_times': finite, 'ray_starts': rays,
                     'periodicity_from': D, 'max_L_minus_12b': mx})
    assert maximum == 5
    return {'all_phase_bound': maximum, 'phases': rows}


def parametric_visits(A, B, n, m, point):
    """All visits to point in B A^n B A^m B, without expanding powers."""
    origin, heading, start, result = (0, 0), 0, 0, []
    for word, repeat in [(B, 1), (A, n), (B, 1), (A, m), (B, 1)]:
        positions, d, _, dh = r.geometry(word)
        rd = r.rotate(d, heading)
        for i, q in enumerate(positions):
            q = r.rotate(q, heading); q = (q[0] + origin[0], q[1] + origin[1])
            diff = point[0]-q[0], point[1]-q[1]
            if repeat == 1:
                j = 0 if diff == (0,0) else None
            elif repeat > 0:
                assert dh == 0
                j = r.multiple(diff, rd)
            else: j = None
            if j is not None and 0 <= j < repeat:
                result.append((start + j*len(word) + i, word[i]))
        origin = origin[0]+repeat*rd[0], origin[1]+repeat*rd[1]
        heading = (heading + repeat*dh) % 4; start += repeat*len(word)
    return sorted(result)


def obstruction_witness(n, m):
    if n == 0: return (0, 2), 32, 184
    if m >= n: return (0, 2), 32, 184 + 56*n
    return (1, 4*(n-m)), 25 + 28*(n-m), 205 + 28*(n+m)


def family(n, wit):
    if n < 0: raise ValueError('nonnegative n required')
    f = wit['sharp_family']
    E = set(map(tuple, f['E'])); D = set(map(tuple, f['cap']))
    return E | {(-2, -2*j) for j in range(1, n+1)} | {(0,-2*j-1) for j in range(1,n+1)} | {(x,y-2*n) for x,y in D}
