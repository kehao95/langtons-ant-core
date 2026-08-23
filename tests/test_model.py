"""Examples that pin down the reference model's orientation and update order."""

from __future__ import annotations

import unittest

from langtons_ant import Heading, State, step


class ClassicalStepTests(unittest.TestCase):
    def test_blank_origin_turns_right_flips_then_moves(self) -> None:
        after = step(State.blank())

        self.assertEqual(after.heading, Heading.EAST)
        self.assertEqual(after.black, frozenset({(0, 0)}))
        self.assertEqual(after.position, (1, 0))

    def test_second_blank_square_uses_the_new_heading(self) -> None:
        after = step(step(State.blank()))

        self.assertEqual(after.heading, Heading.SOUTH)
        self.assertEqual(after.black, frozenset({(0, 0), (1, 0)}))
        self.assertEqual(after.position, (1, -1))

    def test_black_square_turns_left_and_becomes_white(self) -> None:
        before = State(frozenset({(0, 0)}), (0, 0), Heading.NORTH)
        after = step(before)

        self.assertEqual(after.heading, Heading.WEST)
        self.assertEqual(after.black, frozenset())
        self.assertEqual(after.position, (-1, 0))
        self.assertEqual(before.black, frozenset({(0, 0)}))


if __name__ == "__main__":
    unittest.main()
