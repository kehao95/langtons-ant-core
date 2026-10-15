# Wake-determined periods and inverse synthesis

Given a non-axis drift, an initial heading and a finite set of odd translation
classes, one can decide whether any periodic finite-support realization exists,
without specifying its period. A positive answer constructs a word and finite seed.

For diagonal drift, the integer clock gives `P<=K_c(O)` and a crossing recurrence
sharpens the cutoff. With wake growth g and width W, `P<=g(3^(W/2)-1)`.
For general non-axis drift, reciprocal wake moments give
`P^2<=A_+ A_-/kappa^2`. The standard wake has cutoff 856 and a certified
104-step witness; enumeration of the full 856 domain remains open.

## Paper and proof

Hao Ke, *Reading the Wake: Period Bounds and Inverse Synthesis for Langton's Ant*.

- [Zenodo 0.1.0](https://doi.org/10.5281/zenodo.23402422),
  [published PDF](release/v0.1.0/paper.pdf), [LaTeX source](paper/main.tex), [proof](PROOF.md).
- [Evidence and exact audit](evidence/README.md), [literature](paper/LITERATURE.md).
- [Release records](release/README.md): published first preprint, version 0.1.0.

The integer clock's primary treatment belongs to [clock and escape](../clock_escape/).
This paper develops its wake budgets, general non-axis moments, inverse algorithm
and closed-pose insertion corollary. The finite-word realization criterion is
credited to Jillhewar. The proofs are analytic, with exact implementation and
coefficient checks; this project has no Lean formalization.

## Reproduce

```sh
python3 wake_synthesis/reproduce.py
python3 wake_synthesis/reproduce.py --search
make -C wake_synthesis/paper
```

Python 3.10+ and the standard library suffice for the main checks. The optional
finite detour experiment also needs g++ with C++17. Reproduction works in a
disposable directory and compares retained reports. The project is self-contained.

## Open

Version 0.1.0 is published as record 23402422, with verified public downloads.
External mathematical review of the cutoff and completeness arguments remains
a next step. Classifying every realization of the standard wake remains an
open computational problem.
