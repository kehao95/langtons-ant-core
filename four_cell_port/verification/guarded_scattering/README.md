# Guarded scattering and clocked renewal

A restricted, genuinely composable family of classical finite-support inputs.
See [the all-length proof](../../proof/guarded-scattering-renewal.md).
This is not an HC proof or an arbitrary-history termination theorem.

`check.py` contains the immutable 30-rule integer table, the exact mature-wake
constructor, a literal simulator, a separate vector simulator, two finite
all-future tail expressions, complete connector checks and local clock checks.
It depends only on the Python standard library and does not import or modify
shared repository code. Do not run with `-O`.

```sh
python experiments/hc_global/guarded_scattering/check.py \
  --compare experiments/hc_global/guarded_scattering/check_results.json
```

`construct(spec)` takes a sequence of `(fresh_phase, gap_periods)` with each gap
at least 100 and compatible successive orientations. It returns the COMPLETE
initial field with all obstacles preinstalled, the certified collision schedule,
and the final standard boundary. It does not simulate long gaps. For example:

```python
from check import construct
state, events, time, position, orientation, phase = construct([(29,100),(15,100)]*12)
assert len(state.B) == 37 and time == 451214
```

The two orientations are NE and SE, not left/right-reflected rules. The report
records 30 kernel checks, 448 affine pair inequalities, 185224 clocked recovery
steps, and 27 complete finite train controls. Their unbounded extension uses
the proof's half-plane equality and nesting induction, not the finite controls.

Excluded patterns, insufficient gaps and rejection by this library are not
negative answers to HIGHWAY. The old debris remains in the physical state.
