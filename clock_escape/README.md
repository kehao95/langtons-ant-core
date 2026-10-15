# Rational clocks and exponential escape

For an axis-aligned square of n cells per side, first exit satisfies

`T <= 4 floor(3 R_n / 16) + 4 <= (13/4) 3^n + 4`,

where `R_n = 13*3^(n-1) - 6 - 3^(2-n)`. This improves the previous
`8*n*3^n+1` estimate to **O(3ⁿ)**. For N columns and fixed height H,

`T <= floor((9/2)(NH+16)(4N+1)^floor(H/2)) + 3`,

giving **O_H(N^(floor(H/2)+1))**. Both bounds include the exit move and
cover every internal colouring and pose, with arbitrary exterior colours.

The critical potential has positive local increments and uniformly positive
short-block costs. A related rational clock also gives decidable complete-state
reachability, orbit equivalence and a computable orbit section.

## Paper and proof

Hao Ke, *An Ant on the Clock: Exponential Escape Bounds for Langton’s Ant*.

- Published version **0.3.0**: [Zenodo](https://doi.org/10.5281/zenodo.23401306),
  [PDF](paper/paper.pdf), [source](paper/main.tex) and [proof](PROOF.md).
- Previous version **0.2.0**: [Zenodo](https://doi.org/10.5281/zenodo.23341604)
  and its unchanged [PDF](release/v0.2.0/paper.pdf).
- [Critical proof audit](evidence/critical/README.md),
  [literature comparison](paper/LITERATURE.md) and [release records](release/README.md).

The stronger result is a new version of the same preprint, sharing concept DOI
[10.5281/zenodo.23341603](https://doi.org/10.5281/zenodo.23341603).

## Reproduce

From the repository root:

```sh
python3 clock_escape/reproduce.py --critical-only
python3 clock_escape/reproduce.py
make -C clock_escape/paper
```

The first command checks the new critical proof with Python 3.10+ and the
standard library. It reproduces retained reports in a disposable copy and
checks all eight identities by independent exact polynomial arithmetic.
The full command additionally reproduces the established clock evidence and
Lean 4.30.0 local lemmas. The PDF build uses pdfLaTeX and writes `paper/build/`.

The new global range and block arguments are analytic. Lean continues to cover
the supercritical local algebra and telescoping, as documented in the
[earlier audit](evidence/README.md); it does not formalize the new bounds.

## Open

External mathematical review of the stronger square and rectangular estimates,
and journal preparation. Accumulate later revisions for deliberate versioned releases.
