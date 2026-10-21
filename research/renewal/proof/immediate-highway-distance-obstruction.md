# Three-step unbounded amplification of distance to an immediate standard highway

**15 October 2026. Remote baseline inspected: `0ef3f0e149044c64f5a4b2b2ea9e192300fbe4f6`.**

This is the outcome of a failed global-termination-rank attempt. The all-parameter
claim below has an analytic proof supported by exact finite premises and two
literal implementations. It is not Lean-formalized, independently reviewed, a
publication-priority claim, an HC counterexample, or a proof of HC.

The padding in this theorem is NEVER READ BY THE ACTUAL TRAJECTORY. In particular,
the unbounded quantity below must not be called actual active memory, genuine
reactivation, or newly generated feedback. This distinction is the point of the
counterexample to the proposed measure.

## 1. The proposed nonlocal measure

Use the complete finite black set B, a fixed position p and heading h, and the
classical white/right, black/left, toggle-then-move update F. Let P_now mean the
entire future from now is one of the standard P104 phases, allowing unread debris.
Define

    delta(B,p,h) = min {|B symmetric-difference C| :
                         C finite and P_now(C,p,h)}.                 (1)

The comparison holds the ant pose fixed. This is distance to the IMMEDIATE
standard target, not distance to the eventual basin HIGHWAY. Allowing arbitrary
positive transients in (1) would change the definition and the argument.

At one fixed pose there are exactly the 104 cyclic turn words to test. For each
phase j let K_j be its clean finite seed and R_j its complete future read set,
a union of 104 forward arithmetic rays. The full-drift chronology construction
of these seeds is inherited from the existing periodic-certification method;
it is not claimed as a new realization criterion.

**Lemma 1 (exact finite computation).**

    delta_j(B,p,h) = |(B symmetric-difference (p+K_j)) intersect (p+R_j)|
                  = |K_j| + |(B-p) intersect R_j| - 2 |(B-p) intersect K_j|,
    delta(B,p,h) = min_j delta_j(B,p,h).                             (2)

Indeed the initial colour of every future-read cell is forced by its first
prescribed read. Every mismatch there must be toggled. Conversely toggling exactly
those mismatches suffices by first-difference induction. Outside the read set the
original finite field may be retained unchanged, so no additional edits are
necessary. All comparisons in (2) are finite integer-ray tests on the complete
input field. The pose normalization uses quarter turns, not reflections.

This was a plausible improvement over counting discrepancies to ONE fixed
reference: (2) minimizes over ALL standard phases and all compatible geometric
orientations. The following theorem still defeats bounded amplification.

## 2. Complete explicit inputs

Let W be the 104-letter word in the pinned verifier and let K be its clean seed
at the origin facing east:

    K={(-7,0),(-7,1),(-6,-3),(-6,-2),(-6,-1),(-6,2),
       (-5,-2),(-5,0),(-5,1),(-5,2),(-4,-2),(-4,1),
       (-3,-3),(-3,1),(-2,-3),(-2,-1),(-2,1),(-1,-2),(-1,0)}.

Thus |K|=19. Its permanent standard word has drift (2,-2) and all its future
reads lie in -10 <= x+y <= 0. Put

    q=(0,0), r=(1,1), p_star=(1,2),
    D4={(2,2),(2,-2),(-2,2),(-2,-2)}.

For integers n>=0 and M>=1000 define the FINITE set

    E(n,M) = {p_star+k*d : d in D4, M<=k<M+n},
    X(n,M) = (K union {q,r} union E(n,M), (0,0), E).                (3)

The four rays are disjoint in the displayed ranges. These inputs have exactly
21+4n black cells. M and n are parameters of DIFFERENT finite inputs, not time
parameters which add cells while one ant is running.

**Theorem 2.** For every n>=0 and M>=1000:

    delta(X(n,M)) = 1,
    PGStep(X(n,M)) = F^3 X(n,M) =: Y(n,M),
    delta(Y(n,M)) = n+10.                                        (4)

Moreover all these inputs have the SAME entire actual turn/pose trajectory, and
its exact first permanent-standard time is

    tau(X(n,M)) = 12440.                                         (5)

All E(n,M) cells are retained physically and remain unread forever. Thus every
input in (3) is HC-positive, including the arbitrarily large amplification cases.

## 3. A genuine three-update physical PG macro

The literal updates of X(n,M) are:

| Offset | Position | Incoming heading | Read | Next pose |
|---:|---|---|---|---|
| 0 | (0,0) | E | black/L | (0,1),N |
| 1 | (0,1) | N | white/R | (1,1),E |
| 2 | (1,1) | E | black/L | (1,2),N |

The endpoint is exactly

    Y(n,M) = (K union {(0,1)} union E(n,M), p_star, N).            (6)

The blank reference first meets a source-black cell immediately at q. The
singleton-q shadow follows LR and first meets a remaining source-black cell at
r, at offset two; that cell is white in the singleton shadow. No other residual
is read before it. Consequently (6) is the canonical advanced PG endpoint,
provided the source is not already P_now.

The first 104 turns of X(0,M), independent of M, are recorded in the finite
report. They disagree with every cyclic phase of W. All padding lies farther
than 104 from the source, so unit speed makes this same finite nonterminal test
valid for every n,M. The PG immediate-terminal branch therefore does not preempt
this macro. No use of the general one-black theorem is needed to discover this
particular two-step residual query.

## 4. Proof of the source and endpoint distances

Every point of E(n,M) has x+y equal to 3, 3+4k, or 3-4k. These are outside the
reference strip [-10,0] for k>=1000. Also r has x+y=2. Hence

    (K union {r} union E(n,M),0,E)

has exactly the unperturbed standard W future. Removing q from X(n,M) produces
that state, so delta(X)<=1. The nonstandard 104-prefix from Section 3 rules out
delta(X)=0. This proves the first equality of (4).

Now fix ANY standard candidate j from the endpoint pose p_star,N. Its period
drift d_j is in D4. The candidate reads p_star+k*d_j at phase zero of epoch k,
so every one of the n padding cells on its own ray belongs to R_j.

It reads none of the padding on the other three rays. To see this uniformly,
write its relative phase positions as a_i, with ||a_i||_infinity<=104:

* On the opposite ray, a possible intersection would give
  a_i=-(k+l)d_j for k>=1000 and l>=0, contradicting the phase bound.
* On either transverse diagonal, a normal of d_j with coefficients +/-1 has
  value +/-4k on k*d. Its absolute value on a_i is at most 208. Again there is
  no intersection for k>=1000.

All clean seed sites are within infinity-distance 104 of their origin: the
chronological construction places each boundary seed cell on the segment between
two phase positions in one full drift class. Thus no padding cell belongs to K_j.
The exact finite library checks give the stronger radius seven, but that sharper
constant is unnecessary for the all-parameter proof.

It follows for EACH of the 104 candidate phases, before taking a minimum, that

    delta_j(Y(n,M)) = delta_j(Y(0,M))+n.                         (7)

The complete 104-entry vector for the base endpoint is computed by (2) and by a
separate direct symmetric-difference/union-of-rays oracle. Its minimum is 10.
Equation (7) gives delta(Y)=n+10. This argument does not select only the standard
phase nearest to the original source, or ignore a different outgoing direction.

## 5. Proof that all padding is inert and every member is positive

The finite source X(0,M) has no M-dependent cells. Two independent literal
implementations, comparing complete fields, verify its state at time 12544:

    position=(-22,4), heading=W, complete black count=803.

The full 803-cell endpoint is retained in base_positive.json. The supplied
period word there has drift (-2,-2). Both the all-epoch breakpoint-parity check
and clean-seed/discrepancy-ray check certify its entire future. Its phase reads
lie in -29 <= x-y <= -19; the drift preserves that coordinate. All prelude
positions through time 12544 have infinity-norm at most 37.

Every padding point has infinity-norm at least 2M-2>37. Its x-y is either -1,
-1+4k, or -1-4k, never in [-29,-19]. Hence padding misses BOTH the complete
finite prelude and every read in the certified infinite future. First-difference
induction proves equality of the whole actual trajectory for every n and M,
without removing any padding cell from the actual physical field.

The actual prelude agrees with the aligned backward extension of the certified
104-periodic tail from time 12440 onward. At time 12439 the actual letter is L,
whereas that backward periodic extension requires R. An earlier standard suffix
would agree with the certified tail for a full period and thus with its uniquely
aligned backward extension as well, contradicting this mismatch. Therefore the
FIRST standard-entry time is exactly 12440, proving (5). A long finite repetition
alone is not used to establish permanence or earliest entry.

## 6. What this invalidates, and what it does not

**Corollary 3.** There is no finite-valued function g(a,L), computable or not,
which bounds delta(PGStep(X)) by g(delta(X),L) on every advanced PG macro of
literal duration L, even when restricting X to HC-positive inputs.

Proof: choose n with n+10>g(1,3) and apply (4). QED.

In particular a global argument based on nonincrease, contraction, or bounded
amplification of this exact immediate-target edit distance fails. Allowing all
104 targets, rather than one reference, does not repair it. Unbounded delta also
does not force unbounded remaining transient time: the entire family (6) has
remaining first-entry time 12437.

This does NOT exclude every nonlinear scalar function of delta, every ranking
function involving other data, a bounded-lookahead construction, a full-input
budget depending on the entire field, or a correct semantic activity measure.
In particular it is NOT a proof that all nonlocal termination ranks are
impossible. The endpoint value grows because a changed pose makes previously
irrelevant cells obstruct hypothetical immediate standard rays; the TRUE future
still avoids all of them. Calling this physical feedback growth would be false.

The theorem is a method obstruction. Its positive-family statement is an inert
extension of one certified finite trajectory, not a new global convergence
class comparable to the one-black theorem. It does not supply the missing
all-input finiteness of J10 or S_D events.

## 7. Reproduction and provenance

Run `python scripts/check_hc_continuation.py`. The isolated checker replays only
this theorem's 12544-update base, complete endpoint, source nonterminal test,
104-phase distances, 416 phase/heading infinite controls and the padding guards.
It compares the optimized distance calculation to direct integer-ray membership,
including coordinates of magnitude 10^150. The analytic ray proof, not finite
sampling of n, carries the all-parameter conclusion.

The known chronology/parity implementation is copied byte-for-byte from
`experiments/hc_global/integration_2026_10_15/periodic_verify.py` and hash-pinned.
No shared simulator, old kernel, all-256-profile search, one-black Lean library,
or published preprint is changed or represented as newly replayed.

The previous package was independently imported by remote commit
`4a762c3dccdf22839249b0e1dde43d5833cc3a6b`. This note and its new code are a separate
local research batch; their presence in an attachment is not a GitHub push.
