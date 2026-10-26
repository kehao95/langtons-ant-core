# Finite-horizon ballistic rigidity and black-supply bounds

**20 October 2026. Mathematical base inspected:**
`kehao95/langtons-ant@8c414b8963260f5d4d394dc5b4c53065028b4c6e`.

**Status.** Complete written analytic argument with exact finite certificates and
an executable first-event algorithm. Unformalized; no external mathematical
review or priority guarantee. The finite-path fold cover and common-normal lemma
are inherited project results, not new claims. The supply/cofactor estimate,
finite-horizon core theorem, return inequality and one-jump algorithm below are
the new conclusions. None is a proof or disproof of HC. Persistence on a remote
branch must be reported separately; a local delivery is not a remote commit.

## 1. Statements and precise finite-horizon scope

Use the literal classical rule on Z^2: read white/R or black/L, turn, toggle, then
move one edge. A state at t is before update t. Every physical initial field here
is finite and COMPLETE. Quarter turns and translations are allowed; the rule is
not reflected. W is the same standard 104-letter word as in
[ten-factor attraction](ten.md), pinned in the new `model.py`.
Let L10 be its 84 cyclic length-ten factors. A finite word is *ten-legal* if every
length-ten factor wholly inside it belongs to L10. No condition is imposed on a
word shorter than ten. No promise about an infinite legal extension is made.

For a feasible finite word w, let c(w) be its number of DISTINCT physical cells
whose FIRST requested read is L, from the origin facing north. By the established
first-read and alternating-read criterion, c(w) is precisely its minimum finite
initial black cardinality. For a real segment starting with m complete black
cells, c(w)<=m. This is not the current mass at a later checkpoint, nor a count of
all L letters or of all dynamically created black lifetimes.

Set

    F=1322,       K(m)=114m+154693.

**Theorem 1 (one ballistic core).** Every physically feasible finite ten-legal
word admits a decomposition

    w = u (W_r)^k v,      k>=0,
    |u|+|v| <= K(c(w)),                                      (1.1)

where W_r is a cyclic phase of W. The middle block is ONE contiguous part of the
actual word; no rearrangement of separate standard fragments is allowed. k=0 is
permitted. Consequently the Hamming distance of w from a suitably phase-aligned
104-periodic word is at most K(c(w)). This is a statement about the whole finite
trace, not eventual standardness inferred from finite observation.

**Theorem 2 (supply-displacement inequality).** Let Delta be the total head
displacement of the same word. Then

    |w| <= 52 ||Delta||_infinity + 114 c(w) + 223437.          (1.2)

The displacement coefficient 52 cannot be replaced by a smaller number in ANY
uniform bound of this form with finite fixed coefficients on c(w) and the additive
term. Neither 114 nor the additive constants are claimed optimal.

In particular a closed ten-legal return of length L, from a complete m-black
source, satisfies L<=114m+223437, independently of all source coordinates. Thus
moving a fixed number of initial black cells arbitrarily far away cannot make a
zero-defect closed return arbitrarily long. This does not bound a return with an
unrestricted number of defects.

**Corollary 3 (silent lifetime cost).** Suppose a cell is written white-to-black
at b and next read at e>b. If there is no intrinsic J10 event at a time b<t<e,
then

    e-b <= 114 |B_b| + 223437.                              (1.3)

The mass is the COMPLETE field at the birth checkpoint, not the original input
mass at some earlier time. A J10 at birth or at consumption is allowed. The same
conclusion holds under the weaker condition that the finite word on [b,e) is
ten-legal. Initial inverse-history windows must not be confused with windows
wholly contained in that word.

**Theorem 4 (exact next J10 with one standard jump).** For a complete explicit
m-point source, the exact first intrinsic J10 and full post-state, or permanent
absence of future J10, can be computed using at most ONE standard-periodic
first-mismatch query and K(m)+1 ordinary forward updates. It returns the complete
field as the XOR of the original points, O(m+1) finite point changes, and at most
104 finite translating segments. Time and all coordinates may be arbitrarily
large binary integers. Its total bit complexity is polynomial in the sparse
input size. The runtime uses no T/A accelerators, overlap graph or Presburger
solver. A caller-imposed smaller resource cap returns UNKNOWN.

The inherited five-plan algorithm has a different advantage: its bound is in
compressed segment description size even when the represented black cardinality
is enormous. Theorem 4 is not a claim that O(m) work improves that compressed-input
bound. Its novelty is the one-plan normal form and a smaller trusted runtime.

## 2. Inherited finite-path cover, with the extra order explicitly checked

The finite-window graph and the all-parameter three-fold obstruction in
[exact J10 macros](ten-event-macros.md) imply the following cover for EVERY finite
physical ten-legal word. Retain its first 149 letters. Subsequent history states
lift to a 7595-vertex, 7763-edge graph whose only recurrent components are simple
cycles of lengths

    24, 104, 28, 28, 28.

These are phases of T, W and A respectively. Along a path the number of cyclic
stages is at most five, the number of noncyclic steps at most 956, and the sum of
visited cycle lengths at most 212. Splitting a cyclic visit into whole periods,
a proper remainder, and an optional exiting edge gives at most

    149+956+212+5 = F                                      (2.1)

literal letters outside the whole-period powers. This conservative accounting
also covers words ending partway through a component. Shorter words are entirely
literal. It is a bound on description size, NOT on period repetition counts.

The relevant ADDITIONAL finite fact is the order of cyclic components. In the
base graph the 24-component can reach the 104- and 366-components; the
104-component can reach the 366-component; the 366-component reaches neither.
The folded component unfolds into the three A cycles. Hence every covered word
has at most one T power, then at most one W power, then at most three A powers,
with arbitrary fixed pieces between them. Some powers are absent. In particular,
T never occurs after W, and no W component can reappear after departure.

These are fully checked finite facts. The new replay regenerates ALL 6605
feasible length-150 words twice, using Python last-read maps and an independent
C++ current-colour/vector implementation. Their entire sorted word set and all
151 level counts agree. The word and quotient hashes are checked against the
inherited certificate. SCC order, cycle words, and all rank-edge inequalities
are then checked on the complete graph, not a sampled portfolio.

The word-graph method overapproximates physical paths. Every actual path is
covered, but graph membership alone never certifies physical realizability.
The necessary all-parameter no-three-fold step is recalled in Appendix A.

The common-normal certificate from [silent-axis return](silent-axis-return.md)
also applies: for the cyclic components on any ONE oriented finite path there
is n in {(+1,0),(0,+1),(-1,0),(0,-1)} such that n dot d>=0 for every cycle drift d.
This small part of that result is regenerated here on the full four-heading
lift (30380 vertices and 31052 edges). The closed mask table has 88024 states and
never contains an empty mask. The older retreat potentials and constant 43 are
not needed, and are not represented as newly rerun.

## 3. Uniform mode supplies and the transverse overlap constant

Direct finite geometry of the phase words gives:

| Mode | Period | Mass change per full period | Required first-L rays | Read-strip levels |
|---|---:|---:|---:|---:|
| T | 24 | +4 | 2 | 4, axis-aligned |
| A | 28 | +4 | 5 | 4, axis-aligned |
| W | 104 | +12 | 0 | 11, diagonal |

All cyclic phases and all four starting headings have the indicated strip
widths. The drift of T is an axis vector of length 2, that of A one of length 4,
and W has coordinates (+/-2,+/-2). Width means the number of integer levels, not
the numerical difference between the two extremal levels.

Here is a finite all-repetition proof of the supply column. For a phase word u
with drift d, let q_i be its phase positions. Phase i of copy j is at q_i+j d.
An earlier same-cell occurrence at phase l is possible exactly when

    q_l-q_i=s d,   s>0 or (s=0 and l<i),   j>=s.

Consequently any L phase with NO such earlier candidate is a first-L read at
EVERY j>=0. These first reads occur at distinct physical cells. Enumeration of
the fixed phases gives two such phases for each phase of T and five for each
phase of A. Therefore a source executing T^k needs at least 2k black cells on
those first-read positions, and one executing A^k needs at least 5k. Other
first-L phases can add extra finite costs, so they cannot weaken the bound.
No infinite physical black field is an input to this argument.

A W power's entire read set is contained in an eleven-level diagonal strip.
An A power's entire read set is contained in a four-level axis strip. ANY
translated or quarter-turned pair of such strips intersects in at most

    11*4 = 44                                               (3.1)

integer cells: fixing an axis coordinate and the diagonal coordinate determines
at most one point. This is independent of the two power lengths, the placement,
and the age of an existing highway. In particular (3.1) applies to their NET
XOR write sets, which are subsets of their read sets.

The geometric bounded overlap, rather than the fact that input support is finite
by itself, is what prevents an arbitrarily long W block from providing an
arbitrarily large fuel supply to a later silent A block.

## 4. Full-history cofactor accounting; no physical deletion

Fix one covered real word from a complete initial field of cardinality m. Let
k_T, k_W be its whole T and W repetition counts and k_1,k_2,k_3 its ordered A
counts, padding absent A stages by zero. Write f for its actual literal-letter
count, f<=F, and put q=m+F.

Since only literal pieces precede the T power, its first-L supply implies

    2 k_T <= q.                                            (4.1)

Before or after W, define D to be the complete NET toggle set of its chosen
whole W power (D is empty if the power is absent). After that block, write the
ACTUAL complete field as

    B_actual = R symmetric_difference D.                    (4.2)

R is an algebraic cofactor, not a replacement physical state. It contains the
original complete field and all literal and axial writes; it is not assumed to
follow the ant rule on its own. Every distant cell of D remains present in the
real field exactly as (4.2) specifies.

For any finite toggle set Z, a pointwise bit calculation gives

    |R xor Z|-|R| <= |(R xor D) xor Z|-|R xor D| + 2|Z cap D|.
                                                                  (4.3)

Outside Z cap D the two cardinality changes agree; at each point of that
intersection they differ by at most two. This proves (4.3) without a locality,
future-invisibility, or conservation assumption.

For a complete A^k block the real mass change is 4k. Its toggle set meets D in
at most 44 cells by (3.1). Hence its cofactor mass can increase by at most

    4k+88.                                                  (4.4)

Its 5k distinct first-L positions must be black in the real source. At most 44
of them can be supplied by D rather than R. Allocating the ENTIRE literal budget
F from the start (each literal flip increases |R| by at most one), we obtain

    5 k_i <= q+4k_T+4 sum_(j<i) k_j+88(i-1)+44
           <= 3q+4 sum_(j<i) k_j+88(i-1)+44,  i=1,2,3.       (4.5)

This counts all writes made inside silent pieces, all surviving input debris,
and every possible intersection with the long standard block. It does not
charge a newly created lifetime as a new initially black cell.

## 5. Core bound and the sharp displacement coefficient

Let S_i=sum_(j<=i) k_j. Iterating the three rational-linear inequalities (4.5)
from S_0=0 gives

    S_1 <= (3/5)q+44/5,
    S_2 <= (42/25)q+1056/25,
    S_3 <= (453/125)q+15004/125.                             (5.1)

All non-W letters number exactly E=f+24k_T+28S_3. Equations (4.1) and (5.1) yield

    E <= (14184/125)m + 3867322/25
      <= 114m+154693 = K(m).                                (5.2)

The whole W power is contiguous, so (5.2) proves Theorem 1 for the actual source
mass. Apply it to the feasible word's minimal first-L source to get K(c(w)).
This use of a minimal source describes the resource of a finite word; the
executable algorithm always retains the actual complete input.

Choose the common coordinate normal n of Section 2. W's nonzero diagonal drift
has n dot d_W=2; the other whole-cycle contributions have nonnegative projection.
The literal pieces have total projected displacement at least -F. Therefore

    2k_W <= n dot Delta+F <= ||Delta||_infinity+F.            (5.3)

Combining |w|=104k_W+E with (5.2)-(5.3), and 52F=68744, gives (1.2).
If W is absent the same inequality follows from E=|w| without needing (5.3).

For optimality of 52, use a single verified finite standard seed and its words
W^k. Their lengths are 104k, displacements have infinity norm 2k, and first-black
cost stays bounded by that fixed seed mass. A coefficient a<52 would require
(104-2a)k to remain bounded as k tends to infinity. This is impossible. The
replay verifies a 17-black seed against EVERY future parity interval, not just
a long repeated finite prefix. The standard reference itself is inherited.

For Corollary 3 take the finite word on [b,e). Its endpoints are the same cell,
it is ten-legal under the stated hypothesis, and its complete source has |B_b|
black cells. Equation (1.2) with Delta=0 proves (1.3).

## 6. A one-jump exact first-defect algorithm

The initial nine-turn history is recovered by nine literal inverse steps on a
COPY of the full source. It is not fabricated as a standard past. Maintain the
last at most 149 actual turns and perform ordinary forward updates, checking
intrinsic J10 BEFORE each one.

1. Stop if the first J10 is found. Otherwise, after at least 149 actual forward
   updates, stop this first phase when the 149-letter history is a vertex of the
   W cycle. This is a membership test in a fixed 104-element table, not a graph
   construction. Until such a vertex, no whole W core is possible. Theorem 1
   therefore prevents the first phase from continuing indefinitely.
2. At this standard history propose its uniquely phase-aligned W^omega future.
   Use the exact COMPLETE-source ray-parity calculation to locate its first
   mismatch, or certify none. None proves permanent absence of J10 because the
   history seam is already standard. A distant input cell is included in this
   test regardless of distance.
3. If a mismatch occurs, append every skipped write as 104 finite arithmetic
   segments plus at most 103 point changes; advance to its true position/time.
   Check the real J10 and, if necessary, continue literal updates until it occurs.
   A legal mismatch leaves the simple W SCC; the condensation order excludes
   return to W before a defect. No second standard jump is needed or allowed.

For a finite next event at index e, the word on [0,e) is ten-legal. Every literal
update in this algorithm, except the final event itself, lies outside its one
whole W core, or substitutes for part of the initial fixed 149-letter prelude.
A skipped proper W remainder only reduces the ordinary work. Thus the total
ordinary forward work is at most K(m)+1. An allegedly infinite third phase would
produce longer and longer ten-legal finite prefixes with a fixed W core, directly
contradicting (1.1). This proves totality without assuming HC.

At the standard query, the current source is still an explicit set of O(m+1)
points. The ray test uses a constant 104 phase count and exact integer operations
on those points and on fixed phase overlaps. All source hits and prior-write
thresholds, INCLUDING the final infinite parity interval, are tested. Its cost
is polynomial in the sparse input bit length; a nonempty first hit can have a
huge numerical time without a huge bit length.

After the jump the field is stored as the original points XOR literal changes
XOR at most 104 finite diagonal segments. Membership requires at most 104 segment
tests and finite-set operations. Further O(m+1) literal updates add only O(m+1)
point changes. All coordinate and time bit lengths remain input-polynomial.
This proves Theorem 4. Set operations can be implemented with balanced trees;
expected hashing is not a premise of the polynomial bound.

The new `one_jump.py` implements this algorithm. It does not import `graph.py`.
The latter is used only by the proof/certificate replay. Smaller requested step
budgets return UNKNOWN. `NO_FUTURE_DEFECT` is a positive standard-tail certificate,
not NO_HIGHWAY. The complete endpoint is never replaced by a clean motif.

## 7. A local first-event horizon, and the still-missing global step

A further direct corollary is useful. Let K be a fixed finite target set and
R=max_(q in K) ||q-p_0||_infinity. If the FIRST future intrinsic J10 is in K, its
index satisfies

    e <= 52R+114m+223437.                                   (7.1)

Consequently this first-event-location predicate has a literal finite-horizon
algorithm depending on m and K, not on the distances of unrelated input black
cells. It stops NO if an earlier first event is outside K, or if the horizon
passes with no event. It does NOT answer whether some LATER event is in K.
Empty K is an immediate NO. The horizon is numerical in R, not polynomial in
log R; the unrestricted-location one-jump algorithm has the bit-time statement.

The old false endpoint-only bound is NOT revived: m occurs in (1.2). The silent
fold family has m=10n+76 and return age 56n+396, so arbitrarily long folds are
compatible with the new bound. The 20-black scalable feedback circuit has many
J10 events, and therefore does not satisfy the silent-word premise.

Most importantly, m in a restarted interval is that interval's FULL starting
mass. It can grow along an unknown infinite event chain. The core bound is not
a well-founded cross-event rank, and summing it cannot turn |B_t| into a fixed
original resource. Bounded J10 positions in the axial cross remain unresolved;
so do unbounded moving defect locations and other periodic tails. Neither
mu(N)->infinity nor a total event budget has been obtained.

This result does rule out, uniformly over ALL silent geometries and ALL input
coordinates, a mechanism left open by the endpoint-strip theorem alone: a fixed
amount of starting black supply cannot support arbitrarily long closed silent
feedback. Its unbounded duration must be paid for either by displacement, by
starting black supply, or by actual violations of the ten-factor language.

## 8. What is checked and what is not

Run `python scripts/check_silent_supply.py`. The runner makes a disposable copy,
regenerates the report and requires exact equality with the frozen `report.json`.
Only Python standard library and a C++17 compiler are required. No old simulator,
public manuscript, singleton Lean build or unrelated large wake search is altered.

The report records the ACTUALLY completed scope: independent complete finite-word
enumeration, full graph order and common-normal checks, every phase supply/width
identity, exact rational recurrence arithmetic, structured and random finite-word
controls, independently simulated first-event endpoints and a huge-coordinate
whole-field symbolic comparison. The first-event control at 10^60 standard periods
uses one standard plan and 150 literal forward updates; it is not simulated over
10^60 periods. Two different segment descriptions of the COMPLETE endpoint are
compared by an independent translation-class parity sweep.

These checks corroborate rather than replace the analytic all-length proof.
The small finite SCC certificate imports its generic folding argument. No source
in this package has been Lean-kernel checked or reviewed by an external referee.
A separate scope record explains the limited literature search; no independent
publication acceptance or exhaustive novelty determination is asserted.

## Appendix A. Inherited three-fold exclusion and why it covers finite paths

This appendix recalls the argument in `ten-factor-attraction.md`, Section 4.
It is reproduced for proof closure, not claimed as a new lemma. With A28 and
B102 as pinned in `model.py`, the word B A^n B A^m B is infeasible for ALL n,m>=0.
A specific cell has two consecutive reads both requesting R:

| Case | Cell | Earlier time | Later time |
|---|---|---:|---:|
| n=0 | (0,2) | 32 | 184 |
| n>=1, m>=n | (0,2) | 32 | 184+56n |
| n>=1, m<n, r=n-m | (1,4r) | 25+28r | 205+28(n+m) |

The five block poses are (0,0),N; (1,11),S; (1,11+4n),S;
(0,4n),N; and (0,4(n-m)),N. A has x in [-3,0], and its x=0 reads are
(phase,y,letter) = (0,0,L),(7,-1,R),(8,-2,R),(15,-3,L),(16,-2,L),(27,-5,L).
B reads (0,2) only at 32,R; on x=0 its maximum y is 2. Its reads at (1,9)
are 82,R and 90,L; at (1,4) they are 45,L and 53,R; at (1,8) 73,L and 81,R;
on x=1 its maximum y is 12. The first visit to (1,0) is 1,R. These finite facts
are regenerated in the new replay.

For n=0 the reflected second B reaches (0,2) at phase 82, with no intervening
visit. For n>=1 the first A run has x>=1 and the second B would need local
(1,9+4n), above its maximum. The second A run first reaches (0,2) at copy n-1,
phase 8, exactly when m>=n; earlier copies require local y<-5.
For r=n-m>0, the last earlier visit to (1,4r) is B phase 53 or 81 when r=1 or 2,
or A copy r-3, phase 7 when r>=3. Later first-run A copies cannot revisit it;
the second B would require local (0,11+4m), and the second A run lies in x<=0.
The third B first reaches the cell at phase 1,R. All three cases therefore
violate same-cell read alternation. No infinite extension hypothesis is used.

In the finite quotient of the 366-component, visits concatenate an initial
partial loop and words A and B. Counting starts of B allows two complete folds
and a third partial fold, but cannot allow completion of a third. This gives the
bounded lift used above. Every real finite silent path is represented, including
arbitrarily long unbounded powers; the finite enumeration by itself would not
justify this step.

## References and attribution

- Project: `proof/results/ten-factor-attraction.md` and
  `proof/results/ten-event-macros.md`, at the pinned mathematical base.
- Project: `proof/results/silent-axis-return.md`, especially its all-path common
  coordinate-normal certificate. This work does not rebrand the strip theorem.
- Project: `proof/results/silent-fold-reset.md` and
  `proof/results/defect-resource-spectrum.md`, for inherited controlled families.
- A. Gajardo, *A symbolic projection of Langton's Ant*, DMCS 2003, pp. 57-68,
  DOI 10.46298/dmtcs.2312. Symbolic forbidden-word/physical feasibility methodology.
- Exact periodic phase-ray checks retain the attribution of the parent project
  to Jillhewar's 2026 full-drift chronology method. They are not newly invented
  by the one-jump implementation.

The finite-support rule, old theorem scopes, and the distinction between an
all-input finite-event query and HC are unchanged.
