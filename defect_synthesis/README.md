# Counting Defects: Semilinear Reachability and Resource Bounds for Langton's Ant

[PDF](paper/paper.pdf) · [Source](paper/main.tex) · [Proof](PROOF.md) ·
[Evidence](evidence/README.md) · [Zenodo](https://doi.org/10.5281/zenodo.23819737)

## Results

- All-coordinate synthesis for each fixed mass and forward ten-factor defect budget is effectively semilinear, with exact event times and complete endpoint fields.
- Supplied finite collections of powered-word schemas have effective resource spectra and piecewise rational-affine first-black costs. The three-parameter supply family has the sharp inequality `10D<=9C-309`.
- A fixed six-cell shape, translated by any integer k>=0, produces exactly `6702+47k` forward defects before permanent P104, with first entrance `18743+220k`. Consequently `mu(N)<=6` for every N>=1.
- Positive witnesses have polynomial bit length for unary budgets. The restricted quantifier-free backend supports binary linear side conditions and an FP^NP minimum-cost upper bound.

## Reproduce

```sh
python3 defect_synthesis/reproduce.py
python3 defect_synthesis/reproduce.py --six-cell-only
make -C defect_synthesis/paper
```

Python 3.10+, C++17, Z3, ISL/GMP and pdfLaTeX. Run without Python `-O`.

The full replay includes the six-cell recurrence and independent C++ controls, the supplied-schema modules, and all six quantifier-free backend sections. `--new-results-only` runs the quantifier-free backend together with the six-cell module.

The scoped second command checks only the corresponding added theorem. Each
entrypoint preserves retained evidence and uses disposable working copies.
`sources.json` binds the article, proof and verifier files.

## Scope

Forward contained ten-windows and intrinsic J10 events have different initial-history conventions. Six is an upper bound, not a minimality claim. Complexity statements use the stated restricted input model; the general semilinear theorem also covers quantified sources. The original optional small-witness implementation is absent; its proof is analytic.
