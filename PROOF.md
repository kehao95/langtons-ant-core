# Proof

## Convention

A state is read immediately before an update. On white the ant turns right;
on black it turns left. It then toggles the current square and moves one edge.
North increases the second coordinate. `model.py` implements exactly this
definition with an immutable finite set of black lattice points.

## The finite P104 witness

Starting from the blank plane, `verify_blank_highway` performs 9,977 updates
and calls the result `E`. It then replays the next 104 updates and derives,
rather than stores, the colour required on every square when that square is
first read during the block. Repeated reads are checked for consistency.

The replay checks three finite facts:

1. after 104 updates the heading is unchanged and the displacement is
   `(-2, -2)`;
2. the relative read requirements of the next block are identical;
3. at both `E` and its successor, every initially black square outside the
   current block is absent from every later translated block footprint.

For the third fact, a footprint point has the form `o + n(-2,-2)`, where `o`
is one of the finitely many relative read positions and `n` is a nonnegative
integer. `_multiple` decides that equation exactly in integers. Only the
finite black support must be inspected.

## Recurrence lemma

Suppose a state has the witness heading and required local colours, and no
extra black square lies in a later block footprint. Induction over the 104
individual updates gives the same turns and visited positions as the finite
replay, because each decision reads a required colour and all earlier toggles
within the block are identical. Thus the endpoint is displaced by `(-2,-2)`
with the same heading and the same relative local requirements.

The only squares changed during the block are its footprint. An extra black
square is never read because later footprints were required clear. Removing
the completed footprint and translating the index `n` by one therefore gives
the same clear-corridor condition at the endpoint. The finite checks at `E`
and its successor cover the local overlap between adjacent footprints. Hence
the endpoint satisfies the same hypotheses. Induction on the number of
blocks proves an infinite translating period-104 highway.

Applying this lemma to `E` proves the blank-plane result.

## One black square in the blank prefix

The blank orbit first reads exactly 1,376 cells before update 9,977.
`verify_prefix_one_black` derives this set from the literal blank replay. For
each cell `q` it starts from the otherwise white plane with only `q` black and
searches at most 110,000 exact updates for a terminal P104 boundary. Every case
is accepted; the largest observed terminal time is 106,258 updates. This is a
finite exhaustive proof of every prefix-hit position, not a sample. The case
where the black square starts under the ant is included.

Translation and quarter-turn rotation commute with one ant update: they
preserve colour membership, exchange headings and unit moves in the same way,
and leave left and right turns unchanged. Induction on updates transports the
1,376 canonical replays to every initial position and heading.

If `q` is outside this prefix domain, untouched-cell coupling reaches the
complete 715-cell blank-entry state plus `q`. Proving P104 from every such `q`
requires stability against its 702-cell historical wake; the next three
sections supply that argument.

## Pristine P104 plus one arbitrary obstacle

Let `P` be the 13 black requirements of a pristine cycle boundary and `S` its
40-cell read support. Every lattice cell `q` lies in exactly one class:

1. `q in P`, which changes nothing;
2. one of the 27 white cells in `S`;
3. `f + k(-2,-2)`, where `k>=1` and `f` is one of 22 last support cells on its
   translation lane;
4. outside the complete future corridor, where it is never read.

Integer divisibility proves that this partition is exhaustive and unique.
`verify_pristine_one_obstacle` directly replays the 27 active-white cases and
depths 1 through 20 on every lane, for 467 finite cases. All reach a terminal
boundary; the largest finite replay is 64,978 updates.

It remains to cover every greater depth. One clean P104 block moves the active
pattern by `v=(-2,-2)` and leaves a finite XOR wake `E`. For a fixed lane, let
`D` be the complete read footprint of the depth-20 terminal computation. The
verifier checks exactly:

- the depth-21 state after one clean block is the depth-20 input translated by
  `v`, XOR `E`;
- `E` misses every later clean support;
- every ray `E-mv`, `m>=1`, misses `D`;
- those rays also miss every future translate of the final, possibly rotated,
  terminal support.

For depth `20+n`, execute `n` clean blocks. The remaining state is the
depth-20 input translated by `nv`, plus the accumulated wakes
`E,E+v,...,E+(n-1)v`. The four checks make every accumulated wake unread during
the translated depth-20 computation and outside its final corridor. XOR
coupling therefore gives the translated terminal computation. Induction on
`n` proves every lane depth. Together with the other three location classes,
this proves that a pristine P104 boundary plus one arbitrary black cell always
returns to permanent P104.

## Actual blank-entry wake: ordinary lanes

The real blank state at update 9,977 contains 715 black cells: the 13-cell
active pattern and a fixed 702-cell historical wake `H`. Adding an obstacle on
one of the 27 active-white cells gives 27 direct terminal replays.

For each future lane, reuse the pristine depth-20 terminal trace `D`. For a
deeper obstacle, the only possible failure of untouched-set coupling is an
intersection of `H` with `D+nv` or with the final terminal corridor translated
by `nv`. Both questions are exact two-variable integer equations in the clean
drift and the rotated terminal drift. `verify_actual_entry_ordinary` solves
them over all 702 history cells and all finite trace/support cells.

On 21 lanes, every bad parameter is below the depth-20 base. Exact replay of
that finite prefix plus the active-white cases gives 447 cases, with maximum
terminal time 57,717. Beyond the base, `H` is never read and never enters the
terminal corridor, so XOR coupling reduces the complete 715-cell state to the
translated pristine theorem at every depth.

The remaining head is `(-2,-8)`. Its pristine terminal drift is the reverse of
the clean drift, and the two-ray equation has infinitely many intersections
with `H`; the ordinary reduction correctly rejects it. This is the exceptional
phase-72 lane.

## Phase-72 two-way induction

Depths 1 through 19 are direct terminal cases. At depth 20 the pristine
scattering reaches a terminal boundary whose drift is `(2,2)`, opposite the
clean drift. Exact affine intersection of one reverse P104 block with all 702
history cells finds the first hit at the fixed canonical cell `(20,-22)`.
Increasing obstacle depth by one adds one forward clean block and one reverse
clean block, so the local-boundary-to-hit time increases by exactly 104 while
the hit pose stays fixed. The corridor index proves this for every depth; three
consecutive exact replays anchor the recurrence to literal dynamics.

At the fixed hit, consecutive-depth black sets differ by one finite XOR layer
`L`; the next pair differs by `L+(-2,-2)`. One more forward/reverse block
therefore appends the next translate of the same layer. From the base hit,
exact replay reaches a terminal P104 boundary after 7,994 updates, and the
next-depth hit follows the identical post-hit read/turn sequence.

Finally, the verifier checks that every ray
`L+n(-2,-2)`, `n>=0`, misses both the complete post-hit read footprint and
every future translate of the final terminal support. Thus all accumulated
variable layers are inert. Induction on depth gives the same 7,994-step
post-hit computation and a sound terminal boundary for every depth at least
20. With the 19 shallow cases, phase 72 is closed at all positive depths.

## Universal one-black theorem

Normalize the initial ant pose. If its unique black cell is in the 1,376-cell
blank prefix, the exhaustive finite theorem applies. Otherwise exact XOR
coupling follows the blank orbit through update 9,977, producing the complete
715-cell blank-entry state plus that untouched black cell.

At this boundary the added cell is already black, active white, outside the
future corridor, on one of 21 ordinary lanes, or on phase 72. These cases are
respectively trivial, finite, terminal by noninteraction, covered by historical
wake separation, or covered by the two-way induction. Hence every normalized
one-black state reaches permanent P104. Translation and quarter-turn symmetry
give every ant position and heading.

## Clean-envelope theorem

Let `A` be the set of cells read by the blank trajectory during its 9,977-step
prefix and first 104-step highway block. Exact replay gives `|A| = 1398`.
Translate and rotate `A` with an arbitrary initial ant pose.

If every cell of that copy of `A` is initially white, induction on the first
10,081 updates couples the supplied state to the blank trajectory: every read
colour, turn, toggle and move agrees. Black cells outside `A` remain untouched.
At update 9,977, `standard_terminal` additionally decides whether those
untouched cells avoid the infinite future P104 footprint. When it accepts, the
recurrence lemma proves permanent P104. Thus `clean_envelope_entry` is a
decidable sufficient YES condition; rejection makes no negative claim.

## Exact blank-interaction index

The blank prefix before update 9,977 reads exactly 1,376 distinct cells.
`first_blank_hit` stores only their first-read times, then replays one P104
block. Every later blank read is uniquely a block read translated by
`n(-2,-2)`, `n>=0`; `_multiple` solves this condition exactly. Taking the least
prefix or periodic candidate therefore returns the first blank-orbit read of
any supplied finite target set, or `None` exactly when no target is ever read.
Translation and rotation normalize an arbitrary launch pose before the query.

If an actual state launched into fresh white space has a finite black set `D`,
then until this indexed first read of `D` it differs from the blank reference
only on `D`. The update choices and pose agree by induction. If the index
returns `None`, the actual orbit follows the certified blank P104 path forever;
if it returns a time, exact replay reaches the first colour divergence. This is
the finite interaction oracle needed by both universal one-black and renewal.

## Terminal scope and trust

Nothing here proves universal two-black termination or the general
finite-support Highway Conjecture.

The trusted executable base is the Python interpreter, `model.py`, and the
finite arithmetic in `highway.py` and `one_black.py`. The recurrence,
separation and symmetry arguments above are human-checked mathematics; there
is no claim that they have been formalized in a proof assistant.

## Exact structural theorems

The remaining results in this section follow algebraically from one literal
update. They constrain the global research problem but are not termination
theorems.

### Turn words and bounded runs

Write `R` for a white read and `L` for a black read. Once a cell is first read,
each later read of that same cell has the opposite colour because every read
toggles it. Hence the letters attached to successive visits of one cell
alternate. The cells whose first read is `L` are precisely the initially black
cells that the orbit visits, so this exceptional set is finite.

Conversely, a word whose induced walk alternates on each cell and has only
finitely many first-visit `L` cells is realized by making exactly those cells
initially black. Induction on the word position proves equality of every read;
initially black cells never visited are irrelevant. This is an exact orbit
description modulo such inert cells.

Four consecutive equal turns traverse a unit square and return to its first
cell. That cell was toggled on the first visit, so the fifth turn must be the
opposite letter. Thus neither `RRRRR` nor `LLLLL` occurs.

At every `L -> R` transition call the state before `R` a valley. Between two
successive valleys the word is uniquely `R^a L^b`, with `1 <= a,b <= 4`.
Every infinite orbit has infinitely many valleys, and their return time is at
most eight updates. The sixteen labels do not erase the carried black set, so
the valley section is bounded-return but not finite-state.

### Cardinality sector and normalized dynamics

Number headings clockwise in `Z/4Z` and let `N=|B|`. A white update increases
both heading and `N` by one; a black update decreases both by one. Therefore

```text
kappa = heading - |B| mod 4
```

is invariant. In a fixed sector, translate the ant to the origin, toggle the
origin to obtain `C`, and let `d(j)` be the unit vector of heading `j`. The exact
translation-normalized map is

```text
U_kappa(B) = C translated by -d(kappa + |C| mod 4).
```

Its inverse translates by `d(kappa + |B| mod 4)` and toggles the origin. Thus
the map is reversible, but its displacement selector uses global cardinality;
no fixed-radius symbol at the origin determines the next move.

If the full black configuration is restored up to translation, its cardinality
is unchanged, so the invariant forces the heading to be restored as well. In
particular, an exact colour-restoring U-turn or time-reversal gadget is
impossible; it must export residue or consume fuel.

### Head-normalized affine form

Alternatively translate the ant to the origin and rotate its heading to north.
For a finite relative black set `S`, let

```text
Phi_R(x,y) = (-y, x-1),    Phi_L(x,y) = (y, -x-1).
```

After toggling the origin, the exact next set is `Phi_R(S xor {0})` when the
origin was white and `Phi_L(S xor {0})` when it was black. Encoding a finite set
by its Laurent polynomial over `F_2` turns these into

```text
T(P) = Y^-1(P(Y,X^-1)+1)   if constant(P)=0,
T(P) = Y^-1(P(Y^-1,X)+1)   if constant(P)=1.
```

The branch is affine for a prescribed turn word but is selected by the current
constant coefficient. This conjugacy is exact and does not linearize the
adaptive orbit problem.

### Two-step and count lifts

Sample before a vertical move and encode north/south by `s=+1/-1`. If the next
two read colours are `a,b in {0,1}`, put

```text
delta = s(-1)^a,
s' = -s(-1)^(a+b).
```

The paired macro toggles exactly `p` and `p+(delta,0)`, moves by `(delta,s')`,
and retains vertical sign `s'`. This is an exact diagonal-lattice walk with one
sign bit, not a finite automaton.

Let `C_0,...,C_3` count moves north, east, south and west. Position displacement
is `(C_1-C_3, C_0-C_2)`. On a same-cell return north equals south and east
equals west. Since move axes alternate, horizontal and vertical move counts
are equal too. Consequently every return increment is

```text
m(1,1,1,1),  m >= 1.
```

The monotone count lift therefore has a rank-three quotient and a rank-one
same-cell fibre; separate cells can still store independent colour bits.

### Endpoint conservation laws

The parity of `x+y` flips on every move, and the heading axis flips on every
turn. Their XOR is invariant.

Represent each black cell `(x,y)` by an edge between column token `C_x` and row
token `R_y`, and let `partial(B)` be the odd-degree tokens. Toggling the current
cell toggles `{C_x,R_y}`. Those are exactly the ant's axis tokens before and
after its perpendicular move. Hence

```text
partial(B) xor {ant axis token}
```

is conserved. If a macro has the same endpoint axis token, every row and every
column of its net write has even parity. Its finite Laurent polynomial is
therefore divisible by both `1+X` and `1+Y`, hence uniquely equals
`(1+X)(1+Y)g`: a finite plaquette field.

The incidence representation is still unbounded: arbitrarily many diagonal
black cells give arbitrarily many row/column tokens, and a finite old set can
connect them by lattice paths. Connected history therefore does not turn the
charge into a finite-state summary.

Two stronger modulo-four charges are also local. Define

```text
S+(B)=sum(x+y),    S-(B)=sum(x-y)                 (mod 4)
```

and, for pose `(x,y,h)`, use corrections

```text
g+(N)=y,  g+(E)=-x+1,     g+(S)=2x-y,  g+(W)=x+2y+1;
g-(N)=y,  g-(E)=-x+2y+1,  g-(S)=2x-y,  g-(W)=x+1.
```

Substitution in the white and black update shows that the correction changes
by respectively minus or plus the toggled cell's contribution. Thus `S+ + g+`
and `S- + g-` are conserved. These finite-group invariants are endpoint filters,
not descending ranks.

### Finite symbolic predecessors

The head-normalized inverse branch is selected exactly by whether the target's
south cell is black. A class described by finitely many required black cells,
required white cells, and forbidden affine rays therefore has a finite union of
preimage classes of the same form: split on the south-cell condition and apply
the inverse affine map.

By induction, states entering the certified terminal set within any supplied
finite depth `n` have an effectively computable finite symbolic description
and decidable membership. The union over all `n` is `HIGHWAY`; no effective
stabilization or complete complement certificate follows from finite-depth
closure alone.

## Computability interface

Normalize finite states by translating the ant to the origin. Finite subsets
of `Z^2`, headings and times have effective encodings, so normalized seeds are
enumerable. For a supplied seed `z` and time `t`, exact finite replay followed
by `standard_terminal` decides `Entry(z,t)`. Therefore

```text
HIGHWAY = {z | exists t, Entry(z,t)}
```

is computably enumerable.

The following four statements are equivalent:

1. `HIGHWAY` has a total membership decider.
2. Its complement is computably enumerable.
3. There is a total computable `B(z)` such that every positive `z` has an entry
   time at most `B(z)`.
4. There is one decidable finite relation `NoCert(z,c)` that is sound and
   complete for negative seeds.

For `1 -> 3`, return zero on a negative input and search for the first entry on
a positive one. For `3 -> 1`, replay through `B(z)`. Statements 1 and 2 are
equivalent because `HIGHWAY` is already c.e.; dovetail the two enumerations.
For `2 -> 4`, let `c` be a finite accepting computation of the negative
enumerator; checking such a computation is decidable. For `4 -> 2`, enumerate
all pairs and retain accepted certificates.

These equivalences locate the missing object but do not construct it. If HC is
true, `HIGHWAY` is the set of all seeds and is decidable. If HC is false,
`HIGHWAY` may still be a proper decidable set, or it may be a nonrecursive c.e.
set. A membership decider alone therefore does not settle HC unless it also
shows that no seed is negative.

Generic renewal properties cannot settle the classification. A finite word
system that deletes one symbol per step can be made reversible by retaining a
history track; adjoining a growing finite clock interval gives total steps,
strict history growth, acyclicity and finite branching, while every input
halts. The same bookkeeping can be adjoined to a fixed reversible universal
machine, preserving those properties while making input halting undecidable.
Thus any proof using only those abstract properties is insufficient. A final
argument must exploit the literal planar LR geometry, either to obtain a
complete finite negative witness or to implement an exact machine compiler.

## Two boundary results

Semantic archive deletion is sound but non-effective. If a finite discrepancy
set is never read after some time `T`, two states differing only on that set
make identical choices forever by induction on updates. Deleting the set at
`T` therefore preserves the physical future. Determining the hypothesis from
an arbitrary current state would require knowledge of that future, so this is
not an online quotient without a separate finite guard.

There is also a precise constructor obstruction. Suppose a parameterized tally
has one black bulk cell in every column `1..n`, bounded Laurent-polynomial base
and cap residues `b_i,c_i`, finitely many cyclic phases `i`, the same endpoint
axis, and exact restoration except for extension from `n` to `n+1`. Row/column
parity of the same-axis net write forces, over `F_2[X,X^-1]`,

```text
b_i + b_(i+1) = X^(n+1)(1 + c_i + X c_(i+1)).
```

The bounded left side cannot equal a nonzero translate for arbitrarily large
`n`; both sides must vanish. Hence `b_i=b_(i+1)` and
`c_(i+1)=X^-1(c_i+1)`. Around a cycle of length `k`, with
`S=1+X+...+X^(k-1)`, this gives `(X^k+1)c_0=S`. But
`X^k+1=(X+1)S`; cancellation in the Laurent domain would make
`(X+1)c_0=1`, impossible because `X+1` is not a unit. Thus this exact
finite-phase, one-black-column, same-axis architecture cannot be a uniform
constructor. Multi-track, moving-interface, non-restoring and unbounded-control
architectures remain outside the theorem.
