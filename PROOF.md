# General consequences

The complete universal one-black theorem is owned by
[`one_black/`](./one_black/README.md). This document records results that use
that proof kernel but are not premises of the theorem.

## Clean-envelope entry

Let `A` be the cells read by the blank trajectory during its 9,977-step prefix
and first P104 block. Exact replay gives `|A|=1398`. If a translated and rotated
copy of `A` is initially white, induction couples the supplied state to the
blank trajectory for 10,081 updates. Black cells outside `A` remain untouched.
At the highway boundary, `standard_terminal` additionally decides whether they
avoid every future P104 footprint. Acceptance therefore proves permanent P104;
rejection makes no negative claim.

## Exact blank-interaction index

The blank prefix first reads 1,376 cells. `first_blank_hit` stores their first
read times and replays one P104 block. Every later blank read is uniquely a
block read translated by `n(-2,-2)`, `n>=0`; exact integer divisibility decides
that condition. The least prefix or periodic candidate is therefore the first
blank-orbit read of any supplied finite target, or `None` exactly if none is
ever read. Translation and rotation handle an arbitrary launch pose.

Until that indexed hit, a state differing from the blank launch only on the
target set makes identical updates by first-difference induction. Thus `None`
proves permanent blank coupling, while a finite answer locates the first colour
divergence.

## Complete-history renewal

### Finite escape

Every classical Langton trajectory leaves every finite set. If an orbit were
confined to `n` cells, its `4*n*2^n` possible states would eventually repeat.
One update is reversible, so the orbit would be periodic and every visited cell
would recur infinitely often. Move axes alternate and visit-time parity is
fixed by cell parity, hence each cell is always entered on the same axis.

Choose the highest visited row and then its rightmost visited cell `M`. Its
north and east neighbours are unvisited. Horizontal entries must come from the
west and exit south; the first such visit toggles the colour, forcing the next
exit north. Vertical entries analogously come from the south and exit west,
then toggle and force the next exit east. Both contradict confinement. This is
the Cohen--Kong extremal argument recorded by David Gale (1993), and it works
for any finite initial colouring.

Consequently a trajectory exits a fixed `n`-cell set within `4*n*2^n` updates:
a longer confined trace would repeat a state.

### Exact event

A carrier is `(X,U,t)`, with complete finite physical state `X`, every cell
read before time `t` in finite `U`, `black(X) subset U`, and the ant currently
outside `U`. At a carrier, first test the phase-complete terminal predicate.
Otherwise query the blank-interaction index against all black cells of `X`.

- No hit proves permanent blank coupling.
- A hit is replayed exactly through the first divergent update. Add the entire
  read footprint to `U`, then use finite escape to find the first later fresh
  cell. That state is the next carrier.

Thus `renew` is total computable and returns `terminal`, `blank-coupled`, or a
`renewed` edge satisfying

```text
target.time > source.time
target.old = source.old union event.footprint
source.old is a strict subset of target.old.
```

Strictness holds because the fresh launch cell is read during the event. No
physical state, old component, or time is quotiented or capped.

### Bireduction and genealogy

`initial_carrier` computes the first fresh checkpoint of a finite seed. For
every legal carrier `C`,

```text
physical(C) reaches P104 iff the renewal program from C halts.
```

The reverse direction is the meaning of the two halts. If P104 starts at time
`T` but renewal ran forever, strictly increasing event times would eventually
place a checkpoint at or after `T`; forward invariance and phase-completeness
would force a terminal halt. Hence renewal preserves, rather than solves, the
original decision problem.

Label each uninterrupted black lifetime at the first carrier as a root. In an
event, the live blocker dies at divergence and parents every newly born black
lifetime surviving to the target. Absolute birth times uniquely label these
computable edges. Roots and branching are finite, and a blocker parents only
once. Therefore an infinite renewal run creates infinitely many vertices;
Koenig's lemma yields an infinite branch. Event indices increase along edges,
so the converse also holds:

```text
renewal halts iff its canonical genealogy has finite height.
```

For global termination only, all legal carriers may be restricted to connected
nonempty `old`. Read footprints are connected and consecutive footprints
attach. The number of old components cannot increase and drops whenever an
event reaches another component. An infinite chain has a tail after the last
drop; components outside its active one are never read again and may be deleted
by first-difference induction without changing that tail or introducing an
earlier certified halt. This is an existential projection of infinite chains,
not an online preprocessing rule; executable carriers retain all components.

## Exact structural invariants

These follow algebraically from one update and constrain research without
proving termination.

- Visit letters at each cell alternate. Realizable turn words are exactly those
  with per-cell alternation and only finitely many first-visit black letters,
  modulo never-read cells.
- Five identical consecutive turns are impossible: four traverse a unit square
  and toggle the first cell, forcing the fifth turn to differ. Successive
  `L -> R` valleys are separated by `R^a L^b`, `1<=a,b<=4`, so return time to
  the valley section is at most eight; the carried black set remains unbounded.
- With headings numbered in `Z/4Z`, `heading-|B| mod 4` is invariant. In one
  sector, after toggling the origin to get `C`, translation-normalized dynamics
  sends `C` by `-d(kappa+|C| mod 4)`. It is reversible but depends on global
  cardinality. Exact colour restoration up to translation therefore restores
  heading too, ruling out residue-free U-turn gadgets.
- Head normalization gives affine branches
  `Phi_R(x,y)=(-y,x-1)` and `Phi_L(x,y)=(y,-x-1)` after toggling the origin.
  Laurent-polynomial encoding is affine for a prescribed turn word, but the
  current constant coefficient selects the branch.
- Pairing a vertical and horizontal move yields an exact diagonal-lattice walk
  with one sign bit. Direction counts have displacement
  `(C1-C3,C0-C2)`; a same-cell return increment is `m(1,1,1,1)`, `m>=1`.
- `parity(x+y) XOR heading-axis` is invariant. Viewing black cells as edges
  between row and column tokens, `boundary(B) XOR ant-axis-token` is conserved.
  A same-axis macro therefore writes a finite plaquette field divisible by
  `(1+X)(1+Y)` over `F_2`.
- The modulo-four sums of `x+y` and `x-y`, with their unique pose corrections,
  are conserved. These and the preceding charges are endpoint filters, not
  descending ranks.
- Exact head-normalized inverse branches preserve finite symbolic classes
  described by required black cells, required white cells, and forbidden
  affine rays. Entry within any fixed finite depth is therefore decidable; no
  effective stabilization of their increasing union follows.

## Computability boundary

Normalized finite seeds are enumerable, and exact replay plus
`standard_terminal` decides `Entry(z,t)`. Hence

```text
HIGHWAY = {z | exists t, Entry(z,t)}
```

is computably enumerable. The following are equivalent: total membership
decidability; c.e. complement; a total computable upper bound on positive entry
time; and a decidable finite certificate relation complete for negative seeds.
The conversions are the standard search, bounded replay, dovetailing, and
accepting-computation encodings. They identify the missing object but do not
construct it. Even a membership decider settles HC only if it also proves that
no seed is negative.

Generic renewal properties cannot settle this boundary. Reversible systems can
carry their histories and a growing clock while preserving total steps, strict
history growth, acyclicity, and finite branching; the underlying halting set
may still be either decidable or undecidable. A final argument must exploit the
literal planar left/right geometry.

## Two further boundaries

Semantic archive deletion is sound but non-effective: a finite discrepancy
set never read after time `T` may be deleted at `T` by first-difference
induction, but deciding that premise from an arbitrary current state requires
future knowledge.

A bounded finite-phase tally with one black bulk cell in every column, fixed
endpoint axis, and exact restoration except extension from `n` to `n+1` is also
impossible. Row/column parity forces

```text
b_i+b_(i+1) = X^(n+1)(1+c_i+X c_(i+1)).
```

Bounded residues make both sides vanish for unbounded `n`, so
`b_i=b_(i+1)` and `c_(i+1)=X^-1(c_i+1)`. Around a `k`-phase cycle,
`(X^k+1)c_0=1+X+...+X^(k-1)`. Cancelling the geometric sum would give
`(X+1)c_0=1`, impossible in the Laurent domain. Multi-track,
moving-interface, non-restoring, and unbounded-control designs remain open.

## Scope and trust

Nothing here proves universal two-black termination or the finite-support
Highway Conjecture. Executable checks live in `research/check.py` and use the
closed one-black kernel plus `research/renewal.py`. The Python interpreter and
those literal arithmetic modules are trusted; the deductions in this document
are human-checked and are not claimed as proof-assistant formalizations.
