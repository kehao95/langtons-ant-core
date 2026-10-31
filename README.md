# Langton’s Ant: Proofs and Preprints

Eleven article projects about the classical white-right / black-left Langton
ant and cyclic-color generalizations, by Hao Ke. Each project provides its article, proof dependencies,
executable verification and published artifacts.

**Cross-project research perspective:** [Conceptual map](research/README.md) · [How a self-writing medium creates complexity](research/SELF_WRITING_MEDIA.md) · [Testable research agenda](research/NEXT_QUESTIONS.md). These are interpretive research notes and conjectural directions, **not additional published theorems**; the article modules, their sources and certificate interfaces remain authoritative.

## Results and manuscripts

| Project | Result | Publication |
|---|---|---|
| [One-black](one_black/) | Every one-black finite state, at every position and heading, reaches the complete standard P104 trace. | [Zenodo](https://doi.org/10.5281/zenodo.23844645) |
| [Clock and escape](clock_escape/) | Square exit ≤ `(13·3^(n−1)−2n²−4n−5)/2`; fixed-height rectangle degree `⌊H/2⌋+1`; complete-state orbit algorithms. | [Zenodo](https://doi.org/10.5281/zenodo.23844652) |
| [Four and five rows](four_row_escape/) | Exact four-row maximum `34n-150`; five-row quadratic escape and infinite boundary memory; complete two-counter highway recovery and succinct full-state random access. | [Zenodo](https://doi.org/10.5281/zenodo.23844660) |
| [Wake rigidity](wake_synthesis/) | P104 uniquely minimizes the signed quadratic odd-wake moment at full drift `(2,-2)` and width ten. Thin-wake rigidity; Non-axis inverse synthesis and quadratic wake tests; all-axis inversion parity; analytic unit-diagonal exclusion. | [Zenodo](https://doi.org/10.5281/zenodo.23844688) |
| [Factor language](factor_language/) | Ten-factor attraction with sharp slope 12; exact intrinsic local-event macros and quadratic deadlines; all-input mass–defect inequalities with sharp nine-factor window threshold; finite-horizon core/supply bound; archive recovery. | [Zenodo](https://doi.org/10.5281/zenodo.23844669) |
| [Defect synthesis](defect_synthesis/) | All-coordinate bounded-defect semilinearity and resource spectra; a six-cell family with arbitrarily many defects and uniform `mu(N)<=6`; small witnesses and a restricted QF decision backend. | [Zenodo](https://doi.org/10.5281/zenodo.23844674) |
| [Memory and feedback](memory_feedback/) | Exact event prediction and full-history continuation; remote feedback and fixed-mass lifetime obstruction; request-only crossing capacity, speed/spread bounds and a double-logarithmic oblique-width gap. | [Zenodo](https://doi.org/10.5281/zenodo.23844677) |
| [Ports and scattering](four_cell_port/) | Sharp four-cell ports; four-layer rectangle shielding and exact P104 entrance; sharp solid-rectangle bound; finite protected scattering trains and old-wake readback. | [Zenodo](https://doi.org/10.5281/zenodo.23844695) |
| [Intervention capacity](intervention_capacity/) | One timed toggle within a common passive highway needs Θ(T²) predictive bits; a q-time menu needs Θ(qT); exact all-control quotient. | [Zenodo](https://doi.org/10.5281/zenodo.23844704) |
| [Phase clocks and charges](phase_cocycle/) | Complete separated-observable classification; sharp clock order 8n or 4n; classical modulo-16 clock and compact-charge basis. | [Zenodo](https://doi.org/10.5281/zenodo.23844710) |
| [Sparse trace spaces](sparse_trace_space/) | At most m black cells give prefix complexity Θ_m(n^m), exact derived-set hierarchy and rank m+1, attained inside a positive highway family. | [Zenodo](https://doi.org/10.5281/zenodo.23844714) |

[Articles](PREPRINTS.md)

Each project supplies an article PDF built from its accompanying source. Zenodo
DOIs identify archived editions in the same article series. In `publications.json`,
`doi` and `version`, when present, refer to that archived edition; `pdf` and `pdf_sha256`
identify the accompanying repository article.

## Project layout

Each project contains `paper/`, `PROOF.md`, `evidence/`
and `reproduce.py`. Exact checkers live in `verification/`; formalized projects
also contain `lean/`. One-black retains its established dynamics package.
`sources.json` lists the exact files and SHA-256 hashes needed for the source
package. `publications.json` records the current article and DOI for each project.

The clock paper owns general clocks and escape bounds; the four-row paper owns
the four/five-row boundary, exact counter-family recovery and full-state random access. Wake uses them for period budgets;
memory uses escape to bound events in a fixed region; port uses a local clock
inside certified recovery stages. Factor's finite-word mass proof is independent
of its infinite-future attraction proof. Memory owns the twenty-black lifetime
obstruction and the crossing-capacity/width theorems. Defect owns the six-cell
unbounded-defect family. Port owns protected rectangular formation and arbitrary
finite scattering composition. Intervention owns counterfactual predictive
storage on one passive trace; phase owns separated clocks and charges; sparse
trace space owns all-coordinate fixed-mass observation complexity and topology.

One-black has a complete Lean proof. The other new results combine analytic
coverage arguments with exact finite checks. The clock also contains Lean
proofs of its supercritical local identities. Each project describes the proof dependencies and computational trust boundary.

## Reproduce and build

Run a project's scoped checks from the repository root:

```sh
python3 wake_synthesis/reproduce.py --jobs 4
python3 four_row_escape/reproduce.py
python3 intervention_capacity/reproduce.py
python3 sparse_trace_space/reproduce.py
uv run --no-project --with sympy==1.14.0 python phase_cocycle/reproduce.py
python3 factor_language/reproduce.py
python3 defect_synthesis/reproduce.py
python3 memory_feedback/reproduce.py
python3 four_cell_port/reproduce.py
```

Wake defaults to the complete extremal-moment and thin-wake exhaustions.
Use `--moment-only --full` for the 1,616 moment cases with the shared upper
certificate. The thin-wake stage has 76 cases and 83 jobs. Its `--quick` mode checks
the upper graph, count tables and controls but skips those large exclusions.
Factor, wake, defect, memory and port use a C++17 compiler.
Defect and port use ISL/GMP; defect additionally uses Z3.
All use Python 3.10+ without `-O`; phase additionally uses SymPy 1.14.0.
One-black and full clock reproduction additionally require Lean 4.30.0; their
unchanged commands remain in their project READMEs.

Build with `make -C <project>/paper`. Wake, clock, four-row escape and defect synthesis use pdfLaTeX; factor,
memory and the expanded port manuscript use XeLaTeX. One-black retains its
Pandoc/XeLaTeX workflow. Generated files go to ignored `paper/build/` directories.
Validate source integrity and article links with `python3 tools/check_publication.py`.

## Interactive proof labs

Explore the [six interactive proof labs](https://www.kehao.me/langtons-ant-core/):
one-black case coverage, editable integer clocks, wake-class parity, local
language and mass defects, black-cell lifetimes, and composable scattering.
Each route connects a manipulable witness to its proof steps, exact evidence
and paper. The original one-black guide is now at
[one-black.html](https://www.kehao.me/langtons-ant-core/one-black.html).

[Site development and checks](docs/) · [Interaction design](docs/DESIGN.md).
Browser replay retains complete finite fields. The manuscript snapshots are
identified by source paths, SHA-256 hashes and DOI links in the site manifest.
