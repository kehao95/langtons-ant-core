"""Exact classical Langton-ant update used by the one-black proof."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

Point = tuple[int, int]


class Heading(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def right(self) -> Heading:
        return Heading((self + 1) % 4)

    def left(self) -> Heading:
        return Heading((self - 1) % 4)

    def advance(self, point: Point) -> Point:
        x, y = point
        if self is Heading.NORTH:
            return (x, y + 1)
        if self is Heading.EAST:
            return (x + 1, y)
        if self is Heading.SOUTH:
            return (x, y - 1)
        return (x - 1, y)

    def rotate_clockwise(self, turns: int) -> Heading:
        return Heading((self + turns) % 4)


@dataclass(frozen=True, slots=True)
class State:
    """Configuration immediately before the ant reads its current square."""

    black: frozenset[Point]
    position: Point
    heading: Heading

    @classmethod
    def blank(cls) -> State:
        return cls(frozenset(), (0, 0), Heading.NORTH)


def step(state: State) -> State:
    black = state.position in state.black
    heading = state.heading.left() if black else state.heading.right()
    cells = state.black - {state.position} if black else state.black | {state.position}
    return State(cells, heading.advance(state.position), heading)


def advance(state: State, updates: int) -> State:
    for _ in range(updates):
        state = step(state)
    return state
