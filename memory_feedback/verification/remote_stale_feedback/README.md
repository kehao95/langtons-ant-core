# Remote stale-feedback checks

Proof: [remote-stale-feedback](../../proof/remote-stale-feedback.md).

From the repository root run:

```sh
python memory_feedback/reproduce.py
```

The runner uses a disposable copy and compares the exact deterministic report.
`feedback.py` contains an isolated literal implementation, the existing suffix
and period criteria, and the new fixed-region filtered-event decision. `check.py`
uses independent complex-coordinate finite dynamics and a separate chronological
period criterion for its positive controls. All field data are retained.

A `NO_EXTERNAL_EVENT` answer is NOT `NO_HIGHWAY`: it certifies eventual translation,
whose standard identity is a separate question. Resource caps return `INCONCLUSIVE`.
The complete-field baseline functions are local reimplementations; their supplied-word criterion is stated and attributed in the proof.
The all-input theorem is analytic and unformalized, not established by finite tests.
