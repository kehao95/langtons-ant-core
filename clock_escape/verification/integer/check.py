"""Scoped exact controls for the integer-clock square-escape corollary.

The universal proof is in clock_escape/PROOF.md.
This checks all internal states and exits for side lengths 1, 2, 3, plus
the closed-form range for 100 sizes. It does not alter retained reports.
"""
from collections import Counter
from pathlib import Path
import json
import sys

from clock import integer_clock


def step(black, position, heading):
    x, y = position
    dx, dy = heading
    if position in black:
        black.remove(position)
        dx, dy = -dy, dx
    else:
        black.add(position)
        dx, dy = dy, -dx
    return (x + dx, y + dy), (dx, dy)


def main():
    if sys.flags.optimize:
        raise SystemExit('Run without Python -O')
    headings = ((0, 1), (1, 0), (0, -1), (-1, 0))
    counts = Counter()
    for n in range(1, 101):
        direct = sum((n - abs(s)) * (3**abs(s) - 1)
                     for s in range(1 - n, n))
        assert 2 * direct == 3**(n + 1) - 2*n*n - 4*n - 3
        counts['range_formula_sizes'] += 1
    maxima = {}
    for n in range(1, 4):
        cells = [(x, y) for x in range(n) for y in range(n)]
        region = set(cells)
        bound = (13*3**(n - 1) - 2*n*n - 4*n - 5) // 2
        field_range = sum(3**abs(x + y - n + 1) - 1 for x, y in cells)
        extrema = {1: [], -1: []}
        max_exit = 0
        for mask in range(1 << len(cells)):
            seed = {q for i, q in enumerate(cells) if mask >> i & 1}
            for p in cells:
                for h, heading in enumerate(headings):
                    black = seed.copy()
                    sig = (-1)**sum(p) * (1 if h % 2 == 0 else -1)
                    value = integer_clock(black, p, h, n - 1)
                    extrema[sig].append(value)
                    q, hh = step(black, p, heading)
                    if q in region:
                        s = sum(p) - n + 1
                        e, ee = sum(heading), sum(hh)
                        gain = 1 + (4*(3**abs(s) - 1) if e != ee and e*s < 0 else 0)
                        assert integer_clock(black, q, headings.index(hh), n - 1) - value == gain
                        counts['internal_transition_identities'] += 1
                    time = 1
                    while q in region and time <= bound:
                        q, hh = step(black, q, hh)
                        time += 1
                    assert q not in region and time <= bound
                    max_exit = max(max_exit, time)
                    counts['complete_initial_states'] += 1
        for values in extrema.values():
            assert max(values) - min(values) <= field_range + 2*(3**(n - 1) - 1) == bound - 1
        maxima[n] = max_exit
    print(json.dumps({'checks': dict(counts), 'exact_small_square_maxima': maxima}, sort_keys=True))


if __name__ == '__main__':
    main()
