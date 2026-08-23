# Langton's Ant: minimal proof and research core

This clean-room repository locally closes exactly two results for the classical
two-colour Langton ant:

1. The blank plane enters the translating period-104 highway after 9,977
   updates.
2. If the only black square is initially under the ant, the ant enters that
   highway after 9,978 updates, for every initial position and heading.

The predecessor project contains substantially stronger results and a long HC
research program. Their mathematical content, evidence status, failed
abstractions, and remaining proof fork are compressed in [`RESEARCH.md`](./RESEARCH.md).
They are not silently treated as locally reconstructed proofs.

Run the finite proof obligations with:

```sh
python3 scripts/check.py
```

The repository has three proof-bearing parts:

- `engine/langtons_ant/` — the exact update rule and finite witnesses;
- `PROOF.md` — the recurrence and symmetry argument;
- `scripts/check.py` — the direct replay of the two finite obligations.

`RESEARCH.md` is the sole research-state surface. No predecessor source,
certificate data, test matrix, or directory topology was imported.
