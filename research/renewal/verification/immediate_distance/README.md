# Immediate-target edit-distance obstruction

This isolated package proves and checks a failed HC-ranking candidate:

```
all n>=0, M>=1000:
  delta(X(n,M))=1;
  PGStep executes exactly LRL (three updates);
  delta(F^3 X(n,M))=n+10;
  FIRST P104 entry = 12440, independent of n and M.
```

`delta` minimizes colour edits to an **immediate** standard future at the fixed
pose. It is not distance to the eventual basin or an actual active-memory count.
The 4n remote padding cells remain unread on the entire actual trajectory.
They obstruct hypothetical immediate tails only. No HC counterexample or
all-input termination result is asserted.

The proof is `proof/results/immediate-highway-distance-obstruction.md`.
`base_positive.json` records the full 803-cell finite endpoint and its infinite
certificate. `check_results.json` records an actual deterministic local replay.
The baseline periodic verifier is an unchanged, hash-pinned copy of the earlier
integration helper, not a newly claimed realization theorem.

Run from this folder:

```sh
python check.py --compare check_results.json
```

Or use the repository runner `python scripts/check_hc_continuation.py`.
Python 3.10+ standard library suffices. Do not use `-O`. The checker never writes
its frozen witnesses unless an explicit output path is supplied.
