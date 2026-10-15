# Exact first-J10 macros

All-input exact next-event computation, complete finite XOR histories, and a bounded-fold finite graph. Canonical proof: `proof/results/ten-event-macros.md` from the repository root.

Run `python scripts/check_ten_event_macro.py` at the repository root, or `python reproduce.py` here. Python standard library and a C++17 compiler are required. The replay works in a disposable copy. It imports the unchanged `../factor_language/ten` source core and its two hash-pinned finite input witnesses; it does not rerun unrelated proofs.

`macro.next_event(X)` returns exact `time` and `post_state`, or `time=None` with a certified standard `tail_word` and `tail_offset`. `X` is a complete finite XOR-segment state, not a deleted active core. `same_complete_state` compares the represented whole fields even when expression lists differ. Strides 2 and 4 on an axis require epoch congruence classes; those holes must not be filled.

The 7595-vertex/7763-edge lift has five simple cyclic components. One call uses at most 1111 literal updates and five plans, adding at most 1530 terms. Conditional on an event, the full macro has a 1959-cell convex-hull halo. Conditional on n events, post-nth time is at most `n*(212*W+854199)+415308*n*(n-1)`.

`witness.json` fixes the complete new graph/rank hashes; `attempt.json` retains a finite counterexample to a failed 116-step memory shortcut. `checked_report.json` records the successful dedicated replay, including negative controls. These are not a proof that arbitrary repeated calls terminate. HC remains unproved.
