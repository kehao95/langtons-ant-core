# Composable unbounded-return scattering

Exact standard-library checker for the analytic theorem in
`proof/results/return-scattering-closure.md`. This is NOT HC or a self-renewing
controller. All obstacles are finite and preinstalled at input time.

Each parameter n>=100 makes a NW excursion, a phase-72 reversal, a real read of
an earlier NE black lifetime, and a protected recovery. Two initial markers
suffice for the SE convergence result. A third resets the output to NE, allowing
arbitrarily many such packets to be composed. The old lifetime has exact age
208n+53684. Packet size and backward displacement are unbounded.

```
python experiments/hc_global/return_scattering/check.py --compare experiments/hc_global/return_scattering/report.json
```

No `-O`. The checker pins the unchanged neighbouring `guarded_scattering/check.py`
SHA256, reuses its exact word/simulator/infinite-tail/clock primitives, and runs
only the new kernels, bridges, negative controls and complete train witnesses.
`--output PATH` writes a regenerated report. `--compare PATH` byte-compares it.

The all-parameter argument is analytic. The 5685 exact affine inequalities,
finite-XOR field construction and infinite-tail certificates are not replaced
by the 8 supplementary finite input cases. Local clock checks cover 85073 steps;
complete controls contain 15 packets and 1752102 updates per simulator.
Report hashes bind the source and complete fields. No old suite or Lean build
is represented as rerun.

`make_train(gaps, excursions, debris)` constructs a complete finite input and
its exact schedule. Both integer parameter lists must have entries >=100 and
identical lengths. Debris must satisfy x+y<0. Rejected inputs are outside this
certificate class, not counterexamples to HC. Even 10^60-scale parameters use
exact integer coordinates; the literal simulator is not run for such durations.
