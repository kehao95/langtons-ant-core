# HC strategy pivot: rooted contour surgery, not a further defect budget

20 October 2026. Inspected repository base: `8c414b8963260f5d4d394dc5b4c53065028b4c6e`.

**Status: research programme and an exact representation/control package.** No new HC theorem, transience theorem, counterexample, novelty or publication claim. The contour representation and split/merge operation are established ideas. The small finite witness below tests a proposed use, not a newly excluded global HC branch. Existing proof statuses and the theorem ledger are unchanged.

## 1. What changes, and what does not

The canonical problem remains the classical LR ant on the full integer lattice, with a complete finite black set, white/right, black/left, toggle then move. Previously proved J10, supply, periodic classification and arithmetic tools remain available. They are not erased or reopened by this note. We stop treating a better finite-prefix bound as the immediate next global objective. Instead, study how the actual ant reconnects complete planar routing contours.

The first all-input objective of this route is qualitative transience:

    for every finite B0, pose, and fixed finite K,
    only finitely many physical read positions lie in K.

No uniform bound in initial cardinality is requested. This would exclude recurrent finite controllers, but NOT transient nonstandard highways or transient aperiodic computation. HC still needs their exclusion, or a direct standardization argument. Transience is a target, not an assumption or conclusion of this package.

## 2. Prior art and the precise change of representation

Gale, Propp, Sutherland and Troubetzkoy, *Further Travels with My Ant*, Mathematical Intelligencer 17(3), 1995, pp.48-56, Sections 3-4, describe Truchet switches, frozen closed contours and their reconnection. Their recurrent-symmetry theorem concerns generalized rules with an even-run property, not a theorem for the classical two-state LR rule.

    https://arxiv.org/abs/math/9501233

Rechtman and Rechtman, *Equivalence of Deterministic walks on regular lattices on the plane*, Section II, give the square-lattice mirror/rotator correspondence. A homogeneous rotator background becomes a CHECKERBOARD mirror background. Results about a homogeneous mirror background cannot be imported without this transformation.

    https://arxiv.org/abs/1603.08269

The repository already uses a related rotated black-edge graph in `results/nonlocal-cycle-rank-obstruction.md` and rules out functions of its cycle rank alone. This programme retains cyclic order, the moving root, contact ports and their physical embedding; it does not revive that scalar rank.

## 3. Exact rooted-permutation dynamics

Number incoming headings N,E,S,W by h=0,1,2,3, and put

    epsilon = (h-x-y) modulo 2.

It is invariant under each physical step. In one fixed sector let E_epsilon contain incoming states e=(x,y,h) with this parity. Each site has exactly two admissible incoming states, e and bar(e)=(x,y,h+2 mod 4).

For a FROZEN black field B define P_B(e) by reading its colour, turning and moving, but NOT changing B. This is a permutation: every arrival has a unique predecessor because the heading identifies the preceding site and its fixed colour identifies the preceding heading. If q is the current site, let tau_q exchange its two admissible incoming states and fix all others. Direct substitution gives

    P_(B xor {q}) = P_B composed with tau_q.

The exact PHYSICAL update is therefore

    (P,e) -> (P composed with tau_q, P(e)),

where the next marked state uses the OLD permutation. Using the new successor at e would be a different automaton.

This is lossless: P_B compared with the all-right permutation recovers every black bit in the chosen sector. It retains the entire finite field, including remote unvisited cells. The permutation cycles are STATIC routing contours, not periodic physical trajectories. No period-104 premise enters this representation.

## 4. Why the frozen contours can be computed exactly

The all-right permutation P_empty has only four-cycles. A field of m black cells changes the successors at 2m incoming states, by m pairwise-disjoint transpositions. Let U be the union of all all-right four-cycles that meet these 2m states. Then |U|<=8m, U is invariant under the modified permutation, and every cycle outside U remains a four-cycle. Consequently every frozen contour has at most max(4,8m) incoming states. The implementation uses the safe bound 8m+4.

This is an elementary finite-modification observation used for exact cycle traversal, not a new global time bound. m is the CURRENT full black mass, which can grow indefinitely. Frozen finite cycles do not imply a bounded physical orbit.

## 5. Exact split/merge law and a failed sealing hypothesis

If e and bar(e) belong to different P cycles, the transposition joins those two cycles. The new marked contour contains their union.

If they belong to the same P cycle, the transposition splits it in two. The new marked contour contains bar(e) and P(e); the detached one contains e. These two cycles are disjoint as directed incoming states, but both pass through the physical site q. A split therefore does not even remove the contact at its splitting cell.

The tempting assertion "a detached closed contour is permanently retired memory" is false on the unperturbed blank orbit itself. Start at (0,0),N. Use zero-based pre-update indices:

    t=4: a 20-arc contour splits into marked length 4 and detached length 16;
    t=5,6,7: the detached 16-arc contour remains unchanged;
    t=8: the marked 16-arc contour joins that SAME detached contour, giving 32.

The physical turn prefix is RRRRLRRRR. The complete source fields and marked states are in the report. There is no added marker, external intervention or infinite support. This is a finite diagnostic, not an HC counterexample.

A simple closed Truchet contour is not automatically a wall: a visit to its other arc at a shared tile can reconnect it. Neither the Jordan curve theorem alone nor a count of cycles proves permanent causal separation.

## 6. The new research object and its acceptance test

Represent a finite part of the dynamics by the marked contours, their cyclically ordered contact ports, the tile pairing between ports, and physical coordinates. Do not replace it with an unlabelled contact graph, a cycle count, or a fixed-radius snapshot. Do not delete passive contours merely because the marker is elsewhere.

The positive task is to use ORDERED reconnection histories to rule out infinitely many physical returns through a fixed finite region from a finite seed. A useful lemma would show why a proposed recurrent interface cannot reconstruct all of its next required contacts. It must tolerate background four-contours continually being recruited and later-written memory continually being reused. No such lemma is proved here. No fixed-dimensional or finite-state quotient is assumed.

A genuinely successful transience theorem would change the global negative-run split, unlike another fixed-N calculation. It would still not establish HC: after leaving every finite region, the ant might in principle remain nonstandard. A second theorem would have to force a standard protected tail without assuming bounded width or finitely many contour types in advance.

The negative task uses the same representation: synthesize a true expanding reconnection protocol from one finite seed. A certificate must give COMPLETE finite states X_n and exact nonempty physical blocks with F^(ell_n)(X_n)=X_(n+1), while proving infinitely many actual standard-language defects or another rigorous nonstandard-future obstruction. Choosing a different larger seed for each desired duration is not a certificate. The repository already has this general induction-certificate discipline; the change is to design ordered contour surgeries first rather than guess long R/L words or preinstall more remote markers.

This is a programme, not a claim that either endpoint is likely or already reduced to a tractable finite calculation. In particular every ordinary update is a contour surgery, including on P104: one must not require that all splitting/merging eventually stop.

## 7. Actual scoped execution and remaining boundary

`experiments/hc_global/contour_surgery_pivot/check.py` has no third-party dependencies. Its frozen report checks all 512 fields on a 3x3 set, all four headings: 2,048 exact one-step split/merge identities. A sparse permutation updater and a separate vector-turn, full-black-set simulator agree at EVERY step and on the COMPLETE field over 33 inputs, totalling 28,384 updates. Some controls retain an unread marker at coordinate scale 10^60. The blank prefix above explicitly reattaches the same stored 16-arc cycle.

A development report comparison initially failed because tuple coordinates were serialized as JSON arrays; coordinates were normalized before the final frozen report was produced. The corrected default comparison was then actually run and passed. This is a representation bug correction, not new mathematical evidence from a failed run. No other old certificate or broad test suite was replayed.

The purpose of these tests is to establish a usable and exact starting representation and kill an unsound sealing inference immediately. They neither prove transience nor classify infinite contact histories. The established Truchet/mirror methods are credited, not renamed as a new independent publication. The canonical HC frontier is unchanged.
