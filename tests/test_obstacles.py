"""Tests for the exact P104 non-contact obstacle classification."""

from __future__ import annotations

import unittest

from langtons_ant import (
    State,
    add_unread_obstacle,
    advance,
    blank_p104_witness,
    first_future_read_period,
    future_read_lane_heads,
    is_p104_boundary,
    is_permanently_unread_entry_obstacle,
)
from langtons_ant.highway import DISPLACEMENT, ENTRY_UPDATES, PERIOD


class EntryObstacleTests(unittest.TestCase):
    def test_overlapping_footprints_reduce_to_twenty_two_forward_lanes(self) -> None:
        witness = blank_p104_witness()

        self.assertEqual(len(future_read_lane_heads(witness)), 22)

    def test_future_read_period_is_solved_from_the_finite_footprint(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        offset, _ = witness.requirements[0]
        current = (entry.position[0] + offset[0], entry.position[1] + offset[1])
        next_period = (current[0] + DISPLACEMENT[0], current[1] + DISPLACEMENT[1])

        self.assertEqual(first_future_read_period(current, entry.position, witness), 0)
        self.assertEqual(first_future_read_period(next_period, entry.position, witness), 1)

    def test_off_ray_obstacle_remains_outside_the_next_boundary(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        point = (10_000, -9_999)
        decorated = add_unread_obstacle(entry, point, witness)

        self.assertTrue(is_permanently_unread_entry_obstacle(entry, point, witness))
        self.assertTrue(is_p104_boundary(decorated, witness))
        self.assertTrue(is_p104_boundary(advance(decorated, PERIOD), witness))

    def test_ray_obstacle_is_not_misreported_as_irrelevant(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        offset, _ = witness.requirements[0]
        point = (entry.position[0] + offset[0], entry.position[1] + offset[1])

        self.assertFalse(is_permanently_unread_entry_obstacle(entry, point, witness))
        with self.assertRaises(ValueError):
            add_unread_obstacle(entry, point, witness)
