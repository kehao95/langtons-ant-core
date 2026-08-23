"""Focused finite checks for the independently derived blank P104 witness."""

from __future__ import annotations

import unittest

from langtons_ant import (
    Heading,
    State,
    advance,
    blank_p104_witness,
    is_p104_boundary,
    is_standard_p104_boundary,
    rotate_state,
)
from langtons_ant.highway import DISPLACEMENT, ENTRY_UPDATES, PERIOD


class BlankP104WitnessTests(unittest.TestCase):
    def test_blank_entry_and_successor_match_the_same_boundary(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        successor = advance(entry, PERIOD)

        self.assertEqual(len(witness.requirements), 40)
        self.assertEqual(sum(black for _, black in witness.requirements), 13)
        self.assertTrue(is_p104_boundary(entry, witness))
        self.assertTrue(is_p104_boundary(successor, witness))
        self.assertEqual(
            (successor.position[0] - entry.position[0], successor.position[1] - entry.position[1]),
            DISPLACEMENT,
        )

    def test_one_required_colour_change_breaks_recognition(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        (dx, dy), _ = witness.requirements[0]
        changed = (entry.position[0] + dx, entry.position[1] + dy)
        altered = State(entry.black ^ {changed}, entry.position, entry.heading)

        self.assertFalse(is_p104_boundary(altered, witness))

    def test_unread_exterior_does_not_change_the_next_boundary(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        decorated = State(entry.black | {(10_000, 10_000)}, entry.position, entry.heading)

        self.assertTrue(is_p104_boundary(decorated, witness))
        self.assertTrue(is_p104_boundary(advance(decorated, PERIOD), witness))

    def test_rotated_boundary_is_recognized_in_its_own_orientation(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        rotated = rotate_state(entry, 1)

        self.assertEqual(rotated.heading, Heading.NORTH)
        self.assertFalse(is_p104_boundary(rotated, witness))
        self.assertTrue(is_standard_p104_boundary(rotated, witness))
