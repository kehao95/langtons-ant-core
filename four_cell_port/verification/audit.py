#!/usr/bin/env python3
"""Independent integer audit of immutable certificates and exterior completion.

No imports from the original two checkers. Infinite-time verification examines
all per-cell visit lists on finitely many constant intervals, including the
last unbounded interval. Sampled completion cases test the implementation;
the universal completion theorem uses the written geometric proof.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import random
import sys
from completion import GATE, complete, inside, place, step


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def ratio(delta, drift):
    axis = 0 if drift[0] else 1
    if not drift[axis] or delta[axis] % drift[axis]:
        return None
    k = delta[axis] // drift[axis]
    return k if delta == (k * drift[0], k * drift[1]) else None


def plan(p, h, word):
    start, direction = p, h
    phases = []
    for turn in word:
        require(turn in 'LR', 'invalid turn')
        phases.append(p)
        dx, dy = h
        h = (-dy, dx) if turn == 'L' else (dy, -dx)
        p = p[0] + h[0], p[1] + h[1]
    drift = p[0] - start[0], p[1] - start[1]
    require(h == direction and drift != (0, 0), 'not a translating word')
    return phases, drift


def certify_cells(board, p, h, word):
    """Check chronological visits per physical cell, without phase-epoch XOR."""
    phases, drift = plan(p, h, word)
    classes = []
    for i, q in enumerate(phases):
        for anchor, members in classes:
            a = ratio((q[0] - anchor[0], q[1] - anchor[1]), drift)
            if a is not None:
                members.append((i, a))
                break
        else:
            classes.append((q, [(i, 0)]))
    tested = 0
    for anchor, members in classes:
        first = min(a for _, a in members)
        events = {a for _, a in members}
        for q in board:
            n = ratio((q[0] - anchor[0], q[1] - anchor[1]), drift)
            if n is not None and n >= first:
                events.update((n, n + 1))
        for n in sorted(events):
            q = anchor[0] + n * drift[0], anchor[1] + n * drift[1]
            bit = q in board
            visits = sorted((len(word) * (n - a) + i, i)
                            for i, a in members if a <= n)
            require(visits, 'empty class interval')
            for _, i in visits:
                require(bit == (word[i] == 'L'), f'incompatible cell {q}, phase {i}')
                bit = not bit
            tested += 1
    return {'classes': len(classes), 'cell_interval_tests': tested, 'drift': drift}


def replay(seed, count, p=(0, 0), h=(1, 0)):
    board, trace = set(seed), []
    for _ in range(count):
        trace.append((p, h, p in board))
        p, h, _ = step(board, p, h)
    return board, p, h, trace


def verify_table(table):
    family = {frozenset()}
    rows_checked, maxima = 0, []
    require(len(table) == 4, 'wrong depth')
    for depth, rows in enumerate(table):
        seeds = [frozenset(map(tuple, row['seed'])) for row in rows]
        require(len(seeds) == len(set(seeds)) and set(seeds) == family,
                'missing, duplicate or extraneous family member')
        following, times = set(), []
        for seed, row in zip(seeds, rows):
            require(len(seed) == depth, 'incorrect black budget')
            board, p, h, seen, time = set(seed), (0, 0), (1, 0), set(), 0
            while p[0] >= 0:
                require(time < 918, 'uniform bound exceeded')
                if p not in seen and p not in seed:
                    following.add(seed | {p})
                seen.add(p)
                p, h, _ = step(board, p, h)
                time += 1
            require(time == row['time'] and list(p) == row['exit'], 'wrong exit certificate')
            times.append(time)
            rows_checked += 1
        maxima.append(max(times))
        family = following
    require(maxima == [2, 38, 106, 918], 'wrong maxima')
    return rows_checked


def must_reject(action):
    try:
        action()
    except AssertionError:
        return
    raise AssertionError('corrupted certificate accepted')


def completion_cases(word):
    rng = random.Random(20261015)
    cases, headings, longest = 0, set(), 0
    for i in range(96):
        offset = (10**30, -10**30) if i >= 80 else (0, 0)
        shift = lambda q: (q[0] + offset[0], q[1] + offset[1])
        seed = {shift((x, y)) for x in range(-2, 3) for y in range(-2, 3)
                if rng.randrange(4) == 0}
        h = ((1, 0), (0, 1), (-1, 0), (0, -1))[i % 4]
        p = shift((0, 0)); prefix = (0, 1, 7, 20)[(i // 4) % 4]
        protected = {shift((-3, 1)), shift((2, 3))}
        added, certificate = complete(seed, p, h, protected, prefix, i % 3)
        square, tau = certificate['square'], certificate['exit_time']
        ep, eh = certificate['exit_position'], certificate['exit_heading']
        require(len(added) == 4 and not added & (seed | protected), 'invalid edit set')
        require(all(not inside(q, square) for q in added), 'nonexterior edit')
        require(tau > prefix and tau <= 8 * square[2] * 3**square[2] + 1, 'exit budget')
        original, augmented = set(seed), set(seed) | added
        op, oh, ap, ah = p, h, p, h
        for _ in range(tau):
            require((op, oh, op in original) == (ap, ah, ap in augmented), 'prefix diverges')
            require(original ^ augmented == added, 'wrong complete-field difference')
            op, oh, _ = step(original, op, oh)
            ap, ah, _ = step(augmented, ap, ah)
        require((ap, ah) == (ep, eh) and original == certificate['exit_black'], 'exit mismatch')
        debris = set(original)
        require(debris ^ augmented == added, 'exit field union')
        require(all(inside(q, square) for q in debris), 'debris escaped square')
        for _ in range(182):
            require((ap[0] - ep[0]) * eh[0] + (ap[1] - ep[1]) * eh[1] >= 0,
                    'gate crossed supporting line')
            ap, ah, _ = step(augmented, ap, ah)
        require(ap == place((5, 1), ep, eh) and ah == eh, 'placed endpoint')
        require(len(augmented - debris) == 36 and debris <= augmented, 'lost physical debris')
        certify_cells(augmented, ap, ah, word)
        phases, d = plan(ap, ah, word)
        require(d[0] * eh[0] + d[1] * eh[1] > 0, 'nonoutward tail')
        require(all((q[0] - ep[0]) * eh[0] + (q[1] - ep[1]) * eh[1] >= 0
                    for q in phases), 'tail crosses supporting line')
        cases += 1; headings.add(eh); longest = max(longest, tau)
    require(len(headings) == 4, 'not all exit sides covered')
    return {'cases': cases, 'exit_sides': 4, 'max_sample_exit': longest,
            'huge_coordinate_cases': 16, 'full_field_xor_checked': True}


def main():
    root = Path(sys.argv[1])
    table = json.loads((root / 'escapes.json').read_text())
    witness = json.loads((root / 'witness.json').read_text())
    rows = verify_table(table)
    corrupt = copy.deepcopy(table); corrupt[-1].pop()
    must_reject(lambda: verify_table(corrupt))
    corrupt = copy.deepcopy(table); corrupt[0][0]['time'] += 1
    must_reject(lambda: verify_table(corrupt))
    b, p, h, prefix = replay(GATE, 182)
    require((p, h, len(b)) == ((5, 1), (1, 0), 36), 'gate endpoint')
    require(min(q[0] for q, _, _ in prefix) >= 0, 'gate prefix leaves')
    require(sorted(b) == list(map(tuple, witness['gate']['black_after_182'])), 'field mismatch')
    bb, bp, bh, _ = replay(set(), 9977, h=(0, 1))
    _, _, _, block = replay(bb, 104, bp, bh)
    word = ''.join('L' if bit else 'R' for _, _, bit in block)
    require(word == witness['reference']['word'], 'nonstandard word')
    gate = certify_cells(b, p, h, word)
    blank = certify_cells(bb, bp, bh, word)
    phases, drift = plan(p, h, word)
    marker = (phases[0][0] + 10**100 * drift[0], phases[0][1] + 10**100 * drift[1])
    must_reject(lambda: certify_cells(b | {marker}, p, h, word))
    dormant = (-10**100, 10**100)
    certify_cells(b | {dormant}, p, h, word)
    for q in witness['gate']['canonical_tail']['minimal_seed']:
        must_reject(lambda q=tuple(q): certify_cells(b ^ {q}, p, h, word))
    reduced = []
    for q in GATE:
        board, pos, heading, time = set(GATE - {q}), (0, 0), (1, 0), 0
        while pos[0] >= 0:
            require(time < 918, 'three-cell deletion stays')
            pos, heading, _ = step(board, pos, heading); time += 1
        reduced.append(time)
    report = {'status': 'PASS', 'finite_seed_rows': rows,
              'blank_cell_certificate': blank, 'gate_cell_certificate': gate,
              'certificate_mutations_rejected': 2, 'active_cell_mutations_rejected': 13,
              'remote_blocker_epoch': str(10**100), 'dormant_marker_accepted': True,
              'gate_deletion_exit_times': sorted(reduced),
              'completion': completion_cases(word),
              'scope': 'exact finite certificates + analytic all-future reduction; completion samples test implementation'}
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
