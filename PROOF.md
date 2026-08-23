# Consequences of the P104 kernel

[`one_black/`](./one_black/README.md) supplies the literal dynamics, terminal
predicate, blank P104 witness, and universal one-black theorem used below.

## Clean-envelope entry

Let `A` be the cells read by the blank trajectory during its 9,977-step prefix
and first P104 block. Exact replay gives `|A|=1398`. If a translated and rotated
copy of `A` is initially white, induction couples the supplied state to the
blank trajectory for 10,081 updates. Black cells outside `A` remain untouched.
At the highway boundary, `standard_terminal` decides disjointness from every
future P104 footprint. Acceptance proves permanent P104.

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

- `None` certifies permanent blank coupling.
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

Strictness holds because the fresh launch cell is read during the event. The
carrier records complete physical state, old set, and absolute time.

### Bireduction and genealogy

`initial_carrier` computes the first fresh checkpoint of a finite seed. For
every legal carrier `C`,

```text
physical(C) reaches P104 iff the renewal program from C halts.
```

The reverse direction is the meaning of the two halts. If P104 starts at time
`T` but renewal ran forever, strictly increasing event times would eventually
place a checkpoint at or after `T`; forward invariance and phase-completeness
would force a terminal halt. This proves a computable equivalence between P104
entry and renewal termination.

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

Global termination is equivalent on all legal carriers and on carriers with
connected nonempty `old`. Read footprints are connected and consecutive
footprints attach. The number of old components is nonincreasing and drops
whenever an event reaches another component. An infinite chain has a tail
after the last drop; first-difference induction deletes the inert components
from that tail while preserving its orbit and segmentation. The executable
carrier continues to record every component, while the connected-old theorem
acts on complete infinite chains.

## Exact structural invariants

These follow algebraically from one update and provide coordinates for the
global research problem.

- Visit letters at each cell alternate. Realizable turn words are exactly those
  with per-cell alternation and only finitely many first-visit black letters,
  modulo never-read cells.
- Equal-turn runs have length at most four: four turns traverse a unit square
  and toggle the first cell, forcing the fifth turn to differ. Successive
  `L -> R` valleys are separated by `R^a L^b`, `1<=a,b<=4`, so return time to
  the valley section is at most eight; the state also carries an arbitrary
  finite black set.
- With headings numbered in `Z/4Z`, `heading-|B| mod 4` is invariant. In one
  sector, after toggling the origin to get `C`, translation-normalized dynamics
  sends `C` by `-d(kappa+|C| mod 4)`. It is reversible but depends on global
  cardinality. Exact colour restoration up to translation therefore restores
  heading too. A U-turn construction consequently exports residue, consumes
  fuel, or changes its bulk state.
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
  are conserved. Together with the preceding charges they filter admissible
  endpoints; a descending measure additionally tracks causal evolution.
- Exact head-normalized inverse branches preserve finite symbolic classes
  described by required black cells, required white cells, and forbidden
  affine rays. Entry within any fixed finite depth is therefore decidable.

## Computability

Normalized finite seeds are enumerable, and exact replay plus
`standard_terminal` decides `Entry(z,t)`. Hence

```text
HIGHWAY = {z | exists t, Entry(z,t)}
```

is computably enumerable. The following are equivalent: total membership
decidability; c.e. complement; a total computable upper bound on positive entry
time; and a decidable finite certificate relation complete for negative seeds.
The conversions are the standard search, bounded replay, dovetailing, and
accepting-computation encodings. HC is the universal inclusion of normalized
finite seeds in `HIGHWAY`.

There are reversible finite-word systems with history tracks and growing clocks
that realize total steps, strict history growth, acyclicity, finite branching,
and decidable halting. Reversible universal machines realize the same abstract
properties with undecidable halting. Literal planar left/right geometry is
therefore the distinguishing structure sought by a classification theorem.

## Archive deletion theorem

If a finite discrepancy set is never read after time `T`, first-difference
induction deletes it at `T` while preserving the physical future. The deletion
predicate is semantic: its witness describes the complete future read set.

## Finite-phase tally obstruction

Consider a bounded finite-phase tally with one black bulk cell in every column,
fixed endpoint axis, and exact restoration except extension from `n` to `n+1`.
Row/column parity forces

```text
b_i+b_(i+1) = X^(n+1)(1+c_i+X c_(i+1)).
```

Bounded residues make both sides vanish for unbounded `n`, so
`b_i=b_(i+1)` and `c_(i+1)=X^-1(c_i+1)`. Around a `k`-phase cycle,
`(X^k+1)c_0=1+X+...+X^(k-1)`. Cancelling the geometric sum would give
`(X+1)c_0=1`, impossible in the Laurent domain. Hence this architecture admits
no uniform tally. A successful constructor changes at least one of its
finite-phase, one-cell-per-column, fixed-axis, bounded-residue, or exact-
restoration hypotheses.
