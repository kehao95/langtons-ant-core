# Exact escape times of Langton's ant in four rows

**20 October 2026.** Research base: `54cbf29d7454da8c0d088c4c14864a55153e4a18`.

**Evidence:** complete analytic reduction, two separately written exact finite
implementations, and a checked inductive certificate for all widths. Not Lean
formalized or externally peer reviewed. No full Highway Conjecture (HC) solution
is asserted. This is an independent, complete first-exit problem for four rows,
not another fixed-event prefix theorem or an assumption that all HC orbits lie
in a thin strip. The proof imports no earlier project theorem or simulator.

## 1. Main theorem and relation to the literature

Use the classical ant on the full square lattice. White turns right and becomes
black; black turns left and becomes white; then the ant moves one unit. Headings
N,E,S,W are numbered 0,1,2,3. A state at time t precedes update t.

Let S(4,n) be the largest number of updates before first leaving
R_n={0,...,n-1} x {0,1,2,3}, over **every** initial coloring of its 4n cells,
every internal starting cell and all four headings. The exit-producing update
is counted. Exterior colors may be arbitrary: they are not read or changed
before this first exit. The rectangle is an observation region, not a reflecting
boundary or a modification of the classical rule.

**Theorem 1 (complete exact answer).**

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S(4,n) | 2 | 18 | 28 | 46 | 64 | 86 | 104 | 146 | 156 | 206 | 224 | 266 |

For every n>=13,

    S(4,n) = 34n - 150.                                      (1)

In particular S(4,n)<=34n for every n>=1, and the asymptotic coefficient 34
cannot be reduced. Every stated maximum is attained by a complete finite
coloring and an explicitly reconstructible internal pose.

Etse, *How Long Can The Escaping Ant Be Confined?*, MFCS 2026, Section 4.3.3,
Conjecture **11** on p.49:14, conjectures S(4,n)<=34n. Figure 13 and the adjoining
text give a lower family 34n-150 for n>=14 and report agreement of certain small
widths. This theorem proves that conjecture and determines the exact function,
including the exceptional widths. The arXiv v1 numbering is **Conjecture 13**;
it is not the numbering of the published version. The published proof, text,
and Figure 13 were inspected directly. Our attainment proof below is supplied
independently, not inferred from the simulation statement or the figure.

This is a computer-assisted finite-certificate proof. Its infinite quantifier
is established by closure of a persistent response algebra and by an explicit
integer induction. It is not extrapolation from S(4,n) values for n<=23 or 1001.

## 2. A persistent interface, with no reset of internal colors

Set epsilon=(h-x-y) mod 2. A turn changes heading parity and a move changes
checkerboard parity, so epsilon is invariant. In a column x put p=x+epsilon mod 2.
Horizontal entering headings are allowed at exactly the two rows

    I_p=(1-p, 3-p),

and horizontal outgoing moves from that column occur at rows

    U_p=(p, p+2).

Both row lists are indexed by channels 0,1. A horizontal exit from parity p
has precisely the row parity needed to enter an adjacent column of parity 1-p.
A column coloring is the integer mask b=sum_y black(y)*2^y in {0,...,15}.

Choose a near side s: left (0) or right (1). A colored block may be entered
repeatedly through this same side. On each request the caller selects either
allowed input channel. The ant follows the literal rule until it leaves the block.
If it exits the near side, the reply is its output channel and the response
behavior of the **entire resulting coloring**. If it exits top, bottom or the
far side, the reply is terminal, denoted bottom. Such a terminal is never followed
by another request in this interface. Colors are never reset between calls.

A finite response type is therefore a pair

    t=(rho_0,rho_1),   rho_i=bottom or (j,t'),                (2)

where t' is another response type. Its rank is the largest possible number of
successful near-side returns under an arbitrary sequence of requests:

    rank(t)=max({0} union {1+rank(t'):rho_i=(j,t')}).          (3)

An empty block has the terminal type t0=(bottom,bottom). In defining the class
of possible behaviors we do not initially assume that every physical block has
a finite type. That fact is a consequence of the finite closure certificate.

The observation deliberately forgets duration and which terminal side is used.
Neither datum can influence a later call after a terminal. It retains all future
return channels and their persistent residual states. Later, requested durations
are recovered by a weighted refinement. The type is **not** an equality of full
physical states and authorizes no removal of an internal or exterior black cell.

## 3. Exact composition and the finite all-width closure

Adjoin one near column, with mask b and parity p, to a child block with near side
s, parity 1-p and response type r. The response type of the combined block is
written Phi_(s,p)(b,r).

A literal excursion within one column has at most two updates: a horizontally
entering head first moves vertically and next horizontally, unless it exits a
vertical boundary first. A vertically entering head exits horizontally in one
update. This supplies a finite exact one-column table, not a guessed routing rule.

For either input request, execute that table. If the head leaves near, reply
with its channel and Phi_(s,p)(b',r'). If it leaves vertically, reply terminal.
If it enters the child, call the child's channel at that row. A terminal child
reply is terminal for the combined block. On a successful child return, retain
its residual type r', retain the current column mask b', and continue from the
far side of the column. Every successful child reply strictly lowers (3), so a
single request makes only finitely many child calls.

For repeated parent requests, a finite proposed assignment Phi is verified by
these equations and by the rank of its declared result type. A parent near-side
return is required to point to the exact assigned residual product type and
strictly lowers its declared rank. This is a finite well-founded check, not an
assumed global ant termination theorem.

**Finite certificate A.** For each of the four pairs (s,p), there are exactly
269 canonical response types, all with rank at most 13. They include t0 and are
closed under Phi for all 16 column masks and all 269 child types. There are
4*16*269=17,216 product cases, with both request channels checked in each.

Starting with the empty block and adjoining columns, the number of response
types realized at exactly each width is:

| width | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| types, for each (s,p) | 1 | 12 | 36 | 83 | 158 | 240 | 264 | 269 | 269 |

The width-7 and width-8 **sets**, not merely their cardinalities, coincide.
All 269 types have actual representatives of width at most seven, and their
complete future response trees are pairwise different. Consequently the catalog
is an exact behavioral classification for this interface, not only a safe
superset with unknown physical members.

**All-width coverage proof.** The empty block has t0. Assume every coloring of
width n-1 has its exact type. Every width-n coloring is exactly one near mask b
and one colored child. The product equations use the child's true replies,
preserve its residual coloring through its residual type, and apply the literal
updates in the new column. Thus the parent has type Phi(b,r), in the catalog.
The checked ranks prove that all these requests terminate. This induction covers
every n and every initial coloring. Conversely the finite representatives prove
realizability of every catalog type. This proves certificate A's interpretation.

Only the 16 one-column masks and the fixed catalogs are checked computationally.
There is no cutoff on physical width, running time, initial black count, or
number of return requests in this argument. The result happens to bound those
requests: no block admits more than 13 successful returns from one side. This
bound is attained under an explicitly selected compatible request schedule.

## 4. A sharp column bound and an independent proof of 34n

Freeze a column at its first visit. Its complete left and right half-blocks,
including any earlier modifications, have exact response types. During all
subsequent visits to this column, query the appropriate half-block and retain
the returned residual type after each excursion. A successful excursion lowers
the sum of the two half-block ranks. Between excursions, at most two updates
occur in the central column. Therefore the central product always terminates,
regardless of the width or the previous history.

**Finite certificate B.** For every parity, every pair of the 269 possible
half-block types, all 16 central masks, and all eight sector-compatible internal
poses, the total number of central-column updates is at most 34. This checks

    2*269^2*16*8 = 18,524,416 cases.                         (4)

There are four cases attaining 34. A concrete 11-column witness, with masks
listed left-to-right, is

    (15,9,9,9,7,1,11,6,6,6,0),  head (5,1), heading W.

Its actual run makes 159 updates before exit; column 5 is updated exactly 34
times. The full endpoint coloring is checked, not only the number 34.

Every update preceding first escape belongs to one of the n columns. Applying
(4) at each column's first visit gives S(4,n)<=34n. This proves the published
conjecture already, without the weighted refinement below.

The same finite algebra gives a sharp 21-crossing bound for any vertical cut
before first escape. Its 578,888 two-block cases include the first crossing.
The retained witness undoes one literal update before entry, so its 21 crossings
occur on one autonomous finite-seed run; none is a fictitious initial crossing.
These auxiliary bounds are uniform in width but do not bound reentries after
leaving and later returning to the entire four-row observation band.

## 5. Recovering exact times without forgetting persistent responses

The unweighted catalog alone is insufficient to maximize time: two blocks may
have the same responses and different internal durations. We therefore associate
a fixed finite weighted dynamic program to request histories.

An **ordinary query** is F(p,t,q), where t is a response type and q is a finite
sequence of input channels. All requests except possibly the last must return;
the last may return or terminate. Let F_n be the largest total number of real
updates on such a script over all width-n colorings having type t. The type
rank makes every relevant script finite (length at most 14). An empty script
costs zero on an existing type; an unrealizable type at that width has value
minus infinity, not zero.

A **rooted descriptor** is either terminal, or (j,t): the first run starts at
some internal pose, returns on channel j, and leaves ordinary type t. There
are 1+2*269=539 possible descriptors at each parity. A **rooted query** R(p,o,q)
executes that initial run and then the ordinary script q. If o is terminal,
q must be empty. Its value R_n maximizes over every complete width-n coloring
and every internal starting pose that realizes the declared rooted descriptor.
The descriptor is an outcome constraint, not an assumed place of initial entry.

### Exact one-column recurrence

For F, enumerate all mask/child-type pairs whose Phi value is t. Simulate the
specified parent script through the column and child response table. This yields
an integer c counting only new-column updates and a child script q'. The child
query is F(1-p,r,q'), with weight c.

For R, there are exactly two exhaustive placements of the initial head.

* It starts in the new column. Enumerate all eight compatible row/heading poses,
  as well as b and the child's ordinary type. Execute the initial local run,
  then the parent script. The induced child query is ordinary F.
* It starts in the child. Enumerate the child's rooted descriptor. Its first
  run either terminates without entering the new column, or returns with its
  declared channel and residual ordinary type. Process the resulting new-column
  motion and later parent script. The induced child query is rooted R, with its
  initial run followed by exactly the child requests actually issued.

In both cases every internal update is counted either in c or in the child
query, once, and the residual colors are retained. Neither case invents a
controller during a run; the script records calls imposed by the adjacent part
of the very same ant trajectory.

Starting from all 2*539 root descriptors with empty scripts, close these
recurrence rules backwards. Complete reconstruction gives a finite graph G
with 21,248 query vertices, 527,764 weighted edges and 1,078 goals. An edge
v -> u of weight c represents precisely an added column and a child query.
The code also records its mask and, for an R-to-F edge, the initial row/heading.
All required successors are present; all vertices are reached from the goals.

The exact recurrence is

    V_0(F(p,t0,q))=0 for |q|<=1;
    V_0(other states)=-infinity;
    V_n(v)=max_(v->u with weight c) [c+V_(n-1)(u)].           (5)

For an empty block the first ordinary request terminates without any update;
there is no internal root in an empty block. These are the only base cases.

**Exactness lemma.** The values in (5) equal the physical maxima they describe.
For the upper direction, decompose any real source into the near column and its
actual child, with the appropriate initial-head placement; it follows one of
the enumerated edges. For the lower direction, choose an attaining child source
and prepend the recorded column. The exact response equations make all induced
calls agree and establish the claimed parent run. Induction on width proves
both directions. In particular a maximum is attained whenever its value is
finite. The scripts preserve one common persistent child between calls; they
are not separate maximizations that choose a different child on each return.

Finally,

    S(4,n)=max_(goal v) V_n(v).                             (6)

This step covers **all internal starting positions and headings**, not just
boundary entrants. Forgetting the R states would incorrectly give the smaller
maximum for a one-sided horizontal entrant.

## 6. A finite certificate for the exact formula at every width

Direct integer evaluation of (5) supplies V_n through n=23. This by itself is
only a finite calculation. The following local inequalities are what make the
answer valid for all larger widths.

Put A=V_20, B=V_21, d=V_22-V_20 and e=V_23-V_21. All four are integer vectors
on the 21,248 vertices, and A,B have no minus-infinity entries. For every edge
v -> u of weight c the checker verifies

    B(v) >= c+A(u),       e(v) >= d(u),
    A(v)+d(v) >= c+B(u),  d(v) >= e(u).                     (7)

For every v, there is an outgoing edge on which BOTH inequalities in the first
line are equalities, and an edge (possibly different) on which BOTH inequalities
in the second line are equalities. The checks comprise 2,111,056 integer edge
inequalities and 42,496 tight-edge existence obligations.

**Affine induction lemma.** Conditions (7) and the tight edges imply, for all
k>=0 and every vertex,

    V_(20+2k)=A+k*d,     V_(21+2k)=B+k*e.                  (8)

Proof: substitute the first form into (5). The inequalities in the first line
of (7) give an upper bound B+k*e, and a tight edge attains it. Substitute that
result again; the second line similarly gives A+(k+1)*d, including attainment.
The k=0 values were computed exactly. This is ordinary integer induction; no
general max-plus eventual-periodicity theorem is imported or assumed.

On every goal, the certificate verifies

    A<=530, B<=564, d<=68, e<=68.

Some goal has A=530,d=68, and some goal has B=564,e=68. Therefore (6)--(8) give
S(4,n)=34n-150 for every n>=20. Exact evaluation of (5) handles n=13,...,19
and the displayed table for n<=12. This proves Theorem 1.

Every large-width value in this proof has an attaining predecessor edge.
Following such edges down to V_0 yields all n column masks and the unique edge
that chooses the initial internal pose. This is a constructive lower-bound
proof for all widths, not only a few simulated examples. An explicit seed has
length n, so producing all its coordinates naturally requires O(n) output.

## 7. Certificate construction, independent checking, and sharp controls

`core.py` implements the literal one-column table, canonical response trees,
composition, full query closure and complete-field literal controls in Python.
It writes a deterministic candidate certificate, not a trusted solver answer.

`verify.cpp` independently implements the literal turn/flip rule and recomputes
all 17,216 composition cases. It checks acyclic response ranks and catalog
canonicality, reconstructs every expected recurrence edge from both root
placements, compares the complete edge lists, recomputes (5), and checks every
inequality and tight edge in (7). It does not accept the proposed graph or the
claimed asymptotic formula on trust. A separate Python integer calculation
recomputes all DP vectors and repeats (7). Damaged protocol data, a missing
coverage count, a wrong edge weight and a damaged affine vector are rejected.

The deterministic certificates have SHA256 hashes

    graph-and-catalog:
    3e01b0422cf2d921fb0ed4aaa690d8f89ffacfa92973a25c3aea590ac8d1110b
    A,B,d,e integer rows:
    4fb5165094326189694eb227157b578497e089f19eff2abed050b14286c27bca

The full finite tables are reconstructed by readable source instead of stored
as a 12 MB opaque dump. The frozen report records all counts and source hashes.
All 1,076 side/parity-specific catalog representatives are checked using their
entire literal same-side response trees. Every colored block through width
three is also checked (17,472 side/parity behavior comparisons).

Independent native brute-force dynamics evaluates all 4,399,360 complete
coloring/pose inputs for widths one through four, totaling 20,978,524 updates.
It agrees with the exact maxima. Twenty-nine maximizing seeds through width
1001 are independently replayed in Python (89,950 updates). Full-plane controls
retain unqueried exterior black cells, including coordinates of magnitude 10^60.
These controls supplement the closure and induction proofs; they do not extend
a finite cutoff to infinity by observation.

The final checks use only the Python standard library and a C++17 compiler.
There is no SMT solver, numerical optimizer, ISL, upstream graph enumeration,
old Lean build, or inherited simulator in the trusted runtime. The proof is
nevertheless unformalized: trust includes the written reductions, the small
verifier source, language implementations and ordinary integer execution.

## 8. Consequences and exact boundary relative to HC

The finite interface catalog remains valid with any number of columns and any
initial coloring. Thus this is a compositional closure result, not just a list
of separately successful trajectories. The exact maximum (1) completes the
four-row first-exit question, resolves the published 34n conjecture, and gives
its optimal linear coefficient and eventual constant term.

For an orbit hypothetically confined forever to an infinite four-row band,
every fixed column would be updated at most 34 times. Indeed any finite prefix
lies in a finite rectangle; apply the all-color column theorem to that prefix
and then let its length grow. Hence such a confined orbit is transient. This
conditional consequence permits arbitrary initial backgrounds and does not
assume finite support. It does not show that a general plane orbit enters or
stays in a four-row band.

The original HC remains open. A plane ant can leave this observation band,
change exterior history, and later return. Its number of such episodes is not
bounded here. No arbitrary plane trajectory is silently given a width promise,
and the complete field is never cleaned between hypothetical episodes. The
new result is a finished, independently meaningful escape problem, not a full
HC proof, a finite HC counterexample, or a complete plane transience theorem.

## 9. Literature and reproducibility

[1] K. R. Etse, *How Long Can The Escaping Ant Be Confined?*, MFCS 2026,
LIPIcs 386, 49:1--49:17. DOI 10.4230/LIPIcs.MFCS.2026.49. Published Section 4.3.3,
Conjecture 11, Figure 13; full version arXiv:2606.26677v1, Conjecture 13.

Etse's column-by-column analysis and four-row conjecture are explicitly credited.
Behavioral minimization, persistent interfaces and dynamic programming are
standard methods, not claimed as inventions. The new mathematical content is
the complete closed four-row response catalog and the verified exact formula.
A targeted public-source search on 20 October 2026 found no earlier proof of
this formula; this limited search is not an exhaustive priority guarantee.

Run `python scripts/check_four_row_escape.py`. The entrypoint uses a disposable
directory and compares a fresh result to the immutable report. Resource failure
raises an error/UNKNOWN, never an empty case or a proof. Only the new module is
checked. A readable standalone manuscript and full source package accompany it;
no submission, public DOI release or outside acceptance is claimed.
