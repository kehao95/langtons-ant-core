# Exact stale-event macros with complete compressed history

**2026-10-12. Evidence: analytic, unformalized, with exact implementation checks.**
This is an exact operational algebra on all finite-support states. It is not a
finite-state quotient, an unproved archive deletion, or a theorem that its
iteration terminates. No new negative seed, global HIGHWAY decider, unrestricted
nonuniversality, Lean theorem or external independent review is claimed.

## 1. Question actually answered

The preceding stale-memory theorem decides the next occurrence of

    S_D(X): current cell is black and not read in the preceding D updates,

using the intrinsic D-step inverse history of the complete input state.
It can give a very late event by ray arithmetic without simulating up to it.
However, a timestamp alone is not an iterable physical interface: the endpoint
may contain enormous newly written wakes. This note constructs that COMPLETE
endpoint exactly, so it can be passed to the next event computation.

All states are pre-update. A macro returning an event stops JUST AFTER its
black read, left turn, flip and move. Its duration is event_offset+1. This
convention ensures successive calls cannot simply report the same event again.

## 2. Finite XOR segments, not infinite periodic background

For integer a,v and n>=1 put

    Seg(a,v,n) = {a+j*v:0<=j<n}.

If n>1 require v!=0. An encoded colouring consists of a finite list of segments
and means their SYMMETRIC DIFFERENCE. A singleton is a segment of length one.
Thus an explicit finite black set embeds exactly as singleton terms. Every
encoded state still has finite support, including after a huge skipped prefix.
Overlaps cancel modulo two; they are never silently interpreted as union.

Membership of a point is the parity of the segments containing it. For a
nontrivial segment, containment is one integer-collinearity test followed by a
finite-index interval test. A literal update and its inverse therefore remain
exactly computable without expanding any segment. Identical singleton terms may
be cancelled syntactically; no cell is removed because it is presumed irrelevant.
The list is not canonical: distinct expressions may encode the same finite set.

## 3. Exact first mismatch against a periodic motion plan

Let a supplied word u have length P, restore heading, and have nonzero drift d.
Its pre-update phase positions are q_i. The proposed future reads are

    q_i+k*d, 0<=i<P, k>=0.

As in the earlier finite-field verifier, an earlier periodic read at this same
position exists for each pair (j,r) satisfying

    q_j-q_i=r*d, r>=0, and (r>0 or j<i), with k>=r.

Each pair toggles read parity at the one threshold r. These are finite in number.

Now intersect a phase ray with ONE old finite segment:

    q_i+k*d=a+j*v, k>=0, 0<=j<n.                       (1)

If d and v are not parallel, determinants give at most one integer pair (k,j),
which is tested against the bounds. If they are parallel but a-q_i is not,
there is no intersection. Otherwise reduce a nonzero coordinate of d to

    A*k-B*j=C, A>0.

Writing g=gcd(A,|B|), there is no solution unless g divides C. When it does,
solutions for k form one residue class modulo |B|/g. The finite bounds on j
supply an interval [lo,hi], intersected with k>=0. Thus (1) is either empty, a
singleton, or a finite arithmetic progression of epochs. The singleton case
also handles length-one terms independently of the unused stride.

For a phase i, its initial-black contribution is the XOR of membership in
these finitely many epoch progressions. Partition k>=0 at all progression
starts, ends+1, and earlier-read thresholds. Within each partition interval,
the active progressions are fixed; their combined parity is periodic in k,
with period dividing the least common multiple of their moduli. The earlier-
read parity is constant on that interval. Test a whole residue period, or the
shorter finite interval. The final unbounded interval has no active finite
segment and needs one parity test.

This is an exhaustive finite algorithm, not sampling a few epochs. It decides
whether u^omega is the exact future; otherwise it finds the first mismatch.
Until the first mismatch the proposed and literal paths agree by induction,
so its position and time are real. The running time can depend on a large lcm.
No polynomial-time claim is made for arbitrary segment-encoded input strides.

## 4. Exact algebra of the skipped writes

Suppose the first n proposed updates have been verified (including n=0).
For each phase i put

    n_i=max(0, floor((n-1-i)/P)+1).

Its updated cells are exactly Seg(q_i,d,n_i), omitting phases with n_i=0.
Therefore the COMPLETE endpoint is

    B_n = B_0 XOR XOR_(0<=i<P,n_i>0) Seg(q_i,d,n_i).      (2)

If n=kP+i, the endpoint position is q_i+k*d and its heading is the recorded
heading before phase i. Equation (2) accounts for every flip, including
self-overlap, overlap between phases, and overlap with every old segment.
It adds at most P terms regardless of n. The helper applying (2) does NOT
assert that an arbitrary geometric word is physically executable; its caller
must first establish validity through the chosen prefix.

At the first mismatch of the recency-D predictor, the planned turn is R and
the actual turn is L. Toggle that point in (2), turn left and move once. This
is the exact full input for the next macro, with no separate history oracle:
the needed preceding D positions are recovered by the literal inverse.

## 5. Total single-event macro and finite iteration

For D>=1 put Q=2^D. The previous suffix identity says that no S_D event means
one deterministic next turn from the latest D-turn word. There are Q words.
Execute at most Q matching turns until an event or a repeated suffix occurs.
In the latter case the prediction has a period P<=Q.

If its geometric period is nontranslating or rotates the heading, two copies
of a closed-pose block of length at most 4P expose a mismatch: otherwise the
complete state would recur and the ant would be permanently confined. Literal
no-bounded-orbit excludes that. Replaying at most 8P steps handles this case.

For nonzero translation apply Section 3. A valid infinite word gives a certified
permanent event-free tail. Otherwise (2) and one real black update give the next
full post-event state. Every input is finite and every arithmetic search here
is finite, so this single macro is total without caller resource caps.

If the input expression has M terms, an event output has at most

    M+9Q+1 terms.                                         (3)

The loose uniform value covers Q preliminary writes, at most 8Q closed-plan
writes, or at most Q new periodic segment terms, and the final event. Inverse
history recovery is temporary and does not alter the returned physical field.
Nontrivial new segment strides are period drifts; both coordinate magnitudes
are at most Q. The same statement applies to a terminating tail's entry state.

After n successive event outputs from an explicit m-black input, the expression
has at most m+n(9Q+1) terms. Every individual call terminates; the iteration over
ALL events is not asserted to terminate. `event_prefix` computes the first n
events, or stops earlier on a certified event-free tail. Reaching its finite
requested event budget is neither HALT nor NO-HIGHWAY. Optional resource caps
return INCONCLUSIVE and do not change the mathematical total algorithm.

## 6. Parameterized complexity of a FINITE event prefix

For an explicit sparse input with m black cells, coordinate bit length b, fixed
D, and an event count n measured numerically (or in unary), the first n events
and their complete compressed endpoint are computable in

    f(D) * poly(m+n+b).                                   (4)

This is not a polynomial bound in log(n), an ordinary-step cutoff, or a claim
that large D is practical. f may be doubly exponential in D.

Here is the bound rather than an assumption of compactness. All initial terms
are singletons, and every nontrivial generated stride has components of
magnitude at most Q by (3). A parallel intersection modulus is |B|/g<=Q.
Hence all residue periods divide Lambda_Q=lcm(1,...,Q), a function only of D.
The numbers of old terms, phase pairs and interval endpoints are polynomial in
m+n for fixed Q. One whole residue enumeration therefore costs a factor at
most Lambda_Q, not a factor equal to the huge skipped physical time.

For bit lengths use the already proved event deadline, or rederive it by
R(F^t X)<=R(X)+t. With C=R(X)+2Q+10, the nth event, if present, occurs before

    C*((Q+1)^n-1).

All segment endpoints come from the initial support or actual reads before
this time. Their binary coordinate and length encodings thus use O(b+n(D+1))
bits. No cancellation-dependent radius computation or hypothesized mass bound
is required. Membership, determinants, gcd and residue arithmetic consequently
have polynomial bit cost; combining these bounds proves (4).

General arbitrary-stride symbolic inputs retain totality but are outside (4)'s
explicit-input/generated-stride premise. The lcm cost must not be hidden.

## 7. What has changed, and what has not

Previously the next-event solver could locate a far mismatch but returning its
explicit wake could require work proportional to physical time. This note
closes the exact ENDPOINT and ITERATION interface: full XOR histories survive
huge jumps and can be consumed by the same exact next-event solver again.
The outcome is a computable unbounded-dimensional arithmetic transition system,
not a bounded-dimensional counter model or finite automaton.

A universal computation can also have efficiently computable finite prefixes.
Thus (4), linear expression growth, and totality of one macro do NOT disprove
universality. Nor does failure to find a monotone rank prove universality.
An infinite sequence can continue creating and consuming old black lifetimes.
Indeed at D=1 no single unit move can revisit its source, so S_1 is just a black
read. The certified standard P104 word has left turns, hence even an ordinary
P104 tail has infinitely many S_1 events. Requiring termination for EVERY D is
therefore false. The sufficient global route quantifies EXISTS D for each seed,
or needs a different complete classification of infinite macro runs.
A global cutoff, a complete no-HALT certificate coverage theorem, or another
all-compiler restriction remains missing. In particular this is not a proof
that some D eliminates all but finitely many S_D events on every seed.

## 8. Reproducible checks

Implementation uses pairs of integers and finite XOR segments. Finite endpoint
controls use a separately written complex-coordinate literal simulator and
compare FULL materialized states, not just poses or local windows. Arithmetic
progression intersections are checked independently by finite enumeration.

The dedicated `check_symbolic.py` passes 348800 ray/segment membership comparisons,
1024 prescribed-prefix full-XOR controls, 2048 exact next-event endpoint controls,
640 successive macro checks, serialization and finite-prefix driver checks.
Counts and source scope are in `check_results.json`.

A second control starts at the COMPLETE blank-orbit state after 12000 steps and
adds one virgin black cell 10^12 highway periods ahead. Its first stale-D event
for D=128 is at offset 104000000000000. Only 104 preceding updates are explicitly
executed; all skipped flips are retained in 1068 finite segment terms (953 source
singleton terms). Feeding the exact post-event state back into the macro solver
finds the next event after 65 further updates. A fixed recipe and digest preserve
the huge endpoint without expanding it. The point probes of this control are
finite implementation checks; the full infinite-family endpoint theorem is (2).

No old one-black proof or shared simulator was modified. No independent review
or formal verification is implied by independent finite reference code.
