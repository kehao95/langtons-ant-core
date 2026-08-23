# Langton's Ant: minimal proof and research core

This clean-room repository locally closes two terminal families for the
classical two-colour Langton ant:

1. The blank plane enters the translating period-104 highway after 9,977
   updates.
2. Every initial state with exactly one black square eventually enters that
   highway, for every ant position and heading.

It also proves the clean-envelope sufficient condition and the lossless
structural theorems collected in [`PROOF.md`](./PROOF.md). Complete-history
renewal is reconstructed there as a total computable, lossless presentation:
a seed reaches P104 exactly when its renewal program halts, exactly when its
canonical divergence genealogy has finite height.

The predecessor project contains substantially stronger results and a long HC
research program. Their mathematical content, evidence status, failed
abstractions, and remaining proof fork are compressed in [`RESEARCH.md`](./RESEARCH.md).
They are not silently treated as locally reconstructed proofs.

Run the finite proof obligations with:

```sh
python3 scripts/check.py
```

The repository has three proof-bearing parts:

- `engine/langtons_ant/` — the exact update rule, witnesses and renewal event;
- `PROOF.md` — terminal and structural proofs;
- `scripts/check.py` — direct replay of every finite obligation claimed here.

`RESEARCH.md` is the sole research-state surface. No predecessor source,
certificate data, test matrix, or directory topology was imported.
