# Exact fixed-schema query optimizations

Research baseline: `6afea97c2a8a26d03b2bf89de9d23a87d64a31e0`.
The two imported baseline Python files are SHA256-pinned and unchanged.
This opt-in backend changes neither the full physical state nor global schema
coverage. No HC theorem, new all-coordinate exclusion, or global runtime bound.

## What changes

`FastSchema.cardinality_at_most(times, m)` replaces the `(m+1)`-tuple product by
binary powers of a strict-order relation on ONE integer time coordinate. For
m>=1 a fresh query needs floor(log2 m)+popcount(m)-1 relation compositions;
each stored relation has one input and one output time coordinate. Parameters
and ISL's internal elimination variables are not included in that dimension
count. `CountQuery(schema, times)` reuses squared relations across thresholds.

`FastSchema.defect_times(L10)` evaluates a reduced Boolean decision DAG. For
the 84 standard ten-factors it uses 117 nonterminal nodes, 183 mask intersections
instead of 840, and 66 mask unions instead of 84. Every node is exactly coalesced
to prevent intermediate disjunction blow-up. The other Schema methods, including
complete endpoint construction, are inherited without alteration.

From the repository root:

```python
from experiments.hc_global.defect_compiler_optimization.fast import FastSchema, Aff, Block, CountQuery
```

`FastSchema` is an opt-in replacement for `defect_resource_spectrum`'s Schema;
the pinned baseline backend remains available for comparison.
Unbounded coordinate/loop parameters stay symbolic. An integer threshold is not
an affine threshold variable. Multidimensional fibres are explicitly rejected.
Arithmetic failures and caps remain exceptions/INCONCLUSIVE, never UNSAT.

## Reproduction and measurements

```sh
python3 defect_synthesis/reproduce.py
python3 defect_synthesis/verification/defect_compiler_optimization/benchmark.py --repeats 5 --timeout 10 --output /tmp/defect-opt-benchmark.json
```

Python 3.10+, Linux for RSS/benchmark limits, and system libisl/GMP are required;
measured backend is isl-0.27-GMP. Default replay is deterministic and disposable.
Benchmark times are not byte-reproducible claims. The committed benchmark report
losslessly deduplicates repeated outputs/operation counts; all individual timing
and peak-RSS measurements remain. `--case-index 0` through `7` runs one case.

Completed pairs have exact integer-set output equality. Symbolic standard/fold/
marker correctness also has direct expected-set checks and an exhaustive Boolean
truth table; a timed-out original standard matcher is not claimed to have passed.
Timing is for the named query, excluding common schema construction. Peak RSS is
for the entire fresh worker, not additional query memory. Count speedups are NOT
end-to-end global solver speedups. See [proof and scope](../../proof/defect-compiler-optimization.md).
