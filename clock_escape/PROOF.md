# Integer clocks and finite-domain escape

The current manuscript is [An Ant on the Clock](paper/main.tex). Its square
bound uses an integer clock, while its fixed-height rectangular bound uses the
[critical anisotropic potential](evidence/critical/proof.md). Both are analytic
proofs with exact algebraic checks. The retained Lean lemmas cover the
supercritical rational construction in the manuscript appendix.

## 1. Integer clock on complete states

Let X=(B,p,h), with finite B, h=N,E,S,W=0,1,2,3, and the white-right /
black-left, flip-then-move update F. Set chi(q)=(-1)^(q_x+q_y), and let
sigma=chi(p) for vertical h and -chi(p) for horizontal h. Both position parity
and heading axis change, so sigma is invariant. Set epsilon=+1 for N,E and
-1 for S,W. For a fixed integer c, define s(q)=q_x+q_y-c and

    f(s)=3^abs(s)-1,
    J(s,e)=f(s)/2 if e*s>=0, and -3*f(s)/2 otherwise,
    Theta_c(X)=-sigma sum_(q in B) chi(q) f(s(q)) + J(s(p),epsilon(h)).

This is an integer since f(s) is even. It includes the entire finite field.
Writing e,e' for the before/after epsilon, its exact gain is

    Theta_c(FX)-Theta_c(X)=1+4*f(s)*1_{e'!=e and e*s<0} >= 1.

To prove this, let delta=+1 on white and -1 on black. The eight literal
heading/colour cases give delta*sigma*chi(p)=e*e' and s(p')=s+e'. The field
gain is -e*e'*f(s). From the powers defining J,

    J_+(s+1)-J_+(s)=f(s)+1,
    J_-(s-1)-J_-(s)=f(s)+1,
    J_-(s)-J_+(s)=-2*sgn(s)*f(s).

For equal e,e' the gain is one. For + to -, it is
1+2f(s)+J_-(s)-J_+(s), giving the two asserted sign branches; the other
reversal is reflected. At zero f vanishes. Summation gives
Theta_c(F^t X)-Theta_c(X)>=t.

## 2. Square range and first exit

For Q={x0,...,x0+n-1} x {y0,...,y0+n-1}, choose c=x0+y0+n-1 and
restrict the field sum to B intersect Q. This localized finite integer also
covers infinite exterior colourings. Its increment identity holds between
internal states since the only flipped cell is inside Q.

For fixed sigma, the exact range of the field term over all internal
colourings is the sum of its absolute coefficients:

    S_n=sum_(s=-(n-1))^(n-1)(n-|s|)(3^|s|-1)
       =[3^(n+1)-2*n^2-4*n-3]/2.

The identity follows by summing
sum_(j=1)^(n-1)(n-j)3^j=sum_(k=1)^(n-1)sum_(j=1)^k 3^j.
Every head correction lies in [-3M/2,M/2], M=3^(n-1)-1. Thus the total
clock range is at most R_n=S_n+2M. An infinite internal orbit is impossible
because its clock would exceed this finite range. If first exit is at T,
there are T-1 internal-to-internal updates. Hence

    T <= R_n+1 = E(n):=[13*3^(n-1)-2*n^2-4*n-5]/2.

This includes the exit move, works for n=1, and is uniform over all poses
and arbitrary exterior colours. Its leading term is (13/6)*3^n.

## 3. Fixed-height rectangles

The companion [critical proof](evidence/critical/proof.md), Sections 2 and 5,
gives the explicit potential, eight local monomial identities and a two-step
lower bound. With a=1+1/N, b=1+4N, k=floor(H/2), its range is at most
3(NH+16)b^k and each horizontal-arrival internal pair gains more than 4/3.
Heading axes alternate, so r such pairs leave at most two unused internal
steps and T<=2r+3. The resulting bound is

    T <= floor((9/2)(NH+16)(4N+1)^floor(H/2))+3.

One can exchange N,H and take the smaller bound. For fixed height H this
is O_H(N^(floor(H/2)+1)); the square estimate uses Section 2 instead.

## 4. Complete-state algorithms

Fix c=0 on all inputs. A complete-state match F^t X=Y requires
0<=t<=Theta_0(Y)-Theta_0(X), giving a finite simulation budget and a unique
offset. Reversibility gives a decision for two-sided orbit equivalence.

Every two-sided orbit crosses from a negative to a nonnegative clock value
exactly once: forward values tend to +infinity and backward values to
-infinity, with at least unit change at every update. Searching for this
crossing defines a computable representative C and unique integer k with
X=F^k C. The inverse update and the proof that infinitely many distinct
representatives occur are given in the manuscript's orbit section.

## 5. Evidence and dependencies

- `python3 clock_escape/reproduce.py --integer-only`: all 24 algebraic sign
  branches; 100 range sums; all 18,696 states of squares through side three.
- `python3 clock_escape/reproduce.py --critical-only`: retained critical
  tests plus independent Laurent identities and pair/rounding checks.
- `python3 clock_escape/reproduce.py`: also the earlier rational-clock,
  exhaustive four-by-four domain and Lean 4.30.0 local-lemma evidence.

The article develops the integer clock, its square-range argument and
complete-state orbit algorithms. The separate [wake project](../wake_synthesis/)
uses their whole-period increments to solve the prescribed-wake inverse problem.
The [article](paper/paper.pdf) presents the clocks, escape bounds and orbit
algorithms together.
