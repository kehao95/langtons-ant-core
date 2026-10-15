# Factor rigidity and mass–defect balance

[Ten-factor proof](proof/ten.md) owns the 150-window coverage, the non-simple
component and its all-parameter foldback exclusion, finite-mass attraction,
sharp slope, infinite-background nine-factor example and intrinsic J10 decider.
[Exact event macros](proof/ten-event-macros.md) adds a bounded-fold lift with
7,595 vertices and 7,763 edges, exact first-event time/full endpoint, and
`s_n <= n*(212W+854199)+415308*n*(n-1)`. It uses the already proved
finite-word foldback obstruction, not a transfer of S_D budgets.
The runtime import changes only the sibling path to `ten/`; original and
adapted hashes are recorded separately.

[Mass proof](proof/mass.md) independently owns the finite-word 300-window graph,
integer potential, sharp 90-step witness and deletion-of-bad-endpoints argument.
The mass proof does not require an infinite legal extension or the attraction theorem.

The current [manuscript](paper/main.tex) combines these arguments in that order.
[Fresh exact checks](evidence/review-2026-10-15.json) compare Python/C++ kernels
and reject damaged certificates. Old immediate 21/14/13 thresholds are excluded
until their complete proof sources and certificates can be imported.
