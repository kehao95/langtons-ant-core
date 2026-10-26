# Reproduction and certificate scope

The final theorem is `OneBlack.universal_one_black_standard_trace`.
Its proof covers all positions and headings through 22 affine channels and
retains the complete physical history. Both final theorems use `propext`,
`Classical.choice`, `Quot.sound` and three native computation leaves:

- `Highway.checks_pass._native.native_decide.ax_1_1`
- `PrefixLeaf.verified._native.native_decide.ax_1_1`
- `ScatteringLeaf.verified._native.native_decide.ax_1_1`

Lean 4.30.0, its native compiler and runtime form the computational trust base.
The runner builds in a disposable directory and checks both complete axiom lists.

```sh
python3 one_black/reproduce.py
```

[Proof dependencies](../PROOF.md) · [Source file hashes](../sources.json)
