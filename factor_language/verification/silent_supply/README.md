# Silent supply and finite-horizon ballistic rigidity

Every physically feasible finite word with all contained standard ten-factors
has ONE contiguous standard core; at most `114*c+154693` letters lie outside it,
where c is the exact first-read initial-black cost. Its length satisfies

    L <= 52*norm_inf(endpoint-start) + 114*c + 223437.

The displacement coefficient 52 is sharp; the other constants are not asserted
optimal. This is a finite-horizon result for all such words, not a future-language
promise or a proof of all-input HC. The runtime first-J10 query uses one standard
ray-parity plan and O(m+1) ordinary steps on an EXPLICIT complete m-point input.
A compressed description representing huge mass is outside its O(m) guarantee.

## Reproduce

From the repository root:

```sh
python3 factor_language/reproduce.py --new-results-only
```

Python 3.10+ and a C++17 compiler (`g++`) suffice. Use normal Python, not `-O`:
assertions are part of the exact checker. The runner uses a disposable copy,
regenerates the complete finite certificate and compares the frozen report.
The default never rewrites a failed certificate to make it pass. `--generate`
is an explicit development-only mode of `check.py`, not called by the runner.

## Runtime example

```python
import sys
sys.path.insert(0, 'factor_language/verification/silent_supply')
from one_jump import next_defect

result = next_defect({(0, 0)}, head=(0, 0), heading=0)
print(result.status, result.event_time)
# EVENT: event_time is a pre-update index; field/head/heading are AFTER that update.
# NO_FUTURE_DEFECT: field and pose are at elapsed, with a certified standard tail.
# UNKNOWN: an optional user resource cap was reached; not a negative HC answer.
```

`Field.black(point)` queries the complete returned XOR field without expanding
large segments. No black cell is discarded merely because a reference trace misses it.

## Contents and evidence boundaries

`model.py` contains exact integer geometry, full finite XOR fields and the
periodic first-mismatch query. `one_jump.py` is the executable algorithm and does
not import the graph. `graph.py` rebuilds the inherited finite-path cover and
verifies the cycle order and common normal. `independent.cpp` regenerates every
feasible length-150 word and every short-level count with a different enumeration.
`check.py` checks the new supply/cofactor arithmetic, all phase identities,
complete endpoints, huge-coordinate parity equality, and negative controls.

Full proof: [silent-supply-rigidity.md](../../proof/silent-supply-rigidity.md).
The analytic no-three-fold lemma and ten-factor graph coverage are dependencies
recalled in the proof, not established by finite simulation. The analytic proof is not Lean-formalized. No global J10 budget or finite
HC counterexample follows.
