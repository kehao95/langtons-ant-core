#!/usr/bin/env python3
"""Replay every proof obligation currently claimed by this repository."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from langtons_ant.highway import verify_blank_highway, verify_one_black_under_ant


def main() -> None:
    witness = verify_blank_highway()
    verify_one_black_under_ant(witness)
    print("verified: blank P104; one black initially under the ant")


if __name__ == "__main__":
    main()
