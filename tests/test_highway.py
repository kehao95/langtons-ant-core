"""Focused finite checks for the independently derived blank P104 witness."""

from __future__ import annotations

import unittest

from langtons_ant import (
    Heading,
    State,
    advance,
    blank_p104_witness,
    is_p104_boundary,
    is_p104_terminal,
    is_standard_p104_boundary,
    p104_period_successor,
    p104_terminal_successor,
    rotate_state,
    rotate_witness,
)
from langtons_ant.highway import DISPLACEMENT, ENTRY_UPDATES, PERIOD, first_future_read_period, future_read_lane_heads


class BlankP104WitnessTests(unittest.TestCase):
    def test_blank_entry_and_successor_match_the_same_boundary(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        successor = advance(entry, PERIOD)

        self.assertEqual(len(witness.requirements), 40)
        self.assertEqual(sum(black for _, black in witness.requirements), 13)
        self.assertEqual(len(witness.toggles), 32)
        self.assertTrue(is_p104_boundary(entry, witness))
        self.assertTrue(is_p104_boundary(successor, witness))
        self.assertTrue(is_p104_terminal(entry, witness))
        self.assertTrue(is_p104_terminal(successor, witness))
        self.assertEqual(
            (successor.position[0] - entry.position[0], successor.position[1] - entry.position[1]),
            DISPLACEMENT,
        )
        self.assertEqual(p104_period_successor(entry, witness), successor)
        self.assertEqual(p104_terminal_successor(entry, witness), successor)

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
        self.assertTrue(is_p104_terminal(decorated, witness))
        self.assertEqual(p104_period_successor(decorated, witness), advance(decorated, PERIOD))

    def test_future_ray_obstacle_is_not_a_terminal_boundary(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        offset, _ = witness.requirements[0]
        delayed = (
            entry.position[0] + offset[0] + witness.displacement[0],
            entry.position[1] + offset[1] + witness.displacement[1],
        )
        contaminated = State(entry.black | {delayed}, entry.position, entry.heading)

        self.assertTrue(is_p104_boundary(contaminated, witness))
        self.assertFalse(is_p104_terminal(contaminated, witness))

    def test_rotated_boundary_is_recognized_in_its_own_orientation(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        rotated = rotate_state(entry, 1)

        self.assertEqual(rotated.heading, Heading.NORTH)
        self.assertFalse(is_p104_boundary(rotated, witness))
        self.assertTrue(is_standard_p104_boundary(rotated, witness))

    def test_rotated_witness_rotates_its_future_ray_direction(self) -> None:
        witness = blank_p104_witness()
        entry = rotate_state(advance(State.blank(), ENTRY_UPDATES), 1)
        rotated_witness = rotate_witness(witness, 1)
        offset, _ = rotated_witness.requirements[0]
        current = (entry.position[0] + offset[0], entry.position[1] + offset[1])
        next_period = (
            current[0] + rotated_witness.displacement[0],
            current[1] + rotated_witness.displacement[1],
        )

        self.assertEqual(len(future_read_lane_heads(rotated_witness)), 22)
        self.assertEqual(first_future_read_period(current, entry.position, rotated_witness), 0)
        self.assertEqual(first_future_read_period(next_period, entry.position, rotated_witness), 1)
