"""Finite witness and terminal predicate for the standard P104 highway."""

from __future__ import annotations

from dataclasses import dataclass

from .model import Heading, Point, State, advance, step

ENTRY_UPDATES = 9_977
PERIOD = 104
DISPLACEMENT: Point = (-2, -2)
ENVELOPE_CELLS = 1_398
PREFIX_CELLS = 1_376
PREFIX_CASE_BOUND = 110_000


@dataclass(frozen=True, slots=True)
class P104:
    heading: Heading
    requirements: tuple[tuple[Point, bool], ...]
    displacement: Point


def _relative(point: Point, origin: Point) -> Point:
    return (point[0] - origin[0], point[1] - origin[1])


def _requirements(state: State) -> tuple[tuple[Point, bool], ...]:
    initial: dict[Point, bool] = {}
    flipped: set[Point] = set()
    current = state
    for _ in range(PERIOD):
        point = current.position
        boundary_black = (point in current.black) ^ (point in flipped)
        previous = initial.setdefault(point, boundary_black)
        if previous != boundary_black:
            raise AssertionError("inconsistent P104 read requirements")
        if point in flipped:
            flipped.remove(point)
        else:
            flipped.add(point)
        current = step(current)
    return tuple(sorted((_relative(point, state.position), black) for point, black in initial.items()))


def _matches(
    black_cells: set[Point] | frozenset[Point],
    position: Point,
    heading: Heading,
    witness: P104,
) -> bool:
    return heading is witness.heading and all(
        ((position[0] + dx, position[1] + dy) in black_cells) == black
        for (dx, dy), black in witness.requirements
    )


def _rotate(point: Point, turns: int) -> Point:
    x, y = point
    match turns % 4:
        case 0:
            return (x, y)
        case 1:
            return (y, -x)
        case 2:
            return (-x, -y)
        case _:
            return (-y, x)


def _rotated(witness: P104, turns: int) -> P104:
    return P104(
        witness.heading.rotate_clockwise(turns),
        tuple(sorted((_rotate(point, turns), black) for point, black in witness.requirements)),
        _rotate(witness.displacement, turns),
    )


def _multiple(difference: Point, direction: Point) -> int | None:
    counts: list[int] = []
    for delta, stride in zip(difference, direction, strict=True):
        if stride == 0:
            if delta:
                return None
        elif delta % stride:
            return None
        else:
            counts.append(delta // stride)
    if not counts or counts[0] < 0 or any(count != counts[0] for count in counts):
        return None
    return counts[0]


def _future_period(point: Point, position: Point, witness: P104) -> int | None:
    relative = _relative(point, position)
    periods = (
        _multiple((relative[0] - offset[0], relative[1] - offset[1]), witness.displacement)
        for offset, _ in witness.requirements
    )
    candidates = [period for period in periods if period is not None]
    return min(candidates) if candidates else None


def _clear(black_cells: set[Point] | frozenset[Point], position: Point, witness: P104) -> bool:
    return all(
        (period := _future_period(point, position, witness)) is None or period == 0
        for point in black_cells
    )


def _terminal(
    black_cells: set[Point] | frozenset[Point],
    position: Point,
    heading: Heading,
    witness: P104,
) -> bool:
    return _matches(black_cells, position, heading, witness) and _clear(
        black_cells, position, witness
    )


def standard_terminal(state: State, witness: P104) -> bool:
    return any(
        _terminal(state.black, state.position, state.heading, _rotated(witness, turns))
        for turns in range(4)
    )


def _terminal_time(initial: State, witness: P104, bound: int) -> int | None:
    black = set(initial.black)
    position = initial.position
    heading = initial.heading
    orientations = tuple(_rotated(witness, turns) for turns in range(4))
    for elapsed in range(bound + 1):
        if any(_terminal(black, position, heading, oriented) for oriented in orientations):
            return elapsed
        occupied = position in black
        heading = heading.left() if occupied else heading.right()
        if occupied:
            black.remove(position)
        else:
            black.add(position)
        position = heading.advance(position)
    return None


def _blank_envelope() -> frozenset[Point]:
    state = State.blank()
    visited: set[Point] = set()
    for _ in range(ENTRY_UPDATES + PERIOD):
        visited.add(state.position)
        state = step(state)
    return frozenset(visited)


def _blank_prefix_reads() -> dict[Point, int]:
    state = State.blank()
    first: dict[Point, int] = {}
    for elapsed in range(ENTRY_UPDATES):
        first.setdefault(state.position, elapsed)
        state = step(state)
    return first


def first_blank_hit(
    targets: frozenset[Point],
    position: Point,
    heading: Heading,
    witness: P104,
) -> int | None:
    """Return the first time the blank orbit from this pose reads a target."""

    inverse = -int(heading)
    canonical = frozenset(
        _rotate((x - position[0], y - position[1]), inverse) for x, y in targets
    )
    prefix = _blank_prefix_reads()
    candidates = [prefix[point] for point in canonical if point in prefix]

    state = advance(State.blank(), ENTRY_UPDATES)
    for phase in range(PERIOD):
        for target in canonical:
            period = _multiple(
                (target[0] - state.position[0], target[1] - state.position[1]),
                witness.displacement,
            )
            if period is not None:
                candidates.append(ENTRY_UPDATES + period * PERIOD + phase)
        state = step(state)
    return min(candidates) if candidates else None


def clean_envelope_entry(state: State, witness: P104) -> bool:
    """Decide the clean-envelope sufficient condition for P104 entry."""

    turns = int(state.heading)
    envelope = {
        (state.position[0] + dx, state.position[1] + dy)
        for dx, dy in (_rotate(point, turns) for point in _blank_envelope())
    }
    return state.black.isdisjoint(envelope) and standard_terminal(
        advance(state, ENTRY_UPDATES), witness
    )


def verify_blank_highway() -> P104:
    entry = advance(State.blank(), ENTRY_UPDATES)
    successor = advance(entry, PERIOD)
    displacement = _relative(successor.position, entry.position)
    requirements = _requirements(entry)
    if displacement != DISPLACEMENT:
        raise AssertionError("wrong P104 displacement")
    if successor.heading is not entry.heading or _requirements(successor) != requirements:
        raise AssertionError("P104 local boundary does not recur")
    witness = P104(entry.heading, requirements, displacement)
    if not _clear(entry.black, entry.position, witness) or not _clear(
        successor.black, successor.position, witness
    ):
        raise AssertionError("P104 future corridor is not invariant")
    if len(_blank_envelope()) != ENVELOPE_CELLS:
        raise AssertionError("wrong blank-envelope size")
    if len(_blank_prefix_reads()) != PREFIX_CELLS:
        raise AssertionError("wrong blank-prefix domain")
    return witness


def verify_prefix_one_black(witness: P104) -> None:
    for point in _blank_prefix_reads():
        initial = State(frozenset({point}), (0, 0), Heading.NORTH)
        elapsed = _terminal_time(initial, witness, PREFIX_CASE_BOUND)
        if elapsed is None:
            raise AssertionError(f"prefix one-black case did not terminate: {point}")
