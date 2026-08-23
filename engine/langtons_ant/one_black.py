"""Clean-room finite obligations for one obstacle at a pristine P104 boundary."""

from .highway import (
    ENTRY_UPDATES,
    PERIOD,
    PREFIX_CASE_BOUND,
    P104,
    _rotated,
    _terminal,
    _terminal_time,
)
from .model import Point, State, advance

LANES = 22
ACTIVE_WHITE = 27
INDUCTION_DEPTH = 20


def _factor(difference: Point, direction: Point) -> int | None:
    values: list[int] = []
    for delta, stride in zip(difference, direction, strict=True):
        if stride == 0:
            if delta:
                return None
        elif delta % stride:
            return None
        else:
            values.append(delta // stride)
    return values[0] if values and all(value == values[0] for value in values) else None


def _shift(point: Point, displacement: Point, scale: int = 1) -> Point:
    return (point[0] + scale * displacement[0], point[1] + scale * displacement[1])


def _shifted(points: set[Point] | frozenset[Point], displacement: Point) -> set[Point]:
    return {_shift(point, displacement) for point in points}


def _on_ray(point: Point, start: Point, direction: Point) -> bool:
    factor = _factor((point[0] - start[0], point[1] - start[1]), direction)
    return factor is not None and factor >= 0


def _rays_meet(a: Point, da: Point, b: Point, db: Point) -> bool:
    determinant = da[0] * db[1] - da[1] * db[0]
    delta = (b[0] - a[0], b[1] - a[1])
    if determinant:
        m_numerator = delta[0] * db[1] - delta[1] * db[0]
        n_numerator = delta[0] * da[1] - delta[1] * da[0]
        return (
            m_numerator % determinant == 0
            and n_numerator % determinant == 0
            and m_numerator // determinant >= 0
            and n_numerator // determinant >= 0
        )
    factor = _factor(delta, da)
    if factor is None:
        return False
    if da == db:
        return True
    if da == (-db[0], -db[1]):
        return factor >= 0
    raise AssertionError("unexpected parallel P104 drifts")


def _corridor_depth(
    point: Point, boundary: Point, offset: Point, forward: Point, terminal: Point
) -> int | None | bool:
    """Return the largest bad forward depth, False for none, True for infinite."""

    delta = (
        point[0] - boundary[0] - offset[0],
        point[1] - boundary[1] - offset[1],
    )
    determinant = forward[0] * terminal[1] - forward[1] * terminal[0]
    if determinant:
        n_numerator = delta[0] * terminal[1] - delta[1] * terminal[0]
        j_numerator = forward[0] * delta[1] - forward[1] * delta[0]
        if n_numerator % determinant or j_numerator % determinant:
            return False
        n = n_numerator // determinant
        j = j_numerator // determinant
        return n if n >= 0 and j >= 0 else False
    factor = _factor(delta, forward)
    if factor is None:
        return False
    if terminal == forward:
        return factor if factor >= 0 else False
    if terminal == (-forward[0], -forward[1]):
        return True
    raise AssertionError("unexpected parallel P104 drifts")


def _run(initial: State, updates: int) -> tuple[State, frozenset[Point]]:
    black = set(initial.black)
    position = initial.position
    heading = initial.heading
    reads: set[Point] = set()
    for _ in range(updates):
        reads.add(position)
        occupied = position in black
        heading = heading.left() if occupied else heading.right()
        if occupied:
            black.remove(position)
        else:
            black.add(position)
        position = heading.advance(position)
    return State(frozenset(black), position, heading), frozenset(reads)


def _first_read(initial: State, targets: frozenset[Point], bound: int) -> tuple[int, State]:
    state = initial
    for elapsed in range(bound + 1):
        if state.position in targets:
            return elapsed, state
        black = state.position in state.black
        heading = state.heading.left() if black else state.heading.right()
        cells = (
            state.black - {state.position}
            if black
            else state.black | {state.position}
        )
        state = State(cells, heading.advance(state.position), heading)
    raise AssertionError("declared historical set is not read")


def _same_trace(left: State, right: State, updates: int) -> tuple[State, State, frozenset[Point]]:
    reads: set[Point] = set()
    for _ in range(updates):
        if left.position != right.position or left.heading is not right.heading:
            raise AssertionError("post-hit poses diverge")
        reads.add(left.position)
        left_black = left.position in left.black
        right_black = right.position in right.black
        if left_black != right_black:
            raise AssertionError("post-hit read colours diverge")
        heading = left.heading.left() if left_black else left.heading.right()
        left_cells = (
            left.black - {left.position}
            if left_black
            else left.black | {left.position}
        )
        right_cells = (
            right.black - {right.position}
            if right_black
            else right.black | {right.position}
        )
        position = heading.advance(left.position)
        left = State(left_cells, position, heading)
        right = State(right_cells, position, heading)
    return left, right, frozenset(reads)


def _corridor_hit(
    boundary: State, targets: frozenset[Point], oriented: P104
) -> tuple[int, Point]:
    candidates: list[tuple[int, Point]] = []
    state = boundary
    for phase in range(PERIOD):
        for target in targets:
            cycle = _factor(
                (target[0] - state.position[0], target[1] - state.position[1]),
                oriented.displacement,
            )
            if cycle is not None and cycle >= 0:
                candidates.append((cycle * PERIOD + phase, target))
        state, _ = _run(state, 1)
    if not candidates:
        raise AssertionError("reverse P104 corridor does not meet history")
    return min(candidates)


def _lane_heads(support: frozenset[Point], drift: Point) -> tuple[Point, ...]:
    heads = []
    for point in support:
        if not any(
            (factor := _factor((point[0] - other[0], point[1] - other[1]), drift))
            is not None
            and factor < 0
            for other in support
        ):
            heads.append(point)
    return tuple(sorted(heads))


def _orientation(state: State, witness: P104) -> P104:
    for turns in range(4):
        oriented = _rotated(witness, turns)
        if _terminal(state.black, state.position, state.heading, oriented):
            return oriented
    raise AssertionError("declared endpoint is not terminal")


def verify_pristine_one_obstacle(witness: P104) -> None:
    entry = advance(State.blank(), ENTRY_UPDATES)
    origin = entry.position
    support = frozenset(_shift(origin, point) for point, _ in witness.requirements)
    pattern = frozenset(
        _shift(origin, point) for point, black in witness.requirements if black
    )
    heads = _lane_heads(frozenset(point for point, _ in witness.requirements), witness.displacement)
    if len(heads) != LANES or len(support - pattern) != ACTIVE_WHITE:
        raise AssertionError("wrong pristine obstacle partition")

    for point in support - pattern:
        elapsed = _terminal_time(State(pattern | {point}, origin, witness.heading), witness, PREFIX_CASE_BOUND)
        if elapsed is None:
            raise AssertionError(f"active-white obstacle did not terminate: {point}")

    clean_end, _ = _run(State(pattern, origin, witness.heading), PERIOD)
    shifted_pattern = _shifted(pattern, witness.displacement)
    wake = clean_end.black ^ shifted_pattern

    for relative_head in heads:
        head = _shift(origin, relative_head)
        base: State | None = None
        base_time: int | None = None
        for depth in range(1, INDUCTION_DEPTH + 1):
            obstacle = _shift(head, witness.displacement, depth)
            initial = State(pattern | {obstacle}, origin, witness.heading)
            elapsed = _terminal_time(initial, witness, PREFIX_CASE_BOUND)
            if elapsed is None:
                raise AssertionError(f"lane obstacle did not terminate: {relative_head}, {depth}")
            if depth == INDUCTION_DEPTH:
                base, base_time = initial, elapsed

        if base is None or base_time is None:
            raise AssertionError("missing induction base")
        terminal, reads = _run(base, base_time)
        oriented = _orientation(terminal, witness)

        next_obstacle = _shift(head, witness.displacement, INDUCTION_DEPTH + 1)
        after_clean, _ = _run(
            State(pattern | {next_obstacle}, origin, witness.heading), PERIOD
        )
        expected = _shifted(set(base.black), witness.displacement) ^ wake
        if (
            after_clean.black != expected
            or after_clean.position != _shift(base.position, witness.displacement)
            or after_clean.heading is not base.heading
        ):
            raise AssertionError("clean-period lane recurrence failed")

        for cell in wake:
            for footprint in support:
                factor = _factor(
                    (cell[0] - footprint[0], cell[1] - footprint[1]),
                    witness.displacement,
                )
                if factor is not None and factor > 0:
                    raise AssertionError("clean wake enters a later clean block")

            backward_start = _shift(cell, witness.displacement, -1)
            if any(_on_ray(read, backward_start, (-witness.displacement[0], -witness.displacement[1])) for read in reads):
                raise AssertionError("accumulated wake enters the translated scattering trace")

            for offset, _ in oriented.requirements:
                corridor = _shift(terminal.position, offset)
                if _rays_meet(
                    backward_start,
                    (-witness.displacement[0], -witness.displacement[1]),
                    corridor,
                    oriented.displacement,
                ):
                    raise AssertionError("accumulated wake enters the terminal corridor")

def verify_actual_entry_ordinary(witness: P104) -> None:
    entry = advance(State.blank(), ENTRY_UPDATES)
    origin = entry.position
    support = frozenset(_shift(origin, point) for point, _ in witness.requirements)
    pattern = frozenset(
        _shift(origin, point) for point, black in witness.requirements if black
    )
    history = entry.black - pattern
    if len(entry.black) != 715 or len(history) != 702:
        raise AssertionError("wrong actual blank-entry history")

    for point in support - pattern:
        elapsed = _terminal_time(
            State(entry.black | {point}, origin, witness.heading), witness, PREFIX_CASE_BOUND
        )
        if elapsed is None:
            raise AssertionError(f"historical active-white case did not terminate: {point}")

    heads = _lane_heads(
        frozenset(point for point, _ in witness.requirements), witness.displacement
    )
    ordinary = 0
    exceptional: list[Point] = []
    for relative_head in heads:
        head = _shift(origin, relative_head)
        base_obstacle = _shift(head, witness.displacement, INDUCTION_DEPTH)
        base = State(pattern | {base_obstacle}, origin, witness.heading)
        base_time = _terminal_time(base, witness, PREFIX_CASE_BOUND)
        if base_time is None:
            raise AssertionError("missing pristine historical reduction base")
        terminal, reads = _run(base, base_time)
        oriented = _orientation(terminal, witness)

        largest_bad = -1
        infinite = False
        for old in history:
            for read in reads:
                factor = _factor(
                    (old[0] - read[0], old[1] - read[1]), witness.displacement
                )
                if factor is not None and factor >= 0:
                    largest_bad = max(largest_bad, factor)
            for offset, _ in oriented.requirements:
                bad = _corridor_depth(
                    old,
                    terminal.position,
                    offset,
                    witness.displacement,
                    oriented.displacement,
                )
                if bad is True:
                    infinite = True
                elif bad is not False:
                    largest_bad = max(largest_bad, bad)

        if infinite:
            exceptional.append(relative_head)
            continue

        stable_depth = INDUCTION_DEPTH + largest_bad + 1
        stable_time: int | None = None
        for depth in range(1, stable_depth + 1):
            obstacle = _shift(head, witness.displacement, depth)
            elapsed = _terminal_time(
                State(entry.black | {obstacle}, origin, witness.heading),
                witness,
                PREFIX_CASE_BOUND,
            )
            if elapsed is None:
                raise AssertionError(
                    f"ordinary historical lane did not terminate: {relative_head}, {depth}"
                )
            stable_time = elapsed

        expected = base_time + (stable_depth - INDUCTION_DEPTH) * PERIOD
        if stable_time != expected:
            raise AssertionError("historical lane does not reduce to pristine translation")
        ordinary += 1

    if ordinary != 21 or exceptional != [(-2, -8)]:
        raise AssertionError("historical lanes do not split 21+1")


def verify_phase72(witness: P104) -> None:
    entry = advance(State.blank(), ENTRY_UPDATES)
    origin = entry.position
    pattern = frozenset(
        _shift(origin, point) for point, black in witness.requirements if black
    )
    history = entry.black - pattern
    head = _shift(origin, (-2, -8))

    base_obstacle = _shift(head, witness.displacement, INDUCTION_DEPTH)
    pristine = State(pattern | {base_obstacle}, origin, witness.heading)
    local_base = _terminal_time(pristine, witness, PREFIX_CASE_BOUND)
    if local_base is None:
        raise AssertionError("phase-72 pristine base is missing")
    _, pristine_reads = _run(pristine, local_base)
    for old in history:
        for read in pristine_reads:
            factor = _factor(
                (old[0] - read[0], old[1] - read[1]), witness.displacement
            )
            if factor is not None and factor >= 0:
                raise AssertionError("history enters a deep phase-72 scattering trace")

    hits: list[State] = []
    hit_elapsed: list[int] = []
    analytic_hit: tuple[int, Point] | None = None
    for depth in range(INDUCTION_DEPTH, INDUCTION_DEPTH + 3):
        obstacle = _shift(head, witness.displacement, depth)
        initial = State(entry.black | {obstacle}, origin, witness.heading)
        local_updates = local_base + (depth - INDUCTION_DEPTH) * PERIOD
        local, _ = _run(initial, local_updates)
        clean_local = State(local.black ^ history, local.position, local.heading)
        reverse = _orientation(clean_local, witness)
        if reverse.displacement != (-witness.displacement[0], -witness.displacement[1]):
            raise AssertionError("phase-72 local output is not the reverse highway")
        predicted = _corridor_hit(clean_local, history, reverse)
        if analytic_hit is None:
            analytic_hit = predicted
        elif (
            predicted[0] != analytic_hit[0] + (depth - INDUCTION_DEPTH) * PERIOD
            or predicted[1] != analytic_hit[1]
        ):
            raise AssertionError("phase-72 exact corridor hit is not affine")
        elapsed, hit = _first_read(local, history, 10_000)
        if (elapsed, hit.position) != predicted:
            raise AssertionError("phase-72 replay disagrees with exact corridor index")
        hits.append(hit)
        hit_elapsed.append(elapsed)

    if not (
        hits[0].position == hits[1].position == hits[2].position
        and hits[0].position == (20, -22)
        and hits[0].heading is hits[1].heading is hits[2].heading
        and hit_elapsed[1] == hit_elapsed[0] + PERIOD
        and hit_elapsed[2] == hit_elapsed[1] + PERIOD
    ):
        raise AssertionError("phase-72 historical hit is not affine in depth")

    layer = hits[0].black ^ hits[1].black
    next_layer = hits[1].black ^ hits[2].black
    if _shifted(set(layer), witness.displacement) != next_layer:
        raise AssertionError("phase-72 hit-state XOR layer does not translate")

    post_hit = _terminal_time(hits[0], witness, 20_000)
    if post_hit != 7_994:
        raise AssertionError("phase-72 post-hit duration changed")
    end0, end1, reads = _same_trace(hits[0], hits[1], post_hit)
    final = _orientation(end0, witness)
    if (
        end1.position != end0.position
        or end1.heading is not end0.heading
        or not _terminal(end1.black, end1.position, end1.heading, final)
    ):
        raise AssertionError("phase-72 post-hit endpoint is not stable")

    for cell in layer:
        if any(_on_ray(read, cell, witness.displacement) for read in reads):
            raise AssertionError("phase-72 variable layer enters the post-hit trace")
        for offset, _ in final.requirements:
            corridor = _shift(end0.position, offset)
            if _rays_meet(cell, witness.displacement, corridor, final.displacement):
                raise AssertionError("phase-72 variable layer enters the final corridor")

    for depth in range(1, INDUCTION_DEPTH):
        obstacle = _shift(head, witness.displacement, depth)
        elapsed = _terminal_time(
            State(entry.black | {obstacle}, origin, witness.heading),
            witness,
            PREFIX_CASE_BOUND,
        )
        if elapsed is None:
            raise AssertionError(f"shallow phase-72 case did not terminate: {depth}")
