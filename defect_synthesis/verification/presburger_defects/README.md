# Presburger compiler for complete bounded-power ant traces

The canonical proof is `proof/results/presburger-defect-reachability.md`.
This is a new supplied-schema integer-relation compiler and a complete, extremely
large finite schema generator derived from the retained J10 finite-path theorem.
It does not decide unlimited J10 renewal or prove HC.

Run from the repository root:

```sh
python scripts/check_presburger_defects.py
```

Requirements: Python 3.10+ and the system ISL shared library (for example libisl23).
No Python extension package, SMT service, network access, or bundled binary is
required. The recorded run used isl-0.27-GMP. Missing libraries and arithmetic
failures are errors/UNKNOWN, never negative mathematical answers.

`compiler.py` constructs the exact cell-to-(time,colour) relation. Its first and
last reads give required input bits and full output bits. Same-cell successors
check all cross-block colour alternation. `factor_cases` computes contained-window
counts, including short/zero powers. `cover.py` enumerates a finite supercover
for any supplied defect budget; its full nonzero-budget cover was NOT traversed.
A supplied-schema UNSAT is not an all-schema UNSAT. The guarded driver marks
incomplete coverage UNKNOWN.

The checks include all-parameter fold exclusion, a two-depth fold domain, exact
rail exhaustion with every residual preserved, an all-coordinate infinite-marker
guard, an exact first-defect time relation, and existential elimination of all
initial coordinates for three small supplied-schema mass budgets. A separate
vector implementation checks finite plans and complete states. The toy descriptor
set is fully enumerated; no large global schema search is represented as run.

The reproduction report is compared semantically for integer relations, because
ISL versions may print different but equivalent normal forms. Source hashes and
all non-format data are checked exactly. ISL/GMP and the Python adapter/compiler
are in the computational trust boundary. The physical coverage proof is analytic.

Minimal interactive example (from this directory):

```python
from compiler import *
ctx = Context()
n, m = var('n'), var('m')
schema = Schema(['n', 'm'], [B, Power(A, n), B, Power(A, m), B])
result = compile_schema(schema, ctx)
assert result.feasible.is_empty()  # ALL nonnegative n,m, not a sampled box.
```
