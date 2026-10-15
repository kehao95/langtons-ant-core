# Finite-Memory Prediction and Remote Feedback in Langton’s Ant

Total fixed-D old-black event prediction, exact full-history XOR continuation, quadratic finite-event budgets, endpoint tubes, fixed-region event filtering, remote long-lived feedback necessity, and the twenty-black spatial-scale obstruction.

## Manuscript and status

Version **0.1.0** is prepared for review. [Manuscript](paper/main.tex) ·
[Proof dependencies](PROOF.md) · [Fresh verification](evidence/review-2026-10-15.json) ·
[Release preparation](release/README.md).

This project has no Zenodo record yet. Its first-release materials are local.

## Exact scope

The next-event and fixed-region queries are total; iteration over every event need not terminate. S_D, J10 and physical gate events remain distinct. The twenty-cell family excludes a lifetime bound based only on D, intervening event count and initial mass; coordinates still encode its growing scale.

## Reproduce

```sh
python3 memory_feedback/reproduce.py --output-report /tmp/memory_feedback-review.json
make -C memory_feedback/paper
```

Run from the repository root, using Python 3.10+ without `-O`. Checks use disposable copies and retain the imported source and evidence. The manuscript uses XeLaTeX (DejaVu fonts). Builds write to `paper/build/`.

## Open

Review the prepared manuscript and standalone package before authorizing a Zenodo release. Independent mathematical peer review and journal preparation remain separate steps.
