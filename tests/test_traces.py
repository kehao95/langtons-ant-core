"""Tests for the shared finite-to-terminal trace verifier."""

from __future__ import annotations

import unittest

from langtons_ant import (
    State,
    blank_p104_witness,
    canonical_one_black_initial,
    terminal_trace_endpoint,
)
from langtons_ant.one_black import CANONICAL_ENTRY_UPDATES


class TerminalTraceTests(unittest.TestCase):
    def test_canonical_one_black_trace_has_a_terminal_endpoint(self) -> None:
        endpoint = terminal_trace_endpoint(
            canonical_one_black_initial(), CANONICAL_ENTRY_UPDATES, blank_p104_witness()
        )

        self.assertEqual(len(endpoint.black), 715)

    def test_a_short_trace_is_not_upgraded_to_a_terminal_claim(self) -> None:
        with self.assertRaises(AssertionError):
            terminal_trace_endpoint(State.blank(), 1, blank_p104_witness())
