# Small witnesses for bounded-defect Langton dynamics

15 October 2026. Mathematical base: `6afea97c2a8a26d03b2bf89de9d23a87d64a31e0`.

**Status:** complete written analytic argument, not formalized or externally reviewed. This strengthens the existing all-coordinate fixed-defect semilinearity theorem; it is not a second claim to that result. The executable implementation was run locally, but two source-file write requests failed at the tool safety-status layer. This commit records the proof and does NOT claim that a runnable new module has been saved remotely. The full source, reports, six-page manuscript and standalone proof are retained in `langtons-ant-defect-small-witnesses-2026-10-15.zip` delivered with the research session. No existing source or concurrent result is overwritten.

## 1. Exact question and theorem

Use the classical finite-support LR ant on Z^2, initially at the origin heading north. Let W be the fixed standard P104 word and L10 its cyclic ten-letter factors. For a finite forward word w, d10(w) counts forbidden factors WHOLLY contained in w. It is not the intrinsic inverse-history J10 count on the first nine input updates.

Let E(m,N) assert that some COMPLETE initial set of at most m black cells produces at least N contained defects. All source coordinates are quantified over Z; no geometric promise is imposed. For m>=0,N>=1 put

    s=5(N+1), K=2570(N+1), d=s+2m,
    H=2^24(K+d+1), R=64((d+1)! H^d+1).

**Small-witness theorem.** If E(m,N), there is a witness with every initial coordinate and every exponent of a bounded-power description at most R in absolute value. Its Nth contained defect occurs within K(R+1) literal updates. In particular log R=O((m+N+1)log(m+N+2)).

**Complexity corollary.** With m,N in UNARY, E belongs to NP. The minimum initial cardinality mu(N) can be computed in deterministic time 2^O(N^2 log(N+2)). No NP-hardness, new mu value, mu divergence, arbitrary-seed event deadline or HC conclusion is claimed.

The radius is for SOME positive witness, generally a different input, not for every given input. This distinction is essential: an initially black marker arbitrarily far ahead of a standard highway gives fixed-cardinality inputs with arbitrarily late first defects.

## 2. Inherited finite cover, with its coefficients retained

The complete bounded-defect cover in `presburger-defect-reachability.md`, Sections 2-4, gives every feasible word with at most N defects a schema

    v0 u1^k1 v1 ... uq^kq vq,
    q<=5(N+1), sum |vj|<=2048(N+1)+N.

The uj are from the 156 cyclic phases of W104, U28 and T24. All restore heading, are cyclically ten-legal and have nonzero drift. Zero powers are allowed. Fixed vj are explicit words and can rotate the heading. A positive E witness may be stopped at its Nth defect, giving exactly N. The historical flat-cover proof is a dependency; it was not reopened or claimed rerun here.

There are at most K phase types: one for each fixed letter or each phase of a powered word. A type has position A_i(k)+a D_i and time T_j(k)+i+|uj|a, with 0<=a<kj. Its anchor is affine in earlier independent exponents. The nonzero strides, after rotations, are exactly

    D={(+/-2,+/-2),(+/-2,0),(0,+/-2),(+/-4,0),(0,+/-4)}.

A fixed letter is a singleton type. Repeated zero-drift bodies are not allowed by this cover. This is a finite description cover for finite-budget prefixes, not a finite-state quotient of unlimited ant dynamics.

## 3. Polynomial exact verification of the full colour history

At a proposed read, its actual colour is initial membership XOR the parity of ALL preceding prescribed reads at the same cell. A nonzero-stride type visits a given cell at most once, so each earlier type contributes one bit on a set of current occurrence indices.

For two types solve A+aD=B+bE. Nonparallel strides give at most one integral pair by determinants; every nonzero determinant of the fixed strides divides 16. Parallel strides give, after collinearity, a fixed-coefficient one-dimensional equation. The resulting set of current indices is an interval in one residue class modulo |E_j|/gcd(D_j,E_j), at most two. Initial points and fixed singleton types contribute at most one index. All endpoints use affine expressions, comparisons, and floors/ceilings by fixed constants.

Different blocks are chronologically ordered. In the SAME powered block, meeting phases have indices b=a+c with constant c, and earlier/later is determined by the constant |u|c+old_phase-current_phase. No actual previous-write contribution is removed. A repeated phase has nonzero stride and never revisits its own cell.

Split the current index by the least common multiple of all hit moduli, at most two. Each toggle is now an ordinary finite integer interval. Sort starts and one-past-ends; colour is constant between consecutive distinct endpoints. Check every nonempty interval against the required phase bit. All initial black points enter the XOR, including remote and untouched points.

Induction on actual update time proves sufficiency of all colour checks. Necessity is the flip rule. There are O(K(K+m)) pair/point queries and O(K(K+m)log(K+m)+m^2) comparisons, on binary numbers of polynomial bit length. Thus execution validity is checked in polynomial bit time without expanding powers. Complete output membership is initial membership XOR all phase segments, rather than an unguardedly cleaned endpoint.

A word summary records length, first/last nine symbols and contained-defect count. Concatenation checks only crossing factors; binary powering is logarithmic in the exponent. Furthermore, in THIS library every body has length >=24, fixed positive-power boundary contexts and no internal defects. Once each exponent is fixed as zero or positive, the schema's total contained-defect count is constant.

## 4. Linear execution chambers

Let theta list q independent exponents and both coordinates of m' distinct source cells, with q+2m'<=d. For one successful witness fix residues rho modulo 64 and write theta=64z+rho, 0<=rho_i<64.

Follow the exact verifier on affine forms in z. Record every comparison with its witnessed outcome, converting strict integer comparisons to non-strict inequalities with a unit shift. For equality record both inequalities; for a failed equality choose its witnessed strict sign. Also record source distinctness, nonnegative exponents and zero/positive cases. The outcomes in min/max, sorting and grouping equal endpoints are all included.

All modular tests become constant. Nonparallel denominators divide16, point-membership denominators divide4, parallel index steps have magnitude1 or2, and the parity split divides by at most2. Their largest accumulated divisor divides32, hence64. Every floor/ceiling remains affine: only the constant term is rounded. No parameter is a divisor or determines the number of checker iterations.

The recorded conjunction is nonempty because it contains the original witness. Every integer solution follows the same finite comparison path. It preserves all interval parity checks, initial distinctness and the exponent-zero pattern. Hence it preserves physical feasibility and the exact contained-defect count. The conjunction need only be a sufficient chamber through this witness; no complete chamber decomposition is assumed.

Here is an explicit coefficient envelope. Set H0=2^8(K+d+1). After theta=64z+rho, each origin has variable coefficients <=256 and constant <=K+252q; source coordinates and counts fit H0. An origin difference has height <=2H0. A determinant numerator has height <=16H0 and its quotient <=16H0+1. Parallel hit endpoints fit 4H0+16; after parity splitting and adding a successor every endpoint fits16H0+32. The bound follows by dividing an origin difference by a stride, dividing range endpoints by a relative step of magnitude1 or2, and multiplying back by a modulus at most2. Min/max selects an existing form, not a sum of an unbounded list. Comparing endpoints or checking point collinearity and ranges fits128H0+128. Within-body anchor differences cancel the parameters entirely. Thus every recorded coefficient and constant is below256H0<=2^16(K+d+1), and certainly below the conservative H above. The number of guards is polynomial by Section3.

These bounds concern canonical schemas with independent exponents and free source coordinates. An arbitrary user-specified affine family may have larger coefficients; its actual chamber height must be used instead. There is no bound here independent of arbitrary extra coefficient input.

## 5. Small integer solutions and the two complexity conclusions

Use the classical integer small-solution theorem: if Az<=b has an integer solution in n variables and every coefficient and right-hand side has magnitude <=a>=1, then it has a solution with |z_i|<=(n+1)!a^n. This is the Schrijver bound explicitly stated and formally verified in Bottesch--Haslbeck--Reynaud--Thiemann, NFM2020, DOI 10.1007/978-3-030-55754-6_14, Sections1 and3. It has no dependence on the number of inequalities. The external formalization is NOT a formalization of this ant theorem.

Apply the bound to the nonempty chamber. Using n<=d,a<=H gives |z_i|<=(d+1)!H^d. Substitution theta=64z+rho proves the radius R. All inequalities, including distinctness and nonnegativity, remain valid. The word still has exactly N defects and duration <=sum|vj|+sum|uj|kj<=K(R+1). Taking logarithms yields the asserted bit bound.

For unary budgets, guess the schema, source points and exponents within these bounds. They occupy O((m+N+1)^2 log(m+N+2)) bits. Check library membership, schema size, full colour execution and contained defects by Section3. This proves NP membership. A failed guess is not a global negative answer.

Exhaustively enumerating this bounded certificate space gives deterministic time 2^O((m+N+1)^2 log(m+N+2)). The inherited word (LRRL)^k needs 2k initial black cells and has max(0,4k-9) contained defects, so mu(N)<=2 ceil((N+9)/4)=O(N). Testing m through that bound gives 2^O(N^2 log(N+2)) computation of mu. This is an algorithmic upper bound, not a completed global enumeration or numerical mu table.

Short schemas plus small integer solutions are established methodology in flat-counter verification: Demri--Dhar--Sangnier, Information and Computation242 (2015), 306-339, DOI 10.1016/j.ic.2015.03.007. The new ant-specific obligation is the exact mutable-field interval and affine-chamber argument, not a claim to those general tools or to the existing semilinearity theorem.

## 6. Executed checks and the HC boundary

A standard 17-black phase plus marker (-2n,-2n) executes W^n L at n=10^60+1, with one contained defect and 104n+1 updates. The compressed check uses105 phase types,366 phase-pair queries,1890 initial-point queries and168 constant-parity checks. It does not simulate 10^62 steps. Its three-parameter chamber has residues (1,62,62),29 guards and coefficient bound128. The same chamber contains (65,-130,-130), producing another 18-black input with exactly one defect in6761 updates. This is a changed source, not acceleration of the same physical run. The remote-marker mechanism is prior work; the chamber reduction is the new control.

The final locally executed suite checks all156 library bodies,1152 intersections,1228 traces against an independent integer-vector simulator,10841 complete endpoint membership queries,300 summary-monoid cases,2000 raw chamber tests, a second two-loop chamber and explicit invalid-certificate controls. Reports regenerate byte for byte. No full nonzero-budget global schema search, new mu value, old broad regression, Lean build or external review is claimed.

The result removes arbitrary coordinate magnitude from the SIZE of a positive finite-budget certificate. HC still requires finite event counts on each fixed input; mu(N)->infinity is not proved. Nonempty witness families can move with N without supplying one infinite counterexample. The theorem gives no total HIGHWAY decider and no nonstandard periodic or aperiodic seed.

Before this direction a finite nine-factor experiment yielded a large nonsimple cyclic component; nine-factor finite-support attraction remains unproved. That experiment is not a premise here. The natural publication plan is to strengthen the existing fixed-defect manuscript, not to issue overlapping semilinearity claims.

**Persistence boundary.** This proof note is the remote part of the current work. The full six-page draft, exact source, frozen checks and small-chamber data remain in the delivered standalone package because source-upload requests were blocked by the tool before a full module commit. Do not claim that a new repository replay command is available until those files are successfully installed. Concurrent research through the current branch is preserved.
