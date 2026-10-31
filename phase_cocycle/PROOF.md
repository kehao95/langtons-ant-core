# Proof and evidence map

The [complete article](paper/main.tex) provides all definitions and proofs.

| Claim | Universal argument | Computational controls |
|---|---|---|
| Forced additivity of arbitrary coloring function | One-cell finite differences independent of every other color | Raw all-color transition equations |
| Complete mixed-rule presentation | Eight local transitions, square circulations and planar path integration | Explicit construction and exact matrix checks |
| Sharp phase order | Torsion necessity and four-periodic attaining coefficients | Smith normal forms; direct modulo-16 updates |
| Compact-charge basis | Finite-support cycles on the rotated square grid; unique finite plaquette decomposition | Kernel dimensions and independent plaquette controls |

All statements quantify over every complete finite coloring and every pose
in the specified checkerboard sector. Compact charges refer to finite support
of the coloring coefficients. The proof is analytic; exact computational
controls check its formulas and finite consequences. SymPy 1.14.0 is used for
the exact matrix audit; Python and C++ execute separate literal dynamics.
