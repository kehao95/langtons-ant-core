# Effective semilinearity at a fixed Langton-ant defect budget

Exact supplied-schema arithmetic and its proof.
Read **PROOF.md** before interpreting the outputs. The main corollary covers
all initial coordinates at every fixed mass/event budget; it does not supply
a bound on total events or decide the whole Highway Conjecture.

## Reproduce

```sh
python reproduce.py
python reproduce.py --quick
```

Python 3.10+ and a discoverable shared **libisl** are required (the retained run:
`isl-0.27-GMP`). No Python isl package, SMT solver, floating-point optimizer or
network is used. Full replay includes two exact successor formulations of the
all-parameter fold examples and an independent reconstruction of the inherited
flat ten-factor cover. It compares deterministic results, not timings.

A backend/library error is not a negative answer. A schema-generator resource
cap is INCONCLUSIVE. The full universal `E[m,N]` disjunction has NOT been expanded
for a nontrivial budget. The current runtime computes exact time sets and fixed
integer count thresholds; the general piecewise-affine counting theorem is
proved constructively, not claimed as an optimized runtime counting backend.

## Construction and dependencies

The kernel supplies exact relation algebra, complete output fields, finite-schema
coverage and a piecewise-affine root-cost theorem. The ten-factor graph and
triple-fold obstruction are attributed inputs; see the bundled
[ten-factor proof](../../proof/ten-factor-attraction.md) and
[event-macro proof](../../proof/ten-event-macros.md).

The sources use the known equality `Next=C minus C composed with C`; all read
and write chronology is retained. The implementation and libisl are in the
computational trust boundary. Two libisl formulations are NOT two independently
refereed proofs. Independent literal finite tests supplement the written proof.
