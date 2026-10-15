"""Delete transient vertices before checking the standard-wake upper bound.

The input graph recipe is unchanged.  Every closed walk survives zero-degree
peeling, and a separate reverse-insertion check certifies the deletion order.
Only the retained edges need integer potential inequalities.  Python stdlib
only; no optimizer, floating-point premise, or external certificate file.
"""
from __future__ import annotations

import argparse
from collections import deque
import hashlib
import importlib.util
import json
from pathlib import Path


ALPHA = (-50, 32, -18, 8, -2, 0, -2, 8, -18, 32, -50)
DENSITY = (2, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def adjacency(n, edges):
    outgoing = [[] for _ in range(n)]
    incoming = [[] for _ in range(n)]
    for i, j, _ in edges:
        outgoing[i].append(j)
        incoming[j].append(i)
    return outgoing, incoming


def peel(n, edges):
    """Propose the closed-walk core and a deterministic deletion certificate."""
    outgoing, incoming = adjacency(n, edges)
    indegree = [len(row) for row in incoming]
    outdegree = [len(row) for row in outgoing]
    active = bytearray([1]) * n
    queue = deque(i for i in range(n) if not indegree[i] or not outdegree[i])
    deleted = []
    while queue:
        i = queue.popleft()
        if not active[i] or (indegree[i] and outdegree[i]):
            continue
        active[i] = 0
        deleted.append(i)
        for j in outgoing[i]:
            indegree[j] -= 1
            if active[j] and not indegree[j]:
                queue.append(j)
        for j in incoming[i]:
            outdegree[j] -= 1
            if active[j] and not outdegree[j]:
                queue.append(j)
    return [i for i in range(n) if active[i]], deleted


def check_deletions(n, edges, retained, deleted):
    """Check the proposed certificate by insertion, without peeling counters.

    Reverse insertion reconstructs the graph that existed at each deletion.
    The inserted vertex must have no predecessor OR no successor in that graph.
    Include self-loops explicitly: a self-loop cannot be deleted.
    """
    if (len(retained) + len(deleted) != n
            or len(set(retained + deleted)) != n
            or set(retained + deleted) != set(range(n))):
        raise ValueError('Deletion certificate does not partition the vertices')
    outgoing, incoming = adjacency(n, edges)
    active = bytearray(n)
    for i in retained:
        active[i] = 1
    for i in reversed(deleted):
        active[i] = 1
        has_in = any(active[j] for j in incoming[i])
        has_out = any(active[j] for j in outgoing[i])
        if has_in and has_out:
            raise ValueError('A deleted vertex could lie on a closed walk')


def potential(n, edges):
    """Propose integers using capped relaxation; the second scan is decisive."""
    outgoing = [[] for _ in range(n)]
    for i, j, cost in edges:
        outgoing[i].append((j, cost + 1))
    values = [0] * n
    queued = bytearray([1]) * n
    pending = deque(range(n))
    pops = updates = 0
    while pending:
        i = pending.popleft()
        queued[i] = 0
        pops += 1
        for j, cost in outgoing[i]:
            candidate = values[i] + cost
            if candidate > values[j]:
                if candidate > 180:
                    raise ValueError('Potential reconstruction exceeded its cap')
                values[j] = candidate
                updates += 1
                if not queued[j]:
                    queued[j] = 1
                    pending.append(j)
    return values, pops, updates


def check_potential(n, edges, values):
    if len(values) != n or any(type(v) is not int or not 0 <= v <= 180
                               for v in values):
        raise ValueError('Malformed potential')
    worst = max(values[i] - values[j] + cost for i, j, cost in edges)
    if worst > -1:
        raise ValueError('Integer potential inequality failed')
    return worst


def must_reject(fn, *args):
    try:
        fn(*args)
    except ValueError:
        return
    raise ValueError('Negative control was accepted')


def controls(n, edges, retained, deleted, core_edges, values):
    # Two distinct recurrent components, including a self-loop, must survive.
    toy = [(0, 1, 0), (1, 2, 0), (2, 1, 0), (2, 3, 0),
           (4, 4, 0), (5, 6, 0)]
    kept, removed = peel(7, toy)
    if kept != [1, 2, 4]:
        raise ValueError('Peeling lost a recurrent component')
    check_deletions(7, toy, kept, removed)
    must_reject(check_deletions, 7, toy, [1, 2], removed + [4])
    must_reject(check_deletions, n, edges, retained[1:], deleted + retained[:1])
    # Raise a source potential until one real retained edge has left side zero.
    i, j, cost = core_edges[0]
    corrupt = list(values)
    corrupt[i] = values[j] - cost
    must_reject(check_potential, len(retained), core_edges, corrupt)
    return {'disconnected_cycles_and_self_loop_preserved': True,
            'deletion_of_self_loop_rejected': True,
            'deletion_of_actual_core_vertex_rejected': True,
            'violated_edge_inequality_rejected': True}


def verify(upper_source=None):
    """Use an explicit source path when importing into another package layout."""
    source = Path(upper_source) if upper_source else (
        Path(__file__).resolve().parents[1]
        / 'standard_wake_uniqueness' / 'upper_bound.py')
    spec = importlib.util.spec_from_file_location('wake_upper_recipe', source)
    if spec is None or spec.loader is None:
        raise ValueError('Cannot load the upper-bound graph recipe')
    upper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(upper)
    if tuple(upper.ALPHA) != ALPHA or tuple(upper.DENSITY) != DENSITY:
        raise ValueError('Upper-bound input contract changed')
    patterns = upper.forbidden()
    if len(patterns) != 588 or max(map(len, patterns)) != 21:
        raise ValueError('Forbidden-factor recipe changed')
    if not all(upper.geometry(word)[3] for word in patterns):
        raise ValueError('A proposed forbidden factor is physically consistent')
    states, edges, contexts = upper.graph(patterns)
    if (len(contexts), len(states), len(edges)) != (4931, 54718, 90158):
        raise ValueError('Graph recipe changed')
    retained, deleted = peel(len(states), edges)
    check_deletions(len(states), edges, retained, deleted)
    lookup = {old: new for new, old in enumerate(retained)}
    # Include EVERY original edge between retained vertices, without selection.
    core_edges = [(lookup[i], lookup[j], c) for i, j, c in edges
                  if i in lookup and j in lookup]
    if (len(retained), len(core_edges)) != (24424, 37330):
        raise ValueError('Closed-walk core changed')
    values, pops, updates = potential(len(retained), core_edges)
    worst = check_potential(len(retained), core_edges, values)
    budget = -sum(a * o for a, o in zip(ALPHA, DENSITY))
    if budget != 168:
        raise ValueError('Wake sum changed')
    checks = controls(len(states), edges, retained, deleted, core_edges, values)
    return {'verified': True, 'period_bound': budget,
            'forbidden_factors': len(patterns), 'max_factor_length': 21,
            'contexts': len(contexts),
            'original_vertices': len(states), 'original_edges': len(edges),
            'retained_vertices': len(retained), 'retained_edges': len(core_edges),
            'deleted_vertices': len(deleted),
            'alpha': list(ALPHA), 'scale': 1,
            'maximum_edge_lhs': worst,
            'potential_range': [min(values), max(values)],
            'queue_pops': pops, 'potential_updates': updates,
            'graph_recipe_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'patterns_sha256': digest(patterns),
            'original_states_sha256': digest(states),
            'original_edges_sha256': digest(edges),
            'retained_vertices_sha256': digest(retained),
            'deletion_order_sha256': digest(deleted),
            'retained_edges_sha256': digest(core_edges),
            'potential_sha256': digest(values),
            'controls': checks, 'no_optimizer_or_float_used': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upper-source', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.upper_source), indent=2))
