# Wake-determined period bounds and inverse synthesis

The current [manuscript](paper/main.tex) develops the given-wake inverse problem.
The [clock companion](../clock_escape/PROOF.md) owns the integer clock and escape
applications; Section 3 recalls that identity for a self-contained period proof.
The finite-word criterion is attributed to Jillhewar. The arguments are analytic,
with exact local algebra and infinite-trace verification in [evidence](evidence/README.md).
Research source: `9c50691`, publication allocation: `c56a76b`.

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

## 3. A global integer clock at the critical base three

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

This result is global: no strip, periodicity or future-live deletion is assumed.
It differs from the earlier rational noncritical clock and the four-direction
critical clock. No arbitrary-half-integer extension is asserted. It can grow
without bound on the plane, so monotonicity alone does not imply HC.

## 4. A diagonal wake pays for every update

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
suffice for the implementation. No assertion that this is the globally optimal
choice among all possible proof methods is needed.

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

## 5. Arbitrary non-axis drift: two reciprocal moments

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

## 6. A total inverse-synthesis algorithm

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

A known finite-width visit bound can also imply finiteness in some fixed
geometries. We do not claim the first conceivable decidability proof of every
related inverse problem. The central new quantitative objects are the explicit
wake budgets, particularly the integer-clock bound and crossing recurrence.

## 7. A direct obstruction to wake-preserving detour insertion

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

## 8. Standard positive control and complete small inverse NO

The canonical 104-letter word is reproduced by literal simulation of the
repository's thirteen-cell standard template, not identified only by its period.
After rotation to d=(2,-2), sigma=+1, its A_t at t=-3,...,7 is

    2,-1,1,-1,1,-1,1,0,1,-1,2.

Equation (7) gives C_t, t=-3,...,6,

    2,5,16,47,142,145,48,16,5,2.

Their sum is 428, so P<=856. Equation (4) at c=2 also gives 856. All 104 phases,
four rotations and powers 1,2,3 pass: with drift/wake scaled for the power, the
bound is 856 times the power. The given standard witness is accepted by both
realization formulas. We did NOT exhaust the 856-depth search or prove that this
wake uniquely determines P104.

For d=(1,-1), h_0=N and O represented by (0,-3),(0,-1),(0,0),(0,1), the derived
bound is 14. The pruned complete search (2226 nodes) returns NO; an independent
raw enumeration of all 32766 nonempty words of length at most 14 agrees. This
small width case is already excluded by known results; it is an implementation
control, not a newly claimed exclusion or an HC negative seed.

## 9. Actual finite checks, experiment and remaining HC gap

The dedicated suite checks 3200 integer-clock complete updates; 6400 rational
one-sided identities; 23650 level identities across 2133 finite geometric words;
4992 full-period moment identities; 1248 standard phase/rotation/power cases;
eight full-period retained-debris controls; the complete small inverse NO;
64 independent representative changes; and malformed/unsupported inputs.
The geometric-word controls may be physically unrealizable and validate only
geometric algebra. Finite tests supplement the analytic universal arguments.

The separate detour search completed 14386 closed-pose, internally alternating
fragments of lengths at most 28, inserted at 104 standard phase boundaries:
1496144 pairs, no passing nonstandard word. These pairs need not be distinct
resulting words. The search does not exhaust all words of any resulting period.
A longer length-36 attempt was stopped before completion and is not a certificate.

The all-period decision is for EACH supplied finite wake with non-axis drift.
There are infinitely many wakes, some possible drifts are axis-parallel, and a
finite seed could hypothetically be nonperiodic. No theorem extracts a bounded
wake from every finite initial state, forces entrance into periodicity, or
identifies all possible periods as standard. A positive nonstandard output would
refute HC; none is supplied here. Taking an infinite union of individually
decidable wake problems is not a total HIGHWAY classifier.

## 10. Attribution and publication positioning

The finite-word criterion and explicit seed are credited to Atharva Jillhewar,
*Finite-Support Periodic Highways of Langton's Ant: Necessary Conditions,
Transverse Exclusions, and Exact Search*, 2026 preprint, DOI
10.21203/rs.3.rs-10516269/v1. The public source and special width-four period
bound N<=14m were inspected at repository revision
`76a7e234e577d992d086c204c3dea00ae72cf10a`. Its other computational exclusions are
not premises of our code or proofs. The earlier own one-sided clock identities
remain credited to `proof/results/cone.md`; general finite-support model and
standard-word data retain their prior evidence boundaries.

The accompanying manuscript presents the wake budgets, (12)--(13), and the
exact cutoff algorithm together, recalling the integer clock from the clock paper. This is a publication candidate, not confirmed priority,
independent peer review or acceptance. It does not manufacture a new paper from
merely reimplementing the existing supplied-word criterion. All quantitative
claims are separated from the much stronger unproved HC conclusion.
