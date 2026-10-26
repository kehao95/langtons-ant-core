# A nine-factor mass-deficit bound, and the sharp window threshold

Classical white/right, black/left, toggle-then-move ant.
Evidence: the analytic coverage argument below, two complete finite enumerations,
a rebuilt integer certificate and explicit all-parameter finite counterinputs.
The analytic argument is not Lean-formalized. This is a mass bound, not a
nine-factor attraction theorem, HC proof or finite HC counterexample.

## 1. Definitions and exact results

Let W be the fixed standard 104-letter word in the pinned verifier, and let L_k
be the length-k factors of W repeated forever, with all cyclic phases included.
A finite word is k-legal when every wholly contained length-k factor belongs to
L_k. The condition is vacuous for words shorter than k. A word is physically
feasible when a literal classical ant can execute it from a complete finite
black field and some pose. No support shape, mass or coordinate bound is imposed.

For a finite turn word v put

    g(v)=number_R(v)-number_L(v),
    D(v)=3|v|-26g(v) = -23 number_R(v)+29 number_L(v).          (1)

For an actual interval [s,t), g(v)=|B_t|-|B_s|, using the COMPLETE finite fields.
The cell toggle gives this identity one update at a time. No inactive black
cells are deleted when computing the difference.

**Theorem 1 (nine-factor bound).** Every physically feasible nine-legal finite
word v satisfies

    D(v) <= 1004.                                            (2)

The constant 1004 is a certified upper bound, NOT asserted to be the best one.
The earlier ten-factor bound 322 remains valid on its narrower language.

**Corollary 2 (all-input event inequality).** Let N_9(s,t) count the nine-illegal
windows wholly contained in the actual turn interval [s,t). For every complete
finite-support input and every 0<=s<=t,

    3(t-s)-26(|B_t|-|B_s|) <= 1033 N_9(s,t)+1004.             (3)

One may replace N_9 by the larger intrinsic event count, using the unique inverse
to supply the preceding eight turns at the interval's left boundary. This does
not assert total decidability of the next such event or finiteness of all events.

**Theorem 3 (sharp window threshold).** For an integer k>=1, there exists a
finite constant C_k, independent of the seed and word length, with

    D(v)<=C_k for every physically feasible k-legal finite v

if and only if k>=9. The lower-direction counterfamily in Section 6 uses only
FINITE initial fields. The auxiliary infinite-background word is not an HC seed.

## 2. Complete finite coverage, not a simulation sample

A finite geometric R/L word is feasible exactly when successive visits to every
physical cell have alternating letters. Necessity is the toggle rule. For
sufficiency put a black cell at precisely those first-read locations whose first
letter is L. This is a finite complete initial black set. Induction on updates
executes the word. Any additional cells outside its finite footprint are inert
during this finite execution. Fixing the origin and initial heading N loses no
turn words, by translation and quarter-turn rotation; no reflection is used.

Enumerate both possible first letters at a newly visited cell, and only the
opposite of its preceding letter at an old cell. Enforce the nine-factor test as
soon as a window is complete. Enumerating all feasible nine-legal prefixes
through length 150 gives

    search nodes:       3,695,909,
    length-150 words:     164,283,
    SHA256 of the ordered newline-delimited length-150 list:
    61e8ac60994d9dfcdcbf9a0366378215cc0969ec636d1f69d21e4a02f5c1a1a9.

The native implementation uses integer coordinates, an array of previous colours
and bit-mask suffixes. A separate Python implementation uses complex directions,
a coordinate dictionary and tuple suffixes. Both COMPLETE enumerations return
identical node/word counts and the exact same word-list hash. The second visits
every shorter prefix too, including prefixes which cannot extend to length 150;
its maximum D over lengths below 150 is 322. Thus all short words are covered.
Resource-limited exploratory runs are not inputs to this certificate.

Construct the overlap graph G: vertices are 149-letter prefixes/suffixes and an
edge from prefix to suffix, labelled by the last letter, is supplied by each
length-150 word. It has 157,114 vertices and 164,283 edges. Every actual nine-legal
word of length at least 150 is its initial 149 letters followed by the labels of
a path in G. The converse is NOT asserted: a graph path can forget a conflict
between visits separated by more than the retained window.

An independently implemented iterative Tarjan decomposition finds precisely
three cyclic strongly connected components:

| Component | Vertices | Internal edges |
|---|---:|---:|
| H | 34,712 | 36,277 |
| Standard simple cycle | 104 | 104 |
| Other simple cycle | 24 | 24 |

All other components are single vertices without a loop. The condensation is
an acyclic graph with 122,277 vertices and 127,878 cross-component edges.

## 3. Exact treatment of the non-simple component

### 3.1 The follower quotient is a necessary, checked projection

On H, repeatedly refine vertex classes by the two labelled internal successors
(R and L, with a separate absent-successor value). It stabilizes after 129
rounds at 1,213 classes. For every original internal edge u --c--> v, the
checker verifies the corresponding quotient edge pi(u) --c--> pi(v); vertices
in one class have the same entire two-successor signature. In particular every
internal H path projects without changing a single letter. This finite graph
projection is not a quotient of all actual infinite physical states.

### 3.2 Additional forbidden words are certified by literal geometry

The retained JSON supplies seven explicit words and their R/L complements.
Each word has a consecutive same-cell repeat with the SAME read colour, so
cannot occur in ANY real finite trajectory, whatever its initial field. The
independent checker replays every word geometrically and checks that earlier
and later indices have the same position, the same letter and no intervening
read of that position. The seven lengths are

    161, 153, 253, 181, 217, 309, 237.

For each displayed representative the conflict is between index zero and the
last index. Complements are checked independently too. This list need not be
complete. It was found by refuting candidate positive-cost graph cycles, but
neither the discovery search nor a numerical optimizer is a proof premise.

An exact suffix automaton avoiding these fourteen words has 2,697 prefix states.
Take its reachable product with the 1,213-state quotient, allowing EVERY quotient
state with empty forbidden-word history as a start. The product has 9,154 vertices
and 9,550 edges. Resetting the suffix context at the entry to H only weakens the
constraint; every real internal H path lifts into this product. A conflict
straddling entry or exit may be forgotten, but no actual path is discarded.

### 3.3 Every integer edge inequality is verified

The checker reconstructs integers 0<=y_u<=306 on the product such that

    y_u-y_v >= omega(c)    for every u --c--> v,
    omega(R)=-23, omega(L)=29.                              (4)

Start all y at zero. Along reverse adjacency repeatedly increase y_u to
max(y_u,y_v+omega(c)); reject if the proposed value exceeds 306. This reconstruction
is total: every increase is integral and every vertex can increase at most 306
times. The actual reconstruction terminates; every one of the 9,550 inequalities
is then checked afresh, together with the bounds on every y. The report contains
the complete potential vector and graph/vector hashes. Hashes identify data;
the edge inequalities certify it.

Summing (4) along any real internal H path gives

    D(path) <= y_start-y_end <=306.                         (5)

This is not strict time descent: R edges have negative weight and cycles with
nonpositive D are allowed. In particular a surviving non-simple component is
not thereby classified as physically finite or standard.

## 4. Covering all components and both ends of a finite word

The 104-cycle has total weight zero and maximum weight of a contiguous cyclic
subword 237. The 24-cycle has total weight -32 and corresponding maximum 94.
For a cycle with nonpositive total weight, erasing full laps cannot lower the
remaining-path upper bound. Consequently these are valid bounds for internal
paths of ANY length, including arbitrarily many laps. Both numbers are computed
directly from the explicit cycle labels, not from a claimed physical realization.

Give the components internal budgets b_H=306, b_104=237, b_24=94, and zero for
all acyclic singleton components. For component C let

    a_C = max D(v) over its 149-letter vertex histories.

Initialize z_C=a_C+b_C. Process the condensation in topological order, requiring
for each cross-component edge C --c--> E that

    z_E >= z_C+omega(c)+b_E.                                (6)

A real graph path visits each component at most once. Equations (5)--(6), and
the two simple-cycle budgets, bound its cost including the initial 149 letters.
They may overcount compatible endpoint budgets, which only makes the bound safer.
The finite dynamic program gives max_C z_C=1004. The checker verifies all initial
and cross-edge inequalities after completing it; it also verifies acyclicity.
No assertion about the future length of the actual orbit is required.

Together with the separately exhausted short-word bound 322, this proves (2).
The readable code, deterministic report and all integer coefficients are in
[`../verification/nine_mass/`](../verification/nine_mass/). The 150-window enumeration and the finite
projection/edge checks are substantive finite premises of the written argument;
this is not a conclusion extrapolated from sampled initial states.

To prove (3), remove the last letter of each wholly contained nine-illegal
window, keeping the intervening consecutive runs SEPARATE. Every retained run
is nine-legal, since an illegal window within it would have had its last letter
removed. There are at most N_9+1 runs, each of cost at most 1004, and N_9 removed
letters, each of cost at most 29. Additivity of D gives (3). Each run is a real
finite subtrajectory; no disconnected geometric fragments are glued together.

## 5. The eight-legal word and its exact initial field

For the lower direction of Theorem 3, use initial heading N and

    u = LLLLRRLLRRRRLLRRLRLLRR,     |u|=22,
    d=(-3,1),     number_R=number_L=11.                      (7)

All cyclic length-eight factors of u belong to L_8. Exactly one cyclic
length-nine factor does not belong to L_9. These are exact string comparisons.
The word is primitive, restores heading and has nonzero drift.

Its infinite execution is realized on the following INFINITE initial black set:

    A={(0,-1),(1,-1),(2,-1)},
    H={(-1,1),(-2,1),(0,0),(-1,0),(-1,-1)},
    B_infinite = A union union_{a in H}{a+j*d:j>=0}.          (8)

The five rays occupy distinct FULL translation classes modulo Z*d, and A is
disjoint from their forward portions. There are eight visited full classes;
five alternate starting L and need the rays, the others alternate starting R.
Thus (8) cannot be replaced by a finite initial field while preserving u forever.
It is not an HC counterexample, regardless of its perfectly periodic turn word.

For completeness the exact construction is checked in two ways. If phase
q_i=b+a_i*d belongs to one class, far-cell read order is increasing i-22a_i.
Alternation in that order gives the whole stabilized class word. For a cell
b+n*d the available visits are precisely the suffix with a_i<=n; its required
first colour gives the three finite boundary sites below the full-phase threshold
and the indicated constant first colour on each forward ray above it. Induction
in literal time proves the prescribed execution. The independent all-epoch
parity check additionally accounts for every ray start, finite initial hit and
self-write threshold, including the final infinite interval.

This is an application of the existing full-class realization principle; the
principle itself is not claimed new. Infinite support is deliberately explicit.

## 6. Complete FINITE counterinputs to an eight-factor uniform bound

For every integer n>=0 truncate all five rays at the same length:

    B_n=A union union_{a in H}{a+j*d:0<=j<n}.                (9)

These are complete finite HC inputs, with precisely 3+5n black cells and white
elsewhere. Their first 22n updates are exactly u^n. The first departure from the
proposed repeated word occurs at update 22n, at position n*d, heading N: u
requires L, but the actual cell is white and the turn is R.

Here is the all-n coverage, not just a checked range. In one full class choose
b=q_i of any phase and put h=max_i a_i. Its black ray, if present, begins at
b+h*d. A read at phase i in epoch j is at ray index j+a_i-h. For j<n that index
is less than n, since a_i<=h. Whenever it is nonnegative, the ray cell retained
in (9) is exactly the one prescribed in (8); negative indices use the unchanged
finite boundary assignment. Thus all initial colours needed in the first n
epochs agree, and deterministic coupling gives u^n. At phase zero of epoch n,
the missing site n*d is the first read in its class order and has not previously
been updated. It is the first omitted ray cell read, and is white in (9).

Both breakpoint arithmetic and two literal simulators check these interfaces;
the arithmetic includes parameters as large as 10^60 without expanding their
22n-step prefixes. The universal quantifier is supplied by the preceding formula,
not by that finite parameter list.

Every prefix u^n is eight-legal and physically feasible, and

    |B_{22n}|-|B_n|=0,
    D(u^n)=66n.                                             (10)

In (10), B_{22n} denotes the ACTUAL time-22n field evolved from the input B_n;
its notation does not identify it with another initial member of (9). Hence no
seed-independent finite C_8 bounds these words. The same words are k-legal for
every k<=8, proving the lower direction of Theorem 3. This does not exclude
bounds which depend on initial mass (here 3+5n), coordinates or the full input.
Nor does it classify what the finite inputs do AFTER the first mismatch.

For k>=9, a k-legal word of length at least k is also nine-legal, giving (2).
For a shorter word, D(v)<=29(k-1). Therefore

    C_k=max(1004,29(k-1))

is a valid bound. This completes the sharp-threshold proof.

## 7. The HC gap is still present

The new result lowers the window needed for a seed-independent mass-deficit
estimate from ten to nine. It does not prove that nine-legal infinite finite-support
trajectories are standard, or that J_9 or J_10 occurs only finitely often on every
input. In particular, (3) is a LOWER bound on event counts when black mass grows
too slowly; reversing it into an event-termination budget would be invalid.

The canonical J_10-to-HC equivalence and total exact J_10 macros remain separate
dependencies proved separately. No theorem here bounds the number of iterations of those macros.
The 22-period construction cannot refute HC: each finite truncation stops
following it at the explicitly identified first missing initial-black read.

## 8. Reproduction

Run `python3 factor_language/reproduce.py --new-results-only` from the repository
root. Python 3.10+ and a C++17 compiler are required for the complete finite
graph reconstruction; no LP or SAT solver is needed. The native and independent
Python enumerations, every product/condensation inequality, and the explicit
infinite/finite support distinction are checked. Code and declarative reports
are identified by source hashes.
