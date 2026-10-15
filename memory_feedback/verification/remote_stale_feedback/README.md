# Remote stale-feedback checks

Proof: `proof/results/remote-stale-feedback.md`.

From the repository root run:

```sh
python scripts/check_remote_stale_feedback.py
```

The runner uses a disposable copy and compares the exact deterministic report.
`feedback.py` contains an isolated literal implementation, the existing suffix
and period criteria, and the new fixed-region filtered-event decision. `check.py`
uses independent complex-coordinate finite dynamics and a separate chronological
period criterion for its positive controls. All field data are retained.

A `NO_EXTERNAL_EVENT` answer is NOT `NO_HIGHWAY`: it certifies eventual translation,
whose standard identity is a separate question. Resource caps return `INCONCLUSIVE`.
The complete-field baseline functions are local reimplementations; no shared
trusted runtime was edited and no claim of a new periodic-word criterion is made.
The all-input theorem is analytic and unformalized, not established by finite tests.
