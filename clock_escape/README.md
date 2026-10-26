# Integer clocks and exponential escape

For every n-by-n square, arbitrary internal colouring and pose, and arbitrary
exterior colours, first exit including the exit move satisfies

`T <= E(n) = (13*3^(n-1)-2*n^2-4*n-5)/2`.

The leading term is **(13/6)3^n**. For N columns and fixed height H,

`T <= floor((9/2)(NH+16)(4N+1)^floor(H/2))+3`,

giving **O_H(N^(floor(H/2)+1))**. An integer clock with gain at least one
proves the square bound and gives complete-state reachability, orbit equivalence
and a computable orbit section. An anisotropic critical potential proves the
rectangular estimate.

## Paper and proof

Hao Ke, *An Ant on the Clock: Exponential Escape Bounds for Langton's Ant*.

- Published **0.4.0**: [Zenodo](https://doi.org/10.5281/zenodo.23402379),
  [exact PDF](release/v0.4.0/paper.pdf), [source](paper/main.tex),
  [proof](PROOF.md), [integer audit](evidence/integer/README.md).
- Previous **0.3.0**: [Zenodo](https://doi.org/10.5281/zenodo.23401306),
  [unchanged PDF](paper/paper.pdf), leading square coefficient 13/4.
- Earlier **0.2.0**: [Zenodo](https://doi.org/10.5281/zenodo.23341604),
  [unchanged PDF](release/v0.2.0/paper.pdf).
- [Critical audit](evidence/critical/README.md), [literature](paper/LITERATURE.md),
  [release records](release/README.md).

The publication remains in the existing concept DOI
[10.5281/zenodo.23341603](https://doi.org/10.5281/zenodo.23341603).
The new proofs are analytic with exact algebraic checks. Lean covers the
supercritical local identities and telescoping retained in the appendix.

## Reproduce

```sh
python3 clock_escape/reproduce.py --integer-only
python3 clock_escape/reproduce.py --critical-only
python3 clock_escape/reproduce.py
make -C clock_escape/paper
```

The scoped checks use Python 3.10+ and the standard library. Full reproduction
also runs the established clock evidence and Lean 4.30.0 local lemmas. The PDF
build uses pdfLaTeX and writes to `paper/build/`.
