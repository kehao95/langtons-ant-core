# Research state

This file is the compressed research memory of the predecessor repository at
[`045ff9a`](https://github.com/kehao95/langtons-ant/tree/045ff9a3b66a535ab34f2ed2cbf40e5adce5f9ea).
It transfers conclusions and proof strategy, not its implementation or file
structure.

Status words are strict:

- **local** — proved by this repository's current proof cone;
- **source-proven** — closed in the predecessor, but not reconstructed here;
- **source-audited** — supported there by an exact analytic argument or finite
  verifier under a restricted contract;
- **historical** — reported evidence is incomplete;
- **open** — no proof is claimed.

## Architecture

```text
literal LR dynamics
  ├─ finite P104 terminal predicate ──> restricted positive theorems
  └─ complete-history renewal ────────> exact genealogy
                                         │
                     ┌───────────────────┴───────────────────┐
                     │                                       │
            effective compactness                   exact machine compiler
            / finite NO witness                     / non-P104 isolation
                     │                                       │
              membership decidable                  membership undecidable
                     └───────────────────┬───────────────────┘
                                         │
                                  HC still asks whether
                                  every seed is positive
```

The terminal predicate is the positive interface. Renewal is a lossless
re-expression of the original decision problem. Normal forms and invariants
constrain the two final branches; none is itself the missing bridge.

## Result boundary

| Result | Status | Exact boundary |
|---|---|---|
| Blank plane reaches permanent P104 after 9,977 updates | local | Translation and quarter-turn symmetry |
| The only black square lies in the 1,376-cell blank-prefix domain | local | Exact replay of every prefix-hit position, all poses by symmetry |
| Pristine P104 boundary plus one arbitrary black cell | local | 22 affine lanes, 467 finite bases, exact wake/corridor induction |
| Actual 715-cell blank-entry state plus one obstacle on 21 ordinary lanes | local | 447 finite cases and exact historical-wake separation |
| Every initial state with exactly one black square | local | Clean-room finite replay plus all-depth affine wake inductions; predecessor Lean is not imported |
| Guarded obstacle and phase-32 terminal languages | source-audited | Only their complete geometric guards; labels alone are insufficient |
| Clean 1,398-cell blank envelope | local | Decidable sufficient YES witness, never a negative test |
| Prefix-primary two-black family | historical | Transient 914,749-state replay is recoverable; late tables and guard verifier are missing |
| Universal two-black and arbitrary finite support | open | Neither HC nor a counterexample follows from the historical evidence |

The predecessor's universal one-black proof factors through four ideas:

```text
permanent blank P104
  -> pristine P104 plus one arbitrary obstacle
  -> actual 9,977-step blank wake plus one arbitrary obstacle
  -> exhaustion of every time-zero singleton position.
```

Its finite partition used 22 pristine lanes, 21 ordinary historical lanes, one
all-depth phase-72 lane, and the 1,376-position blank prefix. The pristine
all-depth theorem and final prefix exhaustion are now reconstructed locally
without importing certificate tables. The 21 ordinary historical lanes are
also local, and the phase-72 two-way recurrence is rederived from the local
dynamics. Universal one-black is therefore local; the predecessor's Lean proof
remains independent provenance rather than a dependency.

## Exact decision interface

For a normalized finite seed `z`, let `Entry(z,t)` be the decidable permanent
P104 predicate. Define `HIGHWAY = {z | exists t, Entry(z,t)}`. Then:

```text
Level 0: Entry(z,t)       decidable
Level 1: z in HIGHWAY     computably enumerable; decidability open
Level 2: every z is in HIGHWAY (HC)                    open
```

If HC is true, `HIGHWAY` is trivially decidable. If HC is false, membership may
still be a proper decidable language, or it may be a nonrecursive c.e.
language. No theory-relative independence result is known.

The complete-history carrier retains the physical state, clock, every old read
cell, and freshness data. One renewal event is total and computable; on every
nonterminal edge the finite old set grows strictly. The graph is therefore
acyclic, but it need not be well-founded.

The enumeration of `HIGHWAY`, the cutoff/negative-certificate equivalences,
and the generic-abstraction separation theorem are reconstructed locally in
`PROOF.md`. The exact finite blank-interaction oracle used by renewal is also
local. The carrier, finite escape theorem, exact event, divergence genealogy,
and the per-input/global equivalence chains are now reconstructed locally in
one implementation and one proof section. No predecessor certificate schema or
parallel genealogy state was retained.

The local proof establishes the condition-preserving equivalences

```text
z in HIGHWAY
  <=> its deterministic renewal program halts
  <=> its finite-rooted, finitely branching genealogy has finite height.
```

For global truth it also establishes

```text
HC
  <=> every legal finite-old renewal program halts
  <=> the legal renewal relation is well-founded
  <=> its connected-old semantic restriction is well-founded.
```

All four global arrows are local. The connected-old reduction chooses an
existential future tail and is deliberately proved only as a truth-value
equivalence, not an online per-input transformation. The untouched-archive
lemma is local, but recognizing that an archive will never be read is still not
computable without an independent finite guard. Renewal is therefore an exact
presentation, not a simpler algorithm.

Membership decidability is equivalent to any one uniform object:

```text
a computable positive entry or genealogy cutoff;
an enumeration of all negative seeds;
a decidable, sound and complete finite NO-certificate relation.
```

These are characterizations of the missing decider, not consequences of
finite branching, acyclicity, or strict history growth.

Four logical boundaries remain important even when they are not the active
proof step:

- A total all-input generation bound `H_HC(z)` proves HC. A positive cutoff
  `B+(z)` or `G+(z)` need only bound inputs that eventually terminate; a
  negative run reveals itself by crossing the supplied bound. The latter
  decides membership without proving that every answer is positive.
- Reversibility makes the concrete dynamics a computable bijection and makes
  `HIGHWAY` invariant along complete orbits. It supplies neither a basin
  decider nor a computable canonical orbit representative; reversible machines
  can still have undecidable basins of decidable forward-invariant sets.
- Published Langton universality does not close this finite-support problem.
  Finite seeds can evaluate supplied finite circuits, while the known
  unbounded machine simulation uses infinite support. A finite-seed
  self-extension compiler remains a separate open construction.
- An effective-compactness proof must preserve reachable literal roots, be
  uniform and computable from finite data, retain complete history or a proved
  deletion guard, and be both sound and complete. A WQO, pump syntax or
  semantic finite basis without these four properties is only a candidate
  architecture.

## Lossless structural knowledge

The following results have now been reconstructed locally from the literal
step rule and are reusable filters:

- Finite-support orbits correspond exactly to turn words alternating on each
  revisited cell, with finitely many initial-colour defects; five identical
  consecutive turns are impossible.
- Moving the ant to the origin and north gives two exact affine substitutions
  on finite Laurent polynomials over `F_2`, selected by the origin coefficient.
- `heading - number_of_black_cells (mod 4)` is invariant. Thus heading can be
  removed in a fixed sector, but the selector still depends on global
  cardinality.
- Sampling at left-to-right valleys yields only the sixteen words `R^a L^b`,
  `1 <= a,b <= 4`; the remote lamp field remains unbounded.
- Pairing consecutive updates gives an exact diagonal-lattice walk with one
  sign bit and two literal cell toggles per macro; it is lossless, not a finite
  automaton.
- Four monotone direction counts determine displacement. Every same-cell
  return adds exactly `m(1,1,1,1)`, leaving a rank-three quotient and a
  rank-one return fibre.
- Exact symbolic preimages of the P104 terminal set are effectively computable
  at every finite depth. Their ascending union is `HIGHWAY`; no effective
  stabilization theorem is known.
- Checkerboard-axis phase, row/column incidence boundary, and two
  pose-corrected mod-4 charges are conserved. A same-axis macro's net write is
  an even row/column plaquette field.
- Row/column incidence still has unbounded finite information capacity, even
  when old history is connected, so its finite charge is a filter rather than
  a compact state representation.
- The sector invariant forbids a clean colour-restoring time-reversal or clean
  pose-change gadget. Any universal construction must export history, migrate,
  alter bulk state, or carry an unbounded controller.

These formulations remove false degrees of freedom but do not bound the remote
finite store and do not decide P104 membership.

## Dormant exact deductions

Unless explicitly called local, the statements in this section are
**source-audited** predecessor results. They are retained because they constrain
future proofs; their old certificate and test surfaces are not dependencies of
this repository.

### Event accounting

For a renewed event, the full read footprint is a connected lattice walk. The
target old set is the source old set union the strict pre-divergence reads;
post-divergence reads are already old because the first new cell would instead
be the next carrier. The target black set is the source black set XOR the cells
read an odd number of times. Consequently old-component change has an exact
closed-neighbour attachment law, while black components have an exact
birth/death/split/merge ledger rather than a monotone component count.

If `R,L` are white and black reads, `D` the source-live incarnations killed by
the event, and `C` the births still live at its endpoint, then

```text
Theta = R-L = |B_target|-|B_source| = |C|-|D|.
```

This is conservation, not descent. A concrete event can consume one divergence
parent and leave six children, so black count, signed turn, component count and
local branching are not global ranks.

### Genealogy geometry

- Completed parent and child lifetimes satisfy
  `birth(parent)<birth(child)` and `death(parent)<death(child)`. Canonical
  ancestry is proper-interval/FIFO-shaped rather than nested/LIFO, but physical
  query order is not a reliable queue: frame changes, survivors, rebirths and
  predecessor residue can reorder reads.
- If descendants remain inside one already bounded component of the old-set
  complement, their births inject into its finite cells. Along a direct
  descendant chain the pocket area strictly decreases. New pockets can still
  be cut from the unbounded complement, so this is conditional capture rather
  than global well-foundedness.
- If the parent locations of an infinite lineage are bounded, all but finitely
  many selected children are old-white rebirths. After fixing parent, child,
  heading and phase, sources lie on one reverse highway-drift ray with an
  unbounded cycle parameter; their pre-hit words form a nested suffix family,
  growing by exactly 104 reads per cycle.
- In a fixed ray-return class the clean pre-hit state has a fixed active core,
  twelve finite wake rays with a common length parameter, and one rigidly
  translated 702-cell entry cloud. The actual state is this semilinear clean
  part XOR the arbitrary launch black residual; the residual is not deleted.
- After divergence, every carrier in a sufficiently deep fixed ray class
  follows one finite canonical escape path to the same gate. Continuing past
  that gate requires it already belong to source old. History after this gate
  is still uncompressed and may change the frame.
- For any infinite marked genealogy whose productive vertices remain in a
  finite cell set `S`, if `L_n` is the live productive frontier and `r_n` the
  productive children replacing its next parent, then
  `L_(n+1)=L_n-1+r_n` and `sum(r_n-1)<=|S|-L_0`. Productive splitting is
  therefore finite; an infinite bounded remainder eventually transports
  productivity through one child at a time.
- The globally fresh source cell of every event has an exact dichotomy. Its
  first black incarnation either survives as a genealogy child, or a later
  return absorbs it into an Eulerian incidence cycle containing that unique
  fresh edge. An infinite run therefore has infinitely many transmitted source
  marks or infinitely many fresh-edge-rooted cycles. Neither branch yet has an
  unforgeable ownership order.

### Charge, mass and topology

The local incidence charge from `PROOF.md` implies more under guarded recurrent
ray hypotheses: sufficiently remote sources require an external current-black
gate connected to a fixed finite charge token. Infinitely many such gates give
an infinite productive genealogy spine, but the marked gates may remain on
side branches. Distinct gates can share a tether tail, a whole shortest tether
can disappear in one event, and simple birth-time ordering on the tether fails.
Static tether geometry is therefore not fuel.

Signed row/column cut charges also give a global mass bound. If `R0` is the
initial support/pose bounding box and `d` the ant's later `L_infinity` distance
from it, then

```text
|B_t| >= 2 max(d-1,0).
```

Thus every spatially unbounded finite-support trajectory has unbounded black
mass along a subsequence; a bounded black gadget cannot simply translate to
infinity. This does not distinguish productive structure from inert highway
wake.

Black/Tait loops are reversible surgery objects: bridges can be deleted,
cycles split and merge, and previously seen loop identities return. The
monotone object is complete old history, not current black topology. Any useful
topological rank must bind a crossing to time-expanded provenance.

### Finite and guarded leaves

- A shared two-phase finite tally model realizes extension at lengths 2 and 4
  and a bounded probe at lengths 3 and 5. This is a mechanism witness only.
- A local Laurent parity proof rules out a same-axis, exact-restoring,
  one-black-cell-per-column constructor with bounded finite-phase base/cap
  residue. Multi-track, moving, non-restoring and unbounded-control designs
  remain possible.
- A single-parent ray-return experiment covers only cycles `k=0..3`. The two
  observed increments are each 104 updates, signed-turn difference 12 and 12
  target black cells; two equal increments are not an all-depth recurrence.
- The obstacle-chain language has arbitrarily long concrete renewal paths, so
  no finite nonterminal abstraction DAG can cover all renewals. That guarded
  language nevertheless has its own strict fresh-event natural rank; the rank
  has no proved coverage beyond the language.
- Guarded one/two/three-obstacle, sparse-word, rotating-block, obstacle-chain
  and phase-32 families are positive leaves. The sparse phase-32 decoder also
  has exact reset, selector, singleton-orthant and typed-control facts. All
  require their complete guards; labels or quotient edges alone are not
  concrete transitions. More leaves matter globally only with coverage.

## Retained proof interfaces

The predecessor's intermediate work leaves three reusable proof contracts.
They are designs constrained by the exact deductions above, not proved global
theorems.

### Guarded rewrite

A sound corridor rewrite must carry the input frame and active pattern, every
consumed lane slice, all off-lane and backward-history reads with colour and
old/fresh status, a symbolic untouched suffix plus separation proof, exact
replay to a terminal or guarded endpoint, an output split into active/residual
parts, and a separately justified well-founded decrease. A verifier must reject
at the first unencoded read.

The lane word is exact only before first collision. Collision can leave all 22
lanes or run backward through arbitrary wake, so a fixed halo is not closed.
Path-length realizability must accompany quotient states: a Cartesian product
of locally valid fields can invent impossible history intersections or hide a
real one. Every frame-changing scatter must recompute visibility; neither input
order nor incarnation birth order is a global selector.

Even sound local rules need global coverage, suffix preservation, permanent or
guarded residue separation, capture/return to the rule domain, and strict
well-foundedness on every contextual edge.

### Three-way lineage capture

Any proposed proof of connected-old well-foundedness should cover every
hypothetical infinite lineage by the following exhaustive trichotomy:

1. **bounded pocket:** it remains in descendants of an existing bounded pocket
   and consumes finite area;
2. **finite scattering:** bounded parents reduce to a ray-return system with a
   fixed collar, isolated exterior wake, finite normal states and no
   nonterminal recurrent control cycle;
3. **outer ownership:** outward productivity repeatedly consumes a new causal
   gate that cannot be inherited by two infinite descendants or recreated
   without a well-founded payment.

Only the conditional pocket branch is currently closed. The other two clauses
state the missing Langton-specific bridge rather than consequences of generic
finite branching.

### Dynamic ownership

The strongest retained synthesis tracks time-expanded causal ownership, not a
cell, current component or scalar charge. In a bounded rewrite class it may use
finite control plus fixed-dimensional semilinear counters, separating active
counters from inert archive counters. Outside that class it must select a
productive owner frontier and charge each crossing of a monotone old-set
separator to a unique incarnation/cut obligation.

VASS/WSTS or Dickson arguments become relevant only after proving a fixed
counter dimension, exact concrete successor coverage, compatible monotone
simulation, and explicit exemption of certified highway growth. First-hit
selection, XOR cancellation and collision reorder can violate all of these.
An owner record must be computable from a finite renewal/genealogy prefix; it
may not contain semantic predicates such as "has infinitely many productive
descendants."

## Abstractions already ruled out

Do not rebuild any argument that relies only on:

- one fixed-radius local Markov window;
- phase alone, a bounded collar, or a repeated quotient signature as a global
  rank or concrete transition;
- invisibility to the current blank orbit as permanent archive deletion;
- parity or Euler balance without temporal ownership of the residual cells;
- total computable/reversible macros, strict connected history growth,
  acyclicity, finite branching, or a primary/secondary blocker pair;
- ancestry interval order as a complete FIFO store, or birth/input order as a
  global FIFO/LIFO selector;
- finite conserved charge, current black count, or static tether/loop
  topology as a non-cloning budget;
- information depletion, WQO existence or repeated semilinear control without
  exact forward simulation and reachable concrete coverage;
- infinite-support universality, finite circuit evaluation, or a nearby
  one-state-machine theorem as a finite-support P104 classifier.

Explicit decidable and undecidable abstract models satisfy the generic renewal
properties above. Therefore a classification proof must use additional facts
of the literal planar LR walk; this is an abstraction limitation, not a PA/ZFC
independence theorem and not evidence that Langton dynamics is universal.

## Frontier

There are only two classification routes worth promoting:

1. **Effective compactness:** every negative reachable exact renewal run has a
   finite, uniform, history-safe non-P104 certificate. This would decide
   `HIGHWAY` but would not alone prove HC.
2. **Exact compilation:** uniformly compile an undecidable machine into finite
   seeds, proving both halt-to-P104 and nonhalt-to-non-P104. This would make
   membership undecidable and refute HC.

HC itself is equivalent to well-foundedness of every exact renewal run, or to
a total computable all-seed generation bound. Merely naming that bound does not
construct it.

A future result belongs in this repository only if it does at least one of:

- reconstructs a source result as a smaller local proof;
- enlarges a positive family with an exact coverage theorem;
- advances a complete finite NO-certificate language or computable cutoff;
- classifies the exact operational query algebra; or
- supplies one uniform component of the machine compiler.

Another bounded phase, width, obstacle case, or generic halting reformulation
is evidence, not a new architectural layer.
