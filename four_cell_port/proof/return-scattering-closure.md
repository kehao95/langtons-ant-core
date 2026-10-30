# Composable unbounded-return scattering with genuine old-wake consumption

Analytic, unformalized all-parameter proof with exact finite certificates and
scoped independent replay. This is a restricted constructive convergence and
closure theorem, not HC, a global event budget, or a self-renewing controller.

## 1. Result and its difference from the previous closed family

The [previous guarded-scattering family](guarded-scattering-renewal.md) allowed
arbitrarily many encounters but protected western history with increasing x
boundaries. Its finite rule library excluded the reverse-scattering phase 72.
Here a packet makes an arbitrarily long northwest excursion, reverses southeast,
and actually reads an old black cell written on its earlier northeast approach.
After this history-dependent collision it converges. A third preinstalled marker
returns the output to the northeast input interface, allowing any finite number
of these packets to be composed with their complete histories retained.

For every integer n>=100, relative to its first marked read, a packet has:

    second marker:            q2(n)=(-2n-15, 2n+11);
    old-wake read:             q*=(-38,-32), at time 208n+51948;
    that black lifetime born: time -1736 on the incoming highway;
    its lifetime age:         208n+53684;
    output with two markers:  (-22,-60), SE, phase 14, by 208n+61256;
    third marker:             q3=(177,-260);
    output with three:        (203,-244), NE, phase 94, by 208n+75609.

All stated output times are supplied sufficient certificate boundaries, not
claims of first permanent-P104 onset. At the end of the distant reversal, the
head is at (-2n-39,2n-33); backward x displacement is unbounded in this class.
It is therefore not an instance of the previous uniform x-guard construction.
The new all-future protection uses x+y, together with a separate temporary
comparison region at the old-wake collision. No part of the real black field
is physically deleted.

The third marker is essential to THIS chosen NE-to-NE interface, not to
convergence: without it the two-marker packet has a certified SE highway.
It is preinstalled, not generated automatically. No claim of autonomous
indefinite renewal follows from the composability theorem.

## 2. Convention, standard word, and finite mature restrictions

Use the unchanged HC contract: complete finite black set B, integer head p,
headings N,E,S,W=0,1,2,3. Read white/right or black/left, toggle, then move.
State t is before update t. Rotations are clockwise quarter-turns, never an
unannounced reflection of the LR rule.

Use exactly the standard word w and thirteen-cell NE seed K from
`four_cell_port/verification/guarded_scattering/check.py`. Let P_i,H_i be its 104
pre-update positions and headings, with P_0=0, H_0=E and d=(2,2). Its minimum
future value of x+y is zero. Write w_a for its cyclic word beginning at phase a,
and R_k for clockwise rotation through k quarter-turns. The new checker pins
the earlier source's SHA256 and does not rerun its old 30-rule suite.

Put

    s(x,y)=x+y,  r(x,y)=x-y,  ell(x,y)=y-x,  G=-160.

For a phase j, orientation k, and a linear form f with f(R_k d)>0, define

    M(j,k,f,G) = XOR_(i=0..103) XOR_(L_i<=a<=u_i)
                      { R_k(P_i-P_j)+a R_k d },
    L_i=ceil((G-f(R_k(P_i-P_j)))/f(R_k d)),
    u_i=0 if i<j, and -1 otherwise.                         (2.1)

This is finite. It is the exact parity of all planned standard writes before
a phase-j collision, restricted to f>=G. It is a description of a finite
restriction, not an infinite physical input. A finite approach realizes it
once the old physical endpoint and the synthetic past omitted before that
approach lie outside the comparison half-plane. Those obligations are proved
below, not assumed from observed repetition.

Our first collision interface has head 0, heading H_57=S and field

    M1 union {0,q2(n),q3} union H,
    M1=M(57,0,s,G),             H subset {s<G},             (2.2)

where H is ANY finite complete historical black field. The two-marker version
omits q3. Future packets add further markers above the current packet's entire
read extent; their noninterference is proved in Section 8.

## 3. Finite A and C blocks, and the first long flight

### 3.1 First turn A

The exact 832-update orbit from (M1 union {0},0,H_57) ends at

    v_A=(-12,12), h_A=S,

with 580 black cells and a certified standard NW tail w_58. Every A read has
-10<=s<=9 and every tail read has s>=G. Both infinite checkers accept this
COMPLETE reference endpoint. Its initial field has 484 cells.

Let Q_B,i be the phase positions in the primary collision frame of w_58
launched from this endpoint: Q_B,0=(-12,12) and Q_B,14=(-15,11). Then

    q2(n)=Q_B,14+n*(-2,2),

and the first reference read there is exactly 104n+14 updates later. The
finite ray calculation enumerates every i and integer z with
q2(0)-Q_B,i=z*(-2,2). All n+z are nonnegative for n>=100, and
min(104z+i)=14. The expected letter is R. This checks first contact, not just
that the proposed marker eventually lies on the reference route.

The marker q2(n) is strictly left of all A reads, for every n>=100. The fixed
q3 is absent from A and from every future NW phase ray. The old field H is
outside s>=G; the A prefix and its NW reference remain inside. First-difference
coupling proves the actual A block and the subsequent 104n+14-update flight B,
ending at the black marker q2. Its absolute packet time is 104n+846.

### 3.2 Distant reversal C

Let M2=M(72,3,ell,G). The exact 51272-update orbit from

    (M2 union {0},0,(H_72+3) mod 4)

ends at v_C=(-24,-44), heading N, with 2569 black cells and a certified SE
reference tail w_18. Its initial field has 485 black cells. All its finite
reads have ell>=G and, after translation by q2(n), s>=G. Its bounds are
-75<=s<=63 and -76<=r<=54 in LOCAL coordinates.

The true field before this C block agrees with this kernel on

    Omega_C(n)={s>=G and ell(v-q2(n))>=G}.                  (3.1)

Indeed every black cell of the A endpoint and q3 lies strictly below the ell
boundary. So does every point of the synthetic standard past preceding the
A endpoint. Their maxima are finite; subtracting ell(q2(n))=4n+26 makes each
required strict inequality an integer affine inequality in n. They hold at
n=100 with nonnegative slope thereafter. Hence inside (3.1), the actual B
writes equal exactly the mature M2 writes from (2.1). The marker adds {0}.
The arbitrary H contributes nothing because of the s boundary.

Thus C is an actual literal block on the complete input. No all-future
conclusion for the TRUE orbit is inferred from its isolated-kernel tail:
the older field outside Omega_C will matter during the reverse flight.

## 4. Exact first return to old memory, not an assumed invisible archive

At C's end the head is

    q2(n)+v_C=(-2n-39,2n-33), h=N,                        (4.1)

at packet time 104n+52118. Its isolated reference follows w_18 southeast.
Let Q_D,i(0) be the 104 phase positions from (-39,-33), heading N. For general
n the phase positions are Q_D,i(0)-n*(2,-2).

The true field and this reference differ by the following exact XOR:

    A_endpoint XOR B_writes XOR (q2(n)+M2) XOR {q3} XOR H. (4.2)

The finite C writes cancel because both trajectories execute them identically.
The two copies of the marker q2 also cancel. This identity retains every older
write; it does not identify the true state with a cleaned reference.

All reverse reference phase rays have s values strictly below both the NW B
write stream and q2(n)+M2, while still having s>=G. Therefore they cannot read
those two terms or H. The remaining first-difference query is against the fixed
finite A endpoint and q3.

For each phase i and black point b in A_endpoint union {q3}, enumerate integers
z satisfying

    b-Q_D,i(0)=z*(2,-2).

There are 158 phase/cell candidates. Every n+z is nonnegative for n>=100.
The minimum of 104z+i is -170, attained at phase index 38 and b=q*=(-38,-32).
No candidate belongs to q3. The reference letter there is R and the actual
cell is black. Hence the actual reverse flight has EXACT length

    104n-170 = 104(n-2)+38,                                (4.3)

and ends in the old black read at packet time 208n+51948. Before it, all turns
agree with the SE reference. At it, the real turn is L rather than R.

### The black cell was created by the same actual trajectory

In the incoming NE plan relative to phase 57, solve

    q*=P_i-P_57+a*d,
    104a+i-57<0.

The last such read is i=89,a=-17, at time -1736, and w_89=R. The A block never
reads q*; B is disjoint by its s range; C misses the return region below; and
(4.3) proves that D does not read q* earlier. Thus its black lifetime is exactly

    (208n+51948)-(-1736)=208n+53684.                       (4.4)

In every train realization below, the incoming flight has more than 1736
updates, so this birth occurs AFTER the finite input time, even in the first
packet. It is not an initially supplied marker, an intrinsic pre-input lifetime,
or a cell that is simply presumed eventually relevant.

## 5. A constant full comparison field after an arbitrarily long excursion

Use the fixed region

    Omega={s>=G and r>=G}.                                (5.1)

At the old read q*, the true field restricted to Omega is independent of n.
This is the closure-enabling fact. The arbitrary H is absent by its s guard.
The distant q2 marker and ALL C reads are outside Omega for every n>=100:
their r values are -4n-26 plus a bounded local value, strictly below G. This
does not say they were erased; they remain in the complete true endpoint.

For completeness, here is an explicit finite XOR formula for the field in
Omega. Start with A_endpoint union {q3}. For each Q_B,i put

    h_i=floor((r(Q_B,i)-G)/4).

Add by XOR all Q_B,i+j*(-2,2) with 0<=j<=h_i and s(Q_B,i)>=G. All h_i<n for
n>=100. The terminal 14 B reads at epoch n are outside Omega. Thus these are
exactly the B writes inside Omega, not a truncation by simulation time.

For the reverse flight write its complete epochs as v=j-n, so -n<=v<=-3.
For each Q_D,i(0) put

    l_i=ceil((G-r(Q_D,i(0)))/4).

Add by XOR Q_D,i(0)+v*(2,-2) for l_i<=v<=-3 when s(Q_D,i(0))>=G.
All l_i>=-n for n>=100. Finally add the first 38 phase positions at v=-2,
if they lie in Omega. Restrict the resulting finite field to Omega.

The resulting field C_old has 1446 cells. Its exact hash and the 3618 B terms
and 3893 D terms are recorded in the report. This is equality of the ENTIRE
inside field, including the old A scar and both relevant write streams.
It is not equality on the next few read positions or a bounded mask inferred
from matching poses. Every lower/upper epoch omission is justified by the
linear forms above.

### 5.1 Two-marker output

From (C_old minus {q3},q*,S), an exact 9308-update block ends at (-22,-60),S,
with a certified SE w_14 tail. All these finite reads and the infinite tail
stay in Omega. First-difference induction with (5.1) proves that the complete
two-marker state is permanently standard by packet time 208n+61256.

This is already an all-n positive family with a real unbounded-age readback.
Its whole-input realizations from K have FIFTEEN initial black cells when
there is no extra debris. No uniform onset bound depending only on this
cardinality is implied; coordinates still encode n.

### 5.2 Reset to the original NE interface

The marker q3 is not read in that 9308-update recovery. It is the phase-15
first-visit cell exactly 10401 updates along the SE reference, and is read
white/R there by the unmarked reference. The third initial black cell changes
that turn. The complete finite block from (C_old,q*,S) has 23661 updates and
ends at

    v_out=(203,-244), E, standard NE phase 94.             (5.2)

All its reads and its infinite NE tail stay in Omega. Two infinite criteria
accept its complete 3453-black comparison endpoint. The same coupling proves
the actual THREE-marker packet permanently standard by 208n+75609 when no
later packet interrupts it.

The initial q3 has not been manufactured by this process: omitting it gives
the different, permanent SE future just proved. This explicit distinction
prevents treating the reset as an autonomous instruction generator.

## 6. Single-packet theorem and protection under later interruptions

**Theorem 1.** Every complete state (2.2), for n>=100 and arbitrary finite
H subset {s<G}, has the three-marker behavior just described and reaches NE
standard phase 94 by time 208n+75609. The two-marker state has the SE output
from Section 5.1. All supplied black history remains physically present.

**Proof.** Sections 3 and 4 give the exact A, B, C, D execution and first old
read. Section 5 gives the exact whole-field restriction and protected finite
E continuation and tail. The comparison paths remain within the regions on
which field agreement was established, so a first divergent read is impossible.
This is a finite-stage induction plus an infinite-tail certificate, not
extrapolation from the sampled n values. QED.

For the three-marker packet, every read BEFORE (5.2) satisfies

    -109 <= s <= 59.                                      (6.1)

The upper bound also covers all initial M1 cells and the three markers.
The NW and SE flights have constant s on each phase ray; their arbitrarily
long lengths do not enlarge (6.1). The finite A, C, E blocks supply the other
extrema. At the C boundary, (4.1) gives x=-2n-39, so no n-independent backward
x-displacement or bounded-diameter packet footprint can replace this argument.

A later marker may interrupt the final NE tail. The single-packet theorem alone
would not guarantee old-history protection after that interruption. The next
section supplies the necessary nested-guard induction for the FULL composition.

## 7. Finite arithmetic connector and marker ordering

A packet outputs pose v_out, orientation NE, phase 94. After m>=100 full
periods and phase adjustment to 57, its next primary marker is displaced by

    Delta(m)=v_out+(m+1)*d+P_57-P_94
            =(2m+208,2m-242).                             (7.1)

Thus s(Delta(m))=4m-34>=366. The next diagonal guard starts at
s(Delta(m))+G>=206, while all previous packet black cells and reads not
in inherited history have s<=59. The minimum guard slack is 147, strictly
positive. Every synthetic pre-output standard write is also below the next
boundary; this is checked for each phase at its latest possible pre-output
epoch, with all earlier epochs decreasing s further.

It follows that, at the next primary, the full inside field consists exactly
of its M1, its three still-unread markers, and still later preinstalled markers.
The actual NE flight writes and the mature synthetic writes agree there because
the omitted pre-flight past is entirely outside. Inherited earlier history is
below an even older guard and hence below the new one.

The companion markers of this next packet cannot interrupt that NE approach:
q2(n) and q3 have r respectively -4n-26 and 437 relative to the primary, outside
ALL two-sided incoming NE phase lines. This is a geometric disjointness test,
not merely checking a finite flight. Nor can markers from a still later packet
cause a premature contact. Their minimum relative s is -83; (7.1) places them
strictly above both the current packet's entire read maximum and the maximum
s of an incoming flight before its primary. The latter is at most primary s+1,
as checked from the 104 phases with their latest pre-collision epochs.

These inequalities prove the chronological order of all planned contacts, not
just compatibility of consecutive endpoint poses. For m>100 their left sides
increase by 4(m-100); no further trajectory simulation is required.

## 8. Arbitrarily many genuine returns from one complete finite input

Choose ANY integer k>=0 and ANY integer lists

    m_1,...,m_k>=100,    n_1,...,n_k>=100.

Start with pose p_0=0, phase a_0=0, orientation NE. For i=1,...,k set

    Q_i=p_(i-1)+(m_i+1_[57<a_(i-1)])*d+P_57-P_(a_(i-1));
    p_i=Q_i+v_out,     a_i=94.                            (8.1)

Install at INPUT time all three cells

    Q_i,  Q_i+q2(n_i),  Q_i+q3.

The complete input is K plus these cells plus ANY finite black G0 subset
{s<0}; its ant starts at 0,E. All these sets are disjoint, and the input has
exactly 13+3k+|G0| black cells. Markers are never installed during execution.
For k=0 the initial state is already on the certified NE future.

**Theorem 2 (closed arbitrary-return trains).** Every such finite input follows
the prescribed packets with all past writes retained and reaches permanent
standard P104 by

    T = sum_(i=1..k) [104m_i+(57-a_(i-1) mod 104)
                                +208n_i+75609].            (8.2)

The output after k>0 packets is p_k, heading E, NE phase 94. Each packet contains
the genuine post-input-created black lifetime (4.4).

**Proof.** The canonical initial ray has s>=0, so it cannot read G0. The first
primary guard is beyond every K cell and the entire synthetic pre-start past;
at m_1=100 its slack is at least 243. Its companion markers miss the incoming
NE rail, and later markers are beyond the finite read envelope. Therefore the
first collision has the correct complete restricted field (2.2).

Apply Theorem 1 up to its output, but keep all later markers in the physical
state. Section 7 proves that they have not altered this prefix, that the next
collision has exactly the required restricted field, and that its guard is
strictly above all preceding history. Induct on i. The guards strictly increase
in the SAME absolute linear form s. Between collisions the previous certified
tail remains above its previous guard; within each new packet all reads stay
above the new guard. Consequently no later reset reactivates a retired region.
After the last packet there is no remaining forward perturbation and the
certified NE tail persists. Summing the exact block lengths proves (8.2). QED.

The assertion about arbitrary finite G0 is a proved initial guard, not a deletion
of an unknown future-active set. Complete-state train replays retain G0 and every
black point from every earlier excursion.

### Small input and repeated-return examples

With m_1=n_1=100 and no G0, the three markers are

    (204,205), (-11,416), (381,-55).

Together with K this is a SIXTEEN-black finite seed. It writes (166,173) at time
8721 and next reads it black at time 83205, an exact lifetime of 74484 updates.
It has a certified NE output at time 106866, at (407,-39), with 7796 black cells.

The retained six-packet example has m_i=100 and
n_i=(100,101,150,103,211,100). Its THIRTY-ONE-black input executes six such
returns and has a certified NE output at time 675566, at (2447,-249), with
50671 black cells. These are examples of the all-k proof, not a claim about all
sixteen- or thirty-one-black initial states.

## 9. Direction 3: a rank despite unbounded retreat and history reactivation

The packet phases are an exact segmentation of a restricted true orbit, NOT
PG secondary gates or intrinsic S_D reads. Use a finite-stage lexicographic rank

    (packets not yet completed, remaining stage index, local fuel).

The stage order is incoming NE flight, A, B, C, D, E. Each flight has the exact
remaining update count from the formulas above. In each finite A, C or E block,
choose its finite read rectangle, INCLUDING the last endpoint, and use the
scaled integer r=4 clock already proved in [clock.md](../../clock_escape/PROOF.md). The unchanged
exterior contribution cancels. Its computable upper bound over all internal
fields and poses yields the nonnegative integer fuel

    ceil((U_Q-C_Q(X))/epsilon_Q),

which decreases at every internal literal update. This remains valid for the
TRUE complete field: unread differences inside that rectangle merely contribute
constant terms, and the universal clock inequality holds for every colouring.
Transitions to the next stage decrease the middle coordinate, allowing fuel to
reset. Completing a packet decreases the first coordinate and starts the next
incoming flight; completing the last packet halts the certificate program.
The actual ant continues forever along its highway.

Unbounded excursion n makes the two flight counters large but does not create
new unbudgeted stages: the exact XOR return query and full return-region equality
proved that there is exactly the certified old collision and recovery. That is
the closure fact on which the rank relies. The clock did not prove the guard,
the return-field equality, or all-input coverage.

This rank carries the finite packet description. It is not a new all-state
physical rank, a global PG/S_D event bound, or a proof that arbitrary finite
seeds enter this interface.

## 10. Checkable evidence and trust boundary

Run from repository root, without Python -O:

    python four_cell_port/verification/return_scattering/check.py \
      --compare four_cell_port/verification/return_scattering/report.json

The declarative recipe consists of (2.1), the specified phases/endpoints/block
lengths, and the finite stable-XOR formula in Section 5. The checker rebuilds
both kernels and the entire return field, compares independent integer-vector
and position/heading simulators, verifies two finite all-future expressions,
and checks every affine inequality a*n+b>=0 by a>=0 and 100a+b>=0.
The 5685 regenerated inequalities, rather than samples of n, check the all-n
geometric bridge. No floating-point fit or simulation timeout is used as proof.

The regenerated report records all source and field hashes, finite block word
hashes, 85073 clock-step checks, 8 complete-input controls with 15 packets and
1752102 updates PER simulator, and arithmetic checks at 10^60. A second full
scoped invocation byte-compares the regenerated report. There is no claim of
simulating 10^60 periods. Wrong tail colour, a 10^60-period future blocker,
and unsupported or inexact parameter inputs are rejected. Rejection of the
parameter range is NOT a negative HIGHWAY decision.

The dependency is the unchanged earlier checker with its pinned SHA256. Its two
tail criteria share integer geometry primitives; they are distinct exact
formulations, not independently maintained software systems. The analytic
extraction from the ant to the parametric interfaces remains unformalized.

## 11. What was attempted and what is still not closed

The exploration tested the missing reverse phase on full finite incoming wakes,
then paired it with earlier side-turn outputs. The left-turn/phase-72 pair was
chosen because its reverse tail meets the ACTUAL earlier incoming wake, not
merely empty space on a parallel lane. The SE outcome was then composed with
an existing phase-15 reset, with the complete return field checked rather than
replacing it by a clean standard template. Other exploratory phase pairs and
finite samples are not promoted into this theorem.

This closes one previously missing kind of history processing: arbitrary-length
return flight, a read of memory written by the same ant, and repeatable recovery
in a family with unbounded packet diameter. It does NOT close arbitrary early
interruptions, nearby multiple blockers, arbitrary residual shapes at the return,
or creation of the next packet's three marked cells without preinstallation.
Every finite train still has its number of packets encoded in its finite input.
There is no single seed here proved to generate infinitely many packets.

The remaining global obligation is unchanged in kind: prove or refute autonomous
indefinite feedback from one arbitrary finite seed. This result provides a
stronger concrete interface on which that question can be tested; it is not an
all-input answer or a reason to identify positive constructed examples with HC.
