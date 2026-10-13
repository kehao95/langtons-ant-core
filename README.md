# Langton’s Ant: One-Black Highways and Exponential Escape

Two results for the classical white-right / black-left Langton ant, by Hao Ke.
Each project contains its paper, proof sources, verification evidence and release record.

| Project | Result | Proof and preprint |
|---|---|---|
| [One-black highways](one_black/) | Every one-black initial state reaches the standard period-104 highway, at any ant position and heading. | Complete Lean proof · [Zenodo](https://doi.org/10.5281/zenodo.23341609) |
| [Clocks and escape](clock_escape/) | First exit from any n × n square takes at most **8 n 3ⁿ + 1** updates. | Analytic proof with local Lean lemmas · [Zenodo](https://doi.org/10.5281/zenodo.23341604) |

## Layout

```text
one_black/                 clock_escape/
├── README.md              ├── README.md
├── paper/                 ├── paper/
├── lean/                  ├── lean/
├── evidence/              ├── evidence/
├── release/               ├── release/
└── reproduce.py           └── reproduce.py
```

`paper/` holds the manuscript, published PDF and build recipe; `lean/` the
formal proofs; `evidence/` the audit and check results; `release/` the DOI,
receipts and published-source hashes. Project-specific simulation, verification
and illustration tools stay with their project.

[Research](research/) contains further deductions and the ongoing Highway
Conjecture program. [The interactive guide](https://kehao95.github.io/langtons-ant-core/)
explains the one-black proof; its site and exporters live in [`docs/`](docs/).

## Reproduce

With Python 3.10+ and Lean **4.30.0**, from the repository root:

```sh
python3 one_black/reproduce.py
python3 clock_escape/reproduce.py
make -C one_black/paper
make -C clock_escape/paper
```

The one-black command performs a clean Lean build and checks both final axiom
reports. The clock command runs the exact checkers and local Lean proofs.
Paper builds require Pandoc/XeLaTeX and pdfLaTeX respectively; outputs go to
`paper/build/`, alongside the preserved published `paper/paper.pdf`.

Both preprints are version **0.2.0**. The one-black release updates its existing
Zenodo version chain. [Layout migration](CHANGELOG.md) records the new paths;
the published archives retain their original layout.

## Open

Mathematical peer review and journal preparation for both papers. Current
project details live in each project README; ongoing HC research lives in
[`research/README.md`](research/README.md).
