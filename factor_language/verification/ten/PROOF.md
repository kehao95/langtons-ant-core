# Ten-factor highway attraction with a sharp cardinality coefficient

**Date:** 15 October 2026. **Repository read:** `0bcaad6ce318b79479f03e9c9d89cb3fcd4d4489` in `kehao95/langtons-ant`.

**Status:** complete analytic reduction and all-parameter arguments below, together with exact finite certificates checked by two implementations. Not Lean-formalized, externally mathematically reviewed, or certified novel. This is a research-paper candidate, not an HC proof or a finite HC counterexample. Only the new theorem-local checks are replayed. Earlier shared repository modules are not modified.

## 1. Statements and the precise quantifiers

A complete state is $X=(B_0,p,h)$ on $\mathbb Z^2$. White turns right (R), black turns left (L), then the current cell flips and the head moves one edge. Headings are N,E,S,W, numbered 0,1,2,3. Time $t$ is before update $t$. Initially $B_0$ is finite except where arbitrary colourings are explicitly allowed. No wall, prescribed strip, bound on retreat, or future-active deletion is part of the dynamics.

Let $W$ be the fixed standard 104-letter word in the appendix. Let $\mathcal L_k$ be the set of its cyclic length-$k$ factors. A one-sided infinite turn stream $a$ is **$k$-legal** if every forward factor $a_t\cdots a_{t+k-1}$, for every $t\ge0$, belongs to $\mathcal L_k$. This premise concerns ALL future windows, not one finite observation.

**Theorem A (three eventual modes).** Every 10-legal classical-ant stream on an arbitrary initial colouring is eventually a phase of $W^\omega$, $U^\omega$, or $T^\omega$, with least periods 104, 28, and 24 respectively. In particular it is eventually periodic. Periodicity is a conclusion, not a premise.

**Theorem B (cardinality-controlled attraction).** If $B_0$ is finite, $m=|B_0|$, and the stream is 10-legal, then it is eventually standard $W$, and its first standard-entry time satisfies

$$\tau(X)\le 12m+212.$$

This bound is independent of the coordinates and diameter of the COMPLETE initial black set. The coefficient 12 is optimal among uniform affine bounds: an explicit family below has $m_n=2n+13$ and $\tau_n=24n-3$ for every $n\ge1$. No optimality of the additive constant 212 is claimed.

**Theorem C (sharpness for arbitrary-colouring periodicity).** There is an explicitly specified computable infinite initial colouring whose classical-ant stream is 9-legal but not eventually periodic. Consequently 10 is the least factor length forcing eventual periodicity on arbitrary initial colourings.

This is NOT a claim that 10 is the least length forcing eventual standardness on FINITE supports. Such a claim would require a finite nonstandard example for length nine. The infinite-background example is not an HC counterexample.

**Theorem D (all-input local-target decision).** Let $J_{10}(X)$ mean that the true preceding nine turns, recovered by nine inverse updates, followed by the current turn form a word outside $\mathcal L_{10}$. This is a fixed radius-at-most-nine local predicate. On every finite input, existence of any future $J_{10}$ is decidable in polynomial bit time in the sparse binary-coordinate input size. The algorithm advances the main trajectory by at most $12m+221$ updates, plus 104 lookahead updates on a copy and nine inverse updates. It does not always return the event's first occurrence time.

It follows that $H(X)$ is equivalent to finitely many future $J_{10}$ events. The missing all-input event-FINITENESS assertion is not supplied here. No claim of a total HIGHWAY algorithm follows.

## 2. Finite-word feasibility and graph coverage

For any finite prescribed turn word, the geometric path is fixed after choosing an initial pose. It is physically realizable if and only if consecutive reads of each same physical cell have alternating letters. Necessity is the flip rule. For sufficiency, make a visited cell initially black exactly when its first requested letter is L; leave every unvisited cell white. Induction over the finite word proves execution. This is established methodology, not a new criterion; see Gajardo (2003), Section 3.

Let $E$ contain EVERY physically feasible 150-letter word whose 10-factors lie in $\mathcal L_{10}$. Construct a graph $G$ with edge $v_0\cdots v_{148}\to v_1\cdots v_{149}$ for each $v\in E$. No word is removed because it looks unlikely or because its seed is large. Complete enumeration follows all whitelist-compatible extensions and rejects exactly the same-cell alternation conflicts. Induction on word length proves completeness of that enumeration.

Any actual infinite 10-legal stream gives an infinite path in $G$, since each of its length-150 windows is feasible under its own actual execution. The graph can admit paths that fail longer physical consistency. It is an OVERAPPROXIMATION; this does not invalidate exclusion, but prevents interpreting every graph path as a physical orbit.

The immutable certificate `certificates/windows10.txt` contains 6,605 edge words. Both verifiers regenerate the entire set and require exact equality, including cardinality and absence of duplicates. Their complete graph has 6,501 vertices and precisely three cyclic strongly connected components:

| Component | Vertices | Internal edges | Structure |
|---|---:|---:|---|
| $\mathcal W$ | 104 | 104 | exact standard simple cycle |
| $\mathcal T$ | 24 | 24 | exact $T$ simple cycle |
| $\mathcal H$ | 366 | 370 | not a simple cycle |

There are no other cyclic components, including self-loops. The first two component edge sets equal all cyclic length-150 factors of $W$ and $T$. Strongly connected components and reachability are checked on the full graph, not only on a pruned experimental sample.

The non-simple component is crucial: ordinary finite-state periodicity reasoning cannot dispose of it. It is dealt with next by an all-length physical conflict, rather than by assuming its paths are periodic.

## 3. Exact two-loop description of the non-simple component

The certificate `quotient.tsv` assigns each of the 366 vertices of $\mathcal H$ a state in $\{0,\ldots,101\}$. It is a label-preserving homomorphism onto this explicit graph:

- for each $0\le i<102$, the edge labelled $B_i$ leads from $i$ to $i+1$ modulo 102;
- one additional edge, labelled L, leads from 0 to 75.

Here $B$ is the 102-letter word in the appendix, $B_0=\mathrm R$, and the alternative short loop is $A=\mathrm L B_{75}\cdots B_{101}$, of length 28. Every one of the 370 internal edges is checked against this formula. The homomorphism is used only in the forward direction: every infinite internal path projects to a word that, after at most 101 letters, is an arbitrary concatenation of $A$ and $B$.

The edge label is the letter APPENDED to the 149-letter history. It is shifted 149 places from the original stream. This finite shift is harmless for eventual-mode classification. Section 5 instead uses the CURRENT letter $v_0$ of a future-window vertex, and does not confuse these conventions.

The exact geometric data, starting north at the origin, are

$$A:(0,-4),\ h=0;\qquad B:(1,11),\ h=2.$$

Thus $A$ translates and $B$ reverses the heading. The $A$ word is a cyclic phase of $U$.

## 4. Three foldbacks are impossible, at every pair of lengths

**Lemma 1.** For every pair of integers $n,m\ge0$, the finite word $B A^n B A^m B$ is physically infeasible, independently of its initial colouring.

In each case below there are two consecutive visits to a cell $q$ both requesting R:

| Parameter range | $q$ | Earlier time | Later time |
|---|---|---:|---:|
| $n=0$ | $(0,2)$ | 32 | 184 |
| $n\ge1,\ m\ge n$ | $(0,2)$ | 32 | $184+56n$ |
| $n\ge1,\ 0\le m<n$, $r=n-m$ | $(1,4r)$ | $25+28r$ | $205+28(n+m)$ |

All times are pre-update indices in the displayed finite word. It suffices to verify their consecutiveness, not that the rest of the candidate word is feasible.

**Proof.** Let the five block boundaries start at times 0, 102, $102+28n$, $204+28n$, and $204+28(n+m)$. Their respective poses are $(0,0),N$; $(1,11),S$; $(1,11+4n),S$; $(0,4n),N$; and $(0,4(n-m)),N$.

The following finite coordinate facts are computed directly from the two displayed words and checked independently: $A$ has $-3\le x\le0$; on its column $x=0$ the pairs (index, height, letter) are

$$ (0,0,L),(7,-1,R),(8,-2,R),(15,-3,L),(16,-2,L),(27,-5,L).$$

In $B$, the only visit to $(0,2)$ is index 32, R. All $B$ visits at $x=0$ have $y\le2$. Visits to $(1,9)$ are indices 82,R and 90,L; visits to $(1,4)$ are 45,L and 53,R; visits to $(1,8)$ are 73,L and 81,R. On $x=1$ its maximum height is 12.

If $n=0$, the reflected second $B$ reads $(0,2)$ at its local $(1,9)$, index 82. The previous visit is the first $B$'s index 32. This gives the first row.

If $n\ge1$, the first $A$ run lies at $x\ge1$, so cannot revisit $(0,2)$. In the second $B$, a visit there would require local $(1,9+4n)$, above every $x=1$ visit. In the second $A$ run, the first matching copy is number $n-1$ (zero-based), at local index 8, with letter R. All earlier copies miss: on $x=0$ their required local height is below -5. The visit time is $204+28n+28(n-1)+8=184+56n$. This copy exists when $m\ge n$.

Finally let $r=n-m>0$. For $r=1$ or 2, the last earlier visit to $(1,4r)$ is the first $B$'s index 53 or 81, both R. The first $A$ run lies at heights at least 11 and cannot reach those two cells. For $r\ge3$, the last visit in the first $A$ run is copy $r-3$, local index 7, R, at time $102+28(r-3)+7=25+28r$. The column-$x=0$ list for $A$ shows no later visit to that cell in the run; any visit in the first $B$ precedes it. A visit by the second $B$ would require local $(0,11+4m)$, impossible since its column-$x=0$ maximum is 2. The second $A$ run lies at $x\le0$. The third $B$, based at $(0,4r)$, first reaches $(1,4r)$ at index 1, R. This proves the third row and the lemma. QED.

An infinite concatenation of $A$ and $B$ with infinitely many $B$'s contains a forbidden three-$B$ subword. Hence it has only finitely many $B$'s and is ultimately $A^\omega$. This argument disposes of arbitrary interleavings and unbounded run lengths, not only tested values of $n,m$.

An infinite path in a finite graph eventually remains in one cyclic strongly connected component. In $\mathcal W$ and $\mathcal T$ it is forced periodic by the simple cycles. In $\mathcal H$ the preceding homomorphism and Lemma 1 force an $A$-periodic suffix. This proves Theorem A.

## 5. Finite support and the transient bound

For a heading-resetting periodic word of length $P$ with nonzero drift $d$, partition its phase positions by differences in $\mathbb Z d$. For a class write $q_i=b+a_i d$. Visits to $b+nd$ are eligible when $a_i\le n$, and their chronological order is decreasing $a_i$, then increasing $i$. A cell's required initial colour is the first letter of that ordered eligible list. This is the full-drift chronology method of Jillhewar (2026), Theorem 3.1 and Remark 3.2.

The words $U$ and $T$ pass all per-cell alternation tests but have respectively five and two stabilized classes starting L. Each such class demands infinitely many DISTINCT initially black cells. Neither word can be executed forever from finite support. Any finite prelude preserves finite support, so these modes also cannot occur as eventual tails of a finite-support orbit. Consequently every finite-support infinite 10-legal path eventually enters $\mathcal W$.

The complete graph gives 925 vertices that can reach $\mathcal W$. They exclude $\mathcal H$ entirely and include $\mathcal T$. Apart from $\mathcal W$ and $\mathcal T$, they are acyclic. A path cannot leave a strongly connected component and later return to it. The current letters of a run of $L$ successive vertices in $\mathcal T$ form a length-$L$ prefix of a phase of $T^\omega$.

Let $b_j(L)$ count distinct cells whose FIRST read is L in this prefix starting at phase $j$. If the complete black mass at the run's start is $m_T$, physical execution requires $b_j(L)\le m_T$. The count includes only first reads relative to that run; cells written during the run cannot pay for them.

**Lemma 2.** For all phases $j$ and all integers $L\ge0$,

$$L-12b_j(L)\le5.$$

**Proof.** Chronological classes give the first-L read times as a finite set $F_j$ and two arithmetic rays $r_{j,1}+24\mathbb N$, $r_{j,2}+24\mathbb N$. Their exact table is in the appendix. The sets count distinct physical cells, not repeated L reads. Put $D_j=\max(\{0\}\cup\{f+1:f\in F_j\}\cup\{r_{j,1},r_{j,2}\})$. For every $L\ge D_j$, directly from these rays,

$$b_j(L+24)=b_j(L)+2.$$

Thus $L-12b_j(L)$ is 24-periodic for all $L\ge D_j$. Checking the finite interval $0\le L<D_j+24$ covers all lengths. Both implementations derive the class table independently and verify that the maximum across all phases is 5. This is an exact finite reduction with its all-length periodicity proof, not a finite-prefix extrapolation. QED.

Before its first $\mathcal T$ vertex a path uses only the 54 acyclic strict ancestors of $\mathcal T$. Give such a vertex $v$ weight

$$c(v)=1+12\delta(v_0),\qquad \delta(R)=1,\ \delta(L)=-1.$$

Complete acyclic dynamic programming gives maximum total weight 70 for a path ending at $\mathcal T$. Therefore if $t_{pre}$ updates precede that run and their net black change is $\Delta$, then $t_{pre}+12\Delta\le70$ and $m_T=m+\Delta$. After departure from $\mathcal T$, the maximum acyclic path length before $\mathcal W$ is 137. The exit-producing update from a $\mathcal T$ vertex is included in its $T$-prefix, not omitted. By Lemma 2,

$$\tau\le t_{pre}+(12m_T+5)+137\le12m+70+5+137=12m+212.$$

Paths avoiding $\mathcal T$ altogether have length at most 167 before $\mathcal W$, also below this bound. A path whose initial vertex is already in $\mathcal W$ has zero such entrance time. Once the path first reaches $\mathcal W$, leaving it would preclude a later return; because its eventual component must be $\mathcal W$, it never leaves. Its future is standard from that time.

These are future-window vertices at times starting at ZERO. There is no artificial 149-update warm-up in the mathematical transient bound. Every complete initial black cell remains in the physical state; only its count is used in this inequality. Theorem B's upper bound follows.

## 6. An explicit family attaining coefficient twelve

Define

$$E=\{(-2,-1),(-1,0)\},$$

$$D=\{(-1,-4),(-1,-3),(0,-5),(0,-3),(0,-2),(1,-6),(1,-5),(1,-4),(1,-3),(2,-3),(2,-2)\},$$

$$R=\{(-2,0),(-1,-1),(-1,0),(0,-1),(1,-1),(1,0)\}.$$

For $n\ge0$, put

$$B_n=E\ \cup\ \{(-2,-2j),(0,-2j-1):1\le j\le n\}\ \cup\ (D+(0,-2n)).$$

These sets are disjoint. Start north at the origin with exactly $B_n$ black and all other cells white. Then $|B_n|=2n+13$.

The word $T$ has read footprint within $[-2,1]\times[-3,0]$, net displacement $(0,-2)$, and resets heading. For every $n\ge1$ its required initial black cells in that footprint are precisely $E\cup\{(-2,-2),(0,-3)\}$. All later rail cells and all cap cells are outside the footprint. The complete 24-step parity of visits, followed by set cancellation, gives the identity

$$F^{24}(B_n,0,N)=\big((B_{n-1}+(0,-2))\mathbin{\dot\cup}R,\ (0,-2),N\big).$$

This is an identity of FULL states, not a core-only recurrence. A direct all-parameter derivation is: translate the rail terms with $j=1,\ldots,n-1$ by -2; they become the original terms $j=2,\ldots,n$. The cap becomes $D+(0,-2n)$. Only the fixed finite set $E$, the first rail pair, and the translated $E$ remain to compare, and their difference with $R$ equals the exact net toggle set of $T$. This finite equality is checked. It also covers $n=1$ where the shorter rail is empty.

The residual $R$ is at heights -1 and 0. Every future repeated $T$ segment based at height -2 or less remains strictly below it. The $n=0$ complete state is the clean seed of the standard phase $Z$ in the appendix; its full infinite execution is verified by chronology and an independent epoch-breakpoint formula. Its phase footprint has maximum height zero and drift $(-2,-2)$, so its continuation from height -2 also stays below $R$. Induction therefore retains and guards ALL successive residuals and proves the exact infinite word

$$T^n Z^\omega.$$

The factors of $T^2Z^2$ verify every possible length-10 junction; $T^\omega$ and $Z^\omega$ are themselves 10-legal. The last three letters of $T$ and $Z$ agree, but the last four do not. Since $Z$ has least period 104, any earlier standard future agreeing with $Z^\omega$ must be its unique phase-aligned left extension. Hence the first standard time is

$$\tau_n=\max(0,24n-3).$$

For $n\ge1$, $\tau_n=12|B_n|-159$. An affine upper bound with slope less than 12 and fixed intercept fails for large $n$. This proves the sharp coefficient, without claiming 212 is sharp. Every member of this family is H-positive.

## 7. Nine factors admit an aperiodic infinite-background spiral

Let $U$ and $C$ be the 28- and 89-letter words in the appendix and let $n_i=5\cdot2^i$. Consider

$$a=\prod_{i=0}^{\infty} U^{n_i}C.$$

The prescribed geometry is explicitly computable, starting at the origin heading north. Its all-future physical feasibility follows from the next separation proof; it is not assumed.

A $U$ block restores heading, moves $(0,-4)$, and has footprint in $[0,3]\times[-5,0]$. A $C$ block rotates the heading counterclockwise, moves $(13,-4)$, and has footprint in $[0,14]\times[-4,0]$. The finite word $UCU$ is feasible. Every length-9 factor of $U^2CU^2$ is in $\mathcal L_9$.

The start heading of macro $i$ is $-i$ modulo four. For $S=16^k$, the four consecutive start positions are

$$p_{4k}=(-8S+8,4S-4),\quad p_{4k+1}=(-8S+21,-16S-8),$$
$$p_{4k+2}=(32S+25,-16S+5),\quad p_{4k+3}=(32S+12,64S+9).$$

These follow by the two block displacements; one group of four returns the heading and replaces $S$ by $16S$. Entire macro read footprints lie in the respective rectangles

| Index | x interval | y interval |
|---|---|---|
| $4k$ | $[-8S+8,-8S+22]$ | $[-16S-8,4S-4]$ |
| $4k+1$ | $[-8S+21,32S+25]$ | $[-16S-8,-16S+6]$ |
| $4k+2$ | $[32S+11,32S+25]$ | $[-16S+5,64S+9]$ |
| $4k+3$ | $[-128S+8,32S+12]$ | $[64S-5,64S+9]$ |

Each rectangle is disjoint from all nonadjacent earlier rectangles. For the first row, $k\ge1$, earlier rectangles through $4k-2$ have $x\ge-S/2+8$, while the new maximum is $-8S+22$; use $15S>28$. For the second row, earlier rectangles through $4k-1$ have $y\ge-S-8$, while the new maximum is $-16S+6$; use $15S>14$. For the third row, earlier rectangles through $4k$ have $x\le2S+25$, while the new minimum is $32S+11$; use $30S>14$. For the fourth row, earlier rectangles through $4k+1$ have $y\le4S+9$, while the new minimum is $64S-5$; use $60S>14$. The first two empty-earlier-set base cases are automatic. These inequalities hold for every $S=16^k$ in the stated ranges.

It remains to control adjacent macros, which are not claimed disjoint. In local coordinates of the earlier macro, the next macro begins at $(13,-4n_i-4)$ heading west. Its first $U$ block can overlap the earlier $C$, but every later $U$ block has $x\ge17$ while $C$ has $x\le14$; the next $C$ is still farther right. The preceding $U$ rail has $x\le3$, so is disjoint from the next macro. Within one macro, $C$ can meet only the LAST $U$ block: every earlier $U$ block has minimum height at least $-4n_i+3$, above $C$'s maximum $-4n_i$. Thus all interactions with $C$ are contained in the verified word $UCU$. Other repetitions are portions of the physically feasible $U^\omega$ trace. This proves alternating letters at every consecutive same-cell pair in the entire infinite word.

Colour a cell initially black precisely when its first prescribed read has letter L; leave unvisited cells white. The proved consistency makes this a genuine infinite classical-ant execution by induction over time. This colouring is computable: for a queried cell of infinity-norm $M$, choose $k$ with $16^k>M+100$. Every rectangle from macro $4k$ onward lies outside $[-M,M]^2$ in at least one coordinate, so only the first $4k$ finite macros need be searched. It has infinite black support, since interior portions of arbitrarily long $U$ rails demand fresh initial black cells.

The word $D_{bad}=\mathtt{RLRRRRLRRL}$ is absent from $\mathcal L_{10}$ and occurs exactly once in each connector $C$, at offset 11. The finite check of $U^2CU^2$ excludes other occurrences at either junction, and $U^\omega$ has none. Successive occurrences are separated by $89+28n_{i+1}$, which grows without bound. An eventually periodic sequence with infinitely many occurrences of a fixed finite factor has bounded gaps between them. Hence $a$ is not eventually periodic. This proves Theorem C, including its explicitly infinite-background boundary.

## 8. A radius-nine target decidable without waiting for a remote collision

The inverse of a literal step is unique: from post-pose $(p,h)$ set $q=p-\mathrm{dir}(h)$, undo the flip at $q$, and undo the turn dictated by that recovered colour. Nine inverse steps read only cells within distance nine of the current head. Therefore the preceding-nine-turn test $J_{10}$ is an intrinsic finite-local predicate, including at input time zero.

Let $M=12|B_0|+212$. The following total algorithm acts on an arbitrary finite input, with no legality promise:

1. Recover the true nine-turn past. Simulate up to time $M$, checking $J_{10}$ before each update. Return YES with its first time if encountered.
2. At time $M$, test the complete-state predicate $P_{now}$ for permanent standard P104. If it fails, return YES (a future event is forced by Theorem B). This is not an assertion that the event was observed or that its first time has been computed.
3. If $P_{now}$ holds, simulate nine additional updates to check all windows crossing this boundary. Return YES if one is bad; otherwise return NO. All subsequent windows are inside the certified standard future.

Why is the second step sound? Absence of every future $J_{10}$ implies legality of every forward length-10 window from time zero. Theorem B would force $P_{now}$ by time $M$, contradicting the failed test. A far-away blocker cannot be omitted from that test.

The exact $P_{now}$ test first simulates 104 turns on a copy. If they do not equal any phase of $W$, it returns false. Otherwise let $K$ be the unique clean finite seed for that placed phase, computed by the chronological class formula. Let $q_i+\mathbb N d$ be its 104 future phase rays. The actual complete field realizes that future if and only if

$$(B\triangle K)\cap\bigcup_{i=0}^{103}(q_i+\mathbb N d)=\varnothing.$$

Sufficiency follows by first-difference induction; necessity follows at the first read of an initial differing cell. Testing finitely many complete-field points against 104 integer rays is exact, including arbitrarily distant markers. No repeated-prefix heuristic is used.

During the $O(m)$ ordinary updates the complete field has $O(m)$ cells, and coordinate bit lengths grow by only $O(\log(m+1))$ beyond their input sizes. Exact finite-set operations and integer ray tests therefore give a deterministic polynomial bit-time implementation (a balanced search tree can be used instead of hashing). The implementation uses Python integers and finite sets; even worst-case linear set lookups remain polynomial. There is no claim of a polynomial bound for the numerical first-event time or of a bound polynomial in the bit length of a COMPRESSED black count.

### A fixed-mass late-event control

`certificates/far_marker.json` gives a complete 27-black standard state at a mature phase. Add one black marker at $(2n,2n)$ for any $n\ge20$. The new complete mass is always 28. The first contact is exactly at update $104n-92$, and it changes a prescribed R into L, forming the forbidden ten-factor `RRRLLLLRLL`.

The all-parameter first-contact calculation is: for the supplied phase positions $q_i$, write $q_i=s_i(2,2)$ whenever possible. The first visit to the marker has time $104n+\min_i(i-104s_i)$. The minimum is -92, attained at phase 12, and all relevant epochs are nonnegative for $n\ge20$. The marker is outside the finite true nine-step inverse history and the seed. Until contact, first-difference coupling preserves the entire standard path. The standard cyclic preceding nine letters and the changed L give exactly the stated bad factor.

For $n=10^{12}$ the first event is at $103999999999908$, but the new decision algorithm returns a forced-future YES after only 548 main-trajectory updates. The extra operations are nine inverse updates and the constant lookahead and ray tests, not simulation to the event. This family illustrates the distinction between reachability decision and event-time observation. It is not an HC negative family.

## 9. Relation to HC, previous work, and independent-paper scope

For finite states, if $J_{10}$ is absent after time $T$, all forward windows from that time are legal, so Theorem B applied to the COMPLETE state $F^T X$ gives eventual standardness. Conversely any standard future has only finitely many intrinsic violations, since after nine updates the true history is within that future. Therefore

$$H(X)\ \Longleftrightarrow\ \#\{t\ge0:J_{10}(F^tX)\}<\infty.$$

The present work does not prove the right side for arbitrary finite inputs, construct a finite negative seed, or show that every possible future event chain terminates. In particular, the theorem's $12m+212$ is NOT an unrestricted HC entry bound.

The earlier local-factor package proved sharp IMMEDIATE-standardness thresholds 21,14,13 in three different domains. The present conclusion allows a transient, weakens the whitelist to ten, analyzes a non-simple recurrent graph rather than only simple cycles, gives an unbounded-parameter physical foldback exclusion, and obtains a sharp cardinality coefficient. Its arbitrary-background nine-factor spiral establishes a different, precise optimality claim. These are new mathematical statements relative to that package, not a recounting of its numerical threshold.

A defensible publication unit is the combined ten-factor eventual-mode theorem, sharp finite-mass slope, and all-input target algorithm. The earlier immediate-rigidity results can be integrated as a companion section rather than fragmented into multiple overlapping papers. Worth circulating as a research draft is an editorial judgment; novelty and acceptance require outside assessment.

Prior tools are credited: Gajardo's symbolic feasibility/forbidden-word framework, standard-highway certification as treated by Gajardo--Lutfalla--Rao, and Jillhewar's full-drift chronology criterion. This work does not claim the first discovery of those methods or of nonperiodic ants on infinite backgrounds. `LITERATURE.md` records the actual primary sources inspected and the limited scope of the search.

## 10. Reproduction, trust, and persistence

Run `python reproduce.py`. It makes a disposable copy, regenerates and compares the entire edge set, freshly compiles the independent C++ checker, verifies the quotient and exact path/supply bounds, rejects damaged certificates without repairing them, and checks the all-input algorithm against literal controls. The checked-in word and quotient certificates are never overwritten by the default checks. The final report includes return codes, source hashes, certificate hashes, and measured runtimes.

The all-parameter parts of Lemma 1, the seed-family induction, and the spiral separation are the written arguments above. Their finite geometric premises are checked, and large-parameter tests are supplementary. No finite test is being substituted for their quantifiers. The two implementations were written during the same research session: algorithmic independence is not outside mathematical review.

The initial C++ development run correctly exposed a checker bug in accepting an unsuccessful collinearity test's output variable. It was corrected before the passing replay, and all parameter controls were rerun. This was an implementation correction, not an amendment to Lemma 1. The final report and hashes bind only the corrected source.

No prior theorem's evidence level is upgraded. No global suite, old Lean rebuild, outside review, or repository write is implied by generation of this package. Actual remote persistence, if any, must be reported separately using a confirmed commit.

## Appendix A. Exact words

The machine-readable words are in `certificates/witness.json`; line breaks below are not letters. All geometric statements use north at the origin unless a phase placement is explicit.

### W (length 104)

```text
RRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRL
LRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRR
```

### U (length 28)

```text
RRLRLLLLRRRRLRRLRRRRLLLLRLRR
```

### T (length 24)

```text
RRRRLLRLLRRRRLLRRRRLLRLL
```

### A (length 28)

```text
LLRRRRLRRLRRRRLLLLRLRRRRLRLL
```

### B (length 102)

```text
RRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLRRRRLRLLLLRRRR
LRRLRRRRLLLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRLL
```

### C (length 89)

```text
RRLRRRRLLLLRLRRRRLRRLRRRRLLLLRLRRRRLRLLLLRRRRLRRLRRR
RLLLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRR
```

### Z (length 104)

```text
RRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR
RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLL
```

## Appendix B. Exact first-L time table for the 24-mode

The two rays are each advanced by 24. The finite times and the rays are disjoint as read events and correspond to distinct first-read cells.

| Phase | Finite first-L times | Ray starts | Maximum $L-12b_j(L)$ |
|---:|---|---|---:|
| 0 | 5,7 | 8,23 | 5 |
| 1 | 3,4,6 | 7,22 | 3 |
| 2 | 2,3,5 | 6,21 | 2 |
| 3 | 1,2,4 | 5,20 | 1 |
| 4 | 0,1,3 | 4,19 | 0 |
| 5 | 0,2 | 3,18 | 0 |
| 6 | 1 | 2,17 | 1 |
| 7 | 0,7 | 1,16 | 0 |
| 8 | 6 | 0,15 | 0 |
| 9 | 5 | 14,23 | 5 |
| 10 | 3,4 | 13,22 | 3 |
| 11 | 2,3,11 | 12,21 | 2 |
| 12 | 1,2,10,19 | 11,20 | 1 |
| 13 | 0,1,7,9,18 | 10,19 | 0 |
| 14 | 0,6,8,17 | 9,18 | 0 |
| 15 | 5,7,16 | 8,17 | 5 |
| 16 | 3,4,6,15 | 7,16 | 3 |
| 17 | 2,3,5,14 | 6,15 | 2 |
| 18 | 1,2,4,13 | 5,14 | 1 |
| 19 | 0,1,3,12 | 4,13 | 0 |
| 20 | 0,2,11 | 3,12 | 0 |
| 21 | 1,10 | 2,11 | 1 |
| 22 | 0,7,9 | 1,10 | 0 |
| 23 | 6,8 | 0,9 | 0 |
