# Finite-Memory Prediction and Remote Feedback in Langton’s Ant

Total fixed-D old-black event prediction, exact full-history XOR continuation, quadratic finite-event budgets, endpoint tubes, fixed-region event filtering, remote long-lived feedback necessity, and the twenty-black spatial-scale obstruction.

## Constructions and algorithms

The construction gives [birth-filtered feedback](proof/birth-filtered-feedback.md):
the first remote old lifetime created since the source checkpoint is totally
computable, with exact birth, consumption and complete XOR endpoint. Initially
black coordinates remain eligible after erasure and rebirth. On non-eventually-
translating orbits, uniform deadlines yield `Omega(sqrt(H)/log(H))` late-born
lifetimes at simultaneously growing radius and age. Complexity is polynomial
for fixed D and fixed K on explicit sparse input; the theorem is not uniform
polynomial in binary D or K's diameter.

## Article

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof](PROOF.md) ·
[Reproduction details](evidence/README.md) · [Zenodo](https://doi.org/10.5281/zenodo.23675969)

## Exact scope

The next-event and fixed-region queries are total; iteration over every event need not terminate. S_D, J10 and physical gate events remain distinct. The twenty-cell family excludes a lifetime bound based only on D, intervening event count and initial mass; coordinates still encode its growing scale.

## Reproduce

```sh
python3 memory_feedback/reproduce.py --output-report /tmp/memory_feedback-checks.json
make -C memory_feedback/paper
```

Run from the repository root, using Python 3.10+ without `-O`. Checks use disposable copies and retain the imported source and evidence. The manuscript uses XeLaTeX (DejaVu fonts). Builds write to `paper/build/`.

Use `--extensions-only` to replay just birth-filtered feedback. The default
continues to cover the complete main-paper dependency chain.
