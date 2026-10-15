# Verification audit — 15 October 2026

The three central conclusions survive this audit: the sharp 918-update
three-black half-plane bound, the four-black standard P104 port, and universal
four-cell exterior completion of finite observed histories. The proof is
computer assisted, with analytic coverage and geometric coupling. Independent
implementations here are software cross-checks, not external peer review.

## Claims and supporting evidence

| Claim | Universal argument | Executable evidence |
|---|---|---|
| All placements of at most three black cells exit by 918 | First-contact coverage, including arbitrary unbounded coordinates and arbitrary exterior colours | All 284 family records in `escapes.json`; separate online initial-colour branching; third reconstruction |
| Four-cell seed stays in the half-plane and has standard P104 from 182 | Prefix guard, finite parity breakpoints covering every epoch, then induction on time | Complete 36-cell endpoint in `witness.json`; 170 phase/epoch tests; independent 40-interval, 22-class check of both port and blank reference |
| Exactly four remote additions preserve any finite observed prefix and force P104 | First exit from a protected square; outward half-plane placement; full-field coupling | Explicit constructor and 96 implementation cases, all four exit sides, including 16 translations of magnitude 10³⁰ |
| Entry by 8 n 3ⁿ + 183 | Existing square escape bound plus 182 port updates | Arithmetic consequence in the proof; sampled exit-budget checks are auxiliary |

The original `check.py` and `independent.py`, and their three JSON certificates,
are byte-identical to source commit `f8f593ae5d87929bbcd7dd2ddbd2593afe60c28a`.
The new `audit.py` imports neither original checker. It uses integer-vector
dynamics from `completion.py`; it reads the original declarative certificates,
reconstructs families, and checks chronological visits to each physical cell.
The periodic-realisability method is credited to Jillhewar in the manuscript.

## Corrections to the source proof and manuscript

1. Prefix agreement now means equal positions, headings and read colours.
   Complete colourings differ by the four added cells from time zero:
   `B_t^+ = B_t △ A = B_t ∪ A` through the first exit. The old statement of
   complete-trajectory equality was too strong if read as full-state equality.
2. Phase positions in the parity formula are absolute endpoint coordinates,
   consistent with `B_182` and the range `4 <= x <= 9`.
3. The coverage lemma explicitly proves the uniform time bound, rather than
   only excluding trajectories that remain forever in the half-plane.
4. Cell diagrams use centre coordinates and put the supporting line between
   columns −1 and 0. The draft says “from update 182”, avoiding an unsupported
   claim of earliest possible standard entry.
5. The model allows arbitrary exterior colouring for the lower bound and
   restricts to finite support where completion needs it. The paper attributes
   the existing realisability criterion and cites the clock dependency.

These corrections are also applied to the originating research repository.

## Controls and reproducibility

`audit.json` records actual deterministic results. The checker rejects a
missing family row, a false exit time, all 13 individual active-black-bit
mutations, and a blocker 10¹⁰⁰ periods ahead. An off-trace marker is accepted.
Removing each of the four gate cells produces exits at 2, 66, 86 and 170.
Completion cases check full-field symmetric difference before exit, preservation
of every inside black cell afterwards, and the certified infinite tail.

Run `python3 four_cell_port/reproduce.py` from the repository root. It regenerates
original certificates in a disposable directory and compares bytes, then reruns
the third audit against retained data. `reproduction.json` records source hashes
and fresh execution results. `../release/source-manifest.json` pins draft artifacts.

## Manuscript self-review and remaining work

- Logical structure: each universal claim names its analytic reduction before
  the finite computation; completion has a full coupling proof.
- Definitions: observation, full colouring, standard word, phase positions,
  one-sided minimality and step numbering agree across proof and code.
- Evidence: full states and infinite rays are checked, including adverse
  certificate mutations; sampled completion tests are identified as tests.
- Attribution: previous periodic-realisability and escape results are credited;
  the proposed contribution is the sharp port and completion construction.
- Presentation: constructive exposition, a two-witness figure, and reproducible
  commands; administrative release state is outside the manuscript.

The remaining review obligations are external mathematical scrutiny and final
priority assessment. No full Lean proof, referee endorsement or publication
priority is inferred from passing these checks. Existing published one-black
and clock artifacts are preserved without rebuilding unrelated proofs.

## Current completion-bound revision

The independent audit now checks first exit against the stronger integer-clock
bound E(n) on all 96 completion cases. Its result counts and immutable finite
certificates are unchanged. Current source hashes are in
`../release/candidate-manifest.json`; the earlier reproduction and source
manifest describe their dated preparation snapshot.
