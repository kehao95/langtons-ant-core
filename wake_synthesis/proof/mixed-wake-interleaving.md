# Mixed-wake interleaving parity for full drift (2,-2)

**15 October 2026. Research baseline: `2396e9fa4365933b74f27dd84a349b331c66088d`.**

Evidence: a complete written rank/flow reduction and an exact Boolean-polynomial
identity, with independent finite checks. No Lean, outside mathematical review,
priority guarantee, HC proof, or nonstandard finite seed. The algorithm below is
a NECESSARY screen, never a positive realization certificate.

## 1. New theorem and precise normalization

Use the classical rule: white/right, black/left, flip, then move. Start with a
complete finite black set on Z^2. Let a nonempty word of length P repeat forever,
restore the heading, and have the FULL displacement d=(2,-2). An arbitrary finite
prelude and unqueried debris are allowed. We do not bound P, transverse width,
support size, growth, or rereading distance.

A full translation class modulo Z*d is (t,r)=(x+y,x mod 2). Let O be the finite
set of classes with odd phase multiplicity, and g=|O|=#R-#L. The checker/heading
invariant is sigma=chi(p) on vertical headings and -chi(p) otherwise, where
chi(x,y)=(-1)^(x+y). Translate a vertical-arrival phase to the origin, so sigma=+1.
Then even t are vertical-arrival layers Q and odd t horizontal-arrival layers C.
The translated complete black field is retained. No reflection or primitive-drift
substitution is used. For sigma=-1 the implementation first translates t by one;
this just exchanges the parity labels, not the physical hypothesis.

Let V be the number of O classes on Q layers, and let

    J(O) = #{(q,c) in (O on Q) x (O on C): t(q)<t(c)}.

Classes, not individual phase visits, are counted. Distinct classes on the same
layer are counted separately. Q and C cannot have equal t.

**Theorem 1 (mixed-wake parity).** Every such periodic realization satisfies

    V is even,                  J(O)+V/2 = 1 (mod 2).       (1)

Thus the transverse ORDER of odd classes constrains realizability, even after
all signed row/column residues and both checker populations have been fixed.
Changing arbitrary transverse gaps by an even amount preserves this test. The
screen sorts only O and costs O(g log g) integer operations; it does not walk
through potentially enormous gaps, or search any period.

This extends the preceding checker-pure obstruction to an explicit mixed-wake
condition. The phase/port factorization is retained from the earlier proof;
the contribution is its evaluation for arbitrary mixed O and the consequences
below. A necessary screen passing is not evidence that a real trajectory exists.

## 2. Needed finite-support facts and attribution

The stable-class criterion and signed mod-four residues are credited to
A. Jillhewar, *Finite-Support Periodic Highways of Langton's Ant* (2026), source
`Atharva12456/langtons-ant-highway@76a7e234e577d992d086c204c3dea00ae72cf10a`,
`paper/main.tex`. The needed arguments, including the rank factorization, were
already reconstructed in `proof/results/periodic-growth-closure.md`, Sections
2 and 4. The source prose is CC BY 4.0; this is an attributed extension, not a
transfer of authorship of those arguments. No external source code is copied.

For clarity, finite support is used as follows. In one d-class write q_i=b+k_i*d.
Far enough along it every phase occurs, and its initial colour is white.
The chronological order is increasing i-P*k_i. Hence its letters alternate
R,L,R,L,..., and its signed excess is exactly its odd-multiplicity indicator
D_v in {0,1}. Therefore g=#R-#L=|O|, and heading restoration gives 4|g.
The moves alternate axes. A horizontal displacement two requires P/2 even,
so 4|P. Every L event has odd stable rank, whence

    K := sum_(L events) stable_rank = #L = (P-g)/2 = 0 (mod 2).   (2)

Write q_r=|O on Q, lane r| and c_r=|O on C, lane r|. The signed-residue theorem,
using both x and y parity, gives

    q_0-c_0 = q_1-c_1 = q_0-c_1 = q_1-c_0 = 2 (mod 4).    (3)

It follows that q_0=q_1 (mod 4), c_0=c_1=q_0-2 (mod 4), and V=q_0+q_1 is even,
with V/2=q_0 (mod 2). These are hypotheses derived from actual periodic motion,
not assumptions silently imposed on arbitrary seeds.

## 3. General port-permutation sign, before imposing checker purity

At a class, order all visits by stable rank. Let alpha,beta be its incoming and
outgoing positive-port bit strings: at Q the positive ports are N and E, and
at C they are E and N. At Q, L means the bits differ; at C, L means they agree.
For a binary string of length m with A ones,

    inv(alpha)=A(m-1)+sum_k k*alpha_k+binom(A,2) (mod 2).

This follows by subtracting later ones from all positions after each one.
Apply it to both port strings. Positive directed-edge binomial terms cancel
between their source and target. If p_v=sum alpha+sum beta modulo two, the
remaining local correction is

    p_v(D_v+1) on Q,                 D_v(p_v+1) on C.      (4)

For Q use m=2p_v+D_v (mod 4). For C use m=2p_v-D_v (mod 4), together with the
extra binom(m,2) from the equal-bit L rule. This verifies (4) for D_v=0 or 1.
Let L denote the sum of (4), and let E be the sign of the permutation of edge
blocks, with vertices ordered by t then r and negative port before positive.
Order is preserved within every directed edge block: its successor stable time
changes by the same constant 1-P*voltage for all occurrences, including the
period seam. The phase successor is one even-length cycle and has sign one.
Consequently

    K=1+E+L (mod 2),                    E+L=1.             (5)

All visits in the complete periodic realization are represented. E depends on
the PARITIES of directed-edge counts because a block inversion contributes the
product of the two counts. We next eliminate those parities in favor of O.

## 4. Odd classes determine all edge parities

In this section arithmetic is over F2. At even layer 2j write Q_{j,r}=D_(2j,r),
and at odd layer 2j+1 write C_{j,r}=D_(2j+1,r). Let e,w be E/W outgoing-count
parities at Q, and n,s N/S outgoing-count parities at C. Local parity and flow give

    w_j=e_j+Q_j,                    s_j=n_j+C_j,
    n_j=n_(j-1)+Q_j+C_j,
    e_j=e_(j-1)+Q_j+swap(C_(j-1)).                         (6)

All are two-vectors in lanes 0,1. Set the counts to zero below the finite visited
range. Equations (6) determine every parity uniquely. They must also return to
zero above the visited range. Thus the four totals q_0,q_1,c_0,c_1 have the same
parity; this also follows from (3). It is legitimate to start below the range
because one period has only finitely many events, with no width bound needed.

We claim the following exact identity for ANY finite closed solution of (6):

    E+L = J(O)+binom(g,2)+q_0 (mod 2).                     (7)

Combined with (3), 4|g, and (5), it immediately proves (1). The following gives
an explicit, small algebraic verification of (7), so no long-width extrapolation
is hidden in the claim.

## 5. A nine-variable Boolean identity proves (7) at every width

For a layer encode its four outgoing parities as b=(negative_0,positive_0,
negative_1,positive_1). The within-layer edge-inversion signs are

    S_Q(b)=b_0*b_2+b_1*b_2+b_1*b_3,       S_C(b)=b_1*b_2.

For adjacent layers a,b, the inversion sign is

    A(a,b)=(a_1+a_3)(b_0+b_2).

For layers two apart it is

    B_Q(a,b)=a_1(b_0+b_2)+a_3*b_2,
    B_C(a,b)=a_1*b_0+a_3(b_0+b_2).

Layers at greater separation contribute no inversions. These formulas follow
by sorting the directed targets: Q edges swap lane; C edges do not. There are
no hidden internal-block permutations.

Before processing a new pair of layers let the state be (e_0,e_1,c_0,c_1,z),
where e is the previous Q's E parity, c the previous C's D value, and z the
parity of the number of Q odd classes already processed. Recurrences (6) imply

    n_0=e_1+z+c_0,                 n_1=e_0+z+c_1.

For new bits (Q_0,Q_1,C_0,C_1), put

    e'_0=e_0+Q_0+c_1,              e'_1=e_1+Q_1+c_0,
    n'_0=n_0+Q_0+C_0,              n'_1=n_1+Q_1+C_1,
    z'=z+Q_0+Q_1.

The new state is (e'_0,e'_1,C_0,C_1,z'). Form the old C block
b=(n_0+c_0,n_0,n_1+c_1,n_1) and new blocks
u=(e'_0+Q_0,e'_0,e'_1+Q_1,e'_1),
v=(n'_0+C_0,n'_0,n'_1+C_1,n'_1).
Only the positive entries of the old Q block are used; write a=(0,e_0,0,e_1).
Adding the new pair increases the edge sign by

    Delta E=S_Q(u)+S_C(v)+A(b,u)+B_Q(a,u)+A(u,v)+B_C(b,v).

The local correction and inversion-count increases are

    Delta L=(n_0+e'_0)(1+Q_0)+(n_1+e'_1)(1+Q_1)
             +C_0(1+e'_1+n'_0)+C_1(1+e'_0+n'_1),
    Delta J=z'(C_0+C_1).

Let b_0,...,b_3 denote the four new D bits. The prefix population parity is
n_0+n_1, so

    Delta binom(g,2)=(n_0+n_1)(Q_0+Q_1+C_0+C_1)
                     +sum_(i<j) b_i*b_j.

Define the following explicit boundary correction:

    H(e_0,e_1,c_0,c_1,z)
      = e_0+e_1+z+e_0*c_1+e_1*c_0+e_1*c_1+e_1*z+c_0*c_1+c_0*z.

Substitution, using x^2=x in F2, gives the polynomial identity

    H(old)+H(new)=Delta E+Delta L+Delta J+Delta binom(g,2)+Q_0.  (8)

This is an identity in nine Boolean variables. The supplement independently
checks all 512 assignments AND expands it in the exact Boolean polynomial ring;
the reduced residual has no monomials. There is no numerical optimization.
Summing (8) over all layer pairs telescopes H. Before the finite support it is
zero; after the last odd class and empty boundary padding, e=c=n=0 and z=0 by
closure, so it is again zero. The sum of Q_0 is q_0. This proves (7).
For actual motion binom(g,2)=0 mod 2 because 4|g, and q_0=V/2 mod 2 by (3).
Together with E+L=1 this proves Theorem 1. QED.

The finite identity covers arbitrary numbers of layer pairs; it is not a test
up to a maximum width. It also explains why empty gaps can be ignored by the
final closed formula even though the event graph itself is not being quotiented
as a physical realization.

## 6. New growth-eight consequences with two full extreme rails

Now suppose g=8 and each transverse extreme contains BOTH residue classes.
Extremal rigidity says these four classes are C classes. To check the premise
directly, a highest-level visit must arrive with increasing t and depart with
decreasing t. A vertical arrival would force L at every visit, contradicting
the stable class word starting R; hence arrival is E and the turn R. Alternation
then forces a singleton class. The analogous lowest-level visit is W followed
by R. Both extreme layers are therefore horizontal-arrival C layers. It also ensures all
other odd classes lie strictly between them. No width or period is specified.

**Corollary 2.** Such a candidate must have exactly two Q odd classes, one in
each lane, and six C odd classes, three in each lane. Its x/y residue matrix is

    [[1,3],[3,1]].

Proof: V is even and at most four because the extremes supply four C classes.
If V=0 then J+V/2=0, contradicting (1). If V=4 then all four C classes are at the
two extremes; each Q lies below exactly two of them, so J=8 and V/2=2, again a
contradiction. Thus V=2. Equations (3) force (q_0,q_1)=(1,1) and
(c_0,c_1)=(3,3). QED.

There are exactly four internal odd classes: two Q and two C, with one class of
each kind in each lane. The extremes make an even contribution to J. If the
four internal levels are distinct, their increasing type sequence must therefore
have an even number of Q-before-C pairs.

**Corollary 3 (arbitrary-gap interleaving exclusion).** The sequences QCQC and
CQCQ are impossible, irrespective of lane choices and all distances between
layers. The sequences QQCC, QCCQ, CQQC, CCQQ are not excluded by this test.
Coincident same-type layers are also not asserted impossible. This is a
necessary order restriction, not a realization claim for the surviving types.

For example the eight-class wake

    {(1,0),(1,1),(2,0),(3,0),(4,1),(5,1),(11,0),(11,1)}

has the same mixed residue matrix as in Corollary 2 and satisfies the old signed
residues. Its two Q classes and six C classes give J=7 and V/2=1, violating (1).
No periodic word of ANY length can realize it. Spacing any consecutive levels
farther apart by even amounts yields an infinite family of equally excluded
wakes of unbounded width. This is not a finite set of sampled widths.

For contrast replacing (4,1) by (6,1) gives J=6 and passes this test, with the same
growth, width and residue matrix. It is explicitly labelled NOT_EXCLUDED, not
YES. A complete trajectory or an additional impossibility argument is still
required. Nothing here classifies every growth-eight wake or other drifts.

## 7. Actual checks, bounded screens, and scope

Run `python scripts/check_mixed_wake_parity.py`, or `python check.py` in the
standalone module. Add `--enumerate` to reproduce the separate bounded screen.
No optional numerical library, network, SMT solver or native compiler is used.

Actual checks include the 512-assignment and symbolic Boolean identity, 18,895
geometric heading-reset words through length 20 with drift (2,-2), their 187,572
class-order checks, all 65,536 subsets of an eight-layer/two-lane window (8,192
closed parity cases), and all 104 standard P104 phases. The geometric words are
not claimed physically realizable: they test the port-permutation factorization
before imposing the stable-colour condition. The independent layer algorithm
reconstructs edge parities and compares the actual block permutation, rather
than calling the compact screen. Standard class words are checked explicitly.

For growth eight at exact widths 10,12,14, a complete enumeration of odd-class
assignments with occupied extreme levels gives:

| width | pass signed residues and checker mixing | excluded by (1) | not excluded |
|---:|---:|---:|---:|
|10|7410|3058|4352|
|12|26930|11374|15556|
|14|77784|33320|44464|

The old filters named here are ONLY signed residues and checker mixing, not all
other theorems in the repository. Some assignments may already be excluded by
other methods. These counts are wake assignments, NOT finite seeds, actual
periodic trajectories or new mutually independent theorems. No fraction of HC
completion is inferred. The new screen rules out 47,752 of these 112,124 inputs;
64,372 still need other conditions. The mathematical validity of (1) at arbitrary
widths comes from Sections 3-5, not this finite table.

The previous six residue matrices for general growth-eight diagonal wakes still
all have some assignments passing (1); no matrix is globally removed without
an added condition such as the full-extremes premise of Corollary 2. There is no
new certified nonstandard finite seed, no proof g>=12, and no all-input entrance
theorem. The next computation should feed only NOT_EXCLUDED candidates to the
full chronology/realization checker, without interpreting that status as YES.
