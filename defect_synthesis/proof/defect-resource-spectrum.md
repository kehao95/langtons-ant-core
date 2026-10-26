# Exact root-cost spectra and relational verification for defect schemas

The [complete development](../verification/defect_resource_spectrum/PROOF.md)
and [article source](../paper/main.tex) accompany the exact-integer compiler.
The resource refinements use the
[bounded-defect theorem](presburger-defect-reachability.md); neither result proves HC.

## 1. Exact whole-history relation

Let a supplied bounded-power schema have fixed pieces and heading-restoring
powers with arbitrary nonnegative integer exponents. Initial coordinates and
other parameters are unrestricted integers in an effective Presburger domain.
Time and position of each occurrence are affine in the parameters and its copy
index. There is no multiplication of two free variables.

Write V for time-to-cell and R,L for requested letter-time sets. Define

    C={(s,t):s<t and V(s)=V(t)},
    Next=C minus (C composed with C),
    First=Times minus range(C),
    Last=Times minus domain(C)   [finite traces only].

A pair belongs to C composed with C precisely when there is a same-cell read
strictly between its two endpoints. Thus Next is EXACTLY consecutive-read order.
For an explicitly supplied complete initial field B, realization is equivalent
to opposite letters on every Next pair and

    First intersect L = First intersect {t:V(t) in B}.

Necessity is the flip rule; sufficiency is induction in actual time, including
all writes inside long powers. The complete finite endpoint is

    (B minus V(Times)) union V(Last intersect R).

No unread initial cell is erased. An unspecified infinite trace may require
infinitely many initial black cells; the finite-support promise must be checked
separately. The program has an explicit control for this distinction.

## 2. Resource-spectrum theorem

**Theorem.** On the feasible parameter domain of EVERY supplied finite bounded-
power schema, its minimum initial-black cardinality c and its number d of wholly
contained nonstandard ten-factors have effective piecewise rational-affine
formulas on a finite Presburger partition. Their joint graph is semilinear.

Proof. The preceding relations are Presburger by finite unions, composition,
projection and complementation. The first-black cost is |First intersect L|;
different first-read times identify different physical cells. Defect end-times
are also Presburger: shift and intersect the ten letter-time predicates and
subtract the union for all standard factors.

It remains to count a finite fibre in ONE time variable. Eliminate quantifiers;
split all parameter and time residues modulo the constant congruence moduli.
After t=r+Qz, a disjoint Boolean cell constrains z by floors/ceilings of fixed
rational-affine parameter expressions. Refine by the order of these bounds and
constant-denominator residues. Every nonempty fibre piece is a bounded integer
interval with rational-affine endpoints. Its integer length is affine on the
refined domain. Sum disjoint lengths. This gives a finite effective partition
for both counts. QED.

The theorem is NOT an affine-cardinality statement for arbitrary two-dimensional
Presburger sets; an n-by-n square has n^2 points. It is unary first-time counting.
The implementation computes exact time sets and supplied INTEGER thresholds.
A general optimized symbolic counting-partition engine is not claimed built.

For a supplied finite schema collection and fixed mass budget, unboundedness
of the defect count is therefore decidable. If unbounded, a linear component
of its semilinear parameter/count graph supplies an affine family of FINITE
witnesses. This does not give one fixed infinite ant input.

## 3. Exact two-fold example

For the explicit A28 and B102 from the retained ten-factor proof,

    B A^n B A^m is feasible iff n>=1 and 0<=m<n,
    minimum initial-black cost = 5n+5m+47.

The entire parameter region is checked by exact integer-set equality, not
finite samples. The first B has 24 first-L reads, the second 23; every A copy
in either run has precisely five, at local phases 0,9,15,26,27. The compiler
checks equality with the complete First-intersect-L time set. Full phase lists
are in Section 8 of the accompanying proof. These disjoint first times establish
the exact cost. The earlier triple-fold impossibility is independently recomputed
as a control, not claimed newly discovered.

## 4. Fixed-budget global coverage and its limit

The inherited J10 lift is independently reconstructed here: all 6605 feasible
150-letter words, 6501 base vertices, 7595 lifted vertices and 7763 edges.
Every defect-free finite segment has at most five fixed-word powers and a
constant-size literal remainder. For clarity, a prefix ending at its Nth
contained defect is split by REMOVING the N defect-producing letters. There
are N preceding, possibly empty, contiguous pieces; there is no suffix after
the final defect. None of those pieces has an internally contained defect,
since its ending letter would have been removed. Apply the cover separately
and reinsert those N single letters. This justifies the safe bounds 5N powers
and 9+2000N fixed letters used by our conservative generator.

This is consistent with the slightly larger N+1 cover in the parallel theorem,
which also treats arbitrary endpoints after at most N defects. There is no
conflict of event definitions: both count forward-contained windows, not the
first nine inverse-history J10 tests.

The resulting all-coordinate finite-budget relation and computability of mu(N)
are established by the bounded-defect theorem. The existence of a
finite complete schema collection is proved; its nontrivial global disjunction
has NOT been fully traversed. Caps return INCONCLUSIVE. Neither semilinearity
nor computability of mu proves that mu diverges or that infinite intersections
of the nested seed domains are empty.

## 5. Evidence and trust

The source package's full disposable replay passed: 255 short literal words,
48 powered schemas/768 parameter assignments, universal two- and three-fold
relations, complete three-sweep endpoints, all-coordinate marker guards,
26 exact count-threshold identities and explicit invalid/infinite-support controls.
The final unpacked distribution was also replayed. The complete retained graph
was rebuilt rather than taken from a sample. Source hashes fix the tested files.

Both relational formulations use libisl/GMP. Independent vector-rotation finite
replay corroborates them, but no independently proof-checked elimination witness,
Lean proof or outside mathematical review is claimed. Arithmetic failures are
not NO answers.
