# Uniqueness of the Classical Langton Ant Highway from Its Layer Profile

Thin-wake rigidity derives the standard layer profile and all longitudinal residues from full drift (2,-2), growth twelve, width ten and at most one odd class on each interior level. General non-axis wake budgets and inverse synthesis remain.

## Manuscript and status

Version **0.3.0** is prepared for review. [Manuscript](paper/main.tex) ·
[Proof dependencies](PROOF.md) · [Fresh verification](evidence/review-2026-10-15.json) ·
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

## Open

Review the prepared manuscript and standalone package before authorizing a Zenodo release. Independent mathematical peer review and journal preparation remain separate steps.
