# Finite waiting for stale-memory reads: a global local-target theorem

**Date:** 2026-10-11.  
**Model:** Classical square-grid, two-colour Langton ant; white turns right,
black turns left, flip and then move. Every state here includes the COMPLETE
finite black set and a pre-update ant pose.  
**Evidence:** self-contained unformalized analytic proofs; exact implementation
checks. No global nonuniversality, HC, arbitrary local-target decision theorem,
new negative seed, formal proof, third-party review or priority claim.

This continues the memory-classification work, but adds a quantitative theorem:
one specific FAMILY OF LOCAL TARGET LANGUAGES is decidable on ALL finite planar
states, not only states with a promised bounded delay or strip geometry. It
also identifies exactly why this does not finish the requested global proof.

## 1. Definitions and an intrinsic finite-local target

Write X=(B,p,h), headings N,E,S,W. Let F be the literal update. Define

    R(X)=max({||q-p||_infinity:q in B} union {0}).

For integer D>=1, define the stale-black predicate

    S_D(X) iff p in B and position(F^(-k) X) != p for every 1<=k<=D.       (1)

The inverse is literal and unique: q=p-dir(h), flip q, and undo a right turn
when q is black in the supplied post-state, otherwise undo a left turn.
Only cells at distance at most D from p are read during D inverse steps.
Consequently (1) is a translation-invariant FINITE LOCAL PREDICATE on the
present colouring and heading. It does not use an infinite historical oracle.

Using the intrinsic backward orbit makes (1) defined even at input time zero.
At forward times t>=D, it says exactly: the current read is black and the same
cell has not been read in the previous D updates. A very old WHITE reread is
not an S_D event. A never-yet-read initial black cell can be an S_D event too.
This convention is distinguished from an age defined only after time zero.

Let tau_D(X)=min{t>=0:S_D(F^t X)}, when it exists. This target comprises infinitely
many full states; the result below is not just specified-full-state reachability.

## 2. Prediction identity: no event means one unique next turn

For a D-letter R/L word w, execute its geometric turns from a fixed pose.
Compare the final position to the preceding D pre-update positions. If the last
matching position has index j, set f_D(w)=opposite(w_j); if there is no match,
set f_D(w)=R. This depends only on w: translation and quarter turns preserve
position equality.

Recover the actual previous D turns of X using F^(-1), and call them w(X).
The following equality is exact for EVERY finite state:

    actual_turn(X) != f_D(w(X))  iff  S_D(X).                           (2)

Moreover the only possible mismatch is predicted R versus actual L.

Proof: a recent previous read fixes the current colour to its flipped value.
With no recent previous read, f_D predicts R. This is wrong precisely when the
current cell is black. Old white cells and virgin white cells both give R.
The backward suffix is part of the actual orbit, so inconsistent fake histories
cannot enter this argument.

While S_D is absent, suffixes evolve autonomously as

    w -> suffix_(D-1)(w) f_D(w).

This is a deterministic map on Q=2^D states. Its generated infinite turn word
has a transient shorter than Q and period at most Q. This alone does NOT prove
that the physical ant follows the word forever: distant black cells may cause
a first mismatch. The next section bounds WHEN any such mismatch can occur.

## 3. First mismatch against an ultimately periodic motion plan

Consider a complete finite state Y of radius r and a proposed periodic turn
word u of length P, with matching start/end heading and displacement d!=0.
Let q_i, 0<=i<P, be its relative pre-update positions, q_0=0. Its proposed future
reads are

    q_i + k*d,  k>=0.

Earlier periodic reads of the same cell correspond exactly to

    q_j-q_i = l*d, l>=0, and (l>0 or j<i), with k>=l.                     (3)

Each such l is at most P: the finite footprint's pairwise infinity-distance is
at most P, and ||d||_infinity>=1. Earlier-read parity can change only at these
finitely many thresholds l.

The initial colour contribution is 1[q_i+k*d in B_Y]. If this is nonzero then

    k*||d||_infinity <= r+||q_i||_infinity <= r+P,

so k<=r+P. It is a one-epoch contribution, turning on at k and off at k+1.
Thus the colour required by literal dynamics at each phase i is

    1[q_i+k*d in B_Y] XOR parity(number of eligible pairs in (3)).       (4)

All changes occur by epoch r+P+1. Testing every breakpoint, including the last
infinite constant interval, is necessary and sufficient for infinite execution.
If there is a mismatch, its FIRST time is strictly below

    P*(r+P+2).                                                         (5)

This statement concerns the first mismatch, not a hypothetical trajectory after
an earlier mismatch. Induction in time ensures that the proposed path agrees
with the real path up to that first point.

If u does not restore heading, repeat it two or four times to restore heading.
The resulting displacement is zero, since the quarter-rotated displacement
vectors sum to zero. If heading is restored but d=0 already, use u itself.
In either case let v be the closed-pose block, of length at most 4P. If two
consecutive copies of v were both physically valid, all flips would occur twice
and the complete state would recur. Such an orbit would remain in finitely many
cells forever, impossible for the classical ant. Hence a first mismatch occurs
before 2|v|<=8P updates.

For clarity, the elementary no-bounded-orbit argument used here is as follows.
If the set I of infinitely read cells were nonempty and finite, choose a cell
maximizing x+y. After the north and east neighbours have ceased being read,
the checkerboard/heading-axis invariant fixes the only possible entering and
leaving directions at that cell. This requires the same read colour on every
sufficiently late visit, contradicting colour alternation. No periodicity,
finite-support HC or new computational evidence is assumed in this argument.

## 4. Uniform waiting theorem

**Theorem 1.** For every finite state X and D>=1, with Q=2^D, put

    H_D(X)=Q*(R(X)+2Q+10).                                             (6)

Exactly one of the following occurs:

- tau_D(X) exists and 0<=tau_D(X)<H_D(X);
- S_D never occurs at any nonnegative time; the ant has a nonzero translating
  periodic trace with period <=Q, beginning at a time <=Q.

Thus observing no S_D event at times 0,...,H_D(X)-1 proves that none ever occurs.

Proof: construct the autonomous suffix trajectory. If a physical mismatch
occurs before the first repeated suffix, (2) gives the event within Q updates.
Otherwise at a repetition time j<=Q, the physical trajectory has followed the
plan and a periodic suffix cycle of length P<=Q begins from its current phase.
The current complete radius is at most R(X)+j: initial black cells move relative
to the ant by at most j; any newly black cell is also within j steps of it.

For nonzero translational drift, (5) bounds a first future mismatch by

    j+P*(R(X)+j+P+2) <= Q*(R(X)+2Q+3).

For a closed geometric plan, the other bound is j+8P<=9Q.
Both are strictly covered by (6). If no mismatch exists, the planned periodic
trace is the exact infinite future. A closed or rotating periodic plan was
excluded above, so its drift is nonzero. By (2), no mismatch also means no S_D
event. This proves both the waiting bound and the dichotomy.

No width, cone, retreat, mass, visit-count, future-active set, or hypothesized
computation-time bound is supplied as an extra premise. The ONLY spatial size
in (6) is the computable radius of the actual finite input.

### What is the corresponding decision problem?

The family

    L_D={X:there exists t>=0 with S_D(F^t X)}                            (7)

is recursive, uniformly in D. This is a genuine all-input decision theorem for
a family of local predicates, not a HIGHWAY algorithm. Even an input-dependent
computable D(x) cannot make a reduction of an undecidable source language to (7).
An arbitrary HALT pattern is NOT automatically of this form.

A simple decision algorithm simulates the explicit finite bound (6). The
implementation uses the stronger symbolic version: only the first suffix
cycle is produced, then all-future ray/flip arithmetic finds the first event,
or verifies a permanent event-free trace. No simulation to a late arithmetic
collision is necessary.

### Bit complexity of the implemented first-event decision

With an explicit sparse list of m black coordinates of bit length at most b,
the symbolic first-event algorithm uses time 2^{O(D)} times a polynomial in the
input length. In particular, for every fixed D, language (7) is decidable in
polynomial time in the sparse BINARY-coordinate input size.

Indeed inverse-history recovery uses D steps; the suffix search uses at most
Q=2^D states; its explicit black field has at most m+Q+D cells. The candidate
word has length at most Q, and the ray verifier checks O(Q*m+Q^2) phase/cell and
phase/phase relations. All coordinate, epoch and offset arithmetic has bit length
polynomial in b+D. Closed-pose control replay costs at most 8Q updates. Ordinary
polynomial-time set/dictionary implementations suffice. This is a theoretical
bit-complexity upper bound; it is not a timing benchmark or a claim of practical
feasibility for large D. The counting cutoffs (8)--(9) below are separate and
are not claimed to share this first-event complexity bound.

For fixed D the upper bound is linear in R. This order cannot in general be
replaced by a radius-independent constant: take a certified event-free P104
state with D=128 and insert one remote black cell at a virgin frontier site
k highway periods ahead. Until its first read the original periodic trajectory
is unchanged. The first event is at 104k+O(1), while R=2k+O(1). The phase-ray
calculation gives the constants exactly. This is a family of finite perturbed
seeds, not a finite-support counterexample to HC.

## 5. Counting events and bounding first consumption of newly created old memory

Let R=R(X), Q=2^D and C=R+2Q+10. If a trajectory has an nth S_D event, its time
is strictly below the computable deadline

    T_(D,n)(X)=C*((Q+1)^n-1).                                         (8)

Proof: let s_0=0 and let s_(j+1) be one plus the next event time at or after s_j.
Whenever the next event exists, Theorem 1 and R(F^s X)<=R+s yield

    s_(j+1) <= (Q+1)*s_j + Q*C.

Induction gives s_n<=C*((Q+1)^n-1). The nth event is at s_n-1, proving (8).
This is an IF-IT-EXISTS bound valid on every input, not an assertion that the
nth event must exist. In particular the threshold question 'at least n future
S_D events?' is also decidable by a finite simulation cutoff.

Now count black LIFETIMES, not old white cells. A post-input black lifetime
begins at a right-turn write at time b>=0 and ends, if ever, at the next read
e>b of that cell, a left turn. It is D-long if e-b>D. Such a consumption is an
S_D event. Before the first such consumption, every S_D event must consume a
black cell already present in B_0 and not previously read after time zero.
There are at most m=|B_0| such initial lifetimes. Therefore:

**Corollary 2.** If any post-input-created D-long black lifetime is ever
consumed, the FIRST such consumption occurs before

    (R+2Q+10)*((Q+1)^(m+1)-1).                                       (9)

This supplies an explicit primitive-recursive cutoff for a physically
meaningful fixed-D violation test. It does not prove that there is a suitable D
on every input. Cells which remain black forever without being read again do
not constitute such a consumption; stationary debris is not counted as active
memory merely because it ages.

## 6. Consequence for a hypothetical nonperiodic finite-support orbit

If for some D only finitely many S_D events occurred, apply Theorem 1 after the
last one. The orbit would eventually translate periodically. Thus every
non-eventually-translating orbit must have infinitely many S_D events, for EVERY
D. Formula (8) further implies that by update t the event count is at least

    floor(log_(Q+1)(1+t/C)),                                         (10)

where this is interpreted for reads at offsets strictly below t. Equivalently,
use the entirely integer assertion: at least n events occur before T_(D,n).
At most m of these events consume initial black lifetimes. All the rest must
consume post-input-created black cells which have survived longer than D.

This makes the required historical feedback more precise. A very late white
return does not disrupt finite-recency prediction. On any nonperiodic run,
newly manufactured long-lived BLACK memory must keep being read and erased.
For each fixed D these reads cannot have arbitrarily long gaps relative to the
current radius, and cannot become sparser than the logarithmic bound (10).

Neither (10) nor the fact that each event consumes a black lifetime rules out
an infinite run. New right turns create new black lifetimes. Indeed even the
all-white initial state has, for D=128, a black creation at (−3,−2) at time 21
and its consumption at time 197, with lifetime 176. Therefore the number of
initial black cells is NOT a budget for all later stale-memory events. This
specific false extrapolation is refuted by a literal finite control.

## 7. Exact status of the complete-proof attempt

The proved results classify a local EVENT, not an arbitrary local HALT signal,
and do not supply a finite total number of such events on each orbit.
After a detected event the finite-recency prediction can restart from a new
suffix and a changed full field. Infinite restarts are not excluded.

For the repository's effective compiler / finite-local finite-state halt-readout
contract, an eventually translating trace is effectively analyzable by finite
ray exceptions and periodic observer states. Consequently a universal compiler,
if one exists, must have at least one divergent input outside that class.
Theorem 1 and (10) give necessary feedback conditions on that input, not a
contradiction to its existence.

A sufficient completion theorem would prove

    for every finite X, there is D>=1 with only finitely many S_D events. (11)

This is equivalent to the all-eventual-translator statement, not a newly
established lemma or a weakened solved version of the target. It is STRONGER
than necessary for nonuniversality: a different global decidability or compiler
obstruction argument need not establish (11).

What has genuinely been removed here is an unknown waiting-time premise for
an individual stale-memory event, and the unknown last-initial-black-query time
in the fixed-D test (9). What remains is existence of a controlling D or another
all-compiler restriction. Infinitely many positive but finite event segments,
linear creation of new cells, or the event-density lower bound do not by
themselves contradict universal computation.

In particular these implications are NOT proved:

    every L_D recursive => all local target reachability recursive;
    a first stale event => nonperiodicity or no P104;
    each event consumes a token => finite total events;
    fixed-D cutoff exists => some D works for every seed;
    bounded-growth event deadlines => nonuniversality;
    eventual translator => standard P104.

## 8. Implementation and verification boundary

Run `python check.py`, without `-O`, using Python 3.10+ and the standard library.
`first_stale_read` normally executes at most Q suffix steps plus, in the closed
geometry case, at most 8Q finite control steps. A symbolic event certificate may
refer to a much later time. Optional `max_suffix_states` returns INCONCLUSIVE on
resource exhaustion, never a false negative. `is_stale` uses exact D-step inverse
history. Formula (8) is provided by `event_count_deadline`.

`baseline/memory_delay.py` is copied without modification from the supplied
memory-classification package. Its integer-ray periodic verifier is reused.
The fresh checks use a separately written complex-coordinate forward/inverse
simulator for finite controls; this is implementation cross-checking, not an
independent mathematical review.

The completed suite checks 2,048 inverse round trips; 8,192 local-predicate
identities; 8,192 first-event classifications on all 3x3 binary seeds and four
headings for D in {1,2,4,8}; 371 late-white controls; 104 P104 phases and three
additional rotations; two remote-blocker controls, including an event at offset
104,000,000 found after only 104 explicit updates; an irrelevant archive control;
eight mutated periodic words; invalid-input and caller-cap handling.

An earlier, larger rotation replay exceeded a tool time limit and is not counted
as completed. The smaller full-phase suite above was subsequently run to
completion. These finite tests do not replace the all-input arguments in
Sections 2--7. No old Lean or repository-wide regression was performed. No remote
repository files were changed during this turn.

## Sources and scope

- Project baseline: `proof/finite-support-nonuniversality-status.md` fixes the
  compiler/readout contract; `proof/decidability-turn-word-equivalence.md` gives
  the literal per-cell alternating-turn representation.
- Attached `langtons-ant-memory-classification-2026-10-11.zip` supplies the
  previous fixed-delay analysis and the reused arithmetic periodic verifier.
- A. Gajardo, V. H. Lutfalla, M. Rao, *Ants on the highway* (2024), arXiv
  2409.10124v1, Section 2, reviews reversibility, checkerboard-axis coupling,
  unboundedness, and the distinction from periodic-background universality.
  Its colour/turn convention is reflected relative to this package. None of its
  generalized-rule examples is imported as a finite-support classical result.
- No inference of global nonuniversality is taken from a literature claim that
  the original problem is unresolved. The remaining gap is the explicit absent
  implication in Section 7.
