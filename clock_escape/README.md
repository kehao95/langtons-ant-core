# Rational clocks and exponential escape

For an axis-aligned square of n cells per side, n ≥ 1, first exit takes at most
**8 n 3ⁿ + 1 updates**, uniformly over all internal colours and ant poses,
with arbitrary exterior colours. The count includes the move out.

An explicit rational clock increases at every update. Its finite range inside
the square gives the escape bound. On complete finite-support states, the same
clock yields decidable reachability, orbit equivalence and a computable orbit section.

## Paper

Hao Ke, *An Ant on the Clock: Exponential Escape Bounds for Langton’s Ant*,
version 0.2.0.
[Zenodo](https://doi.org/10.5281/zenodo.23341604) ·
[PDF](paper/paper.pdf) · [Source](paper/main.tex).

## Reproduce

From the repository root, with Python 3.10+ and Lean 4.30.0:

```sh
python3 clock_escape/reproduce.py
make -C clock_escape/paper
```

The verifier uses only bundled sources, Python’s standard library and Lean
without Mathlib. It checks the local lemmas, exact rational identities,
small-square state graphs, complete-state algorithms and integer certificates.
The paper build uses pdfLaTeX and writes `paper/build/paper.pdf`.
The checked-in `paper/paper.pdf` is the exact published PDF.

## Sources

| Path | Contents |
|---|---|
| [paper/](paper/) | Analytic proof, literature comparison and published PDF |
| [lean/](lean/) | Local algebra, positivity and telescoping lemmas |
| [verification/](verification/) | Independent checkers, baseline implementation and certificates |
| [evidence/](evidence/README.md) | Proof audit, exact results and Lean axiom output |
| [release/](release/README.md) | Published version, source manifest and publication receipt |

The analytic proof establishes the full escape theorem. Lean covers the local
algebra and interval argument. Independent finite checks cover all 4,213,000
colour/pose states for square side lengths 1 through 4.

## Open

Mathematical peer review, broader literature checking and journal preparation
(Natural Computing candidate).
