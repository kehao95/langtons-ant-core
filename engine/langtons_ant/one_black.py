"""A finite entry check for the smallest one-black initial family.

This module covers the state with the ant initially standing on the only black
square.  Translation and rotation transport that result to the corresponding
family at arbitrary coordinates and headings; they do not cover arbitrary
ant-to-black offsets.
"""

from __future__ import annotations

from .highway import P104Witness, is_standard_p104_boundary
from .model import Heading, State, advance

CANONICAL_ENTRY_UPDATES = 9_978


def canonical_one_black_initial() -> State:
    """Return the one-black state with the ant on that black square, facing north."""

    return State(frozenset({(0, 0)}), (0, 0), Heading.NORTH)


def canonical_one_black_entry(witness: P104Witness) -> State:
    """Compute and validate the canonical family's first recorded P104 boundary."""

    entry = advance(canonical_one_black_initial(), CANONICAL_ENTRY_UPDATES)
    if not is_standard_p104_boundary(entry, witness):
        raise AssertionError("canonical one-black trace misses its recorded P104 boundary")
    return entry
