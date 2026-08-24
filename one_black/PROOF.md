# Universal one-black proof

## Theorem and canonical pose

A state records the black cells, ant position, and heading. Before every move
the ant reads its cell, turns right on white or left on black, toggles the cell,
and advances one lattice edge. The formal result is

```lean
theorem OneBlack.universal_one_black :
    ∀ s, ExactlyOneBlack s → ReachesP104 s
```

Translation and quarter-turn rotation commute with the dynamics and preserve
P104. It is therefore enough to place the ant at the origin, heading north,
with a single black cell `q`.

## 1. Blank orbit and permanent P104

Exact replay of the blank plane reaches a state `E` after 9,977 updates. Its
next 104 updates read a 40-cell support `S`, restore the heading, and translate
the state by

```text
v = (-2, -2).
```

The finite colour difference between one block and its translate lies on
affine rays disjoint from all later translated supports. The checked block
therefore repeats forever by induction. `Core`, `Semantics`, `HighwayData`, and
`Highway` contain the dynamics, symmetries, exact replay, and permanent-block
theorem.

## 2. First contact with the black cell

The first 9,977 blank updates read 1,376 distinct cells.

If `q` is one of them, `PrefixData.lean` supplies its terminal witness time.
Exact replay and the sound terminal checker prove P104 for all 1,376 cases.

Otherwise the singleton orbit has exactly the blank read trace for 9,977
updates. At entry it is

```text
blacken q E.
```

This is the untouched-cell coupling theorem in `Coupling`; `Prefix` packages
the finite branch.

## 3. Geometry at highway entry

At `E`, the cell `q` belongs to exactly one of the following classes.

1. It is already black in `E`.
2. It is a white cell of the active 40-cell support `S`.
3. It lies outside every future translate of `S`.
4. It is a future first-read cell of the highway.

The first class is `E` itself. The second is a finite terminal table. In the
third, the ant never reads `q`, so the permanent blank highway is unchanged.

For the fourth class, let `H` be the support cells whose predecessor under
translation by `v` is outside `S`. Exact affine diagonal, parity, and order
tests prove

```text
|H| = 22,
q = h + d v       for a unique h ∈ H and d > 0.
```

Thus every unbounded post-entry case is a single defect on one of 22 P104
frontier channels. `Geometry`, `Rays`, and `Entry` prove this decomposition.

## 4. Single-defect scattering spectrum

For a channel head `h` and depth `d`, define the scattering state

```text
Σ(h,d) = blacken (h + d v) E.
```

`Scattering.Classification` is the independent structural theorem for this
family. It proves that the 22 heads split exhaustively into

```text
21 ordinary return channels
+
1 exceptional reverse-highway channel.
```

Every positive depth in an ordinary channel returns to P104. The exceptional
channel has head

```text
h₇₂ = base.pos + (-2, -8),
```

and its stable scattering block is an exact opposite-drift P104 block. The
classification also records its affine depth law and proves return to P104 at
every positive depth. The universal theorem consumes this classification as a
single lemma; the two responses are proved below.

## 5. Channel-local anchors

Each head `h` has two finite cut points.

- `P_h = stableDepth h` anchors the pristine scattering induction.
- `A_h = actualCutoff h` ends the direct replay band at the real entry state.

The certificate proves `P_h ≤ A_h` for every ordinary head. These values are
chosen independently for each channel. The finite leaves are therefore

```text
pristine:  1 ≤ d < P_h,
actual:    1 ≤ d < A_h,
```

followed by one stable pristine replay at `P_h`. At a deep actual depth
`A_h+n`, the corresponding pristine induction parameter is

```text
(A_h - P_h) + n.
```

`EntryData.lean` stores only these channel-local witness bands. The exceptional
channel uses two distinct local anchors:

```text
P₇₂ = 11,       A₇₂ = 15,       A₇₂ - P₇₂ = 4.
```

Depth 11 is the first pristine reverse-block anchor. Four clean translations
place the actual historical state at depth 15 into the affine collision family.
For an ordinary channel, `A_h` is the first depth whose complete translated
footprint and terminal corridor are separated from the historical wake. Thus
the cutoff is selected by the geometric invariant used in the theorem, rather
than by an unrelated common search window or a coincident terminal time.

## 6. Ordinary scattering

For a pristine highway, compare one clean P104 block with its translate. Their
finite XOR difference is a wake `W`. Starting at depth `P_h+n` executes `n`
clean blocks before the anchored scattering, accumulating

```text
W ⊕ (W+v) ⊕ ... ⊕ (W+(n-1)v).
```

Exact ray tests prove that these translated copies miss every later clean
read, the anchored scattering trace, and its permanent terminal corridor.
They are inert archives, so the generic induction theorem reduces all depths
`d ≥ P_h` to the checked anchor. `Induction`, `PristineChecks`, and `Pristine`
prove this for all 22 pristine channels.

The actual entry state contains 715 black cells. Thirteen form the active P104
pattern; the remaining 702 form the historical wake `H_E`. For an ordinary
head, the relevant translation lag is

```text
L_h = A_h - P_h.
```

The finite certificate anchors `H_E` at that lag. Affine ray induction proves
that every later translated scattering footprint and terminal corridor stays
disjoint from `H_E`. Untouched-region coupling then identifies the actual tail
at depth `A_h+n` with the pristine tail at depth `P_h+(L_h+n)`. Combined with
the direct band `d < A_h`, this proves every depth of all 21 ordinary channels.

`ActualGuards`, `ActualHistory`, `OrdinaryCorridor`, `OrdinaryGeometry`, and
`Ordinary` implement this reduction.

## 7. Exceptional backscattering

For `h₇₂`, the depth-11 pristine scattering enters a P104 block with drift

```text
-v = (2, 2).
```

`Phase.reverse_block_exact` proves the entire 104-step reverse block, including
its finite XOR wake. The recurrence indexes this wake from the next translated
reverse block. Exact positive-copy ray tests show that every wake cell misses
every later reverse read, so the block iterates indefinitely. At the actual
base depth 15, four forward translations are cancelled by four reverse blocks;
ten further reverse blocks and phase 89 reach the first historical collision
at `(20,-22)`. The certificate checks every earlier phase against every
historical cell.

Increasing the obstacle depth by one adds one forward block and one reverse
block before the same collision, so

```text
t_hit(n) = t_hit(0) + 208 n.
```

At that time `Scattering.Classification.exceptionalAffine` gives the exact
state equation

```text
run(t_hit(n), Σ(h₇₂,15+n))
  = actualHit XOR (L ⊕ (L+v) ⊕ ... ⊕ (L+(n-1)v)).
```

The depth-15 collision reaches a terminal state after 7,994 updates. Exact trace
and ray guards prove that all accumulated layers miss both this post-hit trace
and its permanent corridor. XOR archive induction therefore proves every
depth `15+n`; the channel-local direct band proves depths 1 through 14.

The `Phase*` modules separate the reverse block, first collision, XOR algebra,
affine hit normal form, and terminal tail.

## 8. Universal assembly

`Scattering.single_defect_scattering` assembles the 21 ordinary theorems and
the exceptional affine theorem into the complete 22-channel spectrum.
`Universal.entry_reaches` combines that spectrum with the entry geometry.
`Universal.canonical_reaches` adds the 1,376 prefix cases, and
`Universal.pose_decomposition` restores arbitrary position and heading.

The resulting chain is

```text
blank replay → permanent P104
             → prefix contact or untouched coupling
             → entry geometry
             → 22-channel scattering classification
             → universal one-black theorem.
```

## 9. Finite computation

The complete build has three native computation leaves:

1. the blank 9,977/P104 certificate in `HighwayData`;
2. the 1,376 prefix cases in `PrefixLeaf`;
3. the shared 22-channel scattering certificate in `ScatteringLeaf`.

After the blank leaf, Lake evaluates prefix and scattering in parallel. The
scattering leaf contains:

- active-support terminal witnesses;
- each channel's shallow pristine and actual bands;
- one stable pristine result per channel;
- ordinary historical-wake separation;
- the exceptional reverse block, first hit, and post-hit guards.

Each stable result is produced by one tail-recursive forward pass and stores
its final state, deduplicated read set, cached read list, terminal orientation,
and acceptance bit once. The pristine, ordinary-history, and exceptional
checks share those values. The phase report likewise binds the history list,
reverse state and wake, post-hit replay, terminal orientations, and layer
carrier once. Its reverse-wake checker uses precisely the positive-copy ray
condition required by the reverse block. Known witness times are replayed
directly; generation-time search is absent from proof checking.

The generated lane tables contain 152 pristine replay witnesses and 179
actual-entry replay witnesses. Their known times total 1,380,384 and 2,761,211
updates respectively. The generator computes the exact lane-local geometric
cutoff first and emits only the direct cases below it; this optimization is
confined to the finite leaves and does not appear in the scattering theorem.

`PrefixLeaf` and `ScatteringLeaf` turn the checked Boolean reports into typed
Lean certificates. `Scattering.single_defect_scattering` turns the latter into
the mathematical spectrum. Finally `OneBlack.universal_one_black` combines
the prefix certificate, spectrum, and analytic Lean lemmas.
`python3 one_black/check.py` builds this closed theorem from the checked-in
sources and witness tables.
