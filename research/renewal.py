"""Lossless complete-history renewal for finite Langton states."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from one_black.langtons_ant.highway import PERIOD, P104, first_blank_hit, standard_terminal
from one_black.langtons_ant.model import Point, State, step


def escape_bound(cell_count: int) -> int:
    """Number of states available while the ant stays in fixed finite cells."""

    if type(cell_count) is not int or cell_count < 0:
        raise ValueError("cell_count must be a non-negative integer")
    return 4 * cell_count * (1 << cell_count)


@dataclass(frozen=True, slots=True)
class Carrier:
    """A physical state at a cell outside its complete finite read history."""

    state: State
    old: frozenset[Point]
    time: int = 0

    def __post_init__(self) -> None:
        if type(self.time) is not int or self.time < 0:
            raise ValueError("time must be a non-negative integer")
        if not self.state.black <= self.old:
            raise ValueError("old must contain the complete black support")
        if self.state.position in self.old:
            raise ValueError("a carrier must be at a fresh cell")


Kind = Literal["renewed", "terminal", "blank-coupled"]


@dataclass(frozen=True, slots=True)
class Event:
    """One exact renewal edge or one proof-producing halt."""

    kind: Kind
    source: Carrier
    target: Carrier | None
    divergence: Point | None
    footprint: frozenset[Point]


def _first_fresh(
    state: State,
    old: set[Point],
    time: int,
    footprint: set[Point] | None = None,
) -> Carrier:
    if not state.black <= old:
        raise ValueError("old must contain the complete black support")
    if state.position not in old:
        return Carrier(state, frozenset(old), time)

    # While no exit has occurred, every read lies in the unchanged set old.
    # A longer confined run would repeat one of its 4*n*2^n finite states,
    # hence be periodic, contradicting the unbounded-trajectory theorem.
    for _ in range(escape_bound(len(old))):
        if footprint is not None:
            footprint.add(state.position)
        state = step(state)
        time += 1
        if state.position not in old:
            return Carrier(state, frozenset(old), time)
    raise AssertionError("finite confinement would contradict unboundedness")


def initial_carrier(state: State) -> Carrier:
    """Compute the first fresh checkpoint of a finite-support seed."""

    return _first_fresh(state, set(state.black), 0)


def _on_highway(state: State, witness: P104) -> bool:
    for _ in range(PERIOD):
        if standard_terminal(state, witness):
            return True
        state = step(state)
    return False


def renew(source: Carrier, witness: P104) -> Event:
    """Compute the next complete-history checkpoint, or certify P104 entry."""

    if _on_highway(source.state, witness):
        return Event("terminal", source, None, None, frozenset())

    # Until the first read of source.black, the actual orbit is exactly the
    # blank orbit launched from the same fresh pose.
    hit = first_blank_hit(
        source.state.black,
        source.state.position,
        source.state.heading,
        witness,
    )
    if hit is None:
        return Event("blank-coupled", source, None, None, frozenset())

    state = source.state
    old = set(source.old)
    footprint: set[Point] = set()
    for _ in range(hit):
        footprint.add(state.position)
        old.add(state.position)
        state = step(state)

    divergence = state.position
    if divergence not in state.black:
        raise AssertionError("blank interaction oracle disagrees with replay")
    footprint.add(divergence)
    old.add(divergence)
    state = step(state)

    target = _first_fresh(state, old, source.time + hit + 1, footprint)
    return Event(
        "renewed",
        source,
        target,
        divergence,
        frozenset(footprint),
    )
