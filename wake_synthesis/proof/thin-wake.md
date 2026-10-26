# Rigidity of thin width-ten wakes in the classical Langton ant

**15 October 2026. Research baseline: `bf42eebf88560ef767c77cbf582cd08658b0ce6b`.**

Status: computer-assisted theorem, with all 76 normalized cases completed and
all 83 native runs reproduced in a disposable package. The full replay passed;
its report is `evidence/full_replay.json`. The finite-support criterion, the
short-factor upper certificate, ordered-event representation, and local rank
pruning are inherited with their original evidence boundary. The new work
removes the prescribed standard wake, including its transverse empty layer and
all longitudinal residue choices. No HC proof, negative seed, formal-kernel
verification, peer review, or priority certification is asserted.

## 1. Main statement: no prescribed standard wake

A state is `(B,p,h)`, where B is a complete finite subset of Z^2 and
h=N,E,S,W=0,1,2,3. White turns right (R), black left (L); toggle the current
cell and move. The plane has no walls. A time denotes a pre-update state.

Let a word of P turns repeat forever from a finite black seed, with heading
restored and full displacement d=(2,-2). It need not be a least period.
Its phase positions are q_i. A FULL class modulo Z*d has label

    (t,r)=(x+y,x mod 2).

Let o_t be the number of such classes at level t containing an odd number of
phase visits. These classes are the permanently emitted black strands. They
are not the moving head's entire field, the signed toggles of one arbitrary
period boundary, or individual black cells in an ordinary horizontal row.

The transverse width is W=max_i(q_ix+q_iy)-min_i(q_ix+q_iy).
Call this wake *interior-thin* if o_t<=1 for every strictly interior level.
This is a condition on odd-class occupancy, NOT a bound on visits or cut flow.

**Theorem (thin-wake rigidity).** Suppose

    d=(2,-2),    growth #R-#L=12,    W=10,
    and the wake is interior-thin.

Then P=104 and the turn word is the standard Langton-ant highway, up to the
stated cyclic phase normalization. In particular the complete odd-class wake
is forced; it is not a premise. Corresponding lattice translations and quarter
turns give the equivalent geometric statement.

**Corollary.** Any nonstandard finite-support periodic highway having the same
full drift, growth and width must have BOTH residue classes odd on at least
one interior level. An arbitrary eventual-periodic suffix is covered because
its complete field at its first time is still finite.

The theorem does not assert eventual periodicity, these numerical invariants,
or interior thinness for every finite seed. It does not settle HC. Repeating
standard P104 twice changes drift to (4,-4) and growth to 24, so is not a new
period in this fixed-drift problem. Arbitrary genuinely unread debris is allowed;
uniqueness is of the read word, not of complete colourings.

## 2. Finite support, chronology, and extreme levels

For each class choose b and write q_i=b+a_i*d. Far enough along that class, all
phase visits to b+n*d are present and the cell is initially white. Their times
are (n-a_i)P+i. Thus their stabilized order is by decreasing a_i, then increasing
phase i, and their turns must be R,L,R,L,... . Conversely this condition gives
a finite boundary seed: for min a_i<=n<max a_i, initially blacken b+n*d iff the
number of omitted phases with a_i>n is odd. Induction verifies the entire infinite
word. This known criterion is attributed to A. Jillhewar (2026), Theorem 3.1 and
Remark 3.2, not claimed as a new result.

Consequently the signed turn excess in each class is its odd indicator, and

    growth=sum_t o_t.

At a transverse extreme, one neighbor on each coordinate axis is absent from
the trace. The checkerboard/heading-axis invariant fixes an arrival axis at a
class; therefore the arrival direction and departure direction are fixed there.
Every turn in an extreme class is identical. Stabilized alternation starting
with R implies that an extreme class has exactly one visit, an R. The top event
arrives E and the bottom event W. Normalize the top to t=0 and its position to
the origin. Then sigma=-1, the bottom is -10, and both extremes have one or two
odd classes. Since d=(2,-2), there are exactly two available residues per level.

This is derived from the candidate's periodicity and finite support. It is not
an assumption of confinement imposed on arbitrary original initial states.

## 3. Analytical reduction to five density profiles

Let m_t be the number of phase visits at level t. Let u_t count passages that
enter from t-1 and leave at t+1. In a closed transverse walk the reverse straight
passages have the same count. At even t, R reverses transverse direction and
L is straight; at odd t the roles reverse. Therefore

    m_t=(-1)^t o_t+4u_t.                                  (1)

The movement axis alternates. There are P/2 horizontal moves. Their net
displacement is 2, so P/2 is even and P=0 modulo 4. Summing (1) yields

    sum_t (-1)^t o_t=0 modulo 4.                          (2)

The two rails together contain at most four odd classes, and the nine interior
levels contain at most nine. Growth twelve forces the rail total to be 3 or 4.
If it were 3, all nine interior levels would be occupied; their signed sum is
4-5=-1, so the total signed sum would be 2, contradicting (2).

Hence both rails contain both classes. Exactly eight of the nine interior
levels contain one odd class. If h is the empty level, the signed sum is

    4+(4-5)-(-1)^h = 3-(-1)^h.

It is divisible by four exactly when h is odd. Thus

    h in {-9,-7,-5,-3,-1}.                                (3)

There is NO remaining geometric guess in this finite list. For any such h,
list the eight occupied interior levels in increasing order and encode their
residue choices by an eight-bit mask. There are 256 masks per h.

A translation by (1,-1) swaps every residue. Both top classes are singletons,
so choosing the other top event as phase zero realizes that swap without
changing the turn dynamics. Choose the origin so the highest occupied interior
strand has residue 1. This is exactly mask>=128 and gives one representative
of each complementary pair. No reflection or colour complementation is used.

## 4. Uniform, all-period upper bounds

The retained short-factor certificate is independent of o. It gives, for every
closed walk in its necessary graph on -10<=t<=0,

    y_v-y_w+alpha_t epsilon <= -1,
    alpha_t=-2(-1)^t(t+5)^2,                              (4)

where epsilon=+1 for R and -1 for L. The graph records heading and a suffix
avoiding 588 explicitly checked impossible factors of length at most 21.
Every physical periodic trace lifts after history warmup to a closed walk;
it need not be a simple cycle. The graph intentionally forgets the residue,
but the exact chronology search below retains it.

The inherited integer-only recipe regenerates 54,718 vertices and 90,158 edges,
constructs y in [0,180] by bounded integer relaxation, and checks (4) on every
edge. No optimizer or floating-point tolerance is a premise. Its canonical
source is `inputs/upper_bound.py`; its original proof and source are preserved.

Summing (4) over a true period cancels vertex terms. Finite support supplies
the signed class excesses, so

    P <= -sum_t alpha_t o_t.                              (5)

For (3), this gives respectively

    h:       -9   -7   -5   -3   -1
    upper:  192  168  160  168  192.                      (6)

Thus all possible periods are covered before any chronology search starts.
These are upper bounds, not claimed exact maximum periods.

## 5. Exact residue and count reductions

At a class adjacent to the already processed region, let I and J count arrivals
and departures on that side. Index all class events by stable rank k, and let
m be its length, o its odd indicator. If a of the even ranks arrive on the
processed side, the literal port table gives

    m=2(I+J-2a)+o          (even t),
    m=2(J-I+2a)-o          (odd t),                        (7)

subject exactly to

    m>=0, 0<=a<=ceil(m/2), 0<=I-a<=floor(m/2).

Conversely these inequalities allow a binary arrival string with exactly the
required even- and odd-rank arrivals. This equivalence is of LOCAL COUNTING
conditions; it is not a physical realization theorem.

A boundary frontier is (out_0,out_1,in_0,in_1). At a new row t use

    I=(out_0,out_1), J=(in_1,in_0)  for odd t;
    I=(out_1,out_0), J=(in_0,in_1)  for even t.

For selected m_0,m_1, the new frontier is

    (m_0-J_0,m_1-J_1,m_0-I_0,m_1-I_1).                   (8)

Reduce (7)-(8) modulo four. The term involving a vanishes, so the next residue
frontier is uniquely determined by the current residue frontier and o. Start
at (1,1,1,1) at one saturated rail; the frontier at the other rail must be the
same. A mismatch rejects the mask at EVERY period, not just below (6).

For the remaining masks, the class visit counts modulo four also determine
counts in the four update-phase groups:

    i mod 4 = 2r+(t mod 2).                               (9)

The identity follows by following alternating vertical and horizontal moves
from the normalized top event. Each group has P/4 members. If their residues
are not all equal, reject; otherwise P is fixed modulo sixteen.

Running these short integer recurrences for all masks in (3) gives

    empty layer:           -9  -7  -5  -3  -1
    normalized survivors:  12  20  12  20  12.             (10)

Both construction orientations and all complementary masks are checked. The
full data are regenerated, not accepted as an unverified lookup table.

The full nonnegative version of (7)-(8) gives completion tables. At a repeated
four-count frontier retain the minimum cost; all further count possibilities
depend only on that frontier. The resulting cost is a lower bound for any real
completion. Each table is freshly generated with the correct mask and cap.
Missing entries in an arbitrary supplied table are never trusted as exclusions.

## 6. Complete chronology, not mean flow

For each full class (t,r), list the m events in stabilized order. Their turns
are fixed by rank parity. Enumerate their incoming sides; literal turning fixes
the outgoing sides. Directed lattice edges have a fixed direction of use in
the checker sector, so ordered source occurrences match ordered target
occurrences first-to-first. There is no arbitrary matching permutation to omit.

Each matching edge has integer voltage delta satisfying

    b_source+outgoing_unit=b_target+delta*(2,-2),
    b_(t,r)=(r,t-r).

A completed event graph is accepted exactly when it is one directed cycle with
total voltage +1, and its lifted times j-P*v increase strictly with rank in
each class. This reconstructs the real word, drift and headings. The criterion
of Section 2 constructs a complete finite seed, and an independent epoch/parity
checker verifies its entire infinite future. Every real normalized word
produces one such enumerated graph.

The inherited pruning obligations remain unchanged:

* A closed component before the final rail cannot later join the mandatory
  remaining events, so it is rejected.
* Exact completion costs and four-phase count capacities give necessary lower
  bounds, not assumed finite memory.
* On an open chain, tau_u=z_chain+p_u-P*v_u. Consecutive class ranks require a
  gap at least four. A simple constraint cycle on q chains has weight C+K*P,
  with C>=5q-n and integer K, where n events are already constructed. If K>=1
  it is positive for every P>=n; if K=0 its sign is constant; if K<0 it decreases
  with P. A positive cycle at the search cap therefore rejects every admissible
  P below that cap.
* Within a fixed contiguous chain, successive reads of the same physical cell
  must have consecutive stable ranks, not merely opposite turn bits. Every
  update between them is already fixed; an omitted rank cannot be inserted.

These arguments are independent of the selected thin-wake mask. Only the input
odd indicators and regenerated cost tables change. The inherited source is
hash-pinned; the generalization and its patch are preserved with the supplement.

### Deterministic partition of a difficult branch

A long search may be split only by a coverage-preserving partition. In the
last case, h=-1 and mask 187, the checked phase residue is P=8 modulo 16.
Its analytic bound 192 therefore permits the search cap 184. We enumerate,
in fixed order, all partial graphs at the completed
layer boundary just before row -5. Number these from zero. Shard j of k follows
exactly ordinals congruent to j modulo k. Every full candidate crosses this
boundary exactly once. Upstream recursion and rollback are unchanged, so all
shards enumerate the same cut list. The disjoint union therefore covers the
original tree. All shards must return COMPLETE; matching counts/digests are
additional controls, not substitutes for this argument. An interrupted shard
never supplies a negative conclusion.

## 7. Finished finite classification and the positive witness

The exact case inventory, source hashes, selected traversal directions, caps,
completed native outputs and shard records are in `evidence/cases.json`.
All 76 canonical modular survivors are covered, using 83 completed native
runs (the last case is split into eight). The accumulated prefix visits are
391,065,872, including repeated upstream work in shards; these are not distinct
words or literal ant steps. Outcomes are:

    h=-9: no realization;
    h=-7: no realization;
    h=-5: no realization;
    h=-3: exactly mask 163, and exactly the standard word;
    h=-1: no realization.

The simultaneous complement is mask 92 in the h=-3 frame; it is another
choice of origin for the same geometric periodic trace, not another highway.
The normalized accepted word is

    RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR

Its full odd-class set is forced to be

    {(-10,0),(-10,1),(-9,1),(-8,1),(-7,0),(-6,0),
     (-5,0),(-4,1),(-2,0),(-1,1),(0,0),(0,1)}.

An explicit complete finite seed, head at (0,0) facing E, is

    {(-7,0),(-7,1),(-6,-3),(-6,-2),(-6,-1),(-6,2),
     (-5,-2),(-5,0),(-5,1),(-5,2),(-4,-2),(-4,1),
     (-3,-3),(-3,1),(-2,-3),(-2,-1),(-2,1),(-1,-2),(-1,0)}.

No claim of minimum seed size is made. Its infinite read word is independently
verified from all initial-black hits and all prior-write thresholds, including
the final infinite interval. A distant added black blocker is rejected. The
accepted word has exactly P=104, W=10, growth twelve and the stated profile.
Combining Sections 2-6 with the completed finite inventory proves the theorem.

## 8. Evidence, comparison, and HC boundary

The main statement is stronger than uniqueness under a prescribed complete
standard wake. It removes both the empty-layer prescription and all longitudinal
residue prescriptions, using only thinness and three numerical trace invariants.
It does NOT remove the drift, growth, width or eventual-periodicity hypotheses.
A general HC counterexample is not constrained to satisfy those hypotheses.

The period bound, realization criterion and pruning lemmas retain their prior
attribution. In particular, earlier literature's 'thin crossing profiles' for
primitive-diagonal growth four are different from the interior odd-class
thinness defined here; no discovery claim is based on that ambiguity.

Evidence is conventional mathematical coverage plus integer certificate checks
and native exhaustive enumeration. No new Lean proof or outside peer review is
claimed. Reproduction explicitly separates record checking from full enumeration;
source hashes identify the programs but do not by themselves prove exhaustion.
Resource-limited and failed exploratory attempts are not negative evidence.
