# Quantifier-free bounded-defect decisions

An opt-in, exact supplied-schema backend. All coordinates and repeat counts remain
unbounded. Complete initial fields and all writes are retained as finite XOR terms.
It avoids a global same-cell successor relation and avoids zero-power Cartesian
factor-case expansion. See [the complete proof](../../../proof/results/quantifier-free-defect-complexity.md).

**Scope:** loops must restore heading with diagonal stride 2 or axis stride 2/4;
source terms are finite XOR segments with the same strides, or singletons. Source
anchors, lengths and exponents may be affine. Arbitrary quantified Presburger
sources and complete-field target equality are not supported here. The unchanged
older compiler remains available for those broader tasks and for explicit
semilinear domain construction. This module does not enumerate the full N-event
cover or decide HC.

## Reproduction

From the repository root:

```sh
python scripts/check_presburger_fast.py
python experiments/hc_global/presburger_fast/benchmark.py --part factors --output /tmp/factor-times.json
python experiments/hc_global/presburger_fast/benchmark.py --part decisions --output /tmp/decision-times.json
```

Python 3.10+ and system `libz3`/`libisl` are required. No Python third-party module
or binary library is bundled. The recorded environment used Z3 4.13.3.0 and
ISL 0.27 with GMP. The new encoder itself performs no ISL set operations; the
unchanged imported schema syntax loads its original ISL wrapper, which is also
used for old/new comparisons.

The isolated runner pins the two old modules by Git blob, copies only this module
and those dependencies to a temporary directory, checks every new deterministic
section against the frozen report, and never regenerates unrelated old proofs.
Benchmarks are optional and separate: elapsed times are not immutable evidence.

## Small usable example

Run the following from this directory, or place it in a script alongside api.py:

```python
import _paths
from compiler import Schema, Power, var
from stream_qf import Segment
from api import solve_schema

# A finite row of 2*n black sites, origin heading east.
plan = Schema(('nn', 'kk'), [Power('LRRL', var('kk'))], heading=1)
source = (
    Segment((0, 0), (2, 0), var('nn')),
    Segment((1, 0), (2, 0), var('nn')),
)
result = solve_schema(
    plan, source, defects=31,
    where=lambda c: c.eq('nn', 10),
    timeout_ms=10_000,
)
print(result)
```

A SAT answer includes all parameters, exact compressed post-time/post-pose, defect
count and a separate integer replay. No huge repeat is literally expanded.
UNSAT means only that THIS supplied schema and source family have no satisfying
parameters. UNKNOWN includes native limits/errors; it must not be cached as NO.
Malformed or unsupported syntax raises an exception instead of weakening input.

Schema uses `domain='1=1'`; add optional linear Boolean guards with the `where`
Circuit callback. Powered exponents and source lengths are already nonnegative.
Initial singletons are XOR terms: exact-m coordinate-list synthesis must ALSO
impose pairwise distinctness (`distinct_formula` provides that formula).

To obtain a symbolic endpoint colour, build `Encoder`, call `black_at(point)`,
and ONLY THEN export `encoder.c.text()`: queries add circuit nodes. Combine the
returned bit with `encoder.valid` for actual, rather than merely planned, states.
Explicit symbolic semilinear projection is intentionally left to the old backend.

## Complexity and measurements

Physical feasibility has a polynomial-size QF_LIA circuit by finite parity-change
boundaries on read streams. The factor counter is a linear-size shared suffix
DAG, not the previous 2^s zero/positive case list. With unary N and explicit m
coordinate pairs, a complete bounded-defect schema is a polynomial-size guessed
witness, giving the analytic NP upper bound in the proof. This is NOT a polynomial
deterministic solver or an explicit-polynomial-output claim.

The final factor benchmark at 16 independent powers: 65536 old cases versus
1753 DAG nodes; 3.5823 s versus 0.0280 s median, about 128x. At 128 powers the
new factor circuit was built in 0.2163 s with 14691 nodes; the old 2^128 count
is a formula, NOT an executed old run. At 4/8 powers the old counter was faster.
The separate four supplied-schema nonemptiness tests include three local gains
around 1.8-1.9x and one small case where the new solver is slower. The old path
constructs explicit parameter domains/fields, while the new path asks only an
existential decision. No full-global-synthesis speedup is measured.

`report.json` contains correctness controls and source hashes;
`benchmark-*.json` contains timings. Libraries, the new compiler and the inherited
analytic finite-path cover remain explicit trust dependencies. No external review,
Lean formalization, priority claim or HC conclusion is made.

### Exact timer boundaries

Common Schema construction is outside both timers. The old ISL context and source-set
setup are also before its timer; its measured interval starts at compile_schema.
The new interval includes Encoder construction and a fresh solver session.
The corrected benchmark module docstring states this explicitly. Only that
docstring changed after measurement; the reports retain both source hashes and
the equality check of the complete executable AST. Benchmark code is versioned
separately, not treated as a dependency of the mathematical regression checks.
