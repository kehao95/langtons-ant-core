#!/usr/bin/env python3
"""Bounded regression for the even-diagonal growth-four rank-sign proof.

This script is deliberately not a proof oracle.  It checks the finite local
truth tables, the two four-edge gadget permutations, every gadget-pair
interaction in a representative window, and all two-lane finite binary chains
of a requested length.  The manuscript proof supplies the unbounded finite-
support argument.
"""

from __future__ import annotations

import argparse
import itertools
import json
from math import comb


Block = tuple[str, int, int]


def source_key(block: Block) -> tuple[int, int, int]:
    kind, level, lane = block
    port = 0 if kind in ("W", "S") else 1
    return level, lane, port


def target_key(block: Block) -> tuple[int, int, int]:
    kind, level, lane = block
    port = 0 if kind in ("W", "S") else 1
    if kind == "W":
        return level - 1, 1 - lane, port
    if kind == "E":
        return level + 1, 1 - lane, port
    if kind == "S":
        return level - 1, lane, port
    if kind == "N":
        return level + 1, lane, port
    raise AssertionError(kind)


def inversion_parity(blocks: set[Block]) -> int:
    ordered = sorted(blocks, key=source_key)
    parity = 0
    for i, first in enumerate(ordered):
        for second in ordered[i + 1 :]:
            parity ^= target_key(first) > target_key(second)
    return int(parity)


def cross_parity(first: set[Block], second: set[Block]) -> int:
    parity = 0
    for a in first:
        for b in second:
            parity ^= (source_key(a) < source_key(b)) != (
                target_key(a) < target_key(b)
            )
    return int(parity)


def c_gadget(level: int, lane: int) -> set[Block]:
    return {
        ("N", level, lane),
        ("S", level + 2, lane),
        ("W", level + 1, 1 - lane),
        ("E", level + 1, 1 - lane),
    }


def q_gadget(level: int, lane: int) -> set[Block]:
    return {
        ("S", level, lane),
        ("N", level, lane),
        ("E", level - 1, lane),
        ("W", level + 1, lane),
    }


def toggle_gadget(active: set[Block], gadget: set[Block]) -> None:
    active.symmetric_difference_update(gadget)


def boundary_count(bits: tuple[int, ...]) -> int:
    padded = (0,) + bits + (0,)
    return sum(padded[i] ^ padded[i + 1] for i in range(len(padded) - 1))


def run_count(bits: tuple[int, ...]) -> int:
    padded = (0,) + bits
    return sum(padded[i] == 0 and padded[i + 1] == 1 for i in range(len(bits)))


def audit_local_corrections() -> int:
    checked = 0
    for vertex_type in ("Q", "C"):
        for multiplicity_mod4, p, excess in itertools.product(range(4), range(2), range(2)):
            if vertex_type == "Q":
                if (multiplicity_mod4 - 2 * p - excess) % 4:
                    continue
                raw = p * (multiplicity_mod4 - 1)
                reduced = p * (excess + 1)
            else:
                if (2 * p - multiplicity_mod4 - excess) % 4:
                    continue
                raw = comb(multiplicity_mod4, 2) + p * (multiplicity_mod4 - 1)
                reduced = excess * (p + 1)
            assert raw % 2 == reduced % 2
            checked += 1
    return checked


def audit_gadget_table() -> int:
    checked = 0
    for gadget in (c_gadget, q_gadget):
        base_level = 1
        for lane in range(2):
            assert inversion_parity(gadget(base_level, lane)) == 1
            checked += 1
        for other_lane in range(2):
            for separation in range(-8, 10, 2):
                if separation == 0 and other_lane == 0:
                    continue
                observed = cross_parity(
                    gadget(base_level, 0),
                    gadget(base_level + separation, other_lane),
                )
                expected = int(other_lane == 0 and abs(separation) == 2)
                assert observed == expected
                checked += 1
    return checked


def audit_chains(length: int) -> int:
    checked = 0
    levels = tuple(1 + 2 * index for index in range(length))
    for gadget in (c_gadget, q_gadget):
        for flat in itertools.product(range(2), repeat=2 * length):
            lane_bits = (flat[:length], flat[length:])
            blocks: set[Block] = set()
            for lane, bits in enumerate(lane_bits):
                for level, bit in zip(levels, bits):
                    if bit:
                        toggle_gadget(blocks, gadget(level, lane))
            edge_sign = inversion_parity(blocks)
            boundaries = tuple(boundary_count(bits) for bits in lane_bits)
            runs = tuple(run_count(bits) for bits in lane_bits)
            assert boundaries == tuple(2 * count for count in runs)
            expected = sum(comb(count, 2) for count in boundaries) % 2
            assert edge_sign == expected
            checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chain-length", type=int, default=5)
    args = parser.parse_args()
    if not 1 <= args.chain_length <= 9:
        parser.error("--chain-length must lie in 1..9")

    local_checks = audit_local_corrections()
    gadget_checks = audit_gadget_table()
    chain_checks = audit_chains(args.chain_length)
    print(
        json.dumps(
            {
                "schema": "langton-even-diagonal-rank-parity-audit-v1",
                "status": "bounded_evidence_not_proof",
                "chain_length": args.chain_length,
                "local_correction_checks": local_checks,
                "gadget_checks": gadget_checks,
                "finite_chain_checks": chain_checks,
                "all_checks_passed": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
