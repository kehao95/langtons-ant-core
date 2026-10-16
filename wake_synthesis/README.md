# Uniqueness of the Classical Langton Ant Highway from Its Layer Profile

Thin-wake rigidity derives the standard layer profile and all longitudinal residues from full drift (2,-2), growth twelve, width ten and at most one odd class on each interior level. General non-axis wake budgets and inverse synthesis remain.

## Integrated results — 16 October 2026

The revision adds [mixed-wake interleaving](proof/mixed-wake-interleaving.md):
for full drift `(2,-2)`, `J(O)+V/2 = 1 (mod 2)` at arbitrary growth and width.
The [attributed periodic-growth closure](proof/periodic-growth-closure.md)
retains signed residues, small-drift restrictions and the unit-diagonal certificate.
These are a separate necessary screen, not premises replacing the complete
thin-wake enumeration. The incoming [profile replay](PROFILE_REPLAY.md) is
also bundled as additional evidence for the subsumed profile theorem.

## Manuscript and status

Version **0.3.0** is prepared for review. [Manuscript](paper/main.tex) ·
[Proof dependencies](PROOF.md) · [New-module verification](evidence/review-2026-10-16.json) ·
[Release preparation](release/README.md).

The current public record is [23405441](https://doi.org/10.5281/zenodo.23405441); its published files are preserved. The revision belongs to the same concept **23402421**.

## Exact scope

The theorem classifies periodic traces under the stated drift, growth, width and interior-thinness hypotheses. It derives the standard profile; it does not derive those hypotheses for every finite seed. Full standard-profile and complete-wake uniqueness are corollaries.

## Reproduce

```sh
python3 wake_synthesis/reproduce.py --output-report /tmp/wake_synthesis-review.json
make -C wake_synthesis/paper
```

Run from the repository root, using Python 3.10+ without `-O`. Checks use disposable copies and retain the imported source and evidence. A C++17 compiler is required. The manuscript uses pdfLaTeX. Builds write to `paper/build/`.

Default replay covers the full 76-case/83-job classification, its 90,158-edge upper certificate, and the retained standard-wake/general-synthesis checks. `--quick` skips the 76-case exhaustion but still rebuilds its upper graph, all count tables and controls. `--jobs 4` controls native concurrency. `--baseline` additionally repeats the older exact enumerators.

Use `--extensions-only` to replay just the 16 October additions. The default
continues to cover the complete main-paper dependency chain.

## Open

Review the prepared manuscript and standalone package before authorizing a Zenodo release. Independent mathematical peer review and journal preparation remain separate steps.

## Analytic unit-diagonal proof

The [standalone analytic note](verification/unit_diagonal_analytic/PROOF.md)
replaces the unit-diagonal finite certificate by forced layer words and a binary
interleaving contradiction. The exclusion and its `g>=8` consequence were already
integrated above; this is a new proof, not a duplicate theorem claim.
[Manuscript source](verification/unit_diagonal_analytic/paper.tex) and
[independent regressions](verification/unit_diagonal_analytic/README.md) are
provided separately; finite checks are no longer premises of this exclusion.
No published or previously prepared release artifact is changed.
