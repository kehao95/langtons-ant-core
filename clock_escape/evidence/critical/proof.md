# Critical potentials and sharper first-exit bounds

The local identities and finite-range arguments give quantitative escape bounds.
Exact finite checks accompany the analytic proof.

## 1. Statements

Let S(N,H) be the largest first-exit time from N columns and H rows, starting
at any internal cell and heading, with any initial colouring. The exit-producing
update is counted. Arbitrary exterior black cells are allowed; none is read
before this first exit. The original ant still lives on the infinite plane.

**Theorem A (critical global potential).** For positive real a,b>1 with
(a-1)(b-1)=4, the explicit finite-support potential below has a strictly positive
increment on each literal update. At a=b=3, when both centre coordinates are
integers or both are half-integers, each four-update segment increases it by
at least 16/3. This bound is attained for an appropriate centred unit-square
four-turn segment.

**Theorem B (square bound).** For every n>=1,

    R_n = 3^(1-n)(3^n-1)^2 + 4(3^(n-1)-3^(1-n)),
    S(n,n) <= 4 floor(3 R_n/16)+4 <= (13/4) 3^n+4.

Thus the former internal bound 8n3^n+1 improves to O(3^n).

**Theorem C (rectangle bound).** For every pair of positive integers N,H,

    S(N,H) <= floor((9/2)(NH+16)(4N+1)^floor(H/2))+3.

In particular S(N,H)=O_H(N^(floor(H/2)+1)). These are upper bounds, not exact
worst times. The constants and the degree are not claimed optimal. Quarter-turn
symmetry also permits exchanging N and H and taking the smaller bound.

For comparison, Etse's published MFCS 2026 Theorem 5 gives (n+1)! for squares.
Theorem 12 gives degrees H-1 for even H and H-2 for odd H at fixed height
(the same formulas appear as Theorem 14 of arXiv v1). Our rectangle exponent is
strictly smaller for every H>=6; no improvement of the known linear height-2/3
bounds is claimed. The published version and its page 49:15 were inspected,
rather than using only the looser bound in its abstract.

## 2. Literal state and the critical potential

A state is X=(B,p,h), with complete finite B subset Z^2 and h in {N,E,S,W}.
White turns right, black turns left, then the current cell is toggled and the
head moves by one unit. Let F denote this map. Put

    chi(x,y)=(-1)^(x+y),
    sigma(X)=chi(p) for h=N,S, and -chi(p) for h=E,W.

Both head-location parity and heading axis change every update, so sigma is
invariant. A centre c=(c_x,c_y) is fixed once for the whole trajectory. Define

    U(q)=a^(q_x-c_x), V(q)=b^(q_y-c_y),
    Phi(X)=-sigma(X) sum_(q in B) chi(q)(U(q)-1/U(q))(V(q)-1/V(q))
           + G_h(U(p),V(p)),

where

    G_N=2/(b+1) (U+1/U)(V-b/V),
    G_E=2/(a+1) (U-a/U)(V+1/V),
    G_S=2/(b+1) (U+1/U)(1/V-bV),
    G_W=2/(a+1) (1/U-aU)(V+1/V).

All sums retain the full finite field. With rational parameters and an integer
centre Phi is exactly rational. The square half-centre case also has a rational
expression given below. Nonperiodic, coordinate-dependent weights are essential;
this is not a finite-range translation-invariant pattern-sum rank.

### Eight-case identity

For U=U(p), V=V(p), direct substitution gives the following critical increment:

| Heading before the update | White/right | Black/left |
|---|---:|---:|
| N | 4U/V | 4/(UV) |
| E | 4/(UV) | 4V/U |
| S | 4V/U | 4UV |
| W | 4UV | 4U/V |

For a checkable algebraic derivation, let delta=1 on white and -1 on black,
and let axis=1 for a vertical heading and -1 for a horizontal heading.
The black-field change is -axis*delta*(U-1/U)*(V-1/V). Add the new G evaluated
at U*a^dx,V*b^dy and subtract the old G, where (dx,dy) is the actual outgoing
unit vector. Before imposing criticality, the difference from the table entry
is, in EACH of the eight cases, exactly

    (U^2+1)(V^2+1)(ab-a-b-3)/(UV(a+1)(b+1)).

Since ab-a-b-3=0 on the critical curve, the table follows. Every entry is positive.
This eight-case polynomial identity is a universal proof, not a simulation claim.

The construction combines the four rotated critical one-sided exponential
potentials already suggested by the noncritical clock family. One critical
component can have zero increments; their combined increment is never zero.
The new estimates use short-block lower bounds, not a false uniform lower bound
for all anisotropic single steps.

## 3. Uniform four-update increase at a=b=3

Assume c_x,c_y are both integers or both half-integers. Every monomial UV, U/V,
V/U,1/(UV) in the table is then an integral power of 3.

If a four-letter turn word is not constant, it contains two consecutive opposite
turns. Their entries have the form 4(3^j+3^(-j-1)), j integer. For example, an
N-facing R followed by L contributes 4U/V and 4V/(3U). The other cases follow
by inspecting the table. For integer j,

    3^j+3^(-j-1) >= 1+1/3.

For j>=0 this expression increases with j, and j->-j-1 gives the remaining
case. These two steps alone contribute at least 16/3; the other increments are
positive.

If all four turns agree, the positions trace a unit square. For example an
N-facing RRRR block contributes

    4(U+1/(3U))(1/V+V/3) >= 16/3

by applying AM-GM to both factors. More uniformly, in each of the eight
heading/constant-turn cases the product of the four positive reward entries
is 4^4/81: their U and V exponents cancel, and their coefficient product is
1/81. Four-term AM-GM therefore gives the sum at least 16/3. The independent
Laurent checker verifies these eight products as exact monomial identities. Thus Phi(F^4 X)-Phi(X)>=16/3 for EVERY complete finite-support X.

Sharpness for this statement, not for the exit bounds: take a=b=3, centre
(1/2,1/2), all four cells of {0,1}^2 black, head (0,0) facing S. The LLLL segment
removes those four black cells, returns to its original pose, and increases Phi
by exactly 16/3.

A finite-lookahead one-step clock is also available:

    Theta(X)=Phi(X)+Phi(FX)+Phi(F^2 X)+Phi(F^3 X).

Then Theta(FX)-Theta(X)=Phi(F^4 X)-Phi(X)>=16/3. Computing the three successors
requires no future oracle. This gives another proof of complete-state orbit
algorithms already established by the earlier noncritical clock; those algorithmic
consequences are not counted as new results here.

## 4. Potential range on squares

Place the square at 0<=x,y<n and take a=b=3, c_x=c_y=(n-1)/2. Write
s=x+y-(n-1), t=x-y, f(k)=3^k+3^(-k), and

    g(k,+)=(3^k-3^(1-k))/2,
    g(k,-)=(3^(-k)-3^(k+1))/2.

With epsilon=+ on N,E and - on S,W, the potential is exactly

    sigma sum_B chi(q)(f(t(q))-f(s(q)))
       +g(s(p),epsilon(h))+g(t(p),epsilon(h-1)).

Here h-1 denotes a counterclockwise quarter turn under N,E,S,W indexing.
Both s and t are integers, proving rationality even for an even side length.

For an arbitrary, possibly infinite exterior colouring, use the same potential
with its black-field sum restricted to the observation square. Every update
before the first exit reads an internal cell, so the local identity still
holds between internal states. No infinite sum is required. For a finite
complete field, this localized value differs from the full potential by a
constant throughout the internal prefix.

Throughout an internal prefix the external field contributes one CONSTANT,
because its colours and sigma do not change. Discard that constant only in the
range comparison, not from the physical input. For either diagonal coordinate,

    sum_(q in square) f(s(q))
       = 2*3^(1-n)*((3^n-1)/2)^2,

and the same formula holds for t. Therefore the range of the black-field term
is at most 3^(1-n)(3^n-1)^2. A binary weighted sum has range the sum of the
absolute coefficients; the displayed bound uses |f(t)-f(s)|<=f(t)+f(s).

For |k|<=n-1 the two values g(k,+),g(k,-) together have range at most
2(3^(n-1)-3^(1-n)); monotonicity of the displayed powers gives this directly.
The sum of the two head terms therefore has range at most four times that
parenthesis. Adding proves the range R_n of Theorem B. Equivalently,

    R_n=13*3^(n-1)-6-3^(2-n)<13*3^(n-1).

If T is the first exit time, X_0,...,X_(T-1) have internal heads. There are
T-1 internal-to-internal updates. Each disjoint block of four costs at least
16/3 and all leftover increments are positive. Thus

    floor((T-1)/4) <= floor(3R_n/16),

which proves Theorem B, including the exit-step convention. If an infinite
confined orbit were postulated instead, arbitrarily many four-block increments
would exceed the same finite range, a contradiction. Finiteness is proved,
not assumed in introducing T.

## 5. Short-axis pairing on rectangles

Place the rectangle at 0<=x<N, 0<=y<H. Set

    a=1+1/N, b=1+4N, c_x=0, c_y=floor((H-1)/2), k=floor(H/2).

These parameters lie on the critical curve, and |y-c_y|<=k. Also
1<=U=a^x<=a^(N-1)<3, using the binomial estimate
(1+1/N)^N <= sum_(j=0)^N 1/j! < 3. Consequently each absolute black-field coefficient is
at most 3b^k. Since there are NH cells, its range at fixed sigma is at most
3NHb^k.

Expand each head term as four monomials. Each coefficient has magnitude at
most 2, and each monomial U^(+/-1)V^(+/-1) has magnitude at most 3b^k.
Thus |G_h|<=24b^k and its range is at most 48b^k. An overall valid range is

    R_(N,H) <= 3(NH+16)b^k.                                (1)

Now start a two-update segment with a horizontal heading. Its first move is
vertical, by v=+1 or -1. The two reward monomials have V exponents represented
by

    b^j and b^(-j-1),    j=v(y-c_y) integer,

and their U powers are each at least a^(-(N-1)), because their read positions
have the same x. This does NOT require the second move to be vertical.
The table therefore gives

    Phi(F^2X)-Phi(X)
        >= delta_N := 4a^(-(N-1))(1+1/b) > 4/3,            (2)

provided the two read positions are inside the rectangle. The integer minimum
b^j+b^(-j-1)>=1+1/b is proved exactly as in Section 3.

Heading axes alternate, so a finite internal-to-internal segment consists of
these disjoint two-step blocks, with at most one initial update and one final
update unused. If r full blocks occur before first exit, T<=2r+3. Equations
(1)--(2) imply

    r <= R_(N,H)/delta_N,
    T <= floor(2R_(N,H)/delta_N)+3
      <= floor((9/2)(NH+16)(4N+1)^floor(H/2))+3.

This is Theorem C. Again an infinite confined orbit is excluded by unbounded
block cost, so no appeal to HC or an unproved eventual-exit premise occurs.

### A sharper computable rational bound

The implementation may replace the coarse range by

    R_exact = sum_(q in rectangle) |(U(q)-1/U(q))(V(q)-1/V(q))|
              + max_(q,h)G_h(q)-min_(q,h)G_h(q),

and return floor(2R_exact/delta_N)+3. This is still an UPPER BOUND, not the exact
maximum exit time. It is computed using rational arithmetic on a finite grid.
The negative sign and chi do not affect the coefficient absolute values.

## 6. What remains missing for HC

These theorems apply to the original unrestricted finite-support model. A box
is an observation region; it is not a wall or a permanent-confinement promise.
Every visit after a later re-entry can start a new finite-domain estimate, but
the theorem gives no bound on the number of re-entries or on the growth of the
region needed before P104 begins. A global increasing potential has no common
finite upper bound on the entire plane. Thus it does not force standard entry.

## 7. Reproduction

`python3 clock_escape/reproduce.py --critical-only` from the repository root (standard library only) verifies local identities, all four-
letter words on tested poses, sharp four-step control, rectangular pairing,
small-domain exhaustive exit cases, and retained exterior fields. Source hashes
and exact counts are recorded in check_results.json. An optional independent
SymPy script verifies all eight symbolic identities after critical substitution;
its output is supplementary, not a trusted oracle for the written algebra.

The additional independent `audit.py` imports neither the original implementation
nor a symbolic algebra library. It checks the eight cleared-denominator
identities as exact Laurent polynomials in a,b,U,V, all opposite-turn pairs,
all constant four-turn products and the horizontal two-step exponents. Its
integer rounding checks include zero-length internal segments.

The packaged all-parameter proof is Sections 2--5, not an extrapolation of finite
checks.

### References

K. R. Etse, *How Long Can The Escaping Ant Be Confined?*, MFCS 2026, LIPIcs 386,
49:1--49:17, DOI 10.4230/LIPIcs.MFCS.2026.49. Published PDF: Theorem 5 on p.49:9;
Theorem 12 on p.49:15. The stronger parity-dependent rectangle formula, not just
its simplified corollary, is used in the comparison. Extended version:
arXiv:2606.26677v1, Theorems 5 and 14.

The supercritical clock and complete-state orbit proofs are retained in
[the integrated manuscript](../../paper/main.tex), with local formal lemmas in
[Lean lemmas](../../lean/ClockLemmas.lean). The published version remains
[available unchanged](https://doi.org/10.5281/zenodo.23341604); the stronger proof is now
published as [version 0.3.0](../../paper/paper.pdf).
