"""Parameterization of first contacts between a P104 future and one obstacle."""

from __future__ import annotations

from dataclasses import dataclass

from .coupling import toggle_square
from .highway import (
    P104Witness,
    first_future_read_period,
    future_read_lane_heads,
    p104_period_successor,
)
from .model import Point, State


@dataclass(frozen=True, slots=True)
class LaneContact:
    """A single obstacle placed on one future read lane before its first contact."""

    lane: int
    requested_depth: int
    first_period: int
    obstacle: Point
    boundary: State
    relative_obstacle: Point

    def perturbed_boundary(self) -> State:
        """Return the exact state immediately before the obstacle is first read."""

        return toggle_square(self.boundary, self.obstacle)


def p104_boundary_after(entry: State, witness: P104Witness, periods: int) -> State:
    """Advance an oriented P104 boundary by a non-negative number of macro steps."""

    if periods < 0:
        raise ValueError("periods must be non-negative")
    current = entry
    for _ in range(periods):
        current = p104_period_successor(current, witness)
    return current


def lane_contact(entry: State, witness: P104Witness, lane: int, depth: int) -> LaneContact:
    """Construct a canonical finite presentation of a contact on one lane.

    ``depth`` selects a point on a lane head translated by the P104 drift. Its
    literal first-read period is recomputed because different footprint points
    may overlap one geometric lane.
    """

    if depth < 0:
        raise ValueError("depth must be non-negative")
    heads = future_read_lane_heads(witness)
    try:
        head = heads[lane]
    except IndexError as error:
        raise ValueError(f"lane must be between 0 and {len(heads) - 1}") from error
    obstacle = (
        entry.position[0] + head[0] + depth * witness.displacement[0],
        entry.position[1] + head[1] + depth * witness.displacement[1],
    )
    first_period = first_future_read_period(obstacle, entry.position, witness)
    if first_period is None:
        raise AssertionError("a point built from a lane head must be read")
    boundary = p104_boundary_after(entry, witness, first_period)
    relative = (obstacle[0] - boundary.position[0], obstacle[1] - boundary.position[1])
    if relative not in {offset for offset, _ in witness.requirements}:
        raise AssertionError("first-contact point is absent from the period footprint")
    return LaneContact(lane, depth, first_period, obstacle, boundary, relative)
