# Initial-black supply for bounded-power traces: an effective dichotomy

`f74b09bd3329d7b83fcf323fc580f5a1320fcd48`.

The proof uses attributed Presburger arithmetic, an exact computer-assisted
three-parameter classification and a separate literal checker. The analytic
argument is unformalized; ISL/GMP computes the exact integer relations.

## Dependencies and attribution

At final integration, remote main is `6afea97c2a8a26d03b2bf89de9d23a87d64a31e0`.
Its [resource-spectrum theorem](defect-resource-spectrum.md), Section 2, already
proves the same unary-first-time supply/count semilinearity as Theorem 1 below,
including decidability of a supplied fixed-mass unboundedness query. That general
result is retained as an imported project theorem with an independent derivation
here, NOT registered as a second discovery. The new general addition is the
explicit vertical-ray versus UNIFORM affine-budget corollary over ALL masses of
a fixed finite portfolio. Its proof is a short consequence of the established
semilinear spectrum, not a new arithmetic method or a separate priority claim.

The distinct completed physical result is Section 5: the full three-independent-
parameter fold/consumer classification, exact minimum supply, three-component
resource image, sharp slope/intercept, and exact mass-budget optimum. The new
counter actually executes checked unary interval/residue counting; its limits
are stated below. The two-fold theorem concerns B A^n B A^m, not
our B[9:] A^a B A^b P^r. Neither is silently substituted for the other.

## 1. Question and scope

The preceding bounded-defect reachability theorem fixes an event budget N while
allowing arbitrary input coordinates. Here we instead fix a FINITE collection
of bounded-power word descriptions, and leave the number of defects UNBOUNDED.
The two restrictions are different. Neither covers unlimited HC dynamics by
itself. The new question is whether any amount of repetition in the supplied
collection can create arbitrarily many defects with a fixed initial black mass.

A flat schema is a finite expression

    v0 u1^k1 v1 ... us^ks vs,     ki >= 0,

where all words are supplied finite R/L words. Initially assume every powered
word restores heading. A supplied Presburger condition on the exponents is
allowed. The number of blocks is fixed, not chosen afresh during a run. This
is a description of a finite orbit prefix, not an external control of the ant.
No strip, fixed wake, lifetime threshold, future-invisible deletion, or fixed
period is assumed for an arbitrary HC state.

For a feasible word w, let C(w) be the least number of initially black cells
needed to execute w from its prescribed pose, with every other cell white.
Let D(w) count the forbidden standard ten-factors wholly inside w. D omits at
most nine intrinsic J10 tests crossing time zero. No finite-count identity
between these conventions is used. Arbitrary genuinely unread initial debris
is retained in any larger realizing field.

### Theorem 1 — imported exact supply/count relation

For each supplied schema, the relation

    { (k,c,d) : w(k) is physically feasible,
                C(w(k))=c, D(w(k))=d }

is effectively Presburger, hence effectively semilinear. The same holds for a
finite union of schemas. In particular, MINIMAL initial black cardinality is
counted exactly, without a bounding box and without replacing the field by its
cardinality during execution.

### Theorem 2 — supply dichotomy for a finite schema collection

Exactly one of the following holds, and the alternative is decidable.

(A) Some fixed c0 admits feasible words in the collection with C=c0 and
    arbitrarily large D. One can effectively extract a single schema and an
    affine exponent ray k(n)=k0+n*v, n>=0, with constant C=c0 and
    D=d0+n*delta, delta>0, together with each word's finite minimal seed.

(B) There are effectively computable rational alpha>=0 and beta such that

    D(w) <= alpha*C(w)+beta

    for EVERY feasible instance of EVERY schema in the supplied collection.
    Consequently the same bound with C replaced by m holds whenever a complete
    m-black input actually executes one of these words. An integer affine
    bound follows by rounding upwards.

Case (A) is a family of finite seeds, NOT one fixed seed running forever. It
would refute a cardinality-only event budget for that collection, not HC.
Case (B) is a true whole-collection initial-supply budget, not a stepwise rank
and not a statement about prefixes outside the collection.

The general mathematical decision procedure uses effective unary counting and
semilinear decomposition. The shipped implementation instead uses an explicitly
checked interval/residue counting fast path and checks a supplied complete
semilinear decomposition. Unsupported counting fibres return UNKNOWN by raising
`Unsupported`; no complete general-purpose counting-QE implementation is claimed.
The three-parameter application below is actually completed, with no parameter
cutoff and no unsupported remainder.

## 2. Geometry and feasibility, with attribution

The standard finite-word criterion is inherited from the project's symbolic
feasibility work, attributed there to Gajardo (2003): consecutive reads of any
one physical cell must request alternating letters. Its first requested letter
fixes its initial colour. This criterion is not a new result here.

For a powered phase a and repeat index j, fixed-word geometry gives

    position = p_a + A_a*k + d_a*j,
    time     = t_a + L_a*k + P_a*j,       0<=j<k_i.

All coefficients are constants. Restored heading is why there is no product of
two unbounded variables. Literal pieces are singleton occurrence types. Every
instantiated schema has one read at every time from zero to its finite length
minus one. Same-cell equality and chronological order are Presburger predicates.

Require distinct consecutive same-cell reads to have opposite requested bits.
Necessity is the flip rule. Sufficiency follows by setting exactly the first-L
cells black and inducting through the finite word. No unvisited black cell is
required. Conversely every realizing field must initially contain all these
first-L cells and must omit every first-R cell. Thus C really is their distinct
count, not a count of L turns, births, or current black mass.

This is the same physical lifting interface used in
[presburger-defect-reachability](presburger-defect-reachability.md), but the
supply count and unbounded-defect projection do not use its N-event cover.
The resource-spectrum result independently establishes this same count.

A non-heading-restoring u can be handled by a finite preliminary partition:
let q in {1,2,4} be its heading-return order and write k=q*l+r, 0<=r<q.
Replace u^k by (u^q)^l u^r. Finite products of these residue cases reduce any
flat word expression to the stated class. Zero drift is permitted. The code
requires the normalized form and rejects, rather than misinterprets, an
unnormalized powered word.

## 3. Why initial supply is a UNARY count

Let FirstL(k,t) mean: time t requests L and no earlier time reads its position.
It is Presburger by the preceding occurrence formulas and finite disjunctions
across phase types. There is a bijection

    distinct first-L cells <-> times satisfying FirstL(k,t).

Hence

    C(w(k)) = #{t in N : FirstL(k,t)}.

This is a one-variable fibre, despite the two-dimensional physical field.
Presburger arithmetic is closed under EXACT UNARY counting quantifiers:
for a Presburger phi(t,k) with finite t fibres, the graph of its cardinality is
again effectively Presburger. This is imported from Schweikardt, *Arithmetic,
First-Order Logic, and Counting Quantifiers*, Section 5 (arXiv:cs/0211022;
ACM TOCL 6(3), 2005). It is not a new arithmetic theorem. Chistikov, Haase and
Mansutti, *Quantifier elimination for counting extensions of Presburger
arithmetic*, FoSSaCS 2022, gives later constructive procedures.

The unary qualification matters. Counting arbitrary two-dimensional Presburger
fibres need not give a Presburger function: an n-by-n square has n^2 cells.
The timestamp injection, not an unsupported general counting closure, is the
ant-specific bridge used here.

The defect count is also Presburger. A finite automaton keeps the last nine
letters. For a fixed u, after ceil(9/|u|) copies, that suffix is at a fixed
end-of-u phase; each additional copy adds the same number of bad windows.
Split the finitely many smaller exponents and the remaining unbounded case.
Compose these cases across the fixed number of blocks. Counts are affine on
each branch, including zero powers and junction windows. This construction is
lexical only; it never treats a shortened word as physically executable.

Conjoining feasibility, exact supply and exact defect count proves Theorem 1.
For a minimal seed, terminal black membership is exactly the set of cells
whose last requested letter is R. The general field additionally retains
all unread initial black cells. This explains why no history is being erased.

## 4. Proof and effectivity of the dichotomy

Project away the exponents to obtain S subset N^2 of all (c,d). Effective
semilinearity gives a finite union of linear sets

    b + N*g1 + ... + N*gq,

with bases and generators in N^2. If a generator has first component zero and
second component positive, its component base plus repeated use of this
generator gives constant c and unbounded d: case (A).

Conversely suppose D is unbounded while c is bounded. Some linear component
has this property. Generators with positive first component have bounded
multiplicity under a fixed c bound; zero-first generators with zero second
component do not increase d. Thus a positive vertical generator must exist.
This establishes the exact equivalence, not just a sufficient ray test.

When no such generator exists, choose

    alpha = max({0} union {g_d/g_c : g_c>0}),
    beta  = max_b (b_d-alpha*b_c).

All zero-first generators have zero second component. The proposed inequality
holds at every base and is preserved by every generator. Hence it holds on S,
proving (B). The empty S case uses alpha=beta=0. A negative beta is harmless
on the actual domain; it may be increased to zero for a nonnegative bound.
No well-foundedness of a physical one-step statistic is being claimed.

To extract the exponent ray in (A), fix the c0 found above in the FULL relation
of Theorem 1. Its semilinear decomposition in (k,d)-space has a generator with
positive d component. Its base and that generator give k0+n*v and d0+n*delta.
The same finite schema is selected after passing to one component of the finite
union. Minimal seeds are then computed from first-L occurrences. They need not
be the same seed or the same input coordinates as n changes.

This proof is constructive using the cited standard effective arithmetic.
The ray classification itself uses only rational comparisons and exact set
equality once a complete decomposition is supplied. The new checker verifies
that equality before using any ray or slope; omission of a component is fatal.

### A quantitative corollary

If the collection admits arbitrarily many defects but not case (A), its minimal
initial supply for at least N defects is Theta(N). The lower estimate follows
from (B). For the upper estimate, choose a generator with positive defect
component and use enough repetitions of its ray. If all defect components are
zero, instead D is globally bounded. Thus sublinear-but-unbounded initial supply
cannot occur inside one fixed finite flat collection without fixed-mass
unbounded defects also occurring there.

None of these constants is uniform over enlarging the collection. Substituting
the old N-dependent complete cover makes alpha and beta depend on N and does
not prove HC. This is the exact remaining quantifier, not a complexity issue.

## 5. Completed application: all independently sized fold/consumer words

Use the inherited words, with B9=B[9:] deleting its first nine letters:

    A = LLRRRRLRRLRRRRLLLLRLRRRRLRLL
    B = RRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLRRRRLRLLLLRRRR
        LRRLRRRRLLLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRLL
    P = RLRRRRLRRRRLLLLRLRRL.

Their lengths are 28, 102, 20; A and P restore heading. B9 is a fixed 93-letter
prefix block, not itself a powered block. Start at (-1,0),W and consider

    w(a,b,r) = B9 A^a B A^b P^r,       a,b,r>=0.

No relation between the three parameters is supplied to the checker. The
complete initial colouring is NOT stipulated: it is synthesized minimally
from first reads, or may be any larger finite field actually realizing w.

**Theorem 3.** Exactly the following triples are physically feasible:

    a>=1,    0<=b<a,    0<=r<=b+2.                       (1)

On this full domain the minimum initial supply and contained-window defect
count are

    C = 46+5a+5b,
    D = 0                    if r=0,
        9r-3                 if r>=1.                   (2)

The total word length is 195+28(a+b)+20r. From its minimal seed, the complete
terminal black count is 67+9(a+b)+4r. The latter follows also from (2) and the
literal net black increment 21+4(a+b+r). Mass grows; the supply bound below is
not a net-black-loss assertion.

The original archive prefix is only the subfamily a=n,b=n-1,r=n+1. Equations
(1)--(2) quantify independently over all three parameters and all realizations.
They do not classify arbitrary altered connectors, or the infinite future of
every new asymmetric seed. The older recovery theorem is used only on its
already proved original input family.

### Exact supply/defect image and the sharp budget

The entire image S of (2) is the union of just these THREE linear sets:

    (51,0)  + N*(5,0),
    (51,6)  + N*(5,0),
    (51,15) + N*(10,9) + N*(5,0).                        (3)

For r>=2, write r=q+2. The least possible b is q and the least a is q+1;
this gives the third base and its (10,9) generator. Increasing a, or increasing
both a and b subject to the same r, adds a multiple of (5,0). Conversely every
point of (3) is realized, taking b=q,a=q+1+s in the third component and b=0,
a=1+s in the first two. This proves (3) directly from (1)--(2).

There is no vertical generator. Theorem 2 yields the SHARP inequality

    10 D <= 9 C - 309.                                  (4)

Both slope and intercept are optimal: a=b+1,r=b+2 gives equality for every
b>=0. Reducing the slope fails along this unbounded equality ray; subtracting
310 instead of 309 already fails at (a,b,r)=(1,0,2).

For a complete input mass m>=51, the exact maximum D possible in THIS word
family is

    Dmax(m) = 15+9*floor((m-51)/10).                      (5)

For m<51 the family is not executable at all. To attain (5), choose
b=floor((m-51)/10), a=b+1, r=b+2, and add the remaining zero to nine black
cells outside the finite read footprint. Those cells are genuinely unread
and retained. No arbitrary input of mass m is thereby classified.

The minimal supply for at least N>=0 contained defects in this family is

    51+10*max(0,ceil((N-15)/9)).                          (6)

This is NOT the project's global mu(N); it is a restricted, explicitly named
family's resource function. In particular (4)--(6) cannot be used as a budget
for every finite seed or for the unspecified future after w.

## 6. Why the finite computation covers ALL triples

The code constructs EVERY phase occurrence directly from B9,A,B,A,P. Its
relation maps (x,y) to (t,bit), with exponent bounds left symbolic. Composing
its inverse with itself lists every same-cell pair; restricting to later times
and lexmin takes the actual next same-cell read. Parameter values with equal
bits in a successor pair are excluded. Lexmin per cell determines first reads.
These are exact integer set operations, including congruences and intersections
between nonadjacent blocks. Section 2 proves their physical soundness and
completeness. No coordinates or repeat counts are enumerated in this calculation.

The compiler's complete feasible relation is compared for EQUALITY with (1).
First-L timestamps are partitioned into disjoint integer sets. For each piece,
a candidate arithmetic-progression interval is built from its exact minimum,
maximum and stride and accepted only after proving it EQUAL to the piece.
Residue splitting is used where the one-progression test fails. Counting each
accepted interval and adding across the disjoint cover gives C exactly.
The archive has 40 such counted pieces. Empty parameter fibres count zero.
The full computed C and D graphs are compared for equality with (2).

The independently supplied three-component decomposition (3) is compared for
exact equality with the projected image. Then the ray budget (4), its equality
ray, the failure of the stronger constant 310, and the exact maximization (5)
are all checked in integer arithmetic. These are universal parameter checks,
not regression against a fitted affine function.

This is computer-assisted evidence whose native trusted base includes ISL/GMP
and the new compiler. The finite Python/C++ trajectories below check coding,
conventions and complete fields; they do not independently prove every symbolic
projection or replace the written coverage argument.

## 7. Checks, limits and files

Run `python experiments/hc_global/schema_supply/reproduce.py`. It copies only
this isolated module into a disposable directory and compares a freshly rebuilt
report with the frozen one. Python 3.10+, system libisl and a C++17 compiler
are required. The exact frozen textual report uses isl-0.27-GMP; another ISL
version may format equivalent sets differently and is not a byte-identical replay.

The completed checks include rail, pulse, standard word, the entire two-variable
three-fold exclusion, and the three-variable archive. There are 1323 literal
parameter controls, including 380 feasible complete inputs; each independent
implementation executes 439516 updates on those feasible inputs. Complete native
and Python initial/final fields agree. Thirty-two initial/terminal field pairs
are also compared to the symbolic sets. A 10^60 parameter is checked symbolically.
The standard control has C=17 for every positive number of complete W periods
and zero contained defects; no new minimum highway-seed theorem is claimed.

Omitted semilinear components, wrong supply, wrong event slope, a false sharper
budget, unnormalized powers and unsupported residue holes are rejected or remain
UNKNOWN as appropriate. A vertical-ray branch control uses a clearly marked
SYNTHETIC ARITHMETIC relation, not an ant orbit or negative seed.

A first native parser check found a token-count bug. A later oversized symbolic
full-field control timed out and is NOT recorded as passed. The final checker
uses smaller complete symbolic field controls alongside all the literal controls;
its successful full replay is the retained evidence. Report hashes identify only
the corrected final sources. Shared simulators and prior theorem files are not
modified or broadly rechecked.

## 8. What remains for HC

The new result supplies an actual scalar resource budget for an entire supplied
finite template collection whenever its fixed-mass-unbounded alternative is
absent. It also gives a principled test for finding such an alternative. That is
more general than a single one-parameter recovery script.

It still does not prove that ALL arbitrary finite-input prefixes lie in one
such collection, or that the resulting constants stay bounded as the number of
blocks and kinds of connectors increases. The full old N-event cover grows with
N. No fixed-mass-unbounded ant family was found in this work. An infinite
self-renewing finite seed, a global event budget, and HC remain unproved.

## References and imported boundaries

* N. Schweikardt, *Arithmetic, First-Order Logic, and Counting Quantifiers*,
  arXiv:cs/0211022; ACM TOCL 6(3), 634--671 (2005), Section 5.
  https://arxiv.org/abs/cs/0211022
* D. Chistikov, C. Haase, A. Mansutti, *Quantifier elimination for counting
  extensions of Presburger arithmetic*, FoSSaCS 2022, 225--243.
  https://doi.org/10.1007/978-3-030-99253-8_12
* ISL manual, exact integer sets, lexicographic extrema and disjoint partitions.
  https://libisl.sourceforge.io/user.html
* Repository `proof/results/defect-resource-spectrum.md`: unary supply/count
  theorem, retained as an imported result rather than a second novelty claim.
* Repository `proof/results/presburger-defect-reachability.md`: earlier physical
  schema lifting, original feasibility attribution, and the separate fixed-N
  complete-cover theorem. It is preserved unchanged.

The arithmetic closure and semilinear-ray method are established mathematics;
no priority claim is attached to them. The initial-black timestamp application is shared with the concurrent
resource-spectrum theorem and is NOT counted again. This package adds its checked
counting backend, the explicit affine-budget corollary, and the exact independent-
length fold/consumer classification and sharp budget.
