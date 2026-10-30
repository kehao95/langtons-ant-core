# Reproduction and certificate scope

The analytic bounded-fold cover and read-chronology reduction connect
physical trajectories to integer formulas. Exact supplied-schema checks use
ISL/GMP and Z3; these libraries are computational trust dependencies.
Small-witness bounds are analytic. `--new-results-only` selects the six
quantifier-free backend checks; the default also checks the resource modules.

```sh
python3 defect_synthesis/reproduce.py
```

[Proof dependencies](../PROOF.md) · [Source file hashes](../sources.json)

## Six-cell certificate

Exact XOR recurrence, all-future half-ray guards, seam counts and independent full-field C++ checks.

[Module and retained evidence](../verification/six_cell_feedback/). Run
`python3 defect_synthesis/reproduce.py --six-cell-only`. The analytic coverage
argument is in the article and [proof map](../PROOF.md).
