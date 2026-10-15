# Verification evidence

The analytic statements and proofs are in [PROOF.md](../PROOF.md) and the
[manuscript](../paper/main.tex). Exact checks supplement those arguments.

| Evidence | Scope |
|---|---|
| `check_results.json` | 3,200 full-state integer increments; 6,400 directional increments; 23,650 level identities; 4,992 period moments; 1,248 standard phase/rotation/power cases; small inverse NO |
| `standard_wake.json` | Explicit standard word, finite seed, full-drift wake classes and cutoff 856 |
| `audit.json` | 16 universal Laurent identities for forward and reciprocal clocks; no original implementation imported |
| `audit_integer.json` | 24 universal heading/colour/sign branches, including the centre; independent of the original clock implementation |
| `audit_trace.json` | Infinite certificates for all 416 phase/heading controls, required-seed mutations, a blocker 10^100 periods away and an inert marker |
| `detour_results.json` | Optional finite insertion experiment through length 28 and independent Python comparison through length 20 |

The first two reports and optional experiment are byte-identical imports from
research commit `9c50691`. Their embedded source hashes match the imported
`verification/wake.py`, `check.py` and search sources. The new algebraic audit
uses exact integer/Fraction coefficient arithmetic. Its small integer-clock
audit is also carried in the clock project so both archives remain standalone;
these two copies are the same audit, not two independent implementations.

The general cutoff proof combines whole-period cancellation, the known exact
word criterion and Cauchy--Schwarz. Search completeness follows from the finite
cutoff; a user resource cap returns INCONCLUSIVE. The negative control exhausts
all 32,766 nonempty words through its derived bound 14. The standard 856 search
has not been exhausted.

Run `python3 wake_synthesis/reproduce.py --search` to reproduce every retained
report without changing its bytes. These are exact computational and analytic
checks, not external peer review or a Lean proof.
