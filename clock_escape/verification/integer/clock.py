"""Complete-state integer clock; N,E,S,W are 0,1,2,3."""
from typing import Iterable
Point = tuple[int, int]

def chi(q: Point) -> int:
    return 1 if sum(q) % 2 == 0 else -1

def integer_clock(black: Iterable[Point], position: Point, heading: int, center: int = 0) -> int:
    """A global integer clock with gain >=1 on every classical update."""
    if heading not in range(4) or type(center) is not int:
        raise ValueError('invalid heading/center')
    sig = chi(position) * (1 if heading % 2 == 0 else -1)
    s = sum(position) - center
    f = 3 ** abs(s) - 1
    eps = 1 if heading in (0, 1) else -1
    correction = f // 2 if eps * s >= 0 else -3 * (f // 2)
    return -sig * sum(chi(q) * (3 ** abs(sum(q) - center) - 1) for q in black) + correction

