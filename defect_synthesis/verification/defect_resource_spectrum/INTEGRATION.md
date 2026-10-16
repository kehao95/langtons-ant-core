# Concurrent-source integration and attribution

The mathematical starting point of this package is commit
`2f6010a6bbccf5d342648f1c730a8bd2ea628961`.

During this session, `efe22a9f551b1c1670bf5741013beec11d3c8041` independently
committed `proof/results/presburger-defect-reachability.md` and the
`experiments/hc_global/presburger_defects` implementation. Its all-coordinate
bounded-defect theorem, complete endpoint relation, piecewise-affine event time
and computable minimum root-cost sequence agree with the corresponding
statements here. They are the SAME project results, not a second novelty claim.
The original proposal at c385197 was explicitly read and credited by both works.

This package supplies a separately written relation-subtraction implementation,
its comparison with lexicographic minimization, a fresh complete flat-cover
reconstruction, and the following additional resource refinement: for every
supplied finite bounded-power schema, minimum first-black cardinality AND
contained-defect count form an effective piecewise rational-affine spectrum.
The two-fold domain n>=1, 0<=m<n and exact cost 5n+5m+47 are checked on the whole
parameter domain, using explicit first-read time sets. These are not consequences
of checking finitely many sample parameters. The six-page manuscript presents
one unified theory, not a separate duplicate publication of the common corollary.

The two implementations share the libisl/GMP backend, so they are not independent
proof-producing arithmetic kernels. Only THIS package's tests were run here;
we read the parallel proof, but do not claim to have rerun its entire test suite.
No previous source, earlier lemma, public core manuscript or DOI is overwritten.
No general positive-N all-coordinate supercover was exhaustively executed.
The symbolic counting theorem is proved constructively; an optimized generic
symbolic counting partition is not implemented. HC and root-cost divergence
remain open in this package.
