# Prediction, complete history and remote feedback

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

[Fresh checks](evidence/review-2026-10-15.json) replay all five modules. The old
stale-memory report contains an attached blank-created-memory annotation that
its checker does not generate; comparison excludes that named annotation and
records it explicitly. No assertion of a fresh replay of that attachment is made.
The original reports and proof notes remain unchanged as provenance.
