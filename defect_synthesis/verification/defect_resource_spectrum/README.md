# Effective semilinearity at a fixed Langton-ant defect budget

Research manuscript and exact supplied-schema arithmetic, 15 October 2026.
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

The scholarly draft is `paper/main.tex`; build with pdflatex twice. It is not a
journal submission or a DOI release, and does not change the public core's
existing papers.

## What is new versus inherited

The old project proposal already suggested bounded-defect Presburger synthesis.
This package supplies a concrete exact relation algebra, complete output fields,
a rechecked finite-schema coverage interface, and a piecewise-affine root-cost
theorem. Fixed literal-word lifting, the ten-factor graph, scanner protocols,
and the triple-fold physical obstruction are attributed prior inputs, not new
constructions. The new arithmetic query also determines the exact two-fold
parameter region and its minimum first-black count.

The sources use the known equality `Next=C minus C composed with C`; all read
and write chronology is retained. The implementation and libisl are in the
computational trust boundary. Two libisl formulations are NOT two independently
refereed proofs. Independent literal finite tests supplement the written proof.

Concurrent proof `efe22a9f` is preserved; see `INTEGRATION.md`. The shared
fixed-budget corollary is one result. The additional schema resource spectrum
and exact two-fold cost are recorded separately, with no HC closure claim.
