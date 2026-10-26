# Langton’s Ant: Proofs and Preprints

Eight publication projects about the classical white-right / black-left Langton
ant, by Hao Ke. Each project provides its article, proof dependencies,
executable verification and published artifacts.

## Results and manuscripts

| Project | Current manuscript result | Publication status |
|---|---|---|
| [One-black](one_black/) | Every one-black finite state, at every position and heading, reaches the complete standard P104 trace. | [0.2.0](https://doi.org/10.5281/zenodo.23341609) |
| [Clock and escape](clock_escape/) | Square exit ≤ `(13·3^(n−1)−2n²−4n−5)/2`; fixed-height rectangle degree `⌊H/2⌋+1`; complete-state orbit algorithms. | [0.4.0](https://doi.org/10.5281/zenodo.23402379) |
| [Four-row escape](four_row_escape/) | Exact all-color first-exit maxima: `S(4,n)=34n-150` for every `n>=13`; closed persistent-response classification. | [0.1.0](https://doi.org/10.5281/zenodo.23665471) |
| [Wake rigidity](wake_synthesis/) | Drift `(2,-2)`, growth 12, width 10 and interior odd-class thinness force P104. General inverse synthesis, non-axis quadratic wake tests and analytic unit-diagonal exclusion. | [0.3.0](https://doi.org/10.5281/zenodo.23665515) |
| [Factor language](factor_language/) | Ten-factor attraction with sharp slope 12; exact intrinsic local-event macros and quadratic deadlines; all-input mass–defect inequalities with sharp nine-factor window threshold; finite-horizon core/supply bound; archive recovery. | [0.1.0](https://doi.org/10.5281/zenodo.23665478) |
| [Defect synthesis](defect_synthesis/) | All-coordinate bounded-defect semilinearity; complete endpoints; sharp supply spectra; small witnesses, unary NP membership and a restricted polynomial-size QF decision backend. | [0.1.0](https://doi.org/10.5281/zenodo.23665499) |
| [Memory and feedback](memory_feedback/) | Exact finite-memory event prediction and full-history continuation; exact newly generated remote feedback, growing-scale necessity and a fixed-mass lifetime obstruction. | [0.1.0](https://doi.org/10.5281/zenodo.23665512) |
| [Ports and scattering](four_cell_port/) | Sharp four-cell ports; arbitrary finite protected scattering trains, including unbounded return excursions and old-wake readback. | [0.2.0](https://doi.org/10.5281/zenodo.23665526) |

[Publication versions and packages](PREPRINTS.md) ·
[Literature and contributions](LITERATURE_REVIEW.md) · [Scientific changes](CHANGELOG.md)

DOI links identify the exact published versions. Build the current article
sources using the commands below; each project documents its theorem and proof scope.

## Project layout

Each project owns `paper/`, `PROOF.md`, `evidence/`, `release/`
and `reproduce.py`; exact checkers live in `verification/` and formalized
projects also own `lean/`. One-black retains
its established dynamics package. Published PDFs and release receipts are
immutable; current manuscript builds go to `paper/build/`.

The clock paper owns general clocks and escape bounds; the four-row paper owns
the exact fixed-height-four classification. Wake uses them for period budgets;
memory uses escape to bound events in a fixed region; port uses a local clock
inside certified recovery stages. Factor's finite-word mass proof is independent
of its infinite-future attraction proof. Memory owns the twenty-black lifetime
obstruction; port owns the arbitrary finite scattering composition theorems.

One-black has a complete Lean proof. The other new results combine analytic
coverage arguments with exact finite checks. The clock also contains Lean
proofs of its supercritical local identities. Fresh checks, inherited evidence
and external review are distinguished in each project's evidence records.

## Reproduce and build

Run a project's scoped checks from the repository root:

```sh
python3 wake_synthesis/reproduce.py --jobs 4
python3 four_row_escape/reproduce.py
python3 factor_language/reproduce.py
python3 defect_synthesis/reproduce.py
python3 memory_feedback/reproduce.py
python3 four_cell_port/reproduce.py
```

Wake defaults to the full 76-case, 83-job exhaustion. Its `--quick` mode checks
the upper graph, count tables and controls but skips those large exclusions.
Factor, wake and defect synthesis require a C++17 compiler.
Defect synthesis additionally uses the system ISL/GMP and Z3 shared libraries.
The separate research renewal replay also requires Boost multiprecision headers. All use Python 3.10+ without `-O`.
One-black and full clock reproduction additionally require Lean 4.30.0; their
unchanged commands remain in their project READMEs.

Build with `make -C <project>/paper`. Wake, clock, four-row escape and defect synthesis use pdfLaTeX; factor,
memory and the expanded port manuscript use XeLaTeX. One-black retains its
Pandoc/XeLaTeX workflow. Prepare a local archive with
`python3 tools/prepare_preprints.py --project <project>`. Output goes to the
ignored `<project>/paper/build/package/` directory; `--output-root` selects
an alternative local destination.

## Interactive proof labs

Explore the [six interactive proof labs](https://www.kehao.me/langtons-ant-core/):
one-black case coverage, editable integer clocks, wake-class parity, local
language and mass defects, black-cell lifetimes, and composable scattering.
Each route connects a manipulable witness to its proof steps, exact evidence
and paper. The original one-black guide is now at
[one-black.html](https://www.kehao.me/langtons-ant-core/one-black.html).

[Site development and checks](docs/) · [Interaction design](docs/DESIGN.md).
Browser replay retains complete finite fields. The manuscript snapshots are
identified by their publication receipts in the site's version manifest.

## Supplementary tools

[Complete-history tools](research/) provide exact renewal, contour and
distance constructions with their own proof notes and verification commands.
