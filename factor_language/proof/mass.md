# A sharp finite-word mass deficit and an all-input defect inequality

Classical square-lattice Langton ant, white/right, black/left, flip then move. A state is observed before the update. All finite black fields below are COMPLETE. Evidence: analytic coverage and telescoping arguments plus two independently implemented exhaustive finite kernels. The analytic proof is not Lean-formalized. The result supplies neither HC nor a finite HC counterexample.

## 1. Statements

Fix the standard 104-letter word W in audit.py. Let L10 be all its cyclic length-ten factors. For a finite word v, set g(v)=#R-#L and D(v)=3|v|-26g(v). Call v ten-legal if every length-ten factor contained in it belongs to L10; for words shorter than ten this condition is vacuous. Call v physically feasible if some initial colouring and pose execute it.

**Theorem 1 (all finite lengths).** Every physically feasible ten-legal finite word satisfies

    D(v) <= 322.

In fact D(v)<=284 when |v|>=300. The constant 322 in the unrestricted-length statement is sharp. The asymptotic mass rate 3/26 is sharp: no estimate g(v)>=rho*|v|-C with rho>3/26 and fixed C holds for all such words.

**Theorem 2 (no language promise on the input).** Let X_t=(B_t,p_t,h_t) be any literal orbit from a finite black field. For integers s<=t, let N10(s,t) count forbidden ten-letter factors wholly contained in its turn word a_s...a_(t-1). Equivalently, count bad windows ending at indices j with s+9<=j<t. Then

    3(t-s)-26(|B_t|-|B_s|) <= 351 N10(s,t)+322.             (1)

There is no width, drift, retreat, eventual-periodicity, future-language or active-core hypothesis in (1). The count includes neither unknown future windows nor negative-time history. The value 351 is a valid bound, not asserted optimal.

For the intrinsic J10 predicate of the ten-factor package, let Nint10(s,t) count all its occurrences at s<=j<t. Then Nint10>=N10, and (1) also holds with Nint10 on the right. This distinction matters for sharpness: the displayed 90-step equality witness has two intrinsic boundary violations but zero forbidden windows wholly contained in its word. The sharp constant assertion uses N10, not Nint10.

## 2. Exact finite-word feasibility and enumeration coverage

A prescribed turn word fixes its geometric path from (0,0),N. It is physically feasible exactly when successive reads of each physical cell request opposite turns. Necessity is the flip rule. For sufficiency, put an initial black cell precisely at each visited position whose first request is L, and leave all other positions white. Induction realizes the entire word. The required seed is finite. Arbitrary poses follow by translation and quarter turns.

This elementary criterion is prior methodology, as in Gajardo's symbolic forbidden-word treatment; it is not claimed as new. It implies in particular that finite-word feasibility is the same whether initial colourings are required to be finite or are arbitrary.

Starting at the empty word, branch on BOTH turns. Reject an extension exactly if its new ten-factor is forbidden, or its current cell was previously read with the same letter. Induction on length proves complete enumeration of physically feasible ten-legal words through depth 300. Words of lengths below ten are NOT initially restricted to the standard factor table.

The Python implementation uses breadth-first cloned last-read maps. The C++ implementation instead uses depth-first reversible current-colour assignments. No seed-size or spatial cutoff is used. Their complete sorted depth-300 edge sets and their integer potentials have identical hashes.

## 3. The finite graph certificate covers arbitrarily long finite words

Form a graph from EVERY accepted word of length 300: its 299-prefix is the source, its 299-suffix the target, and the appended letter labels the edge. There are exactly 29,334 vertices and 29,559 edges. Assign the weight

    w(R)=-23, w(L)=29,

so that D(v) is the sum of its letter weights.

The certificate assigns a nonnegative integer h(u) to each vertex, with maximum 251, and verifies EVERY edge inequality

    h(u) >= w(c)+h(v),               u --c--> v,             (2)

and EVERY initial-vertex inequality

    D(u)+h(u) <= 284.                                       (3)

These are direct integer comparisons; an optimizer's output is not trusted. The potential generators are only proposal generators. Their resource caps raise an error with no mathematical conclusion. An independently supplied damaged potential is rejected without repair.

For any physically feasible ten-legal finite word z of length n>=300, all its 300-windows belong to this graph. They define a path starting with its first 299 letters u0. Summing (2) over the appended letters gives

    D(z) <= D(u0)+h(u0)-h(u_final) <= 284,

using (3) and h>=0. This is an overapproximation argument: not every graph path need be physically realizable, but every physical word is covered. No extension to an infinite ten-legal path is assumed. There is no misuse of eventual-cycle classification for a finite segment.

For all lengths 0 through 299, exhaustive enumeration gives maximum 322. Combining the two finite kernels proves Theorem 1 for ALL finite lengths.

Frozen reconstruction hashes (sorted text, one item per line):

- depth-300 words: e935203b28d1e73cebb853a7d7a96c349f26c3c4f66b13ceabe3b8124919808c;
- nonnegative potentials in lexicographic vertex order: f9237bef39462114273c87b585028c028b2b126a4270a2aa8bbe9e22eb1211a3.

The complete finite sets are reconstructed deterministically and checked against these hashes and the local inequalities. They need not be stored as a nine-megabyte enumeration dump. witness.json contains the immutable numerical claim, exact short witness and its complete minimal seed.

## 4. Sharpness

The word

    LLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLL

has length 90, 44 right turns and 46 left turns. It is physically feasible and all of its 81 ten-factors are allowed. Its unique minimal first-read seed has 28 black cells and is listed in witness.json. Literal execution leaves 26 black cells. Thus

    3*90-26*(26-28)=322,

proving the additive constant in Theorem 1 and in (1), with wholly contained windows, cannot be decreased.

The standard word has 104 updates and 12 more R than L. Its certified finite-support realization supplies physically feasible words W^k for every k>=1. Thus any uniform lower estimate g>=rho*n-C with rho>12/104=3/26 fails as k tends to infinity. The standard tail is an existing certified input here; this work does not re-prove HC or claim to discover that standard mass growth. The supplementary literal W^4 check is a control, not the justification of the universal k quantifier.

## 5. Derivation of the unrestricted inequality

In any actual finite orbit segment, every right turn increases complete black mass by one and every left turn decreases it by one. Hence

    g(a_s...a_(t-1))=|B_t|-|B_s|.                            (4)

Remove each letter that ends a forbidden ten-window wholly contained in the segment. These N=N10(s,t) single-letter positions separate at most N+1 consecutive remaining runs. Every ten-window wholly inside a remaining run was wholly inside the original segment and cannot be forbidden: otherwise its last position would have been removed. Each run is a genuine physical subword and is therefore covered by Theorem 1. An empty run has deficit zero and may harmlessly be charged the same upper bound.

Each removed letter has deficit at most 29. Additivity of D, Theorem 1 and (4) yield

    D(total) <= 322(N+1)+29N = 351N+322,

proving (1). This does not require disjoint forbidden windows. Removing their ending letters handles overlaps exactly.

## 6. Consequences for HC and what remains unproved

For s=0, (1) implies

    N10(0,t) >= [3t-26(|B_t|-|B_0|)-322]/351.                (5)

The count is a nonnegative integer, so one can also take the positive part and ceiling. In particular:

- If |B_t|=o(t), liminf N10(0,t)/t >= 1/117.
- If N10(0,t)=o(t), liminf |B_t|/t >= 3/26.
- If limsup |B_t|/t <= alpha < 3/26, then liminf N10(0,t)/t >= (3-26alpha)/351.

For a proposed expanding-shuttle orbit with complete checkpoint mass O(n), checkpoint time Omega(n^2), and only O(n) forbidden ten-factors through that time, (1) is a contradiction. Such a shuttle would have to generate linearly many local violations in elapsed time, not merely a bounded number per long sweep. This is a necessary-condition obstruction to that specified architecture; it does not rule out every shuttle or every HC counterexample.

These results use all finite initial states, not a promised ten-legal future. Nevertheless (5) is a LOWER bound on violations when mass is small, not an upper event budget. Black cells can keep being created. Neither linear black growth nor a small violation density proves standardness. The quantity D is not a global monotone rank because a general trajectory can pay for arbitrarily many positive deficits using violations.

Thus no all-input J10 finiteness theorem, certified finite negative seed, HIGHWAY decision theorem, or nonuniversality theorem follows. The current missing bridge remains prevention or construction of indefinitely regenerating violations from one finite seed. The earlier ten-factor attraction theorem is compatible but is NOT needed to prove (1).

## 7. Evidence, reproduction and source boundary

Run `python3 factor_language/verification/mass/reproduce.py` from the repository root (Python standard library plus a C++17 compiler). A disposable replay independently reconstructs all kernels, compares both sorted edge and potential hashes, tests a damaged native potential without modifying it, and runs literal complete-field controls. witness.json is immutable unless the separate explicit `audit.py --generate` mode is requested. That generation mode is not called by reproduce.py.

The final replay checked 2,816,005 C++ DFS nodes, all 29,559 integer edge inequalities, 128 arbitrary finite seeds, 192,128 prefix inequalities and 16,384 arbitrary-interval inequalities. Sixteen test inputs retain remote black cells with coordinates of size 10^60. The controls supplement rather than replace Sections 2, 3 and 5. The 90-step equality witness was replayed with its full field.
