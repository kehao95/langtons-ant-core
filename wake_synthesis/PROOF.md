# Layer-profile uniqueness and inverse synthesis

## Additions integrated on 16 October 2026

The revision adds [mixed-wake interleaving](proof/mixed-wake-interleaving.md):
for full drift `(2,-2)`, `J(O)+V/2 = 1 (mod 2)` at arbitrary growth and width.
The [attributed periodic-growth closure](proof/periodic-growth-closure.md)
retains signed residues, small-drift restrictions and the unit-diagonal certificate.
These are a separate necessary screen, not premises replacing the complete
thin-wake enumeration. The incoming [profile replay](PROFILE_REPLAY.md) is
also bundled as additional evidence for the subsumed profile theorem.

[New scoped replay](evidence/review-2026-10-16.json) pins research commit
`2f6010a`. Original imported proof notes retain their historical execution
statements; the dated evidence records own current replay status.

## Previously integrated proof chain

The current main theorem fixes full drift `(2,-2)`, growth `12`, transverse
width `10`, and at most one odd translation class on each interior level.
It derives the standard period-104 word and the complete standard wake.

The proof chain is:

1. [Thin-wake proof](proof/thin-wake.md): extreme classes, five possible empty layers,
   complementary phases and 76 modular survivors.
2. [Upper certificate and exhaustive checker](verification/thin_wake/code/check.py):
   90,158 integer inequalities give caps 192/168/160/168/192; all 83 jobs finish.
3. [Standard-profile corollary](proof/layer-profile.md): the fixed count profile
   allows unspecified longitudinal residues. This intermediate theorem is
   subsumed by the current classification.
4. The retained proof below establishes the complete-wake special case,
   ordered-event coverage, general budgets and terminating inverse synthesis.

[Fresh full evidence](evidence/review-2026-10-15.json) records both the new
classification and the retained standard-wake/general checks. The proof notes
are preserved research snapshots; their statements about earlier replay dates
are historical. Current execution status is owned by the evidence report.

# Retained complete-wake and general-synthesis proof

The [current manuscript](paper/main.tex) proves all-period uniqueness for the
complete standard wake and drift `(2,-2)`. It updates the wake preprint within
its existing [Zenodo concept](https://doi.org/10.5281/zenodo.23402421).
The published [v0.1.0](release/v0.1.0/) remains unchanged; its general
wake-dependent bounds, inverse-synthesis theorem and detour obstruction are
retained below and in Appendix A of the new manuscript.

The new proof joins an integer period bound `P<=168` to complete enumeration of
ordered visits. Its conventional coverage and pruning arguments are given here
and in the paper; exact programs regenerate the finite certificates.
[Verification code](verification/standard_wake/) and
[evidence](evidence/standard_wake/) belong to this publication project.
The [clock companion](../clock_escape/PROOF.md) owns the shared integer clock.
The supplied-word criterion and constructive seed are attributed to Jillhewar.

## 1. Literal dynamics and the new inverse question

A complete state is X=(B,p,h), B a finite subset of Z^2, h=N,E,S,W=0,1,2,3.
Read white/R or black/L, turn, flip the current cell, then move one edge. Write F
for this update and chi(x,y)=(-1)^(x+y). The quantity

    sigma(X)=chi(p) for vertical headings, -chi(p) for horizontal headings

is invariant. A quarter-turn rotation changes its sign while rotating the whole
state and preserving the literal rule. A half-turn preserves it.

A word u of length P defines pre-update positions q_i, headings h_i and final
displacement d, starting at p_0=0 and a specified h_0. A periodic realization
means its complete infinite turn stream is u^omega from a finite black seed.
Require h_P=h_0 and d!=0. The field need not translate: retained debris and a
permanently growing wake are allowed.

Two phase positions belong to one translation class when q_i-q_j belongs to
Z*d. The quotient is by the FULL d, not its primitive vector. For d=(m,-m), a
class is specified by (x+y,x mod m). An odd class is one containing an odd number
of phase visits. In a realizable word it emits one permanent black strand per
period. Let O be the finite set of odd classes, given by distinct representatives.
This is not the complete black field, nor necessarily a phase-aligned set of new
black cells. Representatives may be moved independently by integer multiples of d.

**Inverse input:** d with d_x*d_y!=0, h_0, and finite O. No period, seed size,
active-core bound or retreat bound is supplied. Decide whether ANY word and
finite black seed realize exactly this drift, heading and odd-class wake.

This is a target-synthesis problem, not the decision whether an already supplied
arbitrary seed eventually enters that target. The finite wake is explicit input,
not an oracle extracting the unknown future of a seed.

## 2. Prior exact word criterion, recalled with proof

Choose an anchor b in each class and write q_i=b+a_i*d. A read of b+n*d at phase
i occurs in epoch n-a_i>=0, at time nP+(i-Pa_i). Thus its stabilized chronological
order is increasing i-Pa_i, equivalently decreasing a_i then increasing i.

**Known criterion (Jillhewar 2026, Theorem 3.1 / Remark 3.2).** In every class,
the stabilized word must alternate R,L,R,L,... starting R. This is necessary and
sufficient for finite-support realization; it gives an explicit finite seed.

Necessity: far enough along a class, every phase is present; infinitely many
such physical cells start white because the seed is finite. Their first turn is
R, and successive reads flip the color. Sufficiency: at b+n*d the available
phase word is the suffix obtained by deleting larger-a_i groups. For
min a_i<=n<max a_i, put a black seed cell there precisely when the number of
removed phases is odd. All other cells start white. Every available word then
has the correct first color and alternates. Induction on physical time realizes
all prescribed updates. Only finitely many boundary cells have been blackened.

Consequently each class contributes #R-#L equal to 0 or 1, and

    growth #R-#L = |O| = g.

Heading restoration gives g=0 mod 4, hence P even, and d_x+d_y even. These are
necessary filters only. The full chronological test is always retained.

A separate verifier uses the FULL constructed seed B. At phase i, epoch k, its
required color is

    1_B(q_i+k*d) XOR parity{(j,s):q_j-q_i=s*d,
                   s>0 or (s=0 and j<i), 0<=s<=k}.

Old-seed hits and self-write thresholds are finite. Check epoch zero, all those
thresholds, each old hit and one epoch after it. These cover all constant
intervals including the final infinite one. This second formula does not infer
permanence from a finite repeated prefix. A remote black blocker is not omitted.

## 3. Exact standard wake and canonical phase

The theorem fixes the full drift `d=(2,-2)` and these twelve odd classes:

```
Ostd={(-10,0),(-10,1),(-9,1),(-8,1),(-7,0),(-6,0),
      (-5,0),(-4,1),(-2,0),(-1,1),(0,0),(0,1)}.
```

A label `(t,r)` means `t=x+y`, `r=x mod 2`, so it specifies a class in
`Z^2 / Z*d`, including the longitudinal residue.

**Theorem.** Every heading-restoring periodic word of drift `(2,-2)` with this
complete odd-class wake, realizable from a finite complete black field, is a
phase of the standard 104-step highway word. There is no period bound in the
hypothesis. A finite-state orbit with an eventual periodic suffix satisfying
these data consequently has the standard future read trace.

**Normalization.** At an extreme transverse level the checker-axis invariant
forces every visit in a class to have the same turn: both neighbouring visits
are on the inward side. Section 2's alternating criterion forces exactly one R
in that class. Each visited extreme class is therefore odd, so the trace's
extremes equal the wake's extremes, -10 and 0. At the even top level a right
turn with both neighbours below enters east and leaves south; hence sigma=-1.
Both top residue classes occur once. The unique top event in class `(0,0)` is
at `(2k,-2k)`. Choosing it as phase zero and translating by `-k*d` preserves all
class labels and puts the ant at the origin facing east. This derives the
checker sector and pose from the wake.

## 4. A finite integer certificate bounds every period

### Context graph and coverage

Generate physically consistent first returns of length at most 20, append the
first turn again, include complements, and independently check each resulting
factor for a consecutive equal-colour reread. This yields 588 forbidden
factors of length at most 21. Every valid trajectory avoids each factor.

The proper viable prefix contexts form a longest-suffix automaton with 4,931
contexts. Place each context geometrically relative to its endpoint, retaining
only placements in `-10<=t<=0` and headings compatible with sigma=-1. Each edge
is one literal turn, move and context update. This graph has 54,718 vertices
and 90,158 edges. After suffix warmup, every periodic realization lifts to a
closed walk of exactly P edges: level, heading and context all repeat.

Repeatedly delete any vertex with zero incoming or zero outgoing degree in
the retained graph. Every closed walk survives: its first allegedly deleted
vertex would still have its predecessor and successor. A separate reverse
insertion check verifies the proposed deletion order. The retained induced
graph has 24,424 vertices and 37,330 edges, all inherited edges included.
The potential inequalities need be checked only on those retained edges.

### Integer potential and telescoping

Use the per-level weights

```
alpha_t = -2*(-1)^t*(t+5)^2
alpha   = (-50,32,-18,8,-2,0,-2,8,-18,32,-50).
```

With epsilon=+1 for R and -1 for L, the regenerated integer potential obeys

```
y_v-y_w+alpha_t*epsilon <= -1
```

on every edge `v -> w` starting on level t. Start all y at zero and enforce
`y_w>=y_v+1+alpha_t*epsilon` by queued integer increases. Cap all values at 180;
exceeding the cap fails the construction. At most 180 times the number of
vertices increases can occur. A final independent scan checks every retained inequality. The regenerated
potential has range 0..129 and maximum edge left-hand side -1; its construction
uses 89,187 queue removals and 71,847 increases.

The standard wake's level counts are
`o=(2,1,1,1,1,1,1,0,1,1,2)`. The realization criterion gives signed turn excess
o_t on level t. Summing the edge inequalities around the closed walk cancels
the y terms. Direct arithmetic gives `sum alpha_t*o_t=-168`, so `P<=168`.
The full class residues are used by the exact stage below.

## 5. Exact ordered visits and complete finite classification

### Representation

For each complete class `(t,r)`, rank its events by stable visit order
`k=0,...,m-1`. Even ranks turn R and odd ranks turn L. If a_k indicates arrival
from t-1 and d_k departure towards t-1, the literal rule gives

```
d_k = a_k XOR (k mod 2)          for even t,
      1-(a_k XOR (k mod 2))      for odd t.
```

The fixed checker sector orients every directed lattice edge. Occurrences at
its source and target must match in stable order: physical time advances by
one, and changing class representatives shifts every lifted time by the same
constant. Thus first source matches first target, with no free permutation.

Use representative `b_(t,r)=(r,t-r)`. An edge voltage delta is defined by
`b_source+e_out=b_target+delta*d`. A complete matched graph realizes a word if
and only if it is one cycle of voltage 1 and its times `j_i-P*v_i` increase in
rank order within every class. Here j_i is cycle position from the canonical
top event and v_i is accumulated voltage. Necessity follows from a real trace;
sufficiency follows by reconstructing the walk and applying Section 2.

### Exact completion costs and phase congruence

When one side of a class has I arrival edges and J departure edges, let o be
its odd-wake indicator and let a count processed-side arrivals at even ranks.
With complemented side bits for downward construction, feasible counts obey

```
m=2*(I+J-2*a)+o       for even t,
m=2*(J-I+2*a)-o       for odd t,
0<=a<=ceil(m/2),      0<=I-a<=floor(m/2).
```

These conditions are necessary and sufficient for count feasibility: choose
the indicated ones at the even and odd ranks. A boundary carries two incoming
and two outgoing counts with the horizontal residue swap. A finite dynamic
program retains the smallest remaining cost for each boundary; this is a sound
lower-bound oracle because future count transitions depend only on it.
Both directions find minimum 104. All hypothetical periods below 104 are
covered because every partial cost is nonnegative.

The class counts modulo four are, bottom to top,

```
(1,1),(0,3),(2,3),(1,2),(1,0),(3,0),
(2,3),(2,2),(3,2),(0,3),(1,1).
```

The normalized walk has `i mod 4=2*(x_i mod 2)+(x_i+y_i mod 2)`.
Its even x displacement gives `4|P`, and each phase group has P/4 events.
The residue sums in the four groups are all 2 modulo 4, hence `P=8 mod 16`.
Combined with 104<=P<=168, only 104,120,136,152,168 need remain.

### Safe chronological rejection

The search builds class arrival strings and immediately makes every forced
edge match. A closed component before the final level cannot join the mandatory
future events, so it is rejected. Every remaining component is an open chain.
On a chain, lifted event times have the form `z_chain+p_i-P*v_i`.
Consecutive ranks within one class differ by at least four, yielding

```
z_chain(v) >= z_chain(u)+4+p_u-p_v+(v_v-v_u)*P.
```

A positive cycle is impossible. Let n be the constructed event count and L the
search cap. On a simple cycle of q chain variables, its weight is C+K*P with
integer K and `5*q-n<=C<=n+3*q`: each chain contributes one index difference,
and their total ranges are at most n-q. If K>=1 the weight is positive for all
P>=n. For K=0 it is constant; for K<=-1 it decreases with P. A positive cycle
at P=L therefore rules out every n<=P<=L. This justifies the cap-based check.

### Consecutive-visit rank pruning

Lift a fixed open chain to actual lattice coordinates by accumulating voltages.
Two consecutive occurrences of the same physical cell on this chain must have
ranks k and k+1. Indeed, a sufficiently late occurrence is a contiguous segment
of the real periodic trajectory with every involved cell in its stable visit
regime; no other visit to that cell lies between the two occurrences. This
rules out omitted ranks even when the two turn bits happen to alternate.

The implementation scans each chain separately, using lifted coordinate
`(r+2*v,t-r-2*v)` and remembering the previous rank at each cell.
Independent chains are given separate coordinate frames.

### Separation of fixed chains

Distinct fixed chains contain disjoint phase events. In every completed
periodic trajectory, all their period copies occupy disjoint contiguous time
intervals. Suppose adjacent class ranks occur at u in chain A and v in chain B,
with A!=B. Let ell_A count the events of A. Align their translated copies so
both events refer to the same physical cell. Their root times are
`z_A-P*v_u` and `z_B-P*v_v`, up to a common epoch. Stable order puts u before v;
disjointness forces the whole A interval to end before B begins. Therefore

```
z_B >= z_A + max(4+p_u-p_v, ell_A) + (v_v-v_u)*P.
```

Every interchain constant is now at least ell_A>=1. A cycle of those
constraints has weight C+K*P with C>0. For K>=0 it is positive at every positive
P; for K<0 it increases when P decreases. Consequently a positive cycle at the
cap excludes every smaller candidate period. The earlier within-chain tests
remain justified by the preceding cap argument.

The refinement adds an integer maximum on each existing constraint edge;
no new enumeration dimension or physical-state merging is introduced.

### Completed output and theorem composition

The retained original cap-168 traversal visits 40,227,976 class-string prefixes;
the consecutive-rank version visits 12,193,595; and adding chain separation
visits 8,580,751. All three complete and accept only

```
RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR
```

The upper certificate puts every realization in the enumerated domain.
Normalization is lossless, the representation is exact, and each rejection
above is necessary. Complete enumeration therefore proves uniqueness.
The explicit nineteen-cell seed in the paper realizes the accepted word by
the independent all-future formula of Section 2, proving existence.

## 6. General wake theory retained from version 0.1.0

The classification is a concrete application of the broader wake-dependent
inverse problem. The following analytic results and their exact algebraic
checks are preserved from the first release. The general diagonal cutoff for
the standard wake is 856; Section 4's chronological certificate strengthens
that cutoff to 168 and Section 5 completes the classification.

## 7. A global integer clock at the critical base three

Fix an INTEGER center c for the entire computation. Write s=x+y-c,
epsilon(h)=+1 on N,E and -1 on S,W, and

    f(s)=3^|s|-1,
    g(s,e)=f(s)/2        when e*s>=0,
           -3*f(s)/2   when e*s<0.

Define the complete-state integer

    Theta_c(X) = -sigma(X) sum_(q in B) chi(q) f(q_x+q_y-c)
                 + g(p_x+p_y-c,epsilon(h)).                 (1)

It is integral because f(s) is even, and its sum contains EVERY black cell.

**Theorem 1 (exact integer clock).** If e,e' are the before/after values of
epsilon, and s is the before-update coordinate, then

    Theta_c(FX)-Theta_c(X)
       = 1 + 4 f(s) * 1_{e'!=e and e*s<0} >= 1.            (2)

**Proof.** Set delta=+1 for R and -1 for L. The eight literal heading/color cases
give delta*sigma*chi(p)=e*e', while s'=s+e'. The field contribution is therefore
-e*e'*f(s). Let g_+(s)=g(s,+1), g_-(s)=g(s,-1). Directly from the definition,

    g_+(s+1)-g_+(s)=f(s)+1,
    g_-(s-1)-g_-(s)=f(s)+1,
    g_-(s)-g_+(s)=-2*sgn(s)*f(s).

For e'=e the correction cancels -f(s), leaving 1. For + to -, use
f(s)+g_-(s-1)-g_+(s)=1+2f(s)+g_-(s)-g_+(s).
It is 1 at s>=0 and 1+4f(s) at s<0. The - to + case is the same with signs
reversed. This proves (2), including s=0. QED.

The clock is defined on every complete finite state and every integer centre.
Its diagonal periodic application follows by cancelling the head term.

## 8. A diagonal wake pays for every update

Rotate a diagonal drift to d=(m,-m), m>0, preserving the transformed initial
heading. Let t=x+y. For each level t let o_t be the number of representatives of
O on it, and put

    A_t=-sigma*(-1)^t*o_t.                                  (3)

**Theorem 2 (wake budget).** Every realization with this wake and period P obeys,
for EVERY integer c,

    P <= K_c(O):=sum_t A_t(3^|t-c|-1).                       (4)

**Proof.** The head correction in (1) is unchanged over a period: t and heading
return to their initial values. Its field increment is the sum of -sigma*chi*f
for R and the opposite for L. Both chi and t are constant on a full d-class.
Section 2 makes the signed count exactly 1 on O and 0 on the other classes.
Thus Theta_c(F^P X)-Theta_c(X)=K_c(O). Sum the P inequalities (2). Complete
unchanged debris cancels; it has not been deleted. QED.

Any nonpositive K_c rejects the candidate wake. Minimizing over a finite chosen
set of centers strengthens the bound; centers between min(O's t) and max(O's t)
suffice for the implementation.

### Independent crossing-flow derivation and sharper directional bounds

The finite projected period t_i is a closed +/-1 walk. Let f_t be the number of
upward crossings of the cut (t,t+1); it equals the downward count. Let m_t count
visits to t and let u_t count straight increasing passages through t. Inflow/
outflow conservation gives the same number of straight decreasing passages.
The arrival axis is fixed at level t by sigma*(-1)^t. Inspecting R/L for the two
possible axes gives

    m_t=f_(t-1)+f_t=A_t+4u_t,
    0<=u_t<=min(f_(t-1),f_t).                               (5)

This uses the chronological class criterion for (3), not just an imposed net
count. It follows that

    f_t<=3f_(t-1)+A_t,     f_(t-1)<=3f_t+A_t.                (6)

The projected finite period has finite support. Outside the extreme wake levels
ell,h, A_t=0; starting beyond all actual visits and propagating (6) inward gives
f_(ell-1)=f_h=0. Hence the trajectory cannot extend transversely past the wake.
This containment is DERIVED for a finite periodic candidate, not assumed for
arbitrary orbits. If O is empty, (6) forces every f_t=0, an impossibility.

For ell<=t<h set

    L_(ell-1)=0,  L_t=3L_(t-1)+A_t,
    R_h=0,        R_t=3R_(t+1)+A_(t+1),
    C_t=min(L_t,R_t).

Then 0<=f_t<=C_t and

    P=2 sum_t f_t <= 2 sum_t C_t.                            (7)

A negative C_t is an impossibility certificate. At a cut, if
sigma*(-1)^t=+1 the upward horizontal crossings contribute +f_t to x-drift;
otherwise the downward horizontal crossings contribute -f_t. Thus

    d_x=sigma sum_t (-1)^t f_t.                              (8)

If C_+,C_- are the sums of C_t over the positive/negative signs in (8), also

    P<=4C_+-2d_x,           P<=4C_-+2d_x.                    (9)

These explicit inequalities often sharpen the integer-clock bound.

### A coarser bound using only wake width and growth

Extremal transverse visits must reverse their projected direction. At an
extreme class their turn is constant; stabilized alternation forces exactly one
R per class. The extremal arrival axes are the same, so W=h-ell is even.
Take c=(ell+h)/2, an integer. Equation (4) implies

    P <= sum_t A_t^+(3^|t-c|-1)
      <= g(3^(W/2)-1),                                     (10)

where sum A_t^+<=g. No period or retreat bound was supplied. Special-width period
bounds and extremal rigidity are already in the literature; (4)--(10) provide
an explicit all-width wake-dependent quantitative bound.

## 9. Arbitrary non-axis drift: two reciprocal moments

Rotate to d=(a_0,-b_0) with a_0,b_0>0. Let k=gcd(a_0,b_0) and
eta=(b_0/k,a_0/k), a positive integer normal. Choose rational r>1 and put

    a=r^eta_x, b=r^eta_y,
    kappa=1-2/(a+1)-2/(b+1)>0.

The uniform choice r=4 works. Write w(q)=r^(eta dot q). Define

    gamma_N=2/(b+1), gamma_E=2/(a+1),
    gamma_S=-2b/(b+1), gamma_W=-2a/(a+1),
    Psi_+(X)=-sigma sum_B chi(q)w(q)+gamma_h*w(p).

Its literal increment is kappa*w(p) in six heading/color cases, and
(kappa+4)*w(p) in S/black and W/white. Substitution of the current-cell toggle
and the outgoing unit displacement proves these eight identities; no theorem
about admissibility is assumed. Half-turning the formula gives

    Psi_-(X)=-sigma sum_B chi(q)/w(q)+gamma_(h+2)/w(p),
    Delta Psi_- >= kappa/w(p).

These one-sided exponential identities are retained from the earlier clock/cone
line, not claimed as entirely new here. The new use is their cancellation over
a full period to determine its possible length from the wake alone.

Because eta dot d=0 and d_x+d_y is even, all weights and chi are invariant under
d. Let the finite input wake budgets be

    A_+ = -sigma sum_(q in O) chi(q) r^(eta dot q),
    A_- = -sigma sum_(q in O) chi(q) r^(-eta dot q).

Both are strictly positive for a realization, and they equal the respective
full-period clock increments. Hence

    kappa sum_i w(q_i)<=A_+,
    kappa sum_i 1/w(q_i)<=A_-.

Cauchy--Schwarz gives the period bound

    P^2 <= A_+ A_- / kappa^2.                               (11)

All data on the right are rational and effectively computed from d,h_0,O.
Integer square root of floor(A_+A_-/kappa^2) gives a correct integer cutoff.
An arbitrary transverse-center shift rescales A_+ and A_- reciprocally, so the
product does not change. Independent representative shifts by Z*d also leave
every quantity unchanged. Axis drift is OUTSIDE this argument: it would give a
zero coordinate in eta and no positive kappa of this form.

## 10. A total inverse-synthesis algorithm

**Theorem 3.** For the inverse inputs of Section 1, existence of a finite-support
periodic realization is decidable uniformly, without a supplied period cutoff.
A positive answer can return an explicit finite seed and its infinite certificate.

Compute (11); for diagonal drift also compute (4),(7),(9), and take the smallest
valid bound. Nonpositive budgets or elementary parity failures give NO. Otherwise
enumerate every binary turn word of length 1 through the bound. Reject wrong
heading or drift, apply Section 2, and require the exact odd-class set O. Construct
the finite seed and verify it with the independent full-field formula. A passing
word gives YES. Exhaustion gives NO. Every word is finite; there are finitely many
of them; Section 2 is effective and exact. Completeness follows from the proved
period cutoff. QED.

The implementation prunes only a repeated physical cell with a nonalternating
next read and paths that cannot reach d within the remaining cutoff. These are
necessary conditions and do not remove a genuine candidate. It uses an explicit
stack, not a bounded-depth language runtime recursion. A supplied positive word
is only a shortcut and is still fully checked. An optional node resource cap
returns INCONCLUSIVE, never NO. Unsupported axis inputs raise an explicit error.
No practical polynomial bound is claimed; the search tree can be enormous.

The explicit integer-clock budget and crossing recurrence supply quantitative
cutoffs for arbitrary diagonal width; reciprocal moments handle every non-axis
drift.

## 11. A direct obstruction to wake-preserving detour insertion

Suppose a realizable word v is obtained from another realizable word u by
inserting nonempty words that return to the same physical position AND heading.
The original steps remain unchanged. Both words have the same non-axis drift.
For each one-sided clock, every retained original step has the same increment:
that increment depends only on its position, heading and R/L letter. Every extra
step has positive increment. Therefore

    A_+(O_v)>A_+(O_u),       A_-(O_v)>A_-(O_u).              (12)

So such an insertion cannot preserve the odd-class wake, or even just its signed
transverse polynomial. For diagonal drift the integer clock gives the stronger
quantitative condition, for every integer c,

    K_c(O_v)-K_c(O_u) >= |v|-|u| > 0.                       (13)

This holds for arbitrarily long inserted detours, not merely the finite search
reported below. It does NOT exclude detours changing wake budgets, replacements
that remove other steps, or arbitrary nonstandard periodic trajectories.

## 12. Verification and publication evidence

`python3 wake_synthesis/reproduce.py` runs the complete standard-wake certificate
and classification replay, together with the general algebraic checks.
`--baseline` additionally repeats the original unpruned cap-168 traversal;
`--search` retains the supplementary finite detour search from version 0.1.0.
The [standard-wake evidence](evidence/standard_wake/) records exact inputs,
completed outputs and scoped controls. Python 3.10+ and C++17 suffice.

The general suite checks integer-clock updates, rational one-sided identities,
projected-flow identities and full-period moments. Its 1,248 positive controls
cover all 104 standard phases, four rotations and powers 1 through 3 with the
corresponding full drifts and wakes. A separate raw enumeration of all 32,766
nonempty words through length 14 cross-checks the known negative example.
The optional detour experiment examines 1,496,144 insertion pairs; the analytic
wake-budget obstruction is proved for arbitrary closed-pose insertions in
Section 11.

## 13. Attribution and version continuity

Jillhewar's finite-word realization criterion, constructive seed, extremal
rigidity and special-width period bounds are explicitly attributed; see the
[primary-source comparison](paper/LITERATURE.md). The integer clock belongs to
[An Ant on the Clock](https://doi.org/10.5281/zenodo.23402379).
The new classification and its exact computations extend the own
[Reading the Wake, version 0.1.0](https://doi.org/10.5281/zenodo.23402422).
The renamed manuscript is prepared as version 0.2.0 of that same preprint.
Published version-0.1.0 delivery files and hashes remain historical records.

## Current consolidation — research 9223766d

The manuscript now includes the [general quadratic wake proof](verification/general_wake_parity/PROOF.md)
and [analytic unit-diagonal proof](verification/unit_diagonal_analytic/PROOF.md).
The former reconstructs odd-used edges from the boundary, derives the one-tour
sign and evaluates it through arithmetic runs; the latter replaces the old local
enumeration premise with forced words and a binary interleaving contradiction.
The [thin parity splice](proof/thin-wake-parity-splice.md) eliminates three
missing-layer cases analytically. Its alternative route inherits the old h=-7
exhaustion and the separate standard-profile classification. The original
five-profile exhaustive route remains the default replay and is unchanged.

[Fresh arithmetic replay](evidence/consolidation-replay.json) includes the general
character, all-parameter excluded family, unit-diagonal regressions and parity
splice, plus preceding mixed/growth modules. It does not re-execute the large
classification. New internal labels in the paper do not alter original proofs,
source manifests or frozen reports.
