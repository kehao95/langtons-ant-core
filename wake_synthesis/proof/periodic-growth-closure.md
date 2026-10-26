# Closing the periodic-growth proof: residues, ranks, and small drifts

This note supplies the proofs behind the previously external dependencies of the
claim that a finite-support periodic highway has growth at least eight. It also
extracts two all-growth restrictions from those proofs. The unit-diagonal theorem
is accompanied by its original generator, independently written verifier and
controls. This is a complete written proof with finite exact checks, NOT a Lean
formalization, independent peer review, priority certification, or a solution of
HC. In particular no theorem here proves eventual periodicity of arbitrary seeds.

## Attribution and proof dependencies

A. Jillhewar, *Finite-Support Periodic Highways of Langton's Ant: Necessary
Conditions, Transverse Exclusions, and Exact Search*, 2026, is the source of the
stable-class criterion, signed mod-four residue theorem, axis rank factorization,
and two-lane checker-pure rank identity used below. The exact source inspected is
`Atharva12456/langtons-ant-highway@76a7e234e577d992d086c204c3dea00ae72cf10a`,
`paper/main.tex`, Git blob `12cd05962e071c08f3e900c624cd6438452fa847`.
The original paper/prose is CC BY 4.0. This is an attributed rewritten proof,
not a claim to have discovered those results. The two MIT audit scripts in
`third_party/` are preserved byte-for-byte and carry the original license.

The reconstruction supplies explicit coordinate formulas instead
of an implicit mod-four cocycle; a complete dependency chain avoiding the separate
clean-translator theorem; an all-growth axis divisibility consequence; the
all-growth version of the checker-pure obstruction; and the combination with the
unit-diagonal certificate. The two all-growth consequences are elementary
strengthenings of the cited arguments, not claims of an unrelated new method.
The predecessor explicitly established the growth-four cases and its research
note additionally treated checker-pure growth eight. Its authorship is retained.

## 1. Model and main statements

A state is `(B,p,h)` with finite `B subset Z^2` and heading `h in {N,E,S,W}`.
At a white site turn R, at a black site turn L, flip the site, then move one edge.
A nonempty word `w` of length `P` is a periodic realization if `w^omega` is the
whole turn stream from some such state, `h_P=h_0`, and its full displacement is
`d=(a,b) != (0,0)`. Stationary debris and a growing wake are allowed. Define

    g = #R - #L = |B_(t+P)| - |B_t|.

The equality applies at corresponding period phases. Every finite-time black
field remains finite. The drift is NOT replaced by its primitive direction.

**Theorem A (closed growth lower bound).** Every finite-support periodic
realization has `g in 4 Z`, `g >= 8`, and `g >= 2 max(|a|,|b|)`.

**Theorem B (two-cell axis arithmetic, all growth).** If the full drift is in
`{(2,0),(-2,0),(0,2),(0,-2)}`, then

    P = 4 (mod 8),       g = 0 (mod 8).

No bound on period, width, growth or seed size is assumed. In particular growth
12 is impossible for these full axis drifts. This does not exclude growth 8 or
larger multiples of eight, and it says nothing identical about a four-cell drift.

**Theorem C (two-cell diagonal checker mixing, all growth).** For full drift in
`{(2,2),(2,-2),(-2,2),(-2,-2)}`, the odd translation classes of the wake cannot all
have the same checkerboard parity. Both parities occur; indeed each occurs an
even, positive number of times. No period, width or growth cutoff is supplied.

The results apply unchanged to a periodic suffix following any finite prelude.
They classify necessary features of periodic endpoints, not arbitrary transients.

## 2. Finite support and explicit signed residues

### 2.1 Stable class balances

Fix one phase origin. Let `q_i`, `0<=i<P`, be its read positions. In a class
modulo the FULL vector d write `q_i=c+k_i d`. Visits to `c+n d` occur at times
`nP+i-Pk_i` once `n>=k_i`. For all sufficiently large n every phase is present
and the initial color is white, since the seed is finite. Thus the stable order
is decreasing `k_i`, then increasing i, and its letters are `R,L,R,L,...`.

The signed excess in a class is exactly 0 or 1; it is 1 precisely for odd
multiplicity. Let O be these odd classes, represented by one lattice site each.
Then `g=|O|>=0`. Heading restoration gives `g=0 (mod 4)`. Since P and g have the
same parity, P is even, and `a+b` is even. Hence checker parity
`chi(x,y)=(-1)^(x+y)` is invariant under translation by d.

This argument is needed only as a necessary condition for all exclusions here.
It makes no assertion that an arbitrary assigned collection of counts is a
physical trajectory. The full known criterion also constructs a finite seed,
but its sufficiency is not a dependency of the negative theorems.

### 2.2 Explicit potential, including its gauge choice

Take any function `f:Z -> Z/4Z`. Choose `S(0)=0` and extend to ALL integers by

    S(x+1)-S(x)=f(x)+f(x+1).

At `(x,y)`, abbreviate `c=chi(x,y)`. Set, in `Z/4Z`,

    F_N=-c S(x),          F_E=c(S(x)-f(x)),
    F_S=-c(S(x)+2f(x)),   F_W=c(S(x)+f(x)).                 (1)

Then the FULL-state quantity

    I_f(B,p,h)=sum_((x,y) in B) chi(x,y) f(x) + F_h(p)       (2)

is conserved. The finite sum includes every black site.

Here is a direct check, without importing cocycle existence. Put delta=+1 for
R and -1 for L. A step changes the field part by `delta*c*f(x)`. After the step
`c'=-c`. For an E move use `S'=S+f(x)+f(x+1)`; for W use
`S'=S-f(x-1)-f(x)`; for N/S use `S'=S`. Substituting (1) gives the following
values of `F_(h+delta)(p+e_(h+delta))-F_h(p)+delta*c*f(x)`:

| heading | R | L |
|---|---:|---:|
| N | 0 | 0 |
| E | `4 c f(x)` | 0 |
| S | `4 c f(x)` | 0 |
| W | 0 | 0 |

All vanish modulo four. Equation (1), not a floating-point fit, proves (2).
The local table is also exhaustively checked over `S,f(x-1),f(x),f(x+1)` modulo
four, both checker signs, all headings and colors.

### 2.3 Residue monodromy

Suppose `a!=0` and make f periodic with period `|a|`. Then

    S(x+a)-S(x)=2 sign(a) sum_(r mod |a|) f(r).

Checker parity and f are unchanged by d. Each of the four heading corrections
therefore changes by `2 sum_r f(r)` modulo four. Over one complete period, the
field change in (2) is `sum_(q in O) chi(q)f(q_x)`: the weight is constant on a
full d-class, and its signed excess is the indicator of O. Conservation gives

    sum_(q in O) chi(q) f(q_x) + 2 sum_r f(r) = 0 (mod 4).

Choose residue indicator functions. For each x residue r,

    sum_(q in O, q_x=r mod |a|) chi(q) = 2 (mod 4).          (3)

If `a=0`, the complete endpoint correction is unchanged, and arbitrary
single-column indicator functions give

    sum_(q in O, q_x=c) chi(q) = 0 (mod 4).                (4)

Quarter-turn the whole calculation to obtain the analogous y statements.
Representative changes `q -> q+kd` alter none of these data.

A sum of m signs congruent to two modulo four needs at least two terms. Thus
`g>=2|a|` for `a!=0`, and `g>=2|b|` for `b!=0`. Since d is nonzero, g is positive.
This proves `g in 4Z_(>0)` and the density bound WITHOUT separately assuming the
external no-clean-translator or even-winding theorem. This closes that otherwise
unnecessary dependency.

## 3. Rank factorization for full drift (2,0)

We give the complete port-permutation proof of the external axis identity,
then retain its consequences for arbitrary g rather than only g=4.

Choose a vertical incoming phase and translate it to the origin; let it be N.
Such a phase exists: vertical moves alternate with horizontal moves and their
net vertical sum is zero. This fixes checker/axis sector sigma=+1. Write P=2M.
Each horizontal-vertical pair is described by its horizontal sign u_j and
outgoing vertical sign v_j. The cyclic incoming vertical signs are the same
list shifted by one. There are M horizontal moves of net sum 2, so M is even.

On row y the quotient modulo `(2,0)` has exactly one vertical-arrival class
Q_y and one horizontal-arrival class C_y. Each has two negative/positive ports.
Positive incoming/outgoing mean N/E at Q and E/N at C. Order visits by stable
rank k. Let alpha_k,beta_k be these incoming/outgoing bits. At Q, L means the
bits differ; at C, L means they agree. Define

    K=sum_(L events) stable_rank(event) (mod 2).

For a binary word alpha of length m with A ones, its inversion parity is

    inv(alpha)=A(m-1)+sum_k k alpha_k+binom(A,2) (mod 2).     (5)

Indeed, each one at k contributes `m-1-k` later positions, of which its later
ones must be subtracted; their total is binom(A,2). This proves (5) for arbitrary
word length, without a finite enumeration hypothesis.

Apply (5) to both port lists. Positive-edge binomial terms cancel between source
and target. Put h_y for the number of horizontal traversals in row y, n_y for
north edges out of C_y, and s_y for south edges out of C_y. Vertical balance
and alternating motion give

    s_(y+1)=n_y,        h_y=n_(y-1)+n_y.

The linear terms of Q_y and C_y sum to `h_y(h_y-1)`, an even number. It follows
that, with `J=sum_v(inv(alpha_v)+inv(beta_v))`,

    K=J+sum_y binom(h_y,2) (mod 2).                        (6)

Stable order on every fixed directed quotient edge is preserved, including
the period seam: its target stable time equals source stable time plus
`1-P*voltage(edge)`. The phase successor is a single even-length cycle of
permutation sign 1. Sorting outgoing ports, following edges and unsorting
incoming ports therefore gives `J+E=1`, where E is the edge-block sign.

Order quotient vertices by y and then Q before C, negative port first. The
source blocks in row y are `[W_y,E_y,S_y,N_y]`; the target blocks are
`[S_(y+1),N_(y-1),W_y,E_y]`. The reversed block pairs are exactly a horizontal
block on row y versus `S_y,S_(y+1)`, and `N_y` versus `S_(y+1),S_(y+2)`.
Consequently

    E=sum_y h_y(s_y+s_(y+1))+n_y(s_(y+1)+s_(y+2)) (mod 2)
     =sum_y n_y+sum_y n_y n_(y+1) (mod 2).

All sums have finite support because one period has finitely many events.
Also `sum_y binom(h_y,2)=sum_y n_y n_(y+1) (mod 2)`, by expanding the binomial
and canceling its repeated terms. Finally `M=sum h_y=2 sum n_y`. Substitution
in (6) proves the purely kinematic identity

    K=1+P/4 (mod 2).                                      (7)

The 2-cell circumference is essential. Equation (7) is not asserted for a
larger axis displacement.

### 3.1 All-growth axis theorem

For an ACTUAL finite-support periodic realization, every L event has odd stable
rank. Hence `K=#L=(P-g)/2 (mod 2)`. Both P and g are divisible by four; K=0, so
(7) forces

    P=4 (mod 8).                                          (8)

The exact-row version of (4) has only two possible odd classes on each row,
with opposite checker signs. Its signed sum lies in `{-1,0,1}` and is zero
modulo four; the two classes are therefore either both odd or both even.
Thus exactly `g/2` odd classes are Q classes. Over the M pair-first turns,
`sum_j u_j v_(j-1)=g/2`. Moreover `sum u_j=2` and `sum v_(j-1)=0`, whence

    M+2+g/2 = sum_j (1+u_j)(1+v_(j-1)) = 0 (mod 4).         (9)

Each summand is 0 or 4. Equations (8)-(9) imply `g=0 (mod 8)`.
This proves Theorem B. In particular g=4 is impossible, recovering the cited
axis growth-four exclusion with its full proof inside the present package.
Quarter-turns cover the other three 2-cell axis directions.

## 4. Checker-pure diagonal wakes: the all-growth obstruction

Normalize d=(2,-2), choose a vertical incoming phase at the origin, and use
sigma=+1. Let Q be even-t vertical-arrival classes and C odd-t horizontal-arrival
classes, with `t=x+y`, lane `r=x mod 2`. At a transverse extreme, arrival and
departure sides are fixed. Stable alternation then forces one R per visited
class. At the maximum an R joins E to S, and at the minimum it joins W to N;
these extremes are horizontal-arrival C classes. Thus if O is checker-pure,
it must be contained in C. This also handles a putative even-checker pure wake:
a coordinate/phase normalization preserving the rule makes the same conclusion.

We reproduce the two-lane rank lemma in exactly the case now required. Write
D_v=R-L in a class, so D_v is its 0/1 odd indicator. Let `p_v=sum alpha+sum beta`
modulo two for positive ports N/E at Q, E/N at C. Eliminating the rank sums
using (5), the local non-inversion corrections are

    p_v(D_v+1) at Q,      D_v(p_v+1) at C.                 (10)

For Q use `D_v=m_v-2p_v (mod 4)`. For C use
`D_v=2p_v-m_v (mod 4)`, including the extra `binom(m_v,2)` from equal bits.
The binomial terms for directed edges again cancel globally. Thus

    K=1+E+L (mod 2),                                      (11)

where L is the sum of (10), and E is the edge-block sign.

Write w,e for the mod-two W/E outgoing counts at Q_(t,r), and s,n for the S/N
outgoing counts at C_(j,r). Incoming and outgoing balance gives

    w_(t,r)+e_(t,r)=s_(t+1,r)+n_(t-1,r),
    s_(j,r)+n_(j,r)=w_(j+1,1-r)+e_(j-1,1-r).              (12)

Since D_Q=0, w=e=:a. Hence `s_(j,r)=n_(j-2,r)`. Substituting in (12),
`a_(t,r)+n_(t-1,1-r)` is independent of t; finite support makes it zero.
Therefore `a_(t,r)=n_(t-1,1-r)` and

    D_(j,r)=n_(j-2,r)+n_(j,r) (mod 2).

At C, p=D, so its correction in (10) vanishes. The two Q corrections on each
level are identical and cancel. Thus L=0.

The odd directed blocks are the disjoint union, over `n_(j,r)=1`, of gadgets

    G_(j,r)={N_(j,r), S_(j+2,r), W_(j+1,1-r), E_(j+1,1-r)}.

The source order of one gadget is `[N,W,E,S]`, target order `[W,S,N,E]`; its
sign is odd. The cross-inversion parity of two distinct gadgets is 1 precisely
when they have the same lane and their levels differ by two. Here is the whole
interaction table; rows with negative separation follow by symmetry:

| separation | same lane | opposite lanes |
|---|---:|---:|
| 0 | identical gadget, not a pair | 0 |
| 2 | 1 | 0 |
| 4 | 0 | 0 |
| >=6, even | 0 | 0 |

For separation at least six their source AND target ranges are disjoint in the
same order. The other entries follow by the four displayed block coordinates;
the code checks them using separately reconstructed geometric endpoints.
Thus, for arbitrary finite binary chains,

    E=sum_(j,r) n_(j,r)+n_(j,r)n_(j+2,r) (mod 2)
     =sum_r number_of_one_runs(lane r) (mod 2).

The boundary of each run supplies two odd C classes. If o_r counts them in lane r,

    E+L=sum_r binom(o_r,2) (mod 2).                        (13)

Equations (3) for the two x residues, and checker purity, imply
`o_0=o_1=2 (mod 4)`. Thus both binomials in (13) are odd, E+L=0 and (11) gives
K=1. But the horizontal displacement two forces P divisible by four; g is also
divisible by four. Stable alternation gives `K=#L=(P-g)/2=0 (mod 2)`, a
contradiction. This proves that O is not checker-pure for ANY g.

Summing the two residue congruences gives `number_plus-number_minus=0 (mod 4)`.
Together with `number_plus+number_minus=g=0 (mod 4)`, each count is even. Since
neither vanishes, each is at least two. This proves Theorem C and, in particular,
the externally stated checker-pure growth-four and growth-eight cases.

## 5. Unit-diagonal certificate and global closure

The separate self-contained proof in `unit/PROOF.md` establishes that no
finite-support periodic trace has FULL displacement `(1,-1)`. The three-layer
argument has no period, width or growth cutoff: it starts from a necessarily
singleton extreme class, enumerates every locally feasible stable arrival list,
and rejects by a fixed premature cycle, a universally positive affine
chronological circuit, or a same-cell same-color contradiction. All 12,884 local
branches are regenerated; the independently written verifier checks each
rejection and coverage. The maximal 38 constructed events are a derived local
bound, NOT an upper bound on the unknown period. Four rotations cover all unit
diagonal signs. No external growth-four theorem is used in this certificate.

Now suppose g<8. Section 2 gives positive growth divisible by four, hence g=4,
and the density bound gives `|a|,|b|<=2`. Checker parity gives a+b even. The 12
nonzero possibilities split into precisely three four-element orbits:

- 2-cell axis drifts: excluded by Section 3;
- 2-cell diagonal drifts: (3) forces O to be checker-pure, contradicting Section 4;
- unit diagonal drifts: excluded by the three-layer certificate.

For the middle assertion let n_rs be the number of odd classes with x parity r
and y parity s. At g=4 each x fiber and each y fiber has exactly two terms by
the density proof. The two terms in each fiber must have the same checker sign
in order to sum to two modulo four. Therefore

    (n_rs) = [[2,0],[0,2]]  or [[0,2],[2,0]],

and all four odd classes have one checker sign. All three orbits are impossible,
which proves Theorem A. There is now no unexpanded external theorem in this
logical chain: attribution is external, but the needed arguments appear here.
This is not a claim that finite computation has replaced the general algebraic
proofs, nor that the proof has been mechanically formalized end-to-end.

## 6. Further precise reduction of the growth-eight question

At d=(2,-2), g=8, equations (3) constrain the 2x2 residue-count matrix
`[[a,b],[c,d]]` by

    a-b=d-c=a-c=d-b=2 (mod 4),      a+b+c+d=8.

There are ten nonnegative integer matrices satisfying these relations. Four
are checker-pure and are excluded by Section 4. The six remaining are exactly

    [[0,2],[2,4]], [[1,3],[3,1]], [[2,0],[4,2]],
    [[2,4],[0,2]], [[3,1],[1,3]], [[4,2],[2,0]].

This small arithmetic classification is exhaustive, but these six matrices are
NOT claimed realized, nor are they six finite seeds. Transverse spacing, visit
counts, chronological order and period remain unrestricted. They are exact
necessary residue types for the next search, not a solution of growth eight.

For general g=8, density and parity, plus the unit-diagonal theorem, leave the
unordered absolute displacement types

    (2,0),(4,0),(2,2),(4,2),(4,4),(3,1),(3,3).

This list groups magnitudes only; reflections are NOT used as symmetries of
the literal LR rule. Actual signed ordered vectors must still be considered.
The conclusion is a reduced target, not an all-drift g=8 exclusion or g>=12.

## 7. Exact replay and trust boundary

Run `python reproduce.py`. It checks source/provenance hashes, regenerates the
unit certificate in a temporary directory, runs its independent verifier and
controls, reruns both unchanged MIT external audit scripts, and compares the
new independently written checks against the frozen reports. Every command
must succeed. No network, optimization package, SAT solver, C++ compiler or
external mathematical theorem server is needed to replay this package.

The external scripts themselves say `bounded_evidence_not_proof`; this is
preserved. The unbounded argument is Sections 2-5, not their bounded outputs.
The fresh independent checks include the complete 4096-case local mod-four
kernel, 130560 monodromy cases, 6144 literal full-field updates, all 1664 standard
phase/rotation/power controls, 2123 axis words, 4096 finite two-lane chains,
and exact low-growth residue arithmetic. These check algebra/sign conventions;
only the symbolic derivation proves its unbounded parameter range.

This note neither changes the existing HC model nor discards residual black
sites. It does not establish that arbitrary seeds eventually become periodic,
that all allowed growth-eight cases are impossible, or that g=8 is attainable.
No changes are made to existing public preprints or DOI records.
