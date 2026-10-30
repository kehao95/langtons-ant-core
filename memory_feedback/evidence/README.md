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

## Crossing information

Full-field Python/C++ comparisons, exact capacity and packing, corner bounds and remote-history guards.

[Module and retained evidence](../verification/crossing_gap/). Run
`python3 memory_feedback/reproduce.py --crossing-only`. The analytic coverage
argument is in the article and [proof map](../PROOF.md).

The [request-capacity report](../verification/crossing_supply/report.json)
binds the request reconstruction and packing controls. The same
`--crossing-only` command replays both crossing modules.
