"""Finite witness and terminal predicate for the standard P104 highway."""

from __future__ import annotations

from dataclasses import dataclass

from .model import Heading, Point, State, advance, step

ENTRY_UPDATES = 9_977
ONE_BLACK_ENTRY_UPDATES = 9_978
PERIOD = 104
DISPLACEMENT: Point = (-2, -2)
ONE_BLACK_INITIAL = State(frozenset({(0, 0)}), (0, 0), Heading.NORTH)


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


def _matches(state: State, witness: P104) -> bool:
    return state.heading is witness.heading and all(
        ((state.position[0] + dx, state.position[1] + dy) in state.black) == black
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


def _future_period(point: Point, state: State, witness: P104) -> int | None:
    relative = _relative(point, state.position)
    periods = (
        _multiple((relative[0] - offset[0], relative[1] - offset[1]), witness.displacement)
        for offset, _ in witness.requirements
    )
    candidates = [period for period in periods if period is not None]
    return min(candidates) if candidates else None


def _clear(state: State, witness: P104) -> bool:
    return all(
        (period := _future_period(point, state, witness)) is None or period == 0
        for point in state.black
    )


def _terminal(state: State, witness: P104) -> bool:
    return _matches(state, witness) and _clear(state, witness)


def standard_terminal(state: State, witness: P104) -> bool:
    return any(_terminal(state, _rotated(witness, turns)) for turns in range(4))


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
    if not _clear(entry, witness) or not _clear(successor, witness):
        raise AssertionError("P104 future corridor is not invariant")
    return witness


def verify_one_black_under_ant(witness: P104) -> None:
    entry = advance(ONE_BLACK_INITIAL, ONE_BLACK_ENTRY_UPDATES)
    if not standard_terminal(entry, witness):
        raise AssertionError("one-black prefix does not reach P104")
