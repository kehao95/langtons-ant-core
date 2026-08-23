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
    toggles: tuple[Point, ...]
    displacement: Point


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


def _toggle_offsets(before: State, after: State) -> tuple[Point, ...]:
    return tuple(sorted(_relative(point, before.position) for point in before.black ^ after.black))


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
    toggles = _toggle_offsets(entry, successor)
    next_successor = advance(successor, PERIOD)
    displacement = _relative(successor.position, entry.position)
    if displacement != DISPLACEMENT:
        raise AssertionError(f"unexpected P104 displacement: {displacement}")
    if successor.heading is not entry.heading:
        raise AssertionError("P104 boundary does not preserve heading")
    if successor_requirements != requirements:
        raise AssertionError("P104 local requirements do not recur")
    if _toggle_offsets(successor, next_successor) != toggles:
        raise AssertionError("P104 toggle mask does not recur")
    witness = P104Witness(entry.heading, requirements, toggles, DISPLACEMENT)
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
        tuple(sorted(rotate_point(point, quarter_turns) for point in witness.toggles)),
        rotate_point(witness.displacement, quarter_turns),
    )


def is_standard_p104_boundary(state: State, witness: P104Witness) -> bool:
    """Recognize any of the four rotated forms of the derived P104 boundary."""

    return any(_matches(state, rotate_witness(witness, turns)) for turns in range(4))


def is_standard_p104_terminal(state: State, witness: P104Witness) -> bool:
    """Recognize a clear-corridor P104 terminal state in any rotated orientation."""

    return any(is_p104_terminal(state, rotate_witness(witness, turns)) for turns in range(4))


def _nonnegative_multiple(difference: Point, direction: Point) -> int | None:
    """Solve ``difference = count * direction`` with a non-negative integer count."""

    counts: list[int] = []
    for difference_component, direction_component in zip(difference, direction, strict=True):
        if direction_component == 0:
            if difference_component:
                return None
            continue
        if difference_component % direction_component:
            return None
        counts.append(difference_component // direction_component)
    if not counts or any(count != counts[0] for count in counts) or counts[0] < 0:
        return None
    return counts[0]


def first_future_read_period(point: Point, anchor: Point, witness: P104Witness) -> int | None:
    """Return the first P104 period in which the oriented blank highway reads ``point``.

    ``anchor`` is the ant location at a matching oriented boundary. The answer
    follows from the finite footprint and the fixed displacement, so no long
    trajectory is searched.
    """

    relative = _relative(point, anchor)
    candidates: list[int] = []
    for offset, _ in witness.requirements:
        count = _nonnegative_multiple(
            (relative[0] - offset[0], relative[1] - offset[1]), witness.displacement
        )
        if count is not None:
            candidates.append(count)
    return min(candidates) if candidates else None


def future_read_lane_heads(witness: P104Witness) -> tuple[Point, ...]:
    """Return the minimal non-overlapping ray cover of the future read footprint.

    Offsets differing by a non-negative multiple of the period displacement
    generate the same future ray. The head with the greatest first coordinate
    covers the rest of that ray.
    """

    heads: list[Point] = []
    for offset, _ in witness.requirements:
        for index, head in enumerate(heads):
            offset_from_head = _nonnegative_multiple(
                (offset[0] - head[0], offset[1] - head[1]), witness.displacement
            )
            head_from_offset = _nonnegative_multiple(
                (head[0] - offset[0], head[1] - offset[1]), witness.displacement
            )
            if offset_from_head is not None:
                break
            if head_from_offset is not None:
                heads[index] = offset
                break
        else:
            heads.append(offset)
    return tuple(sorted(heads))


def p104_period_successor(state: State, witness: P104Witness) -> State:
    """Run one witness period and confirm its exact local macro description."""

    if not _matches(state, witness):
        raise ValueError("state does not satisfy the oriented P104 boundary")
    successor = advance(state, PERIOD)
    expected_black = state.black ^ {
        (state.position[0] + dx, state.position[1] + dy) for dx, dy in witness.toggles
    }
    if successor.black != expected_black:
        raise AssertionError("P104 period has an unexpected toggle mask")
    if successor.position != (
        state.position[0] + witness.displacement[0],
        state.position[1] + witness.displacement[1],
    ):
        raise AssertionError("P104 period has an unexpected displacement")
    if not _matches(successor, witness):
        raise AssertionError("P104 period does not preserve its boundary")
    return successor


def has_clear_future_corridor(state: State, witness: P104Witness) -> bool:
    """Check that no black square waits in a P104 footprint after this period."""

    return all(
        (period := first_future_read_period(point, state.position, witness)) is None or period == 0
        for point in state.black
    )


def is_p104_terminal(state: State, witness: P104Witness) -> bool:
    """Recognize an oriented P104 boundary with an unobstructed infinite future."""

    return _matches(state, witness) and has_clear_future_corridor(state, witness)


def p104_terminal_successor(state: State, witness: P104Witness) -> State:
    """Run one macro period while preserving the stronger terminal predicate."""

    if not is_p104_terminal(state, witness):
        raise ValueError("state does not satisfy the oriented P104 terminal predicate")
    successor = p104_period_successor(state, witness)
    if not is_p104_terminal(successor, witness):
        raise AssertionError("P104 terminal predicate was not preserved")
    return successor
