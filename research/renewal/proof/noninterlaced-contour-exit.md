# Exact first-contour transfer and sharp noninterlaced exit

**20 October 2026. Mathematical base:** `54cbf29d7454da8c0d088c4c14864a55153e4a18`.

**Status:** complete written local theorems, exact finite witnesses and a scoped
Python/C++ replay. Analytic and unformalized; not externally reviewed. This is
an auxiliary contour result, NOT a global transience theorem, HC proof, finite
HC counterexample, or an assertion that a stand-alone publication threshold has
been met. The rooted-permutation representation is inherited from the contour
pivot and the classical Truchet literature; it is not newly discovered here.

## 1. Fixed target and definitions

A complete state is (B,e), with B a finite set of black lattice sites and
 e=(x,y,h), h=N,E,S,W=0,1,2,3. White turns right, black left, then the read cell
flips and the head moves. An update is indexed by its pre-update state.

Fix the invariant sector epsilon=(h-x-y) mod 2. At a site there are two
admissible incoming states (darts), e and bar(e)=(x,y,h+2 mod 4). For a field
FROZEN at its input value B, P_B turns and moves without flipping. It is a
permutation, and toggling q replaces it by P_B composed with the transposition
of the two q-darts. The actual root moves by the OLD successor P_B(e).

Let C=(e_0,...,e_(L-1)) be the frozen cycle containing the initial dart e_0,
ordered so P_B(e_i)=e_(i+1 mod L). **C stays fixed throughout the query.** It is
not the dynamically changing active cycle. Define

    T_C = min {t>=1: the actual incoming state at time t is not in C}.

This is departure from a set of directed incoming states. It does not promise
permanent departure from the corresponding physical sites, a geographic region,
or every subsequent contour. Later reentry is allowed.

Pair i and j when e_j=bar(e_i). An unpaired index is an exposed port. Distinct
pairs interlace when, after the root cut, their endpoints satisfy a<c<b<d or
c<a<d<b. Noninterlacing is invariant under a change of cyclic cut.

Every physical contour has at most two darts at one site. It cannot have
adjacent paired occurrences, because one update moves to a different site.
In fact paired indices differ by a multiple of four: moves alternate axes,
and a return to the same site takes an even number of moves on each axis.

## 2. Exact transfer theorem: the cyclic matching is enough

**Theorem 1.** The entire incoming-state itinerary up to T_C, its exact time,
and its complete endpoint field can be computed from C's ordered matching and
the original complete B, without following any exterior trajectory.

Initialize a successor array s_i=i+1 mod L and a root index i=0. At an update:

- save next=s_i;
- if i has mate j, swap s_i and s_j;
- if i is a port, its first update replaces s_i by an outside sentinel;
- move to the saved next; reaching an outside sentinel terminates the query.

A port is read at most once before its second read produces the exit. Its
actual outside target is P_B(bar(e_i)), not an arbitrary or reconstructed
infinite-background state. The endpoint update flips that port a second time.

**Proof.** Before exit, every read site has a dart in C. At an internally paired
site both darts lie in C, and its toggle exchanges exactly their successors.
At a port the opposite dart lies in a different ORIGINAL permutation cycle;
its original successor therefore lies outside C. No other physical site can
change the two successors at that port. Before the first port visit they have
their original values; the first visit exchanges them and still moves by the
old internal successor. The second moves by the outside successor. Internal
sites never share a switch with a port. Induction proves equality of the
abstract successor restriction and the true restricted permutation at every
step before and including exit. No external site is read in this prefix. QED.

If n_q is the number of reads of physical site q in this itinerary, the exact
complete output is

    B_T = B symmetric_difference {q:n_q is odd}.                (1)

Every unread black site, however distant, remains present. This is not a
core-only recurrence and does not identify frozen cycles with physical periods.

The time and index itinerary depend only on the ordered matching. Positions,
heading and full output use C's embedding and (1). Thus different embedded
sources can have identical index dynamics, but the matching cannot be replaced
by a count of contacts or an unlabelled region.

## 3. Totality and a coarse contact-parameter bound

A finite-support field with m black sites has finite frozen cycles. The all-white
permutation has only four-cycles; collect every such cycle meeting one of the
2m modified incoming states. Their union has at most 8m darts, is invariant
under all m site transpositions, and contains every modified frozen cycle.
Unchanged cycles have length four. Hence L<=max(4,8m).

There is an exposed port on C: choose a site maximizing x+y on C. If both of
its admissible darts belonged to C, their two outgoing directions would be
opposite. One increases x+y, contradicting maximality. This argument does not
assume a bound on the source's coordinate magnitudes.

We import the elementary no-bounded-orbit theorem, also proved in the project's
column-flux note and in the established ant literature. For self-containment:
if the infinitely often visited sites were finite and nonempty, choose one
maximizing x+y. Eventually its north/east neighbours would not be visited.
The fixed incoming-axis sector then forces all arrivals from the other one
of the two incoming neighbours. Alternation of the read colour forces an exit
to a forbidden north/east neighbour, a contradiction.

A trajectory remaining in C forever would remain in its finite footprint,
so T_C exists. This totality is NOT asserted for arbitrary abstract matchings.

Let p be the number of internally paired sites and q the number of exposed
ports, so L=2p+q. During a run of paired updates without any port update, the
state consists of one of 2p root indices and p switch bits. The already visited
ports do not change during that run. Repeating this state would repeat the
complete physical state and trap the ant in the same finite footprint.
Therefore a paired-only run has at most 2p*2^p updates. At most q nonexiting
port updates occur, splitting paired updates into at most q+1 runs, followed
by the exit-producing port update. Consequently

    T_C <= (q+1)(2p*2^p+1).                                  (2)

This is a coarse finite-state estimate, not a polynomial-time theorem or a
claimed new proof of unboundedness. It is useful as a precise all-input kernel
contract; source coordinates can be arbitrarily large. The useful sharper
result is the next theorem.

## 4. The sharp noninterlaced theorem

**Theorem 2.** If C's contact matching is noninterlaced, then

    T_C <= L+1.                                              (3)

There is an exact closed-form itinerary, not just an upper bound.

If all physical sites in e_0,...,e_(L-1) are distinct, the itinerary is

    e_0,e_1,...,e_(L-1),e_0, then outside C,                  (4)

so T_C=L+1.

Otherwise let b be the least positive index whose site has occurred earlier,
and let a<b be its previous index. Then

    itinerary = e_0,e_1,...,e_b,e_(a+1), then outside C,
    T_C=b+2.                                                (5)

**Proof.** Until time b, all earlier sites are distinct, so the literal run
follows the original frozen contour. At the second read e_b=bar(e_a), the tile
has been toggled once. Its actual successor is therefore P_B(e_a)=e_(a+1).

The index a+1 is strictly smaller than b: adjacent occurrences of one site are
impossible. It cannot have a mate before b, because b was the FIRST repeated
site index. It cannot be paired with a or b, since those already form a pair.
If it had a mate c>b, the two pairs would have cyclic order

    a < a+1 < b < c,

contradicting noninterlacing. Thus a+1 is an exposed port. Its site was read
once already, and its second read is the exit-producing update in Theorem 1.
This proves (5). All prior successors lay in C, so the exit is first. When no
site repeats in one frozen circuit, the same argument at the wrap to e_0 proves
(4). Since b<=L-1, (3) follows. QED.

The argument actually needs only a noninterlaced partial matching with no
adjacent pair, not a full grid embedding. A grid supplies the latter premise.
Dropping it is false: on a three-position abstract circle paired at (0,1) with
port 2, exit takes six updates, exceeding L+1=4.

### Exact endpoint formula

In (5), put q_i=position(e_i). All q_0,...,q_(b-1) are distinct. Only q_a and
q_(a+1) are read twice. Thus

    B_T = B XOR ({q_0,...,q_(b-1)} minus {q_a,q_(a+1)}),
    e_T = P_B(bar(e_(a+1))).                                 (6)

In (4), the corresponding formula is

    B_T = B XOR {q_1,...,q_(L-1)},
    e_T = P_B(bar(e_0)).                                     (7)

These formulae retain the complete field. Once C has been obtained, the matching,
noninterlacing test, exact time and list of changed cells are computed in O(L)
combinatorial operations with indexed/hash lookup. A deterministic dictionary
implementation adds logarithmic factors and ordinary integer-coordinate bit costs.
No claim of linear BIT time in binary-encoded huge coordinates is made.

### A local obstruction stronger than a crossing-count statement

For a general physical C, the same first-repeat argument remains valid up to
e_(a+1). If the run does NOT exit on that next update, a+1 must be paired with
some c>b. This extracts a concrete **adjacently anchored interlacement**
(a,a+1,b,c). A longer residence therefore exposes ordered contact information,
not merely a large circumference. Such an interlacement is necessary for this
particular delay, not sufficient for infinite recurrence or nonstandard motion.

## 5. Sharpness at arbitrarily large physical scales

For each n>=0 start at (0,0),N with exactly

 B_n = {(j+1,j):0<=j<n}
       union {(n+1,n),(n+2,n)}
       union {(n+2-j,n-1-j):0<=j<n}
       union {(2,-1),(1,-1)}.

There are 2n+4 black sites; all unspecified sites are white. Define U=RLRRLR and

    w_n=(RL)^n U (RL)^n U,  L_n=4n+12.                       (8)

Its frozen geometric word is closed, restores heading and has no repeated
physical site before its endpoint. Here is an all-n separation proof, not a
sample extrapolation. The first staircase reads

    S_n={(j,j),(j+1,j):0<=j<n},

then reaches (n,n),N. U has footprint

    A={(0,0),(1,0),(1,1),(2,1),(2,0),(3,0)},

and endpoint (3,-1),S. The four footprints of (8) are

    S_n; (n,n)+A; (n+3,n-1)-S_n; (3,-1)-A.                 (9)

They are pairwise disjoint. The staircases have y-x in {0,-1} and {-4,-3}.
The first cap has y>=n, the reverse staircase has y<=n-1, and the last cap
has y<=-1 while both staircases have y>=0. The first staircase has x<=n,
and its only point with x=n is (n,n-1); the first cap's x=n point is (n,n).
The two caps are separated by y>=0 versus y<=-1, even at n=0. Each displayed
footprint is itself site-simple. This checks all pairs and covers empty n=0
staircases. The second U is rotated by 180 degrees and returns to (0,0),N.

B_n is precisely the L-site set of (8), so the frozen root cycle is exactly
(8), with all indices exposed. Its actual first L_n updates follow that word.
The next update at the origin sees black, turns L, and departs at (-1,0),W.
Hence

    T_C=4n+13=L_n+1,   |B_T|=2n+7.                         (10)

This proves sharpness of (3) on genuine finite inputs with unbounded L. It
certifies only the stated finite transfer, not the subsequent HC outcome of
this entire family.

## 6. Why the unrestricted linear extrapolation fails

An early stronger candidate was T_C<=2L for EVERY physical initial contour.
It is FALSE. The complete 24-black input in `witness.json`, starting at
(4,0),N, has

    L=100, p=40, q=20, T_C=220,
    post-pose=(0,-2),S, post-mass=30.

The full source, complete matching itinerary, and full output are independently
replayed. No prescribed sequence of artificial surgery moves is used. A far
additional black cell at (10^60,10^60) is unqueried and survives at the endpoint.
This one witness refutes the coefficient TWO, not every possible universal linear
bound. We do not infer superlinear asymptotics from it.

There is a further aggregate control. Two distinct 24-edge spanning trees of a
5-by-5 rotated grid (comb and serpent) yield the SAME set of 100 frozen incoming
darts at the SAME root, with 40 paired sites, 20 ports, black cycle rank zero,
and 96 crossing pairs each. Their exit times are respectively 14 and 67. Thus
these geometric/aggregate data do not determine the transfer. The cyclic order
and exact site pairing remain essential. This is not a theorem that every
nonlocal rank fails.

The abstract five-position matching (2,4,0,None,1) has a reachable infinite
loop despite an exposed port. It violates the necessary square-lattice phase
condition and is NOT a physical ant counterexample. General switching diagrams
must not be promoted without a physical embedding and exact lifting.

## 7. Evidence, provenance, and limits

Run `python scripts/check_contour_exit.py`. The default operates in a disposable
directory and compares a frozen report without modifying it. Python's matching
machine, a separate Python vector-turn simulator, and an independently written
C++17 vector-turn simulator use complete fields. The C++ version uses Boost
multiprecision integers, including the retained 10^60-coordinate controls.

The final check covers all 65,536 fields on {-1,0,1,2}^2 at root (0,0),N;
512 three-by-three fields in all four headings; 128 generated complete inputs;
36 sharp-family parameters; the interlaced witness, a remote-cell variant and
two same-dart-set trees. Totals are 67,752 Python complete endpoint/trace
comparisons and 757,531 literal updates. The C++ comparison covers 2,216 inputs
and 28,223 updates. Separately all noninterlaced no-adjacent-pair diagrams through
length 12 are generated: 3,261 qualifying cases. This finite diagram enumeration
checks the formula; the all-length proof is Section 4.

The first native compilation failed because the function name `advance` selected
`std::advance` through argument-dependent lookup. It was renamed before the
successful report generation and fresh default replay. No failed run supports a
mathematical claim. Source hashes bind only the corrected implementation.

These results do not prove transience. Repeatedly exiting successive frozen
contours is fully compatible with returning to a fixed physical region. It also
occurs on standard highways. Theorem 2 cannot be iterated as a decreasing global
rank, and its noninterlacing hypothesis is not asserted for all future contours.
There is no proof that interlacements eventually disappear, that old contours
stop being reactivated, or that the sequence of complete transfers standardizes.

The exact kernel and sharp conditional law are a genuine update to the pivot,
but this session does NOT claim that these local results alone meet the owner's
requested independent-publication threshold or eliminate a complete HC-negative
class. No priority certification, outside review, Lean proof or public release.

## 8. Literature and upstream attribution

The Truchet representation, split/merge picture, and warning that classical ants
leave the ORIGINAL contour after reading a twice-occurring tile are established:
D. Gale, J. Propp, S. Sutherland and S. Troubetzkoy, *Further Travels with My Ant*,
Mathematical Intelligencer 17(3) (1995), 48--56, Sections 3--4;
https://arxiv.org/abs/math/9501233 . The present query is instead exit from the
original set of directed incoming states, and can follow a different arc while
still inside that set. This distinction is essential, not just a name change.

The rooted permutation and finite-modification bound are imported from
`../research-contour-surgery-pivot-2026-10-20.md`. No-bounded-orbit is the classical
result; the self-contained corner argument is also in
`../column-flux-and-clean-writer-obstructions.md`. Neither is counted as a new
contribution here. The prospective new content is the exact fixed-contour port
kernel, the no-interlacement exact itinerary and sharp bound, and the diagnostic
physical witnesses. Novelty of this package as a stand-alone paper is unverified.
