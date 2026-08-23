"""Finite-prefix XOR coupling for a single added black square."""

from __future__ import annotations

from .highway import ENTRY_UPDATES
from .model import Point, State, advance, step


def toggle_square(state: State, point: Point) -> State:
    """Return ``state`` with exactly the colour at ``point`` reversed."""

    black = state.black ^ {point}
    return State(frozenset(black), state.position, state.heading)


def visited_squares(state: State, updates: int) -> frozenset[Point]:
    """Return the squares read during a finite prefix of the trajectory."""

    if updates < 0:
        raise ValueError("updates must be non-negative")
    visited: set[Point] = set()
    current = state
    for _ in range(updates):
        visited.add(current.position)
        current = step(current)
    return frozenset(visited)


def blank_entry_prefix_domain() -> frozenset[Point]:
    """Derive the set of squares read before the blank trajectory's P104 entry."""

    return visited_squares(State.blank(), ENTRY_UPDATES)


def unreached_perturbation_reduces_to_entry(point: Point) -> bool:
    """Check the finite-prefix coupling for a point not read by the blank prefix.

    If ``point`` is unread, both trajectories make identical choices up to the
    entry time.  The returned equality checks that finite consequence directly.
    A point inside the prefix domain is rejected rather than silently treated as
    an unchanged trajectory.
    """

    base = State.blank()
    if point in blank_entry_prefix_domain():
        raise ValueError("the perturbation is read inside the blank entry prefix")
    perturbed = toggle_square(base, point)
    return advance(perturbed, ENTRY_UPDATES) == toggle_square(advance(base, ENTRY_UPDATES), point)
