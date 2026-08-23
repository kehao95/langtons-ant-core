"""Exact, dependency-free dynamics for the classical two-colour Langton ant."""

from .highway import (
    P104Witness,
    blank_p104_witness,
    first_future_read_period,
    future_read_lane_heads,
    is_p104_boundary,
    is_p104_terminal,
    p104_period_successor,
    p104_terminal_successor,
    is_standard_p104_boundary,
    is_standard_p104_terminal,
    rotate_witness,
)
from .coupling import (
    FirstRead,
    blank_entry_prefix_domain,
    blank_entry_prefix_schedule,
    first_reads,
    toggle_square,
    unreached_perturbation_reduces_to_entry,
    visited_squares,
)
from .model import Heading, Point, State, advance, step
from .lanes import LaneContact, lane_contact, p104_boundary_after
from .one_black import CANONICAL_ENTRY_UPDATES, canonical_one_black_entry, canonical_one_black_initial
from .obstacles import add_unread_obstacle, is_permanently_unread_entry_obstacle
from .symmetry import rotate_point, rotate_state, translate_point, translate_state
from .traces import terminal_trace_endpoint

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
    "is_p104_terminal",
    "p104_period_successor",
    "p104_terminal_successor",
    "is_standard_p104_boundary",
    "is_standard_p104_terminal",
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
    "blank_entry_prefix_schedule",
    "FirstRead",
    "first_reads",
    "toggle_square",
    "unreached_perturbation_reduces_to_entry",
    "visited_squares",
    "LaneContact",
    "lane_contact",
    "p104_boundary_after",
    "terminal_trace_endpoint",
]
