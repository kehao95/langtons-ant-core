# Langton's Ant: proof and research core

> **[Explore the interactive one-black proof guide](https://kehao95.github.io/langtons-ant-core/)**

## Status

- **Universal one-black theorem: proved and Lean-checked.** Every classical
  Langton-ant state with exactly one black square reaches the standard P104
  highway, for every ant position and heading.
- **Blank-plane theorem: proved.** The blank orbit enters P104 after exactly
  9,977 updates.
- **General finite-support Highway Conjecture: open.** The root proof and
  research documents develop exact reductions and structural consequences
  without promoting them to a universal finite-support theorem.

This repository proves two terminal families for the classical two-colour
Langton ant:

1. The blank plane enters the translating period-104 highway after 9,977
   updates.
2. Every initial state with exactly one black square eventually enters that
   highway, for every ant position and heading.

[`one_black/`](./one_black/README.md) contains the theorem, proof narrative,
exact dynamics, shared finite certificate, Lean proof, and reproduction entrypoint.

[`docs/`](./docs/) contains the source of the
[interactive proof guide](https://kehao95.github.io/langtons-ant-core/). It
visualizes the certified case split and replays the classical rule in the
browser; it is an explanatory view of `one_black/`, not a separate proof
authority.

The root [`PROOF.md`](./PROOF.md) develops the clean-envelope condition, exact
interaction index, complete-history renewal, and structural results.
Complete-history renewal is reconstructed there as a total computable,
lossless presentation:
a seed reaches P104 exactly when its renewal program halts, exactly when its
canonical divergence genealogy has finite height.

[`RESEARCH.md`](./RESEARCH.md) organizes the broader Highway Conjecture program
around exact state representations, causal ownership, effective compactness,
and finite-seed compilation.

Build the universal one-black proof with:

```sh
python3 one_black/check.py
```

Replay the renewal consequences with:

```sh
python3 research/check.py
```

The architecture is one-way:

```text
one_black/            theorem and replay
    ^
    |
research/             executable consequences
PROOF.md              proved general consequences
RESEARCH.md           Highway Conjecture research program
```

`one_black/` owns the theorem. `research/` builds executable deductions from
it. The two root documents present the general consequences and research map.
