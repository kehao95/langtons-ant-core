"""Exact, dependency-free dynamics for the classical two-colour Langton ant."""

from .highway import (
    P104Witness,
    blank_p104_witness,
    first_future_read_period,
    future_read_lane_heads,
    is_p104_boundary,
    is_standard_p104_boundary,
    rotate_witness,
)
from .coupling import blank_entry_prefix_domain, toggle_square, unreached_perturbation_reduces_to_entry, visited_squares
from .model import Heading, Point, State, advance, step
from .one_black import CANONICAL_ENTRY_UPDATES, canonical_one_black_entry, canonical_one_black_initial
from .obstacles import add_unread_obstacle, is_permanently_unread_entry_obstacle
from .symmetry import rotate_point, rotate_state, translate_point, translate_state

__all__ = [
    "Heading",
    "Point",
    "State",
    "advance",
    "step",
    "P104Witness",
    "blank_p104_witness",
    "first_future_read_period",
    "future_read_lane_heads",
    "is_p104_boundary",
    "is_standard_p104_boundary",
    "rotate_point",
    "rotate_state",
    "rotate_witness",
    "translate_point",
    "translate_state",
    "CANONICAL_ENTRY_UPDATES",
    "canonical_one_black_entry",
    "canonical_one_black_initial",
    "add_unread_obstacle",
    "is_permanently_unread_entry_obstacle",
    "blank_entry_prefix_domain",
    "toggle_square",
    "unreached_perturbation_reduces_to_entry",
    "visited_squares",
]
