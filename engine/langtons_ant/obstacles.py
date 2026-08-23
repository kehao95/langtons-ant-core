"""Exact non-contact classification for one added square at a P104 entry."""

from __future__ import annotations

from .coupling import toggle_square
from .highway import P104Witness, first_future_read_period, is_p104_boundary
from .model import Point, State


def is_permanently_unread_entry_obstacle(
    entry: State, point: Point, witness: P104Witness
) -> bool:
    """Recognize an extra square that lies outside every future P104 footprint.

    The result applies to the witness's orientation. A point on any translated
    104-step footprint is intentionally classified as potentially interactive.
    """

    return is_p104_boundary(entry, witness) and first_future_read_period(point, entry.position, witness) is None


def add_unread_obstacle(entry: State, point: Point, witness: P104Witness) -> State:
    """Add an obstacle only after proving it is outside all future read footprints."""

    if not is_permanently_unread_entry_obstacle(entry, point, witness):
        raise ValueError("the obstacle may be read by a future P104 period")
    return toggle_square(entry, point)
