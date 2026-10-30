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

## Axis parity

Three frozen reports for analytic identities, independent parity controls and exact cycle-edge counts.

[Module and retained evidence](../verification/axis_wake/). Run
`python3 wake_synthesis/reproduce.py --axis-only`. The analytic coverage
argument is in the article and [proof map](../PROOF.md).
