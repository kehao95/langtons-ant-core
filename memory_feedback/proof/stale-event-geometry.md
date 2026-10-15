# Spatially local stale-event macros and quadratic finite-prefix time

**2026-10-12.** Literal classical two-colour ant on Z^2, white right / black
left, flip then move. States are pre-update and the COMPLETE initial black
set is finite. Evidence: analytic, unformalized, plus dedicated exact finite
checks. No Lean theorem, third-party independent review or priority claim.

Base read from the remote project: `432814c2c0389542dda21ffc1d74cfb4b6977b4e`.
This note strengthens the quantitative finite-event prefix bounds, rather than
constructing the still-missing total budget on the NUMBER of events.

## 1. Statements and exact scope

For D>=1 let Q=2^D. S_D is the intrinsic local event: the current cell is black
and absent from the preceding D pre-update read positions, recovered by the
literal inverse if necessary. A finite event macro stops immediately AFTER its
first S_D update. Its duration is the event offset plus one, so the next macro
cannot count the same event again.

Put C(X)=conv(B union {p}), and let W be its l_infinity diameter: the greater
of its x-span and y-span. If R is the largest initial head-to-black l_infinity
distance, W<=2R (and R<=W). Both W and R are zero for a blank state.

**Theorem A (convex halo).** If the next S_D event exists, every ant position
from the source through its full post-event endpoint lies in

    C(X) + [-5Q,5Q]^2.                                      (A)

The complete endpoint black set also lies there. This is not a restriction
on seed geometry, band width, physical retreat, initial mass or history deletion.
No analogous finite-halo claim is made for an infinite event-free tail.

Let X_n be the full state after n successive S_D events from X_0, and t_n its
absolute update time, with t_0=0. Statements for n>0 are conditional on the nth
event actually existing.

**Theorem B (linear spatial expansion and quadratic time).**

    C(X_n) subset C(X_0) + [-5Qn,5Qn]^2,                      (B1)
    R(X_n) <= W+10Qn,                                        (B2)
    t_n <= Q*n*(W+2Q+10) + 5Q^2*n*(n-1) =: T_D(n,W).        (B3)

The same spatial enclosure covers every intermediate position up to t_n.
This improves the previous general exponential deadline in n. It does NOT
bound n itself or assert that the macro iteration eventually stops.

**Theorem C (positive HALT conversion).** For an explicit q-state finite local
observer of radius r, if its first HALT occurs with at most b S_D updates
strictly before it, then its HALT time tau satisfies

    tau < Q*(b+1)*(W+2Q+10+5Qb) + Q*(r+q).                  (C)

HALT has priority over S_D at the same pre-update time. The budget b is a
SUPPLIED premise; no total bound b(X) is constructed for arbitrary HALT-positive
inputs. In particular (C) is not an all-input HALT decision algorithm.

## 2. Existing dependencies used, not silently strengthened

The prior `stale-memory.md` establishes an order-D suffix predictor f_D and

    actual turn != f_D(last D turns) iff S_D,

where a mismatch is necessarily predicted R / actual L. When S_D is absent,
there are at most Q suffix states, so a prediction repeats by j<=Q and has a
cycle of length P<=Q. The physical waiting bound is

    next event offset < Q*(R+2Q+10).                        (1)

An event-free suffix cycle must have heading restored and nonzero drift. A
closed/rotating planned orbit cannot remain physically correct forever: two
repetitions of a closed-pose block would repeat the complete state, contrary to
classical unboundedness (or the prior strictly increasing clock).

The prior `local-observer-macros.md` establishes the first-HALT-or-event bound

    first trigger offset < Q*(R+2Q+r+q+10),                 (2)

including the case of a late HALT on a forever event-free trace. The complete
black field is used in that theorem; unread debris may affect a neighbourhood
observer. (2) is not an arbitrary HALT bound when events keep intervening.

The present result adds GEOMETRY to these exact temporal interfaces. Its new
proof is the periodic-plan enclosure below, followed by finite telescoping.
It does not rely on the general oblique-strip/MSO arguments.

## 3. A geometric lemma for ANY translating periodic motion plan

Start at Y=(B,p,h). Let a nonempty word u of length P restore heading and have
nonzero drift d. Write its pre-update phase positions as q_0,...,q_(P-1), q_0=p.
The prescribed infinite positions are q_i+k*d for k>=0. These are at first just
a MOTION PLAN: executability is not assumed.

Until its first read mismatch with literal LR dynamics, the plan is the actual
orbit, by induction on updates. All earlier plan writes then legitimately
contribute to its current read colour.

### 3.1 Only finitely many old-field and self-read changes matter

A previous phase j visits the position q_i+k*d precisely when

    q_j-q_i=s*d,  s>=0, and (s>0 or j<i),  k>=s.

For each phase pair this toggles parity at one threshold s. Let K_self be the
maximum of all these s and zero. Since the two phase points are connected by
at most P unit moves within the block,

    K_self*||d||_infinity <= P.                              (3)

Let K_B be the greatest epoch k>=0 for which some q_i+k*d is in the ACTUAL
finite set B. If there is no such pair, put K_B=-1. This maximum is finite.
If K_B>=0, retain one corresponding black point

    z=q_j+K_B*d in B.                                       (4)

Put

    K=max(0,K_self,K_B+1).                                  (5)

At every epoch k>=K the old field contributes zero at every phase and every
self-read threshold has stabilized. The prescribed read-colour vector is thus
constant in k there. If a mismatch exists at all, a FIRST mismatch must occur
within epochs 0,...,K, hence at an offset strictly below (K+1)*P.

This remains true if early old-black cells temporarily mask a self-inconsistent
motion plan. Such masking ends by K_B+1 and has not been silently discarded.
The argument works for either direction of colour mismatch; its later suffix
instantiation has the special R-to-L mismatch property.

### 3.2 The same cutoff bounds SPACE by a constant halo, not by travel time

We prove that every prescribed read in epochs 0,...,K is in

    conv(B union {p}) + [-3P,3P]^2.                          (6)

If K=K_self, (3) gives ||k*d||<=P for all k<=K, while ||q_i-p||<=P. These
points are within 2P of p, already sufficient for (6). If K=0 the statement is
immediate.

Otherwise take K=K_B+1 and the old black point z from (4). For 0<=k<=K_B and
K_B>0, put lambda=k/K_B. Then

    q_i+k*d = (1-lambda)*p+lambda*z
              +(q_i-p)-lambda*(q_j-p).

The first two terms lie on the segment [p,z]; the remainder has l_infinity norm
at most 2P. For k=K_B+1, add d to the k=K_B expression; ||d||<=P, giving 3P.
When K_B=0, the two epochs k=0,1 are within 2P of p directly.
Thus (6) holds in every case, including ties between maxima in (5).

In particular, if the plan has a first physical mismatch, ALL positions before
and AT that read satisfy (6). Executing the actual mismatched move instead of
the planned one adds at most one unit of halo. The old field and every new
black cell at the resulting complete endpoint also lie inside (6) enlarged by
one, since each new black cell is a previously updated location.

There is no claim that an arbitrarily long VALID event-free translating tail
stays in (6). The finite mismatch is an essential hypothesis.

## 4. Proof of Theorem A, including rotating/closed plans

Run the order-D predictor from X until an immediate S_D event or a repeated
suffix. Before the repetition j<=Q, all written cells and the head are within
Q of the original head, so

    C(X_j) subset C(X)+[-Q,Q]^2.                             (7)

An immediate event and its outgoing move have the claimed bound trivially.
At a repeated suffix the plan cycle has length P<=Q.

If the heading is restored and drift is nonzero, apply Section 3 from the full
state X_j. A finite next event is exactly its first mismatch. By (6),(7) and
the real final update, the entire macro stays within halo

    Q+3P+1 <= 4Q+1 <= 5Q.                                  (8)

If the cycle rotates heading, repeat it at most four times to get a closed-pose
plan; if its displacement is already zero use one copy. This closed plan has
length L<=4P. Each point of a closed unit-step walk is reachable from its origin
in either time direction, so its distance from the origin is at most L/2<=2P.
If TWO copies of that plan were fully executable, they would flip each cell an
even total number of times and restore the pose, repeating the complete state.
Consequently a mismatch occurs before 2L<=8P. All positions up to its read are
in the same closed footprint, and the true mismatched move adds one unit.
The resulting source-relative halo is at most Q+2P+1<=5Q.

Every unchanged black cell was already in C(X), and every newly black cell was
on the bounded read footprint. This proves both the path and complete-support
parts of (A). Neither the geometric convex-envelope theorem nor deleting any
archive is needed for this new bound.

## 5. Proof of Theorem B and the improved coordinate bit bound

Minkowski sums of l_infinity balls add their radii. Applying (A) successively
proves (B1), and also covers the complete trajectory between checkpoints.
The l_infinity diameter of C(X_0)+[-5Qn,5Qn]^2 is W+10Qn. Both the current head
and each current black cell lie in that set, proving (B2).

The nth macro starts after n-1 events. Because event offset < (1), and the
post-event duration is offset+1, its duration is at most

    Q*(W+10Q*(n-1)+2Q+10).

Summing from 1 through n proves (B3). These are integer non-strict bounds for
post-event time; the event itself occurred one update earlier.

The old exponential event deadline remains sound; this is a stronger conversion,
not a retraction of its proof. No claim of a best constant or sharp lower bound
is made. Smaller D can produce more events, and the constants are exponential
in D; the comparison is for each FIXED D as n grows.

### Complete XOR histories still have a growing number of terms

In the prior symbolic representation, a skipped periodic phase adds a finite
arithmetic segment of actual read positions, and ordinary updates add singletons.
Starting from an explicit m-black input, every generated term endpoint up to
n events is an actual read location covered by (B1); original singleton terms
also lie in that hull. This is true BEFORE syntactic cancellations, since a
term is produced from a genuine finite path, not from invented archive filling.
Each nontrivial segment has nonzero integer stride, so its length is at most
W+10Qn+1 (distance between its two endpoints is length-1 times a norm >=1).
If initial absolute coordinate bit length is b, endpoints and lengths thus have
bit length

    O(b+D+log(n+1)),                                        (9)

improving the earlier O(b+n(D+1)) estimate from the exponential deadline.
The NUMBER of terms can still grow as m+n(9Q+1). Thus (9) is NOT a constant-size
memory theorem, not a finite-state quotient, and not logarithmic-in-n runtime.
Temporary inverse-history reconstruction adds at most D additional local moves;
it changes neither the returned state nor this asymptotic bit bound.

## 6. Necessary feedback density on any infinite event chain

Let N_D(t)=#{s:0<=s<t and S_D(F^s X_0)}. If the chain has infinitely many S_D
read events, all n occur and (B3) implies the exact lower bound

    N_D(t) >= max{n>=0:T_D(n,W)<=t}.                         (10)

For fixed D and fixed input, the right side is Omega(sqrt(t)), with leading
asymptotic coefficient 1/(sqrt(5)*Q). The coefficient describes the inverse of
this particular upper bound, not the exact physical event density. The code
uses integer binary search rather than floating-point square roots.

A non-eventually-translating finite-support orbit must have infinitely many
S_D for EVERY D: if some D has only finitely many, restarting after the last
one and using the prior stale theorem gives a translating tail. Thus (10)
applies for every D to any such orbit. Except for at most |B_0| initial black
lifetimes, the events consume black lifetimes created after input time.

This improves the old logarithmic density lower bound. It does not prove that
these events are computationally independent bits. A frequent interruption can
be redundant; at D=1 even ordinary P104 has infinitely many events.

A distinct all-orbit corollary is exact but not claimed as an effective test:
if N_D(t)=o(sqrt(t)) for SOME fixed D, then S_D is finite and the trajectory is
eventually translating. No theorem says this little-o condition holds for every
finite seed, and observing a finite quiet prefix does not establish it.

## 7. Proof of Theorem C and the precise remaining budget problem

Let e be the actual number of S_D events strictly before first HALT tau.
After those events, the head/field has radius at most W+10Qe by (B2); observer
state has been carried across all prior samples. Apply (2) to the next trigger,
which must now be HALT, possibly simultaneously with an S_D read. Hence

    tau < T_D(e,W)+Q*(W+10Qe+2Q+r+q+10)
         = Q*(e+1)*(W+2Q+10+5Qe)+Q*(r+q).

This expression increases with e>=0, so any supplied b>=e proves (C).
The equality is checked as exact integer algebra in the implementation.

It remains possible that positive instances require an uncomputably large
number e as a function of their finite input. That is EXACTLY the missing
budget in the earlier local-observer theorem. No proof here bounds e in terms
of input alone, or gives coverage of infinite observed event chains.

It is tempting to argue 'linear space and quadratic time in event count cannot
be universal'. This is invalid: an ordinary step-by-step computational model
can also use at most linear new space in its step count, and its number of
steps before halting need not have a computable bound. The current result is a
physical resource RELATION, not a restriction on the computational operations
performed from one event to the next. It cannot alone rule out a growing tape,
queue, or a different encoding of computation.

## 8. Reproduction and finite falsification controls

Run `python check.py` without `-O`, using Python 3.10+ and only its standard
library. The project runner works in a temporary copy; existing baseline source
bytes are pinned to the Git blob IDs in `check_results.json`. It does not modify
or recheck old single-black proofs or unrelated certificate libraries.

The tests cover exact complete source/post-event states, all intermediate
positions in finite macros, cumulative hull and time bounds, generic periodic
motion plans with self/old-field mismatches, long preinstalled two-row rails,
closed/rotating geometry, input validation, and exact inversion of the deadline.
The reference simulator uses direction vectors and a separate inverse update.

A genuine 104-period control with a virgin black cell 10^12 periods ahead has
its first mismatch at offset 104000000000000. Its prescribed footprint to that
read is verified inside a 312-cell halo of the COMPLETE source convex hull by
209 phase-segment extreme points, without expanding the enormous trajectory.
The opposite control explicitly checks that the unperturbed event-free highway
eventually leaves every fixed source halo. Thus the finite-event hypothesis is
not silently dropped. The huge-control input already has huge source diameter;
it is not a violation of the linear-per-event spatial expansion bound.

Finite tests supplement the analytic all-input proof in Sections 3--7; they do
not establish it by exhaustive seed simulation. No complete nonuniversality,
HIGHWAY classification, standard-period uniqueness or finite negative seed is
claimed. The runtime MSO compiler is not used or introduced by this result.

## 9. Provenance and publication

This proof and its checkers were prepared against `432814c2c0389542dda21ffc1d74cfb4b6977b4e`
and first delivered as a conversation package because that preparation session
could not write to the remote. The current integration preserves the proof and
exact checker bytes, reruns the dedicated suite, and publishes them as project
files. The integration report records source hashes and the actual scope.
No remote-publication statement is a mathematical promotion. Existing symbolic
runtime dependencies and old ledger volumes remain unchanged.
