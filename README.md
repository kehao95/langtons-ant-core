# Langton's Ant: proof and research core

> **[Explore the interactive one-black proof guide](https://kehao95.github.io/langtons-ant-core/)**

## Main result

This repository contains a complete Lean-checked proof of the universal
one-black-cell theorem for the classical two-colour Langton ant:

```lean
theorem OneBlack.universal_one_black :
    ∀ s, ExactlyOneBlack s → ReachesP104 s
```

In words: from **every** initial state with exactly one black square, for every
ant position and heading, the ant eventually enters the standard translating
period-104 highway, up to translation and quarter-turn rotation.

The theorem is closed in
[`one_black/`](./one_black/README.md). Its final assembly is the short theorem
in [`one_black/lean/OneBlack.lean`](./one_black/lean/OneBlack.lean); the
definitions, analytic lemmas, finite witness tables, and exact replay checks
are all kept in the same proof cone.

This does **not** prove the general finite-support Highway Conjecture. That
problem remains open.

## Start here

| Goal | Entry point |
|---|---|
| Build intuition and replay representative cases | [Interactive proof guide](https://kehao95.github.io/langtons-ant-core/) |
| Read the complete mathematical argument | [`one_black/PROOF.md`](./one_black/PROOF.md) |
| Understand the artifact layout and finite certificates | [`one_black/README.md`](./one_black/README.md) |
| Inspect the final formal theorem | [`one_black/lean/OneBlack.lean`](./one_black/lean/OneBlack.lean) |
| Rebuild the checked theorem | `python3 one_black/check.py` |

The browser guide is explanatory: it visualizes the certified partition and
runs the classical rule directly, but it is not a proof authority. The Lean
theorem and its checked finite leaves are canonical.

## Proof at a glance

Translation and quarter-turn symmetry reduce an arbitrary one-black state to
an ant at the origin, heading north, with its single black cell at `q`. The
proof then exhausts every possible location of `q`:

1. **Untouched region.** If the blank orbit never reads `q`, the perturbed
   orbit is identical to the blank orbit and inherits its permanent P104
   highway.
2. **Finite prefix.** Before highway entry at update 9,977, the blank orbit
   reads exactly 1,376 distinct cells. Exact replay supplies a terminal P104
   witness for placing `q` at each one.
3. **P104 scattering.** Every remaining future-read cell lies at a unique
   positive depth on one of 22 affine frontier channels of the highway.
   Pristine scattering is reduced to finite anchors plus P104 translation
   induction.
4. **Actual finite history.** The real entry state retains a 702-cell
   historical wake. For 21 ordinary channels, exact separation guards and
   untouched-region coupling transfer the pristine result through that wake.
5. **Exceptional reverse highway.** The remaining phase-72 channel first
   enters an opposite-drift P104 block, returns to a fixed historical
   collision by an affine depth law, and then scatters into permanent P104.

These branches assemble as

```text
blank replay → permanent P104
             → prefix contact or untouched coupling
             → 22-channel entry geometry
             → 21 ordinary returns + 1 exceptional backscatter
             → arbitrary position and heading
             → universal one-black theorem.
```

The numbered views in the interactive guide follow this same case split.

## Verification

Build the complete theorem from any working directory with:

```sh
python3 /path/to/langtons-ant-core/one_black/check.py
```

The command builds the closed Lean target. Verification uses the checked-in
finite witness tables and exact Lean replay; generation-time search is not
part of proof checking. To regenerate the witness tables independently, run:

```sh
python3 one_black/lean/generate.py
```

The proof has three finite computation leaves: the blank 9,977/P104
certificate, all 1,376 prefix placements, and the shared 22-channel scattering
certificate. Lean turns their accepted reports into typed certificates before
the universal theorem consumes them.

## Status and broader research

- **Universal one-black theorem:** proved and Lean-checked.
- **Blank-plane theorem:** proved; the blank orbit enters P104 after exactly
  9,977 updates.
- **General finite-support Highway Conjecture:** open.

The root [`PROOF.md`](./PROOF.md) develops exact consequences beyond the
one-black theorem, including the clean-envelope condition, interaction index,
and complete-history renewal. [`RESEARCH.md`](./RESEARCH.md) records the open
program around effective compactness and finite-seed compilation. Neither file
is promoted to a universal finite-support theorem.

Repository ownership is one-way:

```text
one_black/            closed theorem, certificates, and replay
    ↓
PROOF.md              proved general consequences
research/             executable deductions
RESEARCH.md           open Highway Conjecture program
docs/                  explanatory interactive guide
```
