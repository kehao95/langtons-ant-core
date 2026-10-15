# Local Factor Rigidity and Mass–Defect Bounds for Langton’s Ant

Ten-factor eventual modes; finite-mass entry at most 12m+212 with sharp slope; polynomial bit-time exact first-J10 macros with complete compressed endpoints and quadratic finite-event deadlines; and the all-input inequality 3(t-s)-26(|B_t|-|B_s|) <= 351 N10(s,t)+322 with sharp additive constant.

## Manuscript and status

Version **0.1.0** is prepared for review. [Manuscript](paper/main.tex) ·
[Proof dependencies](PROOF.md) · [Fresh verification](evidence/review-2026-10-15.json) ·
[Release preparation](release/README.md).

This project has no Zenodo record yet. Its first-release materials are local.

## Exact scope

The attraction bound assumes every future ten-window is legal. The mass–defect inequality applies to every finite-support orbit interval independently of that promise. The nine-factor threshold example uses infinite background. Older 21/14/13 immediate thresholds await their full source package and are not dependencies.

## Reproduce

```sh
python3 factor_language/reproduce.py --output-report /tmp/factor_language-review.json
make -C factor_language/paper
```

Run from the repository root, using Python 3.10+ without `-O`. Checks use disposable copies and retain the imported source and evidence. A C++17 compiler is required. The manuscript uses XeLaTeX (DejaVu fonts). Builds write to `paper/build/`.

## Open

Review the prepared manuscript and standalone package before authorizing a Zenodo release. Independent mathematical peer review and journal preparation remain separate steps.
