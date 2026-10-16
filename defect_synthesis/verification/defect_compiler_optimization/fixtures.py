"""Deterministic supplied schemas; these are controls, not new ant theorems."""
from fast import Aff, Block, FastSchema
W = ('RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRL'
     'LRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR')
B = ('RRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLRRRRLRLLLLRRRR'
     'LRRLRRRRLLLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRLL')
A = 'L' + B[75:]
assert len(W) == 104 and len(B) == 102 and len(A) == 28
L10 = set((W * 2)[i:i+10] for i in range(104))


def schema_case(name, ctx=None):
    n, m = Aff.var('n'), Aff.var('m')
    if name == 'standard':
        return FastSchema(['n'], [Block(W, n)], domain='n>=0', ctx=ctx)
    if name == 'rail':
        return FastSchema(['n'], [Block('LRRL', n)], heading=1, domain='n>=0', ctx=ctx)
    if name == 'fold':
        return FastSchema(['n', 'm'], [Block(B), Block(A, n), Block(B), Block(A, m)],
                          domain='n>=1 and 0<=m<n', ctx=ctx)
    if name == 'marker':
        return FastSchema(['n'], [Block(W, n), Block('L')], domain='n>=0', ctx=ctx)
    if name == 'sweeps':
        return FastSchema(['n'], [Block('RLLR', n), Block('LRLLRL'),
                          Block('RLLR', n), Block('LRLLRL'), Block('LRRL', n)],
                          heading=1, domain='n>=1', ctx=ctx)
    raise ValueError('unknown schema fixture')
