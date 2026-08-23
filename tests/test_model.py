"""Examples that pin down the reference model's orientation and update order."""

from __future__ import annotations

import unittest

from langtons_ant import Heading, State, advance, rotate_state, step, translate_state


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

    def test_advance_rejects_negative_lengths(self) -> None:
        with self.assertRaises(ValueError):
            advance(State.blank(), -1)

    def test_rotation_commutes_with_a_classical_update(self) -> None:
        source = State(frozenset({(-1, 2), (3, -4)}), (0, 0), Heading.NORTH)

        self.assertEqual(rotate_state(step(source), 1), step(rotate_state(source, 1)))

    def test_translation_commutes_with_a_classical_update(self) -> None:
        source = State(frozenset({(-1, 2), (3, -4)}), (0, 0), Heading.NORTH)

        self.assertEqual(translate_state(step(source), (7, -9)), step(translate_state(source, (7, -9))))


if __name__ == "__main__":
    unittest.main()
