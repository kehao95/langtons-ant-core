"""Orientation-preserving square-lattice symmetries of the classical rule."""

from __future__ import annotations

from .model import Point, State


def rotate_point(point: Point, quarter_turns: int) -> Point:
    """Rotate ``point`` about the origin clockwise by ``quarter_turns`` right angles."""

    x, y = point
    match quarter_turns % 4:
        case 0:
            return (x, y)
        case 1:
            return (y, -x)
        case 2:
            return (-x, -y)
        case _:
            return (-y, x)


def rotate_state(state: State, quarter_turns: int) -> State:
    """Rotate every geometric component of a state about the origin."""

    return State(
        frozenset(rotate_point(point, quarter_turns) for point in state.black),
        rotate_point(state.position, quarter_turns),
        state.heading.rotate_clockwise(quarter_turns),
    )


def translate_point(point: Point, displacement: Point) -> Point:
    """Translate a lattice point by an integer displacement."""

    return (point[0] + displacement[0], point[1] + displacement[1])


def translate_state(state: State, displacement: Point) -> State:
    """Translate a state without changing its heading."""

    return State(
        frozenset(translate_point(point, displacement) for point in state.black),
        translate_point(state.position, displacement),
        state.heading,
    )
