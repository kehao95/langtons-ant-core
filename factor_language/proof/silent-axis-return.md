# Axis-strip geometry of arbitrary silent returns

`53f98d2e93614a8eea5424b0bb967c7311bb97f7`.

**Evidence.** An all-length analytic lifting/telescoping proof with complete finite
integer certificates, independently regenerated finite words, and scoped literal
controls. Not Lean-formalized, externally reviewed, or a publication-priority claim.
This is a geometric restriction on genuine dynamics, not a compiler speedup, an
HC proof, or a proof that bounded J10 positions imply H.

## 1. Exact result: the strip is a conclusion, not an input promise

Use the complete classical ant convention: white/right (R), black/left (L), flip
then move; time t precedes update t. Let W be the inherited standard 104-letter
word, and L10 its cyclic ten-factors. A finite word is ten-legal when all its
wholly contained ten-factors are in L10. Words shorter than ten are vacuously legal.
Physical feasibility means that some initial colouring executes the whole word.
No eventual periodicity, black-mass bound, future-active deletion or initial strip
is assumed. Finite-word feasibility is identical for arbitrary and finite initial
colourings, by the inherited first-read/alternation criterion.

**Theorem 1 (uniform silent-return strip).** Let p_0,...,p_L be the head positions
of ANY physically feasible ten-legal finite word. There is a coordinate i in {x,y}
such that, simultaneously for every 0<=t<=L,

    min(p_0[i],p_L[i])-43 <= p_t[i] <= max(p_0[i],p_L[i])+43.       (1)

Thus the ENTIRE segment occupies one horizontal OR one vertical infinite strip.
The coordinate is chosen once for that whole segment, not separately at each time.
Its width depends only on one endpoint displacement and the universal constant 43.
There is no bound on distance traveled ALONG the strip. Neither optimality of 43
nor a two-endpoint bounded-ball/tube theorem is claimed.

A slightly stronger oriented formulation is proved: for some
n in {(1,0),(0,1),(-1,0),(0,-1)}, with p_0 translated to zero,

    -43 <= n dot p_t <= n dot p_L + 43  for every t.               (2)

Implication (2)->(1) is immediate. Different silent segments may require different
coordinates/normals. The choice is not asserted computable from only their current
local state without their later path.

## 2. Cross-event consequence with NO bound on the number of events

J10 is the existing intrinsic predicate: the current turn together with the true
preceding nine turns is not in L10. An actual finite word between successive event
updates has no forbidden factor wholly inside it. Removing the event updates, not
concatenating the remaining letters, is essential.

Let K be a fixed nonempty finite set, with bounding rectangle
[x_-,x_+] x [y_-,y_+]. Define the infinite AXIS cross

    A(K) = {x_- -44 <= x <= x_+ +44}
           union {y_- -44 <= y <= y_+ +44}.                       (3)

**Corollary 2 (uniform consecutive-chain container).** For any finite consecutive
list of J10 events whose read positions are in K, all head positions between the
first event and the last event's outgoing move lie in A(K). The constant does not
depend on the event count, elapsed time, initial mass, or exterior colouring.

**Proof.** After an event at q in K, the head is at a nearest neighbour of q.
Before the next event it is in K. Apply Theorem 1 to the contiguous silent word
between these two states. In its chosen coordinate, both endpoints belong to the
rectangle enlarged by one. Equation (1) then gives padding 44. The removed event
updates themselves have source in K and outgoing head within one. Take the union
over all intervals. No black cell is discarded from the complete state. QED.

**Corollary 3 (localized infinite defects have only axial arms).** If a finite-support
orbit has infinitely many J10 events, and all sufficiently late event positions
belong to K, then after the first such event its entire head trajectory stays in
A(K). Every subsequently created black cell also lies there. Existing exterior
black cells remain physically present and unchanged; they are not erased.

In particular an orbit that repeatedly leaves EVERY fixed horizontal/vertical
cross cannot have both infinitely many J10 events and bounded event positions.
A finite controller whose nonstandard events stay in a fixed region cannot service
arbitrarily distant DIAGONAL archives through otherwise silent trajectories.
It must either cease having defects (and hence enter P104 on finite support),
produce defects outside that region, or restrict its unbounded excursions to
these axial arms.

This supplies a genuinely uniform cross-event restriction. It does NOT conclude
that the remaining axis-cross dynamics is impossible. The oblique-strip and
DIAGONAL-cross bounded-visit theorems do not apply to (3): their positive corner
increments explicitly exclude horizontal/vertical strip directions.

## 3. Imported finite-path coverage, and what was actually rebuilt

The [exact J10 macro theorem](ten-event-macros.md), Sections 3--4, provides:

* all 6,605 physically feasible ten-legal words of length 150;
* their 6,501-vertex overlap graph with 149-letter history vertices;
* the 366-vertex folded component, its full quotient on 102 phases, and the
  physical exclusion of B A^n B A^m B for ALL n,m>=0;
* the corresponding bounded-fold lift, 7,595 vertices and 7,763 edges, covering
  every actual finite continuation after its first 149 turns.

The words, initial-colour feasibility method and three-fold obstruction are inherited,
not newly claimed. Here both Python and an independently written C++ enumerator
regenerate all words, all short-level cardinalities, and the maximum short-prefix
coordinate radius. The frozen sorted word hash is

    6b76e51621e15d2304f1c0baa28790cc267cabafca3fc03250dea8721b2b4794.

The quotient is reconstructed and checked on every internal edge; its inherited
hash is also verified. The all-n,m proof of the fold exclusion remains an analytic
upstream dependency, not replaced by finite graph reconstruction.

## 4. New finite certificate: every path has a common coordinate normal

Adjoin the actual incoming heading h=0,1,2,3 to every counted-lift vertex. An edge
appending c updates the heading by +1 for R or -1 for L. Its literal displacement
is dir(h_new). This oriented graph G has 30,380 vertices and 31,052 edges.

Its cyclic strongly connected components are all simple cycles: four 24-cycles,
twelve 28-cycles, and four 104-cycles. Their geometrical displacements are respectively
rotations of (0,-2), (0,-4), and (-2,-2). Words and displacements are computed, not
inferred from their lengths alone.

For a cyclic component C with displacement d(C), attach the mask

    M(C)={n in the four coordinate normals: n dot d(C)>=0}.

Attach all four normals to each acyclic component. An arbitrary finite graph path
receives the intersection of the masks of every component it visits. Crucially,
this includes partial cycle visits; imposing this extra constraint is conservative.

**Finite certificate A.** Every such path's intersection is NONEMPTY.

The certificate is complete: initialize each condensation component with its own
mask, propagate every possible intersection over every condensation edge, and
verify that the empty mask never appears. The resulting table has 88,024
component/mask states. An independent work-list fixed point on the FULL original
oriented graph, without using a condensation ordering, has 90,256 vertex/mask
states and agrees at every vertex. Initializing at EVERY vertex covers every
possible input history, not just one standard seed.

For a small declarative check, the generated mask sets must contain each start
mask, be closed under every outgoing-edge intersection, and exclude zero. Induction
along any finite path then proves certificate A. The generator's heuristic or
execution order is not a mathematical premise.

## 5. New integer potentials: bound coordinate retreat, not time

Fix one normal n. Delete vertices in cyclic components whose mask omits n, obtaining
G_n. Certificate A says that every finite path of G belongs ENTIRELY to at least one
of these four graphs. It does not say that one G_n covers all paths.

**Finite certificate B.** On each G_n there is an integer potential H_n such that

    0 <= H_n(v) <= 33,
    H_n(v) >= H_n(u) - n dot dir(h_u)  for EVERY edge v->u.       (4)

Each G_n has 30,064 vertices and 30,714 edges. All 122,856 integer edge inequalities
are checked exactly. The generator uses integer relaxations; the checker requires
(4), including the bounds. Substituting a zero potential fails on an actual edge
with negative coordinate displacement. Frozen hashes of all four sorted potential
tables are in report.json; regeneration is deterministic.

For any subpath from v_a to v_b, telescoping gives

    n dot (p_b-p_a) >= H_n(v_b)-H_n(v_a) >= -33.                (5)

This sign follows directly by rearranging (4): an edge displacement is at
least the potential at its target minus the potential at its source. In particular,
a continuation from v_0 cannot fall below -H_n(v_0), not below H_n(v_0)-33.
The distinction is important in the startup calculation.

## 6. Full startup proof and the constant 43

Normalize p_0=0 and initial heading north. Quarter-turn rotation later handles
all other headings and only permutes/signs the coordinate normals.

The independent complete short-word enumerations agree at EVERY length 0,...,150.
For every feasible ten-legal word of length at most 149, every position has infinity
norm at most 24. This follows from the maximum over every enumerated endpoint at
those levels, because every earlier subprefix is itself enumerated. Such words
satisfy (1) immediately; to obtain (2) choose the sign with n dot p_L>=0.

Now let L>=150. Its first 149 letters v occur as a vertex of the overlap graph,
since the next letter belongs to a completely enumerated 150-window. Put
q=p_149 and h=the literal heading after this prefix. The counted-lift state starts
at (v,0,h), including when v already belongs to the folded component. The imported
coverage theorem supplies its oriented G path through every later update.

Certificate A chooses one normal n whose allowed subgraph G_n contains that whole
path. Write H0=H_n(v,0,h) and z_t=n dot p_t. The complete startup certificate checks,
for EVERY possible initial 149-word and EVERY normal allowing its startup vertex,

    min( z_t : 0<=t<=149 ) >= -43,
    z_149-H0 >= -43,
    max( z_t-z_149+H0 : 0<=t<=149 ) <= 43.                  (6)

The exact maxima are:

| normal | checked startup states | lower allowance | upper allowance |
|---|---:|---:|---:|
| (1,0) | 6436 | 43 | 43 |
| (0,1) | 6441 | 43 | 43 |
| (-1,0) | 6436 | 42 | 43 |
| (0,-1) | 6431 | 42 | 43 |

For t>=149, (5) gives z_t>=z_149-H0>=-43. Applying (5) to the suffix from t to L
gives z_t<=z_L+33. For t<=149, the first inequality in (6) gives the lower bound,
while z_L>=z_149-H0 and the third inequality in (6) give z_t<=z_L+43.
This proves (2), hence Theorem 1, at every time including the final unupdated head.
No claim is made that 43 is sharp.

An additional useful formulation of (5) is that the SAME selected normal has
backtracking at most 33 between any two times 149<=a<=b<=L. The theorem does not
supply one common normal across an unbounded sequence of different silent words.

## 7. Scope checks and the remaining global obstruction

The inherited silent fold word C A^(n+6) B A^(n+2) D has endpoints 0 and (-1,0)
while reaching y=-4n-26. Its x range is [-5,2]. It is a useful control precisely
because it disproves a bounded endpoint-ball conclusion while satisfying (1).
Seven finite instances, including n=1000, are replayed; the family and its all-n
proof belong to [silent fold/reset](silent-fold-reset.md), not this result.

An actual twenty-black circuit at n=40 makes a 23,444-step return, leaves BOTH
candidate radius-43 endpoint strips, and has 270 contained defects. This confirms
that silence is a real hypothesis. It does not provide a counterexample to (1).
Additional actual finite orbits are split at bad ending letters, and every resulting
silent contiguous word is checked. No bounded simulation is used to infer the
all-length theorem or the infinite corollary.

The remaining step is NOT to repeat a finite-budget query infinitely. One would
need to exclude, or physically realize, repeated history production and consumption
in the axis-cross case (3), or control unbounded migration of the J10 positions.
No such global termination theorem or finite negative seed is proved here.

## 8. Reproduction

Run `python scripts/check_silent_axis_geometry.py`. It uses a disposable directory,
reconstructs the complete finite graph and certificates, compiles the independent
C++17 enumerator, and requires an exact match with the frozen deterministic report.
Python standard library and g++ are sufficient; no numerical optimizer, ISL, SMT
solver, previous large wake search, or old Lean build is used.
