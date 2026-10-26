# Reproduction and certificate scope

[Integer-clock certificates](integer/README.md) check all local branches
and the square range. [Critical-clock certificates](critical/README.md) cover
the critical square and fixed-height rectangle arguments. The supercritical
local algebra is formalized in `../lean/ClockLemmas.lean`; the state model,
finite-range estimates and orbit algorithms have analytic proofs.

Use `--integer-only` or `--critical-only` for the corresponding algebraic checks.
The default also checks the earlier rational clock and its Lean lemmas.

```sh
python3 clock_escape/reproduce.py
```

[Proof dependencies](../PROOF.md) · [Source file hashes](../sources.json)
