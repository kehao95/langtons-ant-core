# Langton's Ant: minimal proof and research core

This clean-room repository locally closes two terminal families for the
classical two-colour Langton ant:

1. The blank plane enters the translating period-104 highway after 9,977
   updates.
2. Every initial state with exactly one black square eventually enters that
   highway, for every ant position and heading.

The complete theorem, proof narrative, exact dynamics, finite verifier, and
reproduction entrypoint are closed under [`one_black/`](./one_black/README.md).
That directory has no dependency on the rest of the repository.

The root [`PROOF.md`](./PROOF.md) collects consequences outside that theorem:
the clean-envelope condition, exact interaction index, and structural results.
Complete-history renewal is reconstructed there as a total computable,
lossless presentation:
a seed reaches P104 exactly when its renewal program halts, exactly when its
canonical divergence genealogy has finite height.

The predecessor project contains substantially stronger results and a long HC
research program. Their mathematical content, evidence status, failed
abstractions, and remaining proof fork are compressed in [`RESEARCH.md`](./RESEARCH.md).
They are not silently treated as locally reconstructed proofs.

Replay only the universal one-black proof with:

```sh
python3 one_black/check.py
```

Replay the separate renewal consequences with:

```sh
python3 research/check.py
```

The architecture is one-way:

```text
one_black/            closed theorem and replay
    ^
    |
research/             executable consequences
PROOF.md              proved general consequences
RESEARCH.md           evidence map and open frontier
```

`one_black/` owns the theorem. `research/` owns executable deductions that use
it. Root documents provide the general proof boundary and research map; they
are not hidden inputs to the one-black replay.

`RESEARCH.md` is the sole research-state surface. No predecessor source,
certificate data, test matrix, or directory topology was imported.
