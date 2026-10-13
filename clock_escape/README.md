# An Ant on the Clock: Exponential Escape Bounds for Langton’s Ant

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23341604.svg)](https://doi.org/10.5281/zenodo.23341604)

Hao Ke, version **0.2.0**, published 2026-10-13.
[Read the preprint](An-Ant-on-the-Clock.pdf) ·
[Zenodo record](https://doi.org/10.5281/zenodo.23341604) ·
[Manuscript source](main.tex).

## Results

For the classical white-right / black-left ant, first exit from an axis-aligned
square of **n cells per side**, n >= 1, takes at most `8*n*3^n + 1` updates,
uniformly over all internal colours and initial poses. The count includes the
move out of the square, and exterior colouring may be arbitrary.

An explicit rational clock supplies a positive increment at each update. Its
finite range inside a square gives the escape bound. On complete finite-support
states, the same construction yields decidable complete-state reachability,
orbit equivalence, and a computable orbit section. The paper develops these
results independently of the one-black theorem and the Highway Conjecture.

## Reproduce

From this directory, with Python 3.10+, Lean **4.30.0** and a LaTeX installation:

```sh
python3 reproduce.py
make
```

The verification uses the Python standard library and Lean without Mathlib.
All baseline implementations and certificates are included under
[`verification/`](verification/); no sibling research repository is required.
`make` writes a fresh PDF to `build/main.pdf`. The checked-in
[`An-Ant-on-the-Clock.pdf`](An-Ant-on-the-Clock.pdf) is the exact published PDF.

- [`main.tex`](main.tex): analytic proofs of the clock, square bound and orbit results.
- [`lean/ClockLemmas.lean`](lean/ClockLemmas.lean): formal local algebra,
  positivity and telescoping lemmas.
- [`verification/check.py`](verification/check.py): independent rational checks
  and all 4,213,000 colour/pose states for side lengths 1 through 4.
- [`evidence/`](evidence/): exact results, certificates and Lean axiom output.
- [`VERIFICATION.md`](VERIFICATION.md): proof dependencies and the precise
  coverage of the analytic, Lean and computational evidence.
- [`LITERATURE.md`](LITERATURE.md): primary-source comparison.
- [`EDITORIAL_REVISION.md`](EDITORIAL_REVISION.md): incorporated structural edits.
- [`RELEASE.md`](RELEASE.md): publication record and file verification.

The analytic proof establishes the full escape theorem. Lean formalizes its
local algebra and interval argument; the finite checks provide additional
independent evidence.

## Published source provenance

The manuscript, proof code, baseline dependencies and historical evidence were
imported byte for byte from the published 0.2.0 source archive.
[`published-source-manifest.json`](published-source-manifest.json) preserves
that archive's original relative paths, source revision and hashes. Repository
navigation and release notes have since been updated for this public home;
the manifest describes the published snapshot, not these later documentation
edits. [`publication-receipt.json`](publication-receipt.json) records the
published artifact checksums. The original mathematical audit and subsequent
editorial revision remain separately identified in `evidence/reproduction.json`
and `EDITORIAL_REVISION.md`.

## Open

Mathematical peer review, broader citation-chain checking, and venue-specific
journal preparation (Natural Computing candidate). Accumulate subsequent edits
before preparing a deliberate versioned release.
