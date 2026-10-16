# Effective semilinear reachability with a bounded standard-defect budget

**Research date: 15 October 2026. Mathematical base: `2f6010a6bbccf5d342648f1c730a8bd2ea628961`.**

Evidence: complete analytic composition of the retained finite-path coverage theorem,
a new exact supplied-schema arithmetic implementation, and scoped independent literal
controls. Unformalized and not externally reviewed. Native ISL/GMP is in the trusted
computing base of the computed examples, not a Lean proof checker. Neither HC, a
finite HC counterexample, a practical unrestricted synthesis solver, nor publication
priority is claimed. This replaces the *proposal status* of the bounded-budget
corollary in [the earlier research note](../research-global-all-coordinate-budget-2026-10-15.md)
with the explicit theorem and proof below. The old note itself remains unchanged.

## 1. Complete inputs, events and the main theorem

A state is X=(B,p,h), B a COMPLETE finite subset of Z^2, heading N,E,S,W=0,1,2,3.
White turns right R and becomes black; black turns left L and becomes white; then
move one unit. State t precedes update t. Let W be the retained standard 104-word,
and L10 its cyclic ten-factors, exactly as in [ten-factor attraction](ten-factor-attraction.md).
For a finite word w, let d10(w) count forbidden ten-factors wholly inside w. Thus
on a forward trajectory it counts ending indices j>=9, not the possible first nine
intrinsic inverse-history J10 events. Their finite counts differ by at most nine;
finiteness is equivalent, hence H(X) iff the forward count is finite.

Let lambda range over an effectively supplied Presburger domain D subset Z^r.
The input family is given by a Presburger formula I(lambda,x,y) with FINITE fibres,
an affine initial pose p(lambda), and a fixed heading. Finite piecewise-affine pose
and heading partitions may be handled by a finite union. All other initial cells
are white. Finite-fibre support is a premise of the family, not a radius restriction.
Arbitrarily large, disconnected, dense or sparse finite fibres are allowed.

**Theorem 1 (bounded-defect reachability).** For every supplied N>=0, the following
relations have effectively constructible Presburger definitions:

1. A finite actual prefix has exactly d defects, 0<=d<=N, duration t, and endpoint
   pose (p,h). The relation may be restricted by any supplied Presburger condition
   on these variables.
2. Membership of (x,y) in the COMPLETE black field at such an endpoint.
3. Equality of that complete field with any supplied Presburger target family,
   as well as finite local colour predicates at the endpoint.

The theorem concerns prefixes with at most N defects, not a promise that every
future prefix has that property. It decides existential and universal arithmetic
questions about these bounded-budget relations. There is no uniform bound on N.

For N>=1 let theta_N(lambda) be the time JUST AFTER the Nth forward-contained
defect, when that event exists. Its event index is theta_N-1.

**Corollary 2 (all coordinates and exact event outputs).** The event-existence
set E_N, the graph of theta_N and its post-pose, and the complete post-event black
membership relation are effectively Presburger. In particular, for fixed m,N,
the set E_(m,N) of ordered distinct m-tuples of initial black coordinates is
semilinear and computable, without bounding any coordinate. Existence or exclusion
of such a seed over the WHOLE plane is decidable.

**Corollary 3 (piecewise-affine event times).** On a finite effective semilinear
partition of E_N, theta_N and each post-position coordinate are rational-affine
functions of lambda, with integer values on their domains. The heading is constant
after a finite further partition. For an affine one-parameter input family, there
is an effective modulus q such that, on each residue class n=qk+a, eventually
either the Nth event never exists or its time and post-position are affine in k.
This is about a FIXED event number, not the unbounded renewal sequence.

All three statements are proved below. The numerical examples check the compiler,
not an exhaustive traversal of the enormous complete N-event cover.

## 2. What is inherited and what must be added

The retained [bounded-fold lift](ten-event-macros.md), Sections 3--5, covers EVERY
physical finite ten-legal path after a 149-letter warm-up. Its graph has 7595
vertices and 7763 edges; each recurrent component is a simple cycle. Along a path
there are at most five cyclic stages, at most 956 noncyclic-vertex steps, and sum
of cycle lengths at most 212. The words are phases of W (104), T (24), or A (28),
all heading-restoring, with nonzero drift. The non-simple original component was
handled by the physical impossibility of B A^n B A^m B for all n,m>=0.

We import that FINITE-path theorem, not just an eventual-periodicity statement.
An infinite-tail classification alone would not cover long dead-end prefixes.
No earlier shared code or graph certificate is changed or presented as rerun.

The old [semilinear trace lifting](../semilinear-trace-lifting.md) treats a fixed
literal word. It does NOT already supply unbounded powers or global event-prefix
coverage. We add both: affine occurrence geometry for bounded power schemas, and
an exact chronological colour test retaining all cross-block dependencies.

Presburger closure, quantifier elimination and effective semilinearity are standard
imported arithmetic. Flat-path-schema reachability is also established verification
methodology; the new application cannot simply declare the ant a finite counter
system, because its current colour field is unbounded. The explicit same-cell
read relation in Sections 4--6 is the missing physical argument.

## 3. A finite, complete cover for every fixed defect budget

Consider a ten-legal physical finite word v. If its length is below 149, keep it
as a fixed word. Otherwise keep its first 149 letters and apply the retained lift
to the remaining path. A cyclic visit, starting at its actual entry phase, is a
whole number of copies of that cycle followed by a proper prefix. A departing
edge costs at most one additional fixed letter. A condensation component cannot
be revisited.

Thus v is a concatenation of at most five powers of fixed heading-restoring words
and fixed pieces of total length at most

    149 + 956 + 212 + 5 = 1322 < 2048.                       (1)

The same argument covers a path that stops inside a cycle, including a finite
prefix of a forever-standard tail. It needs no hypothesis that a later event
exists. A cyclic phase may change the fixed drift orientation; that orientation
is determined by preceding fixed pieces, not by the repetition count.

Given an actual word w with d=d10(w)<=N, cut out the d letters ending forbidden
windows. The remaining at most d+1 CONTIGUOUS pieces are ten-legal: a forbidden
window wholly in such a piece would have had its ending letter removed. Their
physical feasibility follows because they are actual subwords. Keep the removed
letters as fixed one-letter pieces. Combining (1) gives a schema

    v0 u1^k1 v1 ... us^ks vs,      ki>=0,
    s <= 5(N+1),
    sum |vi| <= 2048(N+1)+N.                                 (2)

There are exactly 156 cyclic phase words in the library W,T,A. Therefore all
schemas in (2) form a FINITE EFFECTIVELY ENUMERABLE collection. Enumerating all
R/L fixed pieces and all library choices overapproximates the inherited graph;
that is safe only because the physical and defect tests below are exact.

The implementation `cover.py` includes this full finite generator and a guarded
existence driver. The complete N>=1 collection was NOT traversed in this work.
A supplied-schema exclusion must not be labelled an all-schema exclusion. The
size in (2), rather than any bound on ki or initial coordinates, gives termination
of the mathematical exhaustive construction. No practical complexity is claimed.

## 4. Affine geometry of unbounded-power occurrences

Fix one schema. Index each phase of each powered word, and each fixed letter,
by a type a. Its occurrence index j has a finite linear domain, usually 0<=j<ki;
a fixed letter uses j=0. Geometry gives

    P_a(lambda,k,j)=p(lambda)+c_a+A_a k+d_a j,
    T_a(k,j)=b_a+l_a k+L_a j.                                (3)

All coefficients are FIXED integers. Each powered word restores heading, so the
anchor of every later block is affine in earlier exponents. There is no product
of two variables, including no ki*j. The input pose may be affine in lambda.
Requested read bits b_a are fixed: L=1, R=0. Final duration, position and heading
are also explicit affine expressions and a fixed finite heading.

Define the read relation R_(lambda,k): (x,y) -> (t,b) by the finite union of (3)
with its occurrence-domain constraints. It is Presburger. For each parameter tuple
it has finitely many reads, one at every time from zero to the word length minus
one. Thus chronological minima, maxima and successors exist whenever appropriate.

The code accepts affine exponents and shared parameters as a convenience; the
complete cover only needs independent nonnegative ki. Powers of a non-heading-
restoring word are rejected rather than silently assigned a constant drift.

## 5. Exact physical feasibility without a parity-counting assumption

For an occurrence e define First(e) by absence of an earlier occurrence at its
position. For two same-cell occurrences e<f define Consecutive(e,f) by absence of
an intermediate occurrence at that cell. These are Presburger formulas: equality
of positions and temporal order are linear, phase types form a finite disjunction,
and occurrence indices are ordinary quantified integers with linear bounds.

Impose precisely:

    First(e) => I(lambda,P(e)) = b(e),
    Consecutive(e,f) => b(e) != b(f).                         (4)

Necessity is the literal read/flip rule. For sufficiency, induct through the finite
instantiated word. The first read of a cell sees its actual complete input bit.
At any later read, its immediate preceding same-cell occurrence exists and has
flipped the opposite requested bit to the current one. The actual turn, heading
and next position are therefore exactly those of the plan. This proves physical
execution at EVERY update, not just equality of an endpoint or a count.

In particular (4) retains silent writes, later reactivations, original black
cells, and first-white constraints. A J10 can be R or L. No newborn cell is charged
to an original black cell unless its first read really requires that colour.
No inference of future invisibility or deletion of historical cells is used.

An executable equivalent uses integer relations. Compose R inverse with R,
restrict to increasing times, and take the lexicographically least later (time,bit)
for each earlier (time,bit). This is exactly the same-cell successor, since time
is the first component and each actual time has one bit. Reject parameter values
where a successor pair has equal bits. From lexmin(R), extract first-black and
first-white positions; reject a first-black position absent from I or a first-white
position present in I. Complements/projections perform the universal checks.

ISL uses exact integer sets, including congruence classes arising from strides two
and four. The implementation never replaces an integer progression by its rational
convex hull. All arithmetic failures raise an error or return UNKNOWN, not UNSAT.

## 6. Complete endpoints and regular defect conditions

Let V be the set of positions read in the finite plan. Let LastR be the positions
whose LAST requested read is R, obtained from lexmax(R). On the feasible domain,

    B_end = (B_initial minus V) union LastR.                 (5)

A last R leaves black and a last L leaves white. The first term explicitly retains
EVERY unread original black cell, regardless of distance. Formula (5), not a
count of all toggles with an unproved parametric parity operator, supplies the
complete Presburger output predicate. All the operations are effective.

For a target predicate Q, complete equality is the Presburger condition

    forall x,y: B_end(lambda,k,x,y) iff Q(lambda,t,p,h,x,y).   (6)

A finite local observation is only finitely many substitutions in (5). Theorem 1
does not claim the same for an arbitrary unbounded-state observer history.

The finite-word condition d10(w)=d, or <=N, is regular with a count capped at N+1.
It can be compiled to Presburger conditions on powers using finite automaton
powers. The implementation uses a more direct exact calculation. After
ceil(9/|u|) copies of a fixed u, the last-nine-letter register is at a fixed phase;
each subsequent copy adds a fixed number of forbidden windows. Branch on the
finitely many shorter exponents and the remaining unbounded case. Counts are
affine in the exponent on every branch. Keep the last-letter defect flag too.

This handles zero powers, empty fixed pieces, short words and junction windows.
It never asserts that shortening a lexical word preserves physical feasibility.
For the specific ten-legal mode library, positive full powers add no internal
defects; only zero/positive choices and the boundary contexts matter.

Conjoin the exact physical condition, defect condition, duration and endpoint
conditions for every schema in (2), existentially project k, and take the finite
union. Completeness follows from Section 3. Soundness follows from (4). Equation
(5) and condition (6) give the complete-field and target variants. This proves
Theorem 1, including uniform effective construction for a supplied N and family.

For Corollary 2 require d10(w)=N and a defect on the LAST letter. A word satisfying
these conditions ends precisely just after the Nth counted defect. The complete
m-coordinate input is I(z,x,y)=OR_i[(x,y)=zi] with pairwise-distinct zi; hence it is
one instance of Theorem 1. Arbitrarily distant coordinates remain quantified.

## 7. Why exact times are piecewise affine

Here is the arithmetic argument, rather than an appeal to a suggestive picture.
By Corollary 2 the graph of theta_N is an effective finite union of linear sets

    a + sum_i n_i v_i,      n_i in N,                       (7)

in (lambda,time)-space. It is the graph of a PARTIAL FUNCTION: physical determinism
makes the Nth event time unique. For each linear set, any integer relation among
the lambda projections of its generators must also be a relation among their
time components. Otherwise split its positive and negative coefficients; the two
resulting nonnegative combinations in (7) give the same lambda and different times.

Thus the map from projected generators to time components is rational linear on
their span. Solving a finite rational linear system and fixing the offset a gives
an affine formula for time on that linear set's domain. The same argument applies
to both position coordinates. Partition overlapping domains by set difference;
affine formulae agree wherever both are defined because the function is unique.
Headings take four values and give another finite Presburger partition.

This construction is effective using standard effective semilinearity and rational
linear algebra. In one parameter every semilinear domain is eventually a union
of arithmetic progressions. A common modulus and threshold give the final statement
of Corollary 3. No fixed domain partition or formula size works uniformly as N
grows without a new argument. This proves the corollary.

The full black MEMBERSHIP relation is Presburger, but the complete colouring is
not being encoded by a fixed finite vector. Its size can keep growing. There is
no new finite-dimensional quotient of unlimited physical evolution here.

## 8. Global consequences and the exact unsolved quantifiers

The total-at-most-N event basin in any supplied family is D minus E_(N+1), hence
also effectively semilinear. Therefore the question 'does every member of this
arithmetic family have at most N defects?' is decidable for a SUPPLIED N. If true,
the retained ten-factor attraction theorem proves H for that family.

For fixed m,N an effective witness-radius bound exists: decide whether E_(m,N)
is empty; if nonempty, extract an integer witness from its formula. Its coordinate
radius is one possible bound. This is an effective all-coordinate witness theorem,
not a convenient numerical search cutoff or a complexity claim.

For a physically feasible word let c(w) count DISTINCT first-L cells. It is the
minimum initial black cardinality realizing that word. Define

    mu(N)=min{c(w): w feasible, d10(w)>=N}.

Every test mu(N)<=m is decidable by the finite union of E_(j,N), 0<=j<=m. The
minimum exists: (LRRL)^L has 4L updates, max(0,4L-9) forbidden contained windows,
and a minimal seed of 2L black cells. For L=ceil((N+9)/4),

    0 <= mu(N) <= 2*ceil((N+9)/4).                          (8)

Finite search in this m range computes mu(N); it is nondecreasing. No new numerical
mu table was computed here. Subword-first-L costs are not automatically costs of
the ORIGINAL input, which is why the definition uses complete prefixes.

The unproved strengthening mu(N)->infinity would imply HC and, using the new
emptiness procedure, yield a computable coordinate-independent total event budget
for each initial cardinality. The converse from HC is NOT established.

Precisely, HC requires every fixed coordinate tuple to leave the nested E_(m,N)
eventually. A cardinality-uniform budget requires one E_(m,N) to be empty for each
m. Nonempty semilinear sets may shrink with empty infinite intersection, e.g.
{a>=N}. Equality of two consecutive levels also need not imply later stability.
Neither semilinearity, a finite native run, nor computability of mu resolves those
unbounded quantifiers. No HC conclusion is promoted.

## 9. Implementation results and a reproducible trust boundary

`compiler.py` compiles a supplied bounded-power word to exact same-cell chronology,
first-read requirements, feasible parameter domain and COMPLETE output field.
`isl_exact.py` is a small ownership-safe ctypes adapter to the system libisl; no
binary is vendored. `cover.py` implements the complete finite supercover and an
existence driver with explicit incomplete/resource outcomes. It is not advertised
as a practical full all-coordinate solver for a nonzero global event budget.

The retained check calculates, without exponent or coordinate cutoffs:

- feasibility of B A^n B A^m B is empty for all n,m>=0 (an inherited conflict);
- feasibility of the supplied two-depth silent-fold schema is exactly 0<=m<=n;
- a complete finite 24-mode rail executes k full copies exactly for 0<=k<=n, and
  its output equals the shorter rail PLUS every one of its generated residues;
- all positions for an extra marker preserving the entire W future, by universally
  quantifying the repetition count; this equals an independently derived 104-ray
  exclusion, with marker coordinates unrestricted;
- the complete first-defect relation for W^k L on that 17-cell standard source plus
  one marker is px=py=-2k, k>=1, post-time 104k+1 and post-pose (-2k-1,-2k),W;
- all-coordinate projections of the supplied LRRL-rail schema at initial masses
  0,1,2 yield respectively k=0, k=0, and 0<=k<=1.

The last item is an exclusion for a SUPPLIED TRACE SCHEMA, not an exclusion of
all other words from these masses. The marker and rail examples are regression
controls of known mechanisms, not separately counted HC breakthroughs.

Independent vector-based finite execution checks 273 parameter instances and
37897 proposed updates, including 94 valid COMPLETE endpoints. Invalid geometric
words are not executed and are explicitly checked as infeasible. The test exhausts
557 small toy descriptors only, checks zero powers, rotations, strides 2/4, empty
words, initial-white conflicts, huge coordinates and native failure handling.
The 10^60 marker epoch is an exact symbolic check, not a huge literal replay.

The first development run exposed an ISL parser-format error for parenthesized
integer multipliers; it was corrected before any retained report. One exploratory
native operation cap was reached on an unnecessarily expanded guard; no empty-set
conclusion was drawn. The final checks use exact relations and explicitly test
that incomplete cover/native errors never produce UNSAT.

Run `python scripts/check_presburger_defects.py`. The disposable replay compares
all non-format report data and semantically compares saved relations, allowing ISL
versions to print different normal forms. The actual version was isl-0.27-GMP.
This tests the supplied-schema arithmetic and examples. Universal Theorem 1 still
rests on its written proof and the inherited finite-path coverage, not execution
of the full astronomical cover. No old broad suite, Lean build, earlier large
wake search, published-paper update, or third-party mathematical review is claimed.

## 10. Attribution and publication assessment

Presburger arithmetic, effective semilinearity and flat path schemas are imported
methods. The exact first-read/alternation characterization is the standard Langton
symbolic method used by Gajardo (2003). The ant-specific new composition is an
all-coordinate, arbitrary-Presburger-family bounded-defect reachability theorem
with complete fields and exact piecewise-affine event outputs. It strengthens the
previous point-input macro algorithm and the earlier fixed-literal-word lifting;
it does not claim a new general Presburger decision procedure.

Primary references consulted in this session:

- A. Gajardo, *A symbolic projection of Langton's ant* (2003), HAL-01183320.
- S. Demri, A. Dhar and A. Sangnier, *Taming Past LTL and Flat Counter Systems*,
  Information and Computation (2015), DOI 10.1016/j.ic.2015.03.007.
- N. Decker and A. Pirogov, *Flat Model Checking for
  Counting LTL Using Quantifier-Free Presburger Arithmetic*, arXiv:1901.05692.
- C. Haase, S. N. Krishna, K. Madnani, O. S. Mishra and G. Zetzsche, *An Efficient
  Quantifier Elimination Procedure for Presburger Arithmetic*, ICALP 2024,
  DOI 10.4230/LIPIcs.ICALP.2024.142, arXiv:2405.01183.
- ISL official manual, 'Sets and Relations', 'Lexicographic Optimization', and
  'Error Handling', https://libisl.sourceforge.io/user.html (read this session).

Theorem 1 together with Corollaries 2--3 is a plausible standalone theoretical
paper core, tentatively *Semilinear Reachability of Langton's Ant with Bounded
Highway Defects*. That is an editorial assessment, not publication acceptance or
an exhaustive priority determination. A manuscript must include or properly import
the full finite-path coverage argument; a supplied-schema implementation alone
is not a substitute. The current deliverable is a research proof and reproducible
compiler, not a new public paper version or submission.
