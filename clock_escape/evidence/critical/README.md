# Critical-potential verification

The critical-potential proof gives square first exit by
`4 floor(3 R_n/16)+4 <= (13/4)3^n+4` and rectangular first exit by
`floor((9/2)(NH+16)(4N+1)^floor(H/2))+3`.
The symbolic audit uses a separately written implementation. The universal
claims follow from the analytic arguments and exact finite checks below.

## Claim-to-proof map

| Claim | Universal argument | Verification |
|---|---|---|
| Critical increment is one of four positive monomials | Eight local cases; residual has factor `(a-1)(b-1)-4` | Independent exact Laurent coefficients in four variables, before critical substitution |
| Every four steps cost at least 16/3 at a=b=3 | Opposite-turn integer-power inequality, or four-term AM-GM for a constant word | Eight opposite pairs, eight constant products and all 16 word classes |
| Half-centred square potential is rational | Rewrite with integer diagonal exponents x+y−(n−1), x−y | Four symbolic head decompositions and one field identity |
| Square exit bound | Fixed-sector range R_n and disjoint four-step blocks | Exact range simplification at 100 sizes; boundary rounding; original 12 square-range cases |
| Rectangle bound | Anisotropic range and horizontal-arrival pairs costing more than 4/3 | Eight symbolic pair cases, 200 short segment counts, original 144 range cases |
| Exterior colours do not affect first exit | Restrict the potential sum to the observation region; for finite complete fields exterior terms are constant | Original 80 complete-field trajectory cases |

`audit.py` imports neither `critical.py` nor a computer-algebra library. It
represents Laurent polynomials by integer exponent tuples and rational
coefficients. All eight residuals agree coefficient by coefficient with
`(U+1/U)(V+1/V)(ab-a-b-3)` after multiplying by `(a+1)(b+1)`.
Thus these checks are symbolic identities, not sampled parameter fits.
The ordinary inequality proofs, geometric sums and invariant-sector range
arguments remain the analytic proof in `../../PROOF.md`.

## Reproduction

The standard-library checker reproduces the retained report exactly:

- 3,000 local identities and 6,400 four-update cases;
- 10,608 horizontal-arrival two-step cases;
- 144 rectangular and 12 square range cases;
- 28,808 complete initial states on eight small rectangles, with 86,584 updates;
- 80 exterior-field trajectories, with 575 updates, and eight invalid-input controls.

The symbolic audit is recorded in `audit.json`. The optional SymPy output
provides a second symbolic check; the required algebra audit uses no SymPy.
Run `python3 clock_escape/reproduce.py --critical-only` at the repository root.
The full reproduction command also includes the retained supercritical evidence.

## Localization and proof scope

For arbitrary exterior colouring, the potential sum is localized to the
observation region, avoiding undefined infinite sums.
For finite complete fields this only subtracts a constant during confinement.
The constant-turn proof uses the common four-reward product 4^4/81,
and the rectangle argument spells out the binomial bound for (1+1/N)^N<3.

The critical bounds have exact algebraic checks. Lean covers the supercritical
local identities and telescoping; the critical proofs are analytic.

The comparison with Etse's Theorem 12 uses its parity-dependent degrees;
see [article bibliography](../../paper/main.tex). The degree comparison for H>=6
concerns asymptotic growth at fixed height.

The [article](../../paper/main.tex) presents the critical bounds alongside the
stronger [integer-clock bound](../integer/README.md).
