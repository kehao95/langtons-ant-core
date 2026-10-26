# Uniqueness of the Classical Langton Ant Highway from Its Layer Profile

Thin-wake rigidity derives the standard layer profile and all longitudinal residues from full drift (2,-2), growth twelve, width ten and at most one odd class on each interior level. General non-axis wake budgets and inverse synthesis remain.

## Constructions and algorithms

The article includes the general non-axis quadratic wake character,
its polynomial-bit-time evaluator and all-scale growth-eight exclusion family.
The unit-diagonal exclusion now has a purely analytic layer-forcing proof.
The special `(2,-2)` mixed-wake identity analytically removes three of the five
thin-profile cases; the original complete classification remains available.
These results are integrated into the paper and its `--extensions-only` replay.
The [profile proof](PROFILE_CLASSIFICATION.md) remains bundled for the alternate
shortened classification route. [Current proof map](PROOF.md).

## Article

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof](PROOF.md) ·
[Reproduction details](evidence/README.md) · [Zenodo](https://doi.org/10.5281/zenodo.23665515)

## Exact scope

The theorem classifies periodic traces under the stated drift, growth, width and interior-thinness hypotheses. It derives the standard profile; it does not derive those hypotheses for every finite seed. Full standard-profile and complete-wake uniqueness are corollaries.

## Reproduce

```sh
python3 wake_synthesis/reproduce.py --output-report /tmp/wake_synthesis-checks.json
make -C wake_synthesis/paper
```

Run from the repository root, using Python 3.10+ without `-O`. Checks use disposable copies and retain the imported source and evidence. A C++17 compiler is required. The manuscript uses pdfLaTeX. Builds write to `paper/build/`.

Default replay covers the full 76-case/83-job classification, its 90,158-edge upper certificate, and the retained standard-wake/general-synthesis checks. `--quick` skips the 76-case exhaustion but still rebuilds its upper graph, all count tables and controls. `--jobs 4` controls native concurrency. `--baseline` additionally repeats the older exact enumerators.

Use `--extensions-only` to replay the periodic arithmetic modules. The default
continues to cover the complete main-paper dependency chain.
