# The standard layer-count profile determines the classical highway

The classification combines an analytic coverage argument and complete exact
enumerations.

## 1. The strengthened statement

Use the literal classical rule: white means R, black means L; turn, flip the
current cell, and move. A periodic word has a restored heading and nonzero net
displacement. Realization means that its infinite repetition is the actual turn
stream from some **finite** black set. Permanent wake growth and unread debris
are allowed; the complete board is not assumed to translate.

Fix the **full** displacement `d=(2,-2)`. Translation classes are labeled by

\[
(t,r)=(x+y,x\bmod 2)\in\mathbb Z\times\{0,1\}.
\]

A class is odd when the period contains an odd number of visits to it. Write
`o_t` for the number of odd classes on level `t`.

**Theorem (layer-count uniqueness).** Suppose a finite-support realization has

\[
(o_{-10},o_{-9},\ldots,o_0)
 =(2,1,1,1,1,1,1,0,1,1,2),\qquad o_t=0\quad(t\notin[-10,0]).
\]

Then its period is 104, and its word is a cyclic phase of the standard P104
word. No period bound, seed-size bound, or restriction on unread debris appears
in the hypotheses. The heading and the phase-zero pose need not be supplied.
The same implication applies to an eventual periodic suffix of any finite
initial state, since the state at the start of that suffix still has finite
support.

More precisely, there are exactly **two** possible labeled odd-class wakes.
They are the standard wake and its translation by `(1,-1)`. Consequently they
form **one** geometric class up to translation. The statement does not classify
all finite seeds, nor does it assert that arbitrary seeds eventually acquire
this layer profile.

### What was removed

The published standard-wake theorem prescribes twelve individual classes,
including their residues. Here neither residue is prescribed on the eight
singleton levels

```
-9, -8, -7, -6, -5, -4, -2, -1.
```

They admit `2^8=256` labeled assignments. The two extreme levels contain both
residues; level -3 contains neither. Thus the new theorem removes every free
longitudinal residue, not merely a period-search cutoff.

The full drift and the exact layer-count vector remain assumptions. In
particular, `width=10` and `growth=12` alone do not supply this vector.

## 2. Lossless normalization and a residue-independent period bound

The supplied-word criterion recalled in [PROOF.md, section 2](PROOF.md) orders
visits to each full translation class by their stabilized physical times. The
turns must alternate `R,L,R,L,...`, starting with R. This is the criterion
attributed there to Jillhewar, not a new claim of this extension.

At either transverse extremum, the incoming and outgoing neighbours are both
on the inward side. The checker-axis invariant makes all visits to the same
extreme class have the same turn. Alternation therefore forces exactly one R
in each visited extreme class. A trace extremum is consequently an odd-wake
extremum: the trace cannot secretly extend beyond levels -10 and 0 while
leaving only even classes there.

At top level 0 the R event enters facing east and leaves south. This fixes the
checker sector `sigma=-1`. Both top residue classes occur exactly once. Choose
the `(0,0)` event as phase zero and translate its position by an integer multiple
of `(2,-2)`. The result starts at the origin, facing east. This normalization
preserves every labeled wake in the 256-member family.

The inherited integer potential certificate uses only the transverse level,
heading, and a suffix context, **not the longitudinal residue**. Its weights are

\[
\alpha=(-50,32,-18,8,-2,0,-2,8,-18,32,-50).
\]

For every retained legal-context edge `v -> w`, with starting level t and turn
sign `epsilon=+1` for R and `-1` for L, its integer potential satisfies

\[
y_v-y_w+\alpha_t\epsilon\le-1.
\]

Every realizable periodic trajectory lifts to a P-edge closed walk after
context warmup. Summing the inequalities cancels the potential. Alternation in
each class says that its signed turn excess is its odd indicator, so

\[
P\le-\sum_{t=-10}^{0}\alpha_t o_t=168.
\]

The same bound holds for **all 256 assignments**. No original-wake-specific
period congruence or lower bound is imported into a changed assignment.

The replay regenerates the original, untrimmed certificate in
`verification/standard_wake/inputs/upper_bound.py`. It checks 588 forbidden
factors, 4,931 contexts, 54,718 vertices, and **all 90,158 edges**. Its potential
range is 0..180 and its maximum edge left-hand side is -1. This is the untrimmed
witness, not the later trimmed witness with range 0..129. The checked bound is
the same in both cases.

## 3. An all-period modular exclusion for 216 assignments

This exclusion does not use `P<=168`.

### Local event counts

Build rows downwards. In a class with m events, rank the events in stabilized
chronological order as `k=0,...,m-1`; even ranks turn R and odd ranks L. Let `a_k`
and `b_k` indicate arrival from and departure towards the already processed
upper side. Complementing both physical side bits gives

\[
b_k=\begin{cases}
a_k\oplus(k\bmod2),&t\text{ even},\\
1-(a_k\oplus(k\bmod2)),&t\text{ odd}.
\end{cases}
\]

Set `I=sum a_k`, `J=sum b_k`, let A count the ones at even ranks, and let
`omega` be the prescribed odd indicator. Directly counting even and odd ranks
shows

\[
m=\begin{cases}
2(I+J-2A)+\omega,&t\text{ even},\\
2(J-I+2A)-\omega,&t\text{ odd}.
\end{cases}
\]

The feasibility conditions are

\[
0\le A\le\lceil m/2\rceil,\qquad
0\le I-A\le\lfloor m/2\rfloor.
\]

Conversely these conditions allow the indicated ones to be placed at even and
odd ranks. Thus they are exact for the local count relaxation. In particular,

\[
m\equiv2(I+J)+(-1)^t\omega\pmod4.
\tag{1}
\]

### Boundary recurrence

Write a frontier as `(O0,O1,I0,I1)`, its outgoing and incoming edge counts on
the unprocessed side. At the next row t the processed-side counts are

\[
(I'_0,I'_1)=\begin{cases}(O_0,O_1),&t\text{ odd},\\(O_1,O_0),&t\text{ even},\end{cases}
\]
\[
(J'_0,J'_1)=\begin{cases}(I_1,I_0),&t\text{ odd},\\(I_0,I_1),&t\text{ even}.\end{cases}
\]

After choosing class counts `(m0,m1)`, the next frontier is

\[
(m_0-J'_0,m_1-J'_1,m_0-I'_0,m_1-I'_1).
\tag{2}
\]

The top frontier is `(1,1,1,1)`, and the bottom requires the same tuple. Reduce
(2) modulo two and use (1) to obtain every class count modulo four. Exactly
128 assignments fail the required bottom boundary parity.

### Four time phases

In the normalized checker sector every update advances

\[
\phi(t,r)=2r+(t\bmod2)\pmod4
\]

by one. Drift `(2,-2)` preserves this label, so `4|P`; each of its four phase
groups contains exactly `P/4` events. Hence the four sums of the forced class
residues from (1) must agree modulo four. A further 88 assignments fail this
necessary condition. Only 40 remain.

Mask bits, in increasing bit order, are the residues on
`(-9,-8,-7,-6,-5,-4,-2,-1)`. The 40 masks are

```
0,15,27,30,39,45,51,54,57,60,71,77,83,86,89,92,101,106,113,116,
139,142,149,154,163,166,169,172,178,184,195,198,201,204,210,216,
225,228,240,255.
```

Masks 0,106,149,255 require `P=0 (mod 16)`. The other 36 require
`P=8 (mod 16)`. These congruences are recomputed, not copied from the standard
wake. The recurrence and its full truth table are in
`verification/profile_classification/audit_profile.py` and
`evidence/profile_classification/audits.json`.

## 4. Exact enumeration of the remaining 40 assignments

The representation and chronological pruners are those of [PROOF.md,
section 5](PROOF.md); the new generator changes the wake bits, regenerates the
cost table for each assignment, and adds explicit mask reporting.

A class is an ordered string of arrival-side bits. Once neighbouring rows have
been built, occurrences along a directed lattice edge match in stable order:
first source with first target, and so on. Representatives
`b_(t,r)=(r,t-r)` give edge voltages through

\[
b_{\rm source}+e=b_{\rm target}+v(2,-2).
\]

Every real trajectory therefore has one represented graph. Conversely a
complete graph yields a realization exactly when it is a single cycle, its
total voltage is one, and the lifted times `j_i-P*v_i` increase with rank in
every class. The alternating criterion then supplies a finite seed.

The count dynamic program retains the cheapest future construction per
frontier. Its transitions depend only on that frontier and the **current
assignment**. Costs are nonnegative; therefore discarding histories more
expensive than cap 168 cannot discard a completion below the cap. Loss of
chronological information makes this a necessary relaxation, never an extra
assumption on actual trajectories. Computed minimum total event counts are:

| Remaining assignments | Minimum count-relaxation period |
|---:|---:|
| 16 | 88 |
| 4 | 96 |
| 20 | 104 |

Both construction directions give the same minima for all 40 assignments.

The inherited chronological tests depend on ranks, levels, voltages and the
cap, but **not on the specific original wake indicators**:

* A closed component before all mandatory levels have been built cannot join
  those future events; a one-cycle trajectory cannot contain it.
* Four-phase partial counts cannot exceed `P/4` and hence cannot exceed the cap.
* Consecutive reads of the same lifted physical cell on a fixed open chain
  must have successive ranks. Missing intervening ranks are not merely a color
  mismatch; no time exists inside that contiguous chain interval to insert them.
* Stable rank order imposes difference constraints on chain root times. For
  different chains A and B, the constant is at least the length of A, since
  their periodic copies occupy disjoint contiguous intervals. A directed cycle
  of these inequalities has weight `C+K*P` with `C>0`. If K is nonnegative it is
  impossible at every positive period; if K is negative, positivity at the cap
  implies positivity at every smaller period. Same-chain constraints use the
  inherited `P >= number of constructed events` argument.

Thus the old pruning proofs apply unchanged after parameterizing the wake.
The generator is pinned to the inherited baseline source hash, and ambiguity
in a source replacement fails rather than silently producing another search.

Every one of the 40 cap-168 runs reports **complete**, with no time or node
limit reached. They visit 215,709,876 class-string prefixes in total. This is
not a count of simulated time steps or a claim to have enumerated finite seeds.

## 5. The complete output and infinite-tail checks

Exactly two normalized words are accepted:

| Mask | Period | Phase shift from the displayed standard word | Constructed seed size |
|---:|---:|---:|---:|
| 163 | 104 | 0 | 19 |
| 92 | 104 | 18 | 18 |

The standard word used here is

```
RRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLRLRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLR
```

Both accepted words have primitive period 104. Mask 92 is the bitwise
complement of 163 in eight bits, exactly the effect of translation `(1,-1)` on
all singleton residues. They describe the same standard highway up to phase
and translation, not two different highway types.

For each accepted word, the separate verifier reconstructs lattice positions,
rechecks stabilized alternating visits, builds its complete finite seed, and
checks the exact all-epoch color formula. At phase i and epoch k that formula is

\[
1_B(q_i+kd)\;\oplus\;
\#\{j:q_j-q_i=s d,\ s>0\text{ or }(s=0,j<i),\ s\le k\}\bmod2.
\]

Every seed-hit epoch, the epoch after each hit, every self-write threshold,
and epoch zero are checked. These finitely many breakpoints cover all constant
intervals, including the last infinite interval. A repeated finite prefix is
not used as a permanence certificate.

The replay rejects every single-cell deletion from the two constructed seeds
(37 negative controls), and rejects a black blocker at
`(2*10^12,-2*10^12)` for each word. The latter checks that a distant future
seed hit is not silently discarded.

Normalization puts every realization into one of the 256 assignments. The
modular argument removes 216; the uniform integer certificate bounds every
remaining period; the complete ordered-event enumeration removes 38 more and
accepts only the two standard phases. The independent all-future checks prove
existence. This completes the computationally assisted proof of the theorem.

## 6. Reproduction and trust boundary

Run from the repository root:

```sh
python3 wake_synthesis/verification/profile_classification/reproduce.py
```

Python 3.10+ and g++ with C++17 and undefined-behavior sanitizer support are
required. `--output PATH` writes to a **new** evidence directory. The default
also uses a new directory. `--jobs`, `--seconds`, and `--nodes` control resources;
any incomplete search raises `INCONCLUSIVE` and cannot produce a completed
classification summary. The checker leaves certificate inputs unchanged.

In addition to the full searches and upper witness, the replay checks all
8,191 binary arrival strings of lengths 0..12 against the local count formula
(676 count-input cases), compares top and bottom dynamic-program minima for
40 masks, and compares the inherited baseline and refined enumerators for all
40 masks through cap 104 under UBSan. Those 80 differential runs all complete,
return identical accepted words, and produce no sanitizer diagnostics. The
cap-104 differential test is an audit, not the source of the cap-168 exclusion.

The original standard branch is reproduced exactly: mask 163 visits 8,580,751
prefixes, matching the retained chain-separation traversal. The complemented
branch visits 14,340,920 prefixes. The new result still trusts the analytic
coverage/pruning arguments, Python/C++ execution and the compiler; the full
classifier has not been translated into Lean. Reuse of the inherited
representation is not an independent reimplementation of that representation.

The code is based on the source files read from `kehao95/langtons-ant-core` at
main revision `6aa3728a6da3c9edb122b4bc2b79ff9253d1b70f`, with individual content
hashes pinned by the replay. Evidence and hashes are retained under
`evidence/profile_classification/`.

## 7. Remaining classification boundary

The completed step is

\[
\text{complete standard odd-class wake}
\quad\longrightarrow\quad
\text{standard per-level odd-class counts}.
\]

A nonstandard periodic highway with drift `(2,-2)` must therefore have a
different layer-count profile, even if its width and total growth are 10 and
12. Other drifts and wider traces are not excluded. Arbitrary finite-state
convergence to a periodic translator remains a separate entrance problem.
No inference from this conditional classification to general HC is made.
