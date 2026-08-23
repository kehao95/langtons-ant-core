# Universal one-black proof

## Dynamics and terminal predicate

A state is read immediately before an update. White turns the ant right, black
turns it left; the current cell is then toggled and the ant moves one edge.
North increases the second coordinate. `langtons_ant/model.py` implements this
definition with an immutable finite set of black lattice points.

A terminal boundary records a heading, 40 relative read requirements, and a
displacement. `standard_terminal` checks those local requirements and proves
that every initially black cell outside the block misses every future translate
of its read footprint. Once this predicate holds, literal replay of one block
and induction give a permanent translating orbit.

## Blank P104 witness

`verify_blank_highway` starts from the blank plane, performs 9,977 updates, and
calls the result `E`. It replays the next 104 updates and derives the required
colour of each cell at its first read. Repeated reads must agree. It checks:

1. the endpoint has the same heading and displacement `(-2,-2)`;
2. the next block has the same relative read requirements;
3. at `E` and its successor, all other black cells miss every later translated
   block footprint.

For the third check a future footprint point is `o+n(-2,-2)`, `n>=0`.
`_multiple` decides this equation exactly over the integers, so only finite
black support and one finite footprint are inspected.

If a state satisfies the requirements and separation condition, induction over
104 literal updates reproduces the witness block. Changed cells lie only in
that block; shifting the translate index by one re-establishes separation at
the endpoint. Induction on blocks proves permanent P104. Applying this lemma to
`E` proves the blank-plane result.

## One black square in the blank prefix

Before update 9,977 the blank orbit first reads exactly 1,376 cells.
`verify_prefix_one_black` derives this set from replay. For every such cell `q`
it starts with only `q` black and finds a checked terminal boundary within
110,000 exact updates. The enumeration is exhaustive and includes the starting
cell.

Translation and quarter-turn rotation commute with one update. Induction
therefore transports these canonical replays to every initial pose. If `q` is
outside the prefix, untouched-cell coupling reaches the complete blank-entry
state plus `q`; the remaining sections close those cases.

## Pristine boundary plus one obstacle

At a pristine boundary, let `P` be the 13 black requirements and `S` the
40-cell read support. Every lattice cell belongs uniquely to one class:

1. `q in P`;
2. one of the 27 white cells in `S`;
3. `f+k(-2,-2)`, `k>=1`, for one of 22 last support cells on a lane;
4. outside the entire future corridor.

Integer divisibility checks the partition. Class 1 changes nothing; class 4 is
never read. `verify_pristine_one_obstacle` replays all 27 class-2 cases and
depths 1 through 20 on all 22 lanes: 467 finite cases.

For a lane, one clean block translates the active pattern by `v=(-2,-2)` and
leaves a finite XOR wake `W`. The verifier checks that depth 21 after one clean
block is translated depth 20 XOR `W`, that `W` misses later clean blocks, and
that every backward translate of `W` misses both the depth-20 terminal trace
and its final terminal corridor. Thus depth `20+n` executes `n` clean blocks
and then the translated depth-20 computation while all accumulated wakes stay
inert. Induction closes every depth.

## The actual blank-entry wake

At update 9,977 the blank state has 715 black cells: the 13-cell active pattern
and a 702-cell historical wake `H`. The 27 active-white cases are replayed
directly. On each future lane, exact affine integer equations decide whether
`H` can meet the translated pristine depth-20 trace or its terminal corridor.

On 21 lanes every possible collision occurs below the induction base. Exact
replay closes that finite prefix; beyond it, untouched-set coupling reduces the
actual state to the translated pristine theorem. The sole exceptional lane has
head `(-2,-8)` and reverse terminal drift; it receives its own induction.

## Exceptional phase 72

Depths 1 through 19 are direct terminal cases. At depth 20 the pristine
scattering reaches a boundary drifting opposite to the clean highway. Exact
corridor intersection with all 702 history cells finds the first hit at
`(20,-22)`. Three consecutive literal replays anchor that increasing obstacle
depth by one adds one forward and one reverse P104 block: hit time grows by 104
while hit pose stays fixed.

Consecutive hit states differ by a finite XOR layer `L`, and the next pair by
`L+(-2,-2)`. The base hit reaches a terminal boundary after 7,994 updates.
Exact same-trace replay and affine ray checks prove every accumulated translate
of `L` misses the post-hit trace and final terminal corridor. Induction gives
the same terminal computation for every depth at least 20; direct cases close
the remaining depths.

## Exhaustion and theorem

Normalize the initial pose. If the unique black cell is in the blank prefix,
the 1,376-case theorem applies. Otherwise coupling reaches the complete
715-cell entry state plus the untouched black cell. There it is already black,
active white, outside the future corridor, on one of 21 ordinary lanes, or on
phase 72. The preceding arguments respectively make these cases trivial,
finite, permanently untouched, ordinary, or exceptional. The partition is
exhaustive, so every normalized one-black state reaches permanent P104.
Translation and quarter-turn symmetry give every initial position and heading.

The proof combines the five finite obligations executed by `check.py` with the
recurrence, separation, induction, exhaustive partition, and symmetry lemmas
stated in this document.
