# Langton's Ant: proof and research core

## One-black theorem

This repository contains a complete Lean-checked proof that every classical
Langton-ant state with exactly one black cell, at any ant position and heading,
eventually reaches the standard translating period-104 highway:

```lean
theorem OneBlack.universal_one_black :
    ∀ s, ExactlyOneBlack s → ReachesP104 s
```

- [Read the proof](./one_black/PROOF.md)
- [Inspect and rebuild the proof artifact](./one_black/README.md)
- [Explore the interactive proof guide](https://kehao95.github.io/langtons-ant-core/)

The browser guide is explanatory. The theorem in
[`one_black/lean/OneBlack.lean`](./one_black/lean/OneBlack.lean) and its closed
Lean proof cone are authoritative. This result does not prove the general
finite-support Highway Conjecture.
