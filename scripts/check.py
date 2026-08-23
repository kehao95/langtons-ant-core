#!/usr/bin/env python3
"""Replay every proof obligation currently claimed by this repository."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from langtons_ant.highway import (
    clean_envelope_entry,
    first_blank_hit,
    verify_blank_highway,
    verify_prefix_one_black,
)
from langtons_ant.model import State
from langtons_ant.one_black import (
    verify_actual_entry_ordinary,
    verify_phase72,
    verify_pristine_one_obstacle,
)


def main() -> None:
    witness = verify_blank_highway()
    maximum = verify_prefix_one_black(witness)
    pristine = verify_pristine_one_obstacle(witness)
    historical = verify_actual_entry_ordinary(witness)
    phase72 = verify_phase72(witness)
    if not clean_envelope_entry(State.blank(), witness):
        raise AssertionError("blank state fails its clean-envelope theorem")
    if first_blank_hit(frozenset({(0, 0)}), (0, 0), State.blank().heading, witness) != 0:
        raise AssertionError("blank interaction index has the wrong origin hit")
    print(
        "verified: blank P104; interaction index; clean envelope; "
        f"{1_376} prefix one-black cases (max {maximum} updates); "
        f"{pristine.direct_cases} pristine obstacle bases; "
        f"{historical.ordinary_lanes} ordinary historical lanes; "
        f"phase-72 hit {phase72.historical_hit}"
    )


if __name__ == "__main__":
    main()
