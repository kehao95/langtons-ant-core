# Prediction, complete history and remote feedback

## Arithmetic and feedback constructions

The construction gives [birth-filtered feedback](proof/birth-filtered-feedback.md):
the first remote old lifetime created since the source checkpoint is totally
computable, with exact birth, consumption and complete XOR endpoint. Initially
black coordinates remain eligible after erasure and rebirth. On non-eventually-
translating orbits, uniform deadlines yield `Omega(sqrt(H)/log(H))` late-born
lifetimes at simultaneously growing radius and age. Complexity is polynomial
for fixed D and fixed K on explicit sparse input; the theorem is not uniform
polynomial in binary D or K's diameter.

## Proof dependencies

The proof follows five dependencies in order:

1. [Stale-memory prediction](proof/stale-memory.md): the intrinsic S_D identity,
   finite suffix cycle and exact first mismatch on every sparse finite input.
2. [Symbolic macros](proof/symbolic-stale-macros.md): finite XOR segments,
   arithmetic-progression intersection and exact reusable complete endpoints.
3. [Event geometry](proof/stale-event-geometry.md): the convex halo and quadratic
   finite-event time budget, strengthening the earlier exponential bound.
4. [Remote feedback](proof/remote-stale-feedback.md): endpoint tube, fixed-region
   burst bound, total filtered decision and simultaneous remote/late-born/long-lived consumption.
5. [Twenty-cell circuit](proof/scalable-feedback-circuit.md): all-parameter
   execution, 31 intermediate S_128 reads and exact first P104 entry.

The manuscript uses the current clock bound from version 0.4.0; the retained
remote checker uses the sufficient conservative older bound. Both are stated
explicitly. The code and proof do not exchange S_D, J10 or physical gate budgets.
