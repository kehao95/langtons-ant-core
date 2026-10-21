"""Reconstruct only the finite graph obligations used by silent-supply.

The all-parameter no-three-fold lemma is an imported analytic dependency. A
finite graph computation does not substitute for that lemma's quantifiers.
"""
from __future__ import annotations
from collections import defaultdict, deque
import hashlib
from model import A, B, T, W, DIR, L10, WORD_HASH, geometry


def enumerate_words():
    states = [('', (0, 0), 0, {})]
    counts = [1]
    for depth in range(1, 151):
        result = []
        for w, p, h, previous in states:
            for ch in 'RL':
                if (depth >= 10 and w[-9:]+ch not in L10) or previous.get(p) == ch:
                    continue
                hh = (h+(1 if ch == 'R' else -1)) % 4
                dx, dy = DIR[hh]
                seen = previous.copy()
                seen[p] = ch
                result.append((w+ch, (p[0]+dx, p[1]+dy), hh, seen))
        states = result
        counts.append(len(states))
    words = sorted(w for w, _, _, _ in states)
    digest = hashlib.sha256(('\n'.join(words)+'\n').encode()).hexdigest()
    if len(words) != 6605 or digest != WORD_HASH:
        raise AssertionError('inherited finite-word certificate mismatch')
    return words, counts


def sccs(adj):
    rev = {v: set() for v in adj}
    for v, outs in adj.items():
        for u in outs:
            rev[u].add(v)
    seen, order = set(), []
    for v in sorted(adj):
        if v in seen:
            continue
        seen.add(v)
        todo = [(v, iter(sorted(adj[v])))]
        while todo:
            u, successors = todo[-1]
            x = next(successors, None)
            if x is None:
                order.append(u)
                todo.pop()
            elif x not in seen:
                seen.add(x)
                todo.append((x, iter(sorted(adj[x]))))
    seen, result = set(), []
    for v in reversed(order):
        if v in seen:
            continue
        seen.add(v)
        component, todo = {v}, [v]
        while todo:
            for u in rev[todo.pop()]:
                if u not in seen:
                    seen.add(u)
                    component.add(u)
                    todo.append(u)
        result.append(component)
    return result


def condensation(adj):
    components = sccs(adj)
    ids = {v: i for i, c in enumerate(components) for v in c}
    dag = {i: set() for i in range(len(components))}
    degree = {i: 0 for i in dag}
    for v, outs in adj.items():
        for u in outs:
            if ids[v] != ids[u]:
                dag[ids[v]].add(ids[u])
    for outs in dag.values():
        for u in outs:
            degree[u] += 1
    todo = deque(sorted(i for i in dag if degree[i] == 0))
    top = []
    while todo:
        i = todo.popleft()
        top.append(i)
        for j in sorted(dag[i]):
            degree[j] -= 1
            if not degree[j]:
                todo.append(j)
    assert len(top) == len(dag)
    cyclic = {i for i, c in enumerate(components)
              if len(c) > 1 or any(v in adj[v] for v in c)}
    return components, ids, dag, top, cyclic


def build(words):
    adj = defaultdict(set)
    for w in words:
        adj[w[:-1]].add(w[1:])
        adj[w[1:]]
    components, ids, dag, top, cyclic = condensation(adj)
    assert sorted(len(components[i]) for i in cyclic) == [24, 104, 366]
    downstream = {i: set() for i in dag}
    for i in reversed(top):
        for j in dag[i]:
            downstream[i] |= downstream[j] | ({j} if j in cyclic else set())
    order_table = sorted((len(components[i]), sorted(len(components[j]) for j in downstream[i]))
                         for i in cyclic)
    assert order_table == [(24, [104, 366]), (104, [366]), (366, [])]
    folded = next(components[i] for i in cyclic if len(components[i]) == 366)
    phase = {}
    for word in sorted(folded):
        states = set(range(102))
        for letter in word:
            states = {(q+1) % 102 for q in states if B[q] == letter} | (
                {75} if 0 in states and letter == 'L' else set())
        assert len(states) == 1
        phase[word] = states.pop()
    quotient_hash = hashlib.sha256(''.join(w+'\t'+str(phase[w])+'\n'
                                           for w in sorted(phase)).encode()).hexdigest()
    assert quotient_hash == 'f6d5502737c0ce931c1f9ca62a62ad8307157b4133c8f087f7ac0268b0d05682'
    model = {(i, B[i]): (i+1) % 102 for i in range(102)}
    model[0, 'L'] = 75
    for v in folded:
        for u in adj[v] & folded:
            assert model[phase[v], u[-1]] == phase[u]
    lift = {}
    for v in sorted(adj):
        for count in (range(4) if v in folded else [0]):
            if count == 3 and phase[v] == 0:
                continue
            lift[v, count] = set()
            for u in adj[v]:
                n = count+int(phase[v] == 0 and u[-1] == 'R') if v in folded and u in folded else 0
                if u in folded and (n > 3 or (n == 3 and phase[u] == 0)):
                    continue
                lift[v, count].add((u, n))
    assert len(lift) == 7595 and sum(map(len, lift.values())) == 7763
    comps, lid, ldag, ltop, lc = condensation(lift)
    assert sorted(len(comps[i]) for i in lc) == [24, 28, 28, 28, 104]
    names, cycle_words = {}, {}
    for i in lc:
        c = comps[i]
        v = start = min(c)
        word = ''
        while True:
            outs = lift[v] & c
            assert len(outs) == 1
            v = next(iter(outs))
            word += v[0][-1]
            if v == start:
                break
        basis = {24: T, 28: A, 104: W}[len(word)]
        assert word in {basis[j:]+basis[:j] for j in range(len(basis))}
        names[i] = {24: 'T', 28: 'A', 104: 'W'}[len(word)]
        cycle_words[i] = word
    rank = {}
    for i in reversed(ltop):
        weight = (int(names.get(i) == 'T'), int(names.get(i) == 'W'),
                  int(names.get(i) == 'A'), int(i in lc), int(i not in lc),
                  len(comps[i]) if i in lc else 0)
        rank[i] = tuple(weight[j]+max([rank[k][j] for k in ldag[i]]+[0]) for j in range(6))
        for k in ldag[i]:
            assert all(rank[i][j] >= weight[j]+rank[k][j] for j in range(6))
    maxima = tuple(max(x[j] for x in rank.values()) for j in range(6))
    assert maxima == (1, 1, 3, 5, 956, 212)
    # The common-normal statement is checked on the full orientation lift.
    oriented = {(v, k, h): {(u, n, (h+(1 if u[-1] == 'R' else -1)) % 4)
                            for u, n in outs}
                for (v, k), outs in lift.items() for h in range(4)}
    oc, oi, odag, otop, ocyc = condensation(oriented)
    normals = ((1, 0), (0, 1), (-1, 0), (0, -1))
    masks = {}
    for i in ocyc:
        c = oc[i]
        v = start = min(c)
        word = ''
        while True:
            outs = oriented[v] & c
            assert len(outs) == 1
            v = next(iter(outs))
            word += v[0][-1]
            if v == start:
                break
        _, d, _, h = geometry(word, start[2])
        assert h == start[2] and d != (0, 0)
        masks[i] = sum(1 << j for j, n in enumerate(normals) if n[0]*d[0]+n[1]*d[1] >= 0)
    reached = {i: {masks.get(i, 15)} for i in odag}
    for i in otop:
        for j in odag[i]:
            reached[j] |= {m & masks.get(j, 15) for m in reached[i]}
    assert all(0 not in ss for ss in reached.values())
    for i in odag:
        assert masks.get(i, 15) in reached[i]
        for j in odag[i]:
            assert {m & masks.get(j, 15) for m in reached[i]} <= reached[j]
    return dict(adj=dict(adj), lift=lift, component=lid, cycles=names,
                components=comps, phase=phase, report={
                    'base_vertices': len(adj), 'base_edges': len(words),
                    'cyclic_downstream_sizes': order_table,
                    'lifted_vertices': len(lift), 'lifted_edges': sum(map(len, lift.values())),
                    'path_maxima_T_W_A_cycles_literal_periodsum': maxima,
                    'literal_allowance': 149+maxima[4]+maxima[5]+maxima[3],
                    'oriented_vertices': len(oriented),
                    'oriented_edges': sum(map(len, oriented.values())),
                    'common_normal_mask_states': sum(map(len, reached.values())),
                    'common_normal_closed_and_nonempty': True,
                    'quotient_sha256': quotient_hash})


def parse(word, data):
    """Exact SCC decomposition of a supplied physical ten-legal word.

    The caller separately checks full physical feasibility. Graph admission
    alone is not a positive physical certificate.
    """
    if len(word) < 150:
        return {'literal': len(word), 'T': [], 'A': [], 'W': [], 'core_start': 0, 'core_length': 0}
    hist = word[:149]
    node = (hist, 0)
    assert node in data['lift']
    i = 149
    runs = []
    fixed = 149
    while i < len(word):
        cid = data['component'][node]
        start = i
        if cid not in data['cycles']:
            ch = word[i]
            nxt = hist[1:]+ch
            matches = [u for u in data['lift'][node] if u[0] == nxt]
            assert len(matches) == 1
            node = matches[0]
            hist = nxt
            i += 1
            fixed += 1
            continue
        # Consume every internal cycle edge, then separately its exiting edge.
        while i < len(word):
            nxt = hist[1:]+word[i]
            matches = [u for u in data['lift'][node] if u[0] == nxt]
            assert len(matches) == 1
            u = matches[0]
            if data['component'][u] != cid:
                break
            node, hist = u, nxt
            i += 1
        period = len(data['components'][cid])
        count, remainder = divmod(i-start, period)
        runs.append((data['cycles'][cid], start, period, count))
        fixed += remainder
        if i < len(word):
            nxt = hist[1:]+word[i]
            matches = [u for u in data['lift'][node] if u[0] == nxt]
            node, hist = matches[0], nxt
            i += 1
            fixed += 1
    result = {'literal': fixed, 'T': [], 'A': [], 'W': [], 'core_start': 0, 'core_length': 0}
    for name, start, period, count in runs:
        result[name].append(count)
        if name == 'W':
            result['core_start'] = start
            result['core_length'] = period*count
    assert fixed <= 1322 and len(result['T']) <= 1 and len(result['W']) <= 1 and len(result['A']) <= 3
    assert len(word) == fixed+24*sum(result['T'])+104*sum(result['W'])+28*sum(result['A'])
    return result
