# Local Factor Rigidity and Mass–Defect Bounds for Langton’s Ant

Ten-factor eventual modes; finite-mass entry at most 12m+212 with sharp slope; polynomial bit-time exact first-J10 macros with complete compressed endpoints and quadratic finite-event deadlines; and the all-input inequality 3(t-s)-26(|B_t|-|B_s|) <= 351 N10(s,t)+322 with sharp additive constant.

## Finite intervals and nine-factor mass bounds

Every finite physical ten-legal word has one contiguous standard core, with
at most `114c+154693` remaining letters. Its length obeys
`L <= 52 norm_inf(displacement) + 114c + 223437`, with sharp coefficient 52;
c is the minimum first-read black supply, bounded by the segment's complete
starting mass. A closed silent return therefore has a linear starting-mass bound.
The exact next-J10 algorithm uses one standard jump and O(m+1) literal updates
on explicit m-point inputs. Repeated intervals use their own starting masses.

The separate nine-factor bound is `deficit <= 1004`, giving
`deficit <= 1033 N9 + 1004` on all intervals. Finite eight-legal prefixes have
unbounded deficit, proving nine is the least window for this type of mass bound.
This does not lower the ten-factor threshold for arbitrary-colouring attraction.
[Proof map](PROOF.md) · [Verification](evidence/README.md).

## Constructions and algorithms

The construction gives [silent archive manufacture](proof/silent-archive-amplification.md):
a complete `(10n+41)`-black family produces `2(n+1)` lifetimes during a
J10-free prefix and consumes them later at J10 events. The related
[folded ribbon](proof/silent-fold-reset.md) has exact first P104 time
`152n+2527`, total intrinsic count `56n+926`, and reset flip cost at least
`max(0,4m-136)`. Their full-source geometry explains why the S_D endpoint
tube does not transfer to J10. The two families have different seeds and recovery formulas; the reset bound belongs to the folded ribbon.

## Recovery and geometry

The original `10n+41`-black producer has complete all-parameter recovery:
first entry is `550n+6714` for even `n>=10`, `712n+11087` for odd `n>=17`,
with twelve explicitly checked remaining cases. Every finite ten-legal physical
interval also lies in a single endpoint coordinate strip with padding 43;
consecutive events localized in K have an axis-cross container with padding 44.
[Verification](evidence/README.md) covers both additions.

## Article

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof](PROOF.md) ·
[Reproduction details](evidence/README.md) · [Zenodo](https://doi.org/10.5281/zenodo.23844669)

## Exact scope

The attraction bound assumes every future ten-window is legal. The mass–defect inequality applies to every finite-support orbit interval independently of that promise. The nine-legal counterexample to arbitrary-colouring attraction uses an infinite background. The eight-legal mass-deficit witnesses are finite prefixes realizable from finite support.

## Reproduce

```sh
python3 factor_language/reproduce.py --output-report /tmp/factor_language-checks.json
make -C factor_language/paper
```

Run from the repository root, using Python 3.10+ without `-O`. Checks use disposable copies and preserve the source and evidence. A C++17 compiler is required. The manuscript uses XeLaTeX (DejaVu fonts). Builds write to `paper/build/`.

Use `--new-results-only` for the silent-supply and nine-factor checks.
`--extensions-only` skips the original attraction/event/mass kernels and runs
all later additions. The default covers the complete main-paper chain.
The entrypoints stage their dependencies in disposable directories.
