"""Effective four-cell exterior completion, using exact integer-vector updates."""
from __future__ import annotations

GATE = frozenset({(0, -1), (1, 1), (1, 3), (2, 2)})


def step(black, position, heading):
    """Mutate the finite black set; return the next pose and the read bit."""
    x, y = position
    dx, dy = heading
    bit = position in black
    direction = (-dy, dx) if bit else (dy, -dx)
    black.symmetric_difference_update({position})
    return (x + direction[0], y + direction[1]), direction, bit


def place(point, origin, east):
    """Quarter-turn placement whose local east direction is the vector east."""
    x, y = point
    dx, dy = east
    return origin[0] + x * dx - y * dy, origin[1] + x * dy + y * dx


def inside(point, square):
    x, y, n = square
    return x <= point[0] < x + n and y <= point[1] < y + n


def complete(black, position, heading, protected=(), prefix=0, padding=0):
    """Return four added cells and a finite exit certificate.

    The preserved object is the observed trajectory, not equality of full
    colourings. Termination uses finite-square escape. No search cap or HC
    oracle is used. Coordinates and all arithmetic are Python integers.
    """
    if heading not in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        raise ValueError('heading must be a cardinal unit vector')
    if type(prefix) is not int or type(padding) is not int or min(prefix, padding) < 0:
        raise ValueError('prefix and padding must be nonnegative integers')
    original = set(black)
    protected = set(protected)
    points = original | protected | {position}
    left = min(min(q[0] for q in points), position[0] - prefix) - padding
    bottom = min(min(q[1] for q in points), position[1] - prefix) - padding
    right = max(max(q[0] for q in points), position[0] + prefix) + padding
    top = max(max(q[1] for q in points), position[1] + prefix) + padding
    square = left, bottom, max(right - left, top - bottom) + 1
    board, p, h, elapsed = set(original), position, heading, 0
    while inside(p, square):
        p, h, _ = step(board, p, h)
        elapsed += 1
    added = {place(q, p, h) for q in GATE}
    return added, {'square': square, 'exit_time': elapsed,
                   'exit_position': p, 'exit_heading': h, 'exit_black': board}
