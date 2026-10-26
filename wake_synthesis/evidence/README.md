# Reproduction and certificate scope

The complete classification combines analytic coverage, integer period
bounds and exhaustive ordered-event searches. The default runner covers the
76 thin-wake cases in 83 native jobs. `--quick` checks the upper graph, count
tables and controls while omitting that exhaustion. `--extensions-only` checks
periodic arithmetic. The layer-profile special case also has a separate
`verification/profile_classification/reproduce.py` entrypoint.

```sh
python3 wake_synthesis/reproduce.py
```

[Proof dependencies](../PROOF.md) · [Source file hashes](../sources.json)
