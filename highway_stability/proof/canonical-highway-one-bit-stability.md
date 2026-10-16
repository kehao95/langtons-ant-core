# Uniform one-bit recovery along a canonical Langton highway

**15 October 2026. Research baseline:**
`kehao95/langtons-ant@6afea97c2a8a26d03b2bf89de9d23a87d64a31e0`.

Status: analytic infinite-parameter reduction plus a finite exact certificate,
independently replayed in Python and C++. No Lean formalization, outside
mathematical peer review, exhaustive priority certification, or HC proof.
This is a positive recovery theorem, not another hypothetical-tail exclusion.

## 1. Complete input family and the result

The classical ant reads white/R or black/L, turns, toggles the current cell,
then moves one unit. Positions are in Z^2, headings N,E,S,W are 0,1,2,3.
A state at time t is BEFORE update t. Let F be the literal reversible update.
Use the complete thirteen-black seed

    P={(0,-2),(0,-1),(0,0),(1,-1),(2,-1),(2,1),(3,-2),
       (3,1),(4,-2),(4,0),(5,-1),(5,0),(6,0)},
    X0=(P,(0,0),S).

Its exact turn stream is W^omega, with drift d=(2,-2) every 104 updates, where

    W=LRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLR.

The finite full-field verifier proves this assertion for all epochs. To pin
"standard" rather than merely period 104, the checker also reproduces the
all-white ant's first 9977 updates from heading N and its next 104 letters,
obtaining this same W, and certifies its entire periodic future. Those standard
facts are a checked reference, not a new claim of discovery.

Write Xt=F^t X0=(Bt,pt,ht). For a site q define the one-bit perturbation

    Y(t,q)=(Bt symmetric_difference {q}, pt, ht).

This can REMOVE an existing black cell or ADD a new one. It retains every other
black cell of the actual canonical history. The time t and the site q are
arbitrary, unbounded integer inputs; the ant's pose is not externally reset.
After the one-time initial perturbation the ant evolves autonomously.

**Theorem A (uniform recovery after impact).** For every t>=0 and every q in Z^2,
Y(t,q) eventually follows standard P104, allowing a different heading, location
and phase. Let s be the first update >=t at which the UNPERTURBED orbit reads q.
If s does not exist, the entire future read trace is unchanged. Otherwise the
perturbed ant first disagrees at update s and is in a permanent standard future
by update

    s + 64584.

Between that impact and the certified recovery boundary, every perturbed head
position lies within Chebyshev distance 78 of q. Cells outside that square are
unchanged DURING this recovery interval; this is not equality with the evolving
unperturbed field at the same final time. The outgoing standard highway itself
is unbounded and may point in any of the four diagonal directions.

The time bound is not claimed sharp: certificate times were selected on a
104-step inspection grid. There is no uniform bound on s-t, since an obstacle
may lie arbitrarily far ahead.

**Theorem B (age-independent response).** At a fixed standard phase, flipping
the CURRENT cell has exactly the same infinite read/position trace, after
translation of the period origin, for every canonical age n>=25 full periods.
The complete fields may differ by untouched old tail. In fact the certificate
gives smaller phase-dependent thresholds N_r, 0<=N_r<=25.

**Theorem C (defect budget and effective scattering).** Let J10 use the actual
nine inverse turns and the current turn, tested against the cyclic length-ten
factors of W. A current-cell flip at any Xt has at most 33586 future J10 events;
this maximum is attained at t=800 (period index 7, phase 72). A flip at arbitrary
q has at most 33595 future J10 events, including possible initial inverse-history
boundary effects; optimality of this latter bound is not asserted.

Given t and q in binary, there is an exact polynomial-bit-time algorithm returning
a standard-recovery certificate and a compressed expression for the COMPLETE
endpoint black field. Its literal scattering work is bounded by 64584 updates;
it does not simulate t or the first-impact delay. This complexity claim fixes
the finite certificate as part of the algorithm, not as variable-size input.

**Scope:** the family is the orbit of the stated complete P. It is NOT the set
of all states whose read trace happens to be standard, because those states
can have arbitrary additional unread debris. It is not a theorem for two or
more toggles, repeated environmental interventions, or arbitrary finite initial
black sets. Those distinctions are essential for Section 8.

## 2. Exact complete-tail recurrence

Let q_0,...,q_103 be the pre-update positions of one W period from X0 and let
T be the XOR set of these 104 positions (repeated positions cancel). The exact
complete period identity is

    F^104 X0 = ((P+d) disjoint_union D, d, S),

where the twelve-site deposited set is

    D={(0,-3),(0,0),(1,-4),(1,-3),(1,-2),(2,-1),
       (2,0),(3,0),(6,-1),(7,-1),(7,0),(8,-1)}.

Equivalently D=P XOR (P+d) XOR T. The points of D occupy distinct full classes
modulo Z*d; no D-k*d, k>=1, meets P. The full-field calculation and these finite
integer-ray statements are verified, not assumed from a repeated picture.

Translate the complete state at time 104n by -n*d. Its head is again at the
origin heading S and its field is

    C_n = P disjoint_union union_(k=1,...,n)(D-k*d).          (1)

The formula follows by summing the period write sets, or by telescoping
C_(n+1) XOR C_n=D-(n+1)d. It includes exactly 13+12n black cells, not just an
active template. At phase r, let T_r be the XOR of the first r phase positions.
The normalized field is C_n XOR T_r and the normalized pose is (q_r,h_r).
In particular, for n>=N the difference between phase-r sources is

    union_(k=N+1,...,n)(D-k*d).                             (2)

The same difference holds after toggling their common current cell q_r.

## 3. The guarded-extension lemma

We use an elementary first-difference coupling, already implicit in earlier
full-history scattering proofs. If two initial fields at the same pose differ
only on E, and one trajectory never reads E, then both entire read/position
traces agree and their field difference remains E. Proof: before any first
read of E, the current colours agree and the same cell is toggled on both
fields. Induction rules out a first differing update.

For phase r set

    A_N = union_(k>=N+1)(D-k*d).

This INFINITE set is only an exclusion region for a finite-certificate check.
It is never used as an infinite-background input to the physical theorem.
Every source in (1)-(2) is finite.

**Lemma.** Suppose the current-cell-perturbed source at age N, phase r, has a
finite trajectory of length L to a completely verified permanent standard
suffix. If its finite read footprint AND the suffix's entire read footprint
avoid A_N, then every perturbed source at age n>=N has exactly that same infinite
trace in the normalized frame. If the nine recovered inverse reads also avoid
A_N, the intrinsic J10 history and all future event counts coincide.

**Proof.** The actual finite field difference in (2) is contained in A_N.
The forward coupling proves the first claim without deleting those cells.
The reversible rule applies the same induction to the nine inverse steps,
which proves the last claim. The original inverse history of the UNPERTURBED
state must not be substituted: flipping the current cell can change that past.

### Finite checking of the infinite guard

For a finite read p, membership in A_N asks whether e-p=k*d for e in D and
integer k>=N+1. For a standard suffix with phase reads v_i and drift e_out,
its complete footprint is the union of rays v_i+j*e_out, j>=0. A guard hit is
therefore an integer solution of

    v_i+j*e_out=e-k*d,  j>=0, k>=N+1.                     (3)

For nonparallel directions the determinant gives the unique rational j,k,
which are checked for integrality and signs. For parallel equal drifts,
write v_i-e=a*d; a hit exists iff -a>=N+1. For opposite drifts, equal full
classes would yield unbounded k and are rejected. Unequal classes do not meet.
These finite operations check all of A_N and every suffix epoch exactly.

## 4. The finite certificate and universal coverage

The certificate supplies a threshold N_r for each of the 104 phases, and a
record for EVERY pair 0<=n<=N_r. Its threshold sequence, in phase order, is

    8,7,9,2,1,5,1,3,5,15,7,2,2,1,2,6,1,2,5,2,3,11,21,3,4,3,
    2,1,13,17,1,17,3,7,1,3,18,10,7,0,14,8,3,5,9,9,4,4,9,4,
    5,25,9,13,2,12,7,2,0,16,9,14,12,14,0,3,2,4,14,3,4,8,11,
    6,12,5,12,4,4,15,14,0,0,15,1,15,0,8,0,1,0,3,1,4,2,5,8,
    1,3,0,3,2,1,1.

Thus there are 635 finite exceptional cases n<N_r and 104 infinite-family base
cases n=N_r, 739 records in total. The checker demands exact equality with this
index set, not just that each supplied record passes individually.

Each record declares a finite recovery length, endpoint pose, standard suffix
phase, exact intrinsic defect count, and last defect time. The verifier rebuilds
the complete source, toggles the current cell, reconstructs nine actual inverse
reads, replays EVERY update of the finite word and checks the endpoint.

It then verifies the proposed infinite suffix against the COMPLETE endpoint
field. At phase i, epoch k, the read bit is

    1_B(v_i+k*e_out) XOR
    parity{(j,s):v_j-v_i=s*e_out,
                 s>0 or(s=0 and j<i), 0<=s<=k}.             (4)

An old black cell causes at most one hit on a phase ray; each earlier-phase
self-write causes one epoch threshold. Checking epoch zero, every threshold,
every old hit and one epoch after every hit covers all constant intervals,
including the final infinite interval. This is a finite proof of permanence,
not observation of many repeated cycles. The recovered nine-turn suffix must
also be exactly the cyclic history of the outgoing word.

For each base n=N_r, the finite footprint, inverse reads and all future phase
rays are checked against A_(N_r) by (3). The guard succeeds for all 104 bases.
The lemma proves the same infinite trace and defect count for every n>=N_r.
The remaining n are explicitly covered. This is the all-age quantifier bridge.

Across all records the largest certified recovery length is 64584, at n=22,
r=51; the largest pre-recovery Chebyshev radius is 78, at n=25,r=51. The largest
future J10 count is 33586, at n=7,r=72. No J10 occurs after the verified suffix
begins, since both its forward word and its nine-letter seam are standard.
This proves Theorems A-C for current-cell perturbations, including the attained
defect maximum. It proves Theorem B because every N_r<=25.

The constants are certificate outputs with exact reproduction. The time and
radius bounds are sufficient bounds, not declared optimal across possible
choices of recovery boundary. In particular 64584 is not asserted the latest
FIRST time of standard entrance.

## 5. Arbitrary cell position, including deletion of an old black cell

For an input time t and site q, the unperturbed first future read is

    s=min{104n+i >= t : q=q_i+n*d, n>=0, 0<=i<104},          (5)

when this finite set is nonempty. Each i determines at most one n, so (5) is
computed with 104 integer collinearity/divisibility checks, even for enormous
coordinates. If empty, q is never read and coupling makes the entire future
unchanged.

If s exists, the two fields differ at q until that first read, and their forward
poses and letters agree. At time s the perturbed state is EXACTLY X_s with its
current cell toggled. Write s=104n+r and translate by -n*d. Section 4 applies.
Recovery occurs within 64584 further updates in radius 78 about the impact q.
This proves Theorem A for ALL t and q, not just points in a bounded rectangle.

Before impact, the actual forward letters equal the canonical W stream.
Only windows meeting the input's negative-time history, at most nine of them,
can be J10. The post-impact complete state has at most 33586 future events.
Thus the safe arbitrary-site bound is 33595. If q is never read, the bound nine
suffices. No equality with the original negative-time canonical history was
silently assumed.

## 6. Exact compressed endpoint, with all previous black cells

Given a finite impact s=104n+r, use the reference record
m=min(n,N_r),phase r. Replay its at most 64584 steps from the bounded source
C_m XOR T_r with q_r toggled, and collect the XOR set Z of written cells in the
NORMALIZED frame. If p_end is its normalized endpoint, the actual complete
post-recovery field and pose are

    B_s XOR {q} XOR (Z+n*d),
    p_end+n*d, h_end.                                     (6)

The reference time s describes B_s via (1) and its r partial writes. Thus (6)
retains arbitrarily many old black cells as finitely many arithmetic segments;
it does not return only a clean standard core. Membership can be computed by
exact integer interval tests. The return value records the suffix word/heading
and the verified guard reference as well.

All input-dependent arithmetic has polynomial bit size in t and q. The number
of literal recovery updates is an absolute constant, and the complete endpoint
has a compressed representation of input-polynomial size. This proves the
algorithmic part of Theorem C. It is a total query on this explicitly described
family, not a total HIGHWAY solver on arbitrary finite black sets.

The implementation was also checked at a canonical age 10^60 periods without
expanding the history. The chosen remote cell is first read after 974 further
updates, then the reference requires 6552 recovery updates; 640 finite XOR
write terms supplement the retained old-field formula. This is an exact
large-integer example, not a simulated 10^60-step trajectory.

## 7. Evidence and comparison with prior work

The independently written Python verifier performs 6221280 literal recovery
updates for all 739 records; the C++ implementation reconstructs the same finite
sources and endpoints and agrees on every record. The Python verifier checks
128303 future parity breakpoints and all 104 infinite tail guards. It also
checks source recurrence, inverse round-trips, integer-ray cases, arbitrary-site
first-hit formulas, corrupted certificates and a blocker 10^30 periods ahead.
The endpoint-query tests compare 21 COMPLETE physical endpoints and three
unchanged-read cases. Exact reports, source hashes, and replay recipes are kept.

The finite word/phase-ray method is prior methodology, not claimed new here.
The canonical old implementation `one_black/python/src/langtons_ant/single_obstacle.py`
at the baseline commit already proves P union {q} converges for every q, using
22 frontier rays plus a finite active-white list and an all-depth wake guard.
Its documentation explicitly excludes unrelated historical wake. The present
result does not rebrand that theorem: it quantifies over every time of the
complete growing canonical orbit, allows both white-to-black AND black-to-white
flips at that time, and proves uniform post-impact time, spatial radius and
intrinsic defect-count bounds. The general coupling mechanism is inherited;
these expanded input quantifiers and complete new 739-case certificate are the
new verified content.

Gajardo (2003), *A symbolic projection of Langton's Ant*, supplies the established
same-cell alternation/forbidden-word viewpoint, DOI 10.46298/dmtcs.2312.
The known nonzero periodic-word realization and ray-verification methods are
credited in the existing project wake proofs and to A. Jillhewar (2026).
The present checker spells out the exact parity expression (4) directly.
A targeted public literature query did not establish publication priority;
an independent novelty review and mathematical review are still required.

## 8. What this does and does not do for HC

This provides a positive basin theorem for an infinite, unbounded-cardinality
family WITH its generated history. It demonstrates genuine recovery rather than
merely classifying a presumed final wake, and gives an explicit total defect
budget on this family. It does not prove such a budget for every finite input.

The result does not automatically iterate after two errors. The first repair
creates a new complete field with a scatter scar; although its future is standard,
that field need not equal any unperturbed X_t. Declaring its unread scar harmless
for a future perturbation would repeat the earlier failed cleanup assumption.
An extension must either prove protection for every subsequent repair or show
that a richer family of complete repaired states closes under the operation.
Neither closure theorem is supplied here.

Likewise arbitrary additional finite debris on a standard-realizing state is
not part of the source family. It may lie outside the original highway's reads
but inside the perturbed recovery or the redirected suffix. The earlier
repair-closure counterexample shows exactly why this quantifier cannot be added
without proof. No result here says every finite initial state reaches a canonical
one-bit neighborhood. HC, drift-only P104 uniqueness, and general nonuniversality
remain unresolved by this package.

The natural paper is a uniform recovery result with a small parameterized
scattering certificate, not another claimed proof of HC or of the old single-
obstacle theorem. It is a publication candidate, not an acceptance/priority claim.
