# Standard-wake verification

Run the project entrypoint from the repository root:

```sh
python3 wake_synthesis/reproduce.py
python3 wake_synthesis/reproduce.py --baseline
```

`inputs/` preserves the exact count table generator, original event enumerator,
independent all-future seed verifier and original context-graph recipe.
`code/` and `reproduce.py` preserve the first consecutive-rank overlay and its
controls. `v2/` adds chain separation through a small source-pinned overlay.
`upper_pruning.py` verifies the closed-walk-preserving graph reduction and all
retained potential inequalities. `audit_counts.py` checks local binary strings,
class residue induction and the two count-minimum computations independently.
`audit_partial.py` independently tests 4,000 incomplete cycle embeddings using
the generated native predicate with the undefined-behavior sanitizer.

The project entrypoint selects the reduced upper certificate, runs the full
new enumeration, compares deterministic reports and verifies imported source
hashes. Adding `--baseline` repeats both preceding cap-168 searches. Native
programs may return resource-limit statuses; these are never accepted as a
completed uniqueness verification. Python assertions must remain enabled.

The source programs regenerate finite evidence. Coverage, completeness and
pruning arguments are in the project `PROOF.md` and manuscript; the verifier
makes no inference from finite ant simulation to all initial states.
