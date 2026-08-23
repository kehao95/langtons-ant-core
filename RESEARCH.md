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
local. The carrier, next-fresh totality, genealogy, and their two equivalence
chains remain source-audited until those objects are rebuilt here.

The predecessor establishes the condition-preserving equivalences

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

The last reduction chooses an existential future tail. It is not an online
per-input transformation. The underlying untouched-archive lemma is now proved
locally, but recognizing that an archive will never be read is still not
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

## Finite evidence and narrow obstructions

- A shared two-phase finite tally model realizes extension at lengths 2 and 4
  and a bounded probe at lengths 3 and 5. This is a mechanism witness only.
- A locally reconstructed Laurent parity argument rules out a same-axis, exact-restoring,
  one-black-cell-per-column constructor with bounded finite-phase base/cap
  residue. It does not rule out multi-track, moving, non-restoring, or
  unbounded-controller constructions.
- A single-parent ray-return experiment covers only cycles `k=0..3`; the two
  stable differences observed are not an all-depth recurrence.
- Exact renewal gate, tether, collision, pocket and local-reduction results
  narrow guarded carriers but supply neither a global rank nor well-foundedness.
- Guarded one/two/three-obstacle, sparse-word, rotating-block, obstacle-chain,
  and phase-32 families are positive leaves. More leaves matter globally only
  when a coverage theorem assembles them.

## Abstractions already ruled out

Do not rebuild any argument that relies only on:

- one fixed-radius local Markov window;
- phase alone, a bounded collar, or a repeated quotient signature as a global
  rank or concrete transition;
- invisibility to the current blank orbit as permanent archive deletion;
- parity or Euler balance without temporal ownership of the residual cells;
- total computable/reversible macros, strict connected history growth,
  acyclicity, finite branching, or a primary/secondary blocker pair;
- FIFO, LIFO, birth order, or input order as a global query discipline.

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
