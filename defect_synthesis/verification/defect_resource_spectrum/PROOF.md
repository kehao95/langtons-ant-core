# Effective semilinearity at every fixed defect budget for Langton's ant

15 October 2026 (America/New_York). Research base:
`kehao95/langtons-ant@2f6010a6bbccf5d342648f1c730a8bd2ea628961`.

**Evidence and attribution.** The results below are written mathematical proofs,
with an executable exact-integer supplied-schema kernel and explicit parametric
controls. They are not Lean-formalized or externally refereed. Presburger
elimination and the imported ten-factor flat cover are explicitly identified
premises. The whole all-coordinate schema disjunction is effective but is NOT
reported as having been expanded for a nontrivial event budget. No HC proof,
finite counterexample, general termination algorithm, or priority claim is made.

The repository's `proof/research-global-all-coordinate-budget-2026-10-15.md`
already proposed the fixed-budget Presburger corollary. This work does not
claim that proposal as a new idea. It supplies an exact relational realization,
rechecks its flat-cover dependency, treats complete output fields, proves the
piecewise-affine first-black-cost refinement, and implements the finite-schema
queries. The earlier `proof/semilinear-trace-lifting.md` treated fixed literal
words, not words with unbounded power parameters.

## 1. Literal model and principal theorem

A complete state is `(B,p,h)`, with finite B in Z^2 and headings N,E,S,W. White
turns right (R), black turns left (L), the read cell is flipped and the ant moves.
Time t is before update t. No finite board, erased archive, finite-memory promise,
or restriction on initial coordinates is imposed.

Let W be the fixed standard P104 word. Let L10 be its cyclic ten-letter factors.
For a finite forward turn word w, d10(w) counts all length-ten factors outside L10
that are wholly contained in w. This is NOT the same finite count as intrinsic
J10 at times 0,...,8; the two counts differ in at most those nine initial tests.
Their finiteness is equivalent by the previously proved ten-factor theorem.

For fixed m>=0 and N>=1, write z=(x1,y1,...,xm,ym) for an ordered list of DISTINCT
initial black coordinates; the head is at the origin facing N. Every other cell
is white. Define

    E[m,N] = {z : the actual forward orbit has at least N contained defects}.

**Theorem 1 (all-coordinate bounded-defect synthesis).** E[m,N] is effectively
Presburger-definable, uniformly in the integers m,N supplied to the construction.
The graph of the exact time and pose just after the Nth contained defect is also
effectively Presburger-definable. The complete black field at that time is an
effective finite-fibre Presburger family over the input coordinates.

Consequently existence of such an input, nonexistence, and intersection with ANY
supplied Presburger coordinate domain are decidable. There is no radius bound in
the input. The construction is not claimed efficient in m,N. In particular this
is NOT one fixed Presburger formula having arbitrary m,N as free variables.

A finite union over 0<=r<=m gives an at-most-m black budget. The theorem applies
to every fixed number of defects, not only paths with a preselected geometry.
Its proof is in Sections 2--6.

## 2. A relation that keeps the entire read chronology

Fix a parameter domain D and a prescribed finite or one-sided infinite kinematic
trace. Suppose the following relations are effectively Presburger:

    V(theta) : update time -> physical position,
    R(theta), L(theta) : the times requesting R and L.

The time domain is a contiguous interval {0,...,T(theta)-1}, or N. V is a
function, and the prescribed headings, turns and positions satisfy the literal
movement rules. These hypotheses are ensured by the schema construction below.

Define the strict same-cell relation

    C={(s,t): s<t and V(s)=V(t)}.

Using relational composition in time order, define

    Next = C \ (C composed with C).                         (1)

**Lemma 2.** Next consists EXACTLY of consecutive reads of the same physical cell.

Proof. A pair in C is nonconsecutive exactly when a time u strictly between its
endpoints reads their common cell. This is exactly membership in C composed
with C. No iteration, transitive-closure oracle, or parity-of-an-unbounded-set
assumption is used. For any finite time, only finitely many preceding times
exist, including in an infinite trace. QED.

Let Times=dom(V), First=Times\range(C), and, for finite traces only,
Last=Times\domain(C). First and Last are the first and last read TIMES of their
respective cells. Let B(theta,x,y) be the complete initial black predicate and
Hits={t:B(theta,V(t))}.

**Theorem 3 (exact parameter domain).** The prescribed trace is physically
realized precisely when

    Next has no pair in (R x R) union (L x L),              (2)
    First intersect L = First intersect Hits.              (3)

All parameter assignments violating either condition are an effectively
Presburger set; their complement in D is the exact realization domain.

Necessity is the flip rule and the initial read colour. For sufficiency, induct
on ordinary time. A first visit reads exactly its specified initial colour by
(3). Any subsequent visit has an immediate preceding read of the same cell, and
(2) requests the opposite letter. The requested turn, flip and next position
therefore coincide with the actual update. This proves EVERY finite time, so
also the infinite assertion. Arbitrary silent writes and old-field reactivation
are included; no cells are deleted. QED.

If no initial B is prescribed, (2) alone describes realization on some colouring.
For a FINITE word it is realized by the unique minimum read-support black set

    Required = image_V(First intersect L).                 (4)

For an infinite word (4) can be infinite. It must never be called a finite seed
without an additional finite-fibre argument or an explicitly supplied finite B.
The implementation contains an infinite-black-ray rejection control.

**Theorem 4 (complete output).** For a finite feasible trace the final field is

    B_out = (B \ image_V(Times))
            union image_V(Last intersect R).              (5)

Unvisited initial cells remain. A last R leaves its cell black; a last L leaves
it white. Equation (5) is evaluated only on the realization domain and is
Presburger. It is finite-fibre whenever B was finite-fibre. This establishes
exact macro endpoints, not equality modulo an unverified archive. QED.

## 3. Unbounded powers still have affine kinematics

A bounded-power schema is a FINITE expression

    v0 u1^k1 v1 ... us^ks vs,        ki>=0,                (6)

where all words are fixed and each ui restores heading. Zero powers are allowed.
The initial position may depend affinely on additional integer parameters.
Every phase i of block j has an occurrence index a with linear bounds
0<=a<kj, and its time and position are

    time = c + sum_h ch*kh + |uj|*a,
    point = b + sum_h dh*kh + drift(uj)*a.                 (7)

All coefficients are fixed integers. There is no product of two free variables.
Fixed vj can rotate heading; their effect is known when constructing later
blocks. Substituting an affine expression for a power count preserves the claim.
An infinite final heading-restoring power has simply a>=0.

Thus V,R,L are finite unions of Presburger relations, and Theorems 3--4 apply.
For a rotating variable power, one can first split its count modulo its rotation
order (2 or 4). The runtime deliberately requires heading-restoring variable
powers instead of silently performing an unrecorded split.

A prescribed initial family may be ANY finite-fibre Presburger set. The runtime
has constructors for finite lists of affine points and finite arithmetic
segments with fixed strides; their lengths can be arbitrary affine parameters.
Unions and XORs preserve finiteness. Raw infinite fields are permitted only as
explicit arbitrary-colouring controls, not as finite-support inputs.

## 4. Defects, first-black cost and piecewise-affine resource spectra

For any finite schema (6), the set of END times of a forbidden ten-factor is
Presburger: intersect the ten translated letter-time sets for each allowed
factor, take their finite union, and subtract from Times restricted to t>=9.
This checks boundary-crossing factors and zero powers exactly.

If F(theta) is any unary time set and b is a FIXED nonnegative integer, then

    |F(theta)|>b iff exists t0<...<tb, all ti in F(theta).  (8)

This provides an elementary exact threshold compiler. There is no sampling of
the count and b is not silently treated as a fixed-dimensional free variable.
The implementation uses (8) for first-black-cost and defect thresholds.

**Theorem 5 (effective piecewise-affine resource spectrum).** On the feasible
parameter domain of any finite bounded-power schema, both

    c(theta)=|First intersect L|,
    d(theta)=number of contained forbidden ten-factors

are effective piecewise rational-affine functions on a finite Presburger
partition. Their joint graph is semilinear. c is the MINIMUM initial black
cardinality, not the number of L letters or final black mass.

Proof of the counting step. Eliminate quantifiers from a unary Presburger set
F(theta,t). Split parameter residues and t modulo a common multiple of all
constant congruence moduli. Write t=r+Qz. In a disjoint Boolean cell each atom
with nonzero coefficient of z becomes an upper/lower floor or ceiling of a
fixed rational-affine expression in theta. Zero coefficients are parameter
conditions. Further partition by the order of this finite collection of bounds
and by residues modulo their constant denominators. Every cell is then an
integer interval in z with rational-affine endpoints. Since the fibre is finite,
nonempty intervals have two finite bounds. Sum their disjoint integer lengths.
This constructs the claimed finite partition and affine formulas. Apply it to
First intersect L and to defect times. Equation (4) gives the interpretation
of c because distinct first times refer to distinct physical cells. QED.

This unary-fibre result does NOT claim that arbitrary finite-fibre planar
Presburger sets have affine cardinality: a variable n by n square has n^2
points. The argument counts first-read TIMES, one variable, rather than arbitrary
planar cells. The implementation extracts exact time sets and fixed thresholds;
a general optimized symbolic counting-partition backend is not claimed built.

For any SUPPLIED finite collection of schemas and fixed mass m, unboundedness
of d under c<=m is consequently decidable. If the count is unbounded, the
semilinear spectrum has a linear component with an increasing d direction and
bounded c, yielding an affine parameter family of finite witnesses. This is
not one fixed infinite orbit and does not refute HC. The statement is a
mathematical consequence of Theorem 5, not a completed universal schema search.

## 5. Audited finite schema coverage at a fixed defect budget

The required ant-specific input is the project's already proved flat J10 lift.
For clarity this dependency is independently regenerated here, not attributed
to Presburger arithmetic:

* all 6605 feasible 150-letter words with legal ten-factors;
* the 6501-vertex graph, with cyclic components of sizes 104,24,366;
* the 366-state component's homomorphism to the two loops A (28) and B (102);
* the all-parameter physical impossibility of B A^n B A^m B;
* the resulting 7595-vertex, 7763-edge bounded-fold lift, whose only cyclic
  components are simple cycles of lengths 24,28,28,28,104;
* DAG bounds: at most five cyclic components, 956 acyclic updates, and sum of
  visited cycle lengths at most 212.

The graph reconstruction in `code/flat_cover.py` derives quotient phases by
reading complete 149-letter contexts in the 102-state two-loop automaton.
Every edge is checked. It does not sample contexts or presume a non-simple
component is periodic. The triple-fold lemma is separately reverified on the
WHOLE parameter quadrant by the supplied-schema kernel; its earlier manual
coordinate proof remains an independently readable inherited argument.

A finite event-free segment has at most 149 initial literal steps before this
coverage applies. Its lifted path visits each SCC once. In each simple cyclic
SCC, write the internal segment as whole powers and a remaining partial turn
word, possibly including its exit. The latter costs at most that cycle length.
Therefore a safe finite schema bound for such a segment is five powers and
149+956+212=1317 literal letters. The bound is on DESCRIPTION, not elapsed time,
and permits unbounded exponents, distant markers and silent foldbacks.

For a finite prefix ending exactly at its Nth contained defect, cut after the
N defect-producing letters. Each preceding block has no internally contained
bad factor; apply the cover above. Thus a finite effectively enumerable
superset of schemas suffices, with

    s<=5N,          total literal length<=9+2000N.         (9)

The slack in (9) covers all boundary letters and short empty intervals. Each
power is a cyclic phase of W, A or T and restores heading. Initial/intrinsic
nine-letter issues do not alter the FORWARD-contained definition used here.

One elementary complete generator enumerates every literal word up to the bound,
every distribution among s+1 gaps, and every selection of power phases. It may
be enormously redundant. Exact physical and exact-defect constraints remove
all extraneous schemas. No word is accepted only because the graph permits it.
`code/budget_schema.py` implements this deliberately conservative lazy generator.
A finite cap on generated schemas returns INCONCLUSIVE, never NO.

## 6. Proof of Theorem 1 and a finite-witness radius

For each schema in (9), let its exponent variables be k. Let the complete initial
black field be exactly the distinct coordinate list z. Conjoin:

1. k>=0 and pairwise distinct initial coordinates;
2. the exact realization predicate (2)--(3);
3. exactly N contained defects, and one at the final letter.

Project the exponents, and take the FINITE union over schemas. Necessity follows
from (9); sufficiency follows from Theorem 3 and determinism. Therefore the union
is exactly E[m,N]. Retaining its affine endpoint time/pose gives the exact Nth
post-event relation. Using (5), and then existentially projecting its schema
parameters, gives the COMPLETE endpoint field. Multiple schemas for one physical
prefix have the same endpoint; no arbitrary choice changes it. QED.

A decision can return a satisfying integer coordinate tuple by standard witness
extraction. It is essential to verify such a concrete witness by independent
literal or complete-field symbolic replay before promoting it as a new ant fact.
The present package has not exhaustively compiled a nontrivial E[m,N].

**Corollary 6 (effective all-coordinate small-witness reduction).** There is a
computable R(m,N) such that E[m,N] is nonempty iff it has a witness with every
initial coordinate in [-R(m,N),R(m,N)].

Decide emptiness first. If empty return R=0. Otherwise enumerate radii and use
the just-proved decision procedure on the intersection until one is nonempty.
This terminates. It produces no attractive complexity or numerical bound and
must not be confused with a fixed box chosen BEFORE the theorem.

## 7. A computable root-cost sequence, and its exact HC quantifiers

Let

    mu(N)=min{c(w): w finite feasible and d10(w)>=N}.

The scanner (LRRL)^q at heading E uses 2q initially black row cells and has
max(0,4q-9) defects. Hence mu(N)<=2 ceil((N+9)/4). Searching this finite mass
range with Theorem 1 computes mu(N). Monotonicity in N is immediate.

The proposed global route is now a precise sufficient theorem:

    mu(N) tends to infinity => HC.                        (10)

Indeed an m-black seed can realize only words of first-black cost at most m.
If (10)'s premise holds, it has finitely many contained defects and is standard
by the ten-factor attraction theorem.

The premise has NOT been proved. Neither does bounded mu refute HC. The exact
HC statement in these coordinates is

    for all m, intersection_N E[m,N] is empty.

The stronger uniform-mass strategy requires

    for all m, some N has E[m,N] empty.

Nested semilinear sets such as {a>=N} show why these cannot be interchanged:
witnesses can escape to larger parameter values. One must lock ONE tuple into
all E[m,N] to produce an infinite counterexample. No such tuple was found.

This theorem therefore removes an all-coordinate FINITE-BUDGET synthesis
obstacle. It does not supply the unbounded-event termination argument. It applies
to both possible HC counterexample branches, without asserting they are empty.

## 8. Exact two-fold classification and minimum black cost

Let B and A be the fixed 102- and 28-letter words in `code/examples.py`, with
A=L B[75:]. The inherited triple-fold obstruction is not new here. The new
kernel additionally computes the full parameter set for a double fold:

**Checked parametric proposition.** The word

    B A^n B A^m

is feasible from some finite support iff n>=1 and 0<=m<n. On that domain its
minimum initial black cardinality is exactly

    5n+5m+47.                                            (11)

This classification is certified by equality of exact Presburger sets, not by
an integer parameter cutoff. A compact certificate for the count is:

* in the first B, first-L indices are
  2,3,4,9,20,21,23,24,26,28,29,37,44,45,46,55,61,72,73,74,83,89,100,101;
* in the second B, the same list without index 9;
* in every A copy of BOTH runs, the only first-L indices are 0,9,15,26,27.

Their complete union of time sets is checked equal to First intersect L over
n>=1, 0<=m<n. The 24+23 fixed times and five distinct times per copy are disjoint
and correspond to distinct first-read cells, proving (11). Necessity and
sufficiency of the parameter region are separately checked by (2). This gives
a fully specified all-parameter certificate backed by exact libisl arithmetic;
it is not a small independently proof-producing kernel.

Other reverified controls are the old three-sweep rail with its complete output
field and a scanner with a freely placed extra black marker. For the latter,
starting E with a lower rail 0<=x<2n at y=-1 and an added point (a,b), the run
(RLLR)^n is valid exactly when

    n>=0 and (b!=0 or a<0 or a>=2n).                       (12)

Both n and the marker coordinates are unbounded integers. In particular (12)
checks unwanted initial black hits at required first-white cells. The complete
endpoint retains every unvisited marker, including coordinates of size 10^61.
These controls do not construct a self-renewing infinite ant.

## 9. Verification and limits of implementation

`reproduce.py` runs the isolated arithmetic controls and reconstructs the flat
cover. The backend is libisl with exact GMP integers; the retained run uses
isl-0.27-GMP. The graph identity and theorem proofs are independent of that
choice of library. Runtime outputs are NOT independently checked elimination
proofs: libisl, GMP, the Python bridge and the compiler are part of their trust
boundary. Composition subtraction and lexicographic next-read minimization are
two formulations using the SAME arithmetic backend, not independent proof
assistants. Independent vector-rotation replay checks finite instances.

No numerical approximation or SAT timeout is used as nonexistence. Explicit
operation limits raise ArithmeticFailure. A preliminary generic W-infinity
experiment exhausted a finite operation budget; it was not classified NO.
The all-parameter finite controls, including the double- and triple-fold queries,
are complete. No performance claim is made for arbitrary large schemas or the
full finite-budget disjunction.

The general symbolic affine-count partition is proved constructively in
Section 4; the current kernel computes exact first-time sets and supplied
integer thresholds, not an optimized arbitrary symbolic counting partition.
These implementation boundaries are part of the result, not hidden TODOs in
an allegedly completed HC decider.

## References and provenance

- H. Ke, project proofs at the pinned research commit: `ten-factor-attraction.md`,
  `ten-event-macros.md`, `semilinear-trace-lifting.md`, and the all-coordinate
  proposal named at the start. The finite-word same-cell criterion is attributed
  there to A. Gajardo (2003); periodic-word realization to A. Jillhewar (2026).
- C. Haase, S. N. Krishna, K. Madnani, O. S. Mishra, G. Zetzsche, *An Efficient
  Quantifier Elimination Procedure for Presburger Arithmetic*, ICALP 2024,
  LIPIcs 297, 142:1--142:17, DOI 10.4230/LIPIcs.ICALP.2024.142.
- N. Decker and A. Pirogov, *Flat Model Checking for Counting LTL Using
  Quantifier-Free Presburger Arithmetic*, arXiv:1901.05692. Flat-schema arithmetic
  is established methodology; here the field-changing ant semantics and the
  complete fixed-defect cover are essential extra premises.
- S. Verdoolaege et al., *Integer Set Library manual*,
  https://libisl.sourceforge.io/user.html. Consulted 15 October 2026.
