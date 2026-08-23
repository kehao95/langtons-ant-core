# Lean core

This directory is a clean-room, intentionally narrow Lean 4.30.0 project. It
formalizes the state convention, elementary turn laws, the one-step rule, and
its quarter-turn rotation and translation symmetries used by the Python
reference model. Those symmetry relations are also lifted to every finite
number of updates. It does not yet formalize the finite P104 witness, the
one-black prefix, or the global Highway Conjecture.

The pinned toolchain declaration is `lean-toolchain`. On this machine the local
toolchain is under `/home/kehao95/workspace/.tmp-langtons-ant-lean-v4.30.0/`.
When Lean is on `PATH`, run `lake build` from this directory. During incremental
work, compile only the changed module rather than replaying a broad closure.
