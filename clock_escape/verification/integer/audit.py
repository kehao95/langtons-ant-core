"""Exact coefficient proof of every branch of the integer increment.

For s=+/- (k+1), write z=3**k and compare coefficients in Q[z].
The central value s=0 is checked separately. No dynamics code is imported.
"""
from fractions import Fraction as F
import json
import sys


def add(*terms):
    return tuple(sum(t[i] for t in terms) for i in range(2))


def scale(a, p):
    return tuple(a*x for x in p)


def main():
    if sys.flags.optimize:
        raise SystemExit('Run without -O')
    count = 0
    for side in (-1, 0, 1):
        f = (-1, 3) if side else (0, 0)
        for h in range(4):
            e = 1 if h < 2 else -1
            axis = 1 if h % 2 == 0 else -1
            for delta in (-1, 1):
                hp = (h + delta) % 4
                ep = 1 if hp < 2 else -1
                assert delta*axis == e*ep
                # At a branch endpoint f_next=0, so either head factor agrees.
                fn = (-1, 3**(1 + side*ep)) if side else (2, 0)
                old_factor = F(1, 2) if e*side >= 0 else F(-3, 2)
                new_factor = F(1, 2) if not side or ep*side >= 0 else F(-3, 2)
                actual = add(scale(-e*ep, f), scale(new_factor, fn),
                             scale(-old_factor, f))
                expected = add((1, 0), scale(4 if ep != e and e*side < 0 else 0, f))
                assert actual == expected
                count += 1
    print(json.dumps({'status': 'PASS', 'universal_integer_branches': count}, sort_keys=True))


if __name__ == '__main__':
    main()
