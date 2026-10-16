# Birth-filtered feedback and growing-scale necessity for the nonperiodic branch

**15 October 2026. Source repository read: `2396e9fa4365933b74f27dd84a349b331c66088d`.**

This note treats the branch in which a finite-support classical ant never becomes
an eventually translating periodic trace (abbreviated ETC). It does NOT exclude
that branch. The qualitative statement that such a trajectory must consume
arbitrarily late-born, remote, old black lifetimes is ALREADY proved in
`proof/results/remote-stale-feedback.md`, Section 7. We do not claim that statement
anew. The additions are a total FIRST-birth-filtered feedback operator with exact
birth/death/complete endpoint, its effective budget, a growing-scale uniform
consequence, and a compressed implementation that does not spend initial black
lifetimes twice. These are constructive consequences of the retained global
estimates, not a new descending rank or a claim of independent publication priority.

Evidence: written analytic arguments and exact finite implementation controls;
no Lean formalization, outside mathematical review, HC proof, nonperiodic seed,
or proof of finite-support nonuniversality.

## 1. Model and exact question

Use X=(B,p,h), with COMPLETE finite B subset Z^2, headings N,E,S,W. A white read
turns right, a black read turns left; toggle the read cell and then move one unit.
States are before updates. F denotes this reversible literal map. For D>=1 let

    S_D(X) iff p in B and pos(F^(-j)X)!=p for j=1,...,D.

The inverse history is actual inverse dynamics, not a stipulated blank past.
Let K be any given fixed finite set, with no promise concerning the trajectory.
For the source at time zero, define a fresh exterior feedback to be times b<e
and a cell q such that

    0<=b<e,  e-b>D,  q notin K,
    update b reads q WHITE, update e reads q BLACK,
    q is not read at any intermediate update b<t<e.         (1)

Thus (b,e) is one actual black lifetime. Its age uses pre-update indices.
A cell initially in B may qualify after it is erased and written again.
Excluding every INITIAL COORDINATE forever is therefore incorrect. The excluded
objects are only the black LIFETIMES already present at time zero.

The requested output is the smallest possible consumption time e satisfying
(1), its unique birth b, q, and the entire finite state F^(e+1)X; otherwise a
correct negative answer. The physical path outside K is unrestricted.

## 2. Retained inputs, with their uniform parameters

Put Q=2^D. The following results are dependencies from the existing stale-memory,
clock, and remote-feedback proofs, not new claims in this note:

(A) The next S_D or its permanent absence is total computable. A negative answer
    has a nonzero translating periodic suffix certificate.
(B) Every consecutive event-list run of S_D cells in a fixed K has at most

    b_K=8*l*3^l+1,  l=diam_infinity(K)+2(3Q+2)+1              (2)

    events (b_K=0 for empty K). No restriction on exterior colors is required.
(C) If the nth EXTERIOR S_D exists, its post-event time is at most

    U(n,W)=n(2QW+20Q^2+b_K)+18Q^2 n(n-1),                 (3)
    W=diam_infinity(B union {p} union K).

    This bound is uniform over X,D,K,n. It does NOT require a future input
    to supply its true total number of events.
(D) Every non-ETC orbit has infinitely many S_D for EVERY D. Conversely, finitely
    many S_D for one D implies ETC.

For orientation, (B) is not the false assertion about a moving singleton {p_t}.
Between two stale events the actual path lies within 3Q+2 of the segment between
their cells. Thus events in ONE fixed finite K confine the intervening actual
path to a fixed square; a quantitative first-exit theorem gives (2). All input
black cells are retained. The original proof of (C) charges only a 9Q full-field
halo per EXTERIOR macro, avoiding multiplication of its leading quadratic
coefficient by b_K. Its explicit parameter dependence is essential in Section 5.

## 3. First freshly generated remote feedback is decidable

**Theorem 1.** The question in Section 1 has a total algorithm on all finite
inputs. At most M=|B| exterior S_D events can be skipped as old source lifetimes.
The number of ordinary next-S_D calls is at most

    (M+1)(b_K+1).                                         (4)

If a positive answer exists, its post-event time obeys

    e+1 <= U(M+1,W).                                      (5)

A negative answer implies ETC, NOT NO-HIGHWAY. No standardness inference is made.

**Proof.** Follow the exact successive S_D events, keeping the complete field
and the exact already executed read history. Ignore events in K. At an exterior
black read q, inspect its last nonnegative-time read before this event. If that
read exists, it must have been white and is the birth b. Since the event is S_D,
e-b>D. Return it. If no previous read exists, q was initially black: this event
consumes its unique source lifetime. The same source lifetime cannot be skipped
again. A later black read at the same coordinate is a new lifetime and qualifies.

Hence at most M exterior events are skipped. If no qualifying event were found
and the outer loop ran forever, all but finitely many S_D events would lie in K,
contradicting (B). There are at most M+1 internal runs, each of at most b_K
events. Including the final external event or event-free query proves (4).
Because events are processed in order, the returned e is the first eligible one.
A successful event is no later than the (M+1)st exterior event; monotonicity of
U proves (5), even if only fewer than M+1 exterior events ever exist.
If the result is negative, all future S_D events are finite by the same argument,
so (D) gives ETC. QED.

This proves totality without evaluating 3^l for an enormous l. The implementation
uses no guessed time cutoff. Its separate deadline helper retains the symbolic
form A+C*3^l and refuses materializing an excessive exponent; this is not an
answer to the dynamical question.

**Corollary 2 (checkpoint-wise moving observers).** On a non-ETC orbit, start at
any actual checkpoint s. Choose D and any finite K from the known state or known
history (for example a square about p_s, or the entire previously visited set).
The operator necessarily returns a positive lifetime born at b>=s, consumed at
e>b+D, at q outside K, by the shifted deadline s+U(|B_s|+1,W_s).
After e+1 choose a new checkpoint, region and threshold and repeat. Every call
is total and positive under the non-ETC premise. The resulting lifetimes are
nonoverlapping in time; choosing K to include previously selected cells makes
the feedback cells distinct. The thresholds and regions may grow between calls.

There is no moving-region burst assertion: each K is held fixed DURING its own
call. Nor is this a universal termination proof for repeated calls. Finite support
at every restart does not give a uniform bound on the number of restarts.

## 4. Complete-state arithmetic and read provenance

The black field is a finite XOR of finite integer arithmetic segments

    a+j v,  0<=j<L.

An initial explicitly listed field uses singleton terms. Literal updates append
singleton toggles. A verified repeated word u of length P and nonzero drift d
executed n times appends one segment per phase, with length n and stride d.
Partial periods and the event-producing mismatched update are included.
No coordinate is deleted on the basis of expected future inactivity.

In parallel, retain a read record for every phase segment:

    (a,v,L,time0,time_stride,letter).

Its jth read occurred at time0+j*time_stride. These records partition ALL actual
update times, including long skipped blocks. To recover a birth, intersect the
candidate q with each finite segment and take its largest recorded time strictly
below e. A true finite lifetime returns a previous R. For a source lifetime there
is no nonnegative predecessor. This also catches a source black coordinate that
was previously consumed at a NON-stale event and subsequently rewritten.

Here is the next-event implementation, restated to delimit the trusted arithmetic.
From the true D-turn suffix, reconstruct its relative finite path. If the current
position was read within the suffix, predict the opposite of its most recent
turn; otherwise predict R. The prediction fails exactly at S_D. Until failure,
there is an autonomous finite suffix transition with at most Q states. On first
repeated suffix it proposes a periodic continuation. A rotating-heading or zero-
drift cycle closes geometrically after at most four copies; two closed copies
would repeat the full state. The existing strict clock excludes that, so literal
checking finds a mismatch in a finite O(Q) segment.

For a heading-restoring nonzero cycle, at phase i and epoch k the predicted
actual color is

    1_B(q_i+kd) XOR #{(j,a): q_j-q_i=a*d,
                 a>0 or (a=0 and j<i), 0<=a<=k} mod 2.      (6)

The finite-field part is an XOR of ray/segment intersections. A nonparallel
intersection is one integer determinant solve. For parallel directions write
 d=g u, v=h u, a-q=c u with primitive u; eligibility is g k=c+h j.
The congruence h j=-c mod g and finite index inequalities give an exact finite
arithmetic progression in k. Zero-stride singleton terms are checked separately.

Take the least common multiple L0 of the finite progression steps. On each
residue k=r+L0*z, each contribution becomes a finite interval in z; each self-write
threshold in (6) becomes a final interval. Sorted integer parity changes give the
first mismatch, INCLUDING the final infinite interval. Taking the earliest phase
time gives the literal first mismatch, not a heuristic finite-repeat detector.
Correctness follows by induction on the prescribed updates up to that mismatch.
The accompanying complete post-field and read records account for every toggle.

A resource cap on suffix states, event calls or L0 returns INCONCLUSIVE. An
interrupted computation is never a negative certificate. With caps absent, all
finite arithmetic and the loop in Theorem 1 terminate.

For fixed D and fixed K in a translated source-pose frame, and an explicitly
listed sparse initial B, this is polynomial bit time in its input length. The
constant can be enormous. There are O_D,K(M+1) event calls by (4), O_D(1) new
segment terms per call, and all generated stride components are bounded in terms
of Q. Thus L0 divides a fixed lcm(1,...,4Q). Existing finite-macro halo bounds
control coordinate and time bit lengths by the original bit size plus O(log M).
This claim is NOT uniform polynomial complexity in binary D, K's diameter, or
compressed initial BLACK CARDINALITY. Arbitrary compressed finite input is still
accepted by the algorithm, but (4) uses its actual cardinality, not its term count.

## 5. A uniform growing-scale consequence

The earlier remote theorem fixed D,K and a birth cutoff independently of the
observation horizon. Its explicit uniform estimate (3) yields the following
stronger simultaneous rate statement. This is a diagonal consequence of those
estimates, not a new physical law excluding their satisfaction.

Normalize p_0=0 by translation and let M0=|B_0|, W0=diam(B_0 union {0}). For a
horizon H with L=floor(log_3 H)>=64 define, using exact integer logarithms,

    D_H=floor(log_2 L)-5,       Q_H=2^D_H,
    R_H=floor(L/16),            K_H=[-R_H,R_H]^2 cap Z^2,
    s_H=floor(H^(1/4)).

Put l_H=2R_H+6Q_H+5 and b_H=8*l_H*3^l_H+1. Use W=W0+2R_H in (3); it safely
bounds the actual diameter after adjoining K_H. Let

    n_H=max { n>=0 : U_(D_H,K_H)(n,W0+2R_H)<=H }.

**Theorem 3.** On every non-ETC finite-support orbit, by time H there are at least

    max(0,n_H-M0-2s_H)                                     (7)

black lifetimes satisfying simultaneously

    s_H<=birth<death<H,
    death-birth>D_H,
    ||cell||_infinity>R_H.                                (8)

These are distinct lifetimes, not a claimed count of distinct cells or independent
bits. No simultaneous separation or disjointness among all of them is asserted.

**Proof.** Non-ETC gives an infinite S_(D_H) chain for every chosen H. Apply the
uniform exterior deadline to the fixed region K_H, throughout the interval
[0,H). This supplies at least n_H exterior stale events by H. At most s_H
consumptions precede s_H. At time s_H there are at most M0+s_H black lifetimes,
so at most that many later consumptions can have births before s_H. Subtracting
these two finite supplies gives (7). All remaining events have the long-age and
exterior properties by their S_(D_H) classification. QED.

This does NOT replace K_H by {p_t} during a computation. Each horizon has one
fixed region centered at the original pose; the uniform bound justifies choosing
different regions in different applications of the theorem.

The lower bound has an explicit asymptotic rate. For L>=64,

    L/64 < Q_H <= L/32,
    l_H <= (5/16)L+5,
    b_H=O(L H^(5/16)).

The linear coefficient in U is O_X(L^2+L H^(5/16)), whereas its quadratic
coefficient is 18 Q_H^2=Theta(L^2). Hence

    n_H=(1+o(1))*sqrt(H)/(sqrt(18)*Q_H).

Since M0+2s_H=o(sqrt(H)/L), if F(H) counts the lifetimes in (8),

    liminf_(H->infinity) F(H)*floor(log_3 H)/sqrt(H)
        >= 32/sqrt(18).                                   (9)

In particular F(H)=Omega_X(sqrt(H)/log H), while the excluded radius grows as
log H, the required age as log log H, and the birth threshold as H^(1/4).
This is a requirement on a hypothetical counterexample, not a contradiction.
The modest logarithmic scales and potentially enormous onset should not be
advertised as a proof that the required behavior is impossible.

## 6. Actual controls and a failed termination inference

The implementation independently agrees with literal vector dynamics on 120
birth-filtered examples, including finite K filters and complete endpoint fields.
It checks 5,000 exact ray/segment intersections, 800 parity sweeps through the final
infinite interval, 400 forward/inverse pairs, source-coordinate rebirth, four
rotations of a periodic negative input, resource-limit controls and huge epochs.
The independent finite dynamics does not call the predictor or segment algorithm.
An additional explicit-field infinite parity verifier does not use the ray/segment
or residue-sweep routines. These are controls, not an exhaustive proof of software.

A concrete example prevents a particularly easy bookkeeping error. For the saved
12-black state headed S, (1,0) is black initially and consumed at time 1; it is
written white-to-black at time 5 and consumed at 13. With D=4 and K empty the
answer is birth=5, death=13, not a permanently excluded initial coordinate.

A standard 19-black seed plus one black marker (2N,-2N), with the NUMERICAL input
N=10^60, gives an exact arithmetic control: the initially supplied marker is
consumed at 104N and skipped by the birth filter. The first eligible lifetime is
at (2N-3,-2N+1), born at 104N-102, consumed at 104N+46, age 148. The complete
post-state uses 379 segment terms and accounts for 104N+47 actual updates.
This is a finite huge-integer test of the exact formula, not an asserted new
all-N construction theorem. Smaller numerical N=10 and 100 were also compared
with literal complete-field simulation.

Finally, restart the birth filter after EVERY returned event on the known blank
orbit, with D=128 and K empty. It completes 31 positive renewal rounds and then
returns a periodic negative answer from checkpoint 9990. Thus even successive
new lifetimes are compatible with eventual highway entry. This finite control
is not the proof of Theorem 1; it shows why 'new feedback occurred again' is
not a certificate of nonperiodicity. The program does not extrapolate 31 to other
inputs. Representation simplification between these small-input control rounds
materializes and re-XORs the exact complete field, deleting no physical cells.

## 7. Remaining HC obligation

What is now computable is the first genuine renewed remote feedback, not only
the next read of old initial inventory. On a non-ETC orbit every adaptively
restarted query is positive, with verified provenance and a per-round deadline.
No decreasing quantity across those restarts has been proved. In particular
M=|B_s| in (5) is remeasured, not fixed once for the whole infinite run.

The new quantitative consequence also does not furnish a contradiction with
linear resource growth or finite initial data. It is compatible with ever-new
cells and ever-new black lifetimes. A global upper bound on productive renewal
rounds, or an actual nonperiodic finite seed with an infinite certificate, is
still missing. This note does not replace that task with a strip promise or a
periodic-wake classification, and does not claim HC, HIGHWAY or all observer
HALT problems decidable.

## 8. Reproduction and provenance

Run `python reproduce.py`. It copies the package into a temporary directory,
checks hashes, rebuilds the reports, and compares all deterministic quantities.
No earlier repository test suite or proof is modified or represented as rerun.
Python 3.10+ standard library is enough; no external optimizer or numerical solver.

Dependencies at the pinned source commit:
- proof/results/stale-memory.md: suffix prediction and finite-event/ETC theorem;
- proof/results/remote-stale-feedback.md: endpoint tube, fixed-region bursts,
  uniform exterior quadratic deadline, and the prior qualitative newborn result;
- proof/results/clock.md: the conservative square exit bound used in that proof.

The main input is the classical finite-support dynamics, not an altered background
or an external controller. Software provenance and the exact source read are in
PROVENANCE.json. Mathematical scope and confidence remain as stated above.
