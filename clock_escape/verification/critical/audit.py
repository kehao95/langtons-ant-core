"""Independent exact audit: Laurent identities and short-block proof cases.

No imports from the research implementation or a computer-algebra package.
Polynomials use exponent tuples (a, b, U, V) and rational coefficients.
The eight identities hold as Laurent polynomials before critical substitution.
"""
from fractions import Fraction as Q
from itertools import product
import json


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def mono(a=0, b=0, u=0, v=0, coefficient=1):
    return {(a, b, u, v): Q(coefficient)} if coefficient else {}


def add(*polys):
    out = {}
    for poly in polys:
        for key, value in poly.items():
            out[key] = out.get(key, Q(0)) + value
    return {key: value for key, value in out.items() if value}


def mul(left, right):
    out = {}
    for k, x in left.items():
        for l, y in right.items():
            key = tuple(a + b for a, b in zip(k, l))
            out[key] = out.get(key, Q(0)) + x * y
    return {key: value for key, value in out.items() if value}


def scale(poly, coefficient):
    return mul(poly, mono(coefficient=coefficient))


def shift(poly, dx, dy):
    return {(a + dx*u, b + dy*v, u, v): c for (a,b,u,v),c in poly.items()}


D = mul(add(mono(a=1), mono()), add(mono(b=1), mono()))
FIELD = mul(add(mono(u=1), mono(u=-1, coefficient=-1)),
            add(mono(v=1), mono(v=-1, coefficient=-1)))
HEAD = [
    scale(mul(mul(add(mono(a=1), mono()), add(mono(u=1), mono(u=-1))),
              add(mono(v=1), mono(b=1, v=-1, coefficient=-1))), 2),
    scale(mul(mul(add(mono(b=1), mono()), add(mono(u=1), mono(a=1,u=-1,coefficient=-1))),
              add(mono(v=1), mono(v=-1))), 2),
    scale(mul(mul(add(mono(a=1), mono()), add(mono(u=1), mono(u=-1))),
              add(mono(v=-1), mono(b=1,v=1,coefficient=-1))), 2),
    scale(mul(mul(add(mono(b=1), mono()), add(mono(u=-1), mono(a=1,u=1,coefficient=-1))),
              add(mono(v=1), mono(v=-1))), 2),
]
MOVES = ((0,1),(1,0),(0,-1),(-1,0))
SIGNS = (((1,-1),(-1,-1)), ((-1,-1),(-1,1)),
         ((-1,1),(1,1)), ((1,1),(1,-1)))


def local_identity_audit():
    residual = mul(mul(add(mono(u=1),mono(u=-1)), add(mono(v=1),mono(v=-1))),
                   add(mono(a=1,b=1),mono(a=1,coefficient=-1),
                       mono(b=1,coefficient=-1),mono(coefficient=-3)))
    for h, black in product(range(4), range(2)):
        delta = 1 - 2*black
        next_h = (h + delta) % 4
        dx, dy = MOVES[next_h]
        sx, sy = SIGNS[h][black]
        lhs = add(scale(mul(FIELD,D), -(1 if h%2 == 0 else -1)*delta),
                  shift(HEAD[next_h],dx,dy), scale(HEAD[h],-1),
                  scale(mul(mono(u=sx,v=sy),D),-4))
        require(lhs == residual, 'universal increment identity failed')
    return 8


def word_rewards(h, word, isotropic=True):
    x = y = 0
    rewards = []
    for black in word:
        sx, sy = SIGNS[h][black]
        rewards.append(mono(u=sx,v=sy,coefficient=Q(3)**(x*sx+y*sy))
                       if isotropic else mono(a=x*sx,b=y*sy,u=sx,v=sy))
        h = (h + 1 - 2*black) % 4
        dx,dy = MOVES[h]; x += dx; y += dy
    return rewards


def block_audit():
    # Opposite consecutive turns: reciprocal monomials, product 1/3.
    for h, first in product(range(4),range(2)):
        left,right = word_rewards(h,[first,1-first])
        require(mul(left,right) == mono(coefficient=Q(1,3)), 'opposite pair product')
        require(list(left.values()) == [1], 'first pair coefficient')
    # Constant four-turn words: four positive terms whose product is 1/81.
    # Four-term AM-GM gives their sum >= 4/3, hence reward >= 16/3.
    for h, black in product(range(4),range(2)):
        total = mono()
        for term in word_rewards(h,[black]*4): total = mul(total,term)
        require(total == mono(coefficient=Q(1,81)), 'constant four-block product')
    # Every remaining word contains one of the checked opposite pairs.
    require(all(len(set(w)) == 1 or any(w[i] != w[i+1] for i in range(3))
                for w in product(range(2),repeat=4)), 'four-word coverage')
    # Horizontal arrival: the first vertical exponent is v and the second -v;
    # the second term has the coefficient b^-1, with no a shift.
    for h, first, second in product((1,3),range(2),range(2)):
        left,right = word_rewards(h,[first,second],False)
        lk = next(iter(left)); rk = next(iter(right))
        v = MOVES[(h+1-2*first)%4][1]
        require(lk[:2] == (0,0) and rk[:2] == (0,-1), 'pair coefficient')
        require(lk[3] == v and rk[3] == -v and lk[2] in (-1,1) and rk[2] in (-1,1),
                'pair exponents')
    return {'opposite_pairs':8,'constant_four_blocks':8,'four_turn_words':16,'horizontal_pairs':8}


def square_range(n):
    return Q(13)*3**(n-1)-6-Q(3)**(2-n)


def diagonal_audit():
    # A=UV and C=U/V are integral powers of 3 even for square half-centres.
    # This checks the square head decomposition without approximating sqrt(3).
    def g(u, v, positive):
        return scale(add(mono(u=u,v=v), mono(u=-u,v=-v,coefficient=-3)),Q(1,2)) if positive else scale(add(mono(u=-u,v=-v),mono(u=u,v=v,coefficient=-3)),Q(1,2))
    for h in range(4):
        head = {}
        for (a,b,u,v), c in HEAD[h].items():
            head = add(head, mono(u=u,v=v,coefficient=c*Q(3)**(a+b)/16))
        diagonal = add(g(1,1,h in (0,1)),g(1,-1,(h-1)%4 in (0,1)))
        require(head == diagonal,'square head decomposition')
    require(scale(FIELD,-1) == add(mono(u=1,v=-1),mono(u=-1,v=1),
                                    mono(u=1,v=1,coefficient=-1),
                                    mono(u=-1,v=-1,coefficient=-1)),
            'square field decomposition')
    return 5


def arithmetic_audit():
    rows=[]
    for n in range(1,101):
        original=Q(3)**(1-n)*(3**n-1)**2+4*(Q(3)**(n-1)-Q(3)**(1-n))
        require(original == square_range(n), 'square simplification')
        bound=4*(3*original//16)+4
        require(bound <= Q(13,4)*3**n+4 and bound < 8*n*3**n+1,'square comparison')
        # Maximal T allowed by floor((T-1)/4)<=m is exactly 4m+4.
        m=3*original//16
        require((bound-1)//4 == m and bound//4 == m+1,'exit rounding')
        if n in (1,2,3,4,6,8,12,16):rows.append({'n':n,'square_bound':int(bound)})
    # Pair counts: discard a leading vertical arrival and a trailing unpaired
    # step, for any number of internal-to-internal updates, including zero.
    for length, horizontal in product(range(100), (False,True)):
        used = max(0,length-(not horizontal))
        pairs = used//2
        require(length+1 <= 2*pairs+3,'rectangular exit rounding')
    return rows


def main():
    count=local_identity_audit()
    blocks=block_audit()
    diagonals=diagonal_audit()
    rows=arithmetic_audit()
    print(json.dumps({'status':'passed','method':'exact Laurent polynomial coefficients; no source imports or CAS',
                     'universal_local_identities':count,
                     'universal_square_decompositions':diagonals,
                     'block_cases':blocks,'square_formula_sizes':100,
                     'exit_pair_count_cases':200,'square_bounds':rows},indent=2))


if __name__ == '__main__': main()
