# Langton’s Ant: Highways, Clocks, Ports and Wakes

Proofs, preprints and reproducible artifacts for four results about the classical
white-right / black-left Langton ant, by Hao Ke.

## Results and papers

| Project | Main result | Published preprint |
|---|---|---|
| [One-black highways](one_black/) | Every one-black initial state, at any position and heading, reaches the complete standard period-104 highway trace. | [0.2.0](https://doi.org/10.5281/zenodo.23341609) · [PDF](one_black/paper/paper.pdf) |
| [Clocks and escape](clock_escape/) | Square first exit ≤ **(13·3^(n−1)−2n²−4n−5)/2**; fixed-height rectangle degree **⌊H/2⌋+1**. Also gives complete-state reachability and orbit normal forms. | [0.4.0](https://doi.org/10.5281/zenodo.23402379) · [PDF](clock_escape/release/v0.4.0/paper.pdf) |
| [Four-cell outgoing ports](four_cell_port/) | Four black cells form a one-sided highway port; at most three force half-plane exit within **918** updates from the inward boundary pose. Four remote cells can complete any finite observed history into a standard highway. | [0.1.0](https://doi.org/10.5281/zenodo.23402414) · [PDF](four_cell_port/release/v0.1.0/paper.pdf) |
| [Wake synthesis](wake_synthesis/) | A prescribed finite odd-class wake, non-axis drift and initial heading determine a period cutoff and a terminating inverse-synthesis algorithm. | [0.1.0](https://doi.org/10.5281/zenodo.23402422) · [PDF](wake_synthesis/release/v0.1.0/paper.pdf) |

The one-black theorem has a complete Lean proof. The clock and wake results have
analytic proofs with exact algebraic checks; Lean also verifies the clock's
supercritical local lemmas. The four-cell result combines analytic reductions
with exact finite certificates and infinite-trace checks.

[Publication portfolio and version history](PREPRINTS.md) ·
[Claim–evidence map and review](PREPRINT_REVIEW.md) · [Change history](CHANGELOG.md)

## Project layout

```text
one_black/       Universal one-black highway theorem
clock_escape/    Integer clocks, escape bounds and orbit algorithms
four_cell_port/  Sharp half-plane threshold and exterior completion
wake_synthesis/  Wake-dependent period bounds and inverse synthesis
```

Each project owns its manuscript in `paper/`, proof narrative in `PROOF.md`,
verification records in `evidence/`, release records in `release/`, and a
`reproduce.py` entrypoint. Formal proofs live in `lean/`; project-specific exact
checkers live in `verification/`.

The clock paper develops the integer clock; the wake paper applies it to period
budgets and inverse synthesis. The four-cell completion theorem uses the clock's
escape bound. Each paper states and attributes these dependencies.

## Reproduce

Run from the repository root:

```sh
python3 one_black/reproduce.py
python3 clock_escape/reproduce.py
python3 four_cell_port/reproduce.py
python3 wake_synthesis/reproduce.py
```

All projects use Python 3.10+. The one-black and full clock commands also require
Lean 4.30.0. The clock's `--integer-only` and `--critical-only` options run scoped
checks using Python alone. Adding `--search` to the wake command runs the finite
detour experiment and requires g++ with C++17.

Build a manuscript with `make -C <project>/paper`. One-black uses Pandoc and
XeLaTeX; the other three use pdfLaTeX. Builds write to ignored `paper/build/`
directories. Published PDFs, source hashes and download-verification receipts
remain in the release records linked above. Zenodo also provides self-contained
source archives for independent reproduction.

## Explore further

[Explore the interactive one-black proof guide](https://kehao95.github.io/langtons-ant-core/),
maintained under [docs/](docs/). [Research](research/) contains further deductions
and the separate, ongoing Highway Conjecture program.

## Open

Independent mathematical peer review and journal preparation for the published
preprints. Project-specific next steps are recorded in each project's README.
