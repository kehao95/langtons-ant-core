# Complete-state symbolic stale-event macros

See `PROOF.md` for exact finite XOR-segment semantics, ray intersection parity, complete endpoint identity, term-growth bound, finite event-prefix complexity, and the missing infinite-iteration conclusion.

```sh
python check_symbolic.py
```

```python
from memory_delay import State
from symbolic_stale import SymbolicState, event_prefix, state_data
result = event_prefix(SymbolicState.explicit(State(frozenset())), D=8, n=20)
encoded_complete_endpoint = state_data(result['state'])
print(result['kind'], result['elapsed'])
```

`event_budget_reached` means the requested FINITE prefix is complete, not an infinite-run classification. `permanent_no_stale` supplies a genuine translating future for this D. Caller-imposed caps yield only `inconclusive`. The generic prescribed-write helper is not a proof that an arbitrary proposed word is executable.

The huge example and its full compressed endpoint digest are in `huge_recipe.json`. Its 104000000000000-update event is found with 104 explicitly replayed updates; 1068 terms retain all finite history and can be used for the next event. This is exact arithmetic acceleration, not a claim to have run that many individual updates.
