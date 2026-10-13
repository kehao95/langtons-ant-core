# One-black verification

The proof fixes the blank-highway word at update 9977 and derives complete
future observation equality with a translation/quarter-turn placement of
that state. It covers every one-black position and ant pose, through 22 affine
frontier channels, 21 ordinary classes and the phase-72 reverse channel.
The 702-cell physical history is retained by the isolation arguments.

## Reproduce

Run `python3 one_black/reproduce.py` from the repository root. The script
copies the Lean sources into a new directory without a `.lake` cache, builds
both final targets under Lean 4.30.0, rejects proof placeholders and explicit
axiom declarations, records source hashes, and audits both final axiom lists.

| Evidence | Role |
|---|---|
| [report.json](report.json) | Toolchain, clean-build status and all 43 Lean source hashes |
| [clean-build.log](clean-build.log) | Full fresh-build output |
| [axioms.log](axioms.log) | Dependencies of the universal and standard-trace theorems |

Both final theorems depend on `propext`, `Classical.choice`, `Quot.sound` and
three native computation leaves:

- `Highway.checks_pass._native.native_decide.ax_1_1`
- `PrefixLeaf.verified._native.native_decide.ax_1_1`
- `ScatteringLeaf.verified._native.native_decide.ax_1_1`

The native compiler/runtime is therefore part of the trusted computation.
The standard-trace bridge adds no axiom. Witness generation is separate from
verification: the verifier checks the committed finite witnesses directly.

## Scope

The formal endpoint is
`OneBlack.universal_one_black_standard_trace`: for every exactly-one-black
state, some iterate has the complete standard future read trace. Unlimited
channel depth is covered by induction, with finite replay at the anchors.

The [proof narrative](../PROOF.md) follows the Lean dependency graph;
[release provenance](../release/README.md) identifies the published snapshot.
The earlier semantic comparison and editorial audits remain in the
[pre-reorganization history](https://github.com/kehao95/langtons-ant-core/tree/09acf26205e9f602957fc83216eef38c12307eaa/preprint).
