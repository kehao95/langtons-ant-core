# Exact standard-defect macros through non-simple transient components

Evidence: analytic coverage and geometric arguments, a complete finite lifted-graph certificate checked by Python and independently by C++, and exact full-state controls. No Lean formalization, external mathematical review, priority determination, HC proof, or finite HC counterexample.

## 1. Literal target and results

A state is X=(B,p,h), with the COMPLETE finite black set B and h=N,E,S,W. White turns right (R), black turns left (L); flip, then move. Time t is before update t. Let L10 be the cyclic ten-letter factors of the fixed standard P104 word W. Recover the preceding nine turns by the literal inverse. J10(X) means that those nine letters followed by the current turn are not in L10. This is the same intrinsic event as in [ten-factor attraction](ten-factor-attraction.md), not a new event definition or a PG/S_D identification.

**Theorem 1 (exact next event).** On every complete finite input, the first future J10, or its permanent absence, is decidable. A finite answer returns its exact time AND the complete state after the event. A negative event answer returns a verified standard periodic suffix, not NO-HIGHWAY.

The result extends to complete finite fields supplied as XORs of M finite arithmetic segments with strides

    (0,0), (±2,±2), (±2,0), (0,±2), (±4,0), (0,±4).

Zero stride is a singleton. All lengths are positive finite integers; no infinite background is an algorithmic input. The complexity is polynomial in M and the binary bit size of coordinates and lengths, not in the represented black count or numerical waiting time. At most five periodic-plan computations and 1111 literal main-orbit updates are used. At most 1530 segment terms are added by a finite event call. True inverse history is computed on a copy and is not appended to the returned physical field.

**Theorem 2 (finite-macro geometry and deadline).** Put C(X)=conv(B union {p}) and W0=diam_infinity(B union {p}). If the next event occurs, every actual position and black cell through its outgoing update lies in

    C(X)+[-1959,1959]^2.

Its post-event time is at most

    212 W0 + 854199.

The unbounded continuation of an event-free standard tail is outside this finite-macro statement. Untouched initial black cells are included in C(X), not deleted.

**Theorem 3 (finite prefixes, no supplied geometric promise).** If n future J10 events exist, the time s_n just AFTER the nth one satisfies

    s_n <= n(212 W0+854199)+415308 n(n-1).                 (1)

The full history through these events stays inside C(X)+[-1959n,1959n]^2. Starting with M segment terms, their successive exact post-states have at most M+1530n terms. The first n events, or an earlier certificate of permanent absence, are computable in poly(M+n+b) bit operations, where b bounds the original coordinate/length bit sizes. Here n is numerical, not its binary description length. No bound on the total number of events is asserted.

For an explicit seed one can take M=|B|. For compressed inputs a readily computable safe width is the diameter of all segment endpoints and p; it may overestimate the actual XOR support width. All geometric theorems themselves refer to the actual complete support.

## 2. What was missing from the earlier J10 decision

The earlier O(m)-ordinary-update algorithm decided whether a future J10 exists, sometimes without reaching it. It did not always return its first time or complete post-event state, and its ordinary-work bound was in the explicit numerical black count. The older J13 macro already retained complete compressed history, but its finite graph had only simple recurrent components.

For J10, the physical 150-window graph has a non-simple 366-vertex component. Finite-state periodicity cannot be assumed there. We use the already proved all-parameter fold obstruction to give a genuine bounded rank INSIDE one event-free segment. This is not a rank for an unbounded succession of such segments.

The new proofs do not use the mass-defect inequality as an upper bound: that inequality supplies a lower bound on defects in low-growth trajectories and does not control their total supply.

## 3. Pinned base and finite-path coverage

The base contains every physically feasible 150-letter word all of whose ten-factors are in L10. Its 6605 edge words generate a graph G with 6501 vertices, the 149-letter prefixes/suffixes. Physical feasibility is exactly alternation of requested turns on consecutive reads of the same physical cell. This is the prior forbidden-word method, not claimed new here.

Every actual event-free continuation, once its 149-turn history is a G vertex, follows G. At most 149 nonviolating ordinary updates are needed to obtain such a vertex: afterwards the last 149 turns are wholly new, and if the next turn is legal their feasible 150-word is in the complete enumeration. If the next turn is illegal, it is returned as the event instead. This covers input time zero without inventing a periodic negative-time past.

The pinned graph has simple W and T components of lengths 104 and 24, and one component H with 366 vertices and 370 internal edges. The prior explicit quotient maps H to phases 0,...,101. There is an edge (j,B_j)->j+1 mod 102, plus (0,L)->75, where B is a 102-letter fold word beginning R. The short loop is A=L B_75...B_101, length 28. Their literal geometry is

    A: displacement (0,-4), heading restored;
    B: displacement (1,11), heading reversed.

Every internal H edge is checked against this quotient, not merely sampled. The already supplied all-parameter lemma is

    B A^n B A^m B is physically infeasible for ALL n,m>=0. (2)

Its explicit consecutive same-cell/same-R conflicts and their parameter coverage are in Section 4 of ten-factor-attraction.md. A finite word need not extend to an infinite legal word for (2) to apply. This is the essential finite-path rather than infinite-cycle input.

The base edge hash is `6b76e51621e15d2304f1c0baa28790cc267cabafca3fc03250dea8721b2b4794`; the quotient hash is `f6d5502737c0ce931c1f9ca62a62ad8307157b4133c8f087f7ac0268b0d05682`. The new runtime regenerates and checks these exact inputs. The old sources are unchanged.

## 4. A complete bounded-fold lift

Outside H keep each vertex v with counter 0. Inside H use (v,c), c=0,1,2,3, except that (v,3) with quotient phase 0 is forbidden. On an internal H edge increase c exactly when its quotient starts the long loop, namely phase 0 with appended R. All other internal edges keep c. On entry into H start c=0; on exit forget c. Disallow c>3 and disallow arrival at phase 0 with c=3.

This permits two complete B loops and a third incomplete B loop; a third *completed* loop is excluded. An initial partial loop is not charged, so no assumption is made about the path before H entry. Between three long-loop starts at phase zero there are powers of A, and completing the third yields (2). Thus every real finite event-free path lifts. H cannot be revisited after leaving it because G's SCC condensation is acyclic. Counter reset on reentry cannot therefore mask additional physical folds.

The lift may still contain impossible paths. It is an exclusion-safe overapproximation, not a claim that every lifted path is physical.

Complete reconstruction yields 7595 vertices and 7763 edges. Its ONLY cyclic SCCs are simple cycles of lengths

    24, 104, 28, 28, 28.

The 28-cycles are A phases at counters 0,1,2. The 24- and 104-cycles are the prior T and standard words. No claim follows from cycle lengths alone; the words and their nonzero displacements are checked too.

Assign to each condensation component the three weights (one cyclic-component visit, one noncyclic-vertex update, period): respectively (1,0,P) on a cyclic component, and (0,1,0) on a noncyclic singleton. Backward longest-path values are nonnegative and, over every condensation edge C->D, satisfy

    rank(C) >= weight(C)+rank(D)

coordinatewise. Terminal ranks dominate their own weights. Internal simple-cycle edges keep the same rank. All 7763 lifted edges are checked. The maxima of the three ranks are

    5, 956, 212.                                          (3)

Python uses the base's iterative two-pass SCC routine; the independent native checker reconstructs the lift and uses Tarjan SCCs. Sorted full edge and rank hashes agree. The certificate hashes are `1fe5c8d29ca8a3c4fda593242c875b9bcc00772df1f9bfbad21973f0169836bb` and `d7413c48613c78f693a96362bb0ece77ed764a1c9ab9653a6591719a27a26803`. Integer inequalities, complete reconstruction and (2), not a floating-point solver, carry the proof.

## 5. Exact physical acceleration on a simple component

At a cyclic vertex propose its internal periodic word u, of length P and nonzero displacement d, restoring heading. Let q_i be its phase read positions in the actual pose. At q_i+kd the required old-field contribution is determined by

    actual required turn bit = 1_B(q_i+kd)
       XOR #{(j,s): q_j-q_i=s d,
                    s>0 or (s=0 and j<i), 0<=s<=k} mod 2. (4)

This computes the literal first mismatch by induction up to that mismatch; it is not a finite-repeat heuristic. Prior-write changes occur at finitely many epoch thresholds.

For a finite segment a+jv, 0<=j<L, its intersection with a phase ray q+kd is empty, a singleton, or a finite arithmetic interval in k. Nonparallel directions use an exact determinant. For parallel directions solve the one-dimensional integer congruence after dividing by the greatest common divisor. In the closed stride family its epoch modulus is 1 or 2. This modulus matters: the 24-mode has axis stride 2 and the 28-mode axis stride 4. Treating every parallel intersection as a full interval would be wrong.

Split epochs into k=2z and k=2z+1. Each contribution is then an ordinary finite interval in z; each write threshold is a final interval. Sort parity-change endpoints separately for the two classes, including z=0 and the final infinite interval. This returns the exact earliest mismatch, or certifies none. All arithmetic is on integers of polynomial bit size.

Before a finite mismatch at t=nP+j, append P finite write segments for the full periods (if n>0), and j singleton writes for the partial period. These are XOR contributions; EVERY skipped write is accounted for. There are at most 2P-1 new terms. Shift the history vertex around its simple cycle by t mod P. Read the real cell and execute its actual update. If J10 is true, return the complete post-state. Otherwise the real edge must leave this simple component: the unique internal edge has the different predicted label. Continue in the lifted graph.

If no mismatch exists, the actual infinite continuation equals this cycle word. A finite field cannot realize the 24- or 28-word forever: their stabilized first-read classes require respectively two and five infinite initial black rays, as proved in the prior theorem. Hence only the standard cycle can give permanent absence. All earlier actual updates were individually checked or were legal cycle edges, so the certificate says no J10 at ANY nonnegative time, not only after its standard boundary.

A component is never revisited after exit. By (3), one call therefore uses at most five plans, at most 956 noncyclic updates, at most five cycle exits, at most 149 warm-up updates, and one final event update. A safe literal bound is 1111. The sum of visited cycle periods is at most 212, hence

    new terms <=149+956+2*212+1=1530.

The 2P allocation includes a possible non-event cycle exit. No skipped write or exit update is omitted. Periodic proposals and inverse-history computations use a copy until the actual endpoint is determined.

## 6. A generic finite periodic-plan halo lemma

This lemma concerns ANY supplied periodic turn word of length P restoring heading with d!=0, from a complete finite source Y=(B,p,h). Suppose its first mismatch is at time kP+i, position e=p+q_i+kd, with phase coordinates relative to p.

Let L be the largest positive translation threshold s with q_j-q_i=s d, or zero if none. Since a period has P unit moves,

    ||q_i||_infinity<=P,   L||d||_infinity<=P.

If k<=L then ||e-p||_infinity<=2P. If k>=L+1, all planned previous-write parities at phases i in epochs k-1 and k have stabilized. If the stable required old-field bit is 0, mismatch means e is an original black cell. If it is 1, the preceding occurrence matched, so e-d is an original black cell. Thus in every case

    e belongs to conv(B union {p})+[-2P,2P]^2.             (5)

Here B is the FULL source field before the plan, not an unknown active subset. For k>=1, any earlier phase point q_j+ell*d differs from (ell/k)(q_i+kd) by at most 2P in infinity norm. For k=0, all reads are within P of p. Therefore the entire finite planned read path through e is inside

    conv(B union {p})+[-4P,4P]^2.                         (6)

Its ensuing literal update enlarges this by at most one. Unchanged source cells remain present outside the read footprint; (6) never authorizes deleting them.

For radius R=max_{b in B}||b-p||_infinity (zero for empty B), (5)'s more precise alternatives give: either k<=L<=P, or k||d||<=R+||d||+P. Therefore the first mismatch time is strictly less than

    P(R+P+2).                                           (7)

These are conditional-on-first-mismatch bounds. A valid infinite plan has no finite halo bound.

## 7. All-input J10 geometry, time and bit complexity

Sum (6) over all finite periodic portions of one event call. The period sum is at most 212; all actual literal updates number at most 1111. Convex Minkowski enlargements compose, giving

    H=4*212+1111=1959.

Every intermediate complete state lies in the initial complete convex hull enlarged by H; in particular its width is at most W0+2H and its radius about its current head at most that width. Applying (7) to every periodic part, using P<=104, and including all literal updates, gives post-event duration at most

    212(W0+2H+106)+1111 =212W0+854199.                   (8)

After n-1 event calls width is at most W0+2H(n-1). Summing (8) gives (1), since 212H=415308. No theorem bounds n. In particular an infinite chain is not classified by the finiteness of each call.

The support of every newly appended segment is made of actual read positions. Thus all its endpoints lie in the same enlarged initial hull, even if it later cancels other terms. After n events, all coordinate and segment-length bit sizes are O(b+log(n+1)); event times also have O(b+log(n+1)) bits by (1). The number of terms is at most M+1530n. Each call performs a fixed number of ray/segment intersections, endpoint sorts and fixed-length literal or inverse operations. Exact set/list arithmetic therefore proves poly(M+n+b) bit complexity. Fixed constants may be large; this is not a benchmark or a claim polynomial in log n.

Together with the already proved H(X) iff finitely many J10 events, (1) implies that every hypothetical finite-support HC counterexample, of EITHER the nonstandard-periodic or nonperiodic type, has at least n intrinsic J10 events before every time T with (1)'s right side <=T. In particular its liminf event count divided by sqrt(T) is at least 1/sqrt(415308). This counts intrinsic events; interval-contained ten-factor counts differ only in the first nine boundary positions.

This is a lower rate requirement, not an upper event budget, a NO-HIGHWAY certificate, or a contradiction. The mass-defect lower bound and this timing bound can coexist with infinite renewal.

## 8. Failed bridge retained, and what the controls really check

A tempting shortcut was to equate absence of J10 with the standard 116-step black-memory bound on finite intervals. The saved 397-letter feasible word in attempt.json refutes this: its complete minimal input has 76 black cells, all contained ten-windows are legal, and the origin is read only at times 0 (R, black creation) and 396 (L, consumption). No intermediate origin read occurs. This refutes that 116 bound, NOT every possible larger bound, and is not a finite HC counterexample.

The new graph rank avoids that shortcut. It counts physical fold starts within an H traversal, not black age, black mass, or the number of all future J10 events.

Run `python scripts/check_ten_event_macro.py`. The disposable replay reconstructs the old pinned input witnesses only as necessary, then checks the new lifted graph, independently compiles the new C++ checker, compares the complete edge/rank hashes, rejects damaged rank and missing-word controls, and checks exact event times AND complete endpoint fields. Actual counts are recorded in checked_report.json.

The sparse 28-black remote-marker family at distance parameter n is returned at its exact first event 104n-92, including n=10^60, with 34 literal main-orbit updates and one plan in this implementation. Equality of its returned field with a separate direct periodic-write construction is EXTENSIONAL XOR equality, not equality of expression lists. The capped 24-mode finite family at n=10^60 is certified event-free through its long transient using two plans and 138 ordinary updates, from a 45-term mature input. It has enormous but finite support. The unprotected finite 28-rail also returns its first event rather than being confused with an infinite black background.

Initial control-code mistakes compared differently split XOR expressions for syntactic equality and used an unshifted T word after a 150-step advance. They were corrected before the passing replay. They are not suppressed successful tests. The physical macro source and all future certificates were checked after those corrections.

## 9. Status in the HC proof graph

Completed: a finite physical fold rank for one event-free interval; exact first-J10 time and complete-state closure on compressed finite fields; constant finite-macro halo; explicit quadratic nth-event deadlines and polynomial bit-time bounded event-prefix computation.

Unproved: finiteness of J10 on every finite seed; a rank across arbitrarily many fresh macro calls; a certified negative finite seed; unrestricted HIGHWAY decidability/nonrecursiveness; all-input nonuniversality; HC. The loop counter resets legitimately for a new event macro, so it is NOT the missing global rank. No fresh-language or geometric promise is attached to the input in Theorems 1--3.
