"""Theorem-local exact tests. Finite tests supplement, not replace, the proof.
Run from any working directory, without python -O. Standard library only.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib,json,random,sys
from critical import (State,Potential,advance,sector,square_value,
 square_range_upper,square_exit_bound,rectangular_exit_bound,exact_rectangle_bound)

if sys.flags.optimize: raise SystemExit('Do not disable assertions')
HERE=Path(__file__).resolve().parent
R=random.Random(20261015)
counts=Counter()


def independent_step(black,pos,direction):
    # Complex numbers are used only for small integer-valued reference examples.
    z=complex(*pos)
    black=set(black)
    if pos in black:
        black.remove(pos); direction*=1j
    else:
        black.add(pos); direction*=-1j
    z+=direction
    return black,(int(z.real),int(z.imag)),direction


def word_seed(pos,heading,word):
    # A geometrical turn word prescribes initial colour on first read; reject
    # inconsistent prescriptions when the same coordinate is read again.
    b=set(); init=set();seen=set();p=pos;h=heading
    moves=((0,1),(1,0),(0,-1),(-1,0))
    for c in word:
        bit=c=='L'
        if p not in seen:
            if bit:b.add(p);init.add(p)
            seen.add(p)
        if (p in b)!=bit:return None
        b.symmetric_difference_update((p,))
        h=(h+(-1 if bit else 1))%4
        dx,dy=moves[h];p=p[0]+dx,p[1]+dy
    return State(frozenset(init),pos,heading)


# All eight local identities at multiple parameters/centres with external fields.
parameters=[(Q(3),Q(3)),(Q(2),Q(5)),(Q(5),Q(2)),(Q(8,7),Q(29)),(Q(37,36),Q(145))]
for a,b in parameters:
 for centre in [(0,0),(2,-3),(-1,4)]:
  potential=Potential(a,b,centre)
  for x,y in product(range(-2,3),repeat=2):
   for h,bit in product(range(4),range(2)):
    field={(9,-7),(-6,8),(3,4)}
    if bit:field.add((x,y))
    s=State(frozenset(field),(x,y),h);v=advance(s)
    assert sector(s)==sector(v)
    assert potential(v)-potential(s)==potential.increment(s)
    ib,ip,ih=independent_step(s.black,s.pos,[1j,1,-1j,-1][h])
    assert ib==v.black and ip==v.pos and ih==[1j,1,-1j,-1][v.heading]
    counts['local_identity_cases']+=1

# Four-update coercivity including every turn word, pose and square centre.
minimum=None;sharp=None
for n in range(1,5):
 for x,y in product(range(-2,3),repeat=2):
  for h in range(4):
   for word in map(''.join,product('RL',repeat=4)):
    s=word_seed((x,y),h,word)
    assert s is not None  # four quarter-turn moves never re-read before the end
    z=s
    for _ in range(4):z=advance(z)
    delta=square_value(z,n)-square_value(s,n)
    assert delta>=Q(16,3),(s,word,delta)
    if minimum is None or delta<minimum:
     minimum=delta;sharp={'n':n,'pos':list(s.pos),'heading':h,'word':word,
                         'black':sorted(map(list,s.black)),'increase':str(delta)}
    if n%2:
     p=Potential(Q(3),Q(3),((n-1)//2,)*2)
     assert square_value(s,n)==p(s)
    counts['four_update_cases']+=1
assert minimum==Q(16,3)

# Exact two-step rectangle pair: horizontal arrival, then a vertical move.
for n in range(1,13):
 p=Potential(Q(n+1,n),Q(4*n+1))
 delta=4*(1+1/p.b)*p.a**(-(n-1))
 assert delta>Q(4,3)
 for x in range(n):
  for y in range(-8,9):
   for h in (1,3):
    for word in map(''.join,product('RL',repeat=2)):
     s=word_seed((x,y),h,word);v=advance(advance(s))
     assert p(v)-p(s)>=delta
     counts['vertical_pair_cases']+=1

# Range and coarse-bound checks. These compute ranges, not true worst exit times.
range_rows=[]
for n in range(1,13):
 for h in range(1,13):
  exact,width,delta=exact_rectangle_bound(n,h)
  coarse=rectangular_exit_bound(n,h)
  assert exact<=coarse
  assert width<=3*(n*h+16)*(4*n+1)**(h//2)
  counts['rectangle_range_cases']+=1
 # Direct square field and pose range independent of diagonal decomposition.
 cells=[(x,y)for x in range(n)for y in range(n)]
 empty=State(frozenset(),(0,0),0)
 base=square_value(empty,n)
 field_range=sum(abs(square_value(State(frozenset((q,)),(0,0),0),n)-base)for q in cells)
 heads=[square_value(State(frozenset(),q,h),n)for q in cells for h in range(4)]
 width=field_range+max(heads)-min(heads)
 assert width<=square_range_upper(n)
 assert square_exit_bound(n)<=Q(13,4)*3**n+4
 range_rows.append({'n':n,'certified_square_exit_bound':square_exit_bound(n),
                    'square_range_upper':str(square_range_upper(n)),
                    'exact_range_upper':str(width)})
 counts['square_range_cases']+=1

# Complete enumeration of small rectangles using a separate mutable bit simulator.
# Termination here is guarded by a generous fixed test cap, not presumed from HC.
rectangles=[(1,1),(2,1),(3,1),(4,1),(2,2),(3,2),(4,2),(3,3)]
maxima=[]
for n,h in rectangles:
 A=n*h;number=0;longest=0;witness=None
 bound=exact_rectangle_bound(n,h)[0]
 if n==h:bound=min(bound,square_exit_bound(n))
 for mask in range(1<<A):
  for pos in range(A):
   for hd in range(4):
    bits=mask;x=pos%n;y=pos//n;d=[1j,1,-1j,-1][hd];time=0
    while 0<=x<n and 0<=y<h:
     j=y*n+x
     d*=1j if(bits>>j)&1 else -1j
     bits^=1<<j
     x+=int(d.real);y+=int(d.imag);time+=1
     if time>10000:raise AssertionError('finite test cap reached')
    assert time<=bound
    if time>longest:
     longest=time;witness={'initial_mask':mask,'pos':[pos%n,pos//n],'heading':hd}
    number+=1;counts['small_rectangle_literal_updates']+=time
    counts['small_rectangle_complete_states']+=1
 maxima.append({'n':n,'h':h,'all_initial_states':number,'exact_max_exit':longest,
                'witness':witness,'bound_used':bound})
assert [r['exact_max_exit'] for r in maxima if r['n']==r['h']]==[1,6,17]

# Outside field cancels before first exit: compare exact values along true traces.
for n,h in [(3,6),(6,3),(7,7),(10,6)]:
 p=Potential(Q(n+1,n),Q(4*n+1),(0,(h-1)//2))
 outside=frozenset({(-5,-4),(n+6,h+4),(n+7,-9)})
 for _ in range(20):
  b=frozenset((x,y)for x in range(n)for y in range(h)if R.getrandbits(1))
  s=State(b,(R.randrange(n),R.randrange(h)),R.randrange(4))
  z=State(b|outside,s.pos,s.heading)
  shift=p(z)-p(s);steps=0
  while 0<=s.pos[0]<n and 0<=s.pos[1]<h:
   assert z.pos==s.pos and z.heading==s.heading
   assert z.black.symmetric_difference(s.black)==outside
   assert p(z)-p(s)==shift
   s=advance(s);z=advance(z);steps+=1
   counts['external_archive_update_cases']+=1
  assert steps<=rectangular_exit_bound(n,h)
  counts['external_archive_trajectories']+=1

# Four-block lower bound alone does not certify eventual P104.
# Explicit malformed parameter and non-integer-coordinate rejection controls.
for args in [(2,2),(1,5),(3,4),(0,0)]:
 try:Potential(*args)
 except ValueError:counts['rejected_invalid_inputs']+=1
 else:raise AssertionError('bad critical parameter accepted')
for args in [(0,3),(3,0),(-1,2),(1.5,2)]:
 try:rectangular_exit_bound(*args)
 except ValueError:counts['rejected_invalid_inputs']+=1
 else:raise AssertionError('bad rectangle accepted')

report={'schema':'langtons-ant-critical-clock-check-v1','status':'passed',
        'arithmetic':'exact integers and rational fractions',
        'counts':dict(counts),'four_step_sharp_witness':sharp,
        'small_rectangles':maxima,'square_bounds':range_rows,
        'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (HERE/'critical.py',HERE/'check.py')},
        'not_claimed':['HC','finite HC counterexample','optimal rectangular escape',
                       'Lean formalization','external independent review','priority completeness']}
print(json.dumps(report,indent=2))
