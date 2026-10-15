# Critical-potential verification — 15 October 2026

The new proof supports square first exit by
`4 floor(3 R_n/16)+4 <= (13/4)3^n+4` and rectangular first exit by
`floor((9/2)(NH+16)(4N+1)^floor(H/2))+3`.
No mathematical counterexample or failure of either constant was found.
The results strengthen the existing clock paper. Software independence here
means separate implementations; this audit is not external peer review.

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

## Original package and fresh reproduction

The original `critical.py`, `check.py`, `symbolic_check.py`, `check_results.json`
and `symbolic.json` are retained byte for byte from the incoming research commit.
The standard-library checker reproduces its retained report exactly:

- 3,000 local identities and 6,400 four-update cases;
- 10,608 horizontal-arrival two-step cases;
- 144 rectangular and 12 square range cases;
- 28,808 complete initial states on eight small rectangles, with 86,584 updates;
- 80 exterior-field trajectories, with 575 updates, and eight invalid-input controls.

The additional symbolic audit is recorded in `audit.json`; source hashes and
fresh run metadata are in `reproduction.json`. The retained optional SymPy output
is supplementary history; the required new algebra audit uses no SymPy.
Run `python3 clock_escape/reproduce.py --critical-only` at the repository root.
The full reproduction command also includes the retained supercritical evidence.

## Proof and manuscript revisions

The original arguments are valid under the stated finite-state model. The audit
makes their extension to arbitrary exterior colouring explicit: the potential
sum is localized to the observation region, avoiding undefined infinite sums.
For finite complete fields this only subtracts a constant during confinement.
The constant-turn proof now states the common four-reward product 4^4/81,
and the rectangle argument spells out the binomial bound for (1+1/N)^N<3.
These refinements also land in the original proof and manuscript.

The integrated paper keeps the established title and orbit algorithms, replaces
the main square estimate with the stronger one, and adds the rectangular theorem.
The original published PDF remains unchanged; the eight-page `paper/review.pdf`
is the current revision. The new critical arguments have exact algebra checks,
but the existing Lean proofs still cover only the supercritical local lemmas.
No new Lean coverage is claimed.

The official Etse Theorem 12 comparison uses its parity-dependent degrees, not
just the abstract's coarser summary; see `../../paper/LITERATURE.md`. The lower
new degree for H>=6 is an asymptotic comparison, not a claim of optimal constants.

## Remaining work

External mathematical review and final literature checking before a versioned
update of the existing clock preprint. The new bounds estimate first exit;
they do not bound later re-entries or establish the global Highway Conjecture.
No Zenodo action is part of this integration.

## Publication follow-through

On 15 October 2026 the owner explicitly requested release. Version 0.3.0 was
published in the existing Zenodo chain. The exact reviewed PDF is now
`paper/paper.pdf`; version 0.2.0 is retained at `release/v0.2.0/paper.pdf`.
The uploaded archive passed full isolated reproduction, including the retained
Lean proofs; see [the release receipt](../../release/v0.3.0/publication-receipt.json).
The paragraphs above record the proof audit before that publication action.
