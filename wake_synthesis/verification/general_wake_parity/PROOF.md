# A quadratic wake obstruction for non-axis periodic Langton highways

## Contribution and attribution

This note extends the lifted-port permutation method from special small drifts
to **every non-axis full drift**. Its new ingredients are unique reconstruction
of all odd-used edges from the wake alone, a checker-convention-independent
quadratic wake character, a polynomial-bit-time compressed evaluator, and an
explicit all-scale growth-eight exclusion at drift (3,1).

The stable-class criterion, signed mod-four residues/density bound, and the
axis/two-lane rank-factorization method are due to A. Jillhewar [J]. The project's
mixed-wake formula at drift (2,-2) [M] is an earlier special case, not a new result
of this note. The fact that permutation inversions are quadratic is elementary
and was already used in [J]; the general elimination of the unknown event graph
and the compressed wake-only algorithm are the contributions claimed here.
No source code from those works is copied. This is not global priority assurance.

The theorem is a necessary obstruction, NOT a realization criterion, a decision
of HC for a supplied seed, or an assertion that all growth-eight highways are
impossible.

## 1. Model and theorem

White turns right R, black turns left L; flip the current site and move one edge.
Suppose a nonempty word of length P repeats forever from a complete finite black
field, restores the heading, and has full displacement d=(a,b), ab!=0. Arbitrary
finite preludes and genuinely unread debris are allowed. Do not replace d by its
primitive direction. A half-turn makes a>0. Necessarily a+b is even.

Let O be the finite set of full d-classes containing an odd number of phase
visits. Represent every class canonically by

    pi_d(x,y) = (r, y-b*floor(x/a)),     r=x mod a,  0<=r<a.

Write g=|O|. Define checker parity c(r,y)=(r+y) mod 2. This is well-defined because
a+b is even. Use the convention Q={c=0}, C={c=1}; Q arrivals are vertical and C
arrivals horizontal. This convention will be removed in Lemma 4 below.

### The finite odd-edge graph determined by O

Assume each horizontal and vertical component of Z^2/Zd contains an even number
of O vertices. Vertical components have fixed r=x mod a and coordinate y. Sort
O along each such line and join consecutive pairs by their finite vertical
intervals. Horizontal components have fixed Y=y mod |b|. To express a site (x,y)
on the representative row Y, put

    k=(y-Y)/b,      X=x-k*a.

Sort these X values on each row and join consecutive pairs by horizontal
intervals. Call the union of the interval edges G_d(O). Orient its horizontal
edges from Q to C and its vertical edges from C to Q. Both types are uniquely
directed; parallel quotient edges, when present, retain their edge/port identity.

Order vertices lexicographically by (y,r), and ports negative before positive.
Positive means movement E for a horizontal edge and N for a vertical edge.
Each retained edge has a source key and a target key, both (vertex,port).
Let E_d(O) be the parity of unordered edge pairs whose source and target orders
disagree. Let N_+(O) be the number of positive retained edges and C(O)=|O intersect C|.
Define, with all final values in F_2,

    q_d(O) = E_d(O) + N_+(O) + C(O),                       (1)
    Omega_d(O) = sum_((r,y) in O) floor(y/|b|).             (2)

These definitions do not refer to an unknown period or to visit multiplicities.
The finite graph may be huge; Section 5 evaluates (1) without expanding it.

**Theorem 1 (general wake obstruction).** Every finite-support periodic
realization of non-axis full drift d satisfies

    Omega_d(O)=1,                  q_d(O)=1+a (mod 2).     (3)

There is no period, width, growth, retreat, or seed-size cutoff. Both characters
are independent of representatives, translations, and the checker/heading-axis
convention. In particular no heading or phase origin is an input to the screen.

**Theorem 2 (quadratic structure).** On the F_2 vector space of finite indicators
D having even sums in every horizontal and vertical quotient component, q_d is a
quadratic form: q_d(0)=0 and q_d(A+B)+q_d(A)+q_d(B) is bilinear in A,B. Addition
means symmetric difference, not superposition of physical trajectories.

**Theorem 3 (bit complexity).** Given d and explicit representatives of O in
binary, necessary signed-residue filters followed by (3) can be checked in
polynomial bit time. After the density filter, an implementation needs at most
R=g(a+1)<=g(g/2+1) arithmetic edge runs and O(g^4 log(g+1)) integer arithmetic
operations on numbers of O(B+log(g+1)) bits, where B bounds input coordinate and
drift bit lengths. A passing answer is only NOT_EXCLUDED.

## 2. Why the wake determines every odd-used edge

For a class choose b_v and write phase positions q_i=b_v+k_i*d. Far enough along
it, every phase visit is present and the initial cell is white. Its read times
are nP+i-P*k_i. Thus stable order is by tau_i=i-P*k_i and its letters must be
R,L,R,L,... . This is the necessary part of [J]'s exact criterion. Consequently
R-L at a class is D_v in {0,1}, equal to its visit multiplicity modulo two;
g=sum D_v and heading reset gives 4|g.

The checker/heading-axis invariant assigns vertical incoming headings to one
checker colour and horizontal incoming headings to the other. First work in
Q-vertical convention. Every visit uses exactly one horizontal and one vertical
edge. Modulo two, the horizontal incident-edge boundary and the vertical
incident-edge boundary are therefore BOTH D.

Since b!=0, the horizontal quotient graph is a disjoint union of infinite
paths, not cycles: no nonzero horizontal vector belongs to Zd. Similarly a!=0
makes every vertical component an infinite path. On an infinite path, a finite
edge set with a specified boundary is unique. Its indicator is the cumulative
parity of endpoints, hence consists exactly of intervals pairing consecutive
endpoints. A nonzero finite boundary-free edge set on a line cannot exist.
This proves that actual edge-count parities equal G_d(O), even when the actual
trajectory has arbitrarily many additional even-used edges.

This uniqueness is where the non-axis hypothesis matters. On an axis quotient
one direction has cycles; a complete boundary-free cycle may be added to the
parity data. This note does not treat axis drift as a negative instance.

### Winding parity

Take the seam between x residues a-1 and 0. The actual period crosses this seam
with signed net count one. Modulo two its winding is determined by G_d(O).
A horizontal interval from X_left to X_right crosses the seam
floor(X_right/a)-floor(X_left/a) times modulo two. Summing over paired intervals
is equivalent modulo two to summing floor(X/a) over all endpoints.
For a canonical endpoint (r,y), X=r-a*k, with k=(y-(y mod |b|))/b.
Thus floor(X/a)=-k, whose parity equals floor(y/|b|). This proves (2)--(3)'s
winding condition. Equivalently one may use
floor(x/a)+floor(y/|b|) on arbitrary representatives. Adding d changes that
weight by 1+sign(b), which is even.

## 3. Eliminating visit ranks from the one-tour sign

This section gives the full factorization so that the generalization is not an
appeal to extrapolation from small drifts.

At a vertex v, order m visits by stable rank k=0,...,m-1. Let alpha_k and beta_k
be incoming and outgoing positive-port bits; A and B are their numbers of ones,
and p_v=(A+B) mod 2. At Q, L means alpha!=beta; at C, L means alpha=beta.
For any binary list alpha,

    inv(alpha)=A(m-1)+sum_k k*alpha_k+binom(A,2) (mod 2).   (4)

Each one at k sees m-1-k later positions, minus its later ones; summing the
latter counts binom(A,2). This proves (4) at every length.

Put K=sum_(L visits) stable_rank mod 2. Applying (4) to both port lists gives
local K contributions, apart from inversions and positive-edge binomials,

    Q: p_v(m-1),
    C: p_v(m-1)+binom(m,2).

At Q, m mod 2=D_v, so the correction is p_v(D_v+1). At C, because R means unequal
bits, D_v=2(A+B)-4*sum alpha_k beta_k-m. Thus m=2p_v-D_v modulo four, and the
correction is D_v(p_v+1) for D_v=0 or 1. Summed over all vertices, the binomials
cancel: every positive directed edge has the same multiplicity at source and
target. Therefore, writing I for the sum of all incoming/outgoing port-list
inversions,

    K=I+L,      L=sum_Q p_v(D_v+1)+sum_C D_v(p_v+1).       (5)

For a fixed directed quotient edge of voltage nu, target stable time equals
source stable time plus 1-P*nu. The same constant is used for every occurrence,
including the period seam. Edge occurrences therefore match first-to-first.
Sorting outgoing ports, following edge blocks, and unsorting incoming ports
factors the phase successor. It is a SINGLE even-length P-cycle, hence has odd
permutation sign. Consequently

    I+E=1,                       K=1+E+L.                (6)

Here E depends only on edge-count parities: reversing two blocks of sizes u,v
contributes uv modulo two. All even-used edges can therefore be removed in this
calculation, and E is exactly E_d(O) constructed above.

**Lemma 4 (endpoint cancellation and convention independence).** For G_d(O),

    sum_(v in O) p_v = 0 (mod 2),                         (7)
    L=N_+(O)+C(O) (mod 2).

For one horizontal paired interval, positive incidence at its two endpoints
has parity 1+c(left)+c(right). The same formula holds for a vertical interval.
There are g/2 intervals of each type; each endpoint checker bit occurs twice.
Their sum is g=0 modulo two. Thus (7) holds. Also sum_Q p_v=N_+: each positive
edge is incident to exactly one Q vertex. Expanding (5) proves the second formula.

Changing the total vertex order does not change E: swapping v,w contributes
out(v)out(w)+in(v)in(w)=D_vD_w+D_vD_w=0 modulo two. Reversing the checker
convention reverses every directed edge and complements every port bit.
Inversion sign is unchanged by inversion of a permutation. The extra port-order
reversals contribute sum_v (1+D_v)p_v=0, by (7) and sum_v p_v=0. Moreover G has
an even number of edges (sum of outgoing parities is g), so N_+ and g-N_+ have
the same parity. Swapping Q,C replaces C by g-C, also unchanged modulo two.
Hence q_d is convention independent. A translation relabels vertices, and
possibly exchanges checker conventions, proving translation and phase invariance.
The winding is unchanged by a seam move, since all fibre populations are even.

For an actual stable class list each L has odd rank, so
K=#L=(P-g)/2 modulo two. Exactly P/2 moves are horizontal, and their net x
increment is a; hence P/2=a modulo two. Since 4|g, K=a modulo two.
Equations (1), (5)--(7) now give q_d=1+a. This completes Theorem 1.

For Theorem 2, D -> G_d(D) is linear by uniqueness of the finite boundary
antiderivative. E is a quadratic polynomial in those edge indicators; N_+ and
C are linear. This proves the asserted quadratic structure without a finite-width
hypothesis. It does not make physical dynamics linear.

## 4. Relation to earlier two-lane results

For d=(2,-2), in Q-even normalization let V count Q odd classes and J count
ordered pairs (q,c) in O_Q x O_C with t(q)<t(c), t=x+y. Under the signed residues,
the earlier identity [M] gives

    q_(2,-2)(O)=J+V/2 (mod 2).

Thus Theorem 1 recovers J+V/2=1. More generally, on every finite closed two-lane
parity input the identity is q=J+binom(g,2)+q_0, with q_0 counting Q classes in
lane zero. The supplement checks every one of the 8,192 closed masks in an
eight-layer/two-lane window against that formula. These are regressions; [M]'s
unbounded identity is credited, not claimed newly here.

Our extension does not need a two-lane reduction, a prescribed odd-class order
profile, a width bound, or period-dependent multiplicities. It also applies to
non-diagonal drifts such as (3,1) and (4,2).

## 5. Computing the character without traversing huge gaps

[J]'s signed residue theorem states that each x residue modulo |a| and each y
residue modulo |b| has signed odd-class sum 2 modulo four, with sign (-1)^(x+y).
In particular g>=2 max(|a|,|b|). First check positive g divisible by four and
this density bound, rejecting violations. It limits both drift magnitudes to
g/2 before allocating any residue-sized data. Checking the signed sums also
ensures the even fibre populations needed above.

Use canonical vertices (r,y), sorted by (y,r). An **edge run** contains n edges
whose source and target keys have the form

    source_i=(s_y+h*i, s_x, p),
    target_i=(t_y+h*i, t_x, p),       0<=i<n, h>0.          (8)

One vertical interval splits by bottom-site parity into at most two runs of
step 2. A horizontal interval on representative row Y splits its left endpoint
X=r+a*k by r, and, if a is odd, by k mod 2. Its canonical heights change by -b
per k; orienting the index so height increases gives step |b| or 2|b| and fixed
ports. This gives at most 2a runs per horizontal interval. Therefore

    R<=g(a+1)<=g(g/2+1).

Intervals and runs have disjoint edges. Within a run, source and target orders
are the same, so there are no inversions. Between runs A,B put
z=s_A+h_A*i-s_B-h_B*j and delta=(t_A-s_A)-(t_B-s_B).
Let s=0 if (x_A,p_A)<(x_B,p_B), otherwise s=-1. Similarly let
u=-delta+[0 if (target_x_A,p_A)<(target_x_B,p_B), otherwise -1].
Source and target orders disagree exactly when

    min(s,u)<z<=max(s,u).                                 (9)

Thus two calls counting z<=bound suffice for a run pair.

For lengths n,m, steps u,v, and T=bound-s_A+s_B, count
u*i-v*j<=T, 0<=i<n, 0<=j<m. Put

    l=clip(ceil(-T/v),0,m),
    h=clip(ceil((u*n-T)/v),0,m).

Then the exact pair count is

    (m-h)*n + (h-l)
       + sum_(j=0)^(h-l-1) floor((v*j+T+v*l)/u).          (10)

Below l there are no eligible i; above h all n are eligible; the middle has
floor((T+v*j)/u)+1. This proves (10), including negative coordinates.

The floor sum is evaluated by Euclidean lattice transposition. For
S(n,m,a,b)=sum_(i=0)^(n-1) floor((a*i+b)/m), first remove quotient parts of a,b;
these contribute floor(a/m)n(n-1)/2+floor(b/m)n. Now 0<=a,b<m. If a*n+b<m the
remainder is zero. Otherwise, with n'=floor((a*n+b)/m), b'=(a*n+b) mod m,

    S(n,m,a,b)=S(n',a,m,b').                              (11)

To verify (11), count the lattice points under a*i+b at each positive integer
height. There are n-ceil((m*j-b)/a) eligible i at height j. Reindex j from n'
downwards, using m*n'-b=a*n-b'; the resulting floors are precisely the right
side. Euclidean reduction terminates in O(log(max(a,m)+1)) stages.
The implementation handles arbitrary signs by exact divmod before this step.

Run pair counts have polynomial bit length even when each run has 10^100 edges.
N_+ is a sum of run lengths; C and Omega are computed from O. Equations
(8)--(11), the bound on R, and the density prefilter prove Theorem 3. Numerical
optimization, simulation deadlines, and an unproved search cutoff play no role.

## 6. A new all-scale growth-eight excluded family

Set d=(3,1) and

    O_*={(0,1),(0,3),(1,-2),(1,-1),(1,0),(1,2),(2,0),(2,2)}.

For every integer n>=1, put lambda=12n+1 and let O_n consist of the full classes
of lambda*q, q in O_*. These eight classes remain distinct. Their canonical
coordinates are

    (r, (12y-4r)n+y),                (r,y) in O_*.

Their three signed x-fibre sums are (-2,-2,2), and the sole y-fibre sum is -2;
all are 2 modulo four. They have g=8 and pass the density bound.
Their winding is sum canonical_y=28n+5=1 modulo two. Thus none of these
necessary linear tests excludes them.

Nevertheless the exact run arithmetic gives, in the vertex order (y,r),

    number of odd edges        = 192n+16,
    positive edges             = 96n+9,
    edge-pair inversions       = 400n+19,
    C odd classes              = 5.

It follows that q_d(O_n)=496n+33=1 modulo two, while Theorem 1 requires
1+a=0 modulo two. **Every O_n is impossible at every period.** The transverse
invariant T(x,y)=3y-x has span 16(12n+1), so the excluded family has unbounded
width. No actual initial seed is claimed to realize an excluded or passing wake.

### Exact all-n calculation, not interpolation

`family.py` derives the 32 affine runs directly. On each horizontal pair with
unscaled endpoint coordinates L<R in the representative row, the k bounds for
left residue r are

    k_min=4L*n+ceil((L-r)/3),
    k_max=4R*n+floor((R-1-r)/3).

Splitting k parity yields affine positive run lengths for every n>=1.
The vertical bounds are the canonical affine y coordinates displayed above.
All runs have step 2. For a possible inversion difference z in (9), put
k=(z-s_A+s_B)/2; if parity is wrong there is no contribution. Otherwise the
pair count is exactly

    max(0, min(n_B,n_A-k)-max(0,-k)).                     (12)

Every term is affine in n. Each choice of a minimum or maximum is certified for
ALL n>=1: A*n+B is nonnegative on that domain exactly when A>=0 and A+B>=0.
If two affine expressions cannot be uniformly ordered, the checker fails;
it never extrapolates a branch from sample values. Summing all 496 run pairs,
with 288 parity-compatible terms, gives 400n+19. The supplemental manuscript
table lists every affine run, making this a finite transparent integer identity.
The same symbolic calculation gives 96n+9 and 192n+16. Numerical n=1,2,17,10^100
checks are only additional convention controls, not the proof of the family.

For comparison, the wake

    {(0,1),(0,5),(1,-4),(1,-2),(1,5),(1,6),(2,-4),(2,4)}

has the same signed fibre populations and winding, but q=0 and is NOT_EXCLUDED.
Its realizability is unknown here. This shows strict strengthening of the stated
signed-residue/density/winding screens, not independence from every conceivable
arithmetic invariant. The unscaled O_* is also excluded: direct counts are
16 odd edges, 9 positive edges, 23 inversions and C=5.

## 7. Evidence and HC boundary

The general theorem and complexity result are mathematical proofs, not bounded
experiments. The family uses exact affine arithmetic valid on the entire
parameter domain. The retained regression suite separately checks:

- exact floor sums and run-pair counts against literal enumeration;
- individual-edge reconstruction versus compressed runs for eight drift types;
- vertex-order and checker-convention independence, and quadratic polarization;
- every closed mask in an eight-layer/two-lane window against [M];
- an independently written C++ literal-word port factorization for all binary
  words of even length at most 20, with undefined-behavior sanitizer enabled;
- all 104 P104 phases, four rotations, and powers one through four, using their
  FULL displacements, plus invalid inputs and huge representatives.

Exact counts and source hashes belong to `evidence/full_replay.json`. Neither
regressions nor a manuscript constitute independent human review or a Lean proof.

For HC, the result concerns periodic endpoints: it removes another set of
possible nonstandard highways without period or transverse-gap bounds. It does
not establish that arbitrary finite seeds become periodic, that a passing wake
is realizable, that growth eight is impossible in all geometries, or that
nonperiodic escape is excluded. Its role is a cheap, rigorous prefilter before
exact inverse synthesis and a source of full-family obstructions.

## References and baseline

[J] A. Jillhewar, *Finite-Support Periodic Highways of Langton's Ant: Necessary
Conditions, Transverse Exclusions, and Exact Search*, 2026. Inspected repository:
https://github.com/Atharva12456/langtons-ant-highway , revision
`76a7e234e577d992d086c204c3dea00ae72cf10a`; `paper/main.tex`.
Stable criterion, signed residues and the rank/port method retain this attribution.

[M] H. Ke, *Mixed-wake interleaving parity for full drift (2,-2)*, project research
proof in `wake_synthesis/proof/mixed-wake-interleaving.md`, inspected at
`kehao95/langtons-ant-core@c7bb906ed94d1345694ce0372fb69fd08a6a0a51`.

The unit-diagonal analytic exclusion is a distinct existing result and is NOT a
premise of this theorem.
