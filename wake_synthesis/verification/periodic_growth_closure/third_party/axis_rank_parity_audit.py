#!/usr/bin/env python3
"""Audit a candidate lifted-rank parity identity for axis displacement (2, 0).

This file records finite evidence and local-rewrite diagnostics.  It is not a
proof.  A macro letter encodes two ant moves, first horizontal and then
vertical, after starting with vertical heading north:

    U=(+1,+1), u=(-1,-1), V=(+1,-1), v=(-1,+1).

For a heading-reset path ending at (2,0), the conjectured identity is

    sum(rank(i) for left-turn events i) = N/4 + 1  (mod 2),

where occurrences in each translation class modulo d=(2,0) are ranked by
decreasing x and then increasing phase.  This is exactly the stable P3 order.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
from typing import Iterable


MACRO = {
    "U": (1, 1),
    "u": (-1, -1),
    "V": (1, -1),
    "v": (-1, 1),
}


def turns_from_macro(word: str) -> str:
    """Recover the unique turn word, with initial heading north."""
    incoming_vertical = 1
    turns: list[str] = []
    for letter in word:
        horizontal, outgoing_vertical = MACRO[letter]
        turns.append("L" if horizontal == -incoming_vertical else "R")
        turns.append("L" if horizontal == outgoing_vertical else "R")
        incoming_vertical = outgoing_vertical
    return "".join(turns)


def trace(turns: str) -> tuple[list[tuple[int, int]], tuple[int, int], int]:
    """Return event positions, endpoint, and final compass heading."""
    directions = ((1, 0), (0, -1), (-1, 0), (0, 1))  # E,S,W,N
    heading = 3
    x = y = 0
    positions: list[tuple[int, int]] = []
    for turn in turns:
        positions.append((x, y))
        heading = (heading + (1 if turn == "R" else -1)) % 4
        dx, dy = directions[heading]
        x += dx
        y += dy
    return positions, (x, y), heading


def lifted_rank_parity(turns: str) -> int:
    """Sum zero-based stable ranks of L events, modulo two."""
    positions, _, _ = trace(turns)
    groups: dict[tuple[int, int], list[int]] = {}
    for phase, (x, y) in enumerate(positions):
        groups.setdefault((x % 2, y), []).append(phase)

    rank: dict[int, int] = {}
    for phases in groups.values():
        ordered = sorted(phases, key=lambda i: (-positions[i][0], i))
        rank.update({phase: value for value, phase in enumerate(ordered)})
    return sum(rank[i] for i, turn in enumerate(turns) if turn == "L") % 2


def valid_axis_macro(word: str) -> bool:
    turns = turns_from_macro(word)
    _, endpoint, heading = trace(turns)
    return endpoint == (2, 0) and heading == 3 and len(turns) % 4 == 0


def inversion_parity(bits: list[int]) -> int:
    """Parity of pairs 1...0 in a binary list."""
    ones = 0
    answer = 0
    for bit in bits:
        if bit:
            ones += 1
        else:
            answer ^= ones & 1
    return answer


def permutation_parity(values: list[int]) -> int:
    """Parity of a permutation, by cycle decomposition."""
    seen = [False] * len(values)
    cycles = 0
    for start in range(len(values)):
        if seen[start]:
            continue
        cycles += 1
        value = start
        while not seen[value]:
            seen[value] = True
            value = values[value]
    return (len(values) - cycles) & 1


def factorization_audit(word: str) -> None:
    """Check every equality in the port-permutation proof candidate."""
    turns = turns_from_macro(word)
    positions, endpoint, heading = trace(turns)
    assert endpoint == (2, 0) and heading == 3
    period = len(turns)
    macros = len(word)

    # Incoming and outgoing physical-direction bits at every event.  Positive
    # means N at an even/Q event and E at an odd/C event on input; it means E
    # at Q and N at C on output.
    incoming_vertical = 1
    port_bits: list[tuple[int, int]] = []
    edge_count: Counter[tuple[str, int]] = Counter()
    for macro_index, letter in enumerate(word):
        horizontal, outgoing_vertical = MACRO[letter]
        row = positions[2 * macro_index][1]
        port_bits.append((int(incoming_vertical > 0), int(horizontal > 0)))
        port_bits.append((int(horizontal > 0), int(outgoing_vertical > 0)))
        edge_count[("E" if horizontal > 0 else "W", row)] += 1
        edge_count[("N" if outgoing_vertical > 0 else "S", row)] += 1
        incoming_vertical = outgoing_vertical

    groups: dict[tuple[int, int], list[int]] = defaultdict(list)
    for phase, (x, y) in enumerate(positions):
        # Since x+y == phase (mod 2), phase parity at fixed y is exactly
        # x mod 2, the quotient residue for d=(2,0).
        groups[(phase & 1, y)].append(phase)
    rank: dict[int, int] = {}
    ordered_groups: dict[tuple[int, int], list[int]] = {}
    for key, phases in groups.items():
        ordered = sorted(phases, key=lambda i: (-positions[i][0], i))
        ordered_groups[key] = ordered
        rank.update({phase: value for value, phase in enumerate(ordered)})

    local_sign = 0
    linear = 0
    edge_binomials = 0
    row_binomials = 0
    for (kind, _row), phases in ordered_groups.items():
        a = [port_bits[i][0] for i in phases]
        b = [port_bits[i][1] for i in phases]
        count_a = sum(a)
        count_b = sum(b)
        size = len(phases)
        local_sign ^= inversion_parity(a) ^ inversion_parity(b)
        linear ^= ((count_a + count_b) * (size - 1)) & 1
        edge_binomials ^= (
            count_a * (count_a - 1) // 2
            + count_b * (count_b - 1) // 2
        ) & 1
        if kind == 1:
            row_binomials ^= (size * (size - 1) // 2) & 1

    k_value = lifted_rank_parity(turns)
    assert k_value == (
        local_sign ^ linear ^ edge_binomials ^ row_binomials
    )
    assert linear == 0
    assert edge_binomials == 0

    # Independently form the edge-block permutation between output-port and
    # input-port sorted occurrence lists.
    vertex_keys = sorted(groups, key=lambda key: (key[1], key[0]))
    input_order: list[int] = []
    output_order: list[int] = []
    for key in vertex_keys:
        phases = ordered_groups[key]
        input_order.extend(sorted(phases, key=lambda i: (port_bits[i][0], rank[i])))
        output_order.extend(sorted(phases, key=lambda i: (port_bits[i][1], rank[i])))
    input_position = {phase: value for value, phase in enumerate(input_order)}
    edge_permutation = [input_position[(phase + 1) % period] for phase in output_order]
    edge_sign = permutation_parity(edge_permutation)
    assert local_sign ^ edge_sign == 1  # one even-length phase cycle

    horizontal = Counter()
    north = Counter()
    south = Counter()
    for (direction, row), count in edge_count.items():
        if direction in "EW":
            horizontal[row] += count
        elif direction == "N":
            north[row] += count
        else:
            south[row] += count
    rows = set(horizontal) | set(north) | set(south)
    rows |= {row + delta for row in tuple(rows) for delta in (-2, -1, 1, 2)}
    assert all(south[row + 1] == north[row] for row in rows)
    assert all(horizontal[row] == north[row - 1] + north[row] for row in rows)

    # Direct block-inversion formula on the quotient ladder.
    edge_formula = 0
    for row in rows:
        edge_formula ^= (
            horizontal[row] * (south[row] + south[row + 1])
            + north[row] * (south[row + 1] + south[row + 2])
        ) & 1
    assert edge_sign == edge_formula

    north_sum = sum(north.values())
    adjacent_north = sum(north[row] * north[row + 1] for row in rows) & 1
    assert macros == 2 * north_sum
    assert edge_sign == ((north_sum & 1) ^ adjacent_north)
    assert row_binomials == adjacent_north
    assert k_value == ((macros // 2 + 1) & 1)


def exhaustive(max_macros: int) -> dict[int, int]:
    """Exhaustively audit all macro words through the requested length."""
    counts: dict[int, int] = {}
    for macros in range(2, max_macros + 1, 2):
        count = 0
        for letters in product(MACRO, repeat=macros):
            word = "".join(letters)
            if not valid_axis_macro(word):
                continue
            turns = turns_from_macro(word)
            assert lifted_rank_parity(turns) == (len(turns) // 4 + 1) % 2
            factorization_audit(word)
            count += 1
        counts[2 * macros] = count
    return counts


def rewrite_deltas(words: Iterable[str]) -> dict[str, set[int]]:
    """Measure K changes under basic free-lattice rewrites.

    The contexts need not themselves have endpoint (2,0).  Results are grouped
    by rewrite type to reveal whether a context-free induction is plausible.
    """
    inverse = {"U": "u", "u": "U", "V": "v", "v": "V"}
    axis = {"U": 0, "u": 0, "V": 1, "v": 1}
    deltas: dict[str, set[int]] = {"cancel": set(), "commute": set()}
    for word in words:
        for i in range(len(word) - 1):
            a, b = word[i : i + 2]
            before = lifted_rank_parity(turns_from_macro(word))
            if inverse[a] == b:
                shorter = word[:i] + word[i + 2 :]
                after = lifted_rank_parity(turns_from_macro(shorter))
                deltas["cancel"].add(before ^ after)
            if axis[a] != axis[b]:
                swapped = word[:i] + b + a + word[i + 2 :]
                after = lifted_rank_parity(turns_from_macro(swapped))
                deltas["commute"].add(before ^ after)
    return deltas


def main() -> None:
    counts = exhaustive(8)
    contexts = ("".join(chars) for n in range(2, 7) for chars in product(MACRO, repeat=n))
    deltas = rewrite_deltas(contexts)
    print("schema=langton-axis-rank-parity-audit-v1")
    for period, count in counts.items():
        print(f"period={period} endpoint_words={count} failures=0")
    print(f"rewrite_deltas={deltas}")
    print("status=bounded_evidence_not_proof")


if __name__ == "__main__":
    main()
