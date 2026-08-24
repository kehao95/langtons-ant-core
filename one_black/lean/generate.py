#!/usr/bin/env python3
"""Generate the finite witness times replayed by Lean."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from langtons_ant.highway import (  # noqa: E402
    ENTRY_UPDATES,
    PERIOD,
    PREFIX_CASE_BOUND,
    _blank_prefix_reads,
    _rotated,
    _terminal,
    _terminal_time,
    verify_blank_highway,
)
from langtons_ant.model import Heading, State, advance, step  # noqa: E402


def lean_nats(name: str, values: list[int]) -> str:
    rows = [", ".join(map(str, values[i : i + 12])) for i in range(0, len(values), 12)]
    body = ",\n  ".join(rows)
    return f"def {name} : List Nat := [\n  {body}\n]\n"


def lean_nat_rows(name: str, rows: list[list[int]]) -> str:
    body = ",\n  ".join("[" + ", ".join(map(str, row)) + "]" for row in rows)
    return f"def {name} : List (List Nat) := [\n  {body}\n]\n"


def stable_depth(times: list[int]) -> int:
    """First depth from which the observed terminal times translate by P104."""

    for depth in range(1, len(times) + 1):
        tail = times[depth - 1 :]
        if all(right == left + PERIOD for left, right in zip(tail, tail[1:])):
            return depth
    raise RuntimeError("no stable P104 suffix")


def terminal_time(state: State, witness: object) -> int:
    elapsed = _terminal_time(state, witness, PREFIX_CASE_BOUND)
    if elapsed is None:
        raise RuntimeError(f"no terminal witness for {state.position}")
    return elapsed


def replay(state: State, updates: int) -> tuple[State, frozenset[tuple[int, int]]]:
    reads: set[tuple[int, int]] = set()
    for _ in range(updates):
        reads.add(state.position)
        state = step(state)
    return state, frozenset(reads)


def rotate_ccw(point: tuple[int, int], turns: int) -> tuple[int, int]:
    x, y = point
    match turns % 4:
        case 0:
            return x, y
        case 1:
            return -y, x
        case 2:
            return -x, -y
        case _:
            return y, -x


def terminal_turn(state: State, witness: object) -> int:
    for turns in range(4):
        if _terminal(
            state.black,
            state.position,
            state.heading,
            _rotated(witness, turns),
        ):
            return turns
    raise RuntimeError("stable replay is not terminal")


def normalized(
    point: tuple[int, int], terminal: State, base: State, turns: int
) -> tuple[int, int]:
    px, py = rotate_ccw(point, turns)
    tx, ty = rotate_ccw(terminal.position, turns)
    return base.position[0] + px - tx, base.position[1] + py - ty


def backward(point: tuple[int, int], turns: int, copies: int) -> tuple[int, int]:
    x, y = point
    match turns:
        case 0:
            return x + 2 * copies, y + 2 * copies
        case 1:
            return x - 2 * copies, y + 2 * copies
        case 2:
            return x - 2 * copies, y - 2 * copies
        case _:
            return x + 2 * copies, y - 2 * copies


def separated(source: tuple[int, int], target: tuple[int, int]) -> bool:
    return (
        target[0] - target[1] != source[0] - source[1]
        or target[0] % 2 != source[0] % 2
        or source[0] <= target[0]
    )


def shifted_at_least(
    minimum: int, target: tuple[int, int], source: tuple[int, int]
) -> bool:
    return (
        target[0] - target[1] == source[0] - source[1]
        and (source[0] - target[0]) % 2 == 0
        and 2 * minimum <= source[0] - target[0]
    )


def rays_meet(
    turns: int, left: tuple[int, int], right: tuple[int, int]
) -> bool:
    ax, ay = left
    bx, by = right
    match turns:
        case 0:
            return ax - ay == bx - by and (bx - ax) % 2 == 0 and ax + 2 <= bx
        case 1:
            return (
                (bx + by - ax - ay) % 4 == 0
                and 0 <= bx + by - ax - ay
                and (by - bx - (ay - ax)) % 4 == 0
                and 4 <= by - bx - (ay - ax)
            )
        case 2:
            return ax - ay == bx - by and (bx - ax) % 2 == 0
        case _:
            return (
                (bx + by - ax - ay) % 4 == 0
                and 0 <= bx + by - ax - ay
                and (ay - ax - (by - bx)) % 4 == 0
                and 4 <= ay - ax - (by - bx)
            )


def history_clear(
    lag: int,
    terminal: State,
    reads: frozenset[tuple[int, int]],
    turns: int,
    history: frozenset[tuple[int, int]],
    support: list[tuple[int, int]],
    base: State,
) -> bool:
    for historical in history:
        if any(shifted_at_least(lag, historical, source) for source in reads):
            return False
        anchor = backward(normalized(historical, terminal, base, turns), turns, lag)
        if anchor in support or not all(separated(source, anchor) for source in support):
            return False
        if any(rays_meet(turns, anchor, source) for source in support):
            return False
    return True


def main() -> None:
    witness = verify_blank_highway()
    times: list[int] = []
    for point in _blank_prefix_reads():
        initial = State(frozenset({point}), (0, 0), Heading.NORTH)
        times.append(terminal_time(initial, witness))

    entry = advance(State.blank(), ENTRY_UPDATES)
    current = entry
    support: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for _ in range(PERIOD):
        if current.position not in seen:
            seen.add(current.position)
            support.append(current.position)
        current = step(current)
    pattern = frozenset(point for point in support if point in entry.black)
    active = [point for point in support if point not in pattern]
    base = State(pattern, entry.position, entry.heading)
    pristine_active = [
        terminal_time(State(pattern | {point}, base.position, base.heading), witness)
        for point in active
    ]
    actual_active = [
        terminal_time(State(entry.black | {point}, entry.position, entry.heading), witness)
        for point in active
    ]
    drift = witness.displacement
    heads = [
        point
        for point in support
        if (point[0] + drift[0], point[1] + drift[1]) not in seen
    ]
    lane_window = [
        [
            terminal_time(
                State(
                    pattern
                    | {(head[0] + depth * drift[0], head[1] + depth * drift[1])},
                    base.position,
                    base.heading,
                ),
                witness,
            )
            for depth in range(1, 21)
        ]
        for head in heads
    ]
    phase_head = (base.position[0] - 2, base.position[1] - 8)
    phase_index = heads.index(phase_head)

    pristine_depths = [stable_depth(row) for row in lane_window]
    stable_traces: list[tuple[State, frozenset[tuple[int, int]], int]] = []
    for head, depth, row in zip(heads, pristine_depths, lane_window, strict=True):
        obstacle = head[0] + depth * drift[0], head[1] + depth * drift[1]
        terminal, reads = replay(
            State(pattern | {obstacle}, base.position, base.heading),
            row[depth - 1],
        )
        stable_traces.append((terminal, reads, terminal_turn(terminal, witness)))

    history = frozenset(point for point in entry.black if point not in seen)
    actual_depths: list[int] = []
    for index, pristine_depth in enumerate(pristine_depths):
        if index == phase_index:
            # The reverse-highway block starts at the pristine anchor 11.  At
            # actual depth 15 four clean translations separate it from the
            # historical wake and start the affine collision family.
            actual_depths.append(15)
            continue
        terminal, reads, turns = stable_traces[index]
        cutoff = next(
            (
                pristine_depth + lag
                for lag in range(21)
                if history_clear(
                    lag, terminal, reads, turns, history, support, base
                )
            ),
            None,
        )
        if cutoff is None:
            raise RuntimeError(f"ordinary lane {heads[index]} has no clean entry tail")
        actual_depths.append(cutoff)

    actual_lane_times = [
        [
            terminal_time(
                State(
                    entry.black
                    | {(head[0] + depth * drift[0], head[1] + depth * drift[1])},
                    entry.position,
                    entry.heading,
                ),
                witness,
            )
            for depth in range(1, cutoff)
        ]
        for head, cutoff in zip(heads, actual_depths, strict=True)
    ]

    lane_times = [
        row[:depth] for row, depth in zip(lane_window, pristine_depths)
    ]
    prefix_source = """import OneBlack.Terminal

namespace OneBlack.FiniteData

""" + lean_nats("prefixTimes", times) + "\nend OneBlack.FiniteData\n"
    entry_source = """import OneBlack.Terminal

namespace OneBlack.FiniteData

""" + "\n".join([
        lean_nats("pristineActiveTimes", pristine_active),
        lean_nats("actualActiveTimes", actual_active),
        lean_nat_rows("pristineLaneTimes", lane_times),
        lean_nat_rows("actualLaneTimes", actual_lane_times),
    ]) + "\nend OneBlack.FiniteData\n"
    for name, source in [("PrefixData.lean", prefix_source), ("EntryData.lean", entry_source)]:
        destination = Path(__file__).parent / "OneBlack" / name
        if not destination.exists() or destination.read_text() != source:
            destination.write_text(source)


if __name__ == "__main__":
    main()
