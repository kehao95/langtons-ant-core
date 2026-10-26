# A short analytic proof of unit-diagonal highway exclusion

## Result, provenance, and scope

**Theorem.** A classical two-colour Langton ant started from a finite black
field cannot have an eternally periodic, heading-restoring turn word whose
FULL displacement per chosen period is `(1,-1)` or a quarter-turn rotation.
There is no restriction on period, growth, width, retreat, seed size, or wake.

The full vector matters: standard P104 has displacement `(2,-2)` and is not
excluded because its primitive *direction* happens to be `(1,-1)`.

The theorem itself and the consequent universal growth bound `g>=8` were
integrated by parallel project work in `2067bb5c8cee453988993aa4a63e059751f9866d`,
using a three-layer finite certificate [C]. **The new contribution of this
note is a purely analytic proof**: the 12,884-case finite check is replaced by
forced first/second-layer words and one binary-port interleaving argument.
The independently written Python/C++ enumerations and witness audit in this
package are regressions, NOT mathematical premises of the proof below.

Combining this exclusion with Jillhewar's signed-residue/density and
axis/even-diagonal growth-four results [J] yields `g>=8` for every finite-support
periodic highway of nonzero drift. This is a restated project corollary, not a
second newly discovered theorem. Section 6 identifies all dependencies. The
note neither proves eventual periodicity nor excludes growth eight or proves HC.

## 1. Stable chronology and extremal normalization

The literal rule is white/right, black/left, then toggle the current cell and
move one edge. Let a nonempty word of length P repeat forever, restore the
heading, and translate by `d=(1,-1)`. It need not be a least period. Every finite
time has a finite black field, so a sufficiently late phase can be chosen as
a new origin without changing the assumptions. Unread finite debris is allowed.

There is exactly one FULL translation class at each transverse level `t=x+y`.
Write `b_t=(0,t)` and `q_i=b_t+a_i*d` for the phase positions. Far enough along
the class, every phase is present and its physical cell was initially white.
The stable times for visits to `b_t+n*d` are

    nP + tau_i,       tau_i=i-P*a_i.

Hence each class, in increasing stable rank k, has turns `R,L,R,L,...`.
This is the necessary part of the established finite-support criterion [J].
A path that goes from one event to another in l updates and displacement
`delta*d` changes the corresponding stable times by `l-P*delta`.

The invariant sigma is `(-1)^(x+y)` for vertical incoming headings and its
negative for horizontal incoming headings. Both checker parity and heading
axis change on every step. At a transverse extreme the invariant fixes the
incoming axis, and the inward-neighbor condition then fixes both directions.
All turns of that single class are equal. Stable alternation starting with R
therefore forces one singleton R at each extreme. Normalize the top event T
to the origin: it arrives E, leaves S, and fixes `sigma=-1`. The bottom arrives
W and leaves N, so its level is even. Thus the width W is positive and even.

We will use two elementary consequences of a real period's phase successor.

**Forced edge matching.** Along any fixed directed edge between representatives,
`b_s+e=b_t+delta*d`, the stable time changes by the constant `1-P*delta`.
Thus ordered source occurrences match ordered target occurrences first to
first. The period seam causes no exception: its additional epoch cancels in
`tau=i-P*a_i`. There is no matching permutation to guess.

**Consecutive-return rule.** In a fixed contiguous path, a first return to the
same physical cell must increase its stable rank by exactly one. Translate the
path far enough along d that every involved read is stable. An intervening read
would be another node of this same contiguous path. With none, the ranks must
be adjacent. Opposite colours alone are not enough to permit a rank skip.
If a proposed path closes on its original phase event while obligatory deeper
events remain, it is instead impossible because the phase successor is one
P-cycle and a proper closed component can never join those events.

## 2. Port identities and the first interior layer

Build layers downwards. A bit `a_k=1` means arrival from the already built upper
neighbor, and `b_k=1` means departure to that neighbor. At even t the incoming
headings are W/E for bits 1/0; at odd t they are S/N. Literal R/L turning gives

    b_k = a_k XOR (k mod 2) XOR (t mod 2).                 (1)

For a word of length n, let `I=sum a_k`, `J=sum b_k`, `o=n mod 2`, and let e
count the ones at even ranks. Direct counting yields

    n=2(I+J-2e)+o       for even t,
    n=2(J-I+2e)-o       for odd t.                        (2)

The remaining lower-side counts are `n-J` and `n-I`. At each cut they agree,
starting with `I=J=1` at the singleton top.

Width zero is impossible because each move changes t. If W=2, the singleton
extremes force two middle visits; but (2) at t=-1 gives `2=4e-o`, impossible
because n=2 implies o=0. Consequently W>=4, so layers -1,-2,-3 are strictly
interior and a deeper visited layer always remains during the argument.

Let A_k denote rank k on layer -1. Since I=J=1 there, (2) and the existence of
an arrival give n=3 or 4, with its sole arrival-one at even rank 0 or 2.
The only possibilities are

    100, 1000, 001, 0010.

In either last case, forced matching gives `A_0 -> T -> A_2`, with directions
E,S. It moves by d in two updates, so `tau(A_2)-tau(A_0)=2-P<0`. But rank two
must follow rank zero. There are at least four distinct phase events, so P>=4.
This contradiction leaves only `100` and `1000`. In both cases the fixed top
path is `A_2 -> T -> A_0`.

## 3. The second layer is forced without enumeration

Let B_k denote rank k on layer -2. Write `p_0<p_1<...` for its arrival-one ranks
and `q_0<q_1<...` for its departure-one ranks. Their common number c is 2 when
A has word 100, and 3 when it has word 1000. Forced matching supplies the path

    B_(q_1) -> A_2 -> T -> A_0 -> B_(p_0),                (3)
    directions: N,E,S,W.

This is a first physical return. A coincident endpoint phase would be an
impossible proper closed component. Otherwise the consecutive-return rule gives

    p_0 = q_1 + 1.                                      (4)

At even layer -2, equation (1) says that an even rank belongs to BOTH the p and
q lists or neither, while an odd rank belongs to exactly one. There is no
arrival-one before p_0. Therefore all even ranks before p_0 are in neither list,
and all odd ranks before p_0 are departure-ones. Equation (4) then forces

    q_0=1,    q_1=3,    p_0=4.

Rank 4 is even and hence belongs to both lists, so `q_2=4`. In particular c
cannot be 2: A must have word 1000 and c=3. The departure list is now exhausted.
Every later even rank has arrival bit zero, and every later odd rank has
arrival bit one. The remaining two arrivals are therefore at ranks 5 and 7.
No rank 9 can occur, because it would create another arrival. Thus B has exactly
one of the two words

    00001101,       000011010.                           (5)

This derivation replaces the entire 124-candidate second-layer enumeration.

The forced upper edges in either case include

    B_1 -> A_1 -> B_5,
    B_3 -> A_2 -> T -> A_0 -> B_4 -> A_3 -> B_7.          (6)

The ranks departing B downwards are `0,2,5,6,7` and optionally 8. The ranks
arriving B from below are `0,1,2,3,6` and optionally 8. We use only their first
five entries, so the optional last event does not create another case.

## 4. Two forced returns and two forbidden bridges on the third layer

Let C_k be rank k on layer -3. Reuse p_j for its ordered arrival-one ranks and
q_j for its ordered departure-one ranks. There are at least five of each.
Matching the lists just given and the paths (6) forces

    C_(q_1) -> B_1 -> A_1 -> B_5 -> C_(p_2),
    directions: E,N,W,S;

    C_(q_3) -> B_3 -> A_2 -> T -> A_0 -> B_4 -> A_3 -> B_7 -> C_(p_4),
    directions: E,N,E,S,W,N,W,S.

Both are first returns to their starting physical cell. Thus

    p_2=q_1+1,              p_4=q_3+1.                  (7)

On the other hand two specific identifications are impossible. If `p_1=q_1`,
the common C event joins the following path:

    B_2 -> C_(p_1=q_1) -> B_1 -> A_1 -> B_5,
    directions: S,E,N,W.

It is a first physical return with ranks 2 then 5 on B, violating consecutivity.
If `p_4=q_4`, another fixed path is

    B_4 -> A_3 -> B_7 -> C_(p_4=q_4) -> B_6,
    directions: N,W,S,E.

Its first return has ranks 4 then 6, also impossible. Therefore

    p_1 != q_1,             p_4 != q_4.                 (8)

All stated paths are dictated by first-to-first matching. Their compass words
show explicitly that no intermediate vertex is the starting physical cell.
The first two paths visit no other point on layer -3. No time estimate or
period cutoff has been introduced.

## 5. Binary interleaving contradiction

At odd layer -3, equation (1) says that each EVEN rank belongs to exactly one
of the p and q lists, whereas each ODD rank belongs to both lists or neither.
We show that (7) necessarily violates (8).

If q_1 is odd, it also lies in the p list. Since the next index is p_2=q_1+1,
it must be p_1=q_1, already forbidden. Thus q_1 is even, p_2 is odd, and p_2
also lies in the q list; necessarily `p_2=q_2`.

If q_3 is even, p_4=q_3+1 is odd and also lies in the q list, forcing
`p_4=q_4`, forbidden. Thus q_3 is odd and also lies in the p list; since
p_4=q_3+1, necessarily `p_3=q_3`.

We have obtained two distinct odd indices `p_2=q_2` and `p_3=q_3` that are
successive in BOTH lists. No member of either list can lie strictly between
them. But between distinct odd indices there is an even index, and every even
index belongs to exactly one of the lists. Contradiction.

This excludes every width W>=4. Section 2 excluded all other widths, proving
the theorem. Quarter-turns preserve the rule and finite support and cover the
other three full unit-diagonal displacements. No finite enumeration is a premise.

## 6. Growth corollary and proof dependencies

[J] gives positive growth divisible by four and `g>=2 max(|d_x|,|d_y|)`.
For g=4 the two coordinates have absolute value at most two. Heading restoration
makes P even and hence `d_x+d_y` even. The only nonzero drift types up to
quarter-turns are the unit diagonal, the two-cell axis, and the two-cell diagonal.
The first is excluded above; [J]'s all-period axis and even-diagonal growth-four
exclusions eliminate the others. Therefore g>=8. [C] also supplies an attributed
in-repository reconstruction of those dependencies. They are not new claims
of this note, and our new audit does not independently reprove the cited general
rank/residue theorems. The analytic unit-diagonal proof itself uses only Sections
1-5, not those external exclusions.

## 7. Independent regressions, not premises

The complete-row Python program and independent C++ vector-geometry program
still reproduce the three-layer table 4/124/12,756 candidates, 2/2/0 survivors.
They are retained to audit the derived structure, not to supply the proof.
A separate implementation validates all 12,880 rejection witnesses, 32,766 short
binary words, 32 count domains, eight compass port cases, two corrupted-witness
negative controls, and 936 genuine P104 prefix controls using the FULL `(2,-2)`
quotient. `analytic_audit.py` independently checks the displayed physical paths,
the forced second-layer words, and the interleaving implication on every finite
candidate reached by the old certificate.

Run `python3 reproduce.py --output /tmp/unit-diagonal-replay.json`. Sources,
checks, full retained report and their hashes are supplied together. Reproduction
requires Python 3.10+ without -O and g++ with C++17/undefined-behavior sanitizer;
the mathematical proof requires neither program. Failed or interrupted runs
are not accepted as verification. The proof is analytic; exact computations check its finite controls.

### References and version boundary

[J] A. Jillhewar, *Finite-Support Periodic Highways of Langton's Ant: Necessary
Conditions, Transverse Exclusions, and Exact Search*, manuscript dated 17 August
2026, inspected at `76a7e234e577d992d086c204c3dea00ae72cf10a`.
https://github.com/Atharva12456/langtons-ant-highway/tree/76a7e234e577d992d086c204c3dea00ae72cf10a

[C] H. Ke, *Closing the periodic-growth proof: residues, ranks, and small drifts*,
`wake_synthesis/proof/periodic-growth-closure.md`, with its separately bundled
unit-diagonal finite certificate, as integrated in main revision
`2067bb5c8cee453988993aa4a63e059751f9866d` of `kehao95/langtons-ant-core`.
This parallel result was discovered on the final synchronization; it supersedes
any novelty claim for the theorem itself. The present analytic forcing proof
and its independent regression package are the incremental contribution.
https://github.com/kehao95/langtons-ant-core/blob/2067bb5c8cee453988993aa4a63e059751f9866d/wake_synthesis/proof/periodic-growth-closure.md
