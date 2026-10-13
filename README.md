# Langton’s Ant: One-Black Highways and Exponential Escape

Two results for the classical white-right / black-left Langton ant, with
papers, proofs and reproducible verification:

- **One-black highway theorem:** every initial state with exactly one black
  cell eventually reaches the standard translating period-104 highway.
- **Rational clocks and exponential escape:** every trajectory starting inside
  an n × n square exits within **8 n 3ⁿ + 1 updates**, for every n ≥ 1 and
  arbitrary colouring.

Both preprints are by Hao Ke, published as version **0.2.0** on 2026-10-13.

## One-black highway theorem

The theorem covers every black-cell location, ant position and heading. Its
Lean proof establishes eventual agreement with the full future read trace of
a translated and rotated standard blank highway. The construction combines
22 scattering channels, a 21+1 classification and historical-wake isolation.

**Paper:** *Every One-Black-Cell Langton Ant Reaches the Period-104 Highway:
A Lean-Checked Proof* — [Zenodo](https://doi.org/10.5281/zenodo.23341609).

- [Manuscript and PDF](preprint/README.md)
- [Mathematical proof](one_black/PROOF.md) and [reproduction guide](one_black/README.md)
- [Standard-trace Lean theorem](one_black/lean/StandardTrace.lean)
- [Clean-build and axiom audit](preprint/JOURNAL_REVIEW.md)

The complete theorem is checked in Lean 4.30.0. The audit records the three
native computation leaves used by the finite certificates.

[![Global one-black proof map](preprint/figures/stages/stage-06-global-map.png)](https://kehao95.github.io/langtons-ant-core/)

*Explore the [interactive one-black proof guide](https://kehao95.github.io/langtons-ant-core/):
coloured rays represent affine placement classes covered at every depth.
[Proof animations](media/x/README.md) accompany the guide.*

## Rational clocks and exponential escape

For an axis-aligned square of **n cells per side**, the first-exit bound is

$$T_{\mathrm{exit}}(n) \leq 8n3^n + 1.$$

It holds for every internal colouring and initial ant pose, with arbitrary
exterior colours, and counts the move out of the square. An explicit rational
clock increases at every step; bounding its range inside the square gives the
escape estimate. For complete finite-support states, the clock also yields
algorithms for reachability, orbit equivalence and canonical orbit representatives.

**Paper:** *An Ant on the Clock: Exponential Escape Bounds for Langton’s Ant* —
[Zenodo](https://doi.org/10.5281/zenodo.23341604).

- [Manuscript and reproduction guide](clock_escape/README.md)
- [Published PDF](clock_escape/An-Ant-on-the-Clock.pdf) and [LaTeX source](clock_escape/main.tex)
- [Local Lean lemmas](clock_escape/lean/ClockLemmas.lean)
- [Proof audit](clock_escape/VERIFICATION.md) and [exact verification evidence](clock_escape/evidence/)

The full escape theorem has an analytic proof. Lean 4.30.0 checks the local
algebra, positivity and telescoping lemmas. Independent exact checks include
all 4,213,000 colour/pose states for squares of side lengths 1 through 4.

## Reproduce

Use Python 3.10+ and Lean **4.30.0**. Both proof artifacts are self-contained;
the Python checks use the standard library and the Lean projects use no Mathlib.
Run from the repository root:

```sh
# One-black: build the complete Lean theorem, including standard-trace equality.
python3 one_black/check.py

# Clock: replay exact checks, certificates and local Lean proofs.
python3 clock_escape/reproduce.py
```

For a fresh one-black build without cached proof artifacts, run
`python3 preprint/verify.py`. Build the papers with `make -C preprint`
(Pandoc and XeLaTeX) and `make -C clock_escape` (pdfLaTeX).

## Repository map

| Directory or document | Contents |
|---|---|
| [`one_black/`](one_black/README.md) | One-black dynamics, complete Lean proof and finite certificates |
| [`preprint/`](preprint/README.md) | One-black manuscript, figures, PDF and publication evidence |
| [`clock_escape/`](clock_escape/README.md) | Clock manuscript, PDF, local Lean proofs, exact checkers and certificates |
| [`docs/`](docs/) | Interactive guide to the one-black proof |
| [`PROOF.md`](PROOF.md), [`research/`](research/) | Further deductions and executable research checks |
| [`RESEARCH.md`](RESEARCH.md) | Ongoing finite-support Highway Conjecture research |

## Published versions

The one-black record [23341609](https://doi.org/10.5281/zenodo.23341609)
updates the original preprint [22086968](https://doi.org/10.5281/zenodo.22086968)
within the same version chain (concept DOI
[10.5281/zenodo.22086967](https://doi.org/10.5281/zenodo.22086967)). The clock
paper has its own record [23341604](https://doi.org/10.5281/zenodo.23341604).

Source manifests, artifact hashes and publication receipts are linked from the
[one-black release notes](preprint/RELEASE.md) and
[clock release notes](clock_escape/RELEASE.md).
[Repository integration checks](PUBLICATION_SYNC.md) document agreement with
the published sources and the standalone clock reproduction.

## Open

Mathematical peer review and journal preparation for both papers:
Journal of Automated Reasoning for the one-black paper and Natural Computing
for the clock paper are candidates. Subsequent editorial work accumulates
before the next deliberate versioned release. The general finite-support
Highway Conjecture remains an open research direction in [`RESEARCH.md`](RESEARCH.md).
