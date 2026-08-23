# Research state

This is the compressed research memory of the predecessor repository at
[`045ff9a`](https://github.com/kehao95/langtons-ant/tree/045ff9a3b66a535ab34f2ed2cbf40e5adce5f9ea).
It preserves reusable conclusions, failure boundaries and the active proof
interface, not predecessor code, certificates or document topology.

Evidence words are strict:

- **local** — proved by this repository's current proof cone;
- **source-audited** — proved analytically or by an exact scoped verifier in
  the predecessor, but not reconstructed here;
- **historical** — reported evidence is incomplete;
- **open** — no proof is claimed.

## Proof graph

```text
literal LR dynamics
  ├─ decidable P104 terminal ──> guarded positive families
  └─ lossless renewal ─────────> finite-branching genealogy
                                      │
                 ┌────────────────────┴────────────────────┐
                 │                                         │
         effective compactness                    finite-seed compiler
         / complete NO witness                    / non-P104 isolation
                 │                                         │
        membership decidable                    membership undecidable
                 └────────────────────┬────────────────────┘
                                      │
                              HC asks whether every
                              seed is positive
```

The terminal predicate is the positive interface. Renewal is an exact
re-expression of the original problem, not a simpler algorithm. Normal forms
constrain the two classification branches but do not supply the missing bridge.

## Result boundary

| Result | Status | Boundary |
|---|---|---|
| Blank reaches permanent P104 after 9,977 updates | local | Translation and quarter-turn symmetry |
| Every initial state with exactly one black square reaches P104 | local | 1,376 prefix cells; 22 pristine lanes; 21 ordinary historical lanes; all-depth phase 72 |
| Clean 1,398-cell blank envelope implies P104 | local | Sufficient YES predicate only |
| Guarded obstacle, sparse, rotating and phase-32 languages | source-audited | Only with their complete geometric/history guards |
| Prefix-primary two-black family | historical | A 914,749-state transient replay is recoverable; later tables are missing |
| Universal two-black and arbitrary finite support | open | Neither HC nor a counterexample is known |

The local one-black proof factors as

```text
blank P104
  -> pristine P104 plus one obstacle
  -> actual 702-cell historical wake plus one obstacle
  -> every time-zero singleton position.
```

The predecessor Lean theorem is independent provenance, not a dependency.

## Exact decision boundary

For a normalized finite seed `z`, exact replay decides `Entry(z,t)`, permanent
P104 entry at a supplied time. Hence

```text
Level 0: Entry(z,t)                         decidable
Level 1: HIGHWAY = {z | exists t Entry}     computably enumerable; decision open
Level 2: HC = every z is in HIGHWAY         open
```

Complete-history renewal and its genealogy are local and give

```text
z in HIGHWAY
  <=> its deterministic renewal program halts
  <=> its canonical finite-rooted genealogy has finite height.

HC
  <=> every legal finite-old renewal program halts
  <=> the legal renewal relation is well-founded
  <=> its connected-old semantic restriction is well-founded.
```

Membership is decidable exactly when there is a total positive entry or
genealogy cutoff, an enumeration of negative seeds, or one decidable sound and
complete finite `NoCert(z,c)` relation. These characterize the missing object;
they do not construct it.

Four boundaries prevent false shortcuts:

- An all-input generation bound `H_HC(z)` proves HC. A positive cutoff `G+(z)`
  only bounds terminating inputs and can decide membership even when `HIGHWAY`
  is a proper subset.
- Reversibility gives a computable bijection and orbit-invariant basin, not a
  basin decider or computable canonical orbit representative.
- Known finite-support constructions evaluate finite circuits; the unbounded
  machine simulation uses infinite support. Neither proves finite-support P104
  membership undecidable.
- Effective compactness must be uniform on reachable literal roots, preserve
  complete history or a proved deletion guard, and be sound and complete. A
  semantic basis, WQO or pump syntax alone is insufficient.

## Lossless structural lenses

These local results remove false degrees of freedom without bounding the remote
finite store.

| Lens | Exact information retained | Limitation |
|---|---|---|
| Turn word | Per-cell visits alternate; only finitely many first `L` defects; no five equal turns | Still an unbounded word/store |
| Cardinality sector | `heading-|black| mod 4` is invariant | The move selector still uses global cardinality |
| Head-normalized Laurent map | Two exact affine substitutions selected by the origin coefficient | Adaptive branch remains nonlinear |
| Valley section | Sixteen words `R^aL^b`, `1<=a,b<=4`, with bounded return | Remote lamps remain unbounded |
| Paired steps | Diagonal walk with one sign and two literal toggles | Not a finite automaton |
| Direction counts | Same-cell returns add `m(1,1,1,1)` | Leaves a rank-one return fibre and independent cell bits |
| Endpoint charges | Checkerboard axis, incidence boundary and two mod-4 charges are conserved; same-axis writes are plaquette fields | Filters endpoints but supplies no descent |
| Symbolic preimages | Every finite-depth P104 preimage is computable | No effective stabilization of their union is known |

The sector invariant also forbids a clean colour-restoring reversal or
pose-change gadget. Any exact compiler must export history, migrate, change
bulk state or carry an unbounded controller.

## What the dormant deductions imply

Unless called local, the claims below are **source-audited**. Their combined
value is the synthesis, not the old verifier inventory.

### One event has an exact ledger

A renewed event has a connected read footprint. Its target old set is source
old union the strict pre-divergence reads; post-divergence reads are already old
because the first new cell becomes the target carrier. Target black is source
black XOR the cells read an odd number of times. Old components obey an exact
attachment law, while black components can be born, killed, split and merged.

If `R,L` count white and black reads, `D` source-live deaths and `C` endpoint-live
births, then

```text
R-L = |B_target|-|B_source| = |C|-|D|.
```

A real edge can replace one divergence parent by six children. Counts,
components and signed turn are therefore ledgers, not ranks.

### The unresolved state has three reservoirs

Across the proved recurrent classes, concrete state separates into:

1. a finite **active core** controlling the immediate collision;
2. an affine/semilinear **wake** described by finitely many translated pieces
   and ray-length counters;
3. arbitrary finite **historical residual** carried by the launch state.

For bounded-parent ray-return, the clean pre-hit part is particularly sharp: a
fixed active core, twelve wake rays with one length parameter, and one rigidly
translated 702-cell entry cloud. The actual pre-hit state is this clean part
XOR the launch residual. A sufficiently deep fixed class follows one finite
escape path to a stable old gate.

The first two reservoirs are already finite-control/Presburger-shaped. The
remaining entropy is whether the arbitrary residual, after a frame change, can
be queried again. Current-orbit invisibility cannot delete it: an exact trace
keeps one off-orbit black cell inert for 135 renewal edges before it becomes the
next divergence.

### Infinite productivity has two transport regimes

Every infinite lineage has bounded or unbounded parent positions.

- In the **bounded** regime, all but finitely many selected children are
  old-white rebirths. After fixing parent, child, heading and phase, sources lie
  on one reverse P104 drift ray and pre-hit words form nested suffixes growing
  by 104 reads per cycle. If productive vertices stay in a finite cell set `S`,
  their live frontier satisfies

  ```text
  L_(n+1)=L_n-1+r_n,
  sum(r_n-1) <= |S|-L_0.
  ```

  Productive splitting is finite; any infinite remainder eventually transports
  productivity through one child at a time.
- In the **unbounded** regime, spatial escape alone is not causal progress.
  Signed cut charges give `|B_t| >= 2 max(d-1,0)` at distance `d` beyond the
  initial box, so a bounded black gadget cannot translate forever. But P104
  itself creates unbounded inert wake. A proof must select the structure that
  owns future productivity, not merely count remote black cells.

Bounded pockets provide one genuine local fuel: births remaining in descendants
of an existing bounded old-complement component inject into its finite cells,
and direct descendant pocket area decreases. New pockets may still be cut from
the unbounded complement, so this is capture, not global coverage.

### Static topology must become causal ownership

The first fresh source incarnation of each event either survives as a genealogy
child or is absorbed on a later return into an Eulerian incidence cycle carrying
that unique fresh edge. Thus an infinite run has infinitely many transmitted
source marks or infinitely many fresh-edge-rooted cycles.

Incidence charge forces remote recurrent sources to have current-black gates
tethered to finite charge tokens, and infinitely many marked gates yield a
productive genealogy spine. Yet marks may remain on side branches; gates can
share tether tails; a whole tether can disappear; black/Tait cycles split,
merge and recur. Static topology is not non-cloning fuel.

The high-level conclusion is the main retained insight:

> Any well-founded measure must assign each future productivity obligation to a
> finite, time-expanded causal owner and prove that ownership is transferred to
> at most one infinite descendant or pays an unrecoverable resource.

## Proof contracts worth retaining

### Guarded rewrite

A sound rewrite must encode the input frame and active pattern, every consumed
slice, all off-lane/backward reads with colour and old/fresh status, an untouched
suffix with a separation proof, exact replay to a terminal or guarded endpoint,
an active/residual output decomposition, and an independently justified
decrease. It rejects the first unencoded read.

The 22-lane word is exact only before first collision. A collision can leave the
lanes or run backward through arbitrary wake. Quotient states therefore need a
path-realizability invariant, and visibility must be recomputed after every
frame change. Sound local rules still require global coverage, suffix and
residue preservation, capture/return and well-foundedness.

### Complete lineage capture

A positive HC proof through renewal should cover every hypothetical infinite
lineage by:

1. **bounded pocket descent** — finite area pays for captured descendants;
2. **finite scattering** — bounded ray-return has a fixed collar, isolated
   residual, finitely many normal states and no nonterminal recurrent cycle;
3. **outer ownership** — outward productivity consumes a causal gate that
   cannot finance two infinite descendants or be recreated for free.

Only conditional pocket descent is closed. Finite scattering and outer
ownership are concrete forms of the missing Langton-specific theorem.

### Dynamic ownership

Within a bounded rewrite class, a candidate may use finite control and
fixed-dimensional semilinear counters, separating active from archive counters.
Outside it, a monotone old-set separator must charge each productive crossing
to a unique time-expanded incarnation or causal cut.

VASS/WSTS or Dickson arguments apply only after proving fixed dimension, exact
successor coverage, compatible monotonicity and a certified-highway exemption.
First-hit selection, XOR cancellation and collision reordering can break these
hypotheses. No runtime owner record may contain future-semantic fields such as
"has infinitely many productive descendants."

## Scoped evidence retained

- Guarded one/two/three-obstacle, separated/sparse words, rotating blocks,
  obstacle chains and phase-32 contexts are source-audited positive leaves.
  Reset, selector, singleton-orthant and typed-control facts are dispatch lemmas
  only under their full context guards.
- The obstacle-chain language has arbitrarily long renewal paths, refuting a
  finite nonterminal DAG, while its own guarded events have a natural rank.
- A two-phase tally realizes finite extension at lengths 2 and 4 and probes 3
  and 5. It is a mechanism witness. A local Laurent argument separately rules
  out bounded finite-phase, exact-restoring, one-black-per-column tallies.
- A single-parent ray-return experiment covers only cycles `0..3`; its two
  equal 104-update/12-turn/12-black increments are not an all-depth recurrence.

## Abstractions already refuted

Do not rebuild a proof based only on:

- a fixed-radius local window, phase, bounded collar or repeated quotient
  signature;
- current-blank-orbit invisibility as permanent archive deletion;
- black count, finite charge, Euler balance, static tether or loop topology;
- total/reversible steps, strict connected history growth, acyclicity, finite
  roots/branching or a primary/secondary blocker pair;
- ancestry interval order as a queue, or birth/input order as FIFO/LIFO;
- information depletion, WQO existence or semilinear control without exact
  concrete forward simulation;
- finite circuit evaluation, infinite-support universality or a nearby
  one-state-machine theorem as a finite-support classifier.

Explicit decidable and undecidable abstract systems satisfy the generic renewal
properties. This is an abstraction separation result, not PA/ZFC independence
and not evidence that literal Langton dynamics is universal.

## Frontier

Only two classification routes remain worth promotion:

1. **Effective compactness:** every negative reachable renewal run exposes one
   finite, uniform, history-safe `NoCert`. This decides membership but does not
   alone prove HC.
2. **Exact compilation:** a uniform finite-seed machine compiler proves both
   halt-to-P104 and nonhalt-to-non-P104. This makes membership undecidable and
   refutes HC.

A future result belongs here only if it reconstructs a source theorem more
compactly, enlarges a positive family with coverage, advances a complete
negative certificate/cutoff, classifies the operational query algebra, or
supplies a uniform compiler component. Another bounded phase, width, obstacle
case or generic halting reformulation is evidence, not a new architectural
layer.
