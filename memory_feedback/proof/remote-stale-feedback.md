# Endpoint tubes and remote long-memory feedback

The all-input arguments are analytic. Exact deterministic checks include
separately implemented finite dynamics and two infinite-period checks.
The computational trust boundary consists of the analytic coverage arguments
and the supplied exact checkers; these results are not Lean-formalized.

## 1. Model and dependencies

A complete state is X=(B,p,h), with finite B in Z^2 and all other cells white.
Updates read the current cell, turn white/right or black/left, toggle, then move.
States and read events are pre-update. Let F denote this invertible update.

For D>=1, put Q=2^D and

    S_D(X) iff p is black and pos(F^(-j)X) != p for 1<=j<=D.

This is the existing intrinsic finite-local stale-black predicate. It is not
an arbitrary local HALT, nor necessarily a physical PG primary/secondary event.
No transfer between these two event segmentations is assumed in this note.

The existing [stale theorem](stale-memory.md) provides a deterministic predictor
on D-letter turn suffixes, with at most Q states, whose first prediction failure
is exactly S_D. It also gives a total next-S_D-or-permanent-no-S_D procedure on
any complete finite input. The existing [clock theorem](../../clock_escape/PROOF.md) provides the
conservative square first-exit bound

    E(n)=8*n*3^n+1                                             (1)

for a square with n cells per side and arbitrary exterior colours. A sharper
proved square bound may replace (1), but no such substitution is needed here.
The existing [event geometry](stale-event-geometry.md) provides

    T_D(n,W)=Q*n*(W+2Q+10)+5*Q^2*n*(n-1),                     (2)

an upper bound on the post-nth-event time, conditional on that event existing;
W is the l_infinity diameter of B union {p} at the input.

The new ingredients are an enclosure by the TWO EVENT ENDPOINTS, a uniform
bound on consecutive events in a FIXED finite region, a total spatially filtered
event algorithm, and a simultaneous spatial/temporal remote-feedback theorem.
The finite-memory predictor, supplied-word realization criterion, square escape
and quadratic deadline are attributed dependencies, not newly discovered here.

## 2. Two-endpoint tube for a finite event macro

Start at X with head p. Suppose its first S_D event is at offset tau, at cell e.
The macro includes that read and its actual outgoing move, so its duration is
L=tau+1. Let [p,e] denote the real line segment between its endpoints.

**Theorem 1 (endpoint tube and distance-sensitive time).** Every head position
from time 0 through time tau+1 is in

    [p,e] + [-(3Q+1),3Q+1]^2.                                (3)

Every changed cell is in the same tube, and

    L <= Q*||e-p||_infinity + 5*Q^2.                         (4)

The tube does not depend on the radius or cardinality of B. Unchanged black
cells outside it remain physically present; (3) does NOT enclose the full input
black field. A forever event-free trajectory is expressly outside the premise.

### Proof

Until the first event, the actual turns agree with the autonomous suffix
predictor. Its word has a prefix of length j<=Q and a cycle u of length P<=Q.
If the event occurs in that prefix, its whole path and actual outgoing move
are within Q+1 of p, sufficient for (3)--(4).

Otherwise let a be the head after the j-step prefix, and v_i the relative
pre-update phase positions of u. Then ||a-p||<=j and ||v_i||<=P.

First suppose u restores heading and has nonzero displacement d. Write the
event as phase i, epoch k, so

    e=a+v_i+k*d.

When k>=1, any earlier phase position in epoch ell<=k has

    a+v_s+ell*d = (1-lambda)*a+lambda*e+v_s-lambda*v_i,
    lambda=ell/k in [0,1].                                  (5)

The error has l_infinity norm at most 2P. Moving a to p costs at most j;
the prefix is within j of p as well. For k=0 all cycle-prefix positions are
within j+P of p directly. Thus all positions through the event read lie in
[p,e]+[-3Q,3Q]^2. The TRUE mismatched outgoing move costs at most one more.

Also, since d is a nonzero integer vector,

    k <= k*||d|| <= ||e-p||+j+P.

Hence

    tau+1 = j+k*P+i+1
           <= Q*||e-p||+2Q^2+2Q
           <= Q*||e-p||+5Q^2.                               (6)

If the cycle rotates heading, repeat it twice or four times to restore heading.
The resulting geometric block is closed, since its successively rotated drift
vectors sum to zero. If heading is already restored with d=0, use one copy.
The closed block has length at most 4P; its footprint is within 2P of a, because
a point on a closed unit-step walk is reached by either side of the loop.
Thus (3) again holds. Two physically valid copies of a closed block would repeat
the COMPLETE state (every cell is toggled an even number of times), impossible
by classical unboundedness or the strict clock. Consequently tau+1<=j+8P<=9Q,
which is at most 5Q^2 because Q>=2. This proves (4) also in the closed cases.
Every changed cell was a read position, proving the final assertion. QED.

This argument needs only a finite macro to its first event, not a presumption
that any candidate predictor cycle is physically realizable forever.

## 3. The event skeleton carries the large-scale geometry

List the actual S_D event times t_1<t_2<... and cells e_i. Put

    H_D=3Q+2,
    J_m=||e_1-p_0|| + sum_(i=1 to m-1) ||e_(i+1)-e_i||,
    s_m=t_m+1.

**Corollary 2.** Up to the complete post-mth-event state, the entire head path
is contained in the H_D-neighbourhood of the polygonal chain

    p_0 -> e_1 -> ... -> e_m,                                (7)

and

    J_m+1 <= s_m <= Q*J_m+6Q^2*m.                           (8)

In particular, all changed cells are in that tube; the complete state still
contains every unaltered initial black cell outside it.

Proof: each later macro starts one unit from e_i. Replacing that start by e_i
in (3) adds at most one to the tube radius. Sum (4), bounding each later
source-to-event distance by ||e_(i+1)-e_i||+1. The lower bound follows from
unit-speed motion between the actual event cells. QED.

For every real linear functional a, the maximum of a.p_s over this prefix lies
between max(a.p_0,a.e_1,...,a.e_m) and that value plus H_D*||a||_1. Thus, on an
infinite event chain, any direction in which the head is unbounded above is also
a direction in which these event locations are unbounded above. This is a
statement about directional ranges, not limiting speeds or angular convergence.

This is stronger than using the convex hull of the WHOLE black field: far,
untouched black debris does not enlarge the event-to-event tube. It is not an
assertion that the event skeleton itself is bounded or eventually straight.

## 4. A finite-region burst bound, independent of the outside field

Let K be a nonempty FIXED finite set of lattice cells, w its l_infinity diameter,
and choose an axis-aligned square enclosing K+[-H_D,H_D]^2. A sufficient side is

    ell(K,D)=w+2H_D+1,
    b(K,D)=E(ell(K,D)).                                     (9)

**Theorem 3 (bounded internal bursts).** A consecutive run in the EVENT LIST
whose event cells all belong to K has length at most b(K,D). The bound is
independent of the rest of the complete black field and of the starting time.

Proof: start immediately before the first event of that run. Corollary 2 keeps
the whole actual path, through every completed internal event in the run,
inside the square in (9). Its first exit is no later than E(ell). Thus the
elapsed time through any such consecutive completed run is strictly less than
E(ell), and the number of distinct event reads is at most that elapsed time.
The slightly weaker integer bound b is sufficient. Exterior colours can be
arbitrary because they stay unchanged before first exit. QED.

The word 'consecutive' refers to events, not ordinary updates. The ant may
execute many non-event updates between them. Neither infinite local oscillation
nor arbitrarily much exterior storage invalidates this uniform bound.

**Corollary 4 (joint, not merely separate, escape).** For each fixed D, an orbit
has infinitely many S_D events if and only if their positions form an unbounded
set. If the events are infinite, infinitely many lie outside EVERY fixed finite K.

An infinite tail confined to K would contradict Theorem 3 after its last external
event. A finite event list has a finite position set, giving the reverse direction.
This is not a claim that e_i tends to infinity: returns to K can occur infinitely
often, interleaved with external events.

## 5. A genuinely total spatially filtered event algorithm

**Theorem 5.** Uniformly in a complete finite X, integer D>=1 and explicitly
supplied finite K, the following predicate is decidable:

    exists t>=0: S_D(F^t X) and pos(F^t X) not in K.          (10)

The algorithm returns the FIRST such event, when one exists. A negative answer
also certifies eventual nonzero translating periodicity, but need not certify
standard P104.

Algorithm: call the already-total next-event procedure. If it certifies no future
S_D, return NO_EXTERNAL_EVENT and its periodic certificate. If its event cell is
outside K, return that event and accumulated time. Otherwise execute the finite
prefix through that event with the complete field retained and repeat.

Every individual query and finite replay terminates. Were the outer loop infinite,
there would be infinitely many S_D events all in K, contradicting Corollary 4.
This supplies the previously missing loop-termination proof; it is not a chosen
resource cap. More quantitatively, use K union {p_0} in (9): every completed
inside-only prefix has its whole path inside that square, so fewer than its
E(ell) literal updates, hence at most E(ell) internal events, can precede the
final query. The final external event itself may be arbitrarily distant in time.
For K empty, the original next-event procedure suffices directly.

The implementation leaves E(ell) symbolic, instead of attempting to construct
an integer such as 3^(6*2^128). It uses literal replay of inside-event intervals;
no efficient full symbolic continuation is claimed for huge inside intervals.
Optional resource limits return INCONCLUSIVE, NEVER a false negative answer.

### An explicit first-external-event deadline

Let R_0=max_{q in B_0}||q-p_0|| (zero for empty B), and use
ell_0=ell(K union {p_0},D). If an external event exists, its FIRST time is strictly
less than

    (Q+1)*E(ell_0)+Q*(R_0+2Q+10).                           (10a)

Indeed, the head first exits the guard square at some tau<=E(ell_0). Either an
external event has already occurred, or all preceding event cells are in K.
In the latter case the NEXT S_D after tau, if present, cannot be in K: otherwise
(7) would enclose the whole prefix through it inside that square, contradicting
the exit at tau. Apply the existing first-event waiting bound at X_tau, using
R(X_tau)<=R_0+tau. If there is no next event, there is no external event at all.
This is also a direct two-stage decision proof, independent of the loop argument.

For fixed D and fixed K in the normalized p_0=0 frame, the filtered predicate
is polynomial-time in the sparse binary-coordinate input encoding, using the
existing fixed-D polynomial-time next-event procedure. There are only constantly
many internal events, and the TOTAL literal inside-prefix replay is bounded by
E(ell_0), a constant in this fixed-parameter assertion. These constants can be
enormous; no practical efficiency or uniform polynomial bound in D,K is claimed.

Why this is more than the old first-event test: the first many S_D events can
occur inside K and must be ignored. The earlier fixed-n event theorem alone
does not say when that filtering loop stops. The endpoint tube plus finite-domain
escape now proves that it always does.

## 6. Quantitative exterior feedback on every infinite event chain

Let N_D(t) count all S_D reads at offsets 0<=s<t, and M_(D,K)(t) count those
outside fixed K. Internal events occur in at most M+1 runs. Theorem 3 gives

    N_D(t) <= b+(b+1)*M_(D,K)(t),
    M_(D,K)(t) >= floor(N_D(t)/(b+1)).                       (11)

For an infinite S_D chain, define the computable integer

    n_D(t,W)=max{n>=0:T_D(n,W)<=t},                          (12)

with the retained deadline (2). It follows that

    M_(D,K)(t) >= floor(n_D(t,W)/(b+1)).                     (13)

For fixed X,D,K, this is an Omega(sqrt(t)) lower bound as t tends to infinity,
with a very large fixed denominator b+1. It is not an asserted optimal density.
No independent-bit count or computational power conclusion follows from it.
For empty K, use M=N and b=0. No finite observation can establish the premise
that the entire chain is infinite.

### A stronger exterior-only quadratic deadline

The factor b+1 in (13) can be avoided in the LEADING quadratic coefficient.
Augment the state hull by the observation region:

    C_K(X)=conv(B union {p} union K),
    W_K=diam_infinity(C_K(X_0)).

A finite macro ending just after the FIRST EXTERNAL S_D event satisfies

    C_K(X_new) subset C_K(X)+[-9Q,9Q]^2,                    (13a)
    duration <= 2Q*diam_infinity(C_K(X))+20Q^2+b.            (13b)

To prove (13a), if there are internal events, their entire prefix is in
conv({p} union K)+[-H_D,H_D]^2 by (7). The full field at the last internal
post-event state is therefore in C_K(X)+[-H_D,H_D]^2, WITHOUT dropping the
initial field. Apply the retained 5Q next-event convex-halo theorem to the final
ordinary event macro. Since H_D+5Q=8Q+2<=9Q, (13a) follows. With no internal
event, the original 5Q bound is already sufficient.

For (13b), the first internal event, when present, takes at most
Q*diam(C_K(X))+5Q^2 updates by (4). From its pre-read state through the last
internal post-event state there are fewer than b further updates, by the burst
proof. At that boundary the complete head-relative radius is at most
W+2H_D=W+6Q+4. The existing next-event bound makes the last macro at most
Q*(W+8Q+14) updates. Adding these conservative bounds gives
2QW+13Q^2+14Q+b <= 2QW+20Q^2+b because Q>=2. When no internal event exists,
the original Q*(W+2Q+10) bound is smaller. Overcounting the first internal read
only weakens the estimate. For empty K use b=0; the no-internal case applies.

After n EXTERNAL events, (13a) gives augmented width at most W_K+18Qn.
Consequently the post-nth-external-event time, IF PRESENT, satisfies

    U_(D,K)(n,W_K)
      = n*(2QW_K+20Q^2+b)+18Q^2*n*(n-1).                  (13c)

On an infinite chain,

    M_(D,K)(t) >= max{n>=0: U_(D,K)(n,W_K)<=t}.             (13d)

For every fixed K this lower bound has leading asymptotic coefficient
1/(sqrt(18)*Q) times sqrt(t), INDEPENDENT of K. The linear coefficient and the
onset of that asymptotic regime can grow enormously with K through b. There is
no assertion of an estimate uniform in regions K that grow with time. The new
spatial expansion is in EXTERNAL event count; the weaker bound obtained by
multiplying the old all-event deadline by the internal burst count is not used.

## 7. Simultaneously remote, late-born, arbitrarily long black lifetimes

An orbit that is NOT eventually a nonzero translating periodic trace has
infinitely many S_D for EVERY D, by the existing stale-memory theorem.

**Theorem 6 (remote long feedback necessity).** On every such orbit, for every
D>=1, finite K, and time T, there are infinitely many cells/lifetimes described
by times b,e with

    T < b < e,       e-b>D,       x not in K,
    update b reads x white and makes it black,
    update e is its NEXT read, black.                       (14)

These lifetimes can be chosen at infinitely many DISTINCT, unbounded cells.
This does not assert that the whole event sequence eventually avoids each cell.

Proof: restart at the complete state at time T+1. Corollary 4 supplies infinitely
many later S_D events outside K. At most |B_(T+1)| can consume black lifetimes
already present at the restart. Every other such read consumes a lifetime born
at a real forward white update b>=T+1, at the same exterior cell. The intrinsic
S_D condition then forces e-b>D. There was no intermediate read because black
lifetimes end at their next read. Removing the finitely many initial-lifetime
events from an unbounded event-position set leaves an unbounded set, so the
surviving lifetimes can be chosen at infinitely many distinct cells. Equations
(13) and (13d) also give count bounds after subtracting the finite stock. QED.

This is a genuine quantifier strengthening. Separately knowing 'some blockers
are arbitrarily distant' and 'some lifetimes are arbitrarily long' does NOT imply
(14); those could have been different families. The endpoint-tube argument is
what forces long-lived feedback to recur outside every finite region.

It concerns literal S_D consumptions. It must not be relabelled as a theorem that
the same long-lived cells are PG primary/secondary blockers: some S_D events can
occur inside one PG macro, and no transfer theorem is proved here.

## 8. Eventual translation as a filtered-event condition

For EACH input X, let ETC(X) mean eventual nonzero translating periodicity. The
new results give the exact semantic reformulation

    ETC(X) iff exists D>=1, finite K: not ExternalStale(X,D,K).         (16)

The predicate inside (16) is now total computable. The existential choices of D
and K are not bounded by the input. Searching them is only a positive semidecision,
not a total ETC/HIGHWAY algorithm and not a proof that every X satisfies (16).

## 9. Reproduction and evidence

Run `python3 memory_feedback/reproduce.py` from the repository root. The runner
checks this module alongside the other memory results in disposable copies,
comparing deterministic reports with the retained evidence. Python 3.10+ and
its standard library suffice.

The actual run checks 32,107 finite event intervals, 146,940 exact rational tube
memberships, 96 first-external-event answers against independent dynamics, 384 complete-field
external-macro hull/time controls, 606
geometric motion plans at epoch scale 10^50 (25,640 phase-segment extremes),
25,616 binary burst/count controls, 2,800 original and 2,160 exterior-deadline
inversion boundaries, and exact exterior-deadline telescoping.
A full blank-input run with D=128 filters 1,421 internal events and reaches its
last post-event state at time 10,077. A genuine virgin blocker 10^60 standard
periods ahead is detected exactly at time 104*10^60 with no literal inside-gap
replay; a nonintersecting marker is retained and correctly ignored by the read
trace. The two different infinite tests certify the standard positive control.
Thirty-two instances of the previously known two-sweep protocol verify 1,056
created-then-consumed lifetimes; this is a scoped replay, not a new constructor.

All universal claims are carried by the written arguments and their stated
imported results. These finite controls do not replace the missing global
renewal theorem.
