"""The classical Langton-ant update, with a single before-step convention.

``State`` describes the configuration immediately before the ant reads the
square at ``position``.  A white square causes a right turn and a black square
causes a left turn.  The ant then flips that square and advances one edge in
its new heading.  The plane is the integer lattice; north increases ``y``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

Point = tuple[int, int]


class Heading(IntEnum):
    """The four compass directions, ordered clockwise."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def right(self) -> Heading:
        """Return the heading one quarter turn clockwise from this heading."""

        return Heading((int(self) + 1) % 4)

    def left(self) -> Heading:
        """Return the heading one quarter turn counter-clockwise from this heading."""

        return Heading((int(self) - 1) % 4)

    def advance(self, point: Point) -> Point:
        """Move one lattice edge from ``point`` in this heading."""

        x, y = point
        if self is Heading.NORTH:
            return (x, y + 1)
        if self is Heading.EAST:
            return (x + 1, y)
        if self is Heading.SOUTH:
            return (x, y - 1)
        return (x - 1, y)


@dataclass(frozen=True, slots=True)
class State:
    """A finite black set together with the ant's before-step location and heading."""

    black: frozenset[Point]
    position: Point
    heading: Heading

    @classmethod
    def blank(cls, position: Point = (0, 0), heading: Heading = Heading.NORTH) -> State:
        """Construct the conventional all-white initial configuration."""

        return cls(frozenset(), position, heading)


def step(state: State) -> State:
    """Apply exactly one classical Langton-ant update to ``state``.

    The returned state follows the same before-step convention as the input.
    No mutation occurs: callers can retain previous states as evidence.
    """

    occupied = state.position in state.black
    heading = state.heading.left() if occupied else state.heading.right()
    if occupied:
        black = state.black - {state.position}
    else:
        black = state.black | {state.position}
    return State(frozenset(black), heading.advance(state.position), heading)
