"""Checks for the promoted one-black-under-ant restricted family."""

from __future__ import annotations

import unittest

from langtons_ant import (
    CANONICAL_ENTRY_UPDATES,
    Heading,
    State,
    advance,
    blank_p104_witness,
    canonical_one_black_entry,
    canonical_one_black_initial,
    is_standard_p104_boundary,
    is_standard_p104_terminal,
    rotate_state,
    translate_state,
)


class CanonicalOneBlackTests(unittest.TestCase):
    def test_canonical_initial_state_is_checked_at_its_recorded_entry(self) -> None:
        witness = blank_p104_witness()
        entry = canonical_one_black_entry(witness)

        self.assertEqual(CANONICAL_ENTRY_UPDATES, 9_978)
        self.assertEqual(len(entry.black), 715)
        self.assertTrue(is_standard_p104_boundary(entry, witness))
        self.assertTrue(is_standard_p104_terminal(entry, witness))

    def test_rotations_and_translations_preserve_the_entry_claim(self) -> None:
        witness = blank_p104_witness()
        entry = canonical_one_black_entry(witness)
        transported_initial = translate_state(rotate_state(canonical_one_black_initial(), 3), (11, -6))
        transported_entry = advance(transported_initial, CANONICAL_ENTRY_UPDATES)
        expected = translate_state(rotate_state(entry, 3), (11, -6))

        self.assertEqual(transported_entry, expected)
        self.assertEqual(transported_entry.heading, Heading.EAST)
        self.assertTrue(is_standard_p104_boundary(transported_entry, witness))
        self.assertTrue(is_standard_p104_terminal(transported_entry, witness))

    def test_an_offset_black_square_is_not_silently_included(self) -> None:
        witness = blank_p104_witness()
        offset = State(frozenset({(1, 0)}), (0, 0), Heading.NORTH)

        self.assertNotEqual(offset, canonical_one_black_initial())
        self.assertFalse(is_standard_p104_boundary(offset, witness))
