# All-period uniqueness from the standard layer profile

**15 October 2026. Base inspected:** `bf42eebf88560ef767c77cbf582cd08658b0ce6b`.

Evidence: an analytic reduction to a finite search, complete native enumeration,
and independently implemented infinite-word and local-pruning controls. This is
not a Lean proof, external peer review, a claim of publication priority, or a
proof of the Highway Conjecture. The inherited upper certificate is not newly
claimed here. No existing source or certificate is modified.

## 1. Statement: the longitudinal residues are no longer supplied

Use the literal classical ant on Z², white/right and black/left, flip then move.
The complete initial black set is finite. A heading-restoring word of length P
is *realizable* if its infinite repetition is the actual future of such a state.
Historical black cells outside the future read set are allowed and retained.

Fix the FULL displacement of one word to d=(2,-2). The full translation classes
are `(t,r)=(x+y,x mod 2)`. A class is odd if it contains an odd number of the P
pre-update phase positions. Normalize the highest transverse level to t=0.

**Theorem.** Suppose the numbers of odd classes at levels t=-10,…,0 are

```
o = (2,1,1,1,1,1,1,0,1,1,2),
```

and no other level has an odd class. Then every finite-support-realizable word
is a cyclic phase of the standard P104 word. In particular P=104. There is no
period cutoff among the hypotheses, and the residue of an odd class on any
singleton level is NOT prescribed.

This is stronger than `standard-wake-uniqueness.md`, which supplied all twelve
full class labels. It still does not classify all width-ten/growth-twelve
profiles, other full displacements, all periodic highways, or arbitrary finite
inputs. Repeating a word twice changes its full displacement to (4,-4), and is
not a second word within this theorem's input contract.

Translations, quarter-turn rotations and cyclic phase changes give the
corresponding invariant geometric statement. Reflections/color reversal are
not used. The word, not the entire black field, is classified.

## 2. Why only 256 masks, and why a common cutoff applies

Recall the attributed finite-support criterion: in each full translation class,
order phase positions q_i=b+a_i*d by i-P*a_i. The turns must alternate R,L,…,
starting with R. This is the supplied-word criterion of Jillhewar (2026), as
proved/recalled in `wake-period-synthesis.md`; it is not new in this note.

At a highest or lowest visited transverse level, all visits in a class have the
same turn. Alternation therefore permits exactly one R there. Thus extrema of
actual visits are odd levels, and the supplied odd profile derives the complete
containment -10<=t<=0. It is not an imposed confinement assumption on HC inputs.
Both top classes have one event. The top arrivals face E in the normalized
sigma=-1 sector. Choose the unique event in (0,0) as phase zero, at the origin.

Only these eight levels have a choice of residue:

```
ROWS=(-9,-8,-7,-6,-5,-4,-2,-1).
O(mask)={(-10,0),(-10,1),(0,0),(0,1)}
        union {(ROWS[j],(mask>>j)&1):0<=j<8}.
```

The 256 masks enumerate the entire input class.

Section 3 of `standard-wake-uniqueness.md` already supplies a residue-INDEPENDENT
finite directed graph and checked integer inequalities on all its 90,158 edges:

```
y_v-y_w+alpha_t*epsilon <= -1,
alpha=(-50,32,-18,8,-2,0,-2,8,-18,32,-50),
sum_t alpha_t*o_t=-168.
```

Every realizable periodic word lifts to a closed walk. Summing telescopes y and
uses the signed R-minus-L count o_t, giving P<=168 for EVERY mask above. The
underlying finite-support, forbidden-factor and history-warmup contracts are
unchanged. This package imports that proved/checked certificate; it does not
claim to rerun its graph construction or to improve its bound.

## 3. Complete necessary integer-count filtering

The pinned `counts.py` implements the exact possible counts for one full class.
Writing I,J for its prescribed incoming/outgoing ports on the processed side,
o for its odd indicator, and a for processed-side arrivals at even ranks,

```
m=2*(I+J-2*a)+o           on an even layer,
m=2*(J-I+2*a)-o           on an odd layer,
0<=a<=ceil(m/2), 0<=I-a<=floor(m/2), m>=0.
```

The literal port rule proves necessity. Conversely such a count is realized by
a binary arrival string: choose a even-rank ones and I-a odd-rank ones. This
converse concerns LOCAL COUNTS only, not chronological global trajectories.

An unbuilt-region table keeps the least total cost among all processed count
histories with the same four port counts. Nonnegative layer costs justify
pruning a partial cost greater than 168. Every true completion is retained or
replaced by a no-more-expensive completion with the same interface. Thus an
absent endpoint really excludes a count completion within the cutoff. An
incomplete table supplied externally would NOT justify this inference; the
runner regenerates the complete tables from the pinned algorithm.

The only change in count inputs is `WAKE=O(mask)`. The unrelated old `RESIDUES`
constant and `O` alias are not used by `tables`, `advance`, or `counts`. No
standard-wake congruence or fixed-residue pruning is imported for another mask.

The completed 256-table pass finds:

| Outcome | Number of masks |
|---|---:|
| No complete count profile through 168 | 216 |
| Minimum count period 88 | 16 |
| Minimum count period 96 | 4 |
| Minimum count period 104 | 20 |

The remaining forty masks, BEFORE chronological validation, are

```
0,15,27,30,39,45,51,54,57,60,71,77,83,86,89,92,101,106,113,116,
139,142,149,154,163,166,169,172,178,184,195,198,201,204,210,216,
225,228,240,255.
```

Each generated table's record count, minimum and SHA256 are retained in
`evidence/count_tables.json`. The hash identifies the data, not the proof.

## 4. Complement symmetry halves the remaining exhaustive search

Choosing the other unique top event as phase zero and translating its position
to the origin changes the x-origin by an odd integer, and leaves t and d
unchanged. Consequently every class residue changes r -> 1-r. The top heading
is still E. This is a cyclic rephasing and translation of an actual periodic
trace; the finite-state suffix at that phase remains a finite-support realization.
Applying the operation again gives the converse correspondence.

Hence realizability for mask m is equivalent to realizability for 255-m.
There is no fixed mask under this involution. The forty feasible masks consist
of twenty pairs. Exhausting precisely the twenty representatives m<128 is
therefore complete; it is NOT claimed that all forty native jobs were run to
completion. Incomplete exploratory trials are separately marked, unused.

## 5. Chronology-exact enumeration and the added local check

The baseline is the unchanged, exact ordered-event engine `glue_top.cpp`, Git
blob `718e3eb10f47e06660abfc3f7759bc8fefd1067b`. The count engine is Git blob
`9c973f1518e8101f37bf62e23b8ccea50fe8d43e`. Both exact byte copies are bundled.
A patch refuses any other baseline and requires each textual insertion anchor
to occur exactly once.

The ordered-event completeness argument from `standard-wake-minimum.md` is
independent of the chosen odd mask: for each full class enumerate every binary
arrival sequence, assign turns by stable rank, and match ordered directed edge
occurrences first-to-first. A complete object is accepted only if it is ONE
cycle, its translation voltage is +1, and the lifted times `j-P*v` increase in
every class's stable rank. These conditions reconstruct a literal word with
d=(2,-2); the supplied-word criterion then supplies its finite boundary seed.
Every normalized physical realization produces one of the enumerated objects.

The baseline's count lower bounds, premature-component rejection and cap-safe
chronology constraints use the actual chosen mask. In particular the proof of
cap-safe difference constraints depends on chain lengths, voltages and stable
rank gaps, not on the standard mask's special period congruence. A count-only
boundary does not replace the actual matching/order state in this search.

The overlay also uses the already proved consecutive-rank lemma from
`standard-wake-pruning.md`: in a contiguous open chain, consecutive reads of a
lifted physical cell must have successive stable class ranks. Their physical
coordinates are `(r+2v,t-r-2v)`; storing `(t,r+2v)` suffices. In a genuine
completion, translate this finite segment far enough forward that stable
chronology applies to all its finitely many reads. A skipped class rank would
require a missing visit inside an interval all of whose updates are fixed.
This proof works for every mask; it does not impose a finite-memory bound.

A stamped-array implementation of that rule is inserted during chain traversal.
Its placement differs from the earlier optimized manuscript's implementation,
so the present prefix counts should not be identified with that manuscript's
12,193,595 count. No other baseline rejection rule is changed.

All twenty representative searches completed at cap 168. They traversed a total
of **151,688,735 event-string prefixes** and accepted exactly one normalized
word, at mask 92:

```
RRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLR
```

It has length 104 and is phase 18 of the pinned standard word. The complementary
mask 163 is the old standard normalization. Thus only masks 92 and 163 are
realizable, and both are the same standard highway up to the stated symmetry.
Combining this exhaustion with the all-period upper bound proves the theorem.

## 6. Positive witness and separate infinite check

At the origin facing E, the accepted word has the following complete seed:

```
{(-6,-1),(-6,0),(-5,-4),(-5,-3),(-5,-2),(-5,1),
 (-4,-3),(-4,1),(-3,-3),(-3,0),(-2,-4),(-2,0),
 (-1,-4),(-1,-2),(-1,0),(0,-3),(0,-2),(1,-2)}.
```

The 18-cell count is phase-dependent, not a global minimal-seed claim.
An independently implemented verifier accounts at epoch k and phase i for

```
1_B(q_i+k*d)
XOR #{(j,s):q_j-q_i=s*d, s>0 or (s=0 and j<i), s<=k} mod 2.
```

The expression changes only at computable self-write thresholds, individual
initial-black hits and their successor epochs. Checking every such breakpoint
and zero covers the final infinite interval as well, not merely a long repeated
prefix. This witness requires 266 phase/epoch evaluations. Every one of its
18 active-cell deletions is rejected; a blocking cell 10^100 epochs ahead is
rejected; genuinely unread extra debris is accepted and retained.

## 7. Reproduction and exact trust boundary

From the repository root:

```
python3 wake_synthesis/verification/profile_classification/reproduce.py
```

The replay regenerates all 256 count tables and exhausts all forty native searches (including both complementary phases). The replay
executes independent infinite-word tests, the local-count oracle, native/local-order
comparisons, malformed-input checks and resource-limit controls. A time or node
limit is INCONCLUSIVE, never a negative result.

The all-parameter reduction and completeness arguments are mathematical proofs,
not Lean-kernel certificates. Native enumeration trusts the stated C++ program,
compiler/runtime and the analytical coverage proof. Independent controls reduce
implementation risk; they do not make a second independent proof of the entire
classification. Upstream upper-certificate and singleton dependencies retain
their own evidence levels. The actual final replay is `evidence/audit.json`.

No theorem here asserts that an arbitrary finite seed ever acquires this profile.
