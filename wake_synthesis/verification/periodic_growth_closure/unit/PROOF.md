# A three-layer obstruction to unit-diagonal highways

**15 October 2026.** Classical two-colour Langton ant, white/right and black/left,
flip then move. Research baseline: `cc1e8c3706082fda095d8b5da98fce9f217971c0`.

Evidence: a written all-input coverage argument for the stated periodic-drift
class, and a finite certificate whose every branch and rejection is independently
checked with integers. No Lean formalization, external peer review, exhaustive
literature-priority certification, full HC proof, or finite HC counterexample.
The certificate uses no time/period cutoff, numerical optimizer, or SAT UNSAT result.

## 1. Main result and its quantifiers

A complete state is `(B,p,h)`, with finite B in Z^2 and h=N,E,S,W. One update
reads the current colour, turns R on white or L on black, toggles the cell and
moves one unit in the new heading. Consider any nonempty period word w of
length P which restores its heading and has full displacement d.

**Theorem (unit-diagonal obstruction).** There is no complete finite black seed
whose infinite turn trace is w^omega with full period displacement d=(1,-1).
Quarter-turn rotations exclude all four vectors (+/-1,+/-1).

The theorem has NO bound or prescribed value for P, growth, transverse width,
initial black count, seed coordinates, transient length, or odd-class wake.
It applies after an arbitrary finite prelude: its suffix boundary still has a
complete finite black field.

The word *unit* refers to the FULL displacement, not the primitive direction.
The standard P104 has full displacement (2,-2) in one orientation and is NOT
excluded. Replacing its full displacement by its primitive direction would
change the problem. No claim about (m,-m) for m>=2 follows from this theorem.

## 2. Stable chronological classes from finite support

For d=(1,-1), the full classes modulo Z*d are exactly the layers t=x+y.
Choose the representative b_t=(0,t), and write each phase position

    q_i=b_t+a_i*d,    a_i=x_i.

The visit of phase i at the far cell b_t+n*d occurs at time

    nP + (i-P*a_i).

For sufficiently large n every phase of this class occurs at a nonnegative
epoch and the cell was initially white, because the initial black support is
finite. Therefore its visits, ordered by tau_i=i-P*a_i, alternate

    R,L,R,L,... .

Let k=0,...,m_t-1 denote this stable order. Even k is R, odd k is L. Distinct
phases have distinct tau: equality would force equal phases modulo P.
Consequently the signed count R-L in a class is m_t mod 2, and the total
period growth is the number of odd classes. In particular heading restoration
implies g=#R-#L=0 modulo four. These are known consequences of the exact
finite-support word criterion, not a new criterion; the necessity just proved
is all that the new obstruction uses.

An actual return to the SAME physical cell takes a positive multiple of four
updates: horizontal and vertical moves alternate, and their individual counts
must both be even on a closed lattice walk. Thus consecutive stable ranks in
one class satisfy

    tau_(k+1) >= tau_k+4.                                  (1)

This holds also when the period itself is 2 modulo four. No assumption P=0
modulo four is made for unit-diagonal drift.

## 3. The top rail is a singleton, and three interior layers exist

The projected periodic path t_i=x_i+y_i is a finite closed +/-1 walk. Normalize
its largest value to zero and select a topmost visit as phase zero.
The checker/axis invariant is

    sigma=chi(p) on vertical arrivals, and -chi(p) on horizontal arrivals,
    chi(x,y)=(-1)^(x+y).

It is unchanged by one update. At the top level every visit arrives from below
and leaves downwards. Its incoming axis is fixed, so its turn type is constant:
E to S is R, whereas N to W is L. Stable alternation beginning with R forces
exactly one phase visit to the unique top class, and its heading is E.
Translate it to (0,0). Then sigma=-1; even layers have horizontal arrivals and
odd layers vertical arrivals. This is a consequence, not an extra initial-state
restriction.

The bottom extremum similarly has one R visit, arriving W and leaving N.
Both extrema therefore have horizontal arrivals, and the width W is even.
Width zero is impossible because each move changes t by +/-1. If W=2, there
are only three classes, the extremes both odd; hence g is two or three, contrary
to g=0 modulo four. Thus W>=4.

In particular layers -1,-2,-3 are present, and at least one further lower
layer remains after they have been constructed. This fact is the only width
information used below. The published stronger diagonal-width exclusions are
NOT dependencies of this proof.

## 4. An exact finite description of the first three layers

Construct complete stable visit lists in decreasing t. The top layer consists
of one event `(t,k,h)=(0,0,E)`.

For an interior event, let b_k be 1 for arrival from the already processed upper
side, and 0 for arrival from below. Let e_k be 1 for departure to that upper side.
The literal turn rule, with turn R/L fixed by the parity of k, gives

    e_k=b_k XOR (k mod 2)            at even t,
    e_k=1-(b_k XOR (k mod 2))        at odd t.               (2)

The arrival heading is W/E for b=1/0 at even t, and S/N at odd t.
The next layer's incoming and outgoing incidences on the upper side are fixed
by the preceding complete layer. Call their counts I,J. A local arrival word
b_0...b_(m-1) is count-compatible exactly when

    sum b_k=I,    sum e_k=J.

**Local length bound.** Every compatible word satisfies

    m <= 2(I+J)+1.                                        (3)

At even t each odd-ranked event contributes one to b+e; at odd t each
even-ranked event contributes one. Thus floor(m/2)<=I+J, proving (3).
This bound is independent of P and of all deeper layers. It makes the finite
local enumeration complete even though the global period and width are unknown.

### Ordered edge matching, with the full drift retained

In the sigma=-1 sector each undirected lattice edge has a fixed direction of
use. On a physical edge, outgoing traversals at its source and incoming
traversals at its target match first to first, second to second, and so on.
There is no additional pairing permutation: the arrival is one time step later.

For representatives b_t=(0,t), the integer voltage delta of an edge is defined by

    b_source + outgoing_unit_vector = b_target + delta*(1,-1).

Thus delta=+1 for E, -1 for W and zero for N/S. Ordered matching on any edge
whose two classes are already constructed fixes a directed successor edge
between events. Source and target stable times obey

    tau_target-tau_source = 1-P*delta.                     (4)

Every actual periodic trace induces exactly such a matched partial graph. A
partial graph may be rejected by necessary conditions without asserting that
all unrejected graphs extend to a physical trace.

## 5. Three elementary rejection certificates

The complete current layer's visits will never be changed within one branch.
Only visits in previously unbuilt layers may be adjoined.

### 5.1 Premature phase cycle

A closed directed component of fixed successor edges cannot later connect to
mandatory events on a lower unbuilt layer. But a period consists of one cycle
of all P phase events. A certified fixed closed component is therefore
impossible before the lower layers have been reached.

### 5.2 A universally positive chronological circuit

If no closed component exists, all components are open directed chains. For
an event i in chain A, let p_i be its index starting at zero, v_i its accumulated
voltage, and z_A the chain-root stable time. Equation (4) gives

    tau_i=z_A+p_i-P*v_i.

For consecutive ranks i,j in one class, (1) yields

    z_B-z_A >= 4+p_i-p_j+(v_j-v_i)*P.                       (5)

Sum specified inequalities (5) around a directed circuit of chain variables.
The roots cancel, yielding `0 >= C+KP`, with integer C,K. Let n be the number
of constructed events. Every eventual period has P>=n. Therefore

    K>=0 and C+K*n>0                                     (6)

is a certificate of impossibility for EVERY possible final period.

Each retained rejection lists the original consecutive-rank pairs producing
its circuit. The independent checker reconstructs its edges and sums C,K;
it verifies (6) directly. Thus neither Bellman--Ford correctness nor treating
P as an infinitely large parameter is a premise of the certified result.
The generator uses lexicographic affine weights merely to find witnesses.

### 5.3 A repeated physical cell with unchanged read colour

An open fixed chain is a contiguous physical orbit segment in any completion.
Translate it sufficiently far along the hypothetical highway so all its visits
lie in the stabilized finite-support regime. Reconstruct its successive
physical positions by literal moves. Two consecutive readings of the same cell
must have opposite turn letters. A fixed segment violating this is impossible.

In every final case here the conflicting word is

    R L R R R R L L R.                                    (7)

Starting north at (0,0), its nine pre-update positions are

    (0,0),(1,0),(1,1),(2,1),(2,0),(1,0),(1,1),(0,1),(0,0).

The origin is first read R, is not read during the seven intermediate updates,
and is then read R again. It should be black on the second read, so its turn
must be L. This contradiction is independent of initial colouring and heading;
quarter-turn rotation handles other headings. The other repeated cells in the
segment do have alternating colours and do not remove the origin contradiction.

## 6. Exhaustive local certificate and conclusion

Enumerate all complete arrival strings satisfying (2)-(3), layer by layer.
Reject only by one of the explicit certificates in Section 5. The results are:

| Added layer | Complete local branches | Fixed cycles | Chronological circuits | Conflicting reads | Survive |
|---|---:|---:|---:|---:|---:|
| -1 | 4 | 0 | 2 | 0 | 2 |
| -2 | 124 | 26 | 96 | 0 | 2 |
| -3 | 12,756 | 3,198 | 9,534 | 24 | 0 |

Total: **12,884** local branches. At no point are more than **38** events
constructed. These are not period limits: they are consequences of the local
incidence bound and the surviving upper layers.

After layer -1 the only arrival strings are `100` and `1000`. The former has
no admissible next layer. The latter has exactly these two surviving extensions:

    1000 / 00001101,
    1000 / 000011010.

The first is an even class at layer -2; the second an odd class. After the
third layer, 24 candidates survive only the cycle/order checks. Every one
contains (7), so all are rejected by literal read consistency.

The generator's complete certificate is `evidence/certificate.json`, containing
one outcome for each enumerated arrival-string path. The independent checker:

1. enumerates complete strings using combinations of I incoming positions,
   instead of the generator's incremental binary recursion;
2. reconstructs all nodes first and matches geometric directed edges afterwards,
   instead of attaching them during growth;
3. checks each negative witness directly, rather than running the generator's
   affine-cycle search;
4. requires exactly one record for every possible child, and no unexplored leaf.

Every hypothetical real trace must reach one of these branches, by Sections
2-4. Every terminal branch is impossible, by its verified certificate and
Section 5. Since W>=4, premature closed components really do have mandatory
unbuilt successors below. No candidate reaches a fourth layer. This contradiction
proves the theorem, with no global period or width bound. QED.

## 7. Integration note

The unit-diagonal argument combines with the periodic-growth lemmas.
The project reproduction entrypoint checks their exact certificates.
