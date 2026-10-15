"""Independent Laurent-coefficient audit of both directional clock families.

Normalize the current weight to one and clear (a+1)(b+1).
Integer exponent pairs represent Laurent monomials in a,b, so no samples
or symbolic algebra dependency are needed. No wake implementation is imported.
"""
from collections import defaultdict
import json
import sys


def add(*polynomials):
    result = defaultdict(int)
    for p in polynomials:
        for exponent, coefficient in p.items():
            result[exponent] += coefficient
    return {e: c for e, c in result.items() if c}


def scale(c, p):
    return {e: c*v for e, v in p.items() if c*v}


def shift(p, displacement):
    x, y = displacement
    return {(a+x, b+y): c for (a, b), c in p.items()}


def main():
    if sys.flags.optimize:
        raise SystemExit('Run without -O')
    moves = ((0, 1), (1, 0), (0, -1), (-1, 0))
    denom = {(1, 1): 1, (1, 0): 1, (0, 1): 1, (0, 0): 1}
    kappa = {(1, 1): 1, (1, 0): -1, (0, 1): -1, (0, 0): -3}
    gamma = ({(1, 0): 2, (0, 0): 2}, {(0, 1): 2, (0, 0): 2},
             {(1, 1): -2, (0, 1): -2}, {(1, 1): -2, (1, 0): -2})
    count = 0
    for inverse in (False, True):
        for h in range(4):
            axis = 1 if h % 2 == 0 else -1
            for delta in (-1, 1):
                hp = (h + delta) % 4
                index = (h + 2) % 4 if inverse else h
                next_index = (hp + 2) % 4 if inverse else hp
                move = tuple(-x for x in moves[hp]) if inverse else moves[hp]
                actual = add(scale(-axis*delta, denom), shift(gamma[next_index], move),
                             scale(-1, gamma[index]))
                extra = (index == 2 and delta == -1) or (index == 3 and delta == 1)
                expected = add(kappa, scale(4 if extra else 0, denom))
                assert actual == expected
                count += 1
    print(json.dumps({'status': 'PASS', 'universal_directional_identities': count}, sort_keys=True))


if __name__ == '__main__':
    main()
