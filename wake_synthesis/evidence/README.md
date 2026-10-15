# Verification evidence

The analytic statements and proofs are in [PROOF.md](../PROOF.md) and the
[manuscript](../paper/main.tex). Exact checks supplement those arguments.

## Standard-wake uniqueness — version 0.2.0

The [standard-wake evidence](standard_wake/) accompanies the complete
classification of periodic realizations with the twelve specified odd classes
and full drift `(2,-2)`.

| Evidence | Scope |
|---|---|
| `standard_wake/provenance.json` | Research provenance and SHA256 of every imported verifier source |
| `standard_wake/counts.json` | Independent binary-string count controls, modulo-four residue induction, and matching minimum-104 computations in both directions |
| `standard_wake/rank-pruning.json` | Retained first rank-pruning comparison: 40,227,976 to 12,193,595 prefixes at cap 168 |
| `standard_wake/upper-pruning.json` | Closed-walk-preserving deletion certificate; 24,424 states and all 37,330 integer edge inequalities, giving `P<=168` |
| `standard_wake/partial-embeddings.json` | 4,000 independently generated partial-cycle embeddings, including unbuilt phases and periods smaller than the cap; native undefined-behavior checks |
| `standard_wake/chain-separation.json` | Complete refined enumeration; independent contiguous-chain controls, exact seed and interruption controls; baseline comparisons |

The degree-deletion checker verifies the proposed deletion order by reverse
insertion. Every original edge between retained vertices is included in the
potential check. The exact search keeps both residues, stable class ranks,
full-chain lengths and translation voltages. A successful run must end with
`status=complete`; a node limit is checked to return an incomplete status.

The new chain rule uses the fact that different fixed chains occupy disjoint
contiguous time intervals. Their stable ordering therefore separates the entire
chains, strengthening the previous event-to-event inequalities. Its written
proof appears in [PROOF.md](../PROOF.md) and the manuscript.

## Retained general synthesis evidence — version 0.1.0

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
all 32,766 nonempty words through its derived bound 14. The general binary-word search at cutoff 856 is retained as the original
algorithm. The specialized standard-wake proof now derives the smaller bound
168 and exhausts its exact event representation, completing that classification.

Run `python3 wake_synthesis/reproduce.py --baseline --search` to reproduce
the new certificates, both preceding enumeration engines, and the optional
retained detour experiment without changing evidence files. Omit the two flags
for the default complete uniqueness check and general algebraic audits. These are exact computational and analytic
checks, not external peer review or a Lean proof.
