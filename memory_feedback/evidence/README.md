# Reproduction and certificate scope

The analytic finite-memory predictor is checked against literal dynamics.
Exact arithmetic-segment XOR representations preserve every skipped write.
The modules cover stale-memory events, symbolic continuation, event geometry,
remote feedback, the twenty-cell family and birth-filtered queries.
`--extensions-only` selects birth-filtered feedback; the default covers all six.

```sh
python3 memory_feedback/reproduce.py
```

[Proof dependencies](../PROOF.md) · [Source file hashes](../sources.json)
