"""A compact, independently derived witness for the blank P104 highway.

The witness is deliberately computed from the reference dynamics rather than
stored as a copied table.  Its finite obligations are small: after the blank
trajectory's entry state, a period reads forty squares; the same relative
requirements recur one period later after a fixed translation.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import Heading, Point, State, advance, step
from .symmetry import rotate_point

ENTRY_UPDATES = 9_977
PERIOD = 104
DISPLACEMENT: Point = (-2, -2)


@dataclass(frozen=True, slots=True)
class P104Witness:
    """The finite local data needed to recognize one oriented highway boundary."""

    heading: Heading
    requirements: tuple[tuple[Point, bool], ...]


def _relative(point: Point, origin: Point) -> Point:
    return (point[0] - origin[0], point[1] - origin[1])


def _requirements(state: State, updates: int) -> tuple[tuple[Point, bool], ...]:
    """Recover the initial colours needed to reproduce a finite trajectory.

    A square may be read more than once.  The current read colour is corrected
    by the parity of preceding flips, yielding its colour at the boundary.
    """

    initial: dict[Point, bool] = {}
    flip_parity: dict[Point, bool] = {}
    current = state
    for _ in range(updates):
        point = current.position
        observed_black = point in current.black
        boundary_black = observed_black ^ flip_parity.get(point, False)
        old = initial.setdefault(point, boundary_black)
        if old != boundary_black:
            raise AssertionError("inconsistent boundary-colour reconstruction")
        flip_parity[point] = not flip_parity.get(point, False)
        current = step(current)
    return tuple(sorted((_relative(point, state.position), black) for point, black in initial.items()))


def _matches(state: State, witness: P104Witness) -> bool:
    """Check the local boundary requirements at the ant's current position."""

    if state.heading is not witness.heading:
        return False
    for (dx, dy), black in witness.requirements:
        if ((state.position[0] + dx, state.position[1] + dy) in state.black) != black:
            return False
    return True


def blank_p104_witness() -> P104Witness:
    """Derive and validate the P104 local recurrence from the blank orbit.

    The routine is a finite check.  It validates the entry length, period,
    displacement, heading, and all required initial colours before returning a
    witness.  Any change to the reference dynamics therefore invalidates the
    result instead of silently changing its interpretation.
    """

    entry = advance(State.blank(), ENTRY_UPDATES)
    successor = advance(entry, PERIOD)
    requirements = _requirements(entry, PERIOD)
    successor_requirements = _requirements(successor, PERIOD)
    displacement = _relative(successor.position, entry.position)
    if displacement != DISPLACEMENT:
        raise AssertionError(f"unexpected P104 displacement: {displacement}")
    if successor.heading is not entry.heading:
        raise AssertionError("P104 boundary does not preserve heading")
    if successor_requirements != requirements:
        raise AssertionError("P104 local requirements do not recur")
    witness = P104Witness(entry.heading, requirements)
    if not _matches(entry, witness) or not _matches(successor, witness):
        raise AssertionError("derived P104 witness does not recognize its boundaries")
    return witness


def is_p104_boundary(state: State, witness: P104Witness) -> bool:
    """Decide whether ``state`` has the witness's local highway boundary shape."""

    return _matches(state, witness)


def rotate_witness(witness: P104Witness, quarter_turns: int) -> P104Witness:
    """Transport a local boundary witness through a clockwise rotation."""

    return P104Witness(
        witness.heading.rotate_clockwise(quarter_turns),
        tuple(sorted((rotate_point(point, quarter_turns), black) for point, black in witness.requirements)),
    )


def is_standard_p104_boundary(state: State, witness: P104Witness) -> bool:
    """Recognize any of the four rotated forms of the derived P104 boundary."""

    return any(_matches(state, rotate_witness(witness, turns)) for turns in range(4))


def first_future_read_period(point: Point, anchor: Point, witness: P104Witness) -> int | None:
    """Return the first P104 period in which the oriented blank highway reads ``point``.

    ``anchor`` is the ant location at a matching oriented boundary. The answer
    follows from the finite footprint and the fixed displacement, so no long
    trajectory is searched.
    """

    relative = _relative(point, anchor)
    candidates: list[int] = []
    for offset, _ in witness.requirements:
        x_gap = offset[0] - relative[0]
        y_gap = offset[1] - relative[1]
        if x_gap < 0 or y_gap < 0 or x_gap != y_gap or x_gap % 2:
            continue
        candidates.append(x_gap // 2)
    return min(candidates) if candidates else None


def future_read_lane_heads(witness: P104Witness) -> tuple[Point, ...]:
    """Return the minimal non-overlapping ray cover of the future read footprint.

    Offsets differing by a non-negative multiple of the period displacement
    generate the same future ray. The head with the greatest first coordinate
    covers the rest of that ray.
    """

    heads: dict[tuple[int, int], Point] = {}
    for offset, _ in witness.requirements:
        key = (offset[0] - offset[1], offset[0] % 2)
        old = heads.get(key)
        if old is None or offset[0] > old[0]:
            heads[key] = offset
    return tuple(sorted(heads.values()))
