# Factor rigidity and mass–defect balance

## Finite-interval bounds

| Claim | Universal bridge | Executable support |
|---|---|---|
| [Single finite standard core and supply bound](proof/silent-supply-rigidity.md) | Ordered finite-fold cover; 44-cell transverse overlap; full-field XOR cofactor inequality; common normal | `verification/silent_supply`: two complete enumerations, component order, phase supplies, 174 complete endpoints and huge-coordinate parity |
| [Nine-factor mass bound and minimal window](proof/nine-factor-mass-bound.md) | Every finite path projects to checked forbidden-word product; potentials telescope through the full condensation; all-n ray truncation defeats eight | `verification/nine_mass`: 164,283 words, 9,550 edge inequalities and the finite counterfamily |

## Arithmetic and feedback constructions

The construction gives [silent archive manufacture](proof/silent-archive-amplification.md):
a complete `(10n+41)`-black family produces `2(n+1)` lifetimes during a
J10-free prefix and consumes them later at J10 events. The related
[folded ribbon](proof/silent-fold-reset.md) has exact first P104 time
`152n+2527`, total intrinsic count `56n+926`, and reset flip cost at least
`max(0,4m-136)`. Their full-source geometry explains why the S_D endpoint
tube does not transfer to J10. Both families now have complete futures; their seeds, formulas and reset claims remain distinct.

## Recovery and geometry

[Complete archive recovery](proof/silent-archive-recovery.md) closes the future
of the producer family;
`verification/silent_archive_recovery` checks every affine band and infinite tail.
[Silent-axis geometry](proof/silent-axis-return.md) uses the inherited all-parameter
fold obstruction, new mask closure and four integer potentials to cover every
finite legal word. Its constant 43 is a certified bound, not a sharpness claim.
The reproduction entrypoint checks these constructions together with the attraction, event and mass kernels.

## Proof dependencies

[Ten-factor proof](proof/ten.md) owns the 150-window coverage, the non-simple
component and its all-parameter foldback exclusion, finite-mass attraction,
sharp slope, infinite-background nine-factor example and intrinsic J10 decider.
[Exact event macros](proof/ten-event-macros.md) adds a bounded-fold lift with
7,595 vertices and 7,763 edges, exact first-event time/full endpoint, and
`s_n <= n*(212W+854199)+415308*n*(n-1)`. It uses the already proved
finite-word foldback obstruction, not a transfer of S_D budgets.
The runtime uses the sibling `verification/ten/` kernel;
`sources.json` identifies the complete dependency set.

[Mass proof](proof/mass.md) independently owns the finite-word 300-window graph,
integer potential, sharp 90-step witness and deletion-of-bad-endpoints argument.
The mass proof does not require an infinite legal extension or the attraction theorem.

The current [manuscript](paper/main.tex) combines these arguments in that order.
The exact checks compare Python/C++ kernels and reject damaged certificates.
