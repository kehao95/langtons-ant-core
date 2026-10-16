# Local Factor Rigidity and Mass–Defect Bounds for Langton’s Ant

Ten-factor eventual modes; finite-mass entry at most 12m+212 with sharp slope; polynomial bit-time exact first-J10 macros with complete compressed endpoints and quadratic finite-event deadlines; and the all-input inequality 3(t-s)-26(|B_t|-|B_s|) <= 351 N10(s,t)+322 with sharp additive constant.

## Integrated results — 16 October 2026

The revision adds [silent archive manufacture](proof/silent-archive-amplification.md):
a complete `(10n+41)`-black family produces `2(n+1)` lifetimes during a
J10-free prefix and consumes them later at J10 events. The related
[folded ribbon](proof/silent-fold-reset.md) has exact first P104 time
`152n+2527`, total intrinsic count `56n+926`, and reset flip cost at least
`max(0,4m-136)`. Their full-source geometry explains why the S_D endpoint
tube does not transfer to J10. The two families retain distinct future claims.

## Manuscript and status

Version **0.1.0** is prepared for review. [Manuscript](paper/main.tex) ·
[Proof dependencies](PROOF.md) · [New-module verification](evidence/review-2026-10-16.json) ·
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

Use `--extensions-only` to replay just the 16 October additions. The default
continues to cover the complete main-paper dependency chain.

## Open

Review the prepared manuscript and standalone package before authorizing a Zenodo release. Independent mathematical peer review and journal preparation remain separate steps.
