# Proof and evidence map

## Six cells and a uniform resource bound

With head at (0,0) facing north, let the complete initial black set be
`{(-87,-55),(-87,-52),(-84,-55),(-82,-61),(-81,-55),(-80,-60)} + k*(-2,-2)`
for any integer k>=0. The entire future contains exactly `6702+47k` forward
length-ten defects and `6706+47k` intrinsic J10 events. The first permanent
standard trace begins at `18743+220k`. Thus the minimum initial mass needed to
produce at least N defects satisfies `mu(N)<=6` for every N>=1.

The article's six-cell proof constructs the complete word
`C W_*^(32+k) U V^k Z O^omega`, where W_* is the phase-57 left rotation of the article's Appendix A word. A 116-step XOR recurrence retains a 140-cell
archive at each repeat. Integer half-ray guards isolate every archive from the
whole recovery and periodic future. Finite suffix-register identities count all
seams, and the last disagreement with the periodic backward extension gives
first entry. The initial shape has fixed diameter 9; its distance from the head
grows with k. The theorem is a family of finite trajectories with eventual P104.

[Certificate and checker](verification/six_cell_feedback/) supply the literal
words, complete fields, independent C++ replay and exact ray tests.
`python3 defect_synthesis/reproduce.py --six-cell-only` checks this added chain.
The existing semilinear synthesis and scoped complexity theorems remain the
algorithmic basis for minimum-cost questions; the construction bounds the mass
search range, without asserting that six is minimal.


| Result | Mathematical bridge | Executable support |
|---|---|---|
| All-coordinate fixed-defect synthesis | [Bounded-fold cover and physical relation algebra](proof/presburger-defect-reachability.md); first reads fix source bits, consecutive visits alternate | `verification/presburger_defects`; all-parameter identities and independent literal controls |
| Complete outputs and resource spectra | [Unary finite-fibre counting](proof/defect-resource-spectrum.md); unread input union last-right output | `verification/defect_resource_spectrum`; exact alternate successor algebra and rebuilt cover |
| Fixed-collection dichotomy and sharp supply | [Semilinear generators and full three-parameter domain](proof/flat-schema-supply-dichotomy.md) | `verification/schema_supply`; exact relation equality and independent C++ controls |
| Unary NP and small witnesses | [Interval verifier, residue-64 chambers and integer small solutions](proof/defect-small-witnesses.md) | Analytic proof; original optional implementation archive absent, no fresh controls claimed |
| Fixed-schema query optimization | [Unary strict-order powers and Boolean factor DAG](proof/defect-compiler-optimization.md) | `verification/defect_compiler_optimization`; exact baseline equivalence, invalid-input controls |

The [quantifier-free refinement](proof/quantifier-free-defect-complexity.md) is
based on three obligations: the stride-1/2 residue
intersection lemma, parity-boundary elimination of universal reads and shared
suffix-register factor counting. Complete coverage then gives unary NP with
binary side constraints and an FP^NP minimum-cost corollary. The new theorem
does not extend that complexity guarantee to arbitrary quantified sources or
complete-field target equality.

Z3 and ISL/GMP remain native trust dependencies; UNSAT outputs are
not accompanied by independently checked proof objects. Benchmarks remain
historical timing evidence, not correctness replay targets. The original
optional small-witness implementation archive remains absent.

The finite cover inherits the all-parameter three-fold physical obstruction.
Its [ten-factor proof](proof/ten-factor-attraction.md) and
[event-macro proof](proof/ten-event-macros.md) are bundled; the resource module
independently reconstructs the covering graph. This archive needs no sibling
research checkout. The companion factor paper remains the main owner of those
upstream theorems.

The article presents a physical synthesis theorem and its resource consequences. The resource dichotomy is a consequence of semilinearity; its explicit
sharp three-parameter application is a separate theorem within the same paper.
The small-witness bound applies to canonical schemas with free source coordinates,
not arbitrary coefficient-sized affine families.

No universal nonzero-budget disjunction or numerical μ table was computed.
