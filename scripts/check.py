#!/usr/bin/env python3
"""Replay every proof obligation currently claimed by this repository."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from langtons_ant.highway import (
    ENTRY_UPDATES,
    clean_envelope_entry,
    first_blank_hit,
    verify_blank_highway,
    verify_prefix_one_black,
)
from langtons_ant.model import Heading, State, advance
from langtons_ant.one_black import (
    verify_actual_entry_ordinary,
    verify_phase72,
    verify_pristine_one_obstacle,
)
from langtons_ant.renewal import Carrier, initial_carrier, renew


def main() -> None:
    witness = verify_blank_highway()
    verify_prefix_one_black(witness)
    verify_pristine_one_obstacle(witness)
    verify_actual_entry_ordinary(witness)
    verify_phase72(witness)
    if not clean_envelope_entry(State.blank(), witness):
        raise AssertionError("blank state fails its clean-envelope theorem")
    if first_blank_hit(frozenset({(0, 0)}), (0, 0), State.blank().heading, witness) != 0:
        raise AssertionError("blank interaction index has the wrong origin hit")
    if renew(initial_carrier(State.blank()), witness).kind != "blank-coupled":
        raise AssertionError("blank renewal program did not halt by coupling")
    entry = advance(State.blank(), ENTRY_UPDATES + 1)
    if renew(Carrier(entry, entry.black, ENTRY_UPDATES + 1), witness).kind != "terminal":
        raise AssertionError("renewal terminal test is not phase-complete")
    seed = State(frozenset({(-2, -2)}), (0, 0), Heading.NORTH)
    edge = renew(initial_carrier(seed), witness)
    if (
        edge.kind != "renewed"
        or edge.target is None
        or not edge.source.old < edge.target.old
        or edge.target.old != edge.source.old | edge.footprint
        or edge.target.time <= edge.source.time
    ):
        raise AssertionError("renewal edge lost strict complete-history progress")
    print(
        "verified: blank P104; interaction index; renewal outcomes; clean envelope; "
        "universal one-black partition"
    )


if __name__ == "__main__":
    main()
