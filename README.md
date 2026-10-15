# Langton’s Ant: Highways, Escape Bounds and Four-Cell Ports

Three results for the classical white-right / black-left Langton ant, by Hao Ke.
Each project contains its paper, proof sources, verification evidence and release record.

| Project | Result | Proof and preprint |
|---|---|---|
| [One-black highways](one_black/) | Every one-black initial state reaches the standard period-104 highway, at any ant position and heading. | Complete Lean proof · [Zenodo](https://doi.org/10.5281/zenodo.23341609) |
| [Clocks and escape](clock_escape/) | Square first exit is **O(3ⁿ)**; fixed-height rectangles have degree **⌊H/2⌋+1**. | Analytic proof with local Lean lemmas · [revised draft](clock_escape/paper/review.pdf) · [published v0.2.0](https://doi.org/10.5281/zenodo.23341604) |
| [Four-cell outgoing ports](four_cell_port/) | Three black cells force half-plane exit by **918** updates; four form a standard highway and complete any finite observed history. | Computer-assisted proof · [review draft](four_cell_port/paper/paper.pdf) |

## Layout

```text
one_black/       clock_escape/       four_cell_port/
```

Each project uses `README.md`, `paper/`, `evidence/`, `release/` and
`reproduce.py`. `paper/` holds the manuscript, PDF and build recipe;
`evidence/` the certificates and audit results; `release/` the release state
and source hashes. Formal proofs live in `lean/` where available; exact
checkers and other project-specific tools stay with their consumer.

[Research](research/) contains further deductions and the ongoing Highway
Conjecture program. [The interactive guide](https://kehao95.github.io/langtons-ant-core/)
explains the one-black proof; its site and exporters live in [`docs/`](docs/).

## Reproduce

With Python 3.10+ and Lean **4.30.0**, from the repository root:

```sh
python3 one_black/reproduce.py
python3 clock_escape/reproduce.py
# For only the critical strengthening:
python3 clock_escape/reproduce.py --critical-only
python3 four_cell_port/reproduce.py
make -C one_black/paper
make -C clock_escape/paper
make -C four_cell_port/paper
```

The one-black command performs a clean Lean build and checks both final axiom
reports. The clock command runs the exact checkers and local Lean proofs.
The four-cell command checks finite certificates, algebraic infinite tails and
the exterior constructor using only Python. Paper builds require Pandoc/XeLaTeX
for one-black and pdfLaTeX for the other two projects; outputs go to
`paper/build/`. Existing published PDFs are preserved in `paper/paper.pdf`.

The one-black and clock preprints are version **0.2.0**. The one-black release updates its existing
Zenodo version chain. [Layout migration](CHANGELOG.md) records the new paths;
the published archives retain their original layout. The strengthened clock
source and review PDF await a versioned update of the existing preprint. The four-cell paper is a
review draft with no Zenodo record.

## Open

Mathematical peer review and journal preparation for the two published papers;
external review and final novelty assessment for the four-cell draft. Current
project details live in each project README; ongoing HC research lives in
[`research/README.md`](research/README.md).
