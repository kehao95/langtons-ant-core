# Current literature revision — 26 October 2026

The [primary-source review](LITERATURE_REVIEW.md) compares all six candidates
with their nearest located predecessors and records the revised contributions.
Introductions, bibliography, literature notes and descriptions were updated.
No theorem statement, proof certificate or executable mathematical checker changed.

The candidate standalone records use `editorial-only`: the source ZIP and PDF
are rebuilt in isolation, while proof checks are inherited from the preserved
pre-review candidates by exact non-editorial source hashes. Five predecessor
records are full replays; wake retains its documented new-module replay plus
hash-matched full classification. This distinction supersedes the package dates
below without replacing their mathematical evidence.

The six candidate versions remain pending. Owner review and external mathematical
review remain separate, and no Zenodo operation was performed.

| Candidate | PDF pages | Source files checked | Mathematical replay inherited from |
|---|---:|---:|---|
| [Four-row](four_row_escape/release/v0.1.0/standalone-check.json) | 8 | 15 | Full, 21 October |
| [Factor](factor_language/release/v0.1.0/standalone-check.json) | 31 | 102 | Full, 21 October |
| [Defect](defect_synthesis/release/v0.1.0/standalone-check.json) | 12 | 71 | Full, 21 October |
| [Memory](memory_feedback/release/v0.1.0/standalone-check.json) | 27 | 60 | Full, 16 October |
| [Wake](wake_synthesis/release/v0.3.0/standalone-check.json) | 25 | 229 | Extensions, 16 October; retained full base, 15 October |
| [Port](four_cell_port/release/v0.2.0/standalone-check.json) | 18 | 28 | Full, 15 October |

All six isolated builds pass and reproduce the delivered PDF text. All 505
source hashes match their archives; 466 files outside manuscript/README scope
match the preserved predecessors. Formal theorem environments and display
mathematics were compared unchanged, alongside manual review of the prose diff.
No unresolved references or overfull boxes remain. Revised introduction and
bibliography pages were visually checked. A changed-proof-source negative
control is rejected by the inheritance checker before any pass report is written.

---

# Mathematical integration review — 20 October 2026

Research source: `16b9b465a291933d0229f8febf180fcc3be7fddc`; core base: `22e0c9e`.
Eight publication projects now contain six local release candidates. This revision
changes three candidates and adds scoped research tools. No Zenodo or journal action.

## Claim–evidence map

| Claim | Evidence | Status and boundary |
|---|---|---|
| Four-row exact maximum `34n-150` for every `n>=13` | [Full new-module replay](four_row_escape/evidence/replay-2026-10-20.json), persistent closure and two-vector affine induction in the paper | Supported by an unformalized computer-assisted proof; covers all colors and internal poses, not general plane HC |
| One contiguous standard core and `L<=52 norm_inf(Delta)+114c+223437` | [Factor replay](factor_language/evidence/replay-2026-10-20.json); ordered cover, transverse 44-cell intersection, full-field cofactor estimate | Supported for every finite ten-legal word; 52 is sharp, other constants need not be |
| One standard jump for the exact first J10 | Same replay, complete compressed endpoints and huge-coordinate parity checks | Explicit m-point input only; O(m+1) literal work is not a compressed-mass guarantee |
| Nine-factor bound 1004 and least window nine | Same replay; 164,283 complete words, 9,550 integer edges, complete condensation, all-n finite eight-legal truncation | Supported; mass threshold is distinct from attraction threshold, no finite HC counterexample |
| Polynomial-size QF physical realization and shared factor circuit | [Six-section backend replay](defect_synthesis/evidence/replay-2026-10-20.json), parity-boundary proof and complete cover | Restricted source/stride syntax; general quantified sources and complete target equality remain with the old compiler |
| Unary NP with binary side constraints and FP^NP minimum cost | Complete-cover argument, integer small solutions and O(N) padding/search range | Analytic upper bounds; no deterministic polynomial solver or computed mu table |
| Noninterlaced contour exit and rank-obstruction controls | [All three research modules replayed](research/renewal/evidence/replay-2026-10-20.json) | Local results only; detached contours can rejoin, and interlaced `2L` fails |
| Complete-history one-bit recovery | [Recovery status](highway_stability/README.md) | Original 739-case archive still absent; numerical theorem remains conditional |

## Manuscript outline and internal review

- **Contribution — pass:** four-row classification answers an explicit published
  conjecture and has an independent proof runtime. Factor develops local-language
  rigidity through finite-horizon supply into mass bounds. Counting Defects keeps
  one arithmetic story, distinguishing general semilinearity from restricted QF
  decision syntax. Prior NP membership is not presented as a second discovery.
- **Clarity — pass:** four-row follows interfaces, closure, weighted maxima and
  induction. Factor places silent supply immediately after interval geometry and
  the nine-factor threshold after the ten-factor mass proof. Counting Defects
  places QF realization after small witnesses. Definitions distinguish contained
  forward defects from inverse-history intrinsic events.
- **Evidence strength — pass for internal checks:** exact finite premises are
  reconstructed, full endpoints retained and damaged controls rejected. Literal
  replays supplement the universal arguments rather than extend cutoffs. Separate
  implementations are not external mathematical review.
- **Evaluation completeness — package review:** new modules pass their scoped
  checks. The three standalone records below own full archive replay and PDF reconstruction;
  historical unchanged results are not implicitly reverified by a new theorem.
- **Design and soundness — pass within stated scope:** silent bounds restart with
  the actual complete mass; interfaces preserve residual state; QF checks keep
  intra-loop chronology, XOR parity and pairwise-distinct sparse inputs. No
  global event budget, general strip restriction or HC conclusion is inferred.

The QF timing reports are retained historical measurements. A roughly 128-fold
factor-construction ratio is not an end-to-end synthesis ratio. The old general
backend and new existential backend also have different output contracts.

## Packaging and remaining work

The full standalone replays from this integration are preserved with the
pre-literature-review snapshots:
[four-row](four_row_escape/release/v0.1.0/revisions/2026-10-26-before-literature-review/standalone-check.json),
[factor](factor_language/release/v0.1.0/revisions/2026-10-26-before-literature-review/standalone-check.json), and
[Counting Defects](defect_synthesis/release/v0.1.0/revisions/2026-10-26-before-literature-review/standalone-check.json).
All three PDFs build without unresolved references or overfull boxes. Title,
affine-induction, finite-core, eight-factor construction and QF transition pages
were visually inspected. Prior factor/defect PDF, metadata, manifests and replay records are retained in
`revisions/2026-10-20-before-integration/`. Published artifacts remain immutable.

External mathematical review remains open. The missing one-bit archive is a
release blocker for that separate draft. The missing original small-witness
implementation is optional support for an existing analytic proof; the restored
QF implementation does not silently replace its provenance. Further HC research
needs a cross-event argument or a justified extension of persistent interfaces.

---

# Historical consolidation review — 16 October 2026

Research source: `9223766d`; public-core base: `733a5115`. This revision prepares
five release candidates in seven publication projects and one additional
certificate-conditional recovery draft. No Zenodo write or publication occurred.

| Manuscript change | Universal proof obligation | This revision's evidence |
|---|---|---|
| Wake: general quadratic character | Reconstruct parity edges from finite boundary; cancel port terms; compress run-pair inversion counts | [Arithmetic replay](wake_synthesis/evidence/consolidation-replay.json): original module hashes, exact affine excluded family, Python/C++ and UBSan controls |
| Wake: analytic unit diagonal and thin pruning | Forced layers and binary interleaving; convention-correct parity splice | Same replay: analytic-structure regressions and all 1,280 thin masks. The large h=-7/profile exclusions are inherited |
| Factor: all-length endpoint strip | Every oriented lift path has a common normal; four bounded potentials telescope, with all startup states covered | [Replay](factor_language/evidence/consolidation-replay.json): rebuilt 30,380-vertex graph, independent 6,605-word enumeration, 122,856 edge inequalities |
| Factor: original producer's complete recovery | Two affine parity regimes plus twelve exceptions; complete chronological colours; all-parameter infinite-tail parity | Same replay: original 12-file package restored at its hashes, complete module replay, Python/C++ endpoint controls |
| New Counting Defects paper | Bounded-fold coverage → exact mutable-field relation → unary time counting → finite-portfolio spectra | [Replay](defect_synthesis/evidence/consolidation-replay.json): four included modules, complete finite-cover reconstruction and exact symbolic resource identities |
| Counting Defects: small witnesses | Polynomial interval verifier → residue-64 affine chamber → integer small solutions | Analytic proof checked against the cited NFM 2020 bound `(d+1)!H^d`. The original optional executable archive is absent; none of its reported checks is counted as freshly replayed |
| One Bit Off the Highway draft | First-impact coupling and infinite-age guards reduce to 739 exact finite recoveries | [Partial controls](highway_stability/evidence/analytic-controls.json) verify the canonical infinite tail, wake recurrence and case index only. The numerical theorem remains conditional on the missing archive |

## Structure and contribution review

- **Contribution:** pass for allocation. The general wake screens strengthen the
  existing inverse/classification question; archive recovery completes an existing
  factor construction. Semilinear synthesis answers a separate input/complexity
  question and receives one paper, merging overlapping research implementations.
  The one-bit family has distinct complete-input quantifiers and a separate draft.
- **Clarity:** revised abstracts and transitions lead with the resulting mathematics.
  Factor runs from attraction through event macros, geometry, memory/recovery to
  the independent mass proof. Wake keeps classification first and develops its
  general arithmetic and analytic exclusions in integrated appendices. Counting
  Defects moves from physical semantics to finite coverage, resource budgets and
  small witnesses. Operational status stays in repository evidence, except the
  recovery draft's necessary certificate hypothesis.
- **Evidence:** analytic all-parameter bridges are stated explicitly. Computed
  identities use exact integer relations and complete fields. Hashes identify
  sources; they do not replace coverage. Internal implementation cross-checks are
  not described as external mathematical review or new Lean formalization.
- **Completeness:** wake/factor unchanged base mathematics is compared to previously
  fully replayed archives; the new modules are replayed from isolated packages.
  Defect synthesis replays every bundled module without the research checkout.
  Full universal nonzero-budget enumeration is not an executed result. The missing
  one-bit archive is a release blocker; the small-witness software is optional
  support for the written analytic proof.
- **Design/soundness:** keep full drift, true inverse history and complete endpoint
  fields. Contained forward defects and intrinsic J10 differ at the first nine
  tests. Strip confinement chooses one coordinate per interval, not a bounded ball.
  Fixed-budget synthesis, finite-portfolio budgets and single-input termination
  retain their respective quantifiers. The supply theorem has an explicit sharp
  equality family; the strip constant and recovery time are sufficient bounds.

## Packaging and layout checks

The wake, factor and defect PDFs build without undefined references, missing
citations or overfull boxes. Representative title, theorem, recovery-table,
integer-bound and certificate pages were visually inspected. The new recovery
draft also builds cleanly. The versioned standalone records bind each candidate
ZIP, all source hashes and the rebuilt PDF text. Published releases are retained;
prior same-day wake/factor candidates are archived separately.

## Remaining work

Author review and external mathematical review remain distinct from this internal
verification. Restore the one-bit package identified in its owner README and replay
its finite certificate before promoting its numerical claims. The optional original
small-witness code can add implementation controls without changing the analytic
proof. Future journal choice and any Zenodo publication need their own next step.

---

## Historical review — earlier 16 October revision (research 2f6010a)

The following is the previous snapshot; its open producer future and six-paper
allocation have been superseded by the current sections above.

# Six-paper review — 16 October 2026

Research source: `2f6010a` (following `11894a5`); core baseline: `7ed1162`.
The six-paper allocation remains unchanged. New source imports are byte-pinned;
the original external attribution and licenses are retained. No Zenodo action.

| Current addition | Proof obligation | Evidence and scope |
|---|---|---|
| Wake mixed parity | Signed residues and stable-rank factorization; nine-variable identity telescopes at every width | [New replay](wake_synthesis/evidence/review-2026-10-16.json): reconstructed growth dependencies/unit certificate, 512 Boolean assignments plus symbolic expansion, independent geometric and finite-screen controls |
| Factor legal memory producer | Complete affine arrangement over n=1,2,3 and n>=4; chronological colours and consecutive lifetime identities | [New replay](factor_language/evidence/review-2026-10-16.json): exact immutable witness, Python/C++ controls and eight damaged witnesses |
| Factor folded recovery/reset | Affine endpoint order stabilizes at n=2; complete-field infinite-tail test; all alignments of required read bits | Same report: regenerated masks, full recovery and reset comparisons; clean-reset event cost uses the existing mass inequality |
| Memory birth-filtered query | Each source lifetime can be skipped once; bounded fixed-region bursts; exact last-writer records and complete endpoints | [New replay](memory_feedback/evidence/review-2026-10-16.json): source-coordinate rebirth, literal full-field controls, huge epochs and capped-query controls |
| Memory growing scales | Uniform exterior deadline; subtract pre-cutoff consumptions and the complete lifetime supply at cutoff | Analytic proof in the manuscript; exact integer-log/deadline controls in the dedicated module |

## Internal review

- Contribution: the newly generated lifetime query and mixed-wake order identity
  extend existing interfaces. The folded constructions answer how legal segments
  produce memory and what resetting one interface costs. Prior periodic residue
  and port-sign arguments remain attributed to Jillhewar, with licensed sources.
- Clarity: factor proceeds through attraction, exact events, legal memory production,
  and an independently proved mass bound. Memory proceeds through prediction,
  continuation, geometry, birth filtering, growing scales, and the fixed-mass
  spatial obstruction. Wake retains thin-wake rigidity as its main theorem and
  places the arbitrary-width necessary test in a separate appendix.
- Evidence: finite coverage and all-parameter bridges appear in the papers and
  supplemental proofs. Two implementations are implementation cross-checks,
  not external independent mathematical review. No new Lean claim is made.
- Completeness: immutable old mathematical sources are hash-matched; new modules
  run from copied archives without the research checkout. Wake's earlier large
  classification is inherited. The separate 256-lift profile package is retained
  and hash-checked rather than newly enumerated. Published artifacts are unchanged.
- Soundness: births identify lifetimes, not permanently excluded coordinates;
  K stays fixed within a query; growing-scale counts concern lifetimes, not
  distinct cells. The finite archive family has no all-future claim, whereas
  the second ribbon has a certified standard tail. Clean-reset event cost
  and arbitrary-debris flip cost retain different hypotheses.

The research rank-obstruction module was also replayed to assess its scope.
It remains research material; the all-coordinate budget proposal remains an
open strategy rather than an imported theorem. No new journal or external
review is represented as complete.

## Historical preparation review — 15 October 2026

The following records the preceding candidate snapshot and its actual full
replays. Its page structure and source pins predate the present additions.

# Six-paper review — 15 October 2026

Current allocation is in [PREPRINTS.md](PREPRINTS.md). Research source commit
`0ef3f0e` strengthens the proposed `4a762c3` baseline with thin-wake rigidity
and composable old-wake returns. The later factor import `0a41fba` adds exact first-event macros and quadratic
deadlines. Published artifacts remain untouched.

## Current claim–evidence map

| Manuscript | Main proof obligations | Fresh evidence | Review status |
|---|---|---|---|
| Wake 0.3.0 | Extremal classes → five profiles → 76 masks → all-period caps → exact chronology and complete shard coverage | [Full replay](wake_synthesis/evidence/review-2026-10-15.json): 90,158 edge inequalities, 83 completed jobs, 391,065,872 prefix visits; retained general theory replayed | Internal coverage/source audit and exact replay passed |
| Factor 0.1.0 | 150-window graph plus all-parameter foldback exclusion; independent 300-window potential and bad-endpoint deletion | [Replay](factor_language/evidence/review-2026-10-15.json): Python/C++ kernels, 7,763 lifted edges, sharp witnesses and damaged-certificate controls | Infinite and finite proof routes separated; old 21/14/13 excluded |
| Memory 0.1.0 | Predictor → ray mismatch → full XOR endpoint → convex and endpoint tubes → burst termination → parametric circuit | [Replay](memory_feedback/evidence/review-2026-10-15.json): all five modules, full-field and affine controls | Old exponential event count bounds subordinate to quadratic budgets |
| Port 0.2.0 | First-contact coverage → protected tail → nested-guard induction → exact return-field equality | [Replay](four_cell_port/evidence/review-2026-10-15.json): base port, 30 rules/448 pairs, return packets | All-parameter arguments retained; output times distinguished from first entry |

The wake full report joins two actual invocations (retained standard/general
runner and new thin-wake runner); the integrated entrypoint was also exercised
in quick mode. Quick success is not counted as a second full enumeration.
All new proofs remain analytic with exact native/integer checks. Two implementations
are internal cross-checks, not external independent mathematical review.

## Manuscript structure and self-review

- Contribution: each main result has one owner. Shared clocks and full-drift
  chronology are attributed. The profile theorem is a corollary of thin-wake
  rigidity; it is not another publication.
- Clarity: wake moves from geometric data to complete classification; factor
  moves from legal infinite streams to event decision and then the independent
  finite-word inequality; memory moves from prediction to full continuation,
  geometry and the scale obstruction; port moves from a sharp interface to composition.
- Evidence: finite sets are regenerated and potentials checked, rather than
  accepting hashes as coverage. Universal foldback, affine-family and nested-guard
  arguments remain explicit in the manuscripts and source proofs.
- Completeness: source archives must replay without the private research checkout.
  The older threshold package and unimplemented general PG cover constructor
  are excluded from the claimed closure.
- Soundness: retain full drift, full black fields, true inverse history, strict
  event endpoints, fixed observation regions and every completed search shard.
  Event existence does not assert finiteness of its chain.

Primary sources for symbolic forbidden words, periodic-word chronology and
highway background were reread. This is a targeted attribution check; broader
literature comparison and external mathematical review remain open.

## Historical review: initial publication batch

The following is the preserved review of the earlier 0.1.0 wake and port batch.
Its version labels and Gemini discussion apply only to those historical texts.

# Preprint review — 15 October 2026

The current wake revision is reviewed in
[wake_synthesis/paper/LITERATURE.md](wake_synthesis/paper/LITERATURE.md), with
[new verification evidence](wake_synthesis/evidence/standard_wake/). It closes
the standard-wake classification discussed as open in the historical 0.1.0
review below. The prior Gemini discussion applies to the published 0.1.0 text;
it is not a review of the newly prepared uniqueness manuscript.

This is the internal review record for the [publication portfolio](PREPRINTS.md).
Administrative status and review questions stay here; the manuscripts present
the mathematical constructions and their evidence.

## Contribution allocation and manuscript outlines

| Paper | Argument sequence | Main contribution |
|---|---|---|
| Clock, published 0.4.0 | model → integer clock → square range → critical rectangle potential → orbit algorithms → verification; rational clock appendix | Unit integer clock and stronger square bound, alongside the retained rectangle and complete-state results |
| Wake, published 0.1.0 | inverse input → known word test → diagonal budgets → reciprocal moments → finite synthesis → insertion corollary → examples | Explicit period bounds from a prescribed wake and a period-unknown decision procedure |
| Four-cell port, published 0.1.0 | sharp threshold → infinite port certificate → exterior completion → evidence | Minimal one-sided black-cell count, sharp 918 exit and four-cell completion |
| One-black, existing 0.2.0 | retained manuscript and formal proof | Existing universal one-black standard-trace theorem |

The clock theorem is stated in the wake manuscript with an explicit companion
citation and a short derivation for readability. Primary novelty ownership is
assigned once. The port's completion time is an application of E(n), not a
separate escape-bound claim. One-black keeps its original published title.

## Claim–evidence map

| Claim | Evidence | Status |
|---|---|---|
| Integer clock gain >=1 | Clock Section 2; 24 exact sign/heading/colour polynomial identities | Analytic proof plus exact coefficient audit |
| Square exit <=E(n) | Localized finite sum, exact geometric range, T−1 internal updates; 100 range sums and 18,696 small-square states | Analytic all-n proof with finite controls |
| Rectangular degree floor(H/2)+1 | Critical eight-case identity, horizontal pair costs and localized range; retained Laurent audit | Retained analytic proof and exact checks |
| Complete-state target and orbit algorithms | Integer clock telescoping and explicit inverse update; existing rational-clock algorithm controls retained | Analytic proof; no new broad historical replay claimed |
| Wake-dependent period cutoff | Whole-period cancellation, crossing-flow recurrences and reciprocal Cauchy–Schwarz bound; 16 universal directional identities | Analytic proof plus exact audit |
| Period-unknown synthesis is total | Finite cutoff plus attributed exact word criterion; full search below derived bound 14 | Analytic completeness, implementation controls |
| Standard wake realizes 104 within cutoff 856 | Full-field infinite certificates, all phases/headings, retained power controls | Certified positive witness; uniqueness search remains open |
| Same-wake closed-pose insertion impossible | Retained-step increments unchanged; inserted steps strictly positive | Analytic all-length corollary |
| Sharp 918 and four-cell port | First-contact coverage, 284-seed finite certificate, infinite parity and chronological tests | Computer-assisted proof |
| Four-cell completion by E(n)+182 | Geometric coupling plus clock exit theorem; 96 implementation cases checked against improved budget | Analytic proof plus finite controls |
| One-black standard trace | Existing clean Lean build and axiom audit; all 43 source hashes match retained report | Published formal proof; no new build required by unchanged sources |

The new integer, critical and wake arguments are not represented as Lean
formalizations. The old supercritical local Lean lemmas remain in the clock
appendix with their exact scope.

## Checks performed for this preparation

- `clock_escape/reproduce.py --integer-only`: passed; 24 universal branches,
  100 range sums, 18,696 complete initial states and 12,416 internal transitions.
- `clock_escape/reproduce.py --critical-only`: passed; original retained report
  and independent Laurent audit reproduce exactly.
- `wake_synthesis/reproduce.py --search`: the imported suite and optional finite
  experiment reproduced exactly; new algebraic audits passed. The additional
  full-field audit certifies 416 phase/heading cases, rejects 13 necessary-seed
  deletions and a blocker 10^100 epochs away, and accepts an off-trace marker.
- `four_cell_port/reproduce.py`: passed, including stronger-budget checks for
  all 96 completion cases. Original certificates and audit counts are unchanged.
- Three manuscripts built twice with pdfLaTeX, with resolved references and no
  overfull boxes. Review PDFs have 8, 6 and 6 pages respectively. Page images
  were inspected for layout and equation clipping.
- `tools/prepare_preprints.py`: checks every source ZIP entry against its SHA256,
  the retained one-black PDF against its publication receipt and all 43 Lean
  files against the prior clean-build report. It labels current working-tree
  snapshots explicitly and performs no network action.

Scoped reproduction from the extracted candidate archives is recorded beside
each candidate package. Historical full one-black and clock suites are retained
as prior evidence; they are not rerun merely because the independent wake
project has been added.

## Five-part manuscript self-review

1. **Contribution:** each paper has its own mathematical question and theorem;
   the known supplied-word criterion and special width-four bounds are credited.
2. **Clarity:** abstracts lead with the result and mechanism; headings track the
   proof dependencies; administrative publication disclaimers are outside the papers.
3. **Evidence strength:** all-parameter identities and written coverage arguments
   carry universal claims; finite searches are labeled by their actual domains.
4. **Evaluation completeness:** complete small negative search, positive infinite
   witness, all rotations/phases, remote blockers, inert debris and integer-centre
   branches are covered. The 856 search and global HC remain distinct research questions.
5. **Method soundness:** full drift classes are used; physical debris is retained;
   arbitrary exterior colouring is handled by finite localization; exit moves,
   non-axis hypotheses and resource-cap INCONCLUSIVE responses are explicit.

## Gemini editorial discussion

On 15 October 2026, `agy` model `gemini-3.8-flash-high` read all four complete
manuscript sources, then discussed the actual three-paper revision diff in a
second turn. Both calls completed successfully in conversation
`ef860915-0ae2-4605-b5b7-b46e8b5e150d`. The first turn addressed reverse outlines,
transitions, repetition and standalone readability; the second challenged
specific suggestions and reviewed the resulting edits. This was an editorial
discussion, not an independent mathematical verification.

| Manuscript | Assessment and action |
|---|---|
| One-black | Keep its existing proof architecture and published text. The pristine-state paragraph already defines the active pattern and explains the archive induction; the suggested extra definition would repeat it. |
| Clock | Introduce the time-to-spatial-range mechanism before notation, announce the complete-state orbit results with theorem references, and explain separate coordinate growth rates before the rectangular potential. |
| Four-cell port | Keep the threshold → infinite port → exterior completion sequence. Explain the epoch difference before the parity formula and identify the first exit position explicitly as outside the square. |
| Wake | Lead with the inverse question, put period cancellation before the clock formulas, supply the flow-to-recurrence algebraic step, and motivate reciprocal moments. Shorten repeated scope and verification prose; keep the attributed clock proof self-contained. |

The first response called the square bound “sharp”, proposed an unestablished
formula for the one-black XOR layer, and removed useful proof details in two
replacement passages. These suggestions were rejected. The revision retains
the port phase range `4..9` and the wake colour-count derivation. Gemini agreed
with these corrections in the second round and accepted retaining the short
clock proof. Its final suggestion—to mention rotation before using `x+y` as
the transverse coordinate—was adopted. Its broad praise of mathematical
correctness is not treated as evidence.

The final editorial pass keeps every theorem/lemma/corollary statement and
displayed equation unchanged. Proof edits only identify the port exit pose;
the new wake recurrence explanation spells out the existing algebra. Verification
code, proof artifacts and retained reports match the previously reproduced
candidate sources. Accordingly the new checks rebuild the three manuscripts
and source archives, compare extracted-PDF text, and verify source hashes;
the mathematical runs recorded above remain prior evidence, not new runs.
The final PDFs remain 8, 6 and 6 pages, with resolved references and no box
warnings. One-black's source and the two published delivery PDFs remain unchanged.

## Publication outcome

After reviewing these materials, the owner explicitly requested the new Zenodo
releases on 15 October 2026. Published clock 0.4.0 as record 23402379 within
concept 23341603, port 0.1.0 as 23402414, and wake 0.1.0 as 23402422.
The two first releases now cite the exact clock DOI. Final changes after
editorial review were limited to those bibliography entries, release metadata
and project README status. Final source ZIPs were extracted and rebuilt, with
matching PDF text and no box/reference warnings.

All nine published attachments were anonymously downloaded and SHA256-verified.
The previous clock and one-black PDFs were also downloaded and matched their
original receipts. Versioned release directories contain exact source manifests,
build evidence and public-readback receipts. One-black was not republished.
The owner subsequently authorized README cleanup and Git commit/push of this
batch. Journal submission remains a separate step.
