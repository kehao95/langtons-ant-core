"""Theorem-local checks for the clock manuscript, using a separate stepper."""
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path
import hashlib
import json
import random
import sys

HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / 'clock'
if not (BASELINE / 'diagonal_clock.py').is_file():
    BASELINE = HERE / 'baseline'
if not (BASELINE / 'diagonal_clock.py').is_file():
    raise SystemExit('Place the unchanged diagonal_clock.py in ../clock or ./baseline')
if sys.flags.optimize:
    raise SystemExit('Do not run exact assertion checks with Python -O')
sys.path.insert(0, str(BASELINE))
import diagonal_clock as source


def step(B, p, h):
    z = complex(*p)
    heading = (1j, 1, -1j, -1)[h]
    b = p in B
    heading *= 1j if b else -1j
    B.symmetric_difference_update((p,))
    z += heading
    return (int(z.real), int(z.imag)), (1j, 1, -1j, -1).index(heading)


def phi(B, p, h, r=F(4), center=0):
    parity = lambda p: 1 if sum(p) % 2 == 0 else -1
    sigma = parity(p) * (-1 if h % 2 else 1)
    s = sum(p) - center
    pose = (r**s-r**(1-s)) if h in (0, 1) else (r**(-s)-r**(s+1))
    return -sigma*sum((parity(q)*(r**(sum(q)-center)+r**(center-sum(q))) for q in B), F(0))+2*pose/(r+1)


def bound(n, r=None):
    r = F(3)+F(3,n) if r is None else F(r)
    a = r**(1-n)*(r**n-1)**2/(r-1)**2+r**(n-1)-r**(1-n)
    a *= (r+1)/(r-3)
    return a.numerator//a.denominator+1

local = 0
for r, x, y, h, colour, center in product((F(31,10),F(10,3),F(4),F(6)),
                                          range(-3,4),range(-3,4),range(4),range(2),(-2,0,3)):
    B = {(x,y)} if colour else set()
    B.add((40, -40))  # A fixed external contribution must cancel.
    p=(x,y); old=phi(B,p,h,r,center)
    B2=set(B); p2,h2=step(B2,p,h)
    s=x+y-center; d=(r-3)/(r+1); e=(5*r+1)/(r+1)
    sign = h in (0,1); sign2=h2 in (0,1)
    expected=d*(r**s+r**(-s)) if sign==sign2 else (d*r**s+e*r**(-s) if sign else e*r**s+d*r**(-s))
    assert phi(B2,p2,h2,r,center)-old==expected and expected>=2*d
    st=source.State(frozenset(B),p,h)
    assert source.clock(st,r,center)==old
    assert source.inverse_step(source.step(st))==st
    local += 1
squares=[]
for n in range(1,4):
    cells=list(product(range(n),repeat=2)); cases=0; longest=0; updates=0
    for mask in range(1<<len(cells)):
        initial={p for i,p in enumerate(cells) if mask>>i&1}
        for start,h0 in product(cells,range(4)):
            B=set(initial); p,h=start,h0; t=0
            while 0<=p[0]<n and 0<=p[1]<n:
                p,h=step(B,p,h);t+=1
                assert t<=bound(n)
            longest=max(longest,t);cases+=1;updates+=t
    squares.append(dict(n=n,cases=cases,maximum_exit=longest,updates=updates,clock_bound=bound(n)))
comparisons=[]
for n in range(1,101):
    assert bound(n)==source.square_escape_bound(n)
    assert bound(n)<=8*n*3**n+1
    if n in (1,2,3,4,6,8,10,12,16,20,30):
        comparisons.append(dict(n=n,clock=bound(n),coarse=8*n*3**n+1,factorial=factorial(n+1)))
report={'schema':'clock-manuscript-check-v1','local_cases':local,'square_exhaustion':squares,
        'bound_parameter_checks':100,'bound_comparisons':comparisons,
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_blob_sha1':hashlib.sha1(b'blob '+str(len(Path(source.__file__).read_bytes())).encode()+b'\0'+Path(source.__file__).read_bytes()).hexdigest(),
        'independent_external_review':False,'lean_build':False,'global_HC':False}
Path(__file__).with_name('clock_check_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
