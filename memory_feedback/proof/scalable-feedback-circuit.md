# A twenty-cell one-shot feedback circuit and a failed global closure

Evidence: analytic all-parameter arguments plus regenerated integer inequality
certificates, exact finite dynamics, and two all-future checks. Not Lean-formalized,
externally reviewed, or a publication-priority claim. This proves a positive
family and refutes a proposed global age bound. It does NOT prove or refute HC.
The four-cell port and the supplied-word verification methods are inherited.

## 1. The closure attempted, and the outcome

The [endpoint-tube theorem](remote-stale-feedback.md) says that the next S_D
macro, if its event is at e and its source head is p, has duration at most

    Q*||e-p||_infinity + 5*Q^2,     Q=2^D.

For a black lifetime born at b and next read at e, its birth and consumption
positions coincide. If there are NO intervening S_D reads, this immediately
bounds its age. A possible closure was to extend this to a bound depending only
on D, the number of intervening S_D reads, and initial black cardinality.

That extension is FALSE. We construct a complete twenty-black initial state
X_n for EVERY even n>=20, with a newly created black lifetime satisfying

    birth at (0,2):                  b=60,
    its next read, black:           e=624*n-1516,
    lifetime age:                   e-b=624*n-1576,
    S_128 reads strictly in (b,e):  exactly 31.

Nevertheless X_n is HC-positive, with exact FIRST standard-entry time

    tau(X_n)=624*n-742 = e+774.                              (1)

Thus the circuit really executes an arbitrarily large feedback excursion from
constant black cardinality, but it does not renew itself. All twenty black cells
are placed at INPUT time. The run has no intervention, repositioning, recolouring,
external controller, infinite prelaid track, or deletion of historical cells.
The coordinates depend on n; one fixed seed is NOT made to execute arbitrarily
many circuits.

## 2. Exact seed and the inherited reference

The literal rule is white/right, black/left, toggle then move, on Z^2. A state
at time t precedes update t. Headings are N,E,S,W=0,1,2,3. All unspecified input
cells are white.

Use the already certified [outgoing four-cell port](../../four_cell_port/PROOF.md)

    G={(0,-1),(1,1),(1,3),(2,2)}

at the origin facing E. Let rho be clockwise quarter rotation. At a pose (p,h),
write G[p,h]=p+rho^(h-1)G. For even n>=20 the complete input black set is

    B_n = union of G[p_i,h_i], i=0,...,4,

with the following five poses:

| i | p_i | h_i |
|---|---|---|
| 0 | (0,0) | E |
| 1 | (n-1,n) | N |
| 2 | (-n,3n-4) | W |
| 3 | (-5n+5,-n) | S |
| 4 | (-3n,-3n+8) | E |

Start the one physical ant at (0,0),E. Section 3 proves that these five four-cell
sets are pairwise disjoint, so the input has EXACTLY twenty black sites.

### Reference data, checked rather than inferred from a long run

From G the 182-step prefix A reaches position (5,1),E with 36 black sites. Its
entire subsequent word is U^omega, where U is the fixed standard 104-word with
drift (2,2). Define q_i and h_i to be the absolute reference pose at time 182+i.
The finite phase data used below are

    q_14=(8,2), h_14=E, U_14=R;
    q_61=(7,8), h_61=N;
    q_71=(6,9), h_71=N.

The reference reads (0,2) white at update 60, does not read it again in the
182-step prelude, and never reads it on the tail (all tail x-coordinates are
at least four). It is therefore a newly born, permanent black lifetime on the
UNPERTURBED reference. The constructed circuit will read it again.

The four initial G sites are first read at offsets 1,22,32,58. The only later
S_128 reads of this reference are at offsets 157,280,281, with respective
previous reads 9,144,145. The no-later-events claim is checked for all future:
for each L phase of U, there is a same-cell preceding phase at distance <=128
already available by tail epoch one. The finite prelude/first epoch is checked
literally. The stationary maximum black reread gap is 116, as in the retained
standard-memory analysis.

The reference's complete 36-cell state passes both the all-epoch breakpoint
parity verifier and the independent stable-class/clean-seed-and-ray verifier.
The latter criterion retains its attribution to Jillhewar's 2026 supplied-word
result, already cited in `periodic-candidate-certification.md`; neither it nor
the four-cell port is claimed new here.

## 3. Universal autonomous execution of the five stages

Put n=2k, k>=10. The five claimed stage words, in their respective rotated poses,
are

    A U^(k-4)  U[:61],
    A U^(2k-5) U[:71],
    A U^(4k-6) U[:61],
    A U^(2k-7) U[:71],
    A U^(3k-4) U[:14].                                      (2)

The endpoint identities from the phase data give the start times

    t_0=0,
    t_1=52n-173,
    t_2=156n-440,
    t_3=364n-821,
    t_4=468n-1296,
    e=624n-1516.                                             (3)

Stages 0 through 3 end at the next table pose. Stage 4 ends at (0,2),E, BEFORE
its next update. This final update is not included in (2).

Endpoint algebra alone would not prove these words executable: previous wakes
and future initial ports could cause an earlier divergence. The next certificate
is the missing physical guard.

### 3.1 Pairwise separation of all stage READ sets

Let V_i(k) be the full set of pre-update read positions in stage i of (2), not
its black set and not just its net flips. The following ten strict separations
cover every pair. A row states max l(V_A) < beta <= min l(V_B).

| A | B | l(x,y) | beta(k) |
|---|---|---|---|
| 0 | 1 | y | 2k |
| 2 | 0 | x | 0 |
| 3 | 0 | y | -2 |
| 4 | 0 | x | 0 |
| 2 | 1 | x | -2k+1 |
| 3 | 1 | y | 2k |
| 4 | 1 | y | 2k |
| 3 | 2 | y | -2k+1 |
| 2 | 4 | x-y | -11 |
| 3 | 4 | x | -6k |

Here is the all-parameter checking argument. Each read set is exactly a union
of 182 affine points, 104 affine arithmetic segments, and the stated 14/61/71
partial-epoch points. For a segment

    p_i(k)+rho^r q_j + a*d_i,    0<=a<R_i(k),

its extrema under l are at a=0 or a=R_i(k)-1, according to the sign of l(d_i).
They are affine integer functions of k. Partial-epoch positions use a=R_i(k).
Thus each table row reduces to FINITELY many inequalities alpha*k+gamma>=0.
Such an inequality holds for all integers k>=10 iff alpha>=0 and
10*alpha+gamma>=0. These two conditions are checked exactly, for every point
and segment; no sampling or floating-point optimization is involved.

The regenerated certificate contains 6,832 such inequalities and has minimum
integer slack zero. Every R_i(k) is also checked to be positive throughout the
domain. In particular the table establishes V_i(k) intersect V_j(k)=empty.
Every initial port cell belongs to the corresponding reference's first 59 reads,
hence to its V_i. The twenty input cells are consequently distinct, and a port
belonging to another stage is outside the whole current read set.

### 3.2 Why the disjoint read sets suffice

At the start of stage i, previous stages have changed only cells in their V_j.
Every other initial port is also outside V_i. On V_i the complete true field
therefore agrees with a fresh rotated G, with white everywhere else on that read
set. First-difference induction makes the entire stage word in (2) literal.
Induction over the five stages proves (2)--(3) for the ONE complete input B_n.
All previous black residue is still present outside the current stage reads.

The apparent online placing of gates used during discovery is not the theorem's
execution model. Formula B_n places all gates at time zero, and the read-set
separation proves precisely why these remote initial additions do not alter
an earlier stage.

### 3.3 The actual long-memory return and the count 31

The target x=(0,2) is not initially black. Stage 0 writes it black at b=60.
It is not read again in that stage, and the read-set separations exclude it
from stages 1--4 up to time e. At time e the ant reaches x, E, and reads it
black; its next turn is L, while the fresh stage-4 reference would require R.
This is an exact first returned lifetime, not a geometric near-return.

In (60,e), stage 0 contributes its three offsets 157,280,281. Each of stages
1--4 contributes all seven reference offsets 1,22,32,58,157,280,281. No other
stage has read any of its cells. Its four initial black first reads occur at
absolute times greater than 128, and so are genuine intrinsic S_128 events.
All other gaps are those of the reference. Therefore the count is exactly

    3+4*7=31.                                                (4)

The consumption at time e itself is NOT included. This convention matters.

## 4. The loop does not renew: a full-history P104 recovery certificate

To decide whether the return might start another enlarged circuit, retain the
FULL endpoint B_e(n). It has all five old wakes. We do not replace the physical
input by a cleaned configuration.

Use the fixed unbounded region

    Omega={ (x,y): x>=-16 and -14<=x+y<=12 }.                 (5)

We prove that the restriction of B_e(n) to Omega is the SAME 90-cell set C for
every k>=10. This is an equality of restrictions for this constructed family,
not a confinement hypothesis on arbitrary HC inputs.

### 4.1 All-parameter equality of the protected field

The complete endpoint is the XOR of all twenty initial sites and every actual
read position in (2), counted with its visit parity. The stage-1 read set has
x+y>12. Stage 3 has x+y<-14. Stage 2 has x-y<-44, whereas Omega entails
x-y=2x-(x+y)>=-44. Those three stages and their initial ports miss Omega.

Stage 0 has a fixed prefix and NE period streams. Every epoch j>=6 has x+y>12;
all k>=10 include the first six epochs. Its terminal partial epoch is outside
Omega. Thus its restriction is constant.

For stage 4, let r=3k-4 and change epoch variable from j to v=j-r. Every tail
point becomes

    p_4(k)+q_i+j*(2,2) = q_i+(-8,0)+v*(2,2),               (6)

independent of k. Complete epochs have -r<=v<=-1; the partial epoch has v=0 and
i<14. At k=10, r=26. Every additional epoch v<=-27 lies below x+y=-14. The
stage-4 initial port and 182-step prefix also lie below that line for all k>=10.

Consequently C is the following finite XOR, restricted to Omega:

    G;
    all 182 stage-0 prefix reads;
    q_i+j*(2,2), 0<=i<104, 0<=j<6;
    q_i+(-8,0)+v*(2,2), 0<=i<104, -26<=v<0;
    q_i+(-8,0), 0<=i<14.                                    (7)

The checker evaluates (7), not an assumed invisible-history oracle. It obtains
90 cells. It additionally verifies all 1,247 affine and 208 constant inequalities
used above. The genuine full endpoints for eight parameters are checked against
an independent literal replay as a control, not as the universal argument.

### 4.2 Protected scattering and exact first standard time

From the reference state (C,(0,2),E), execute 774 literal updates. All positions
remain in Omega. The complete reference endpoint has 162 black cells and pose
(5,-3),E. Its next 104-word is the cyclic phase-103 shift of the inherited U,
with drift (2,-2). Both independent infinite checks certify its entire future.
Every tail phase lies in Omega, and adding (2,-2) preserves x+y and increases x.
Thus the whole infinite reference future stays in Omega.

The TRUE state at time e agrees with this reference on all of Omega. By
first-difference coupling its whole future read trace is the same, for every n,
irrespective of the physically retained exterior wakes. This proves standardness
from e+774.

The reference turn at offset 773 is R; the preceding letter in the backwards
104-periodic extension of the certified tail is L. Therefore a standard future
cannot start at or before e+773: any such 104-periodic word would agree with
the known tail over a whole period and hence at the preceding offset as well.
The mismatch contradicts that. Together with the positive certificate, this
proves the exact FIRST time (1), including the exclusion of starts before e.
It does not rely on a finite observed repetition as an infinite certificate.

This closes this particular self-renewal attempt in the positive direction.
At the return it does NOT recreate the original five-port input. The certified
future is P104, not a second expanding circuit.

## 5. Precise consequence for the attempted global bound

Let N_D(b,e) count S_D reads strictly between a black lifetime's birth and its
consumption. On all complete finite-support classical inputs there is no finite-
valued function F(D,m,M), computable or otherwise, satisfying

    e-b <= F(D,N_D(b,e),|B_0|)                               (8)

for every post-input-created consumed black lifetime. In this family the three
arguments are fixed at (128,31,20), while e-b=624n-1576 is unbounded.
The same examples refute a bound in terms of an upper budget m=31 and M=20.
Their excursion radius is unbounded as well.

By contrast, the zero-intervening-event estimate remains true. At a white birth
b there is no S_D event. If e-b>D and there is none in (b,e), the death is the
FIRST S_D from X_b and its source/event positions are equal. The endpoint-tube
time estimate gives e-b+1<=5*4^D. If e-b<=D the weaker bound e-b<=5*4^D is
immediate. Thus

    N_D(b,e)=0 => e-b<=5*4^D.                                (9)

Equation (9) is a direct corollary of the retained theorem, not a separate
rediscovery of its predictor proof. The false step was extending it across an
arbitrary finite number of intervening events without carrying spatial scale.

No bound depending on the COMPLETE input, its coordinate bit length or spatial
diameter is refuted. Here |B_0|=20 but diam(B_0)=Theta(n). The retained quadratic
event deadline explicitly includes input diameter and is fully consistent with
these linear-in-n delays. Nor does this show that one fixed seed has unbounded
lifetimes, or refute a uniform bound on event count for each input.

### The same obstruction for the J10 event

The factor-language article defines L10 as the ten-letter cyclic
factors of U, and J10 as a true ten-turn window outside L10. We use only this
definition, not its separate rigidity theorem. There are 84 allowed factors.
On every X_n the number of J10 events strictly in (60,e) is exactly **264**.

To check this uniformly, replace each U^r in (2) by one U. All r are positive.
Every removed complete standard cycle contains only allowed factors; both
length-nine boundary contexts are unchanged and one retained cycle is longer
than their combined lengths. Therefore no forbidden-factor occurrence is lost
or created at a splice. Direct counting on the fixed compressed word gives 264.
The same calculation through the protected recovery and nine following standard
turns gives 532 J10 events from absolute update 9 onwards, with the last at
e+782. Later factors are standard. Eight uncompressed physical runs corroborate
the interior count.

Thus a bound using only J10 count and initial black count cannot bound this
newly created lifetime's age either. This does NOT refute a bound on the TOTAL
number of J10 events as a function of the complete input; that is a different
potential route to HC.

## 6. Relation to HC and the exact remaining closure

The remote-feedback theorem still forces every non-ETC finite seed to reproduce
arbitrarily remote, late-born, long-lived black feedback. This construction shows
that long newly created feedback, even with a constant count of interruptions,
is physically possible. Its eventual positive certificate shows just as sharply
why that is NOT an infinite counterexample.

A proof may still use a spatially sensitive nonlocal rank or a full-input event
budget. A disproof would have to replace the four preinstalled remote turns by
a proven autonomous regeneration mechanism, with an exact next-source identity
and full-history guards. Neither mechanism is supplied here. New remote gates
cannot be appended after the run, and increasing n between separate inputs is
not an autonomous iteration.

The mainline therefore remains: exclude or construct indefinitely renewable
migrating feedback from ONE finite seed, and separately treat nonstandard
periodic tails. We do not replace that target by this family, by a strip promise,
by sparse-input time growth, or by a count-only surrogate already falsified above.

## 7. Reproduction and trust boundary

Run `python scripts/check_scalable_feedback_circuit.py`. Only the new isolated
package is copied and replayed. The runner requires byte-identical deterministic
JSON against the committed report. Python 3.10+ standard library suffices.

Actual controls: 6,832 all-parameter stage-separation inequalities; 1,247 affine
and 208 constant protected-field inequalities; 20 affine endpoint identities;
eight full literal runs and complete endpoints totalling 303,568 updates;
two different all-future tests for the port and recovery; 14,584 finite controls
of (9) from 21,600 further updates; malformed-parameter rejection; a remote
blocker rejection and retained off-trace marker. A parameter 2*10^60 is handled
by the proved formulas and twenty coordinates, not by a purported literal run.

The generic coverage and coupling are the written proofs above. These finite
controls are not an enumeration of arbitrary seeds.
