"""Tests for the finite-prefix decomposition used by arbitrary-offset research."""

from __future__ import annotations

import unittest

from langtons_ant import (
    State,
    blank_entry_prefix_domain,
    unreached_perturbation_reduces_to_entry,
    visited_squares,
)
from langtons_ant.highway import ENTRY_UPDATES


class PrefixCouplingTests(unittest.TestCase):
    def test_blank_entry_domain_is_derived_from_the_trace(self) -> None:
        domain = blank_entry_prefix_domain()

        self.assertEqual(domain, visited_squares(State.blank(), ENTRY_UPDATES))
        self.assertEqual(len(domain), 1_376)
        self.assertIn((0, 0), domain)

    def test_unread_square_has_an_exact_entry_reduction(self) -> None:
        self.assertTrue(unreached_perturbation_reduces_to_entry((10_000, -10_000)))

    def test_read_square_is_not_misclassified_as_unread(self) -> None:
        with self.assertRaises(ValueError):
            unreached_perturbation_reduces_to_entry((0, 0))
