# Highway Conjecture research program

The program classifies finite-support Langton-ant seeds through two exact
interfaces: permanent P104 entry and complete-history renewal. Current local
proofs establish the blank and universal one-black families. Archived theorem
and experiment provenance is anchored at
[`045ff9a`](https://github.com/kehao95/langtons-ant/tree/045ff9a3b66a535ab34f2ed2cbf40e5adce5f9ea).

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
                         classify every finite seed
```

The terminal predicate supplies positive certificates. Renewal transports the
same decision problem into a deterministic finite-rooted genealogy. Structural
normal forms organize the two classification constructions.

## Established base

Exact local replay and induction prove:

- blank entry into permanent P104 after 9,977 updates;
- permanent P104 for every initial state with one black square;
- the clean 1,398-cell envelope criterion;
- exact first interaction with any finite set along the blank orbit;
- renewal termination exactly when the physical state reaches P104;
- renewal termination exactly when the canonical genealogy has finite height.

The one-black proof factors as

```text
blank P104
  -> pristine P104 plus one obstacle
  -> actual 702-cell historical wake plus one obstacle
  -> every time-zero singleton position.
```

The archived program supplies guarded one-, two-, and three-obstacle languages,
separated and sparse words, rotating blocks, obstacle chains, and phase-32
contexts with their recorded geometry and history predicates. It also records
a 914,749-state prefix-primary two-black transient. These objects provide
reusable hypotheses, mechanisms, and finite traces for reconstruction.

## Decision formulation

For a normalized finite seed `z`, exact replay decides `Entry(z,t)`, permanent
P104 entry at a supplied time. Define

```text
HIGHWAY = {z | exists t, Entry(z,t)}
HC      = forall normalized finite seed z, z in HIGHWAY.
```

`HIGHWAY` is computably enumerable. Complete-history renewal gives

```text
z in HIGHWAY
  <=> its deterministic renewal program halts
  <=> its canonical finite-rooted genealogy has finite height.

HC
  <=> every legal finite-old renewal program halts
  <=> the legal renewal relation is well-founded
  <=> the connected-old renewal relation is well-founded.
```

Membership decidability is equivalent to each of the following constructions:

1. a total computable entry-time bound for positive seeds;
2. an enumeration of the complement of `HIGHWAY`;
3. a decidable finite relation `NoCert(z,c)` that is sound and complete for
   seeds outside `HIGHWAY`.

A proof of HC may instead construct a total entry-time bound on every finite
seed. A compiler route constructs finite seeds whose P104 behavior represents
machine halting. Both routes act on literal reachable states and complete
physical history.

## Structural coordinates

| Coordinate | Exact theorem | State carried forward |
|---|---|---|
| Turn word | Per-cell visits alternate; equal-turn runs have length at most four | Finite black support attached to the word |
| Cardinality sector | `heading-|black| mod 4` is invariant | Global cardinality selects displacement |
| Head-normalized Laurent map | Two affine substitutions selected by the origin coefficient | Adaptive branch coefficient |
| Valley section | Sixteen words `R^aL^b`, `1<=a,b<=4`, with return at most eight | Remote finite lamps |
| Paired steps | Diagonal walk with one sign and two literal toggles | Sign and finite lamp field |
| Direction counts | Same-cell returns add `m(1,1,1,1)` | Rank-one return fibre and cell bits |
| Endpoint charges | Checkerboard-axis, incidence, and two mod-4 charges are conserved | Time-expanded causal ownership |
| Symbolic preimages | Every finite-depth P104 preimage is computable | Increasing depth parameter |

The sector invariant forces every colour-restoring pose-change construction to
export history, migrate, change bulk state, or carry an unbounded controller.
Endpoint charges make every same-axis net write a plaquette field. Together
these coordinates reduce candidate constructions to explicit state variables.

## Renewal event ledger

A renewed event has a connected read footprint. Its target old set is the
source old set union the strict pre-divergence reads; post-divergence reads are
already old because the first new cell becomes the target carrier. Target black
is source black XOR the cells read an odd number of times. Old components obey
an attachment law, while black components may be born, killed, split, or
merged.

If `R,L` count white and black reads, `D` source-live deaths, and `C`
endpoint-live births, then

```text
R-L = |B_target|-|B_source| = |C|-|D|.
```

A concrete edge replaces one divergence parent by six children. Counts,
components, and signed turn therefore form an exact conservation ledger. A
well-founded measure additionally assigns the future productivity represented
by those children.

## Three state reservoirs

Across the recurrent classes, concrete state separates into:

1. a finite **active core** controlling the immediate collision;
2. an affine or semilinear **wake** represented by translated pieces and ray
   counters;
3. a finite **historical residual** carried by the launch state.

For bounded-parent ray-return, the clean pre-hit component consists of a fixed
active core, twelve wake rays with one length parameter, and one translated
702-cell entry cloud. The physical state is this component XOR the launch
residual. A sufficiently deep fixed class follows one finite escape path to a
stable old gate.

The active core and wake already admit finite-control and Presburger
coordinates. The historical residual remains operational across frame changes:
an exact trace carries one off-orbit black cell inert for 135 renewal edges and
then reads it as the next divergence. A complete abstraction therefore carries
the residual or a finite separation certificate for its future queries.

## Productivity transport

Every infinite lineage has bounded or unbounded parent positions.

### Bounded transport

After finitely many events, selected children are old-white rebirths. Fixing
parent, child, heading, and phase places sources on one reverse P104 drift ray;
their pre-hit words form nested suffixes growing by 104 reads per cycle. If
productive vertices stay in a finite cell set `S`, their live frontier obeys

```text
L_(n+1)=L_n-1+r_n,
sum(r_n-1) <= |S|-L_0.
```

Productive splitting is finite, and an infinite tail transports productivity
through one child at each event. Within a bounded old-complement pocket, births
remaining in descendant pockets inject into its finite cells and direct
descendant area decreases.

### Unbounded transport

Signed cut charges give `|B_t| >= 2 max(d-1,0)` at distance `d` beyond the
initial box. Long-range transport therefore carries growing black support.
P104 itself produces an unbounded inert wake. Productive transport is therefore
identified by causal ownership, with distance and black count retained as
coordinates.

The first fresh source incarnation of each event either survives as a genealogy
child or is absorbed on a later return into an Eulerian incidence cycle carrying
its unique fresh edge. Hence every infinite run supplies infinitely many
transmitted source marks or infinitely many fresh-edge-rooted cycles. Incidence
charge tethers remote recurrent black gates to finite charge tokens, and
infinitely many marked gates yield a productive genealogy spine.

These facts point to the central invariant:

> Assign each future productivity obligation to a finite, time-expanded causal
> owner. Every event transfers that owner to one infinite descendant or spends
> an unrecoverable finite resource.

## Candidate proof architectures

### Guarded rewrite

A guarded rewrite records the input frame and active pattern, every consumed
slice, off-lane and backward reads with colour and old/fresh status, an untouched
suffix with a separation witness, exact replay to a terminal or guarded
endpoint, an active/residual output decomposition, and an independently
justified decrease. The first unencoded read terminates the rule application.

The 22-lane word describes the orbit through first collision. Subsequent rules
carry path realizability, recompute visibility after frame changes, preserve
suffix and residue, and connect every guarded endpoint to capture, return, or a
well-founded successor.

### Complete lineage capture

A renewal proof of HC decomposes every infinite lineage into three mechanisms:

1. **bounded pocket descent** — finite area pays for captured descendants;
2. **finite scattering** — bounded ray-return has a fixed collar, isolated
   residual, finitely many normal states, and terminal recurrent classes;
3. **outer ownership** — outward productivity consumes a causal gate whose
   ownership follows one descendant.

Bounded pocket descent supplies the local decrease. Finite scattering and
outer ownership are the two construction targets that connect it to a global
well-founded measure.

### Dynamic ownership

Within a bounded rewrite class, finite control and fixed-dimensional semilinear
counters separate active and archive state. Across classes, a monotone old-set
separator charges each productive crossing to a unique time-expanded
incarnation or causal cut.

A VASS, WSTS, or Dickson implementation establishes fixed dimension, exact
successor coverage, compatible monotonicity, and a certified-highway terminal
class. Runtime owner records use event-local data: incarnation, source mark,
cut, transfer, and expenditure.

## Archived mechanism witnesses

- Guarded obstacle, sparse-word, rotating-block, obstacle-chain, and phase-32
  constructions supply exact positive leaves under their recorded input
  predicates.
- The obstacle-chain language contains arbitrarily long renewal paths and a
  natural rank on its guarded events.
- A two-phase tally realizes finite extension at lengths 2 and 4 and has probes
  at 3 and 5. The Laurent obstruction in `PROOF.md` classifies the bounded
  finite-phase, exact-restoring, one-black-per-column architecture.
- A single-parent ray-return trace at cycles `0..3` records two consecutive
  increments of 104 updates, 12 turns, and 12 black cells.

## Abstraction separation

Explicit decidable and undecidable systems both realize reversible total steps,
strict connected-history growth, acyclicity, finite roots, and finite branching.
Consequently a Langton-specific classifier contains additional literal
geometry. The existing countermodels isolate the data it carries:

- spatial memory extending beyond a fixed-radius window or bounded collar;
- an operational separation witness for archived cells;
- causal ownership refining black count, charges, Euler balance, and static
  tether topology;
- event semantics refining generic renewal growth and blocker bookkeeping;
- concrete forward simulation accompanying WQO or semilinear coordinates;
- finite-support compilation accompanying any universality construction.

These are constructive requirements for the next abstraction: each names data
that its successor relation consumes.

## Frontier

Two exact constructions classify `HIGHWAY`:

1. **Effective compactness:** construct a finite, uniform, history-safe
   `NoCert(z,c)` for every reachable seed outside `HIGHWAY`.
2. **Exact compilation:** construct a uniform finite seed for each machine and
   prove halt-to-P104 together with nonhalt-to-non-P104.

The renewal route advances by proving finite scattering and outer causal
ownership. The compiler route advances by implementing one finite-support
state transition with exact restoration of its reusable control interface.
