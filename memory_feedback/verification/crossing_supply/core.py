"""Request-only capacity bounds for complete blank-half-plane histories.

Counts bound request codes, not the number of physically realizable records.
No procedure decides an arbitrary half-plane return or proves all-input HC.
"""
from __future__ import annotations


def natural(*values: int) -> None:
    if any(type(v) is not int or v < 0 for v in values):
        raise ValueError('nonnegative integers required')


def geometric_sum(base: int, terms: int) -> int:
    natural(base, terms)
    if base == 0:
        return int(terms > 0)
    if base == 1:
        return terms
    return (base ** terms - 1) // (base - 1)


def request_count(height: int, pairs: int) -> int:
    """Upper capacity of records of length 2*pairs+1 and height span <=height.

    For positive height, each code has pairs+1 even-parity entries, normalized
    at its minimum and divided by two. Some codes have no admissible response.
    """
    natural(height, pairs)
    if height == 0:
        return int(pairs == 0)
    q = height // 2 + 1
    return q ** (pairs + 1) - (q - 1) ** (pairs + 1)


def request_capacity(height: int, max_pairs: int) -> int:
    natural(height, max_pairs)
    if height == 0:
        return 1
    q = height // 2 + 1
    return q * geometric_sum(q, max_pairs + 1) - (q - 1) * geometric_sum(q - 1, max_pairs + 1)


def request_packing(height: int, number: int) -> int | None:
    """Exact minimum total length in the UPPER request-code multiset.

    None means there are not enough codes at height zero. This is not itself
    a dynamical nonexistence answer without the blank-side/prefix premises.
    """
    natural(height, number)
    if number == 0:
        return 0
    if height == 0:
        return 1 if number == 1 else None
    if height == 1:
        return number * number
    used = cost = pairs = 0
    while used < number:
        take = min(number - used, request_count(height, pairs))
        cost += take * (2 * pairs + 1)
        used += take
        pairs += 1
    return cost


def incoming_key(record) -> tuple[int, ...]:
    """record entries are (time, direction +/-1, height), ending eastward.

    A key is a lossless code ONLY for genuine initially-blank-side histories.
    Equality is not a proof when the records are invented or initial debris is
    omitted. Actual full-state certificate verification is a separate step.
    """
    if not record or len(record) % 2 != 1:
        raise ValueError('nonempty odd record required')
    for i, (time, direction, height) in enumerate(record):
        if any(type(value) is not int for value in (time, direction, height)):
            raise ValueError('integer crossing entries required')
        if direction != (1 if i % 2 == 0 else -1):
            raise ValueError('record must alternate east/west and end east')
    ys = [entry[2] for entry in record[::2]]
    low = min(ys)
    if any((y - low) % 2 for y in ys):
        raise ValueError('incoming rows must share parity')
    return tuple((y - low) // 2 for y in ys)


def reconstruct_right(record, cut: int, end_time: int, cap: int = 1_000_000):
    """Check a claimed finite record using only its INCOMING requests.

    Starts with the complete white half-plane x>cut. Each completed right
    episode is simulated until its first left exit; the claimed exit is checked.
    The final partial episode is stopped at end_time. Time caps raise, never
    certify a nonreturn. No colour is reset between episodes. Returns the full
    final inside black set and actual local update count.
    """
    incoming_key(record)
    if type(cut) is not int or type(end_time) is not int or type(cap) is not int or cap < 0:
        raise ValueError('integer cut/time and nonnegative cap required')
    if any(type(t) is not int for t, _, _ in record):
        raise ValueError('integer crossing times required')
    if not (0 < record[0][0] <= record[-1][0] <= end_time):
        raise ValueError('bad chronological range')
    if any(a[0] >= b[0] for a, b in zip(record, record[1:])):
        raise ValueError('crossings must be strictly time ordered')
    black = set()
    work = 0
    for index in range(0, len(record), 2):
        time, _, y = record[index]
        x, dx, dy = cut + 1, 1, 0
        duration = (record[index + 1][0] - time if index + 1 < len(record)
                    else end_time - time)
        for step in range(duration):
            if work >= cap:
                raise RuntimeError('UNKNOWN: finite replay cap reached')
            if x <= cut:
                raise ValueError('claimed exit is later than actual first exit')
            point = x, y
            bit = point in black
            if bit:
                black.remove(point)
                dx, dy = -dy, dx
            else:
                black.add(point)
                dx, dy = dy, -dx
            x += dx
            y += dy
            work += 1
        if index + 1 < len(record):
            _, _, exit_y = record[index + 1]
            if (x, y, dx, dy) != (cut, exit_y, -1, 0):
                raise ValueError('claimed exit differs from complete inside dynamics')
        elif x <= cut:
            raise ValueError('final partial episode has already exited')
    return black, (x, y), (dx, dy), work
