# Four-cell one-sided highway forcing: a sharp half-plane threshold

**15 October 2026. Classical Langton ant, white -> right, black -> left, flip then move.**
Evidence: analytic coverage and coupling, exact finite certificates, three independently implemented finite checks, and two algebraic all-future reductions. See the [15 October audit](evidence/README.md) for the verification scope and source corrections.

## 1. Main theorems (complete quantifiers)

Write `H_+ = {(x,y) in Z^2 : x>=0}`. Let `F` be the ordinary classical Langton update on an infinite plane, and start the ant at `(0,0)` facing east (E). For the displayed finite seeds, unspecified cells are initially white.

**Theorem 1 (sharp one-sided escape threshold).** For every initial colouring, including arbitrary colours outside `H_+`, having at most THREE black sites inside `H_+`, the ant first visits the complementary left half-plane at a time `1<=t<=918`. The bound is attained by the finite black set

```
{(0,-1),(2,1),(3,3)}.
```

In particular, there is no black seed with at most three cells anywhere that keeps the entire forward trajectory in `H_+`.

**Theorem 2 (outgoing four-cell P104 port).** For the finite initial black set

```
G={(0,-1),(1,1),(1,3),(2,2)}
```

and `(p_0,h_0)=((0,0),E)`, every position `p_t` has `x>=0`. After 182 literal updates, the complete state has position `(5,1)`, heading E and 36 black sites. Its entire future has the exact standard blank-orbit P104 turn word, with period 104 and drift `(2,2)`, not merely an unknown translating cycle. The terminal period's read locations have x-coordinates in `[4,9]`, so the future remains in `H_+`.

Therefore **four is the exact minimum number of initially black cells for a one-sided, forever-right-half-plane (hence in particular one-sided standard-highway) port** from this fixed boundary pose.

**Theorem 3 (four-bit universal exterior P104 completion).** For EVERY complete finite-support initial state `X=(B,p,h)`, EVERY finite protected subset `K` of the plane and EVERY nonnegative integer `T`, there is an effectively computable four-element finite set `E` of initially white cells outside a square containing `B`, `K` and the entire radius-`T` ball about `p`, such that

```
E intersect B = empty,
positions, headings and read colours agree at every time 0 <= t < T,
(B union E,p,h) eventually has the standard P104 future.
```

If the protected square has n cells per side, the standard trace begins by update `E(n)+182`, where `E(n)=(13*3^(n-1)-2*n^2-4*n-5)/2`: the [integer clock](../clock_escape/PROOF.md) bounds first exit by E(n), followed by 182 port updates.

No restriction is placed on the trajectory or the initial shape of `B`. The theorem concerns the **changed initial configuration** `B union E`, not the original one, and does **not** imply HC. Neither does Theorem 1 establish that fewer than four exterior additions could never work by a more complicated non-one-sided mechanism.

## 2. Exhaustive proof of Theorem 1: no coordinate cutoff

Let `t(S)` be the first time the trajectory from finite seed `S subset H_+`, starting `(0,0),E`, is at x<0. In a finite prefix ending immediately BEFORE `t(S)`, let `V(S)` consist of all cells at their FIRST read during that prefix which were not in `S` (their first read was white). Define

```
F_0={empty},
F_(k+1)={S union {q}: S in F_k, q in V(S)}.
```

**Coverage lemma.** Suppose every member of `F_0,...,F_k` exits in finite time, and let `M` be the maximum of those exit times. Every colouring with at most k black cells in `H_+` exits by M. Otherwise its trajectory remains in `H_+` through M. Start with `S=empty`, a subset of its actual initially black set in `H_+`. If the trajectories agree until `t(S)`, the actual trajectory exits by M, a contradiction. Otherwise their first differing read must be at a cell initially black in the actual configuration and white in S: all previous writes agree. This cell has never been read earlier, so it belongs to `V(S)`. Adjoin it and repeat, advancing to the next family. At most k additions exhaust the actual initially black set in `H_+`; then no differing read is possible before exit. This proves the uniform bound, not only eventual escape.

This argument makes no bounding-box assumption on the positions of the input black sites: arbitrarily remote black cells are simply first read later, if ever. Initial black sites in `x<0` cannot be read before the first exit, and have no effect on it.

The complete finite enumeration gives

| k | distinct seeds `F_k` | maximum first-exit time |
|--:|--:|--:|
| 0 | 1 | 2 |
| 1 | 2 | 38 |
| 2 | 20 | 106 |
| 3 | 261 | **918** |

The maximal 918 occurs for exactly the displayed witness `{(0,-1),(2,1),(3,3)}` within the list. The last two states are: at time 917 (before update 917), ant `(0,7)` heading south, current square white; the right turn places the ant at `(-1,7)` heading west at time 918. The complete first-exit enumeration is stored in `evidence/escapes.json`; the small exact core checker recomputes every seed, its exact first-visit list, the next level, and each first-exit time. `verification/independent.py` independently branches online on *initial* colours of cells at their first visit using complex-coordinate turns, rather than enumerating predetermined seed subsets; its maximum is also 918. The independent online tree has fewer leaves because never-read/redundant placed black cells are not counted as meaningful choices.

The analytic coverage lemma plus these checked finite instances proves the universal claim. The finite check is a machine-assisted finite leaf, not a finite-radius experiment or an unproved sampling inference. No one-black or two-black pre-existing theorem is needed.

## 3. Verified four-cell infinite tail

The two integer/complex simulators agree on the full 182-update gate prefix, including the endpoint 36-cell black field (declarative list in `evidence/witness.json`):

```
B_0=G, p_0=(0,0), h_0=E;
B_182 has 36 black cells, p_182=(5,1), h_182=E.
```

All of `p_0,...,p_182` have nonnegative x-coordinate. Starting from that endpoint, the next 104 turns are the exact certified standard word from the blank-orbit period at update 9977:

```
LRLLRRRRLLRLLRRRRLLRRRRLLRLRRRRLRLLLLRRRRLRRLRRRRLLLLRLRRRRLRRRRLLLLRLRRRRLRLLRRLLLLRRLLRRRRLLRRLRLLRLLR
```

The heading returns to E, drift is `(2,2)`, and phase pre-update positions have x-coordinates in `[4,9]`. The repeated-word motion plan thus stays in x>=4, with x increasing by two each period. It remains to prove that the turn word repeats **forever**, not only for finitely many blocks.

### Two complementary all-future verifications

Write the 104 absolute pre-update phase positions as `q_i` and drift `d=(2,2)`. A prescribed read at epoch `k` and phase `i` is `q_i+k*d`. Before it, the colour is

```
colour(i,k) = 1_(q_i+k*d in B_182)
       XOR parity { (j,s): q_j-q_i=s*d,
                  s>0 or (s=0 and j<i), 0<=s<=k }.
```

For fixed i, every initial black hit occurs at one computable integer epoch, while each prior-phase contribution changes parity at a single computable threshold s. Inspect epochs zero, every self-overlap threshold, every initial black-hit epoch, and the epoch immediately after each hit. These partition all nonnegative epochs into constant intervals including the final infinite interval. The verifier checks all cases against the prescribed turn. Exactly 170 independent `(phase,epoch)` evaluations are performed. Induction on time proves the infinite tail.

The second, translation-class test, applying the periodic-realisability criterion of Jillhewar (2026), independently constructs the unique smallest initial black set `K_182` for the prescribed standard infinite ray starting at `(5,1),E`. It uses the chronological order of all 104 phase positions modulo the **full** drift group `Z*(2,2)`. For each class, stabilized turns must alternate `R,L,...` starting in white; finite leading prefixes may require finitely many initially black cells. The derived **13 black sites** are

```
(4,3),(4,4),(5,1),(5,5),(5,6),(5,7),(6,1),
(6,2),(6,3),(6,6),(7,1),(7,4),(7,5).
```

They are a subset of the complete physical B_182; the **remaining 23 black cells**, explicitly retained in the witness, miss every phase ray `q_i+N*(2,2)`. First-difference coupling thus shows the full 36-cell physical state has exactly the standard infinite read trace, without deleting the 23 inactive residuals. These two methods are separate checks of the full-future assertion; neither uses a finite 'observe many repeated blocks' heuristic.

The same direct all-future parity method rechecks the source blank orbit at time 9977 and confirms the canonical turn word and drift `(-2,-2)`.

## 4. Effective exterior four-cell completion: proof of Theorem 3

Given arbitrary complete finite X, finite K and prefix length T, choose an axis-aligned square Q containing `B`, `K`, the ant and the L-infinity ball of radius T about the original head. Use exact simulation to find the first exit state after `tau` updates: pose `(e,g)` with `e` outside Q. Every previous update is at a cell inside Q; the exiting step moves exactly one grid edge outward, so `g` is an outward side normal. This search terminates by classical finite-domain escape (independent proofs available; our existing strict clock gives an explicit time bound).

Rotate the four-cell gate G so that its initial heading E becomes g, and translate its origin to e. Call the resulting four-cell set E. Since all gate cells have x>=0 before rotation, they lie in the outward closed half-plane based at e, disjoint from Q and its complete black initial field. The original trajectory never reads E prior to tau. Induction gives identical positions, headings and read colours for `0<=t<tau`, together with the exact complete-field relation `B_t^+=B_t triangle E=B_t union E` for `0<=t<=tau`. The complete colourings differ by E from time zero. At the exit its actual field equals the old (possibly very complicated) finite black field inside Q, together with E outside Q.

From the exit, compare to the standalone gate run. All its future reads remain in its outside half-plane, while the original black debris remains strictly inside Q. Since those read regions are disjoint, exact colour first-difference coupling forces the augmented physical trajectory to agree with the standalone gate's future, starting at `(e,g)`, forever. The extra inside-Q black cells are physically present, but never read by this outgoing trajectory. Hence after 182 more updates it has the rotated standard P104 tail. Choosing Q to contain the radius-T ball ensures the augmented and original trajectories have identical first T position/heading/read-colour observations; K is unaffected. No future-live oracle or deletion appears in the construction.

This effectively constructs a standard-P104 certificate for the **four-cell augmented input**, whose standard trace starts by update `E(n)+182` for a protected n-by-n square. The original X may or may not already have a standard future. In particular, `forall X exists E (|E|=4 and H(X+E))` is NOT `forall X H(X)`.

## 5. What is new, and limits of publication claims

This advances the earlier 13-cell universal exterior-completion gate to a four-cell gate, and adds a **sharp** unbounded-coordinate half-plane exit theorem for at most three black sites, complete with a finite total proof checker. The upper/lower cardinalities agree for the canonical *one-sided gate* contract; no claim is made about the optimal number of arbitrary exterior edits without that contract.

The available literature check found prior work on finite-support circuit construction (Gajardo--Moreira--Goles 2002), standard P104, finite-support periodic realization (Jillhewar 2026), and quantitative finite-box escape (Etse, MFCS 2026). It did not locate this particular sharp half-plane cardinality theorem or four-cell exterior forcing property. This is a **nonexhaustive novelty search**, not proof of priority, accepted publication or external review.

The result is a coherent, self-contained **short-paper candidate** directly connected to finite-support HC: it shows that every finite physical initial history can be locally preserved while four additional exterior black cells guarantee a standard highway. It does not show any original input is necessarily positive, produce a negative seed, or classify nonperiodic orbits.

## 6. Reproduce the computer-assisted finite leaves

From the repository root:

```sh
python3 four_cell_port/reproduce.py
```

The runner copies the package to a temporary directory, reproduces the original
integer checker and independent online colour tree, and compares all three
original JSON artifacts byte for byte. It then runs a third integer-vector audit
against the declarative evidence and compares its deterministic result with
`audit.json`. All scripts use only Python 3.10+ and its standard library.

The third audit reconstructs all 284 family records, verifies 40 chronological
cell intervals in 22 translation classes for both the port and blank reference,
and tests adverse certificate changes, active-cell mutations and a blocker
10^100 periods ahead. Its 96 exterior-completion cases check observations,
complete-field difference, retained debris and the infinite tail, including
16 cases with coordinate offsets of magnitude 10^30. These cases validate the
constructor; the universal completion argument is the geometric proof above.

### References

- A. Gajardo, A. Moreira, E. Goles, *Complexity of Langton's ant*, Discrete Applied Mathematics 117 (2002), 41--50, DOI 10.1016/S0166-218X(00)00334-6.
- K. R. Etse, *How Long Can The Escaping Ant Be Confined?*, MFCS 2026, DOI 10.4230/LIPIcs.MFCS.2026.49.
- A. Jillhewar, *Finite-Support Periodic Highways of Langton's Ant*, public preprint and exact software, 2026, DOI 10.5281/zenodo.21381637.
- H. Ke, *Every One-Black-Cell Langton Ant Reaches the Period-104 Highway: A Lean-Checked Proof*, Zenodo (2026), version 0.2.0, DOI 10.5281/zenodo.23341609.
- H. Ke, *An Ant on the Clock: Exponential Escape Bounds for Langton’s Ant*, Zenodo (2026), version 0.2.0, DOI 10.5281/zenodo.23341604.
