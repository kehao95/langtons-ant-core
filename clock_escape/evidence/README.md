# Proof and verification audit — 2026-10-13

The manuscript and scientific sources are identified by the
[published source manifest](../release/published-source-manifest.json). This is an agent-led internal audit with separately implemented code,
not independent third-party peer review. No mathematical counterexample or
failure of the claimed constant was found in this audit.

## Universal proof, in dependency order

1. **Model and parity.** States are observed before the read/turn/flip/move.
   N,E,S,W have vectors (0,1),(1,0),(0,-1),(-1,0). At every move, both
   checkerboard parity and heading axis change; sigma is invariant. All eight
   heading/colour cases give delta*sigma*chi(p)=epsilon*epsilon'.
2. **Local finite sum.** Only the read cell changes. Its contribution is
   `-epsilon*epsilon'*(U+V)`. The diagonal coordinate changes by epsilon'.
   For negative integer exponents, powers are positive rational reciprocals;
   U*V=1. A remote black cell cancels from the increment because sigma is fixed.
3. **Four identities.** Multiplication by r+1>0 gives the four polynomial
   identities in `../lean/ClockLemmas.lean`. They hold for all rational r,U,V,
   with no sampled-parameter premise. Denominator clearing is reversible.
4. **Strict lower bound.** For U>0 and UV=1, `(U-1)^2>=0` gives U+V>=2.
   r>3 makes d positive; mixed cases add positive terms. Thus increment >=2d.
   At r=4, 2d=2/5. At r=3 an actual equal-sign branch has zero increment;
   that endpoint is excluded. Lean checks the universal algebraic lower bound.
5. **Square field range.** Fix sigma along the orbit, restrict the sum to
   `B intersect K_n`, and centre at c=n-1. Each optional coefficient has range
   equal to its absolute value, so the total range is at most their sum, not
   twice their sum. Reflection exchanges the two exponent sums and yields
   `F_n=2*r^(1-n)*((r^n-1)/(r-1))^2`. This holds for arbitrary exterior colours.
6. **Pose range.** g(s,+) is increasing in s for r>1; g(s,-)=g(-s,+).
   Both signs on [-R,R] therefore have total range
   `G_n=2*(r^R-r^(-R))`. Ignoring parity restrictions enlarges the possible
   range and is safe for an upper bound. At n=1, G_n=0.
7. **Existence before division.** A nonexiting run would accumulate positive
   uniform increments inside a bounded interval. Once finite exit T exists,
   the internal states are 0,...,T-1, yielding exactly T-1 increments.
   The generic interval inequality is Lean-checked. The last move out is
   not bounded using the internal head range.
8. **The constant 8.** With r=3+3/n, `(r+1)/(r-3)<=7n/3`,
   `r^2/(r-1)^2<=9/4`, and the bracket is at most `(13/4)*r^(n-1)`.
   The binomial/geometric-series estimate `(1+1/n)^n<3` implies
   `r^(n-1)<3^n`. Since 91/12<8 the expression inside the floor is
   strictly below 8*n*3^n. The reported +1 bound is conservative.
9. **Complete-state consequences.** Clock monotonicity bounds any specified
   target time, including t=0. The inverse inspects the post-colour at p-e_h,
   flips it, and undoes the corresponding turn. Telescoping also sends the
   backward clock to -infinity, giving a unique zero crossing. Equality of
   clock values does not imply equality of states. Sparse coordinate encoding
   does not make exponentiation or simulation polynomial-time.
10. **Infinite section.** The original draft stated infinitude without an
    explicit proof. The revised manuscript supplies the invariant row-parity
    vector with a horizontal-head correction. Singletons in distinct rows
    lie on distinct complete-state orbits. This closes an exposition gap;
    it is not advertised as a separate novel theorem.

## Machine evidence actually obtained

| Layer | Coverage | Result |
|---|---|---|
| Kernel-checked Lean 4.30.0 | Four universal polynomial identities, reciprocal sum, scaled lower bound, telescoping, internal interval | Pass; printed axioms only propext, Classical.choice, Quot.sound |
| New independent rational checker | 9,720 local cases; five rational bases, negative positions, three centres, remote black support | Pass |
| Independent finite graph | All 4,213,000 colour/pose states at n=1,2,3,4 | Exit maxima 1,6,17,46; no confined cycle |
| Independent witness replay | One maximum witness per square with integer-vector turns | Pass |
| Direct finite sum vs formula | 60 parameter pairs | Pass |
| Coarse bound spot checks | n=1..1000 | Pass; not the universal proof |
| Original baseline/checker replay | 4,704 local cases; 18,696 small-square states; 100 bounds | See legacy.json |

The graph checks every transition once, shares exact suffix distances, and
rejects a cycle if encountered. It imports no simulator or clock implementation
from the research repository. The float-based older small-coordinate stepper
is restricted to its original small cases; the new stepper uses Python integers
and includes a 10^30 coordinate control.

## Formalization boundary

The Lean file does **not** encode the ant state, field sums, integer powers,
finite geometric sums, floor specialization, complete-state algorithms, or the
row-parity invariant. Those remain analytic proofs plus scoped exact checks.
No native computation is used by these Lean local lemmas. Full theorem
formalization remains an optional strengthening, not a claimed completed result.


## Supplementary replay and repository checks

The retained complete-state implementation passes 1,200 inverse round trips,
120 signed reachability pairs, 120 orbit-normal-form comparisons, and 12
negative equal-clock pairs. The 12 declarative integer square clocks pass all
4,576 internal transition inequalities in both sigma sectors. Their LP
search is not part of the verification dependency.

## Reproduce and provenance

Run `python3 clock_escape/reproduce.py` from the repository root. This uses
bundled dependencies only and writes results here. The manuscript lives in
[`../paper/main.tex`](../paper/main.tex).

[reproduction.json](reproduction.json) identifies the inputs of the latest
recorded run. [public-integration.json](public-integration.json) preserves the
original standalone import check. The [release manifest](../release/published-source-manifest.json)
retains the published source layout and hashes; the released PDF is preserved
in [`../paper/paper.pdf`](../paper/paper.pdf).
