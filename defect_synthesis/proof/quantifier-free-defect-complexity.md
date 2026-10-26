# Quantifier-free defect synthesis and a polynomial witness bound

`f74b09bd3329d7b83fcf323fc580f5a1320fcd48`.

**Evidence:** complete written analytic reduction, a new exact arithmetic encoder,
solver-checked identities over unbounded integers, and independent compressed and
literal controls. Unformalized; no external mathematical review or priority claim.
Z3 and ISL/GMP are trusted for the reported native checks, not treated as Lean
kernels or accompanied here by independently checked UNSAT proof objects.

This is an upper-complexity theorem and an opt-in decision backend. It is NOT HC,
a total bound on future defects, a deterministic polynomial-time global solver,
or a polynomial-size explicit semilinear decomposition theorem.

## 1. Scope and the new statements

Keep the complete finite black field and the classical white/right, black/left,
flip-then-move rule. Time precedes its numbered update. Let W be the unchanged
standard word and d10(w) the number of wholly contained forbidden ten-factors.
This differs from the intrinsic J10 count only at the first nine indices.

Let D be the fixed stride set

    {(±2,±2), (±2,0), (0,±2), (±4,0), (0,±4)}.

A supplied schema consists of explicitly spelled fixed words and powers u^k.
Every powered u restores heading and has nonzero displacement in D in its
actual orientation. Exponents and anchors may be affine expressions in shared
integer parameters. Every exponent is constrained nonnegative.

The complete source is the XOR of M finite segments a+jv, 0<=j<L, with v in D,
plus singletons. Lengths and anchors are affine parameters; L>=0. A zero-stride
term means exactly one cell. XOR duplicates cancel, they do not denote union.
A sparse initial list of m sites is represented by m singletons PLUS explicit
pairwise distinctness. There are no unlisted initially black cells.

**Theorem A (polynomial-size existential encoding).** For this supplied-schema
and source syntax there is a polynomial-time construction of a quantifier-free
linear-integer/Boolean circuit F(parameters,aux) such that

    the complete source executes the entire schema
    iff there are auxiliary values satisfying F.

For each fixed parameter valuation the auxiliary arithmetic/Boolean values are
uniquely determined before the final feasibility assertion. No coordinate,
length, waiting-time or loop-exponent cutoff is imposed. Exact defect counts,
the last-letter defect flag, affine endpoint poses/times, and any polynomial
number of complete endpoint colour queries have polynomial-size circuits too.

The exported SMT-LIB contains only linear integer constraints, Boolean
operations and if-then-else, with named sharing. Division is eliminated by
linear defining inequalities. It contains no quantified first/next-read test,
variable multiplication or variable-modulus operation.

**Theorem B (all-coordinate upper bound).** Supply m in unary (equivalently,
m explicitly named coordinate pairs), N>=1 in unary, and an optional
quantifier-free linear-integer condition Q of binary input length b on those
coordinates, the Nth event's time/post-position, and additional existential
integer parameters. The question whether some complete m-black initial state
has an Nth forward-contained defect satisfying Q belongs to NP.

This includes every placement in Z^2, not a selected coordinate box. NP is an
upper bound; no NP-hardness or NP-completeness claim is made. It does not say
that an algorithm enumerates all witnesses or computes their full semilinear
partition in polynomial time. When N is binary, this is only a bound polynomial
in the NUMERICAL N for the witness description, not an NP claim in log N.

**Corollary (small witness and root-cost oracle bound).** There is a fixed
polynomial p such that every positive query in Theorem B has a witness with
coordinates and repetition counts of at most p(m+N+b) binary bits. In particular
a witness may be chosen within an exponential numerical radius, but this is
not a bound on every possible witness, on an original input's total defects,
or on an unbounded future. For unary N, the project's minimum initial-black
cost mu(N) can be computed in FP^NP (polynomial time with an NP decision oracle).
No new numerical value of mu(N) is claimed computed here.

The prior general [Presburger reachability theorem](presburger-defect-reachability.md)
remains more expressive: arbitrary quantified finite-fibre source predicates
and arbitrary complete target equality are NOT given this new polynomial/NP
bound. The new backend rejects those unsupported inputs instead of silently
approximating them. In particular zero-displacement powered loops are outside
Theorem A's syntax, though available in the older general compiler.

## 2. Exact read streams, including intra-loop order

For each phase i of a powered block, write its read occurrences as

    a_i(lambda) + j*d,  0<=j<k(lambda),
    time tau_i(lambda)+j*P, required bit b_i in {0,1}.

Every such stream is injective because d!=0. A fixed update is a singleton.
Their anchors and times are affine: powered words restore heading, so the
orientation of every later block is fixed by the spelled fixed words, not by
an unbounded repetition count. Each parameter valuation with nonnegative
lengths spells one finite word and exactly one read at every update time.

At a planned read, the actual colour, provided earlier updates followed the
plan, is the source bit XOR the parity of all earlier planned writes there.
Therefore matching this value to b_i at EVERY read is necessary and sufficient.
Sufficiency is induction through the entire finite plan. This is the same
literal flip rule underlying the old consecutive-read criterion; it includes
silent manufacture, later reactivation, both R and L defects, and all history.

For two streams in different blocks, either all occurrences of the first block
precede all those of the second, or none do. For two phases r,i of the SAME
powered block, an equality of positions implies l=j+s where s is a fixed
integer, if the phase-offset difference is a multiple of d. The time comparison
reduces exactly to

    P*s + r < i.

If this fails, that phase contributes no prior writes. If it holds, the
eligible current indices are -s<=j<k-s. There is no order quantifier and no
product of two variable indices. The implementation keeps this same-block
case separate; it does not wrongly place all phases in block order.

## 3. A bounded-modulus intersection lemma

For a target stream a+jd and a source/prior stream b+lv, put delta=b-a.
All anchors are affine; d and v are fixed. If det(d,v)!=0, equality implies

    j=det(delta,v)/det(d,v),
    l=det(delta,d)/det(d,v).

Divisibility and 0<=l<L determine whether this is one possible target index.
For a singleton source the same conclusion follows by one coordinate division
and the other-coordinate equality.

In the parallel case, first require collinearity. Choose an axis with d_axis
nonzero and write alpha=d_axis, beta=v_axis, c=delta_axis. Solve

    alpha*j-beta*l=c,  0<=l<L.

Divisibility by gcd(|alpha|,|beta|), one fixed residue for j, and the minimum/
maximum of c and c+beta*(L-1) give a finite arithmetic interval in j. Its modulus
is |beta|/gcd(|alpha|,|beta|). In D it is ALWAYS 1 or 2. Signs are handled by
reversing the fixed inequalities, not by relaxing integer membership.

Split j=2z+e, e=0,1. In each part, every contribution is either empty or a
single GUARDED integer interval [lo(lambda),hi(lambda)] in z. Its guard and
endpoints use affine expressions, fixed divisibility, floors and ceilings.
The same-block contribution in Section 2 has this form as well. A nonpositive
source length contributes no interval. A target residue exists only when

    0<=z<=floor((k-1-e)/2).

All fixed divisions have positive constant denominator after a sign change.
A quotient q=floor(a/c), c>0, is defined uniquely by

    c*q<=a<c*(q+1).

Thus every guard, endpoint and exact divisibility test has a constant-size
linear circuit once its affine anchor expressions are shared. These formulas
cover all integer parameters; no assumption on their numerical magnitudes is
made. The 312 native all-integer controls compare this interval construction
with direct point-on-segment membership for every stride pair and both residues.
They supplement, rather than replace, the preceding general argument.

## 4. Eliminating the universal read test by parity jumps

Fix one target residue with maximum index K. Suppose its colour contributions
are guarded intervals [l_a,h_a]. On the integer line their XOR is a step
function. It changes only at an ACTIVE interval's l_a and h_a+1, where active
includes its guard and l_a<=h_a. It follows that the desired bit is seen at
all z in [0,K] if and only if:

1. if K>=0, the value at zero is the desired bit;
2. at every active boundary p with 0<p<=K, the XOR of ALL active boundary
   contributions whose position equals p is zero.

For necessity, any nonzero jump changes the bit at an interior integer index.
For sufficiency, order the actual numerical boundary positions for one fixed
parameter valuation. Starting with the correct zero value, every subsequent
jump vanishes, so the bit is constant on the whole finite target interval.
The encoder need not sort SYMBOLIC endpoints or enumerate their possible
orders. It simply instantiates the equality/XOR check at each candidate boundary.
Coincident beginnings and endings cancel with their full parity. Boundaries
outside the target interval, and empty/inactive source intervals, are ignored
only under their exact guards.

An alternative checked encoding tests the value at zero and at every boundary
inside [0,K]. Both are equivalent by the same step-function argument. The
implementation supplies both; the jump form cancels identical syntactic
boundaries before constructing the pair comparisons.

If there are q contributions, this needs O(q^2) Boolean/linear wire operations.
With R read streams and M source streams, q<=R+M, so the parity stage is bounded
by O(R(R+M)^2), apart from the polynomial cost of shared affine expressions.
Point reads are even simpler. This is polynomial in the explicit schema/source
bit size. It does NOT say the satisfiability solver has polynomial running time.

Before this calculation, literally identical segment terms in completed blocks
may cancel by XOR. This is exact algebra of complete past writes, NOT a claim
that some unknown future will avoid those cells. Every new block is added to
that algebra, and all original terms remain available for complete output
queries and independent replay.

The endpoint at a queried cell is its initial bit XOR membership in EVERY
planned read stream. Stream injectivity makes each such contribution a Boolean
membership test, even for enormous repetitions. This retains untouched remote
black cells and supplies polynomial-size endpoint colour queries. Only feasible
parameter values identify this planned endpoint with the actual endpoint.

## 5. Exact factor counting without an exponential case list

Store the preceding at most nine turns as nine Boolean registers and a length
register in {0,...,9}. A fixed new letter determines whether the ten-window is
forbidden, shifts the registers and increments the count. The standard whitelist
is fixed, so this transition has constant circuit size.

For a power u^k, after q=ceil(9/|u|) copies the suffix is fixed independently of
the incoming suffix. The subsequent copies add a fixed cyclic defect count.
Compute the at most q short transfers and one stabilized transfer, and select
between them by nested if-then-else expressions on k. At k=0 the entire incoming
suffix, count and last-event flag are preserved. A length-nine boundary is
handled separately if its final ten-window did not yet exist. Shared registers
flow to the next part instead of multiplying cases across parts.

Consequently the DAG construction is linear in total spelled length and block
count (including input affine-expression encoding), with the fixed ten-factor
language absorbed in the constant. The older factor_cases explicitly has 2^s
branches on the benchmark's s independent modal powers. No claim is made that
shortening a power preserves physical feasibility; this step concerns only word
syntax, which is conjoined with the exact physical condition of Sections 2--4.

Here linear size counts DAG nodes and operand occurrences; printed auxiliary
names can add logarithmic bookkeeping overhead. Neither Python wall time nor
SMT solving time is asserted linear.

Boolean sharing is essential. The export uses named defining equations; it
never expands the DAG into a disjunctive normal form. Each if-then-else and XOR
can be represented by a bounded-size propositional/linear subcircuit. Together
with uniquely defined constant quotients this proves Theorem A.

## 6. From supplied schemas to the all-coordinate NP upper bound

Use the inherited complete finite-word cover, not a guessed restriction on
arbitrary trajectories. A prefix ending at its Nth contained defect has exactly
N defects, and belongs to a schema with at most 5(N+1) powers and
2048(N+1)+N fixed letters. Each powered word is a phase of W104, T24 or A28,
of maximum length 104. These restore heading and have strides in D after
rotation. Thus a whole schema spelling is O(N), with independent repetition
variables. This is Section 3 of presburger-defect-reachability.md; its full
finite-path coverage remains an imported, unformalized project dependency.

A nondeterministic algorithm guesses that polynomial-length schema. It does
NOT enumerate the exponentially many schema spellings or loop-slot placements.
Use m independent initial coordinate pairs, conjoin pairwise distinctness, and
apply Theorem A with those m singleton source terms. Conjoin exactly N defects,
a bad final letter and Q on the parameters and affine endpoint outputs. All
integer constants and coefficients retain their binary input encoding. The
result is a polynomial-size quantifier-free linear-integer circuit.

Choose its Boolean branches nondeterministically and introduce definitions
for every shared arithmetic node. This reduces satisfiability to a polynomial-
size conjunction of integer linear equations and inequalities. The standard
small-integer-solution theorem for integer programming supplies polynomial-bit
integer witnesses. Checking these integers and Boolean gates takes polynomial
time. This proves NP membership, subject to the stated unary/explicit input
encoding. Integer-programming NP membership is imported, not a new ant theorem.
See Papadimitriou, On the Complexity of Integer Programming, JACM 28(4), 1981
(also the 1980 MIT report), and the primary references below.

Completeness: the actual N-event prefix has one of the covered schemas and
satisfies every physical, lexical and source condition. Soundness: the encoded
source and complete planned word execute literally, and its Nth defect is its
last update. A satisfiable graph-only relaxation does not suffice. No previously
unread black site has been removed or introduced during execution.

Polynomial-bit coordinates and powers give an exponential numerical bound for
SOME positive witness, since total duration is linear in those powers. This is
not an efficient numerical search-box algorithm and not a universal bound on
all original coordinate placements or event counts. The finitely many Boolean
cases may still need exponential search in a deterministic implementation.

For mu(N), a row of 2L black cells, starting at its left end facing east,
executes (LRRL)^L. Its cyclic ten-factors are all forbidden, yielding 4L-9
contained defects for 4L>=9. Therefore

    0<=mu(N)<=2*ceil((N+9)/4).

A finite word with minimum initial cost c<=m can be executed with exactly m
initial black cells by padding unvisited cells outside its finite footprint.
Hence the NP query with no coordinate side constraint decides mu(N)<=m.
Binary search on this O(N) range uses O(log(N+1)) NP-oracle calls of polynomial
unary-N size. This proves the FP^NP upper bound for fixed finite targets.

## 7. Actual implementation, controls and timing boundary

The optional module is `verification/presburger_fast`. It uses hash-pinned
`compiler.py` syntax and `isl_exact.py` for baseline comparisons.

- stream_qf.py: exact complete-field parity boundaries, constant-division DAG.
- factor_dag.py: shared suffix-register count and final-event flag.
- numeric.py: independent integer/time-intersection witness checker, sorted
  numerical XOR sweep, complete endpoint membership and lexical counting.
- solver.py/api.py: system-libz3 SMT-LIB decision and independently replayed SAT
  witnesses. Resource exhaustion is UNKNOWN; supplied-schema UNSAT is not a
  complete global exclusion. Unsupported syntax raises rather than weakens.

The numerical checker shares the unchanged schema syntax and fixed-word geometry,
but reconstructs temporal intersections by integer timestamps rather than the
encoder block rules. Separate literal controls move the ant one step at a time.
These are algorithmic cross-checks, not two wholly disjoint formal trust bases.

The final deterministic report records 312 unbounded-integer intersection
identities; 544 parameter instances against BOTH the old ISL compiler and literal
execution; 278 complete valid endpoints; 175175 endpoint-cell controls; 1280
factor tests with a second compressed count; an unbounded 64-power all-standard
count identity; exact all-coordinate marker and rail domains; a complete endpoint
identity over all query coordinates with a remote marker and XOR cancellation;
an equality of the two boundary encodings; eight rejection controls; and an
actual native UNKNOWN resource response. The 10^60-cycle SAT witness is validated
by 272 numerical parity checks, not 10^60 literal iterations.

benchmark-factors.json contains three-repeat local timings at 4,8,12,16 powers,
then only the new circuit at 32,64,128. Exponential OLD case counts above sixteen
are exact combinatorial formulas, not performed old runs or runtime forecasts.
At sixteen, the final median old construction was 3.582292425 seconds versus
0.028013011 seconds for the new 1753-node circuit (about 128x). At 4 and 8 powers,
the old constructor is still faster. At 128 powers, the new count circuit had
14691 nodes and took 0.216318914 seconds in that one run. These are factor-only
costs, not full physical synthesis or complete global-cover costs.

benchmark-decisions.json separately records one-shot supplied-schema decisions.
The old backend first computes explicit semilinear domains/endpoints; the new
keeps a succinct existential circuit. The answer being compared is nonemptiness,
not full-output construction. Three larger examples improved locally; the tiny
rail case got slower. No universal speed multiplier is claimed. Timings are
kept separate from deterministic logical checks and are not byte-replay targets.

No nontrivial full N-event schema cover is exhausted in this work. The old
conservative generator is still available, unchanged. The new NP proof avoids
materializing it in a nondeterministic witness description; it is not a claim
that a practical complete global synthesis frontend has been implemented.

## 8. Position relative to prior work and remaining limits

Quantifier-free encodings of flat path schemas and shared counting automata are
established verification ideas. Decker and Pirogov (2019), for example, encode
flat counting-LTL model checking in quantifier-free Presburger arithmetic. They
are credited as prior methodology; our physical stream-parity coverage is what
permits applying a polynomial succinct representation to this ant input class.
The generic initial-read/alternation method remains the project's credited
Gajardo methodology; the retained full-drift period checks are not rediscovered.

The [resource-spectrum theorem](defect-resource-spectrum.md) concerns explicit
effective piecewise-affine minimum-root-cost and defect spectra. The present
restricted-syntax succinct decision upper bound complements its general
partition/counting statement. No comparative timing against that relation
compiler is claimed.

Missing: efficient complete all-schema search at useful N; sharp practical
complexity of those instances; deterministic polynomial-time existence; arbitrary
quantified source/target NP bounds; global mu divergence; a finite HC counterexample;
HC. A small encoding for every finite budget is not termination of its unbounded
sequence. Published priority and independent correctness review remain separate.

## Primary external references checked for this work

1. C. H. Papadimitriou, On the Complexity of Integer Programming, JACM 28(4),
   1981, 765-768; MIT-LCS-TM-152 (1980).
   https://dspace.mit.edu/handle/1721.1/148979
2. N. Decker and A. Pirogov, Flat Model Checking for Counting LTL Using
   Quantifier-Free Presburger Arithmetic, arXiv:1901.05692v1, 2019.
   https://arxiv.org/html/1901.05692v1
3. Official ISL integer-set library manual: https://libisl.sourceforge.io/user.html
4. Official Z3 C API: https://z3prover.github.io/api/html/group__capi.html

The references support imported methods and library contracts, not a claim
that an external source has established these new Langton-specific conclusions.
