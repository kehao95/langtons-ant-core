# Preprint Outline: Universal One-Black Theorem

> **Narrative structure locked.** This outline records the agreed three-part
> structure: proof architecture, literature and academic positioning, and the
> section-by-section preprint plan. Claims may be corrected or qualified when
> evidence requires it, but the narrative and chapter order should not be
> changed without explicit agreement.

## I. Proof Architecture

The proof follows the layered architecture

> geometric normalization → finite-prefix coupling → entry-channel
> decomposition → single-defect scattering theory (ordinary-channel induction
> plus an affine reverse-channel collision) → Lean 4 assembly.

```text
        arbitrary one-black initial state s
        (arbitrary black cell, ant position, and heading)
                              │
                 [1. Symmetry normalization]
                              ▼
        canonical pose: ant at (0,0), North, black cell q ∈ ℤ²
                              │
                 [2. Blank 9,977-step prefix]
                              │
            ┌─────────────────┴─────────────────┐
            ▼                                   ▼
   Case A: q ∈ Prefix                    Case B: q ∉ Prefix
   (1,376 lattice cells)                 (q remains unread)
            │                                   │
   [finite exact replay]              [first-difference coupling]
            │                                   │
            │                          state E plus defect q
            │                          at update 9,977
            │                                   │
            │                    [3. Four-way entry geometry]
            │                                   │
            │          ┌────────────┬────────────┴───────────┬────────────┐
            │          ▼            ▼                        ▼            ▼
            │     already black   27 active-white       never read    22 frontier
            │       in E          support cells           again        channels
            │          │            │                        │        q=h+d·v, d≥1
            │          │            │                        │            │
            │          │            │                        │   [4. Scattering]
            │          │            │                        │            │
            │          │            │                        │    ┌───────┴───────┐
            │          │            │                        │    ▼               ▼
            │          │            │                        │ 21 ordinary   1 exceptional
            │          │            │                        │  channels     reverse channel
            │          │            │                        │    │               │
            └──────────┴────────────┴────────────────────────┴────┴───────────────┘
                                           ▼
                              permanent standard P104 highway
```

### 1. Canonical Pose and Baseline P104

- **Pose equivariance.** The dynamics commutes with translations in `ℤ²` and
  quarter-turn rotations in `ℤ/4ℤ`. Every exactly-one-black state can therefore
  be normalized to an ant at `(0,0)`, heading north, with its black cell at an
  arbitrary point `q ∈ ℤ²`.
- **Blank orbit and permanent highway.** From the blank plane, the ant reaches
  the entry state `E` after 9,977 updates, at `(-15,10)` heading west. The next
  104 updates use a 40-cell support `S`, restore the heading, and translate the
  active state by `v=(-2,-2)`. Ray-separation checks prove that the XOR wake
  `W` left by consecutive blocks never obstructs a later translated support,
  so induction makes the P104 behavior permanent.

### 2. Prefix Hit versus Untouched Coupling

- The first 9,977 updates of the blank orbit read 1,376 distinct cells.
- **Prefix branch.** If `q` is one of those cells, exact finite replay in
  `PrefixData.lean` and `PrefixLeaf.lean` supplies a terminal P104 witness.
- **Untouched branch.** If `q` is absent from the prefix, first-difference
  induction proves that the singleton orbit agrees exactly with the blank
  orbit through update 9,977, where its state is precisely `blacken(q,E)`.

### 3. Entry Geometry and the 22 Frontier Channels

At state `E`, the defect location `q` belongs to exactly one of four classes.

1. **Already black.** It is one of the 715 black cells of `E`; blackening it
   changes nothing.
2. **Active-support white.** It is one of the 27 white cells in the 40-cell
   support; these are finite direct cases.
3. **Geometrically separated.** It satisfies

   ```text
   q ∉ ⋃_{k≥0} (S + k v).
   ```

   The permanent blank highway never reads it.
4. **Frontier channel.** Define

   ```text
   H = {s ∈ S | s - v ∉ S}.
   ```

   Exact geometry gives `|H|=22`, and every future-read defect has a unique
   representation `q=h+d·v` with `h∈H` and `d≥1`.

### 4. Single-Defect Scattering Spectrum

The 22 affine channels admit an exhaustive classification formalized by
`Scattering.Classification`.

- **Twenty-one ordinary channels.** On a pristine P104 boundary, each channel
  becomes inductive beyond a finite depth `P_h`; its XOR wake is disjoint from
  every later read and output corridor. In the physical entry state `E`, a
  fixed 702-cell historical wake `H_E` remains. A channel-specific geometric
  cutoff `A_h` separates this history from the scattering footprint. Depths
  `1≤d<A_h` are checked directly, and depths `d≥A_h` couple to the pristine
  family.
- **One exceptional reverse channel.** Its head is
  `h₇₂=base.pos+(-2,-8)`. At pristine depth 11 the scattering produces an
  exact reverse P104 highway with drift `-v=(2,2)`. With the physical history
  restored, the affine collision family begins at actual depth 15; depths 1
  through 14 are direct cases. For actual depth `15+n`, the reverse highway
  returns to the historical wake according to

  ```text
  t_hit(n) = t_hit(0) + 208 n
  ```

  and first hits the fixed cell `(20,-22)`. The depth-15 collision undergoes a
  7,994-update transient before entering forward P104. XOR layer-archive
  induction transfers that post-hit computation to every greater depth.

## II. Literature Background and Academic Positioning

| Work | Date / authors | Main contribution | Relation to this work |
|---|---|---|---|
| Original model | 1986, C. G. Langton | Introduced the two-state two-dimensional ant and reported its emergent transition from irregular behavior to a highway. | Origin of the problem. |
| Early unboundedness result | Original source and the common “Cohen--Kong” attribution require a primary-source audit and must not be conflated with Gale et al. (1995). | Establishes that the relevant ant trajectory cannot remain confined to a finite region. | Unboundedness does not imply entry into a particular P104 orbit. |
| Lorentz lattice gases | 1992/1994, Bunimovich and Troubetzkoy | Studied scattering dynamics and topological properties of particles in reflector or obstacle arrays. | Provides a broader lattice-scattering perspective. |
| Complexity and universality | 2002, Gajardo, Moreira, and Goles | Built Boolean circuits with finite-support inputs and proved P-hardness; universality and undecidability use an infinite but finitely described background. | Shows computational complexity without resolving the finite-support Highway Conjecture. |
| Highway experiments and generalized ants | Computational literature, including Gajardo, Lutfalla, and Rao (2024) | Reports extensive experiments on finite configurations and systematic results about generalized-ant highways. | The audited sources have not yet revealed a theorem covering every exactly-one-black initial state, but priority remains subject to a complete literature audit. |
| This work | 2026, formal mathematics / cellular automata | Proves that the complete natural exactly-one-black family reaches standard P104, introduces the frontier-channel decomposition and `21+1` scattering classification, and closes the result in Lean 4. | Covers arbitrary relative defect position and arbitrary ant pose. Any priority claim for this exact scope remains conditional on the literature audit. |

### Academic Value Propositions

1. **A complete natural configuration family.** The theorem covers every
   exactly-one-black state, with no bound on the black-cell coordinate, ant
   position, or heading. “First” does not enter the title or abstract before
   the primary-source audit is complete.
2. **A dynamical mechanism.** The `21+1` scattering split, and especially the
   reverse highway and affine historical-hit law of `h₇₂`, expose rigid
   algebraic and geometric structure inside an apparently irregular collision.
3. **Computer-assisted proof in Lean 4.** The infinite reductions, exhaustive
   classifications, inductions, and certificate-soundness arguments are
   expressed in Lean. Three closed finite reports are evaluated by
   `native_decide`. Verification does not depend on generation-time external
   search, but native evaluation extends the trusted computing base to the
   Lean compiler, runtime, and code-generation backend; the result must not be
   described as kernel-only or axiom-free.

## III. Preprint Structure and Drafting Plan

Provisional arXiv categories are `math.DS`, `cs.FL`, `cs.LO`, and `nlin.CG`.
Possible later venues include *Experimental Mathematics*, *Journal of Cellular
Automata*, *Discrete Applied Mathematics*, ITP, and CPP. Category and venue fit
must be checked again before submission.

### Working title

**Every One-Black-Cell Langton Ant Reaches the Period-104 Highway: A
Lean-Checked Proof**

### Section-by-Section Plan

#### Abstract (approximately 200--250 words)

- **Context.** Introduce Langton's ant and the finite-support Highway
  Conjecture, including the diagonal period-104 highway with displacement
  `(-2,-2)` per period in the paper's convention.
- **Gap.** Earlier unboundedness results do not imply entry into P104. The
  audited literature has not yet revealed a proof for every exactly-one-black
  state; any final priority language awaits the complete audit.
- **Result.** State that every exactly-one-black configuration on `ℤ²`, with
  arbitrary ant position and heading, reaches standard permanent P104.
- **Method.** Summarize the 22 affine frontier channels, the 21 ordinary
  scattering families, and the exceptional reverse-highway family with its
  affine hit law.
- **Formalization.** State that the infinite proof and certificate soundness
  are formalized in Lean 4, with closed finite reports checked using
  `native_decide` and no generation-time search in proof checking.

#### 1. Introduction

- **1.1 The Highway Phenomenon.** Describe the blank-plane progression from
  early symmetry through an irregular transient to the certified entry at
  update 9,977.
- **1.2 The General Conjecture and the Unboundedness Barrier.** Review early
  unboundedness and the complexity/universality results, explaining why neither
  yields P104 and why long-range history is the central obstacle. Keep the
  finite-support and infinite-support input contracts separate.
- **1.3 Main Contribution.** State

  ```text
  ∀ s ∈ State, ExactlyOneBlack(s) → ReachesP104(s).
  ```

- **1.4 Proof Strategy.** Preview normalization, the 9,977-step first-contact
  split, 22 affine channels, pristine scattering, the 21 physical-history
  channels, phase-72 backscattering, and universal assembly.
- **1.5 Contributions.** Claim only the complete one-black theorem, exhaustive
  channel decomposition, all-depth `21+1` classification, and Lean-checked
  artifact currently supported by the repository.
- **1.6 Paper Organization.** Map the sections to the mathematical and Lean
  dependency graph.

#### 2. Dynamics, Symmetries, and the Main Theorem

- **2.1 Formal Dynamics.** Define
  `s=(grid : ℤ²→𝔹, pos∈ℤ², dir∈{N,E,S,W})` and the read--turn--flip--move
  transition under the pre-update time convention.
- **2.2 Symmetries.** Establish that translations `shift_v` and quarter-turn
  rotations `rot_θ` commute with `step`, and normalize every one-black state to
  `pos=(0,0)`, `dir=North`, `black={q}`.
- **2.3 Standard P104.** Define the standard P104 reference trace, translated
  and rotated phase agreement, `PermanentP104`, and `ReachesP104`. Emphasize
  permanent agreement rather than finite-window resemblance.
- **2.4 Main Theorem.** State the canonical and arbitrary-pose forms and fix all
  conventions used later.

#### 3. The Blank Baseline and First-Contact Reduction

- **3.1 Exact Blank Replay.** Set `N₀=9,977` and
  `E=run(9977,white)`.
- **3.2 Invariant P104 Support and Wake.** Give `p=104`, `v=(-2,-2)`,
  `|S|=40`, and prove `W∩(S+kv)=∅` for `k≥1`, yielding permanent P104 by
  induction.
- **3.3 Prefix-Hit Partition.** Define
  `Prefix={p∈ℤ² | ∃t<9977, pos(t)=p}`, prove `|Prefix|=1,376`, close its finite
  cases, and prove that every `q∉Prefix` yields `blacken(q,E)` at entry.

#### 4. Frontier Channel Decomposition

- **4.1 Support Geometry at Entry.** Classify `q` as already black,
  active-support white, geometrically separated, or future-interacting.
- **4.2 The 22 Frontier Heads.** Define `H={s∈S | s-v∉S}`, prove
  `|H|=22`, and establish the bijection between future-interacting untouched
  cells and `(h,d)∈H×ℤ⁺`.

#### 5. Pristine Single-Defect Scattering

- **5.1 Pristine Boundary Problem.** Remove the 702-cell historical wake and
  study one future defect against the active P104 boundary.
- **5.2 Finite Channel Anchors.** Define a stable anchor depth `P_h` for every
  channel and give exact terminal witnesses for its shallow band and anchor.
- **5.3 Translated Normal Form.** Prove that `n` clean blocks produce only

  ```text
  ⊕_{i=0}^{n-1} (W + i v),
  ```

  together with exact translated-footprint and accumulated-archive forms.
- **5.4 All-Depth Pristine Induction.** Use ray and corridor separation to
  prove that the archive is never read and one checked recurrence closes all
  depths on all 22 channels.

#### 6. Ordinary Scattering with the Actual Entry History

- **6.1 Restoring the Historical Wake.** Restore the 715 black cells of `E`:
  13 in the active P104 pattern and 702 in the historical wake `H_E`.
- **6.2 The 21 Ordinary Channels.** Define the channel criterion and geometric
  cutoff `A_h` separating history from the entire scattering footprint and
  terminal corridor.
- **6.3 Shallow Direct Band.** Close `1≤d<A_h` by exact replay.
- **6.4 Deep Coupling to the Pristine Family.** For `d≥A_h`, prove equality of
  the relevant read traces with the translated pristine family and apply
  untouched-region coupling.
- **6.5 Ordinary-Channel Theorem.** Assemble the shallow and deep bands for all
  21 ordinary channels.

#### 7. Exceptional Phase-72 Backscattering

- **7.1 Failure of Ordinary Separation.** Explain why
  `h₇₂=pos_E+(-2,-8)` cannot use the ordinary history-separation mechanism.
- **7.2 Reverse P104 Generation.** Prove that pristine depth 11 generates
  reverse P104 with drift `-v=(2,2)`. The physical affine family starts at
  actual depth 15; depths 1--14 are direct cases.
- **7.3 Exact Historical Hit.** Prove

  ```text
  t_hit(n) = t_hit(0) + 208 n,    pos_hit = (20,-22).
  ```

- **7.4 Post-Hit Computation.** Show that the depth-15 collision reaches
  forward permanent P104 after 7,994 updates.
- **7.5 XOR Layer-Archive Induction.** Prove that the additional layer at each
  greater depth misses both the fixed post-hit trace and its terminal corridor.

#### 8. Universal Assembly

- **8.1 Scattering Classification.** Combine the 21 ordinary-channel theorem
  and the phase-72 theorem into the 22-channel classification.
- **8.2 Entry-State Exhaustion.** Combine scattering with the four-way entry
  geometry to prove `blacken(q,E)` reaches P104 for every `q∈ℤ²`.
- **8.3 Time-Zero Dichotomy.** Combine the 1,376 prefix cases with untouched
  coupling to prove every canonical one-black initial state reaches P104.
- **8.4 Restoring Arbitrary Pose.** Transport the canonical theorem by
  translation and quarter-turn rotation.
- **8.5 Final Statement.** Present the mathematical theorem beside the short
  declaration `OneBlack.universal_one_black`.

#### 9. Lean Formalization and Checked Computation

- **9.1 Project Layout.** Describe Core, Geometry, Induction, Prefix,
  Scattering, Phase, and Universal.
- **9.2 Dependency Graph.** Show the Lean proof cone from semantics and blank
  P104 to prefix coupling, entry geometry, ordinary/exceptional scattering,
  and universal assembly.
- **9.3 Computation Leaves.** Separate analytic proofs from the three finite
  leaves: blank 9,977/P104, 1,376 prefix placements, and shared 22-channel
  scattering.
- **9.4 Computation without Search.** Explain that proof checking replays
  checked-in witness times deterministically; generation-time search is not a
  proof dependency. Report performance only after measurement.
- **9.5 Trusted Computing Base.** Distinguish kernel-checked analytic and
  soundness arguments from `native_decide`, and state the compiler/runtime/code
  generation extension of the TCB. The Python generator is for independent
  regeneration and is not in the proof-checking TCB.
- **9.6 Reproduction.** Give the pinned toolchain, complete check command,
  witness-table regeneration procedure, and manuscript--artifact consistency
  checks.

#### 10. Related Work and Broader Perspective

- **10.1 Unboundedness Results.** Audit the original theorem and attribution;
  distinguish escape from finite regions from P104 entry.
- **10.2 Complexity and Universality.** Separate finite-support Boolean-circuit
  P-hardness from infinite-support universality and undecidability.
- **10.3 Highway Experiments and Generalized Ants.** Review classical P104
  experiments, bounded-radius one-black experiments, and generalized-ant
  highways; state the exact academic position only after the full audit.
- **10.4 Toward the General Highway Conjecture.** Retain the broader research
  program while fencing it from the one-black proof evidence:
  - complete-history renewal and canonical genealogy;
  - structural invariants, including the four-step turn-word restriction,
    `heading-|B| mod 4`, and Laurent-polynomial branches;
  - multi-black interference and the 914,749-state prefix-primary transient
    computation, explicitly a state count rather than a trajectory length.

#### 11. Conclusion

- Restate the exact theorem for arbitrary exactly-one-black states.
- Summarize the finite-prefix plus 22-affine-channel reduction.
- Emphasize the distinct ordinary-history and phase-72 induction mechanisms.
- State the Lean-checked scope and finite-computation trust boundary accurately.
- End with multi-black interference and the general finite-support Highway
  Conjecture without enlarging the theorem proved here.
