# Langton's Ant: two proved initial families

This clean-room repository contains exactly two results for the classical
two-colour Langton ant:

1. The blank plane enters the translating period-104 highway after 9,977
   updates.
2. If the only black square is initially under the ant, the ant enters that
   highway after 9,978 updates, for every initial position and heading.

The arbitrary-offset one-black problem and the finite-support Highway
Conjecture are not proved here.

Run the finite proof obligations with:

```sh
python3 scripts/check.py
```

The repository has three proof-bearing parts:

- `engine/langtons_ant/` — the exact update rule and finite witnesses;
- `PROOF.md` — the recurrence and symmetry argument;
- `scripts/check.py` — the direct replay of the two finite obligations.

No predecessor source, proof text, or certificate data was imported.
