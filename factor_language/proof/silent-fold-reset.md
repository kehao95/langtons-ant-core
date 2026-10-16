# Silent foldbacks, autonomous depletion, and the cost of resetting a ribbon

**15 October 2026. Base inspected: `11894a516e40fef9be730e266936071c7750142c`.**

Evidence: the analytic finite reduction below, exact integer/word certificates,
and independent complete-state finite dynamics with two all-future tail checks.
Not Lean-formalized, externally reviewed, or a priority claim. No HC solution or
finite HC counterexample is asserted. No earlier implementation is changed.

## 1. Question and result

The new [exact J10 macro](ten-event-macros.md) invites two possible closures:
transport the [S_D two-endpoint tube](remote-stale-feedback.md) to J10, or reset
an event-free folded computation by a bounded local repair and run it again.
Both require additional physical information. Here one explicit family gives
an obstruction to the first and a quantitative lower bound for the second.
We also follow its ACTUAL autonomous continuation to its permanent standard tail.

States are complete finite black sets with pre-update pose on Z^2. White turns
right, black left; toggle, then move. Headings N,E,S,W are 0,1,2,3. J10 is the
existing intrinsic event: the true nine preceding turns plus the current turn
are not a cyclic ten-factor of the fixed standard word W. All other initial
cells are white. A reflected rule, torus, intervention, and extra ant are absent.

For each integer n>=0, the family X_n below has exactly 10n+76 initial black cells.
It creates a black lifetime at the origin at time zero and next reads that cell
at time 56n+396. Its first nine updates are intrinsic J10 events, but there are
NO J10 events at times 9 through 56n+396. The next is exactly at 56n+397.
After this long folded prefix, six autonomous scans take place, without new
markers. The first permanent standard time and the total intrinsic J10 count are

    tau(X_n) = 152n+2527,
    number of all future J10 = 56n+926.                     (1)

Thus this is a proved positive family, not an indefinitely renewable circuit.
The large input is an explicit finite ribbon, not a fixed-cardinality family.

For Y_n, the COMPLETE state immediately after the event at 56n+397, a literal
repair of length ell enabling the folded prefix of another member X_m, at ANY
translated/quarter-turned pose and with arbitrary unread additional debris, obeys

    ell >= max(0,4m-136).                                  (2)

The target is the prescribed folded finite read word, not necessarily equality
of complete fields. This stronger target flexibility makes (2) a useful reset
obstruction. It does not exclude repairs of length proportional to m, different
interfaces, or autonomous renewal for other inputs.

## 2. Explicit finite input, and inherited criteria

Use the following fixed words (wrapped B lines are concatenated):

    A = LLRRRRLRRLRRRRLLLLRLRRRRLRLL                         (28)
    B = RRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLRRRRLRLLLLRRRR
        LRRLRRRRLLLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRLL   (102)
    C = RLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLL        (44)
    D = LLRRRRLRRLRRRRLLLLRLRRRRLRL                         (27)

The A,B words are the inherited short loop and fold word from
[ten-factor attraction](ten-factor-attraction.md), not newly discovered modes.
Define

    w_n = C A^(n+6) B A^(n+2) D,       P_n=|w_n|=56n+397.  (3)

Run its GEOMETRIC turn plan from origin,N. Let B_n contain exactly those visited
cells whose FIRST requested letter is L. This is a finite, effective complete
input specification; cells outside the finite plan are white. Put X_n=(B_n,0,N).
Section 4 verifies all-n physical consistency and the subsequent continuation;
it is not assumed in the construction of the candidate input.

The supplied finite-word criterion is inherited: a geometric word is realizable
exactly when its requests at each physical cell alternate. The first letter
then determines that cell's required initial colour. This is the methodology
attributed to Gajardo (2003) in ten-factor-attraction, Section 2. The infinite
period checks retain the full-drift chronology attribution to Jillhewar (2026)
there. No new claim of either criterion is made.

The declarative [grammar](../../experiments/hc_global/silent_fold_reset/grammar.json)
contains every fixed letter and all affine exponents used below. It contains no
unverified statement about a simulated endpoint. A parser must derive geometry,
read identities, and initial colours from its words.

## 3. Exact autonomous continuation

Let

    V1=RLRLLRLR,                    |V1|=8;
    V2=RLRLLRLLLLRRRRLR,            |V2|=16;
    V3=RLRLRLLLLRLRRRRLLLLRLRRR,    |V3|=24.

The actual continuation from the COMPLETE state after w_n is

    f_n = E0 V1^(n+5) E1 V1^(n+5) E2
             V2^(n+4) E3 V2^(n+4) E4
             V3^(n+3) E5 V3^(n+4) E6.                    (4)

E0,...,E6 are the seven literal recovery blocks in grammar.json; their lengths
are 3,258,2,142,449,566,542. All their letters are explicitly supplied there.
In particular E0=RLL. Giving them as finite data avoids pretending that their
long finite scattering is a short symbolic identity.

The six variable scans have restored heading and vertical drift +4 or -4 in
their actual poses. Their anchors have fixed x and y of the form a*n+b with
a=0 or -4. The verifier derives these statements by the literal geometry.
Equation (4) has length 96n+2338. At time

    T_n=P_n+|f_n|=152n+2735

the exact head is (8,7),E and the complete black count is 18n+301. At the end
of w_n the head is (-1,0),W; its first subsequent R is the claimed J10 event.
Just after it, Y_n has head (-1,1),N and black count 18n+128.

The words in (4) are the NATURAL physical continuation on the input B_n.
No reseeding, cleaning, copying a reference field, or choice of a future branch
is allowed. The all-parameter certificate for this claim is the next section.

## 4. All-parameter coverage by ordered affine read intervals

This section explains why a finite check proves (3)--(4) for EVERY n, rather
than promoting a sampled family. It uses the special algebra of the supplied
script; it is not a general HC abstraction.

Represent a physical cell by (x,r-4k), 0<=r<4, k integer. Each literal phase of
a fixed block gives a singleton k interval. Each phase of a variable repeated
block gives an interval

    L(n)<=k<=U(n),

whose endpoints have integer slope 0 or 1. A record stores x,r,L,U, its block
index, requested letter, and its physical time as a*n+b*k+c. There are 2287
such records, including every recovery phase. They are reconstructed, not loaded
as trusted simulated traces.

For completeness, if a block phase is at y=a*n+b before repetition, set
alpha=-a/4 and beta=(r-b)/4. If its drift is -4, repetitions j=0,...,n+c-1 give

    k=alpha*n+beta+j;
    L=alpha*n+beta, U=(alpha+1)n+beta+c-1;
    time within block = P*k-P*alpha*n+(i-P*beta).

For drift +4 they give

    k=alpha*n+beta-j;
    L=(alpha-1)n+beta-c+1, U=alpha*n+beta;
    time within block = -P*k+P*alpha*n+(i+P*beta).

All phases in a block have the same alpha and P, so their chronological order
at any fixed physical cell is the CONSTANT order of i-P*beta or i+P*beta.
Different blocks are ordered by their script positions. Literal blocks are
ordered by phase index. Thus the exact per-cell word is the ordered subsequence
of records whose intervals contain k. No chronological permutation is guessed.

**Affine-order lemma.** For a finite collection of integer endpoint functions
of slopes 0 and 1, put

    N = 1 + max({0} union {b0-b1 : b0 is a slope-zero constant,
                                      b1 is a slope-one constant}).

For n>=N, the order of all endpoints is fixed, except for identical functions
which remain identical. Every open endpoint gap which is positive at N remains
positive, since any sign change would require an excluded crossing. Its integer
membership type therefore stays the same. To check a property depending only on
which intervals contain a cell and on their fixed record order, it suffices to
check every n=0,...,N, sweeping the integer intervals between consecutive values
of L and U+1. Such a sweep includes endpoint cells and all unbounded empty ranges.

Apply the lemma separately in each (x,r) group. Include endpoints of the field
templates in Section 6 and boundaries at every fixed cell queried in the nine
inverse updates or the all-future tail test. Exact reconstruction gives 874
endpoint functions, 1772 cross-slope pairs, and MAXIMUM crossing parameter 1.
Consequently **N=2**, and the three cases n=0,1,2 cover all parameter values.
This is an integer-order theorem, not an empirical stabilization assumption.

For each nonempty cell interval, read the entire selected record sequence.
If a fold record is present, its first letter defines the initial bit. Otherwise
the bit must start white, so a recovery-only first read must request R. Starting
with that bit, EVERY record is checked, toggling after each read. This proves
both feasibility and execution from precisely B_n rather than a larger implicit
seed. Source, Y_n, and final fields are obtained by the appropriate complete XOR
of actual reads. No old black cell is thrown away.

The resulting 7491 ordered-read checks prove the finite dynamics. Field template
and mask equality use the same ordering lemma with their extra endpoints. Linear
mass formulas above the last crossing are checked as exact coefficient sums of
interval lengths, not guessed from two numerical masses. Finite endpoint poses
and times are symbolic identities. The minimum fold y-coordinate is -4n-26:
all record endpoints satisfy this inequality coefficientwise and one attains it.

## 5. Permanent tail, exact first time, and J10 count

The last 208 letters of f_n are two copies of one phase u of standard W. The
previous letter disagrees with the backward 104-periodic extension of u. At
T_n the full field has x coordinates between -14 and 10, independently of n.
The proposed u tail has drift (2,2).

For each phase q_i+k*(2,2), there are only finitely many k>=0 with x in this
field range: together there are 29 possible fixed source-colour query cells.
Every other future ray cell starts white. Their bits are included in the affine
ordering check of Section 4, so their eventual n-dependence is exactly covered.
Previous planned writes turn on at the finite full-drift overlap thresholds.
The exact parity verifier checks epoch zero, every overlap threshold, every
initial hit and its successor epoch, including the final infinite interval.
All three parameter order cases pass. An independently written ordered-class
minimal-seed/ray verifier agrees. These are infinite certificates, not inference
from the observed 208-letter repetition.

It follows that the future is standard at T_n and therefore at T_n-208. If it
were standard at any earlier time, the infinite tail would agree on a full
104-letter block and hence on its whole backward periodic extension, contrary
to the letter at T_n-209. Thus (1)'s FIRST entry is exact.

All A powers have only allowed cyclic ten-factors. The fixed fold interfaces
also pass. Its only origin reads are time 0,R and P_n-1,L, as verified from the
record times. The true initial nine-turn history is LLLLRLLLL; it is derived by
literal inverse updates on B_n, not stipulated. All nine initial J10 events
occur, then none occur at 9,...,P_n-1, and P_n is a J10. Therefore Z_n=F^9 X_n
has source pose (-1,2),W and first J10 at offset 56n+388, at (-1,0),W; its
post-event pose is (-1,1),N. Z_n has 10n+75 black cells.

For the complete future, the numbers of illegal cyclic ten-factors per V1,V2,V3
period are 8,9,11 respectively. Every minimum repeated block leaves at least
nine letters on both sides of a period insertion. Inserting one whole period
preserves those boundary contexts, so its contribution is exactly the cyclic
count. This gives the slope 2*8+2*9+2*11=56 in (1). Counting the finite n=0
script and the next nine standard letters gives 926 intrinsic events, with the
last at 2534. The last violating ending context lies in the fixed recovery cap,
so for every n the last event is at tau(X_n)+7. There are no later events.
Wholly forward-contained windows starting at time zero omit exactly the first
nine intrinsic events, giving 56n+917. These two counts must not be confused.

**Corollary (no universal J10 endpoint tube).** The exact first-J10 macros from
Z_n have the SAME source, event and post-event poses, but their duration and
excursion depth are unbounded. No finite radius depending only on those poses,
and no endpoint-distance-only time budget with universal constants, covers all
complete finite inputs. In particular the S_D tube cannot simply be renamed a
J10 tube. The input mass and diameter grow with n; the prior COMPLETE-SOURCE-hull
J10 bounds remain valid. This corollary does not prove undecidability of any
spatially filtered J10 predicate; it refutes this particular proposed proof.

## 6. A reset must alter linearly many required cells

Use n disjoint four-row tiles y=-12-4j+r, 0<=j<n, 0<=r<4. The fold read-footprint
and initial colour requirements I, and the complete post-event bulk O, are:

    x       I (r=0,1,2,3)        O (r=0,1,2,3)
   -5       00..                 1100
   -4       0000                 1111
   -3       0011                 1100
   -2       1101                 0001
   -1       1011                 1000
    0       1100                 0011
    1       0000                 1111
    2       ..00                 0011

A dot imposes no target read requirement; it is not an additional prescribed
black cell. There are 28 requirements and ten black requirements per tile.
O has eighteen black cells per tile. The source caps have 28 top and 48 bottom
black cells. Y_n has 50 top and 78 bottom cap cells. Their complete coordinate
lists are regenerated in `derived_masks.json`. Top caps are fixed; bottom caps
are translated by (0,-4n). All these black fields are inside -5<=x<=2.
Section 4 checks their equality to the COMPLETE fields for all n.

To enable a translated/rotated w_m, the field after a repair must agree with I
on each of its m disjoint target tiles: their FIRST reads force those bits.
Additional black cells outside the target footprint are allowed.

First take parallel orientations (zero or a half turn). Against the infinite
periodic band O, enumerate all vertical residues modulo four and all overlapping
horizontal offsets. The range -12<=dx<=12 contains every overlap; outside it
all target black requirements are against white. The exact table of 5600 bit
comparisons proves at least FOUR mismatches per complete target tile, in either
orientation, for every offset. With no vertical overlap the number is ten.
Truncating O to the n-tile bulk can split at most two target tiles at its two
horizontal boundary lines. Discarding these two loses at most eight from this
FOUR-per-tile lower count. Restoring the 128 cap black cells can fix at most
128 mismatches. Thus Y_n differs from the necessary target bits at at least
4m-8-128=4m-136 distinct cells.

For perpendicular orientations the target tiles occupy disjoint four-column
slabs. The width-eight support of Y_n meets at most three of them. Every other
tile needs ten black cells where Y_n is white. Hence the bound is
10*max(0,m-3), which is at least 4m-136 for every m>=0.

Every literal repair update toggles exactly one cell. To correct d distinct
initial mismatches needs at least d updates, regardless of intermediate motion
or repeated toggles. The endpoint pose can only add obligations. This proves
(2) uniformly in n,m and all translated/quarter-turned target poses.

The proof concerns the actual autonomous states Y_n, with both old and newly
written black cells retained. It is stronger than comparing cardinalities, or
comparing complete fields at only one chosen alignment. In particular no repair
word of fixed literal length, independent of m, can reset arbitrarily large
members into this same folded-word interface. Repairs growing with m survive.

## 7. Conditional J10 cost for a CLEAN nonexpanding reset

There is an additional, narrower consequence of the already proved
[all-input mass-defect inequality](mass-defect.md). Suppose a real repair from
Y_n ends at EXACTLY a translated/rotated complete B_m, with no additional debris.
Its black change is 10m-18n-52. If V counts forbidden ten-windows wholly contained
in its ell updates, the imported inequality gives

    351 V >= 3ell + 468n - 260m + 1030.                    (5)

Combining with (2) is valid but not essential. In particular, for m=n and n>=34,

    V >= ceil((220n+622)/351).                             (6)

Thus a clean same-size reset cannot use a bounded number of J10 events either.
This is an application of an imported all-input theorem; only its exact algebra
is newly checked here. No reset of that kind is asserted to exist. If arbitrary
leftover black debris is allowed, its mass belongs in (5), and (6) is NOT an
unconditional event-cost bound. The more general flip bound (2) still applies.

## 8. What the closure attempt has and has not achieved

The family shows that a J10-free segment may contain an arbitrarily long return
to a newly created black cell, and that its endpoints need not describe its
geometry. It then performs six real autonomous scans, not six externally reset
experiments. The complete parameter-dependent continuation is certified positive.
A constant-size patch cannot reproduce an arbitrarily large next ribbon; even
a clean nonexpanding reset has a linearly growing defect cost.

None of these is a well-founded rank for ALL finite states. A growing reset,
a different pattern, unrestricted archive interaction, or a different nonstandard
periodic word is not excluded. The universal J10 macro still has no total event
budget. The fixed finite-support HC input is not replaced by this special family,
and the parameter n is never increased by external intervention within a run.
No global contradiction or finite negative seed has been obtained.

## 9. Reproduction

Run `python scripts/check_silent_fold_reset.py`, or `python check.py --compare
report.json` inside the isolated package. The repository runner uses a temporary
copy. It reconstructs all records, masks, finite order cases, complete endpoints,
infinite tails and mismatch tables, and requires byte-identical reports/masks.
Python standard library only; no graph optimizer or solver is trusted.

Current evidence: 2287 read records; 874 affine functions and 1772 cross-slope
pairs; all parameter order cases n=0,1,2; 7491 ordered reads; 510 all-future parity
checks; 5600 reset-mask comparisons. Independent mutable dynamics checks ten
parameters through n=64, totalling 59826 complete-field updates; these are controls,
not the universal proof. Damaged recovery, changed initial colour, and a blocker
10^20 standard epochs away are rejected; an off-trace marker remains harmless
without being erased. The known four-cell standard port is a scoped positive
control, not a rerun of its original coverage theorem. No old broad test suite,
large wake search, previous Lean proof, or publication release is repeated.
