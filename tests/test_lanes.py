"""Tests for the exact first-contact presentation of each future P104 lane."""

from __future__ import annotations

import unittest

from langtons_ant import State, advance, blank_p104_witness, lane_contact
from langtons_ant.highway import ENTRY_UPDATES


class LaneContactTests(unittest.TestCase):
    def test_first_lane_starts_inside_the_current_period_footprint(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        contact = lane_contact(entry, witness, lane=0, depth=0)

        self.assertEqual(contact.first_period, 0)
        self.assertIn(contact.relative_obstacle, {offset for offset, _ in witness.requirements})
        self.assertNotEqual(contact.perturbed_boundary(), contact.boundary)

    def test_deeper_contact_recomputes_its_literal_first_period(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)
        contact = lane_contact(entry, witness, lane=0, depth=12)

        self.assertLessEqual(contact.first_period, contact.requested_depth)
        self.assertIn(contact.relative_obstacle, {offset for offset, _ in witness.requirements})

    def test_invalid_lane_and_negative_depth_are_rejected(self) -> None:
        witness = blank_p104_witness()
        entry = advance(State.blank(), ENTRY_UPDATES)

        with self.assertRaises(ValueError):
            lane_contact(entry, witness, lane=22, depth=0)
        with self.assertRaises(ValueError):
            lane_contact(entry, witness, lane=0, depth=-1)
