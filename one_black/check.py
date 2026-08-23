#!/usr/bin/env python3
"""Replay every finite obligation in the universal one-black proof."""

from langtons_ant.highway import verify_blank_highway, verify_prefix_one_black
from langtons_ant.one_black import (
    verify_actual_entry_ordinary,
    verify_phase72,
    verify_pristine_one_obstacle,
)


def main() -> None:
    witness = verify_blank_highway()
    verify_prefix_one_black(witness)
    verify_pristine_one_obstacle(witness)
    verify_actual_entry_ordinary(witness)
    verify_phase72(witness)
    print("verified: blank P104 and the universal one-black partition")


if __name__ == "__main__":
    main()
