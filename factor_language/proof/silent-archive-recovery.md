# Complete autonomous recovery of the silent-archive family

Evidence: a complete analytic finite-reduction argument, declarative exact words,
and an integer affine-cell verifier; separate Python/C++ full-state controls.
The analytic proof is not Lean-formalized.
This closes the all-parameter terminal behaviour left unresolved in
[silent archive amplification](silent-archive-amplification.md), not general HC.
The construction retains the complete field and its lifetime table; no reset
is externally applied.

## 1. Precise result

Use the classical LR convention: at a pre-update state, white turns right (R),
black left (L); flip the current cell, then move. Headings N,E,S,W are 0,1,2,3.
Let X_n, n>=1, be the COMPLETE (10n+41)-black input of the preceding note. Its
exact finite specification is repeated in Section 2 to avoid a hidden input
change. J10 uses the true preceding nine turns, obtained by inverse updates,
followed by the current turn; its whitelist is the cyclic length-ten factors
of the fixed standard W. Let tau_n denote FIRST permanent standard entry, and
E_n the number of ALL future intrinsic J10 events starting at input time zero.

**Theorem 1 (all-parameter recovery).** Every X_n eventually enters standard
P104. The entire autonomous future after the earlier twenty-step consumer is
covered: the trajectory is not truncated when that consumer first fails.

**Theorem 2 (exact infinite families).**

| Input class | First entry tau_n | Total J10 E_n | Complete black mass at entry | Entry pose | Drift per 104 |
|---|---:|---:|---:|---|---|
| even n>=10 | 550n+6714 | 507n/2+3154 | 50n+337 | (-10,-3), W | (-2,-2) |
| odd n>=17 | 712n+11087 | (743n+10351)/2 | 46n+622 | (16,8), N | (2,2) |

For both infinite classes the LAST intrinsic J10 occurs at tau_n+8. This does
not conflict with permanent standardness at tau_n: the local test still contains
pre-entry turns during those nine boundary windows.

The twelve remaining inputs have the exact values in Section 7 and certified
infinite standard tails. Thus the two infinite families plus those finite cases
cover EVERY integer n>=1. No period/strip promise is imposed on an arbitrary HC
input; the formulas concern this specified family, including its unbounded n.

**Corollary (this candidate cannot renew forever).** Silent manufacture and the
following consumer on X_n cannot sustain infinitely many J10 events from the
same seed. This does not assert that no finite return to another producer-like
pattern occurs during recovery, or that perturbed caps, different bulk words,
other marker arrangements, or arbitrary finite seeds share this conclusion.

## 2. Full input and previously certified prefix

Put

    B_n = L union UNION_{j=0,...,n-1}(M+(0,4j)) union (H+(0,4n)).

All other input cells are white; the head starts at (-1,0),W. The finite templates
are as follows (each row is a set of integer pairs).

    L = [(-1, 0), (-1, 3), (-1, 6), (-1, 7), (0, -1), (0, 3), (0, 5), (0, 7), (1, -1), (1, 2), (1, 3), (1, 4), (1, 6), (1, 7), (2, -2), (2, 2), (2, 4), (2, 5), (3, -2), (3, 1), (3, 2), (4, -1), (4, 0)]

    M = [(-1, 10), (-1, 11), (0, 8), (0, 9), (0, 11), (1, 8), (1, 10), (1, 11), (2, 8), (2, 9)]

    H = [(-3, 11), (-3, 12), (-2, 9), (-2, 10), (-2, 13), (-1, 9), (-1, 11), (-1, 12), (-1, 13), (0, 8), (0, 9), (0, 12), (1, 8), (1, 10), (1, 12), (2, 8), (2, 9), (2, 12)]

The low, bulk, and high parts are disjoint by their y bands; their cardinalities
are 23, 10n, and 18. The inherited source and prefix data are pinned separately
in grammar-manifest.json. A compressed JSON is DATA, not executable code;
`unpack_grammar.py` exposes every letter and count for inspection.

With A,B,P from the preceding note, the actual prefix is

    B[9:] A^n B A^(n-1) P^(n+1) RLL.

At time s_n=76n+190 it reaches head (0,4n+9),W, with complete mass 22n+61.
This is the complete post-consumer state, not a cleaned reference. The new
all-parameter verifier actually includes these six prefix blocks from X_n,
then the recovery below. It therefore rechecks precisely the prefix-to-recovery
interface needed here, without rerunning the old lifetime theorem or old suite.

## 3. Exact recovery scripts and the parity split

The certificate gives alternating fixed finite words and parameterized vertical
loops. Every letter of every fixed word is stored in grammar.json.zlib, with
length and SHA256 verified before reading. Fixed words are not oracles for a
successful simulation: Section 4 verifies their actual execution on the COMPLETE
field, jointly with every repeated block, at all parameters.

For even n>=10 there are 21 parameterized loops and 22 fixed words (43 blocks).
For odd n>=17 there are 27 parameterized loops and 28 fixed words (55 blocks).
A zero repetition is permitted at the smallest odd parameter. These are counts
of declared parameterized blocks, not a claim that every informal physical
'scan' has a unique decomposition.

The loop lengths, repeat counts, and actual vertical displacements are:

### Even regime

| Loop | Word length | Repetitions as a function of n | Vertical drift |
|---:|---:|---|---:|
| 1 | 32 | 1n + 0 | -4 |
| 2 | 32 | 1n + 0 | +4 |
| 3 | 20 | 1n - 1 | -4 |
| 4 | 32 | 1n + 0 | +4 |
| 5 | 84 | 1n - 1 | -4 |
| 6 | 8 | 1n + 1 | +4 |
| 7 | 8 | 1n - 1 | -4 |
| 8 | 36 | 1n - 3 | +4 |
| 9 | 8 | 1n - 3 | -4 |
| 10 | 20 | 1n - 5 | +4 |
| 11 | 8 | 1n - 5 | -4 |
| 12 | 20 | 1n - 5 | +4 |
| 13 | 24 | 1n - 4 | -4 |
| 14 | 8 | 1n - 6 | +4 |
| 15 | 28 | 1n - 7 | -4 |
| 16 | 8 | 1n - 6 | +4 |
| 17 | 12 | 1n - 5 | -4 |
| 18 | 100 | 1/2n - 4 | +8 |
| 19 | 20 | 1n - 6 | -4 |
| 20 | 8 | 1n - 8 | +4 |
| 21 | 8 | 1n - 9 | -4 |

### Odd regime

| Loop | Word length | Repetitions as a function of n | Vertical drift |
|---:|---:|---|---:|
| 1 | 32 | 1n + 0 | -4 |
| 2 | 32 | 1n + 0 | +4 |
| 3 | 20 | 1n - 1 | -4 |
| 4 | 32 | 1n + 0 | +4 |
| 5 | 84 | 1n - 1 | -4 |
| 6 | 8 | 1n + 1 | +4 |
| 7 | 8 | 1n - 1 | -4 |
| 8 | 36 | 1n - 3 | +4 |
| 9 | 8 | 1n - 3 | -4 |
| 10 | 20 | 1n - 5 | +4 |
| 11 | 8 | 1n - 5 | -4 |
| 12 | 20 | 1n - 5 | +4 |
| 13 | 24 | 1n - 4 | -4 |
| 14 | 8 | 1n - 6 | +4 |
| 15 | 28 | 1n - 7 | -4 |
| 16 | 8 | 1n - 6 | +4 |
| 17 | 12 | 1n - 5 | -4 |
| 18 | 100 | 1/2n - 9/2 | +8 |
| 19 | 20 | 1n - 7 | -4 |
| 20 | 8 | 1n - 7 | +4 |
| 21 | 8 | 1n - 7 | -4 |
| 22 | 8 | 1n - 9 | +4 |
| 23 | 28 | 1n - 10 | -4 |
| 24 | 108 | 1/2n - 15/2 | +8 |
| 25 | 32 | 1n - 14 | -4 |
| 26 | 64 | 1/2n - 17/2 | +8 |
| 27 | 8 | 1n - 8 | -4 |

The first seventeen loop words agree across the two regimes. The next has
length 100 and drift +8. It sees a different terminal cap according to the parity
of n, after which the fixed recovery words differ. Parity selects our proof case;
it is not an external choice or controller applied during the ant's run.

Summing the supplied word lengths times their exponents gives recovery lengths

    even: 474n+6524;
    odd:  636n+10897.

Adding s_n proves the claimed candidate entry times. Actual execution and the
infinite continuation are proved next; summing lengths by itself would not.

## 4. Why finitely many arithmetic checks prove every parameter

### 4.1 Coordinate classes and records

In each case write n=2k+n0 with k>=0 and n0=10 or 17. Use classes (x,rho),
0<=rho<8, and represent a physical cell by (x,rho+8r), r integer.
Every fixed block starts at a point with x constant and y=8a*k+b. A repeated
block restores heading and has vertical displacement +/-4 or +/-8. This is
derived directly from its letters, not assumed from a picture of a ribbon.

For drift +/-4 split the repetition index by parity, j=z+2u, z=0,1. Its repetition
count is an affine integer function of k with even slope, so each subcount is
also affine. For drift +/-8 no splitting is needed. Thus every word phase gives
ONE or TWO records of the form

    (x,rho); L(k)<=r<U(k); block index; prescribed turn;
    physical time = a*k+b*r+c.

The input field is described by records of the same form: split its 4-row bulk
by parity, keep its fixed lower cap and its upper cap translated by 8k. No
unbounded black set is an input. For each fixed k there are only finitely many
cells in all records.

The even program produces 9,402 read records and the odd program 16,363; each has
61 source records. Their union includes EVERY read and EVERY input black cell.
The complete field at a boundary is exactly source XOR all earlier read records.
This is a lossless description, not deletion of a supposedly inactive archive.

### 4.2 Parameter slabs

Two affine endpoints a*k+b and a'*k+b' change order only at their rational
intersection. For each nonnegative crossing q, include floor(q) and floor(q)+1
as slab starts, together with zero. In each resulting integer slab, endpoint
orders are fixed. Equalities of distinct functions are isolated as singleton
slabs. For each proposed order, the verifier checks g(k)-f(k)>=0 at both finite
endpoints, or at the lower endpoint together with nonnegative slope on the final
infinite slab. These are exact integer inequalities.

After duplicate coincident endpoint values are merged, consecutive endpoints
L,U delimit spatial bands L(k)<=r<U(k). The verifier additionally checks U-L>=1
throughout the slab. Membership of every source/read record is constant within
such a moving band. Hence checking the sequence of active records once per band
covers every cell and every k in that entire slab, including its infinite end.
Outside all endpoint ranges there are neither input bits nor reads.

The derived parameter partitions are:

    even: k=0; k>=1;
    odd:  k=0; k=1; k>=2.

The fact that there are only two/three order types is an OUTPUT of all endpoint
comparisons, not an assumption that samples k=0,1,2 suffice.

### 4.3 Physical consistency and time order

Within each block, the coefficient of r and coefficient of k in a phase's time
are common to records in the same class; the remaining constant orders reads.
Blocks themselves are ordered by the supplied word script. The implementation
also checks every consecutive active time difference is at least one throughout
the spatial band, reducing the affine-in-r expression to r=L and r=U-1 and then
to the parameter-slab endpoint/slope tests. Thus chronological order is verified,
not guessed from a quotient graph.

At every band start with the COMPLETE input bit. Walk its chronologically
ordered reads; require R exactly on zero and L exactly on one, then toggle.
This necessary and sufficient finite-word condition follows immediately by
induction over actual update time. It is the established symbolic feasibility
method credited to Gajardo in the repository's ten-factor paper, not a new
realizability criterion claimed here.

Every actual time belongs to a derived record; therefore all prescribed reads
are legal and the literal dynamics executes the entire script. The terminal
pose is calculated from the same letters and counts. No residue outside the
read set is changed; in particular its black colour is retained in the endpoint.

The complete checks comprise 11,371 spatial bands, 91,849 alternating-read
checks, and 80,982 strict chronological inequalities. Hashes identify the exact
arrangements. Hash agreement is evidence identity, not a substitute for this
coverage argument.

## 5. Permanent tails, whole history, and FIRST entry

The two terminal poses are constant in k. All source cells and all preceding
reads have constant x coordinates; their derived x ranges are [-24,15] in the
even script and [-24,20] in the odd script. These ranges include every initial
black cell and every write. They are conclusions about these scripts, not a
geometric restriction introduced for arbitrary HC inputs.

Let q_i be the 104 absolute phase positions from a terminal pose, and d its
nonzero diagonal drift. At phase i of epoch e, the required actual read bit is

    1_{B_terminal}(q_i+e*d)
      XOR parity{(j,z): q_j-q_i=z*d, 0<=z<=e,
                         z>0 or (z=0 and j<i)}.             (5.1)

The second term accounts for every prior prescribed flip, at any earlier epoch.
The first term is computed from ALL source and finite-prefix read records by
XOR. No comparison region replaces the full state.

For fixed i, all epochs potentially meeting the complete pre-tail support are
finite in number because d_x=+/-2 and the above x ranges are bounded. Enumerate
all such epochs and their successors. Add epoch zero, all previous-write
thresholds z in (5.1), and one epoch after their maximum. Outside this finite
set, the colour expression is constant between successive thresholds, including
the final infinite interval.

For each of these finitely many q_i+e*d, its membership in an affine record can
change with k only when an endpoint crosses its fixed r. Isolate those crossings
and check both inequalities (or their negation) over each entire slab. The XOR
bit in (5.1) must equal the prescribed tail letter on every slab. This supplies
1,255 all-parameter parity checks. Induction over future time now proves the
infinite standard tail from the stated boundary.

This is the inherited full-field periodic-ray/parity certification principle,
not a new assertion that a long repeated prefix implies permanent repetition.
The finite comparison algorithm can detect markers 10^60 epochs away.

Finally W has 104 distinct cyclic phases, checked directly. Immediately before
each claimed entry, the actual last letter of the fixed recovery cap differs
from the unique preceding letter of the certified standard phase. If standard
motion had started earlier, its common infinite suffix would force that phase
alignment and hence that previous letter, a contradiction. Thus the boundary is
FIRST permanent entry, not merely a sufficient certificate time.

## 6. Exact defect counts and reusable complete future queries

The nine inverse updates are checked on the full affine source, including
constancy of each queried colour across all k. They give the inherited true past,
not an artificially selected legal history. J10 is then a finite-state count
with the nine most recent turns as its state.

Each variable loop has length at least eight. After two copies its last nine
letters no longer depend on the entering history, and every further whole copy
adds a fixed cyclic defect count. For k>=2 every nonconstant repetition count
is at least two, so this gives an exact affine count for the whole program.
The two remaining k values are counted separately, and agree with the same
formula. The nine boundary windows after entry are included; all later windows
are wholly within W and are legal. This gives E_n and last-event time in
Theorem 2. Black mass follows independently by adding #R-#L to 10n+41.

The verified script also supplies an exact first-read query for any point q.
For its class evaluate each active record's a*k+b*r+c and minimize; then include
all solutions q=q_i+e*d with e>=0 from the infinite tail, using time tau_n+104e+i.
There are finitely many records and 104 rays independent of numerical n.
`first_read` implements this for both infinite parameter regimes using integer
arithmetic, with no iteration over n or the returned time. Twelve small cases
are finite explicit words and admit the same construction.

Consequently a FINITE XOR perturbation E to this particular initial field has
an exact first colour divergence at the least of these reference read times.
If every answer is absent, first-difference induction proves permanent coupling
with all E physically retained. This is a supplied-reference interface, not a
solver for the future after an arbitrary interruption or for arbitrary HC.
It uses the standard first-difference coupling principle.

## 7. The twelve finite exceptions

The data contain literal recovery words for the following complete inputs, not
untrusted simulation summaries. Both implementations replay the full source,
earlier producer/consumer, and recovered word, compare the complete terminal
fields, and check their infinite standard futures. First entry is verified by
the previous-letter mismatch as above.

| n | First permanent entry | Total intrinsic J10 | Black mass at entry |
|---:|---:|---:|---:|
| 1 | 7936 | 3591 | 603 |
| 2 | 6564 | 2816 | 511 |
| 3 | 24214 | 12216 | 1199 |
| 4 | 5244 | 2275 | 433 |
| 5 | 16825 | 7841 | 1060 |
| 6 | 15026 | 7124 | 975 |
| 7 | 11134 | 5180 | 777 |
| 8 | 12786 | 6163 | 775 |
| 9 | 18441 | 8953 | 1134 |
| 11 | 17125 | 8132 | 1150 |
| 13 | 21371 | 10510 | 1300 |
| 15 | 21603 | 10642 | 1324 |

These are exhaustive exceptions to the stated infinite-case domains. A finite
check is sufficient here because this part of the theorem is an explicitly
finite set of inputs, unlike the affine family.

## 8. What changed in the HC proof picture

The preceding note left the full future after the twenty-step consumer open.
Here that exact family is now completely positive, with a finite, explicit
per-input event budget. This rules out its proposed infinite self-renewal;
it is not another demonstration that a finite experiment happens to stop.

The candidate does not fail by monotone black depletion: entry mass grows to
50n+337 or 46n+622. Nor is the argument a rank based only on defect births: the
old J10-free manufacture remains genuine. Instead, each entire annotated script
has a finite sequence of compatible bulk transformations and cap interactions.
Parameter parity selects different finite continuations, all ending in P104.
The remaining word length gives a family-specific countdown once this COMPLETE
script has been proved; no such script has been established for arbitrary inputs.

No theorem says that arbitrary additional cap markers, interrupted recovery,
a different producing word, or a different finite-support periodic tail must
enter this library. One may not identify two bulk patterns while forgetting
their caps and historical field, or treat the shadow's first-contact oracle as
a solution of its interrupted continuation. A global J10 bound, a global rank,
and an autonomous HC-negative seed remain unsupplied.

## 9. Reproduction and trust

Run from the repository root:

    python3 factor_language/verification/silent_archive_recovery/reproduce.py

Or compare directly:

    python3 factor_language/verification/silent_archive_recovery/check.py --compare factor_language/verification/silent_archive_recovery/checked_report.json

Only Python's standard library and a C++17 compiler named g++ are required.
The default command does not change the grammar or report. `unpack_grammar.py`
checks both compressed and decoded hashes and prints the JSON for inspection.
The grammar includes every constant recovery word, all affine repeat counts,
the exact source, standard word, and all twelve finite-exception words. No old
shared simulator, graph solver, network service, or arbitrary future-colour
oracle is invoked.

The generic proof is the analytic coverage in Sections 4--6, plus its finite
integer premises. Separately, Python uses vector rotations and C++ uses headings
on complete mutable fields. They check 88 complete inputs (n=1,...,80 and
127,128,255,256,511,512,1000,1001), each implementation performing 5,222,713 literal
updates, and compare all 88 COMPLETE terminal fields. Each checks every finite
requested turn and an exact infinite-tail criterion. The analytic coverage argument supplies the universal parameter quantifier.

Wrong recovery turns, a shortened parameterized scan, a wrong tail phase, a
missing source bulk bit, and a marker 10^60 tail epochs away are rejected.
An off-trace marker is retained and correctly accepted. Six hundred exact
first-contact queries match finite traces; a 10^60 input-parameter/epoch control
uses only finite integer formulas, not literal simulation through that time.
