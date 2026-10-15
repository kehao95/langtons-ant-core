"""Integer-only 168 upper certificate, generated without numerical optimization.

This graph deliberately forgets longitudinal residue and is only a necessary
model. The exact enumeration in the separate module retains that residue.
A capped longest-path construction proposes a potential; EVERY edge is checked.
"""
from __future__ import annotations
from collections import deque
import hashlib
import json

MOVES = ((0, 1), (1, 0), (0, -1), (-1, 0))
DENSITY = (2, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2)
ALPHA = (-50, 32, -18, 8, -2, 0, -2, 8, -18, 32, -50)


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def forbidden() -> list[str]:
    """First-return words of at most 20 updates, followed by the wrong read."""
    result: set[str] = set()
    board: dict[tuple[int, int], int] = {}
    path: list[str] = []

    def visit(x: int, y: int, h: int) -> None:
        length = len(path)
        if length and x == y == 0:
            word = ''.join(path) + path[0]
            result.add(word)
            result.add(''.join('1' if c == '0' else '0' for c in word))
            return
        if length == 20 or abs(x) + abs(y) > 20 - length:
            return
        old = board.get((x, y))
        choices = [old] if old is not None else ([0] if not length else [0, 1])
        for bit in choices:
            board[x, y] = 1 - bit
            path.append(str(bit))
            new_h = (h + (1 if bit == 0 else -1)) % 4
            dx, dy = MOVES[new_h]
            visit(x + dx, y + dy, new_h)
            path.pop()
        if old is None:
            del board[x, y]
        else:
            board[x, y] = old

    visit(0, 0, 0)
    return sorted(result)


def geometry(word: str):
    """Vector turns, independent of the recursive factor generator."""
    x = y = 0
    dx, dy = 0, 1
    points = []
    previous = {}
    conflict = False
    for bit in word:
        if bit not in '01':
            raise ValueError('Nonbinary factor')
        p = x, y
        if p in previous and previous[p] == bit:
            conflict = True
        previous[p] = bit
        points.append(p)
        dx, dy = (dy, -dx) if bit == '0' else (-dy, dx)
        x, y = x + dx, y + dy
    return points, (x, y), MOVES.index((dx, dy)), conflict


def rotate(p, n):
    x, y = p
    for _ in range(n % 4):
        x, y = y, -x
    return x, y


def graph(patterns):
    """Direct suffix matching and forward placement; no failure-link code."""
    bad = set(patterns)
    lengths = sorted({len(p) for p in patterns})

    def forbidden_suffix(s):
        return any(len(s) >= n and s[-n:] in bad for n in lengths)

    prefixes = dict.fromkeys([''])
    for word in patterns:
        for k in range(1, len(word) + 1):
            prefixes.setdefault(word[:k], None)
    contexts = [s for s in prefixes if not forbidden_suffix(s)]
    index = {s: i for i, s in enumerate(contexts)}
    transition = []
    spans = []
    for context in contexts:
        row = []
        for bit in '01':
            s = context + bit
            if forbidden_suffix(s):
                row.append(-1)
            else:
                for k in range(len(s), -1, -1):
                    suffix = s[-k:] if k else ''
                    if suffix in index:
                        row.append(index[suffix])
                        break
        transition.append(row)
        points, endpoint, end_h, _ = geometry(context)
        span = []
        for h in range(4):
            sums = [0] + [sum(rotate((p[0]-endpoint[0], p[1]-endpoint[1]), h-end_h)) for p in points]
            span.append((min(sums), max(sums)))
        spans.append(span)
    states = [(t, h, a) for t in range(-10, 1) for h in range(4)
              if h % 2 == (t+1) % 2
              for a in range(len(contexts))
              if t+spans[a][h][0] >= -10 and t+spans[a][h][1] <= 0]
    lookup = {s: i for i, s in enumerate(states)}
    edges = []
    for i, (t, h, a) in enumerate(states):
        for bit in (0, 1):
            nxt = transition[a][bit]
            if nxt < 0:
                continue
            new_h = (h + (1 if bit == 0 else -1)) % 4
            dx, dy = MOVES[new_h]
            j = lookup.get((t+dx+dy, new_h, nxt))
            if j is not None:
                edges.append((i, j, ALPHA[t+10]*(1-2*bit)))
    return states, edges, contexts


def verify() -> dict:
    patterns = forbidden()
    if len(patterns) != 588 or max(map(len, patterns)) != 21:
        raise ValueError('Factor recipe changed')
    if not all(geometry(word)[3] for word in patterns):
        raise ValueError('A proposed forbidden factor is consistent')
    states, edges, contexts = graph(patterns)
    n = len(states)
    if (len(contexts), n, len(edges)) != (4931, 54718, 90158):
        raise ValueError('Graph recipe changed')
    adjacency = [[] for _ in states]
    for i, j, cost in edges:
        adjacency[i].append((j, cost+1))
    potential = [0] * n
    queued = bytearray([1]) * n
    pending = deque(range(n))
    pops = updates = 0
    while pending:
        i = pending.popleft()
        queued[i] = 0
        pops += 1
        for j, cost in adjacency[i]:
            candidate = potential[i] + cost
            if candidate > potential[j]:
                if candidate > 180:
                    raise ValueError('Potential witness construction failed')
                potential[j] = candidate
                updates += 1
                if not queued[j]:
                    queued[j] = 1
                    pending.append(j)
    # A second scan is the certificate check. The construction is not trusted.
    worst = max(potential[i]-potential[j]+cost for i, j, cost in edges)
    if worst > -1:
        raise ValueError('Integer inequality failed')
    budget = -sum(a*o for a, o in zip(ALPHA, DENSITY))
    if budget != 168:
        raise ValueError('Wake sum failed')
    return {'verified': True, 'period_bound': budget,
            'forbidden_factors': len(patterns), 'max_factor_length': 21,
            'contexts': len(contexts), 'vertices': n, 'edges': len(edges),
            'alpha': list(ALPHA), 'scale': 1, 'maximum_edge_lhs': worst,
            'potential_range': [min(potential), max(potential)],
            'queue_pops': pops, 'potential_updates': updates,
            'patterns_sha256': digest(patterns), 'states_sha256': digest(states),
            'edges_sha256': digest(edges), 'potential_sha256': digest(potential),
            'no_optimizer_or_float_used': True}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))
