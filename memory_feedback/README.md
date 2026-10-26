# Finite-Memory Prediction and Remote Feedback in Langton’s Ant

Total fixed-D old-black event prediction, exact full-history XOR continuation, quadratic finite-event budgets, endpoint tubes, fixed-region event filtering, remote long-lived feedback necessity, and the twenty-black spatial-scale obstruction.

## Integrated results — 16 October 2026

The revision adds [birth-filtered feedback](proof/birth-filtered-feedback.md):
the first remote old lifetime created since the source checkpoint is totally
computable, with exact birth, consumption and complete XOR endpoint. Initially
black coordinates remain eligible after erasure and rebirth. On non-eventually-
translating orbits, uniform deadlines yield `Omega(sqrt(H)/log(H))` late-born
lifetimes at simultaneously growing radius and age. Complexity is polynomial
for fixed D and fixed K on explicit sparse input; the theorem is not uniform
polynomial in binary D or K's diameter.

## Manuscript and status

Version **0.1.0** is [published on Zenodo](https://doi.org/10.5281/zenodo.23665512). [Manuscript](paper/main.tex) ·
[Proof dependencies](PROOF.md) · [New-module verification](evidence/review-2026-10-16.json) ·
[Release and artifacts](release/README.md).

The first preprint is record **23665512**. Its exact PDF, source archive and
publication receipt are retained in [release/v0.1.0/](release/v0.1.0/).

## Exact scope

The next-event and fixed-region queries are total; iteration over every event need not terminate. S_D, J10 and physical gate events remain distinct. The twenty-cell family excludes a lifetime bound based only on D, intervening event count and initial mass; coordinates still encode its growing scale.

## Reproduce

```sh
python3 memory_feedback/reproduce.py --output-report /tmp/memory_feedback-review.json
make -C memory_feedback/paper
```

Run from the repository root, using Python 3.10+ without `-O`. Checks use disposable copies and retain the imported source and evidence. The manuscript uses XeLaTeX (DejaVu fonts). Builds write to `paper/build/`.

Use `--extensions-only` to replay just the 16 October additions. The default
continues to cover the complete main-paper dependency chain.

## Open

Independent mathematical peer review and journal preparation remain open.
